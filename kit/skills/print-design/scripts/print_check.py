#!/usr/bin/env python3
"""print_check.py: check a mesh before it goes to a 3D printer.

Reads STL (binary or ASCII) and 3MF. Reports size, volume, watertightness, non-manifold edges,
flipped or mixed normals, degenerate triangles, the share of surface that overhangs past a limit,
and whether the part fits a printer's build volume.

Commands:
  check     Check one mesh file. Exit 1 on a blocking finding.
  printers  List the printer profiles in references/printers.json.

Exit codes: 0 pass, 1 findings, 2 usage or an unreadable file.
Standard library only. No network. Writes nothing.
"""
import argparse
import json
import math
import os
import re
import struct
import sys
import zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PRINTERS = os.path.normpath(os.path.join(HERE, "..", "references", "printers.json"))
UNIT_MM = {"micron": 0.001, "millimeter": 1.0, "centimeter": 10.0, "inch": 25.4, "foot": 304.8, "meter": 1000.0}
MAX_TRIANGLES = 5_000_000
MAX_3MF_BYTES = 512 * 1024 * 1024
EPS_AREA = 1e-9
PLATE_TOL = 0.05


class MeshError(Exception):
    pass


# ---------------------------------------------------------------- loading

def _key(v):
    return (round(v[0], 6), round(v[1], 6), round(v[2], 6))


def from_triangle_soup(tris):
    """Weld a list of (a, b, c) vertex triples into (vertices, faces)."""
    index, verts, faces = {}, [], []
    for tri in tris:
        face = []
        for v in tri:
            k = _key(v)
            if k not in index:
                index[k] = len(verts)
                verts.append(k)
            face.append(index[k])
        faces.append(tuple(face))
    return verts, faces


def load_stl(data):
    if len(data) >= 84:
        count = struct.unpack("<I", data[80:84])[0]
        if 84 + count * 50 == len(data):
            if count > MAX_TRIANGLES:
                raise MeshError("more than %d triangles" % MAX_TRIANGLES)
            tris = []
            for i in range(count):
                off = 84 + i * 50 + 12
                vals = struct.unpack("<9f", data[off:off + 36])
                tris.append((vals[0:3], vals[3:6], vals[6:9]))
            return from_triangle_soup(tris)
    try:
        text = data.decode("utf-8", "replace")
    except Exception as exc:  # pragma: no cover
        raise MeshError("cannot decode STL: %s" % exc)
    if not text.lstrip().lower().startswith("solid"):
        raise MeshError("not a binary STL of the right length and not an ASCII STL")
    nums = re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", text)
    if len(nums) % 3:
        raise MeshError("ASCII STL has a vertex count that is not a multiple of three")
    if len(nums) // 3 > MAX_TRIANGLES:
        raise MeshError("more than %d triangles" % MAX_TRIANGLES)
    try:
        pts = [tuple(float(x) for x in n) for n in nums]
    except ValueError:
        raise MeshError("ASCII STL holds a vertex that is not a number")
    return from_triangle_soup([(pts[i], pts[i + 1], pts[i + 2]) for i in range(0, len(pts), 3)])


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def load_3mf(path):
    """Read every mesh in every model part of a 3MF package, in millimeters."""
    try:
        zf = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise MeshError("not a 3MF package (not a zip file)")
    with zf:
        total = sum(i.file_size for i in zf.infolist())
        if total > MAX_3MF_BYTES:
            raise MeshError("3MF package unpacks to more than %d bytes" % MAX_3MF_BYTES)
        parts = [n for n in zf.namelist() if n.lower().endswith(".model") and not n.startswith("/")
                 and ".." not in n.split("/")]
        if not parts:
            raise MeshError("3MF package holds no .model part")
        tris = []
        for name in parts:
            try:
                root = ET.fromstring(zf.read(name))
            except ET.ParseError as exc:
                raise MeshError("cannot parse %s: %s" % (name, exc))
            scale = UNIT_MM.get(root.get("unit", "millimeter"), None)
            if scale is None:
                raise MeshError("unknown unit '%s' in %s" % (root.get("unit"), name))
            for mesh in root.iter():
                if _local(mesh.tag) != "mesh":
                    continue
                verts = []
                for child in mesh:
                    if _local(child.tag) == "vertices":
                        for v in child:
                            verts.append((float(v.get("x")) * scale, float(v.get("y")) * scale,
                                          float(v.get("z")) * scale))
                for child in mesh:
                    if _local(child.tag) == "triangles":
                        for t in child:
                            try:
                                a, b, c = int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))
                                tris.append((verts[a], verts[b], verts[c]))
                            except (TypeError, ValueError, IndexError):
                                raise MeshError("a triangle in %s names a vertex that does not exist" % name)
                if len(tris) > MAX_TRIANGLES:
                    raise MeshError("more than %d triangles" % MAX_TRIANGLES)
        if not tris:
            raise MeshError("3MF package holds no triangles")
        return from_triangle_soup(tris)


def load_mesh(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".3mf":
        return load_3mf(path)
    if ext == ".stl":
        with open(path, "rb") as handle:
            return load_stl(handle.read())
    raise MeshError("unsupported file type '%s': use .stl or .3mf" % ext)


# ---------------------------------------------------------------- geometry

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def analyze(verts, faces, overhang_deg=45.0):
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    bbox_min = (min(xs), min(ys), min(zs))
    bbox_max = (max(xs), max(ys), max(zs))
    size = tuple(round(bbox_max[i] - bbox_min[i], 3) for i in range(3))
    edges, directed = {}, {}
    volume6, area, degenerate, overhang_area = 0.0, 0.0, 0, 0.0
    limit = -math.cos(math.radians(overhang_deg))
    zmin = bbox_min[2]
    for f in faces:
        a, b, c = verts[f[0]], verts[f[1]], verts[f[2]]
        n = cross(sub(b, a), sub(c, a))
        twice = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
        if twice / 2.0 < EPS_AREA or len(set(f)) < 3:
            degenerate += 1
            continue
        area += twice / 2.0
        volume6 += a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
        nz = n[2] / twice
        on_plate = max(a[2], b[2], c[2]) - zmin <= PLATE_TOL
        if nz < limit and not on_plate:
            overhang_area += twice / 2.0
        for i in range(3):
            u, v = f[i], f[(i + 1) % 3]
            key = (min(u, v), max(u, v))
            edges[key] = edges.get(key, 0) + 1
            directed[(u, v)] = directed.get((u, v), 0) + 1
    boundary = sum(1 for c in edges.values() if c == 1)
    non_manifold = sum(1 for c in edges.values() if c > 2)
    misoriented = sum(1 for (u, v), c in edges.items()
                      if c == 2 and (directed.get((u, v), 0) != 1 or directed.get((v, u), 0) != 1))
    volume = volume6 / 6.0
    return {
        "triangles": len(faces), "vertices": len(verts),
        "bboxMin": [round(x, 3) for x in bbox_min], "bboxMax": [round(x, 3) for x in bbox_max],
        "sizeMm": list(size), "volumeMm3": round(abs(volume), 3), "areaMm2": round(area, 3),
        "watertight": boundary == 0 and non_manifold == 0,
        "boundaryEdges": boundary, "nonManifoldEdges": non_manifold,
        "misorientedEdges": misoriented, "degenerateTriangles": degenerate,
        "inverted": volume < 0, "overhangDeg": overhang_deg,
        "overhangShare": round(overhang_area / area, 4) if area else 0.0,
        "onPlate": abs(zmin) <= PLATE_TOL,
    }


def fit(size, volume_xyz, margin=0.0):
    usable = [max(0.0, v - 2 * margin) for v in volume_xyz]
    as_is = all(size[i] <= usable[i] for i in range(3))
    rotated = all(s <= u for s, u in zip(sorted(size), sorted(usable)))
    return {"buildVolume": volume_xyz, "marginMm": margin, "fitsAsOriented": as_is, "fitsRotated": rotated}


def findings_for(report, fit_report=None, overhang_warn=0.10):
    blocking, warnings = [], []
    if report["boundaryEdges"]:
        blocking.append("HOLES: %d open edges; the mesh is not watertight" % report["boundaryEdges"])
    if report["nonManifoldEdges"]:
        blocking.append("NON_MANIFOLD: %d edges are shared by more than two triangles" % report["nonManifoldEdges"])
    if report["degenerateTriangles"]:
        blocking.append("DEGENERATE: %d triangles have no area" % report["degenerateTriangles"])
    if report["misorientedEdges"]:
        blocking.append("NORMALS: %d edges show mixed triangle orientation" % report["misorientedEdges"])
    if report["inverted"]:
        blocking.append("INVERTED: normals point inward (negative volume)")
    if fit_report is not None and not fit_report["fitsRotated"]:
        blocking.append("TOO_BIG: %s mm does not fit %s mm in any axis order; split the part"
                        % (report["sizeMm"], fit_report["buildVolume"]))
    elif fit_report is not None and not fit_report["fitsAsOriented"]:
        warnings.append("ORIENT: the part fits only after a rotation on the plate")
    if report["overhangShare"] > overhang_warn:
        warnings.append("OVERHANG: %.0f%% of the surface overhangs past %g degrees; reorient or plan supports"
                        % (report["overhangShare"] * 100, report["overhangDeg"]))
    if not report["onPlate"]:
        warnings.append("FLOATING: the lowest point is not at z = 0; drop the part to the plate before slicing")
    return blocking, warnings


# ---------------------------------------------------------------- printers

def load_printers(path):
    with open(path, "r", encoding="utf-8") as handle:
        doc = json.load(handle)
    printers = doc.get("printers") if isinstance(doc, dict) else None
    if not isinstance(printers, list):
        raise MeshError("printers file has no 'printers' list")
    return {p["id"]: p for p in printers if isinstance(p, dict) and isinstance(p.get("id"), str)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--printers-file", default=DEFAULT_PRINTERS)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="machine output")
    sub_p = parser.add_subparsers(dest="command")
    p_check = sub_p.add_parser("check", parents=[common], help="check one STL or 3MF file")
    p_check.add_argument("path")
    p_check.add_argument("--printer", help="a printer id from printers.json")
    p_check.add_argument("--volume", nargs=3, type=float, metavar=("X", "Y", "Z"), help="build volume in mm")
    p_check.add_argument("--margin", type=float, default=2.0, help="Default: 2 mm kept clear on each side")
    p_check.add_argument("--overhang", type=float, default=45.0, help="Default: 45 degrees from vertical")
    p_check.add_argument("--overhang-warn", type=float, default=0.10, help="Default: warn above 10%% of surface")
    sub_p.add_parser("printers", parents=[common], help="list printer profiles")
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_usage(sys.stderr)
        return 2

    if args.command == "printers":
        try:
            printers = load_printers(args.printers_file)
        except (OSError, ValueError, MeshError) as exc:
            print("cannot read printers: %s" % exc, file=sys.stderr)
            return 2
        rows = [{"id": p["id"], "name": p.get("name"), "buildVolumeMm": p.get("buildVolumeMm")} for p in printers.values()]
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            for r in rows:
                print("%-24s %-36s %s" % (r["id"], r["name"], r["buildVolumeMm"]))
        return 0

    if not 0 < args.overhang < 90:
        print("--overhang must be between 0 and 90 degrees", file=sys.stderr)
        return 2
    volume = None
    if args.printer:
        try:
            printers = load_printers(args.printers_file)
        except (OSError, ValueError, MeshError) as exc:
            print("cannot read printers: %s" % exc, file=sys.stderr)
            return 2
        if args.printer not in printers:
            print("unknown printer '%s'; run 'printers'" % args.printer, file=sys.stderr)
            return 2
        volume = printers[args.printer].get("buildVolumeMm")
    elif args.volume:
        volume = list(args.volume)
    try:
        verts, faces = load_mesh(args.path)
    except (OSError, MeshError, ValueError) as exc:
        print("cannot read mesh: %s" % exc, file=sys.stderr)
        return 2
    if not faces:
        print("cannot read mesh: no triangles", file=sys.stderr)
        return 2
    report = analyze(verts, faces, args.overhang)
    fit_report = fit(report["sizeMm"], volume, args.margin) if volume else None
    blocking, warnings = findings_for(report, fit_report, args.overhang_warn)
    result = {"path": os.path.basename(args.path), "printer": args.printer, "mesh": report, "fit": fit_report,
              "blocking": blocking, "warnings": warnings, "ok": not blocking}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        m = report
        print("%s: %d triangles, %s mm, %.1f mm3" % (result["path"], m["triangles"], m["sizeMm"], m["volumeMm3"]))
        print("watertight %s, overhang %.0f%% past %g deg" % (m["watertight"], m["overhangShare"] * 100, m["overhangDeg"]))
        if fit_report:
            print("fits %s: as oriented %s, rotated %s" % (fit_report["buildVolume"], fit_report["fitsAsOriented"],
                                                         fit_report["fitsRotated"]))
        for line in blocking:
            print("BLOCK  " + line)
        for line in warnings:
            print("WARN   " + line)
        print("print check: %s" % ("pass" if not blocking else "%d blocking finding(s)" % len(blocking)))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
