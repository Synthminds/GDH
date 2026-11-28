"""Tests for kit/skills/print-design/scripts/print_check.py."""
import contextlib
import importlib.util
import io
import json
import os
import struct
import tempfile
import unittest
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "kit", "skills", "print-design", "scripts", "print_check.py")
PRINTERS = os.path.join(REPO, "kit", "skills", "print-design", "references", "printers.json")

spec = importlib.util.spec_from_file_location("print_check", SCRIPT)
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)


def box(w=10.0, d=10.0, h=10.0, z0=0.0):
    """Twelve outward-facing triangles of an axis-aligned box."""
    v = [(0, 0, z0), (w, 0, z0), (w, d, z0), (0, d, z0), (0, 0, z0 + h), (w, 0, z0 + h), (w, d, z0 + h), (0, d, z0 + h)]
    quads = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    tris = []
    for a, b, c, e in quads:
        tris.append((v[a], v[b], v[c]))
        tris.append((v[a], v[c], v[e]))
    return tris


def flipped(tris):
    return [(a, c, b) for a, b, c in tris]


def binary_stl(tris):
    out = bytearray(b"\0" * 80) + struct.pack("<I", len(tris))
    for a, b, c in tris:
        out += struct.pack("<3f", 0, 0, 0) + struct.pack("<9f", *a, *b, *c) + b"\0\0"
    return bytes(out)


def ascii_stl(tris):
    lines = ["solid t"]
    for a, b, c in tris:
        lines += ["facet normal 0 0 0", "outer loop"] + ["vertex %g %g %g" % p for p in (a, b, c)] + ["endloop", "endfacet"]
    return ("\n".join(lines + ["endsolid t"]) + "\n").encode()


def three_mf(tris, unit="millimeter"):
    verts, faces = pc.from_triangle_soup(tris)
    vx = "".join('<vertex x="%g" y="%g" z="%g"/>' % v for v in verts)
    tx = "".join('<triangle v1="%d" v2="%d" v3="%d"/>' % f for f in faces)
    model = ('<?xml version="1.0"?><model unit="%s" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             '<resources><object id="1" type="model"><mesh><vertices>%s</vertices><triangles>%s</triangles></mesh>'
             '</object></resources><build><item objectid="1"/></build></model>') % (unit, vx, tx)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("3D/3dmodel.model", model)
    return buf.getvalue()


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = pc.main(list(argv))
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


class AnalyzeTests(unittest.TestCase):
    def report(self, tris, **kw):
        verts, faces = pc.from_triangle_soup(tris)
        return pc.analyze(verts, faces, **kw)

    def test_clean_cube(self):
        r = self.report(box())
        self.assertTrue(r["watertight"])
        self.assertEqual((r["boundaryEdges"], r["nonManifoldEdges"], r["misorientedEdges"]), (0, 0, 0))
        self.assertFalse(r["inverted"])
        self.assertAlmostEqual(r["volumeMm3"], 1000.0, places=3)
        self.assertEqual(r["sizeMm"], [10.0, 10.0, 10.0])
        self.assertEqual(r["overhangShare"], 0.0)
        self.assertTrue(r["onPlate"])

    def test_open_box_has_holes(self):
        r = self.report(box()[2:])
        self.assertFalse(r["watertight"])
        self.assertEqual(r["boundaryEdges"], 4)

    def test_flipped_cube_is_inverted(self):
        self.assertTrue(self.report(flipped(box()))["inverted"])

    def test_one_flipped_face_is_misoriented(self):
        tris = box()
        a, b, c = tris[3]
        tris[3] = (a, c, b)
        self.assertGreater(self.report(tris)["misorientedEdges"], 0)

    def test_floating_cube_is_measured_from_its_own_base(self):
        r = self.report(box(z0=5.0))
        self.assertFalse(r["onPlate"])
        self.assertEqual(r["overhangShare"], 0.0)
        _, warnings = pc.findings_for(r)
        self.assertTrue(any(w.startswith("FLOATING") for w in warnings))

    def test_degenerate_triangle(self):
        tris = box() + [((0, 0, 0), (1, 1, 1), (2, 2, 2))]
        self.assertEqual(self.report(tris)["degenerateTriangles"], 1)

    def test_overhang_threshold(self):
        # A cube resting on the plate plus a raised slab: the slab bottom overhangs.
        r = self.report(box() + box(30, 30, 2, z0=20))
        self.assertGreater(r["overhangShare"], 0.0)


class FitAndFindingsTests(unittest.TestCase):
    def test_fit_orientations(self):
        self.assertTrue(pc.fit([250, 10, 10], [256, 256, 256])["fitsAsOriented"])
        f = pc.fit([10, 10, 250], [256, 256, 200])
        self.assertFalse(f["fitsAsOriented"])
        self.assertTrue(f["fitsRotated"])
        self.assertFalse(pc.fit([300, 10, 10], [256, 256, 256])["fitsRotated"])

    def test_margin_shrinks_the_volume(self):
        self.assertFalse(pc.fit([254, 10, 10], [256, 256, 256], margin=2.0)["fitsAsOriented"])

    def test_findings(self):
        verts, faces = pc.from_triangle_soup(box(300, 10, 10))
        rep = pc.analyze(verts, faces)
        blocking, _ = pc.findings_for(rep, pc.fit(rep["sizeMm"], [256, 256, 256]))
        self.assertTrue(any(b.startswith("TOO_BIG") for b in blocking))


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, data):
        path = os.path.join(self.tmp.name, name)
        with open(path, "wb") as handle:
            handle.write(data)
        return path

    def test_binary_and_ascii_stl_agree(self):
        b = pc.load_mesh(self.write("a.stl", binary_stl(box())))
        a = pc.load_mesh(self.write("b.stl", ascii_stl(box())))
        self.assertEqual(len(b[1]), 12)
        self.assertEqual(len(a[1]), 12)
        self.assertEqual(len(b[0]), 8)

    def test_3mf_units(self):
        verts, faces = pc.load_mesh(self.write("in.3mf", three_mf(box(1, 1, 1), unit="inch")))
        r = pc.analyze(verts, faces)
        self.assertEqual(r["sizeMm"], [25.4, 25.4, 25.4])

    def test_bad_files(self):
        with self.assertRaises(pc.MeshError):
            pc.load_mesh(self.write("x.obj", b"o x"))
        with self.assertRaises(pc.MeshError):
            pc.load_mesh(self.write("x.3mf", b"not a zip"))
        with self.assertRaises(pc.MeshError):
            pc.load_mesh(self.write("x.stl", b"garbage that is not a mesh at all"))
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("3D/3dmodel.model", '<model unit="parsec"><resources/></model>')
        with self.assertRaises(pc.MeshError):
            pc.load_mesh(self.write("u.3mf", buf.getvalue()))


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cube = os.path.join(self.tmp.name, "cube.stl")
        with open(self.cube, "wb") as handle:
            handle.write(binary_stl(box(20, 20, 20)))
        self.open_box = os.path.join(self.tmp.name, "open.stl")
        with open(self.open_box, "wb") as handle:
            handle.write(binary_stl(box()[2:]))

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_cube_passes(self):
        code, out, _ = run("check", self.cube, "--volume", "220", "220", "220", "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertTrue(data["ok"])
        self.assertTrue(data["fit"]["fitsAsOriented"])

    def test_open_mesh_blocks(self):
        code, out, _ = run("check", self.open_box, "--json")
        self.assertEqual(code, 1)
        self.assertTrue(any(b.startswith("HOLES") for b in json.loads(out)["blocking"]))

    def test_usage_errors(self):
        self.assertEqual(run()[0], 2)
        self.assertEqual(run("check", os.path.join(self.tmp.name, "missing.stl"))[0], 2)
        self.assertEqual(run("check", self.cube, "--overhang", "95")[0], 2)
        self.assertEqual(run("check", self.cube, "--printer", "no-such-printer")[0], 2)

    def test_every_printer_profile_loads(self):
        printers = pc.load_printers(PRINTERS)
        self.assertGreaterEqual(len(printers), 2)
        for pid, p in printers.items():
            vol = p["buildVolumeMm"]
            self.assertEqual(len(vol), 3, pid)
            self.assertTrue(all(isinstance(v, (int, float)) and 50 <= v <= 1000 for v in vol), pid)
            code, _, _ = run("check", self.cube, "--printer", pid)
            self.assertEqual(code, 0, pid)


if __name__ == "__main__":
    unittest.main()
