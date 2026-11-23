"""Tests for kit/skills/mood-board/scripts/moodboard.py.

Run: python3 -m unittest discover -s tests
"""

import contextlib
import copy
import importlib.util
import io
import json
import os
import re
import shutil
import tempfile
import unittest
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "kit", "skills", "mood-board", "scripts", "moodboard.py")
TEMPLATE = os.path.join(ROOT, "kit", "skills", "mood-board", "templates", "board.json")

_spec = importlib.util.spec_from_file_location("gdh_moodboard", SCRIPT)
mb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mb)


def template():
    with open(TEMPLATE, "r", encoding="utf-8") as handle:
        return json.load(handle)


class TagCheck(HTMLParser):
    """Collect tags and attributes, and check that non-void tags close in order."""

    VOID = {"meta", "link", "img", "input", "br", "hr"}

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack, self.errors, self.tags, self.attrs = [], [], [], []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.append((tag, dict(attrs)))
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append("unexpected </%s>" % tag)
        else:
            self.stack.pop()


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-moodboard-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def path(self, *parts):
        return os.path.join(self.tmp, *parts)

    def write_board(self, board, name="board.json"):
        target = self.path(name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            json.dump(board, handle)
        return target

    def cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = mb.main(argv)
        return code, out.getvalue(), err.getvalue()

    def diff(self, board, *extra):
        code, out, _ = self.cli(["diff", self.write_board(board), "--json"] + list(extra))
        return code, json.loads(out)

    def build(self, board, *extra):
        target = self.path("out", "board.html")
        code, out, _ = self.cli(["build", self.write_board(board), "-o", target, "--json"] + list(extra))
        page = ""
        if os.path.isfile(target):
            with open(target, "r", encoding="utf-8") as handle:
                page = handle.read()
        return code, json.loads(out), page

    def codes(self, result, level=None):
        return [f["code"] for f in result["findings"] if level is None or f["level"] == level]


class ColorMath(Case):
    def test_contrast_extremes(self):
        self.assertAlmostEqual(mb.contrast("#000000", "#ffffff"), 21.0, places=1)
        self.assertAlmostEqual(mb.contrast("#fff", "#ffffff"), 1.0, places=3)

    def test_contrast_known_pair(self):
        # #767676 on white is the usual example of a pair just above 4.5:1.
        ratio = mb.contrast("#767676", "#ffffff")
        self.assertTrue(4.5 <= ratio < 4.6, ratio)

    def test_oklch_hues(self):
        red = mb.oklch(mb.hex_to_rgb("#ff0000"))[2]
        green = mb.oklch(mb.hex_to_rgb("#00ff00"))[2]
        blue = mb.oklch(mb.hex_to_rgb("#0000ff"))[2]
        self.assertTrue(20 < red < 40, red)
        self.assertTrue(130 < green < 150, green)
        self.assertTrue(255 < blue < 275, blue)

    def test_gray_has_no_chroma(self):
        self.assertLess(mb.oklch(mb.hex_to_rgb("#808080"))[1], 0.001)

    def test_hue_distance_wraps(self):
        self.assertEqual(mb.hue_distance(350, 10), 20)
        self.assertEqual(mb.hue_distance(10, 350), 20)
        self.assertEqual(mb.hue_distance(0, 180), 180)

    def test_norm_hex(self):
        self.assertEqual(mb.norm_hex("#ABC"), "#aabbcc")


class TemplateBoard(Case):
    def test_template_passes_diff(self):
        code, out, _ = self.cli(["diff", TEMPLATE])
        self.assertEqual(code, 0, out)
        self.assertIn("Result: pass", out)
        self.assertIn("The test is a floor", out)

    def test_template_has_three_directions_with_all_parts(self):
        code, result = self.diff(template())
        self.assertEqual(code, 0)
        self.assertEqual(len(result["directions"]), 3)
        self.assertEqual(self.codes(result, "error"), [])
        self.assertEqual(sorted(d["spread"] for d in result["directions"]), ["expected", "outside", "safe"])
        self.assertTrue(all(p["verdict"] == "distinct" for p in result["pairs"]))
        self.assertTrue(all(row["shared"] == [] for row in result["categoryDefault"]))

    def test_template_warns_that_it_is_a_template(self):
        _, result = self.diff(template())
        self.assertIn("MB_TEMPLATE", self.codes(result, "warning"))

    def test_template_is_ascii(self):
        with open(TEMPLATE, "rb") as handle:
            data = handle.read()
        self.assertTrue(data.isascii(), "the board template holds a non-ASCII byte")

    def test_skeleton_is_required_and_from_the_closed_list(self):
        # The skeleton comes from the closed list in directions.md section 5. A coined name would hide a clone.
        for value in ("", "   ", None):
            board = template()
            if value is None:
                del board["directions"][1]["layout"]["skeleton"]
            else:
                board["directions"][1]["layout"]["skeleton"] = value
            code, result = self.diff(board)
            self.assertEqual(code, 1, repr(value))
            paths = [f["path"] for f in result["findings"] if f["code"] == "MB_PART_MISSING"]
            self.assertIn("directions[1].layout", paths)
        board = template()
        board["directions"][1]["layout"]["skeleton"] = "staggered ledger"
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertEqual(self.codes(result, "error"), ["MB_SKELETON"])
        board["directions"][1]["layout"]["skeleton"] = "Timeline Rail"
        self.assertEqual(self.diff(board)[0], 0)

    def test_closed_list_matches_the_reference(self):
        with open(os.path.join(ROOT, "kit", "skills", "mood-board", "references", "directions.md"),
                  encoding="utf-8") as handle:
            text = handle.read()
        section = text.split("## 5.")[1].split("## 6.")[0]
        listed = re.findall(r"^\| `([a-z-]+)` \|", section, re.M)
        self.assertEqual(tuple(listed), mb.SKELETONS)

    def test_script_is_ascii_and_offline(self):
        with open(SCRIPT, "rb") as handle:
            text = handle.read().decode("ascii")
        for needle in ("urllib", "http.client", "import socket", "import requests", "subprocess"):
            self.assertNotIn(needle, text)


class Uniqueness(Case):
    def twin(self):
        board = template()
        twin = copy.deepcopy(board["directions"][0])
        twin.update({"id": "b", "name": "Arrival Board", "spread": "expected",
                     "concept": "Arrivals lead: the screen greets people stepping off with onward connections.",
                     "adjectives": [{"word": "welcoming", "opposite": "cold"}, {"word": "onward", "opposite": "stuck"},
                                    {"word": "brisk", "opposite": "slow"}]})
        twin["palette"][3]["hex"] = "#ffa31a"
        board["directions"][1] = twin
        return board

    def test_near_identical_pair_fails(self):
        code, result = self.diff(self.twin())
        self.assertEqual(code, 1)
        self.assertIn("MB_NEAR_IDENTICAL", self.codes(result, "error"))
        pair = [p for p in result["pairs"] if (p["a"], p["b"]) == ("a", "b")][0]
        self.assertEqual(pair["verdict"], "near-identical")
        self.assertLess(pair["hueDistance"], 30)
        self.assertEqual(len(pair["shared"]), 3)
        self.assertFalse(result["pass"])

    def test_text_output_names_the_pair(self):
        code, out, _ = self.cli(["diff", self.write_board(self.twin())])
        self.assertEqual(code, 1)
        self.assertIn("ERROR MB_NEAR_IDENTICAL", out)
        self.assertIn("A Departure Board and B Arrival Board", out)
        self.assertIn("Result: fail", out)

    def test_one_changed_part_makes_it_weak_not_failed(self):
        board = self.twin()
        board["directions"][1]["layout"]["skeleton"] = "split-screen"
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertIn("MB_WEAK_SPREAD", self.codes(result, "warning"))
        self.assertNotIn("MB_NEAR_IDENTICAL", self.codes(result))

    def test_far_hue_breaks_the_palette_family(self):
        board = self.twin()
        board["directions"][1]["palette"][3]["hex"] = "#0b6e63"
        board["directions"][1]["palette"][4]["hex"] = "#ffffff"
        code, result = self.diff(board)
        pair = [p for p in result["pairs"] if (p["a"], p["b"]) == ("a", "b")][0]
        self.assertFalse(pair["samePaletteFamily"])
        self.assertEqual(pair["verdict"], "weak")
        self.assertEqual(code, 0)

    def test_same_hue_on_dark_ground_is_another_family(self):
        board = self.twin()
        colors = {"bg": "#101820", "text": "#f7f5ef", "muted": "#b8c0c8"}
        for entry in board["directions"][1]["palette"]:
            entry["hex"] = colors.get(entry["role"], entry["hex"])
        _, result = self.diff(board)
        pair = [p for p in result["pairs"] if (p["a"], p["b"]) == ("a", "b")][0]
        self.assertFalse(pair["sameGround"])
        self.assertFalse(pair["samePaletteFamily"])

    def test_two_achromatic_palettes_are_one_family(self):
        board = self.twin()
        for direction in board["directions"][:2]:
            direction["palette"] = [{"role": "bg", "name": "Paper", "hex": "#ffffff"},
                                    {"role": "text", "name": "Ink", "hex": "#111111"},
                                    {"role": "accent", "name": "Graphite", "hex": "#444444"}]
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertTrue(result["directions"][0]["achromatic"])
        self.assertIsNone(result["directions"][0]["hue"])

    def test_hue_threshold_flag(self):
        board = self.twin()
        board["directions"][1]["palette"][3]["hex"] = "#ff7a00"
        code_default, result = self.diff(board)
        distance = [p for p in result["pairs"] if (p["a"], p["b"]) == ("a", "b")][0]["hueDistance"]
        self.assertTrue(10 < distance < 30, distance)
        self.assertEqual(code_default, 1)
        code_strict, _ = self.diff(board, "--hue-threshold", "10")
        self.assertEqual(code_strict, 0)

    def test_type_class_and_skeleton_are_normalized(self):
        board = self.twin()
        board["directions"][1]["type"]["class"] = "Grotesque Sans"
        board["directions"][1]["layout"]["skeleton"] = "Table led"
        code, _ = self.diff(board)
        self.assertEqual(code, 1)

    def test_category_default_match_fails(self):
        board = template()
        first = board["directions"][0]
        first["palette"][3]["hex"] = "#1a73e8"
        first["palette"][4]["hex"] = "#ffffff"
        first["type"]["class"] = "geometric-sans"
        first["layout"]["skeleton"] = "card list"
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertIn("MB_SAME_AS_CATEGORY_DEFAULT", self.codes(result, "error"))

    def test_category_default_match_can_be_accepted_with_a_reason(self):
        board = template()
        first = board["directions"][0]
        first["palette"][3]["hex"] = "#1a73e8"
        first["palette"][4]["hex"] = "#ffffff"
        first["type"]["class"] = "geometric-sans"
        first["layout"]["skeleton"] = "card list"
        first["allowCategoryDefault"] = "The brief asks for the familiar transit look."
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertEqual(result["categoryDefault"][0]["accepted"], "The brief asks for the familiar transit look.")

    def test_default_without_structured_fields_fails_at_explore(self):
        # Review finding: the comparison was skipped without a word. At stage explore it is an error.
        board = template()
        board["categoryDefault"] = {"description": "Blue, rounded cards."}
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertEqual(result["categoryDefault"], [])
        self.assertIn("MB_DEFAULT_UNSTRUCTURED", self.codes(result, "error"))
        board["stage"] = "refine"
        self.assertEqual(self.diff(board)[0], 0)

    def test_renamed_skeleton_clone_fails(self):
        # Review finding: a cloned direction with the skeleton renamed passed as 'weak'.
        board = self.twin()
        board["directions"][1]["layout"]["skeleton"] = "table-led v2"
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertIn("MB_SKELETON", self.codes(result, "error"))

    def test_same_concept_is_near_identical_whatever_the_labels(self):
        board = template()
        clone = copy.deepcopy(board["directions"][0])
        clone.update({"id": "b", "name": "Quay Rows", "spread": "expected"})
        clone["type"]["class"] = "slab-serif"
        clone["layout"]["skeleton"] = "card-list"
        clone["palette"][3]["hex"] = "#0b6e63"
        board["directions"][1] = clone
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        pair = [p for p in result["pairs"] if (p["a"], p["b"]) == ("a", "b")][0]
        self.assertEqual(pair["shared"], [])
        self.assertEqual(pair["verdict"], "near-identical")
        self.assertTrue(any("concept words" in s for s in pair["sameContent"]))
        self.assertIn("adjectives", pair["sameContent"])

    def test_concept_overlap_uses_content_words(self):
        a = mb.content_words("The app is the quay-side departure board in your pocket.")
        b = mb.content_words("The ticket is the interface you hold in your hand.")
        self.assertLess(mb.jaccard(a, b), mb.CONCEPT_OVERLAP)


class KnownDefaults(Case):
    """Review finding: a board of the current default looks passed as distinct."""

    def direction(self, board, index, bg, accent, type_class, skeleton):
        direction = board["directions"][index]
        for entry in direction["palette"]:
            if entry["role"] == "bg":
                entry["hex"] = bg
            if entry["role"] == "accent":
                entry["hex"] = accent
            if entry["role"] == "text":
                entry["hex"] = "#141414" if mb.oklch(mb.hex_to_rgb(bg))[0] > 0.6 else "#f2f2f2"
            if entry["role"] == "muted":
                entry["hex"] = "#3c3c3c" if mb.oklch(mb.hex_to_rgb(bg))[0] > 0.6 else "#c8c8c8"
        direction["type"]["class"] = type_class
        direction["layout"]["skeleton"] = skeleton
        return direction

    def test_three_default_looks_fail(self):
        board = template()
        self.direction(board, 0, "#f4efe6", "#c2410c", "transitional-serif", "editorial-columns")
        self.direction(board, 1, "#0b0b0c", "#a3e635", "grotesque-sans", "split-screen")
        self.direction(board, 2, "#0b0b12", "#8b5cf6", "geometric-sans", "card-grid")
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        hits = [f for f in result["findings"] if f["code"] == "MB_KNOWN_DEFAULT"]
        self.assertEqual(len(hits), 3)
        self.assertEqual([m["knownDefault"] for m in result["directions"]],
                         ["warm-editorial", "night-signal", "violet-tech"])
        self.assertEqual(result["knownDefaultsTable"], mb.KNOWN_DEFAULTS_DATE)

    def test_palette_alone_does_not_match(self):
        board = template()
        self.direction(board, 0, "#f4efe6", "#c2410c", "humanist-sans", "table-led")
        _, result = self.diff(board)
        self.assertNotIn("MB_KNOWN_DEFAULT", self.codes(result, "error"))

    def test_reason_from_the_brief_accepts_a_match(self):
        board = template()
        self.direction(board, 0, "#f4efe6", "#c2410c", "transitional-serif", "editorial-columns")
        board["directions"][0]["allowCategoryDefault"] = "The brief asks for the house editorial style."
        _, result = self.diff(board)
        self.assertNotIn("MB_KNOWN_DEFAULT", self.codes(result, "error"))

    def test_gradient_signature_matches_unless_negated(self):
        board = template()
        board["directions"][0]["signature"] = "A violet gradient behind a glass card."
        self.assertIn("MB_KNOWN_DEFAULT", self.codes(self.diff(board)[1], "error"))
        board["directions"][0]["signature"] = "One split-flap row, with no gradient or glow."
        self.assertNotIn("MB_KNOWN_DEFAULT", self.codes(self.diff(board)[1], "error"))

    def test_table_matches_the_tell_scan(self):
        spec = importlib.util.spec_from_file_location(
            "gdh_tells_parity", os.path.join(ROOT, "kit", "skills", "design-critique", "scripts", "tells.py"))
        tells = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tells)
        self.assertEqual(tells.SECOND_WAVE_DATE, mb.KNOWN_DEFAULTS_DATE)
        for look, (_side, ground, bands, _name) in tells.SECOND_WAVE_LOOKS.items():
            self.assertIn(look, mb.KNOWN_DEFAULTS)
            self.assertEqual(mb.KNOWN_DEFAULTS[look][1], ground)
            self.assertEqual(mb.KNOWN_DEFAULTS[look][2], bands)


class Fonts(Case):
    """Review finding: specimens showed fallback faces with no notice."""

    def test_offline_build_warns_and_marks_each_specimen(self):
        code, result, page = self.build(template())
        self.assertEqual(code, 0)
        warned = [f for f in result["findings"] if f["code"] == "MB_FONT_NOT_LOADED"]
        self.assertTrue(warned)
        self.assertIn('data-check-family="Overpass"', page)
        self.assertIn("Fallback face shown", page)
        self.assertIn("measureText", page)

    def test_local_font_file_becomes_a_font_face(self):
        board = template()
        os.makedirs(self.path("fonts"), exist_ok=True)
        with open(self.path("fonts", "overpass.woff2"), "wb") as fh:
            fh.write(b"wOF2")
        for key in ("display", "body"):
            board["directions"][0]["type"][key]["files"] = ["fonts/overpass.woff2"]
        code, result, page = self.build(board)
        self.assertEqual(code, 0)
        self.assertIn('@font-face{font-family:"Overpass";src:url("../fonts/overpass.woff2")', page)
        paths = [f["path"] for f in result["findings"] if f["code"] == "MB_FONT_NOT_LOADED"]
        self.assertNotIn("directions[0].type.display", paths)

    def test_remote_or_missing_font_file_is_an_error(self):
        board = template()
        board["directions"][0]["type"]["display"]["files"] = ["https://example.com/a.woff2"]
        board["directions"][1]["type"]["display"]["files"] = ["fonts/absent.woff2"]
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertEqual(self.codes(result, "error").count("MB_FONT_FILE"), 2)

    def test_google_fonts_build_does_not_warn_for_linked_families(self):
        _, result, _page = self.build(template(), "--google-fonts")
        names = [f["message"] for f in result["findings"] if f["code"] == "MB_FONT_NOT_LOADED"]
        self.assertFalse(any(n.startswith("Overpass") for n in names), names)


class Validation(Case):
    def test_direction_count(self):
        board = template()
        board["directions"] = board["directions"][:1]
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertIn("MB_DIRECTION_COUNT", self.codes(result, "error"))
        board = template()
        board["directions"] = board["directions"] + [copy.deepcopy(board["directions"][0])] * 2
        self.assertIn("MB_DIRECTION_COUNT", self.codes(self.diff(board)[1], "error"))

    def test_two_directions_are_allowed(self):
        board = template()
        board["directions"] = [board["directions"][0], board["directions"][2]]
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertNotIn("MB_SPREAD", self.codes(result))

    def test_two_directions_need_one_outside(self):
        board = template()
        board["directions"] = board["directions"][:2]
        _, result = self.diff(board)
        self.assertIn("MB_SPREAD", self.codes(result, "warning"))

    def test_three_directions_need_the_full_spread(self):
        board = template()
        board["directions"][2]["spread"] = "safe"
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertIn("MB_SPREAD", self.codes(result, "warning"))

    def test_each_part_is_required(self):
        for key in ("concept", "imagery", "texture", "motion", "signature", "palette", "type", "layout", "sample"):
            board = template()
            del board["directions"][1][key]
            code, result = self.diff(board)
            self.assertEqual(code, 1, key)
            paths = [f["path"] for f in result["findings"] if f["code"] in ("MB_PART_MISSING",)]
            self.assertIn("directions[1].%s" % key, paths, key)

    def test_adjectives_need_three_pairs(self):
        board = template()
        board["directions"][0]["adjectives"] = board["directions"][0]["adjectives"][:2]
        self.assertIn("MB_ADJECTIVES", self.codes(self.diff(board)[1], "error"))
        board = template()
        del board["directions"][0]["adjectives"][0]["opposite"]
        self.assertIn("MB_ADJECTIVES", self.codes(self.diff(board)[1], "error"))

    def test_palette_roles_and_hex(self):
        board = template()
        board["directions"][0]["palette"] = [p for p in board["directions"][0]["palette"] if p["role"] != "text"]
        self.assertIn("MB_PALETTE_ROLE", self.codes(self.diff(board)[1], "error"))
        board = template()
        board["directions"][0]["palette"][0]["hex"] = "chalk"
        self.assertIn("MB_HEX", self.codes(self.diff(board)[1], "error"))

    def test_text_contrast_is_an_error(self):
        board = template()
        board["directions"][1]["palette"][1]["hex"] = "#9fb3ad"
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        hits = [f for f in result["findings"] if f["code"] == "MB_CONTRAST" and f["level"] == "error"]
        self.assertTrue(hits)
        self.assertIn("text on bg", hits[0]["message"])
        self.assertIn("4.5", hits[0]["message"])

    def test_on_accent_contrast_is_an_error(self):
        board = template()
        board["directions"][0]["palette"][4]["hex"] = "#ffffff"
        result = self.diff(board)[1]
        self.assertTrue(any(f["code"] == "MB_CONTRAST" and f["level"] == "error" and "on-accent" in f["message"]
                            for f in result["findings"]))

    def test_weak_accent_on_ground_is_a_warning(self):
        code, result = self.diff(template())
        hits = [f for f in result["findings"] if f["code"] == "MB_CONTRAST"]
        self.assertEqual([f["level"] for f in hits], ["warning"])
        self.assertIn("fills only", hits[0]["hint"])
        self.assertEqual(code, 0)

    def test_type_block_shape_and_vocabulary(self):
        board = template()
        del board["directions"][0]["type"]["body"]["stack"]
        self.assertIn("MB_PART_MISSING", self.codes(self.diff(board)[1], "error"))
        board = template()
        board["directions"][0]["type"]["class"] = "techy"
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertIn("MB_TYPE_CLASS", self.codes(result, "warning"))

    def test_placeholder_copy_is_an_error(self):
        board = template()
        board["directions"][0]["sample"]["body"] = "Lorem ipsum dolor sit amet."
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertIn("MB_PLACEHOLDER_COPY", self.codes(result, "error"))

    def test_difference_lines(self):
        board = template()
        board["directions"][0]["differsFromDefault"] = ""
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertIn("MB_DIFFERENCE_LINE", self.codes(result, "error"))
        board = template()
        board["directions"][0]["differsFromOthers"] = "It is the blue one."
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertIn("MB_DIFFERENCE_NAMES_COLOR", self.codes(result, "warning"))

    def test_category_default_description_is_required(self):
        board = template()
        board["categoryDefault"]["description"] = ""
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertIn("MB_CATEGORY_DEFAULT", self.codes(result, "error"))

    def test_duplicate_names(self):
        board = template()
        board["directions"][1]["name"] = board["directions"][0]["name"]
        self.assertIn("MB_DUPLICATE_NAME", self.codes(self.diff(board)[1], "error"))

    def test_brief_block_warning(self):
        board = template()
        board["brief"]["brandWords"] = ["dependable"]
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertIn("MB_BRIEF", self.codes(result, "warning"))

    def test_reference_needs_source_and_license(self):
        board = template()
        del board["directions"][0]["references"][0]["license"]
        code, result = self.diff(board)
        self.assertEqual(code, 1)
        self.assertIn("MB_REF_SOURCE", self.codes(result, "error"))

    def test_remote_reference_file_is_an_error(self):
        for value in ("https://example.org/a.jpg", "//example.org/a.jpg", "data:image/png;base64,AAAA"):
            board = template()
            board["directions"][0]["references"][0]["file"] = value
            code, result = self.diff(board)
            self.assertEqual(code, 1, value)
            self.assertIn("MB_REF_REMOTE", self.codes(result, "error"))

    def test_missing_reference_file_is_a_warning(self):
        _, result = self.diff(template())
        self.assertEqual(self.codes(result).count("MB_REF_FILE_MISSING"), 6)

    def test_one_source_for_all_references(self):
        board = template()
        for direction in board["directions"]:
            for ref in direction["references"]:
                ref["source"] = "https://gallery.example.org/item/%s" % ref["file"]
        _, result = self.diff(board)
        self.assertIn("MB_REF_ONE_SOURCE", self.codes(result, "warning"))

    def test_direction_without_references_warns(self):
        board = template()
        board["directions"][0]["references"] = []
        code, result = self.diff(board)
        self.assertEqual(code, 0)
        self.assertIn("MB_REF_NONE", self.codes(result, "warning"))

    def test_every_finding_has_a_hint(self):
        board = template()
        board["directions"] = board["directions"][:1]
        del board["directions"][0]["palette"]
        _, result = self.diff(board)
        for item in result["findings"]:
            for key in ("code", "level", "path", "message", "hint"):
                self.assertIn(key, item)
            self.assertTrue(item["hint"])


class Build(Case):
    def board_with_images(self):
        board = template()
        os.makedirs(self.path("refs"), exist_ok=True)
        for direction in board["directions"]:
            for ref in direction["references"]:
                with open(self.path(ref["file"]), "wb") as handle:
                    handle.write(b"not a real image")
        return board

    def test_build_writes_a_well_formed_page(self):
        code, result, page = self.build(self.board_with_images())
        self.assertEqual(code, 0)
        self.assertTrue(result["offline"])
        self.assertTrue(page.startswith("<!doctype html>"))
        check = TagCheck()
        check.feed(page)
        self.assertEqual(check.errors, [])
        self.assertEqual(check.stack, [])
        self.assertEqual(check.tags.count("article"), 3)

    def test_page_loads_nothing_from_the_network(self):
        _, _, page = self.build(self.board_with_images())
        check = TagCheck()
        check.feed(page)
        for tag, attrs in check.attrs:
            for key in ("src", "href", "action", "poster", "srcset"):
                value = attrs.get(key) or ""
                self.assertFalse(re.match(r"^(?:https?:)?//", value), (tag, key, value))
        self.assertNotIn("<link", page)
        self.assertNotIn("@import", page)
        self.assertNotIn("url(", page)

    def test_google_fonts_only_with_the_flag(self):
        code, result, page = self.build(self.board_with_images(), "--google-fonts")
        self.assertEqual(code, 0)
        self.assertFalse(result["offline"])
        links = re.findall(r'<link rel="stylesheet" href="([^"]+)">', page)
        self.assertEqual(len(links), 3)
        self.assertTrue(all(link.startswith("https://fonts.googleapis.com/css2?") for link in links))

    def test_other_font_hosts_are_dropped(self):
        board = self.board_with_images()
        board["googleFontsHref"] = "https://fonts.example.org/css?family=Evil"
        _, _, page = self.build(board, "--google-fonts")
        self.assertNotIn("fonts.example.org", page)

    def test_swatches_show_hex_and_ratio(self):
        _, _, page = self.build(self.board_with_images())
        self.assertIn("<code>#ffb000</code>", page)
        self.assertIn("<code>#0b6e63</code>", page)
        self.assertRegex(page, r"\d+\.\d\d:1 on bg, text")
        self.assertIn("on accent, text", page)
        self.assertIn("fills only", page)
        self.assertIn("Contrast pairs", page)

    def test_specimen_uses_real_copy_and_font_stacks(self):
        _, _, page = self.build(self.board_with_images())
        self.assertGreaterEqual(page.count("Next boat 7:40"), 6)
        self.assertIn("font-family:&quot;Overpass&quot;, &quot;Helvetica Neue&quot;, Arial, sans-serif", page)
        self.assertIn("font-weight:800", page)
        self.assertIn("0123456789", page)

    def test_local_images_are_relative_to_the_output(self):
        _, _, page = self.build(self.board_with_images())
        self.assertIn('<img src="../refs/a-quay-board.jpg"', page)
        self.assertIn("Source: Own photo of the departure board at the quay.", page)

    def test_missing_images_are_not_linked(self):
        code, result, page = self.build(template())
        self.assertEqual(code, 0)
        self.assertNotIn("<img", page)
        self.assertIn("MB_REF_FILE_MISSING", self.codes(result))
        self.assertIn("Row rhythm and the size of the first row.", page)

    def test_feedback_table_has_every_part_for_every_direction(self):
        _, _, page = self.build(self.board_with_images())
        self.assertEqual(page.count('type="radio"'), 3 * len(mb.PARTS) * 3)
        for _, title in mb.PARTS:
            self.assertEqual(page.count('data-part="%s"' % title), 3)
        self.assertIn('value="keep"', page)
        self.assertIn('value="change"', page)
        self.assertIn('value="remove"', page)
        self.assertIn("Base direction", page)
        self.assertIn("Keep / Change / Remove:", page)

    def test_every_radio_has_an_accessible_name(self):
        _, _, page = self.build(self.board_with_images())
        check = TagCheck()
        check.feed(page)
        inputs = [attrs for tag, attrs in check.attrs if tag == "input"]
        self.assertTrue(inputs)
        for attrs in inputs:
            self.assertTrue(attrs.get("aria-label") or attrs.get("id"), attrs)

    def test_text_is_escaped(self):
        board = self.board_with_images()
        board["directions"][0]["name"] = "<script>alert(1)</script>"
        board["directions"][0]["concept"] = "Rows & \"rules\" <b>bold</b>"
        board["directions"][0]["type"]["display"]["stack"] = "Overpass; } body { visibility:hidden } </style><script>x()</script>"
        _, _, page = self.build(board)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertNotIn("<b>bold</b>", page)
        self.assertNotIn("visibility:hidden", page)
        self.assertNotIn("</style><script>", page)
        self.assertNotIn("<script>x()", page)
        self.assertEqual(page.count("<script>"), 1)

    def test_uniqueness_table_and_findings_are_on_the_page(self):
        board = self.board_with_images()
        twin = copy.deepcopy(board["directions"][0])
        twin.update({"id": "b", "name": "Arrival Board"})
        board["directions"][1] = twin
        code, result, page = self.build(board)
        self.assertEqual(code, 1)
        self.assertTrue(result["output"])
        self.assertIn("Uniqueness test", page)
        self.assertIn("near-identical", page)
        self.assertIn("MB_NEAR_IDENTICAL", page)

    def test_contrast_failure_is_marked_on_the_page(self):
        board = self.board_with_images()
        board["directions"][1]["palette"][1]["hex"] = "#9fb3ad"
        code, _, page = self.build(board)
        self.assertEqual(code, 1)
        self.assertIn(">FAIL<", page)

    def test_build_writes_only_the_output_path(self):
        board_path = self.write_board(self.board_with_images(), "in/board.json")
        before = set()
        for current, _, files in os.walk(self.tmp):
            before.update(os.path.join(current, name) for name in files)
        target = self.path("site", "deep", "board.html")
        code, _, _ = self.cli(["build", board_path, "-o", target])
        after = set()
        for current, _, files in os.walk(self.tmp):
            after.update(os.path.join(current, name) for name in files)
        self.assertEqual(code, 0)
        self.assertEqual(after - before, {target})

    def test_text_output_of_build(self):
        target = self.path("board.html")
        code, out, _ = self.cli(["build", self.write_board(self.board_with_images()), "-o", target])
        self.assertEqual(code, 0)
        self.assertIn("Wrote %s (3 directions, offline)." % target, out)


class Usage(Case):
    def test_no_command(self):
        self.assertEqual(self.cli([])[0], 2)

    def test_build_needs_an_output(self):
        self.assertEqual(self.cli(["build", TEMPLATE])[0], 2)

    def test_missing_file_and_bad_json(self):
        self.assertEqual(self.cli(["diff", self.path("absent.json")])[0], 2)
        bad = self.path("bad.json")
        with open(bad, "w", encoding="utf-8") as handle:
            handle.write("{nope")
        code, _, err = self.cli(["diff", bad])
        self.assertEqual(code, 2)
        self.assertIn("cannot read", err)

    def test_wrong_shape_writes_no_board(self):
        target = self.path("board.html")
        code, out, _ = self.cli(["build", self.write_board({"directions": "three"}), "-o", target, "--json"])
        self.assertEqual(code, 1)
        self.assertIsNone(json.loads(out)["output"])
        self.assertFalse(os.path.exists(target))
        code, out, _ = self.cli(["diff", self.write_board([1, 2]), "--json"])
        self.assertEqual(code, 1)
        self.assertIn("MB_SHAPE", [f["code"] for f in json.loads(out)["findings"]])

    def test_json_shape(self):
        code, result = self.diff(template())
        self.assertEqual(code, 0)
        for key in ("tool", "version", "command", "board", "hueThreshold", "directions", "pairs", "categoryDefault",
                    "findings", "summary", "pass"):
            self.assertIn(key, result)
        self.assertEqual(result["command"], "diff")
        self.assertEqual(len(result["pairs"]), 3)
        self.assertEqual(result["summary"]["errors"], 0)


if __name__ == "__main__":
    unittest.main()
