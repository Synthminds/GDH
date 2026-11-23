#!/usr/bin/env python3
"""moodboard.py: comparison board and uniqueness check for design directions.

  moodboard.py build <board.json> -o board.html [--google-fonts] [--json]
  moodboard.py diff  <board.json> [--hue-threshold N] [--json]

build renders one self-contained HTML board: the directions side by side,
each with swatches (hex and contrast ratio), a type specimen in real copy,
local reference images, notes and a keep / change / remove table to fill.
The page loads nothing from the network unless --google-fonts is given.

diff reports how far the directions differ: accent hue distance, ground,
type class and layout skeleton from a closed list. It fails when two
directions share palette family, type class and layout skeleton, when their
concepts or adjectives are the same, or when a direction
matches the category norm or a known default look (KNOWN_DEFAULTS).

Python 3.9+, standard library only. No network calls. build writes only the
path given with -o. Exit code 0 on pass, 1 on findings (errors), 2 on a
usage error. --json prints one JSON object on stdout.
"""

import argparse
import html
import json
import math
import os
import re
import sys
from collections import OrderedDict

VERSION = "0.1.0"

HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
SAFE_STACK_RE = re.compile(r"[^A-Za-z0-9 ,'\"_.-]")
LOREM_RE = re.compile(r"lorem\s+ipsum|dolor\s+sit\s+amet|consectetur\s+adipisc", re.I)
COLOR_WORD_RE = re.compile(
    r"\b(?:red|orange|amber|yellow|green|teal|cyan|blue|indigo|violet|purple|magenta|pink|brown|black|white|"
    r"gray|grey|beige|cream|navy|gold|silver|dark|darker|light|lighter|pastel|neon|monochrome)\b", re.I)
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg"}

SPREADS = ("safe", "expected", "outside")
STAGES = ("explore", "refine", "finalize")
TYPE_CLASSES = (
    "humanist-sans", "grotesque-sans", "neo-grotesque-sans", "geometric-sans", "rounded-sans", "condensed-sans",
    "old-style-serif", "transitional-serif", "modern-serif", "slab-serif", "mono", "script", "blackletter",
    "display",
)
PARTS = (
    ("concept", "Concept"),
    ("palette", "Palette"),
    ("type", "Type pairing"),
    ("imagery", "Imagery and texture"),
    ("layout", "Layout and shape"),
    ("motion", "Motion"),
    ("signature", "Signature element"),
    ("sample", "Sample"),
)
# The closed skeleton list of references/directions.md section 5. A coined name hides a clone from diff.
SKELETONS = (
    "centered-stack", "hero-split", "split-screen", "asymmetric-split", "editorial-columns",
    "single-column-longform", "full-bleed-media", "poster-type-led", "sidebar-shell", "chat-thread", "card-list",
    "card-grid", "bento-grid", "object-stack", "table-led", "timeline-rail", "map-led", "canvas-led",
)
# Known default looks, the table of references/directions.md section 6. The tell scan in design-critique holds
# the warm-editorial and night-signal looks in SECOND_WAVE_LOOKS; tests keep the two in step.
# Default: the hue bands are a rule of thumb. id: (name, ground test, accent OKLCH hue bands, type classes, skeletons)
KNOWN_DEFAULTS_DATE = "2026-11-23"
KNOWN_DEFAULTS = OrderedDict([
    ("warm-editorial", ("Warm editorial", "cream", ((20.0, 60.0),),
                        ("old-style-serif", "transitional-serif", "modern-serif"), ("editorial-columns",))),
    ("night-signal", ("Night signal", "near-black", ((15.0, 45.0), (110.0, 150.0)),
                      ("grotesque-sans", "neo-grotesque-sans"), ("split-screen", "asymmetric-split"))),
    ("violet-tech", ("Violet tech", "any", ((265.0, 330.0),), ("geometric-sans",),
                     ("card-grid", "bento-grid", "hero-split", "chat-thread"))),
    ("blue-product", ("Blue product", "white", ((240.0, 270.0),), ("geometric-sans", "neo-grotesque-sans"),
                      ("hero-split", "card-grid", "card-list"))),
])
SIGNATURE_HABIT_RE = re.compile(r"\b(gradient|glass|glassmorphism|frosted|glow|glowing)\b", re.I)
HABIT_NEGATION_RE = re.compile(r"\b(?:no|not|without|never|avoid|instead\s+of)\b(?:\W+\w+){0,3}\W*$", re.I)
CONCEPT_OVERLAP = 0.5   # Default: content-word Jaccard at or above which two concepts state one idea.
STOPWORDS = set("""a an and are as at be by for from has in into is it its of on or that the their this to was
with which who what when where while your our you we they them than then there these those each every one""".split())
FONT_EXT = {".woff2", ".woff", ".ttf", ".otf"}
DEFAULT_HUE_THRESHOLD = 30.0   # Default: degrees of OKLCH hue. A rule of thumb, not a standard.
ACHROMATIC_CHROMA = 0.04
TEXT_RATIO = 4.5
UI_RATIO = 3.0


# ---------------------------------------------------------------- color

def hex_to_rgb(value):
    digits = value.strip().lstrip("#")
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    return tuple(int(digits[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def norm_hex(value):
    return "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in hex_to_rgb(value))


def _linear(channel):
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(hex_a, hex_b):
    la, lb = luminance(hex_to_rgb(hex_a)), luminance(hex_to_rgb(hex_b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def oklch(rgb):
    """Return (lightness, chroma, hue in degrees) in the OKLCH space."""
    r, g, b = (_linear(c) for c in rgb)
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1.0 / 3.0)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1.0 / 3.0)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1.0 / 3.0)
    light = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b2 = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return light, math.hypot(a, b2), math.degrees(math.atan2(b2, a)) % 360.0


def hue_distance(a, b):
    diff = abs(a - b) % 360.0
    return min(diff, 360.0 - diff)


# ---------------------------------------------------------------- helpers

def finding(code, level, path, message, hint):
    return OrderedDict([("code", code), ("level", level), ("path", path), ("message", message), ("hint", hint)])


def has_errors(findings):
    return any(f["level"] == "error" for f in findings)


def text_of(value):
    return value.strip() if isinstance(value, str) else ""


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", text_of(value).lower()).strip("-")


def esc(value):
    return html.escape(str(value), quote=True)


def safe_stack(value):
    return SAFE_STACK_RE.sub("", text_of(value))


def role_map(direction):
    roles = OrderedDict()
    for entry in direction.get("palette") or []:
        if isinstance(entry, dict) and isinstance(entry.get("hex"), str) and HEX_RE.match(entry["hex"].strip()):
            roles.setdefault(slug(entry.get("role")), norm_hex(entry["hex"]))
    return roles


def label_of(direction, index):
    ident = text_of(direction.get("id")) or chr(ord("a") + index)
    return "%s %s" % (ident.upper(), text_of(direction.get("name")) or "(unnamed)")


# ---------------------------------------------------------------- validation

def validate(board, base_dir):
    """Return findings for the board structure, the copy, the contrast pairs and the references."""
    out = []
    if not isinstance(board, dict):
        return [finding("MB_SHAPE", "error", "", "The board file is not a JSON object.",
                        "Start from templates/board.json.")]
    if text_of(board.get("status")).lower() == "template":
        out.append(finding("MB_TEMPLATE", "warning", "status", "The board still has status \"template\".",
                           "Replace the example content with this project and remove the status field."))
    stage = text_of(board.get("stage")).lower()
    if stage not in STAGES:
        out.append(finding("MB_STAGE", "warning", "stage", "The stage is absent or unknown.",
                           "Set stage to explore, refine or finalize. A direction board is an explore round."))
    brief = board.get("brief") if isinstance(board.get("brief"), dict) else {}
    words = brief.get("brandWords") if isinstance(brief.get("brandWords"), list) else []
    if not (text_of(brief.get("subject")) and text_of(brief.get("audience")) and text_of(brief.get("primaryJob"))
            and len([w for w in words if text_of(w)]) == 3):
        out.append(finding("MB_BRIEF", "warning", "brief",
                           "The brief block lacks subject, audience, primary job or three brand words.",
                           "Copy these four lines from design/brief.md. A board with no brief cannot be judged."))
    default = board.get("categoryDefault") if isinstance(board.get("categoryDefault"), dict) else {}
    if not text_of(default.get("description")):
        out.append(finding("MB_CATEGORY_DEFAULT", "error", "categoryDefault.description",
                           "The category norm is not described.",
                           "Write one line: what most products in this category look like today."))
    missing = [k for k in ("accentHex", "typeClass", "layoutSkeleton") if not text_of(default.get(k))]
    if stage == "explore" and missing:
        out.append(finding("MB_DEFAULT_UNSTRUCTURED", "error", "categoryDefault",
                           "At stage explore the category norm lacks %s, so no direction is compared to it."
                           % ", ".join(missing),
                           "Give the norm's accentHex, typeClass and layoutSkeleton from the competitor sheet."))
    if text_of(default.get("layoutSkeleton")) and slug(default.get("layoutSkeleton")) not in SKELETONS:
        out.append(finding("MB_SKELETON", "error", "categoryDefault.layoutSkeleton",
                           "The skeleton \"%s\" is not in the closed list." % text_of(default.get("layoutSkeleton")),
                           "Use one of: %s." % ", ".join(SKELETONS)))
    for key in ("accentHex", "groundHex"):
        if key in default and not (isinstance(default[key], str) and HEX_RE.match(default[key].strip())):
            out.append(finding("MB_HEX", "error", "categoryDefault.%s" % key, "The value is not a hex color.",
                               "Write #rgb or #rrggbb."))

    directions = board.get("directions")
    if not isinstance(directions, list) or not all(isinstance(d, dict) for d in directions):
        out.append(finding("MB_SHAPE", "error", "directions", "directions must be a list of objects.",
                           "Start from templates/board.json."))
        return out
    if not 2 <= len(directions) <= 4:
        out.append(finding("MB_DIRECTION_COUNT", "error", "directions",
                           "The board holds %d direction(s). It needs two to four." % len(directions),
                           "Default: three. Use two when the brand rules are strict. Never more than four."))

    seen_ids, seen_names, hosts, ref_total = set(), set(), set(), 0
    for index, direction in enumerate(directions):
        base = "directions[%d]" % index
        ident, name = slug(direction.get("id")), slug(direction.get("name"))
        if not name:
            out.append(finding("MB_PART_MISSING", "error", base + ".name", "The direction has no name.",
                               "Name the idea in two or three words. Do not name a color."))
        if (ident and ident in seen_ids) or (name and name in seen_names):
            out.append(finding("MB_DUPLICATE_NAME", "error", base, "Two directions share an id or a name.",
                               "Give each direction its own id and name. Keep names stable between rounds."))
        seen_ids.add(ident)
        seen_names.add(name)
        if text_of(direction.get("spread")).lower() not in SPREADS:
            out.append(finding("MB_SPREAD", "warning", base + ".spread", "The spread is absent or unknown.",
                               "Set spread to safe, expected or outside."))

        if not text_of(direction.get("concept")):
            out.append(finding("MB_PART_MISSING", "error", base + ".concept", "The concept sentence is missing.",
                               "Write one sentence that states the idea without naming a color or a font."))
        adjectives = direction.get("adjectives")
        if not (isinstance(adjectives, list) and len(adjectives) == 3 and all(
                isinstance(a, dict) and text_of(a.get("word")) and text_of(a.get("opposite")) for a in adjectives)):
            out.append(finding("MB_ADJECTIVES", "error", base + ".adjectives",
                               "The direction needs exactly three adjectives, each with its opposite.",
                               "Write pairs such as {\"word\": \"exact\", \"opposite\": \"approximate\"}."))

        palette = direction.get("palette")
        if not isinstance(palette, list) or not palette:
            out.append(finding("MB_PART_MISSING", "error", base + ".palette", "The palette is missing.",
                               "List each color with role, name and hex. Include the roles bg and text."))
        else:
            for p_index, entry in enumerate(palette):
                if not (isinstance(entry, dict) and isinstance(entry.get("hex"), str)
                        and HEX_RE.match(entry["hex"].strip())):
                    out.append(finding("MB_HEX", "error", "%s.palette[%d].hex" % (base, p_index),
                                       "The value is not a hex color.", "Write #rgb or #rrggbb."))
                elif not text_of(entry.get("role")):
                    out.append(finding("MB_PALETTE_ROLE", "error", "%s.palette[%d].role" % (base, p_index),
                                       "The color has no role.", "Name the job: bg, text, muted, accent, on-accent."))
            roles = role_map(direction)
            for needed in ("bg", "text"):
                if needed not in roles:
                    out.append(finding("MB_PALETTE_ROLE", "error", base + ".palette",
                                       "The palette has no color with the role \"%s\"." % needed,
                                       "A direction needs a ground and a text color before it can be judged."))
            if "bg" in roles:
                pairs = [("text", "bg", TEXT_RATIO, "error"), ("muted", "bg", TEXT_RATIO, "error"),
                         ("on-accent", "accent", TEXT_RATIO, "error"), ("accent", "bg", UI_RATIO, "warning")]
                for fg, bg, floor, level in pairs:
                    if fg in roles and bg in roles:
                        ratio = contrast(roles[fg], roles[bg])
                        if ratio < floor:
                            hint = "Change one of the two colors until the pair holds %.1f:1." % floor
                            if level == "warning":
                                hint = ("Use this accent for fills only. Do not set text or a control outline "
                                        "in it on this ground.")
                            out.append(finding("MB_CONTRAST", level, base + ".palette",
                                               "%s on %s is %.2f:1. The floor is %.1f:1." % (fg, bg, ratio, floor), hint))

        type_block = direction.get("type") if isinstance(direction.get("type"), dict) else {}
        type_ok = text_of(type_block.get("class")) and all(
            isinstance(type_block.get(k), dict) and text_of(type_block[k].get("family"))
            and text_of(type_block[k].get("stack")) for k in ("display", "body"))
        if not type_ok:
            out.append(finding("MB_PART_MISSING", "error", base + ".type",
                               "The type pairing needs class, display and body, each with family and stack.",
                               "Name the class of the display face and give a CSS stack with a system fallback."))
        elif slug(type_block.get("class")) not in TYPE_CLASSES:
            out.append(finding("MB_TYPE_CLASS", "warning", base + ".type.class",
                               "The type class \"%s\" is not in the board vocabulary." % text_of(type_block.get("class")),
                               "Use one of: %s." % ", ".join(TYPE_CLASSES)))

        for key, what in (("imagery", "imagery treatment"), ("texture", "texture treatment"),
                          ("motion", "motion character"), ("signature", "signature element")):
            if not text_of(direction.get(key)):
                out.append(finding("MB_PART_MISSING", "error", "%s.%s" % (base, key), "The %s is missing." % what,
                                   "Every direction carries the same parts, so that the user can compare them."))
        layout = direction.get("layout") if isinstance(direction.get("layout"), dict) else {}
        if not (text_of(layout.get("skeleton")) and text_of(layout.get("shape"))):
            out.append(finding("MB_PART_MISSING", "error", base + ".layout",
                               "The layout needs a skeleton and a shape language.",
                               "Take the skeleton from the closed list and describe corners, rules and edges."))
        elif slug(layout.get("skeleton")) not in SKELETONS:
            out.append(finding("MB_SKELETON", "error", base + ".layout.skeleton",
                               "The skeleton \"%s\" is not in the closed list." % text_of(layout.get("skeleton")),
                               "Use one of: %s. Put the idea's own name for the layout in layout.notes."
                               % ", ".join(SKELETONS)))
        if type_ok:
            out.extend(font_file_findings(type_block, base, base_dir))
        sample = direction.get("sample") if isinstance(direction.get("sample"), dict) else {}
        if not (text_of(sample.get("headline")) and text_of(sample.get("body"))):
            out.append(finding("MB_PART_MISSING", "error", base + ".sample",
                               "The sample needs a headline and a body line in real copy.",
                               "Take the copy from the brief or the product. One hero or one card is enough."))
        copy = " ".join(text_of(sample.get(k)) for k in ("headline", "body", "cta"))
        if LOREM_RE.search(copy):
            out.append(finding("MB_PLACEHOLDER_COPY", "error", base + ".sample",
                               "The sample holds placeholder Latin text.",
                               "Use real project copy. Mark a missing fact with a bracketed label."))

        for key, what in (("differsFromOthers", "the other directions"), ("differsFromDefault", "the category norm")):
            line = text_of(direction.get(key))
            if not line:
                out.append(finding("MB_DIFFERENCE_LINE", "error", "%s.%s" % (base, key),
                                   "The line that says how this direction differs from %s is missing." % what,
                                   "Write one line. State the difference in idea, structure or behavior."))
            elif key == "differsFromOthers" and COLOR_WORD_RE.search(line):
                out.append(finding("MB_DIFFERENCE_NAMES_COLOR", "warning", "%s.%s" % (base, key),
                                   "The difference line names a color or a tone.",
                                   "A difference in idea can be stated with no color word. Rewrite the line."))

        references = direction.get("references")
        if not isinstance(references, list) or not references:
            out.append(finding("MB_REF_NONE", "warning", base + ".references", "The direction shows no reference.",
                               "Add two or more references from the subject's own world, or say why none exists."))
            references = []
        for r_index, ref in enumerate(references):
            r_path = "%s.references[%d]" % (base, r_index)
            if not isinstance(ref, dict):
                out.append(finding("MB_REF_SOURCE", "error", r_path, "The reference is not an object.",
                                   "Give file, source, license and note."))
                continue
            ref_total += 1
            source, file_name = text_of(ref.get("source")), text_of(ref.get("file"))
            if not source or not text_of(ref.get("license")):
                out.append(finding("MB_REF_SOURCE", "error", r_path, "The reference lacks a source or a license note.",
                                   "Record where it came from and its terms. A reference never ships."))
            host = re.match(r"^[a-z]+://([^/]+)", source.lower())
            hosts.add(host.group(1) if host else source.lower())
            if re.match(r"^(?:[a-z]+:)?//", file_name.lower()) or file_name.lower().startswith("data:"):
                out.append(finding("MB_REF_REMOTE", "error", r_path + ".file",
                                   "The reference file is a remote address or a data URI.",
                                   "Save the image beside board.json and give the local path."))
            elif file_name and not os.path.isfile(os.path.join(base_dir, file_name)):
                out.append(finding("MB_REF_FILE_MISSING", "warning", r_path + ".file",
                                   "The file %s does not exist beside the board file." % file_name,
                                   "Save the reference locally, or remove the file field and keep the note."))
    if ref_total >= 3 and len(hosts) == 1:
        out.append(finding("MB_REF_ONE_SOURCE", "warning", "directions",
                           "All %d references come from one source." % ref_total,
                           "Default: draw on three or more sources. Start in the subject's own world."))

    spreads = [text_of(d.get("spread")).lower() for d in directions]
    if len(directions) >= 3 and not all(s in spreads for s in SPREADS):
        out.append(finding("MB_SPREAD", "warning", "directions",
                           "The board does not hold one safe, one expected and one outside direction.",
                           "Default: one near the current brand, one in between, one outside the safe zone."))
    elif len(directions) == 2 and "outside" not in spreads:
        out.append(finding("MB_SPREAD", "warning", "directions", "Neither of the two directions is marked outside.",
                           "Default: with two directions, make one of them leave the safe zone."))
    return out


def font_files(block):
    files = block.get("files") if isinstance(block, dict) else None
    return [text_of(f) for f in files if text_of(f)] if isinstance(files, list) else []


def font_file_findings(type_block, base, base_dir):
    out = []
    for key in ("display", "body"):
        for f_index, name in enumerate(font_files(type_block.get(key))):
            where = "%s.type.%s.files[%d]" % (base, key, f_index)
            if re.match(r"^(?:[a-z]+:)?//", name.lower()) or name.lower().startswith("data:"):
                out.append(finding("MB_FONT_FILE", "error", where, "The font file is a remote address or a data URI.",
                                   "Save the font beside board.json through find-assets and give the local path."))
            elif os.path.splitext(name)[1].lower() not in FONT_EXT:
                out.append(finding("MB_FONT_FILE", "error", where, "%s is not a woff2, woff, ttf or otf file." % name,
                                   "Give the path of the font file itself."))
            elif not os.path.isfile(os.path.join(base_dir, name)):
                out.append(finding("MB_FONT_FILE", "error", where, "The file %s does not exist beside the board file."
                                   % name, "Save the font file locally, or remove the files field."))
    return out


def font_findings(board, google_fonts):
    """MB_FONT_NOT_LOADED: a named family that the board has no way to load, so the specimen shows a fallback."""
    out = []
    hrefs = [text_of(board.get("googleFontsHref"))]
    for direction in board.get("directions") or []:
        if isinstance(direction, dict) and isinstance(direction.get("type"), dict):
            hrefs.append(text_of(direction["type"].get("googleFontsHref")))
    web = " ".join(h for h in hrefs if h.startswith("https://fonts.googleapis.com/css")).replace("+", " ").lower()
    for index, direction in enumerate(board.get("directions") or []):
        type_block = direction.get("type") if isinstance(direction, dict) and isinstance(direction.get("type"), dict) \
            else {}
        for key in ("display", "body"):
            block = type_block.get(key) if isinstance(type_block.get(key), dict) else {}
            family = text_of(block.get("family"))
            if not family or font_files(block):
                continue
            if google_fonts and "family=%s" % family.lower() in web:
                continue
            out.append(finding("MB_FONT_NOT_LOADED", "warning", "directions[%d].type.%s" % (index, key),
                               "%s has no font file%s, so its specimen shows a fallback face." % (
                                   family, "" if google_fonts else " and the build is offline"),
                               "Add type.%s.files with a local font (license read through find-assets), or build "
                               "with --google-fonts and a googleFontsHref that names it. Tell the user which "
                               "specimens show a fallback face." % key))
    return out


def content_words(text):
    return set(w for w in re.findall(r"[a-z][a-z'-]{2,}", text_of(text).lower()) if w not in STOPWORDS)


def jaccard(a, b):
    return float(len(a & b)) / len(a | b) if a and b else 0.0


def label_free_signals(a, b):
    """Signals that read no labels: concept overlap and the same adjectives."""
    signals = []
    overlap = jaccard(content_words(a.get("concept")), content_words(b.get("concept")))
    if overlap >= CONCEPT_OVERLAP:
        signals.append("concept words (%.0f%% shared)" % (overlap * 100))
    words = [set(text_of(x.get("word")).lower() for x in (d.get("adjectives") or []) if isinstance(x, dict))
             for d in (a, b)]
    if words[0] and words[0] == words[1]:
        signals.append("adjectives")
    # Sample copy is not compared: the board shows every direction with the same real copy on purpose.
    return signals


def ground_kind(bg_hex):
    lightness, chroma, hue = oklch(hex_to_rgb(bg_hex))
    kinds = {"any"}
    if lightness >= 0.9 and 0.008 <= chroma <= 0.06 and 50.0 <= hue <= 110.0:
        kinds.add("cream")
    if lightness <= 0.25:
        kinds.add("near-black")
    if lightness >= 0.97 and chroma < 0.01:
        kinds.add("white")
    return kinds


def known_default_match(direction, metrics):
    """Return (look id, reason) when a direction matches a known default look, else None."""
    roles = role_map(direction)
    signature = text_of(direction.get("signature"))
    for match in SIGNATURE_HABIT_RE.finditer(signature):
        if not HABIT_NEGATION_RE.search(signature[:match.start()]):
            return "violet-tech", "its signature is a %s" % match.group(1).lower()
    if "bg" not in roles or metrics["hue"] is None:
        return None
    grounds = ground_kind(roles["bg"])
    for look, (_name, ground, bands, classes, skeletons) in KNOWN_DEFAULTS.items():
        if ground not in grounds or not any(low <= metrics["hue"] <= high for low, high in bands):
            continue
        if metrics["typeClass"] in classes:
            return look, "palette family and type class"
        if metrics["layoutSkeleton"] in skeletons:
            return look, "palette family and layout skeleton"
    return None


# ---------------------------------------------------------------- analysis

def direction_metrics(direction, index):
    roles = role_map(direction)
    key_hex = roles.get("accent")
    if key_hex is None:
        candidates = [value for role, value in roles.items() if role not in ("bg", "text")] or list(roles.values())
        if candidates:
            key_hex = max(candidates, key=lambda value: oklch(hex_to_rgb(value))[1])
    hue, chroma = None, 0.0
    if key_hex:
        _, chroma, hue = oklch(hex_to_rgb(key_hex))
    achromatic = key_hex is None or chroma < ACHROMATIC_CHROMA
    ground = None
    if "bg" in roles:
        ground = "light" if oklch(hex_to_rgb(roles["bg"]))[0] >= 0.6 else "dark"
    type_block = direction.get("type") if isinstance(direction.get("type"), dict) else {}
    layout = direction.get("layout") if isinstance(direction.get("layout"), dict) else {}
    return OrderedDict([
        ("id", text_of(direction.get("id")) or chr(ord("a") + index)),
        ("name", text_of(direction.get("name"))),
        ("spread", text_of(direction.get("spread")).lower()),
        ("accentHex", key_hex),
        ("hue", None if achromatic else round(hue, 1)),
        ("chroma", round(chroma, 3)),
        ("achromatic", achromatic),
        ("ground", ground),
        ("typeClass", slug(type_block.get("class"))),
        ("layoutSkeleton", slug(layout.get("skeleton"))),
    ])


def same_palette_family(a, b, threshold):
    if a["ground"] is None or b["ground"] is None or a["ground"] != b["ground"]:
        return False, None
    if a["achromatic"] and b["achromatic"]:
        return True, 0.0
    if a["achromatic"] or b["achromatic"]:
        return False, None
    distance = hue_distance(a["hue"], b["hue"])
    return distance < threshold, distance


def analyse(board, threshold=DEFAULT_HUE_THRESHOLD):
    """Return (metrics, pairs, default rows, findings) for the uniqueness test."""
    directions = [d for d in (board.get("directions") or []) if isinstance(d, dict)]
    metrics = [direction_metrics(d, i) for i, d in enumerate(directions)]
    pairs, out = [], []
    for i in range(len(metrics)):
        for j in range(i + 1, len(metrics)):
            a, b = metrics[i], metrics[j]
            family, distance = same_palette_family(a, b, threshold)
            if distance is None and not a["achromatic"] and not b["achromatic"] and a["hue"] is not None \
                    and b["hue"] is not None:
                distance = hue_distance(a["hue"], b["hue"])
            same_type = bool(a["typeClass"]) and a["typeClass"] == b["typeClass"]
            same_layout = bool(a["layoutSkeleton"]) and a["layoutSkeleton"] == b["layoutSkeleton"]
            shared = [name for name, flag in (("palette family", family), ("type class", same_type),
                                               ("layout skeleton", same_layout)) if flag]
            signals = label_free_signals(directions[i], directions[j])
            verdict = "near-identical" if len(shared) == 3 or signals else ("weak" if len(shared) == 2 else "distinct")
            pairs.append(OrderedDict([
                ("a", a["id"]), ("b", b["id"]),
                ("hueDistance", None if distance is None else round(distance, 1)),
                ("sameGround", a["ground"] is not None and a["ground"] == b["ground"]),
                ("samePaletteFamily", family), ("sameTypeClass", same_type), ("sameLayoutSkeleton", same_layout),
                ("shared", shared), ("sameContent", signals), ("verdict", verdict),
            ]))
            where = "directions[%d] and directions[%d]" % (i, j)
            names = "%s and %s" % (label_of(directions[i], i), label_of(directions[j], j))
            if verdict == "near-identical":
                what = "palette family, type class and layout skeleton" if len(shared) == 3 else \
                    "the same %s" % " and ".join(signals)
                out.append(finding("MB_NEAR_IDENTICAL", "error", where, "%s share %s." % (names, what),
                                   "They are one idea in two skins. Replace one with a different idea. "
                                   "Do not only change its color or rename a field."))
            elif verdict == "weak":
                out.append(finding("MB_WEAK_SPREAD", "warning", where,
                                   "%s share %s." % (names, " and ".join(shared)),
                                   "Check that the two ideas differ. Move one of the shared parts."))

    default = board.get("categoryDefault") if isinstance(board.get("categoryDefault"), dict) else {}
    default_rows = []
    d_accent = default.get("accentHex") if isinstance(default.get("accentHex"), str) \
        and HEX_RE.match(default["accentHex"].strip()) else None
    d_ground = default.get("groundHex") if isinstance(default.get("groundHex"), str) \
        and HEX_RE.match(default["groundHex"].strip()) else None
    d_type, d_layout = slug(default.get("typeClass")), slug(default.get("layoutSkeleton"))
    if d_accent and d_type and d_layout:
        _, d_chroma, d_hue = oklch(hex_to_rgb(d_accent))
        ref = {"ground": "light" if not d_ground or oklch(hex_to_rgb(d_ground))[0] >= 0.6 else "dark",
               "achromatic": d_chroma < ACHROMATIC_CHROMA, "hue": d_hue}
        for i, m in enumerate(metrics):
            family, distance = same_palette_family(m, ref, threshold)
            shared = [name for name, flag in (("palette family", family), ("type class", m["typeClass"] == d_type),
                                               ("layout skeleton", m["layoutSkeleton"] == d_layout)) if flag]
            accepted = text_of(directions[i].get("allowCategoryDefault"))
            default_rows.append(OrderedDict([("id", m["id"]),
                                             ("hueDistance", None if distance is None else round(distance, 1)),
                                             ("shared", shared), ("accepted", accepted or None)]))
            if len(shared) == 3 and not accepted:
                out.append(finding("MB_SAME_AS_CATEGORY_DEFAULT", "error", "directions[%d]" % i,
                                   "%s matches the category norm in palette family, type class and layout "
                                   "skeleton." % label_of(directions[i], i),
                                   "Derive the direction from the subject. When the brief asks for the norm, "
                                   "record the reason in allowCategoryDefault."))
    for i, m in enumerate(metrics):
        hit = known_default_match(directions[i], m)
        m["knownDefault"] = hit[0] if hit else None
        if hit and not text_of(directions[i].get("allowCategoryDefault")):
            out.append(finding("MB_KNOWN_DEFAULT", "error", "directions[%d]" % i,
                               "%s matches the known default look '%s' (table of %s): %s." % (
                                   label_of(directions[i], i), KNOWN_DEFAULTS[hit[0]][0], KNOWN_DEFAULTS_DATE, hit[1]),
                               "Derive the palette, face or skeleton from the subject. When the brief asks for this "
                               "look, record the reason in allowCategoryDefault and log it."))
    return metrics, pairs, default_rows, out


# ---------------------------------------------------------------- render

CHROME_CSS = """
*{box-sizing:border-box}
html{font-family:system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;font-size:16px;line-height:1.45;
color:#1c1e21;background:#ecebe7}
body{margin:0;padding:24px}
h1{font-size:1.5rem;margin:0 0 4px}
h2{font-size:1.25rem;margin:0}
h3{font-size:.8125rem;margin:20px 0 6px;text-transform:none;font-weight:700;color:#3d4147}
p{margin:0 0 8px}
.meta{color:#3d4147;max-width:75ch}
.notice{border:1px solid #1c1e21;padding:8px 12px;margin:12px 0 20px;max-width:75ch;background:#fff}
.board{display:grid;grid-template-columns:repeat(var(--n),minmax(320px,1fr));gap:16px;overflow-x:auto;
align-items:start;padding-bottom:8px}
.direction{background:#fff;border:1px solid #c9c8c2;padding:16px;min-width:0}
.tag{display:inline-block;border:1px solid #1c1e21;padding:0 6px;font-size:.75rem;margin-left:6px;
vertical-align:middle}
.concept{font-size:1.0625rem}
.adjectives{list-style:none;padding:0;margin:0 0 8px;display:flex;flex-wrap:wrap;gap:4px 12px}
.sample{padding:28px 20px;border:1px solid #c9c8c2;background:var(--bg);color:var(--text)}
.sample.center{text-align:center}
.sample-headline{margin:0 0 10px;font-size:2rem;line-height:1.1;color:inherit;text-wrap:balance}
.sample-body{margin:0 0 16px;font-size:1rem;line-height:1.5;max-width:44ch}
.sample.center .sample-body{margin-left:auto;margin-right:auto}
.sample-cta{display:inline-block;padding:10px 16px;font-weight:600;background:var(--cta-bg);color:var(--cta-fg);
border-radius:var(--radius)}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:8px;padding:0;margin:0;
list-style:none}
.swatch{border:1px solid #c9c8c2}
.chip{height:44px;border-bottom:1px solid #c9c8c2}
.swatch dl{margin:0;padding:6px 8px;font-size:.8125rem}
.swatch dt{font-weight:700}
.swatch dd{margin:0}
code,.num{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.8125rem}
table{border-collapse:collapse;width:100%;font-size:.8125rem}
th,td{border:1px solid #c9c8c2;padding:4px 6px;text-align:left;vertical-align:top}
th{background:#f5f4f0}
.fail{font-weight:700;color:#8f1d1d}
.pass{color:#1d5c2e}
.specimen{border:1px solid #c9c8c2;padding:12px}
.specimen-display{font-size:2.25rem;line-height:1.1;margin:0 0 8px;text-wrap:balance}
.specimen-body{font-size:1rem;line-height:1.5;margin:0 0 8px;max-width:60ch}
.specimen-nums{font-size:1.25rem;margin:0;font-variant-numeric:tabular-nums}
.refs{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin:0;padding:0}
.refs figure{margin:0;border:1px solid #c9c8c2;padding:6px}
.refs img{display:block;width:100%;height:120px;object-fit:cover;background:#ecebe7}
.refs figcaption{font-size:.75rem;margin-top:4px;overflow-wrap:anywhere}
.kcr input[type=text]{width:100%;min-width:90px;font:inherit;padding:2px 4px;border:1px solid #6b6f76}
.kcr td.pick{text-align:center;width:3.5rem}
.kcr input[type=radio]{width:20px;height:20px}
.panel{background:#fff;border:1px solid #c9c8c2;padding:16px;margin-top:16px;max-width:1100px}
textarea{width:100%;min-height:220px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.8125rem}
button,select{font:inherit;padding:6px 12px;border:1px solid #1c1e21;background:#fff;color:#1c1e21}
button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #0b57d0;
outline-offset:2px}
.findings li{margin-bottom:4px}
.fallback{border:2px solid #8f1d1d;color:#8f1d1d;background:#fff;padding:4px 8px;font-weight:700;margin:0 0 8px}
@media print{body{background:#fff;padding:0}.board{display:block}.direction{break-inside:avoid;margin-bottom:12px}
button{display:none}}
"""

BOARD_JS = """
(function(){
  // Show a banner on each specimen whose named face did not load. A face counts as loaded when text set in it
  // measures differently from both generic fallbacks.
  function loaded(family){
    var c=document.createElement('canvas').getContext('2d');var s='Hamburgefonstiv 0123456789';
    return ['monospace','serif'].some(function(g){
      c.font='40px '+g;var a=c.measureText(s).width;
      c.font='40px "'+family+'",'+g;return c.measureText(s).width!==a;});
  }
  function mark(){
    document.querySelectorAll('[data-check-family]').forEach(function(el){
      el.hidden=loaded(el.getAttribute('data-check-family'));
    });
  }
  if(document.fonts&&document.fonts.ready){document.fonts.ready.then(mark);}else{mark();}
})();
(function(){
  var out=document.getElementById('feedback-text');
  document.getElementById('feedback-make').addEventListener('click',function(){
    var lines=[];
    var base=document.getElementById('base-direction');
    lines.push('Keep / Change / Remove:');
    document.querySelectorAll('tr[data-part]').forEach(function(row){
      var pick=row.querySelector('input[type=radio]:checked');
      var note=row.querySelector('input[type=text]').value.trim();
      if(pick||note){
        lines.push('- '+row.getAttribute('data-direction')+' / '+row.getAttribute('data-part')+': '+
          (pick?pick.value:'no choice')+(note?' ('+note+')':''));
      }
    });
    if(lines.length===1){lines.push('- nothing marked yet');}
    lines.push('Base direction: '+(base.value||'not chosen'));
    var extra=document.getElementById('feedback-extra').value.trim();
    if(extra){lines.push('Missing or other: '+extra);}
    out.value=lines.join('\\n');
    out.focus();out.select();
  });
})();
"""


def render_direction(direction, index, base_dir, out_dir, sample_copy):
    ident = text_of(direction.get("id")) or chr(ord("a") + index)
    name = text_of(direction.get("name")) or "(unnamed)"
    roles = role_map(direction)
    bg, text = roles.get("bg", "#ffffff"), roles.get("text", "#111111")
    cta_bg = roles.get("accent", text)
    cta_fg = roles.get("on-accent", bg if "accent" not in roles else
                       ("#ffffff" if contrast("#ffffff", cta_bg) >= contrast("#000000", cta_bg) else "#000000"))
    layout = direction.get("layout") if isinstance(direction.get("layout"), dict) else {}
    radius = layout.get("radiusPx")
    radius = max(0.0, min(64.0, float(radius))) if isinstance(radius, (int, float)) and not isinstance(radius, bool) \
        else 0.0
    type_block = direction.get("type") if isinstance(direction.get("type"), dict) else {}
    display = type_block.get("display") if isinstance(type_block.get("display"), dict) else {}
    body = type_block.get("body") if isinstance(type_block.get("body"), dict) else {}

    def font_style(block):
        stack = safe_stack(block.get("stack")) or "system-ui, sans-serif"
        weight = block.get("weight")
        weight = int(weight) if isinstance(weight, (int, float)) and not isinstance(weight, bool) \
            and 1 <= weight <= 1000 else 400
        return "font-family:%s;font-weight:%d" % (stack, weight)

    sample = direction.get("sample") if isinstance(direction.get("sample"), dict) else {}
    headline = text_of(sample.get("headline")) or text_of(sample_copy.get("headline"))
    body_copy = text_of(sample.get("body")) or text_of(sample_copy.get("body"))
    cta = text_of(sample.get("cta")) or text_of(sample_copy.get("cta"))
    align = "center" if text_of(sample.get("align")).lower() == "center" else "left"

    parts = []
    parts.append('<article class="direction" aria-labelledby="dir-%s" style="--bg:%s;--text:%s;--cta-bg:%s;'
                 '--cta-fg:%s;--radius:%gpx">' % (esc(slug(ident)), bg, text, cta_bg, cta_fg, radius))
    spread = text_of(direction.get("spread")).lower()
    parts.append('<h2 id="dir-%s">%s %s%s</h2>' % (
        esc(slug(ident)), esc(ident.upper()), esc(name),
        '<span class="tag">%s</span>' % esc(spread) if spread else ""))
    parts.append('<p class="concept">%s</p>' % esc(text_of(direction.get("concept"))))
    adjectives = [a for a in (direction.get("adjectives") or []) if isinstance(a, dict)]
    if adjectives:
        parts.append('<ul class="adjectives">%s</ul>' % "".join(
            "<li><strong>%s</strong>, not %s</li>" % (esc(text_of(a.get("word"))), esc(text_of(a.get("opposite"))))
            for a in adjectives))

    parts.append("<h3>Sample (%s, real copy)</h3>" % esc(text_of(sample.get("kind")) or "hero"))
    parts.append('<div class="sample %s">' % align)
    parts.append('<p class="sample-headline" style="%s">%s</p>' % (esc(font_style(display)), esc(headline)))
    parts.append('<p class="sample-body" style="%s">%s</p>' % (esc(font_style(body)), esc(body_copy)))
    if cta:
        parts.append('<span class="sample-cta" style="%s">%s</span>' % (esc(font_style(body).split(";")[0]), esc(cta)))
    parts.append("</div>")
    sample_file = text_of(sample.get("file"))
    if sample_file and not re.match(r"^(?:[a-z]+:)?//|^data:", sample_file.lower()):
        rel = os.path.relpath(os.path.join(base_dir, sample_file), out_dir).replace(os.sep, "/")
        parts.append('<p>Built sample: <a href="%s">%s</a></p>' % (esc(rel), esc(sample_file)))

    parts.append("<h3>Palette</h3>")
    parts.append('<ul class="swatches">')
    for entry in direction.get("palette") or []:
        if not (isinstance(entry, dict) and isinstance(entry.get("hex"), str) and HEX_RE.match(entry["hex"].strip())):
            continue
        value = norm_hex(entry["hex"])
        ratio = contrast(value, bg)
        role = slug(entry.get("role"))
        if role == "bg":
            note = "ground"
        elif role == "on-accent" and "accent" in roles:
            on_ratio = contrast(value, roles["accent"])
            note = "%.2f:1 on accent, %s" % (on_ratio, "text" if on_ratio >= TEXT_RATIO else "below the text floor")
        elif ratio >= TEXT_RATIO:
            note = "%.2f:1 on bg, text" % ratio
        elif ratio >= UI_RATIO:
            note = "%.2f:1 on bg, large text and UI only" % ratio
        else:
            note = "%.2f:1 on bg, fills only" % ratio
        parts.append('<li class="swatch"><div class="chip" style="background:%s"></div><dl><dt>%s</dt>'
                     '<dd>%s</dd><dd><code>%s</code></dd><dd class="num">%s</dd></dl></li>'
                     % (value, esc(text_of(entry.get("role"))), esc(text_of(entry.get("name"))), value, esc(note)))
    parts.append("</ul>")
    rows = []
    for fg, ground, floor in (("text", "bg", TEXT_RATIO), ("muted", "bg", TEXT_RATIO),
                              ("on-accent", "accent", TEXT_RATIO), ("accent", "bg", UI_RATIO)):
        if fg in roles and ground in roles:
            ratio = contrast(roles[fg], roles[ground])
            ok = ratio >= floor
            verdict, css = ("pass", "pass") if ok else ("FAIL", "fail")
            if not ok and fg == "accent":
                verdict, css = "fills only", ""
            rows.append('<tr><td>%s on %s</td><td class="num">%.2f:1</td><td class="num">%.1f:1</td>'
                        '<td class="%s">%s</td></tr>' % (fg, ground, ratio, floor, css, verdict))
    if rows:
        parts.append('<table><caption class="meta">Contrast pairs</caption><thead><tr><th>Pair</th><th>Ratio</th>'
                     '<th>Floor</th><th>Result</th></tr></thead><tbody>%s</tbody></table>' % "".join(rows))

    parts.append("<h3>Type pairing</h3>")
    parts.append('<p>Class: <code>%s</code>. Display: %s. Body: %s.%s</p>' % (
        esc(text_of(type_block.get("class"))), esc(text_of(display.get("family"))), esc(text_of(body.get("family"))),
        " Source: %s." % esc(text_of(type_block.get("source"))) if text_of(type_block.get("source")) else ""))
    parts.append('<div class="specimen">')
    for block in (display, body):
        family = safe_stack(block.get("family")).replace('"', "").replace("'", "")
        if family:
            parts.append('<p class="fallback" data-check-family="%s" hidden>Fallback face shown: %s did not load. '
                         'Do not choose type from this specimen.</p>' % (esc(family), esc(family)))
    parts.append('<p class="specimen-display" style="%s">%s</p>' % (esc(font_style(display)), esc(headline)))
    parts.append('<p class="specimen-body" style="%s">%s</p>' % (esc(font_style(body)), esc(body_copy)))
    parts.append('<p class="specimen-nums" style="%s">0123456789 7:40 08:10 12.5%%</p>' % esc(font_style(body)))
    parts.append("</div>")

    parts.append("<h3>Imagery and texture</h3>")
    parts.append("<p>%s</p><p>%s</p>" % (esc(text_of(direction.get("imagery"))), esc(text_of(direction.get("texture")))))
    figures = []
    for ref in direction.get("references") or []:
        if not isinstance(ref, dict):
            continue
        file_name = text_of(ref.get("file"))
        caption = "%s Source: %s. Terms: %s." % (text_of(ref.get("note")), text_of(ref.get("source")) or "not recorded",
                                                text_of(ref.get("license")) or "not recorded")
        image = ""
        if file_name and not re.match(r"^(?:[a-z]+:)?//|^data:", file_name.lower()) \
                and os.path.splitext(file_name)[1].lower() in IMAGE_EXT \
                and os.path.isfile(os.path.join(base_dir, file_name)):
            rel = os.path.relpath(os.path.join(base_dir, file_name), out_dir).replace(os.sep, "/")
            image = '<img src="%s" alt="%s" loading="lazy">' % (esc(rel), esc(text_of(ref.get("note")) or file_name))
        figures.append("<figure>%s<figcaption>%s</figcaption></figure>" % (image, esc(caption.strip())))
    if figures:
        parts.append('<div class="refs">%s</div>' % "".join(figures))

    parts.append("<h3>Layout and shape</h3>")
    parts.append("<p>Skeleton: <code>%s</code>. %s</p><p>%s</p>" % (
        esc(text_of(layout.get("skeleton"))), esc(text_of(layout.get("notes"))), esc(text_of(layout.get("shape")))))
    parts.append("<h3>Motion</h3><p>%s</p>" % esc(text_of(direction.get("motion"))))
    parts.append("<h3>Signature element</h3><p>%s</p>" % esc(text_of(direction.get("signature"))))
    parts.append("<h3>How it differs</h3>")
    parts.append("<p>From the other directions: %s</p><p>From the category norm: %s</p>" % (
        esc(text_of(direction.get("differsFromOthers"))), esc(text_of(direction.get("differsFromDefault")))))
    if text_of(direction.get("notes")):
        parts.append("<h3>Notes</h3><p>%s</p>" % esc(text_of(direction.get("notes"))))

    parts.append("<h3>Your feedback</h3>")
    parts.append('<table class="kcr"><thead><tr><th scope="col">Part</th><th scope="col">Keep</th>'
                 '<th scope="col">Change</th><th scope="col">Remove</th><th scope="col">Note</th></tr></thead><tbody>')
    full = "%s %s" % (ident.upper(), name)
    for key, title in PARTS:
        group = "%s-%s" % (slug(ident) or str(index), key)
        cells = "".join(
            '<td class="pick"><input type="radio" name="%s" value="%s" aria-label="%s: %s, %s"></td>'
            % (esc(group), choice, esc(full), esc(title), choice) for choice in ("keep", "change", "remove"))
        parts.append('<tr data-direction="%s" data-part="%s"><th scope="row">%s</th>%s<td><input type="text" '
                     'aria-label="%s: %s, note"></td></tr>' % (esc(full), esc(title), esc(title), cells,
                                                               esc(full), esc(title)))
    parts.append("</tbody></table>")
    parts.append("</article>")
    return "\n".join(parts)


def render(board, metrics, pairs, default_rows, findings, base_dir, out_dir, google_fonts):
    directions = [d for d in (board.get("directions") or []) if isinstance(d, dict)]
    brief = board.get("brief") if isinstance(board.get("brief"), dict) else {}
    default = board.get("categoryDefault") if isinstance(board.get("categoryDefault"), dict) else {}
    sample_copy = board.get("sampleCopy") if isinstance(board.get("sampleCopy"), dict) else {}
    project = text_of(board.get("project")) or "Untitled project"
    question = text_of(board.get("feedbackQuestion")) or \
        "For each direction and each part: keep, change or remove? Which direction is the base?"
    head = ['<!doctype html>', '<html lang="en">', "<head>", '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>Direction board: %s</title>" % esc(project)]
    if google_fonts:
        links = [text_of(board.get("googleFontsHref"))]
        for direction in directions:
            type_block = direction.get("type") if isinstance(direction.get("type"), dict) else {}
            links.append(text_of(type_block.get("googleFontsHref")))
        for link in OrderedDict.fromkeys(l for l in links if l.startswith("https://fonts.googleapis.com/css")):
            head.append('<link rel="stylesheet" href="%s">' % esc(link))
    faces = []
    for direction in directions:
        type_block = direction.get("type") if isinstance(direction.get("type"), dict) else {}
        for key in ("display", "body"):
            block = type_block.get(key) if isinstance(type_block.get(key), dict) else {}
            family = safe_stack(block.get("family")).replace('"', "").replace("'", "")
            for name in font_files(block):
                if re.match(r"^(?:[a-z]+:)?//|^data:", name.lower()) or not os.path.isfile(os.path.join(base_dir, name)):
                    continue
                rel = os.path.relpath(os.path.join(base_dir, name), out_dir).replace(os.sep, "/")
                weight = block.get("weight")
                weight = int(weight) if isinstance(weight, (int, float)) and not isinstance(weight, bool) \
                    and 1 <= weight <= 1000 else 400
                faces.append('@font-face{font-family:"%s";src:url("%s");font-weight:%d;font-display:block}'
                             % (family, esc(rel), weight))
    head.append("<style>%s%s</style>" % ("\n".join(OrderedDict.fromkeys(faces)) + "\n" if faces else "", CHROME_CSS))
    head.append("</head>")

    body = ["<body>", "<header>", "<h1>Direction board: %s</h1>" % esc(project)]
    body.append('<p class="meta">Stage: %s. Date: %s. %d directions.</p>' % (
        esc(text_of(board.get("stage")) or "explore"), esc(text_of(board.get("date")) or "not set"), len(directions)))
    words = ", ".join(text_of(w) for w in (brief.get("brandWords") or []) if text_of(w))
    body.append('<p class="meta">Brief: %s for %s, so they can %s. Brand words: %s.</p>' % (
        esc(text_of(brief.get("subject")) or "[SUBJECT]"), esc(text_of(brief.get("audience")) or "[AUDIENCE]"),
        esc(text_of(brief.get("primaryJob")) or "[PRIMARY JOB]"), esc(words or "[THREE BRAND WORDS]")))
    body.append('<p class="meta">Category norm: %s</p>' % esc(text_of(default.get("description")) or "[NOT WRITTEN]"))
    body.append('<p class="notice"><strong>Feedback wanted:</strong> %s References on this board show direction '
                'only. They do not ship in the product.</p>' % esc(question))
    body.append("</header>")
    body.append('<main><div class="board" style="--n:%d">' % max(1, len(directions)))
    for index, direction in enumerate(directions):
        body.append(render_direction(direction, index, base_dir, out_dir, sample_copy))
    body.append("</div>")

    body.append('<section class="panel" aria-labelledby="unique-h"><h2 id="unique-h">Uniqueness test</h2>')
    if pairs:
        rows = "".join(
            "<tr><td>%s and %s</td><td class=\"num\">%s</td><td>%s</td><td>%s</td><td>%s</td><td class=\"%s\">%s</td></tr>"
            % (esc(p["a"].upper()), esc(p["b"].upper()),
               "n/a" if p["hueDistance"] is None else "%.0f" % p["hueDistance"],
               "same" if p["samePaletteFamily"] else "differs", "same" if p["sameTypeClass"] else "differs",
               "same" if p["sameLayoutSkeleton"] else "differs",
               "fail" if p["verdict"] == "near-identical" else "pass", esc(p["verdict"])) for p in pairs)
        body.append('<table><thead><tr><th>Pair</th><th>Accent hue distance</th><th>Palette family</th>'
                    '<th>Type class</th><th>Layout skeleton</th><th>Verdict</th></tr></thead><tbody>%s</tbody></table>'
                    % rows)
    body.append('<p class="meta">A pair fails when it shares palette family, type class and layout skeleton. '
                'The test is a floor. Two directions can pass it and still be one idea.</p>')
    shown = [f for f in findings]
    if shown:
        body.append('<h3>Findings from the board check</h3><ul class="findings">')
        for item in shown:
            body.append('<li><span class="%s">%s</span> <code>%s</code> %s %s</li>' % (
                "fail" if item["level"] == "error" else "", esc(item["level"].upper()), esc(item["code"]),
                esc(item["message"]), esc(item["hint"])))
        body.append("</ul>")
    else:
        body.append("<p>The board check found nothing.</p>")
    body.append("</section>")

    options = "".join('<option value="%s">%s</option>' % (esc(label_of(d, i)), esc(label_of(d, i)))
                      for i, d in enumerate(directions))
    body.append('<section class="panel" aria-labelledby="fb-h"><h2 id="fb-h">Send your feedback</h2>'
                '<p><label for="base-direction">Base direction</label> <select id="base-direction">'
                '<option value="">not chosen</option>%s<option value="none of these">none of these</option></select></p>'
                '<p><label for="feedback-extra">What is missing, or anything else</label><br>'
                '<input type="text" id="feedback-extra" style="width:100%%;font:inherit;padding:4px"></p>'
                '<p><button type="button" id="feedback-make">Write my feedback as text</button></p>'
                '<p><label for="feedback-text">Copy this text into the chat</label></p>'
                '<textarea id="feedback-text" readonly></textarea></section>' % options)
    body.append("</main>")
    body.append("<script>%s</script>" % BOARD_JS)
    body.append("</body></html>")
    return "\n".join(head + body) + "\n"


# ---------------------------------------------------------------- commands

def load_board(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def summary_of(findings):
    return OrderedDict([("errors", sum(1 for f in findings if f["level"] == "error")),
                        ("warnings", sum(1 for f in findings if f["level"] == "warning"))])


def format_findings(findings):
    lines = []
    for item in findings:
        lines.append("%s %s at %s" % (item["level"].upper(), item["code"], item["path"] or "(file)"))
        lines.append("  %s" % item["message"])
        lines.append("  fix: %s" % item["hint"])
    return lines


def run(command, board_path, output=None, google_fonts=False, threshold=DEFAULT_HUE_THRESHOLD):
    """Run one command. Return (exit code, result dict). Raises ValueError on unreadable input."""
    try:
        board = load_board(board_path)
    except (OSError, ValueError) as error:
        raise ValueError("cannot read %s: %s" % (board_path, error))
    base_dir = os.path.dirname(os.path.abspath(board_path))
    findings = validate(board, base_dir)
    metrics, pairs, default_rows = [], [], []
    structural = any(f["code"] == "MB_SHAPE" for f in findings)
    if not structural:
        metrics, pairs, default_rows, more = analyse(board, threshold)
        findings = findings + more
        if command == "build":
            findings = findings + font_findings(board, google_fonts)
    result = OrderedDict([("tool", "moodboard.py"), ("version", VERSION), ("command", command),
                          ("board", board_path)])
    if command == "build":
        written = None
        if not structural:
            out_path = os.path.abspath(output)
            out_dir = os.path.dirname(out_path)
            page = render(board, metrics, pairs, default_rows, findings, base_dir, out_dir, google_fonts)
            os.makedirs(out_dir, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as handle:
                handle.write(page)
            written = output
        result["output"] = written
        result["offline"] = not google_fonts
    result["hueThreshold"] = threshold
    result["knownDefaultsTable"] = KNOWN_DEFAULTS_DATE
    result["directions"] = metrics
    result["pairs"] = pairs
    result["categoryDefault"] = default_rows
    result["findings"] = findings
    result["summary"] = summary_of(findings)
    result["pass"] = not has_errors(findings)
    return (0 if result["pass"] else 1), result


def format_text(result):
    lines = []
    if result["command"] == "build":
        if result.get("output"):
            lines.append("Wrote %s (%d directions, %s)." % (
                result["output"], len(result["directions"]),
                "offline" if result["offline"] else "loads Google Fonts"))
        else:
            lines.append("No board was written. Fix the file shape first.")
    lines.append("Directions:")
    for m in result["directions"]:
        lines.append("  %s %-22s spread %-8s accent %s hue %s ground %s type %s skeleton %s" % (
            m["id"].upper(), m["name"], m["spread"] or "-", m["accentHex"] or "-",
            "none" if m["hue"] is None else "%.0f" % m["hue"], m["ground"] or "-", m["typeClass"] or "-",
            m["layoutSkeleton"] or "-"))
    if result["pairs"]:
        lines.append("Pairs (accent hue distance in degrees; threshold %g):" % result["hueThreshold"])
        for p in result["pairs"]:
            lines.append("  %s and %s: hue distance %s; palette family %s; type class %s; layout skeleton %s; %s" % (
                p["a"].upper(), p["b"].upper(), "n/a" if p["hueDistance"] is None else "%.0f" % p["hueDistance"],
                "same" if p["samePaletteFamily"] else "differs", "same" if p["sameTypeClass"] else "differs",
                "same" if p["sameLayoutSkeleton"] else "differs", p["verdict"]))
    lines.append("Known default looks: table of %s (%s)." % (
        result["knownDefaultsTable"], ", ".join(v[0] for v in KNOWN_DEFAULTS.values())))
    for row in result["categoryDefault"]:
        lines.append("  %s and the category norm: shares %s%s" % (
            row["id"].upper(), ", ".join(row["shared"]) or "nothing",
            "; accepted: %s" % row["accepted"] if row["accepted"] else ""))
    lines.extend(format_findings(result["findings"]))
    lines.append("Result: %s (%d error(s), %d warning(s))" % (
        "pass" if result["pass"] else "fail", result["summary"]["errors"], result["summary"]["warnings"]))
    if result["command"] == "diff":
        lines.append("The test is a floor. Two directions can pass it and still be one idea. Read the concept lines.")
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(prog="moodboard.py",
                                     description="Comparison board and uniqueness check for design directions.")
    parser.add_argument("--version", action="version", version="moodboard.py " + VERSION)
    sub = parser.add_subparsers(dest="command")
    build = sub.add_parser("build", help="Render the offline comparison board.")
    build.add_argument("board")
    build.add_argument("-o", "--output", required=True, help="path of the HTML file to write")
    build.add_argument("--google-fonts", action="store_true",
                       help="add the Google Fonts links named in the board file; the page then needs a network")
    diff = sub.add_parser("diff", help="Report how far the directions differ.")
    diff.add_argument("board")
    for parser_ in (build, diff):
        parser_.add_argument("--hue-threshold", type=float, default=DEFAULT_HUE_THRESHOLD,
                             help="accent hue distance below which two palettes are one family (default %g)"
                             % DEFAULT_HUE_THRESHOLD)
        parser_.add_argument("--json", action="store_true", help="print one JSON object on stdout")
    return parser


def main(argv=None):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as stop:
        return int(stop.code or 0)
    if not args.command:
        parser.print_usage(sys.stderr)
        return 2
    try:
        code, result = run(args.command, args.board, getattr(args, "output", None),
                           getattr(args, "google_fonts", False), args.hue_threshold)
    except ValueError as error:
        sys.stderr.write("moodboard.py: %s\n" % error)
        return 2
    print(json.dumps(result, indent=2) if args.json else format_text(result))
    return code


if __name__ == "__main__":
    sys.exit(main())
