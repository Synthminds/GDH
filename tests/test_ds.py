"""Tests for kit/skills/design-system/scripts/ds.py.

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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS_PATH = os.path.join(ROOT, "kit", "skills", "design-system", "scripts", "ds.py")
TEMPLATE = os.path.join(ROOT, "brands", "_template")

_spec = importlib.util.spec_from_file_location("gdh_ds", DS_PATH)
ds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ds)


def run(argv):
    """Run the CLI. Return (exit code, stdout text)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ds.main(argv)
    return code, out.getvalue()


def run_json(argv):
    code, text = run(argv)
    return code, json.loads(text)


def codes(findings, level=None):
    return [f["code"] for f in findings if level is None or f["level"] == level]


def base_doc():
    return json.loads(json.dumps(ds.starter_tokens("Test")))


class TmpCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-ds-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def path(self, *parts):
        return os.path.join(self.tmp, *parts)

    def write(self, name, text):
        p = self.path(name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        return p

    def write_doc(self, doc, name="tokens.json"):
        return self.write(name, json.dumps(doc))


class ColorMath(unittest.TestCase):
    def test_hex_forms(self):
        self.assertEqual(ds.parse_color("#fff").to_css(), "#ffffff")
        self.assertEqual(ds.parse_color("#08262c").rgb255(), (8, 38, 44))
        self.assertAlmostEqual(ds.parse_color("#00000080").alpha, 128 / 255.0, places=4)
        self.assertIsNone(ds.parse_color("#12"))
        self.assertIsNone(ds.parse_color("red"))

    def test_rgb_and_hsl(self):
        self.assertEqual(ds.parse_color("rgb(8 38 44 / 0.08)").to_css(), "rgba(8, 38, 44, 0.08)")
        self.assertEqual(ds.parse_color("rgba(8, 38, 44, 0.08)").to_css(), "rgba(8, 38, 44, 0.08)")
        self.assertEqual(ds.parse_color("rgb(100% 0% 0%)").to_css(), "#ff0000")
        self.assertEqual(ds.parse_color("hsl(210 50% 40%)").to_css(), "#336699")
        self.assertEqual(ds.parse_color("hsl(0, 100%, 50%)").to_css(), "#ff0000")

    def test_oklch_known_values(self):
        # sRGB primaries in OKLCH, from the published OKLab matrices.
        self.assertEqual(ds.parse_color("oklch(0.627955 0.257683 29.2339)").to_css(), "#ff0000")
        self.assertEqual(ds.parse_color("oklch(0.86644 0.294827 142.4953)").to_css(), "#00ff00")
        self.assertEqual(ds.parse_color("oklch(0.452014 0.313214 264.052)").to_css(), "#0000ff")
        self.assertEqual(ds.parse_color("oklch(1 0 0)").to_css(), "#ffffff")
        self.assertEqual(ds.parse_color("oklch(0 0 0)").to_css(), "#000000")
        self.assertEqual(ds.parse_color("oklch(62.7955% 0.257683 29.2339deg)").to_css(), "#ff0000")
        # L = 0.5 with no chroma is the mid gray #636363.
        self.assertEqual(ds.parse_color("oklch(0.5 0 0)").to_css(), "#636363")

    def test_oklch_round_trip(self):
        for hexv in ("#003b4f", "#e8b00f", "#b30003", "#7c828d"):
            c = ds.parse_color(hexv)
            L, C, H = ds.srgb_to_oklch(*c.rgb)
            back = ds.Color(ds.oklch_to_srgb(L, C, H))
            self.assertEqual(back.hex6(), hexv)

    def test_out_of_gamut_is_flagged(self):
        self.assertTrue(ds.parse_color("oklch(0.7 0.4 150)").clipped)
        self.assertFalse(ds.parse_color("oklch(0.7 0.1 150)").clipped)

    def test_nested_function_is_not_a_literal(self):
        self.assertIsNone(ds.parse_color("oklch(calc(0.5 + 0.1) 0.1 20)"))
        self.assertIsNone(ds.parse_color("rgb(var(--x) / 0.5)"))

    def test_contrast_known_values(self):
        black, white = ds.parse_color("#000000"), ds.parse_color("#FFFFFF")
        self.assertAlmostEqual(ds.contrast_ratio(black, white), 21.0, places=6)
        self.assertAlmostEqual(ds.contrast_ratio(white, black), 21.0, places=6)
        gray = ds.contrast_ratio(ds.parse_color("#767676"), white)
        self.assertAlmostEqual(gray, 4.54, places=2)
        self.assertGreaterEqual(gray, 4.5)
        self.assertLess(ds.contrast_ratio(ds.parse_color("#777777"), white), 4.5)
        self.assertAlmostEqual(ds.contrast_ratio(white, white), 1.0, places=6)

    def test_contrast_composites_alpha_text(self):
        half = ds.parse_color("rgba(0, 0, 0, 0.5)")
        ratio = ds.contrast_ratio(half, ds.parse_color("#ffffff"))
        solid = ds.contrast_ratio(ds.parse_color("#808080"), ds.parse_color("#ffffff"))
        self.assertAlmostEqual(ratio, solid, places=1)


class ColorMix(unittest.TestCase):
    def test_srgb(self):
        text, computed, err = ds.resolve_color_mix("color-mix(in srgb, #ff0000 50%, #0000ff)")
        self.assertIsNone(err)
        self.assertEqual(text, "#800080")
        self.assertEqual(len(computed), 1)

    def test_srgb_unequal_weights(self):
        text, _c, err = ds.resolve_color_mix("color-mix(in srgb, #ffffff 25%, #000000)")
        self.assertIsNone(err)
        self.assertEqual(text, "#404040")

    def test_transparent_keeps_color_and_scales_alpha(self):
        text, _c, err = ds.resolve_color_mix("color-mix(in srgb, #003b4f 20%, transparent)")
        self.assertIsNone(err)
        self.assertEqual(text, "rgba(0, 59, 79, 0.2)")

    def test_percentages_under_100_scale_alpha(self):
        text, _c, err = ds.resolve_color_mix("color-mix(in srgb, #ff0000 20%, #ff0000 20%)")
        self.assertIsNone(err)
        self.assertEqual(text, "rgba(255, 0, 0, 0.4)")

    def test_oklch_and_oklab(self):
        text, _c, err = ds.resolve_color_mix("color-mix(in oklab, white, black)")
        self.assertIsNone(err)
        self.assertEqual(text, "#636363")
        text, _c, err = ds.resolve_color_mix("color-mix(in oklch, #ff0000, #ff0000)")
        self.assertIsNone(err)
        self.assertEqual(text, "#ff0000")
        # An achromatic operand has no hue: the mix keeps the hue of the other color.
        text, _c, err = ds.resolve_color_mix("color-mix(in oklch, #0000ff, white)")
        self.assertIsNone(err)
        L, C, H = ds.srgb_to_oklch(*ds.parse_color(text).rgb)
        self.assertAlmostEqual(H, 264.05, delta=1.5)

    def test_oklch_takes_shorter_hue_arc(self):
        text, _c, err = ds.resolve_color_mix(
            "color-mix(in oklch, oklch(0.7 0.1 350), oklch(0.7 0.1 10))")
        self.assertIsNone(err)
        L, C, H = ds.srgb_to_oklch(*ds.parse_color(text).rgb)
        self.assertTrue(H > 355 or H < 5, H)

    def test_nested_and_embedded(self):
        text, _c, err = ds.resolve_color_mix(
            "0 1px 2px color-mix(in srgb, color-mix(in srgb, #fff, #000) 50%, #000)")
        self.assertIsNone(err)
        self.assertTrue(text.startswith("0 1px 2px #"))
        self.assertNotIn("color-mix", text)

    def test_unsupported_space_is_an_error(self):
        _t, _c, err = ds.resolve_color_mix("color-mix(in lch, red, blue)")
        self.assertIn("not supported", err)
        _t, _c, err = ds.resolve_color_mix("color-mix(in srgb, var(--x), blue)")
        self.assertIn("not a literal", err)


class Validate(TmpCase):
    def test_starter_is_clean(self):
        self.assertEqual(ds.validate_doc(base_doc()), [])

    def test_cli_exit_codes(self):
        good = self.write_doc(base_doc())
        code, data = run_json(["validate", good, "--json"])
        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        doc = base_doc()
        doc["color"]["tokens"][0]["value"] = "red"
        bad = self.write_doc(doc, "bad.json")
        code, data = run_json(["validate", bad, "--json"])
        self.assertEqual(code, 1)
        f = data["findings"][0]
        self.assertEqual(f["code"], "COLOR_NAMED")
        self.assertEqual(f["path"], "color.tokens[0]")
        self.assertTrue(f["hint"])
        code, _ = run(["validate", self.path("missing.json")])
        self.assertEqual(code, 2)

    def _color(self, value):
        doc = base_doc()
        doc["color"]["tokens"][0]["value"] = value
        return codes(ds.validate_doc(doc))

    def test_accepted_color_values(self):
        for v in ("#fff", "#ffff", "#08262c", "#08262c80", "rgb(8 38 44)", "rgba(8, 38, 44, 0.5)",
                  "hsl(210 50% 40%)", "oklch(0.7 0.1 200)", "oklch(70% 0.1 200 / 50%)", "{text}"):
            self.assertEqual(self._color(v), [], v)
        self.assertEqual(self._color({"light": "#fff", "dark": "{text}"}), [])

    def test_rejected_color_values(self):
        self.assertEqual(self._color("red"), ["COLOR_NAMED"])
        self.assertEqual(self._color("transparent"), ["COLOR_NAMED"])
        self.assertEqual(self._color("var(--bg)"), ["COLOR_VAR"])
        self.assertEqual(self._color("color-mix(in srgb, #fff, #000)"), ["COLOR_MIX"])
        self.assertEqual(self._color("{nope}"), ["COLOR_ALIAS_MISSING"])
        self.assertEqual(self._color("{bg}"), ["COLOR_ALIAS_SELF"])
        self.assertEqual(self._color("oklch(calc(0.5) 0.1 20)"), ["COLOR_NESTED_FUNCTION"])
        self.assertEqual(self._color("rgb(1 2)"), ["COLOR_SYNTAX"])
        self.assertEqual(self._color("#12"), ["COLOR_HEX"])
        self.assertEqual(self._color(""), ["VALUE_MISSING"])
        self.assertEqual(self._color({"light": "#fff", "dark": "var(--x)"}), ["COLOR_VAR"])
        self.assertEqual(self._color({"light": "#fff", "dark": "#000", "sepia": "#eee"}), ["COLOR_THEME_UNKNOWN"])

    def test_unlisted_function_and_missing_theme_are_warnings(self):
        doc = base_doc()
        doc["color"]["tokens"][0]["value"] = "lab(50% 10 10)"
        self.assertEqual(codes(ds.validate_doc(doc), "warning"), ["COLOR_FUNCTION_UNLISTED"])
        doc["color"]["tokens"][0]["value"] = {"light": "#fff"}
        self.assertEqual(codes(ds.validate_doc(doc), "warning"), ["COLOR_THEME_VALUE_MISSING"])

    def test_alias_cycle(self):
        doc = base_doc()
        doc["color"]["tokens"][0]["value"] = "{surface}"
        doc["color"]["tokens"][1]["value"] = "{bg}"
        self.assertIn("COLOR_ALIAS_CYCLE", codes(ds.validate_doc(doc)))

    def test_names(self):
        for bad in ("-lead", "has space", "a" * 65, "", "caf" + chr(233), ".dot"):
            doc = base_doc()
            doc["spacing"]["tokens"][0]["name"] = bad
            self.assertIn("NAME_INVALID", codes(ds.validate_doc(doc)), bad)
        for good in ("a", "9lives", "space.1", "A_b-c.d", "a" * 64):
            doc = base_doc()
            doc["spacing"]["tokens"][0]["name"] = good
            self.assertEqual(ds.validate_doc(doc), [], good)

    def test_names_unique_across_families_but_not_type(self):
        doc = base_doc()
        doc["radius"]["tokens"][0]["name"] = "space-1"
        f = [x for x in ds.validate_doc(doc) if x["code"] == "NAME_DUPLICATE"]
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["path"], "radius.tokens[0]")
        doc = base_doc()
        doc["spacing"]["tokens"][0]["name"] = "body"  # also a type style name
        self.assertEqual(ds.validate_doc(doc), [])

    def test_lengths(self):
        for good in ("8px", "0.5rem", "1em", "50%", "0", 4, 1.5, "-2px"):
            doc = base_doc()
            doc["spacing"]["tokens"][0]["value"] = good
            self.assertEqual(ds.validate_doc(doc), [], good)
        for bad in ("8pt", "1vw", "calc(1px + 1rem)", "big", "8 px"):
            doc = base_doc()
            doc["radius"]["tokens"][0]["value"] = bad
            self.assertEqual(codes(ds.validate_doc(doc)), ["LENGTH_INVALID"], bad)

    def test_var_and_color_mix_rejected_in_any_family(self):
        doc = base_doc()
        doc["shadow"]["tokens"][0]["value"] = "0 1px 2px var(--shade)"
        self.assertEqual(codes(ds.validate_doc(doc)), ["VALUE_VAR"])
        doc["shadow"]["tokens"][0]["value"] = "0 1px 2px color-mix(in srgb, #000 10%, transparent)"
        self.assertEqual(codes(ds.validate_doc(doc)), ["VALUE_COLOR_MIX"])

    def test_usage_note_missing_is_a_warning(self):
        doc = base_doc()
        del doc["color"]["tokens"][0]["usage"]
        doc["spacing"]["tokens"][0]["usage"] = "  "
        f = ds.validate_doc(doc)
        self.assertEqual(codes(f, "warning"), ["USAGE_MISSING", "USAGE_MISSING"])
        self.assertEqual(codes(f, "error"), [])
        p = self.write_doc(doc)
        self.assertEqual(run(["validate", p])[0], 0)
        self.assertEqual(run(["validate", p, "--strict"])[0], 1)

    def test_dtcg_map_is_reported_clearly(self):
        doc = base_doc()
        doc["spacing"] = {"sm": {"$value": "8px", "$type": "dimension"}}
        doc["color"] = {"brand": {"primary": {"$value": "#003b4f"}}}
        f = [x for x in ds.validate_doc(doc) if x["code"] == "DTCG_MAP"]
        self.assertEqual(sorted(x["path"] for x in f), ["color", "spacing"])
        self.assertIn("cannot read", f[0]["message"])
        self.assertIn("from-dtcg", f[0]["hint"])
        doc = base_doc()
        doc["radius"] = {"sm": {"value": "4px"}}
        self.assertIn("DTCG_MAP", codes(ds.validate_doc(doc)))

    def test_family_shape(self):
        doc = base_doc()
        doc["spacing"] = [{"name": "a", "value": "1px", "usage": "x"}]
        self.assertEqual(codes(ds.validate_doc(doc)), ["FAMILY_SHAPE"])
        doc = base_doc()
        doc["spacing"] = {"note": "no list"}
        self.assertEqual(codes(ds.validate_doc(doc)), ["FAMILY_SHAPE"])
        doc = base_doc()
        del doc["color"]["themes"]
        self.assertIn("THEMES_MISSING", codes(ds.validate_doc(doc)))

    def test_type_shape(self):
        doc = base_doc()
        doc["type"]["groups"][0]["family"] = "serif"
        self.assertEqual(codes(ds.validate_doc(doc)), ["TYPE_GROUP_FAMILY"])
        doc = base_doc()
        doc["type"]["groups"][0]["styles"][0]["fontSize"] = "big"
        self.assertEqual(codes(ds.validate_doc(doc)), ["TYPE_FONT_SIZE"])
        doc = base_doc()
        del doc["type"]["groups"][0]["styles"][0]["fontSize"]
        self.assertEqual(codes(ds.validate_doc(doc)), ["TYPE_FONT_SIZE_MISSING"])
        doc = base_doc()
        doc["type"]["groups"][0]["styles"][0]["fontWeight"] = 1200
        self.assertEqual(codes(ds.validate_doc(doc)), ["TYPE_FONT_WEIGHT"])
        doc = base_doc()
        doc["type"] = {"tokens": [{"name": "body", "value": "16px", "usage": "x"}]}
        self.assertEqual(codes(ds.validate_doc(doc)), ["TYPE_SHAPE"])
        doc = base_doc()
        del doc["type"]["families"]
        self.assertIn("TYPE_FAMILIES_MISSING", codes(ds.validate_doc(doc)))
        doc = base_doc()
        doc["type"]["groups"][1]["styles"][0]["name"] = "display"
        self.assertEqual(codes(ds.validate_doc(doc)), ["TYPE_STYLE_DUPLICATE"])
        doc = base_doc()
        doc["type"]["fonts"] = [{"family": "Inter"}]
        self.assertEqual(codes(ds.validate_doc(doc), "warning"), ["TYPE_FONT_FILE_MISSING"])

    def test_caps(self):
        doc = base_doc()
        doc["color"]["themes"] = [{"id": "t%d" % i, "name": "T"} for i in range(9)]
        doc["color"]["tokens"] = [{"name": "c", "value": "#000", "usage": "x"}]
        self.assertIn("CAP_THEMES", codes(ds.validate_doc(doc)))
        doc = base_doc()
        doc["spacing"]["tokens"] = [{"name": "s%d" % i, "value": "1px", "usage": "x"} for i in range(61)]
        self.assertEqual(codes(ds.validate_doc(doc)), ["CAP_FAMILY_TOKENS"])
        doc = base_doc()
        for i in range(8):
            doc["extra%d" % i] = {"tokens": [{"name": "e%d" % i, "value": "1", "usage": "x"}]}
        self.assertIn("CAP_FAMILIES", codes(ds.validate_doc(doc)))


CSS_SAMPLE = """
/* Brand colors */
:root {
  --navy: #003b4f; /* Primary brand color. */
  --navy-rgb: 0 59 79;
  --white: white;
  --bg: var(--white);
  --fg: var(--navy);
  --link: var(--undefined-thing, var(--navy));
  --tint: color-mix(in srgb, var(--navy) 20%, transparent);
  --mix: color-mix(in oklch, var(--navy), #ffffff 30%);
  --overlay: rgb(var(--navy-rgb) / 0.5);
  --primary: 222.2 47.4% 11.2%;
  --space-1: 4px;
  --space-2: calc(var(--space-1) * 2);
  --space-fluid: clamp(1rem, 2vw, 2rem);
  --radius-md: 0.5rem;
  --shadow-sm: 0 1px 3px rgb(var(--navy-rgb) / 0.1);
  --duration-fast: 120ms;
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
  --font-sans: "Inter", system-ui, sans-serif;
  --text-lg: 1.125rem;
  --text-lg--line-height: 1.5;
  --font-weight-bold: 700;
  --missing: var(--nope);
  --loop-a: var(--loop-b);
  --loop-b: var(--loop-a);
  --crimson: crimson;
}
[data-theme="dark"] { --bg: #08262c; --fg: #e2e5e8; --shadow-sm: 0 1px 3px #000; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --tint: #112233; }
}
@media (min-width: 800px) { :root { --space-1: 8px; } }
.card { --card-pad: 12px; }
@font-face { font-family: "Inter"; src: url("fonts/Inter.woff2") format("woff2"); font-weight: 100 900; }
"""


class FromCss(TmpCase):
    def convert(self, css=CSS_SAMPLE, **kw):
        return ds.css_to_tokens([css], "T", file_names=["a.css"], **kw)

    def colors(self, doc):
        return {t["name"]: t["value"] for t in doc["color"]["tokens"]}

    def test_themes_from_selectors_and_media(self):
        doc, _rep = self.convert()
        self.assertEqual([t["id"] for t in doc["color"]["themes"]], ["light", "dark"])
        c = self.colors(doc)
        self.assertEqual(c["bg"], {"light": "{white}", "dark": "#08262c"})
        self.assertEqual(c["tint"], {"light": "rgba(0, 59, 79, 0.2)", "dark": "#112233"})

    def test_dot_dark_class_and_base_theme_guess(self):
        doc, _ = ds.css_to_tokens([":root{--bg:#fff}.dark{--bg:#000}"], "T")
        self.assertEqual(self.colors(doc)["bg"], {"light": "#fff", "dark": "#000"})
        doc, rep = ds.css_to_tokens([":root{--bg:#000}[data-theme=light]{--bg:#fff}"], "T")
        self.assertEqual([t["id"] for t in doc["color"]["themes"]], ["dark", "light"])
        self.assertEqual(self.colors(doc)["bg"], {"dark": "#000", "light": "#fff"})
        self.assertTrue(any("dark" in a for a in rep["assumed"]))
        doc, _ = ds.css_to_tokens([":root{--bg:#000}"], "T", base_theme="night")
        self.assertEqual([t["id"] for t in doc["color"]["themes"]], ["night"])

    def test_var_chains_and_fallback(self):
        doc, _ = self.convert()
        c = self.colors(doc)
        self.assertEqual(c["fg"], {"light": "{navy}", "dark": "#e2e5e8"})
        self.assertEqual(c["link"], "#003b4f")
        doc, _ = self.convert(no_alias=True)
        self.assertEqual(self.colors(doc)["fg"], {"light": "#003b4f", "dark": "#e2e5e8"})
        self.assertEqual(self.colors(doc)["bg"]["light"], "#ffffff")

    def test_color_mix_is_resolved_to_a_literal(self):
        doc, rep = self.convert()
        c = self.colors(doc)
        self.assertEqual(c["tint"]["light"], "rgba(0, 59, 79, 0.2)")
        self.assertRegex(c["mix"], r"^#[0-9a-f]{6}$")
        expect, _c, _e = ds.resolve_color_mix("color-mix(in oklch, #003b4f, #ffffff 30%)")
        self.assertEqual(c["mix"], expect)
        froms = [x["from"] for x in rep["computed"] if x["name"] == "mix"]
        self.assertEqual(froms, ["color-mix(in oklch, #003b4f, #ffffff 30%)"])

    def test_triplet_forms(self):
        doc, rep = self.convert()
        c = self.colors(doc)
        self.assertEqual(c["overlay"], "rgb(0 59 79 / 0.5)")
        self.assertEqual(ds.parse_color(c["overlay"]).to_css(), "rgba(0, 59, 79, 0.5)")
        self.assertEqual(c["navy-rgb"], "#003b4f")
        self.assertEqual(c["primary"], "hsl(222.2 47.4% 11.2%)")
        self.assertTrue(any("primary" in a for a in rep["assumed"]))
        shadow = doc["shadow"]["tokens"][0]["value"]
        self.assertEqual(shadow, "0 1px 3px rgb(0 59 79 / 0.1)")
        doc, rep = ds.css_to_tokens([":root{--x: 1 2 3}"], "T")
        self.assertEqual(rep["unconverted"][0]["name"], "x")

    def test_classification(self):
        doc, _ = self.convert()
        self.assertEqual([(t["name"], t["value"]) for t in doc["spacing"]["tokens"]],
                         [("space-1", "4px"), ("space-2", "8px")])
        self.assertEqual(doc["radius"]["tokens"][0]["value"], "0.5rem")
        self.assertEqual([t["name"] for t in doc["motion"]["tokens"]], ["duration-fast", "ease-out"])
        self.assertEqual(doc["type"]["families"], {"font-sans": "\"Inter\", system-ui, sans-serif"})
        style = doc["type"]["groups"][0]["styles"][0]
        self.assertEqual((style["name"], style["fontSize"], style["lineHeight"]), ("text-lg", "1.125rem", 1.5))
        self.assertNotIn("fontWeight", style)  # never invented
        self.assertEqual(doc["type"]["fonts"], [{"family": "Inter", "file": "fonts/Inter.woff2", "weight": "100 900"}])
        self.assertEqual(doc["font"]["tokens"][0]["name"], "font-weight-bold")

    def test_usage_comes_from_a_trailing_comment_only(self):
        doc, _ = self.convert()
        usage = {t["name"]: t["usage"] for t in doc["color"]["tokens"]}
        self.assertEqual(usage["navy"], "Primary brand color.")
        self.assertEqual(usage["white"], "")

    def test_everything_not_converted_is_reported(self):
        _doc, rep = self.convert()
        un = {u["name"]: u["reason"] for u in rep["unconverted"]}
        self.assertIn("not defined", un["missing"])
        self.assertIn("cycle", un["loop-a"])
        self.assertIn("cycle", un["loop-b"])
        self.assertIn("named color", un["crimson"])
        self.assertIn("not a length", un["space-fluid"])
        self.assertIn("theme override dropped", un["shadow-sm"])
        skipped = {s["name"]: s["reason"] for s in rep["skipped"]}
        self.assertIn("card-pad", skipped)
        self.assertIn("@media", skipped["space-1"])

    def test_output_is_valid_and_never_holds_var(self):
        doc, _ = self.convert()
        self.assertEqual(codes(ds.validate_doc(doc), "error"), [])
        text = json.dumps(doc)
        self.assertNotIn("var(", text)
        self.assertNotIn("color-mix(", text)

    def test_cli(self):
        css = self.write("a.css", CSS_SAMPLE)
        out = self.path("out", "tokens.json")
        code, data = run_json(["from-css", css, "--name", "T", "-o", out, "--json"])
        self.assertEqual(code, 1)  # the sample holds properties that cannot be converted
        self.assertTrue(os.path.isfile(out))
        self.assertTrue(data["report"]["unconverted"])
        clean = self.write("b.css", ":root{--bg:#fff; /* Page ground. */ --space-1:4px}")
        # The token file already exists and may hold hand-written usage notes: refuse without --force.
        code, _ = run(["from-css", clean, "--name", "T", "-o", out])
        self.assertEqual(code, 2)
        code, _ = run(["from-css", clean, "--name", "T", "-o", out, "--force"])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.isfile(out + ".bak"))
        self.assertEqual(run(["validate", out])[0], 0)

    def test_export_then_from_css_keeps_values(self):
        doc = base_doc()
        css, _f = ds.build_css(doc)
        back, rep = ds.css_to_tokens([css], "Test")
        self.assertEqual(rep["unconverted"], [])
        self.assertEqual([(t["name"], t["value"]) for t in back["color"]["tokens"]],
                         [(t["name"], t["value"]) for t in doc["color"]["tokens"]])
        for fam in ("spacing", "radius", "shadow", "motion"):
            self.assertEqual([(t["name"], t["value"]) for t in back[fam]["tokens"]],
                             [(t["name"], t["value"]) for t in doc[fam]["tokens"]])
        want = [(s["name"], s["fontSize"], s["lineHeight"], s["fontWeight"])
                for g in doc["type"]["groups"] for s in g["styles"]]
        got = [(s["name"], s["fontSize"], s["lineHeight"], s["fontWeight"])
               for g in back["type"]["groups"] for s in g["styles"]]
        self.assertEqual(got, want)


def rich_doc():
    doc = base_doc()
    doc["meta"] = {"source": "test"}
    doc["color"]["tokens"].append({"name": "link", "value": "{accent}", "usage": "Links. Text on bg."})
    doc["color"]["tokens"].append({"name": "brand.ok", "value": "oklch(0.7 0.1 200)", "usage": "Chart fill."})
    doc["color"]["tokens"].append({"name": "veil", "value": "rgba(8, 38, 44, 0.08)", "usage": "Scrim."})
    doc["spacing"]["note"] = "Four steps."
    doc["spacing"]["tokens"].append({"name": "space-em", "value": "1.5em", "usage": "Paragraph gap.", "since": "0.2.0"})
    doc["shadow"]["tokens"].append({"name": "shadow-ring", "value": "0 0 0 2px #1d55b0, inset 0 1px 0 rgba(255, 255, 255, 0.2)", "usage": "Focus."})
    doc["motion"]["tokens"].append({"name": "ease-all", "value": "0.2s ease", "usage": "Links."})
    doc["layout"] = {"tokens": [{"name": "measure", "value": "65ch", "usage": "Line length."},
                                {"name": "z-top", "value": 10, "usage": "Overlays."}]}
    doc["type"]["groups"][0]["note"] = "Tight headings."
    doc["type"]["groups"][0]["styles"][0]["letterSpacing"] = "-0.01em"
    doc["type"]["groups"][0]["styles"][0]["sample"] = "Ready"
    doc["type"]["fonts"] = [{"family": "Inter", "file": "fonts/Inter.woff2", "weight": "400 700", "style": "normal"}]
    return doc


class Dtcg(TmpCase):
    def test_round_trip_is_exact(self):
        for doc in (base_doc(), rich_doc()):
            dtcg, _notes = ds.claude_to_dtcg(doc)
            back, rep = ds.dtcg_to_claude(json.loads(json.dumps(dtcg)))
            self.assertEqual(rep["unconverted"], [])
            self.assertEqual(json.loads(json.dumps(back)), doc)

    def test_round_trip_cli(self):
        src = self.write_doc(rich_doc())
        mid, out = self.path("t.tokens.json"), self.path("back.json")
        self.assertEqual(run(["to-dtcg", src, "-o", mid])[0], 0)
        self.assertEqual(run(["from-dtcg", mid, "-o", out])[0], 0)
        with open(out) as fh:
            self.assertEqual(json.load(fh), rich_doc())
        self.assertEqual(run(["validate", out])[0], 0)

    def test_to_dtcg_uses_the_2025_10_object_forms(self):
        dtcg, _ = ds.claude_to_dtcg(rich_doc())
        bg = dtcg["color"]["bg"]
        self.assertEqual(bg["$type"], "color")
        self.assertEqual(bg["$value"], {"colorSpace": "srgb", "components": [1, 1, 1], "hex": "#ffffff"})
        self.assertEqual(bg["$description"], "Page ground.")
        self.assertEqual(dtcg["color"]["link"]["$value"], "{color.accent}")
        ok = dtcg["color"]["brand-ok"]  # a dot is not legal in a DTCG name
        self.assertEqual(ok["$value"]["colorSpace"], "oklch")
        self.assertEqual(ok["$value"]["components"], [0.7, 0.1, 200])
        self.assertEqual(ok["$extensions"]["gdh"]["name"], "brand.ok")
        self.assertEqual(dtcg["color"]["veil"]["$value"]["alpha"], 0.08)
        self.assertEqual(dtcg["spacing"]["space-1"]["$value"], {"value": 4, "unit": "px"})
        self.assertEqual(dtcg["spacing"]["space-1"]["$type"], "dimension")
        self.assertNotIn("$type", dtcg["spacing"]["space-em"])  # em is not a DTCG unit
        self.assertEqual(dtcg["motion"]["duration-fast"]["$value"], {"value": 120, "unit": "ms"})
        self.assertEqual(dtcg["motion"]["ease-standard"]["$value"], [0.2, 0, 0, 1])
        self.assertEqual(dtcg["shadow"]["shadow-sm"]["$type"], "shadow")
        self.assertEqual(len(dtcg["shadow"]["shadow-ring"]["$value"]), 2)
        self.assertEqual(dtcg["type"]["family"]["sans"]["$value"][0], "system-ui")
        body = dtcg["type"]["style"]["Text"]["body"]["$value"]
        self.assertEqual(body["fontFamily"], "{type.family.sans}")
        self.assertEqual(body["fontSize"], {"value": 16, "unit": "px"})

    def test_to_dtcg_refuses_an_invalid_file(self):
        doc = base_doc()
        doc["color"]["tokens"][0]["value"] = "var(--x)"
        src = self.write_doc(doc)
        out = self.path("o.json")
        self.assertEqual(run(["to-dtcg", src, "-o", out])[0], 1)
        self.assertFalse(os.path.exists(out))

    def test_edited_dtcg_value_wins(self):
        dtcg, _ = ds.claude_to_dtcg(base_doc())
        dtcg = json.loads(json.dumps(dtcg))
        dtcg["spacing"]["space-1"]["$value"] = {"value": 6, "unit": "px"}
        dtcg["color"]["accent"]["$value"] = {"colorSpace": "srgb", "components": [1, 0, 0]}
        back, rep = ds.dtcg_to_claude(dtcg)
        self.assertEqual(back["spacing"]["tokens"][0]["value"], "6px")
        accent = [t for t in back["color"]["tokens"] if t["name"] == "accent"][0]
        self.assertEqual(accent["value"], "#ff0000")
        self.assertEqual(len(rep["notes"]), 2)

    FOREIGN = {
        "color": {"$type": "color",
                  "brand": {"primary": {"$value": {"colorSpace": "srgb", "components": [0, 0.231373, 0.309804], "hex": "#003b4f"},
                                        "$description": "Brand"},
                            "wide": {"$value": {"colorSpace": "display-p3", "components": [1, 0, 0], "hex": "#ff0000"}},
                            "lost": {"$value": {"colorSpace": "display-p3", "components": [1, 0, 0]}}},
                  "text": {"$value": "{color.brand.primary}"},
                  "legacy": {"$value": "#ABCDEF"}},
        "spacing": {"sm": {"$type": "dimension", "$value": {"value": 8, "unit": "px"}}},
        "radius": {"md": {"$type": "dimension", "$value": "0.5rem"}},
        "font": {"body": {"$type": "fontFamily", "$value": ["Inter Tight", "sans-serif"]}},
        "text": {"body": {"$type": "typography",
                          "$value": {"fontFamily": "{font.body}", "fontSize": {"value": 16, "unit": "px"},
                                     "fontWeight": 400, "lineHeight": 1.5}}},
        "motion": {"fast": {"$type": "duration", "$value": {"value": 120, "unit": "ms"}},
                   "ease": {"$type": "cubicBezier", "$value": [0.2, 0, 0, 1]}},
        "shadow": {"sm": {"$type": "shadow", "$value": {
            "color": {"colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1},
            "offsetX": {"value": 0, "unit": "px"}, "offsetY": {"value": 1, "unit": "px"},
            "blur": {"value": 3, "unit": "px"}, "spread": {"value": 0, "unit": "px"}}}},
        "edge": {"card": {"$type": "border", "$value": {"color": "#000", "width": "1px", "style": "solid"}}},
    }

    def test_foreign_dtcg_file(self):
        doc, rep = ds.dtcg_to_claude(copy.deepcopy(self.FOREIGN), name="F")
        c = {t["name"]: t for t in doc["color"]["tokens"]}
        self.assertEqual(c["color-brand-primary"]["value"], "#003b4f")
        self.assertEqual(c["color-brand-primary"]["usage"], "Brand")
        self.assertEqual(c["color-text"]["value"], "{color-brand-primary}")
        self.assertEqual(c["color-legacy"]["value"], "#ABCDEF")
        self.assertEqual(c["color-brand-wide"]["value"], "#ff0000")
        self.assertEqual(doc["spacing"]["tokens"][0], {"name": "spacing-sm", "value": "8px", "usage": ""})
        self.assertEqual(doc["radius"]["tokens"][0]["value"], "0.5rem")
        self.assertEqual(doc["shadow"]["tokens"][0]["value"], "0 1px 3px rgba(0, 0, 0, 0.1)")
        self.assertEqual([t["value"] for t in doc["motion"]["tokens"]], ["120ms", "cubic-bezier(0.2, 0, 0, 1)"])
        self.assertEqual(doc["type"]["families"], {"font-body": "\"Inter Tight\", sans-serif"})
        self.assertEqual(doc["type"]["groups"][0]["styles"][0]["fontSize"], "16px")
        un = {u["name"]: u["reason"] for u in rep["unconverted"]}
        self.assertIn("color.brand.lost", un)
        self.assertIn("edge.card", un)
        self.assertEqual(codes(ds.validate_doc(doc), "error"), [])

    def test_theme_files(self):
        dark = {"color": {"$type": "color", "brand": {"primary": {"$value": "#88ccdd"}}}}
        doc, _ = ds.dtcg_to_claude(copy.deepcopy(self.FOREIGN), theme_files=[("dark", dark)])
        self.assertEqual([t["id"] for t in doc["color"]["themes"]], ["light", "dark"])
        c = {t["name"]: t["value"] for t in doc["color"]["tokens"]}
        self.assertEqual(c["color-brand-primary"], {"light": "#003b4f", "dark": "#88ccdd"})
        self.assertEqual(c["color-legacy"], "#ABCDEF")
        main = self.write("m.json", json.dumps(self.FOREIGN))
        dfile = self.write("d.json", json.dumps(dark))
        out = self.path("o.json")
        code, data = run_json(["from-dtcg", main, "-o", out, "--theme", "dark=" + dfile, "--json"])
        self.assertEqual(code, 1)  # two tokens cannot be converted and are reported
        self.assertEqual(len(data["report"]["unconverted"]), 2)

    def test_legacy_value_keys(self):
        doc, rep = ds.dtcg_to_claude({"color": {"primary": {"value": "#112233", "type": "color", "description": "Brand."}},
                                      "size": {"gap": {"value": "8px"}}})
        self.assertEqual(doc["color"]["tokens"][0], {"name": "color-primary", "value": "#112233", "usage": "Brand."})
        self.assertEqual(rep["unconverted"], [])


class Export(TmpCase):
    def test_css(self):
        doc = rich_doc()
        css, findings = ds.build_css(doc)
        self.assertEqual(findings, [])
        first = css.splitlines()[0]
        self.assertTrue(first.startswith("/* Generated from tokens.json") and first.endswith("*/"), first)
        self.assertIn(":root {", css)
        self.assertIn('[data-theme="light"] {', css)
        self.assertIn('[data-theme="dark"] {', css)
        self.assertIn("@media (prefers-color-scheme: dark)", css)
        self.assertIn("--link: var(--accent);", css)
        self.assertIn("--brand-ok: oklch(0.7 0.1 200);", css)
        self.assertIn("--type-body-size: 16px;", css)
        self.assertIn('@font-face', css)
        root = css.split(":root {")[1].split("}")[0]
        self.assertIn("--bg: #ffffff;", root)
        dark = css.split('[data-theme="dark"] {')[1].split("}")[0]
        self.assertIn("--bg: #111318;", dark)
        self.assertIn("--link: var(--accent);", dark)  # aliases are redeclared so they follow the theme
        self.assertEqual(css.count("{"), css.count("}"))

    def test_css_name_collision_is_an_error(self):
        doc = base_doc()
        doc["color"]["tokens"].append({"name": "a.b", "value": "#000", "usage": "x"})
        doc["color"]["tokens"].append({"name": "a-b", "value": "#111", "usage": "x"})
        _css, findings = ds.build_css(doc)
        self.assertEqual(codes(findings), ["CSS_NAME_COLLISION"])

    def test_tailwind(self):
        tw = ds.build_tailwind(base_doc())
        self.assertTrue(tw.splitlines()[0].startswith("/* Generated from"))
        self.assertIn("@theme inline {", tw)
        self.assertIn("--color-bg: var(--bg);", tw)
        self.assertIn("--spacing-1: 4px;", tw)
        self.assertIn("--radius-md: 8px;", tw)
        self.assertIn("--shadow-sm:", tw)
        self.assertIn("--text-body: 16px;", tw)
        self.assertIn("--text-body--line-height: 1.5;", tw)
        self.assertIn("--ease-standard: cubic-bezier(0.2, 0, 0, 1);", tw)
        self.assertIn("--font-sans:", tw)

    def test_flat_json_resolves_aliases_per_theme(self):
        flat = ds.build_flat(rich_doc())
        self.assertEqual(list(flat.keys()), ["light", "dark"])
        self.assertEqual(flat["light"]["link"], "#1d55b0")
        self.assertEqual(flat["dark"]["link"], "#8fb4ff")
        self.assertEqual(flat["dark"]["space-1"], "4px")
        self.assertEqual(flat["light"]["type.body.fontSize"], "16px")

    def test_cli_writes_three_files(self):
        src = self.write_doc(base_doc())
        css, tw, flat = self.path("o", "tokens.css"), self.path("o", "theme.css"), self.path("o", "flat.json")
        code, _ = run(["export", src, "--css", css, "--tailwind", tw, "--json", flat])
        self.assertEqual(code, 0)
        for p in (css, tw, flat):
            self.assertTrue(os.path.getsize(p) > 0)
        with open(flat) as fh:
            self.assertIn("light", json.load(fh))
        self.assertEqual(run(["export", src])[0], 2)
        doc = base_doc()
        doc["color"]["tokens"][0]["value"] = "red"
        bad = self.write_doc(doc, "bad.json")
        self.assertEqual(run(["export", bad, "--css", self.path("x.css")])[0], 1)
        self.assertFalse(os.path.exists(self.path("x.css")))


class Contrast(TmpCase):
    def test_pairs_from_usage_notes(self):
        pairs = ds.pairs_from_usage(base_doc())
        got = set((p["fg"], p["bg"], p["kind"]) for p in pairs)
        self.assertIn(("text", "bg", "text"), got)
        self.assertIn(("text", "surface", "text"), got)
        self.assertIn(("on-accent", "accent", "text"), got)
        self.assertIn(("border", "surface", "ui"), got)
        self.assertEqual(len(pairs), 11)

    def test_usage_note_forms(self):
        doc = base_doc()
        t = doc["color"]["tokens"]
        t[3]["usage"] = "Body text on `bg`, surface, and accent in both themes."
        t[4]["usage"] = "Large text on bg. Text on nothing-here."
        got = set((p["fg"], p["bg"], p["kind"]) for p in ds.pairs_from_usage(doc))
        self.assertTrue({("text", "bg", "text"), ("text", "surface", "text"), ("text", "accent", "text"),
                         ("text-muted", "bg", "large")} <= got)
        self.assertFalse(any(p["fg"] == "text-muted" and p["kind"] == "text" for p in ds.pairs_from_usage(doc)))

    def test_known_ratios_through_the_cli(self):
        doc = {"name": "K", "color": {"themes": [{"id": "light", "name": "Light"}], "tokens": [
            {"name": "white", "value": "#FFFFFF", "usage": "Ground."},
            {"name": "black", "value": "#000000", "usage": "Text on white."},
            {"name": "gray", "value": "#767676", "usage": "Text on white."},
            {"name": "gray-alias", "value": "{gray}", "usage": "Text on white."},
            {"name": "ok-red", "value": "oklch(0.627955 0.257683 29.2339)", "usage": "Large text on white."},
            {"name": "hsl-blue", "value": "hsl(240 100% 50%)", "usage": "Text on white."},
            {"name": "rgb-gray", "value": "rgb(119 119 119)", "usage": "Text on white."}]}}
        src = self.write_doc(doc)
        code, data = run_json(["contrast", src, "--json"])
        self.assertEqual(code, 1)
        r = {x["fg"]: x for x in data["results"]}
        self.assertEqual(r["black"]["ratio"], 21.0)
        self.assertEqual(r["gray"]["ratio"], 4.54)
        self.assertTrue(r["gray"]["pass"])
        self.assertEqual(r["gray-alias"]["ratio"], 4.54)
        self.assertEqual(r["ok-red"]["ratio"], 3.99)   # #ff0000 on white
        self.assertTrue(r["ok-red"]["pass"])           # large text needs 3:1
        self.assertFalse(r["ok-red"]["passNormalText"])
        self.assertEqual(r["hsl-blue"]["ratio"], 8.59)  # #0000ff on white
        self.assertEqual(r["rgb-gray"]["ratio"], 4.47)  # #777777 on white
        self.assertFalse(r["rgb-gray"]["pass"])
        self.assertEqual(data["failed"], 1)

    def test_every_theme_is_checked(self):
        doc = base_doc()
        doc["color"]["tokens"][4]["value"]["dark"] = "#3a3d44"  # muted text that fails on dark only
        src = self.write_doc(doc)
        code, data = run_json(["contrast", src, "--json"])
        self.assertEqual(code, 1)
        bad = [(x["theme"], x["fg"]) for x in data["results"] if not x["pass"]]
        self.assertEqual(set(bad), {("dark", "text-muted")})
        self.assertEqual(data["checked"], 22)

    def test_pairs_file_text_and_json(self):
        src = self.write_doc(base_doc())
        pf = self.write("pairs.txt", "# pairs\ntext on bg\naccent on surface large\n#767676 on #ffffff\n")
        code, data = run_json(["contrast", src, "--pairs", pf, "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(data["pairs"], 3)
        self.assertEqual(data["results"][-1]["ratio"], 4.54)
        pj = self.write("pairs.json", json.dumps([{"fg": "text-muted", "bg": "bg", "themes": ["dark"]},
                                                  {"fg": "bg", "bg": "surface", "kind": "ui"}]))
        code, data = run_json(["contrast", src, "--pairs", pj, "--json"])
        self.assertEqual(code, 1)
        self.assertEqual(data["checked"], 3)
        self.assertEqual(run(["contrast", src, "--pairs", self.write("bad.txt", "nonsense line here ok\n")])[0], 2)

    def test_no_pairs_and_unknown_token_fail(self):
        doc = base_doc()
        for t in doc["color"]["tokens"]:
            t["usage"] = "A color."
        src = self.write_doc(doc)
        self.assertEqual(run(["contrast", src])[0], 1)
        pf = self.write("p.txt", "ghost on bg\n")
        code, data = run_json(["contrast", src, "--pairs", pf, "--json"])
        self.assertEqual(code, 1)
        self.assertIn("ghost", data["results"][0]["error"])

    def test_translucent_ground_is_not_scored(self):
        doc = base_doc()
        doc["color"]["tokens"][1]["value"] = "rgba(0, 0, 0, 0.1)"
        res = ds.check_contrast(doc, [{"fg": "text", "bg": "surface", "kind": "text"}])
        self.assertIsNone(res[0]["ratio"])
        self.assertFalse(res[0]["pass"])

    def test_starter_passes(self):
        src = self.write_doc(base_doc())
        self.assertEqual(run(["contrast", src])[0], 0)


class DesignMd(TmpCase):
    def test_front_matter_and_sections(self):
        text, findings = ds.build_design_md(rich_doc(), ds.starter_readme("Test"))
        lines = text.splitlines()
        self.assertEqual(lines[0], "---")
        end = lines.index("---", 1)
        front = lines[1:end]
        tops = [l.split(":")[0] for l in front if not l.startswith(" ")]
        self.assertEqual(tops, ["name", "description", "version", "colors", "typography", "spacing", "rounded"])
        self.assertIn('  bg: "#ffffff"', front)
        self.assertIn('  link: "#1d55b0"', front)          # alias resolved
        self.assertIn('  "brand.ok": "%s"' % ds.parse_color("oklch(0.7 0.1 200)").hex6(), front)  # oklch as hex
        self.assertIn('  space-1: "4px"', front)
        self.assertIn('  radius-md: "8px"', front)
        self.assertIn("    fontSize: \"16px\"", front)
        self.assertIn("    lineHeight: 1.5", front)
        for h in ("## Overview", "## Colors", "## Typography", "## Layout", "## Elevation", "## Shapes",
                  "## Motion", "## Components", "## Do's and Don'ts"):
            self.assertIn(h, lines, h)
        self.assertIn("| `text` on `bg` | light | 17.58:1 | 4.5:1 (text) | pass |", lines)
        self.assertIn("- Use `bg` for the page ground and `surface` for raised ground.", lines)
        self.assertEqual(codes(findings), ["README_TODO"])
        self.assertNotIn("<!--", text)
        text.encode("ascii")

    def test_without_readme(self):
        text, findings = ds.build_design_md(base_doc())
        self.assertEqual(findings, [])
        self.assertIn('description: "Test design system."', text)
        self.assertIn("- Use a named token for every color", text)

    def test_cli(self):
        src = self.write_doc(base_doc())
        readme = self.write("README.md", "A calm brand.\n\n## Usage rules\n\n- Use `bg`.\n")
        out = self.path("DESIGN.md")
        self.assertEqual(run(["design-md", src, "--readme", readme, "-o", out])[0], 0)
        with open(out) as fh:
            text = fh.read()
        self.assertIn('description: "A calm brand."', text)
        self.assertIn("- Use `bg`.", text)

    def test_refuses_to_overwrite_a_hand_written_design_md(self):
        src = self.write_doc(base_doc())
        hand = "# DESIGN.md\n\nOur rules, written by hand.\n"
        out = self.write("DESIGN.md", hand)
        code, text = run_json(["design-md", src, "-o", out, "--json"])
        self.assertEqual(code, 2)
        self.assertIn("--force", text["error"])
        with open(out) as fh:
            self.assertEqual(fh.read(), hand)
        self.assertEqual(run(["design-md", src, "-o", out, "--force"])[0], 0)
        with open(out) as fh:
            self.assertIn(ds.DESIGN_MD_MARK, fh.read())

    def test_replaces_its_own_output_and_the_project_template(self):
        src = self.write_doc(base_doc())
        out = self.path("DESIGN.md")
        self.assertEqual(run(["design-md", src, "-o", out])[0], 0)
        self.assertEqual(run(["design-md", src, "-o", out])[0], 0)
        template = os.path.join(ROOT, "kit", "templates", "project", "DESIGN.md")
        with open(template, encoding="utf-8") as fh:
            target = self.write("project/DESIGN.md", fh.read())
        self.assertEqual(run(["design-md", src, "-o", target])[0], 0)
        with open(target) as fh:
            self.assertNotIn("status: template", fh.read())


SHADCN_V3 = """@tailwind base;
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
  }
}
"""

SHADCN_V4 = """@import "tailwindcss";
@theme inline {
  --color-background: var(--background);
  --radius-lg: var(--radius);
}
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
}
.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
}
"""


class SafeWrite(TmpCase):
    """Review finding: export, specimen, from-css, from-dtcg and to-dtcg replaced any file at the output path."""

    def hand(self, name, text):
        return self.write(name, text)

    def assert_kept(self, path, text):
        with open(path, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), text)

    def test_export_refuses_hand_files_and_writes_nothing(self):
        src = self.write_doc(base_doc())
        css = self.hand("tokens.css", "/* hand tweak */\n:root { --x: 1px; }\n")
        flat = self.path("flat.json")
        code, data = run_json(["export", src, "--css", css, "--json", flat, "--report-json"])
        self.assertEqual(code, 2)
        self.assertIn("--force", data["error"])
        self.assert_kept(css, "/* hand tweak */\n:root { --x: 1px; }\n")
        self.assertFalse(os.path.exists(flat))

    def test_export_replaces_its_own_output(self):
        src = self.write_doc(base_doc())
        css, tw, flat = self.path("tokens.css"), self.path("theme.css"), self.path("flat.json")
        argv = ["export", src, "--css", css, "--tailwind", tw, "--json", flat]
        self.assertEqual(run(argv)[0], 0)
        self.assertEqual(run(argv)[0], 0)
        self.assertFalse(os.path.exists(css + ".bak"))

    def test_force_keeps_a_backup(self):
        src = self.write_doc(base_doc())
        css = self.hand("tokens.css", "/* hand tweak */\n")
        code, data = run_json(["export", src, "--css", css, "--force", "--report-json"])
        self.assertEqual(code, 0)
        self.assertEqual(data["backups"], [css + ".bak"])
        self.assert_kept(css + ".bak", "/* hand tweak */\n")

    def test_flat_json_that_is_not_the_export_shape_is_refused(self):
        src = self.write_doc(base_doc())
        flat = self.hand("flat.json", json.dumps({"settings": {"x": {"y": 1}}}))
        self.assertEqual(run(["export", src, "--json", flat])[0], 2)

    def test_specimen(self):
        src = self.write_doc(base_doc())
        page = self.hand("specimen.html", "<!doctype html><p>My page</p>")
        self.assertEqual(run(["specimen", src, "-o", page])[0], 2)
        self.assert_kept(page, "<!doctype html><p>My page</p>")
        other = self.path("own.html")
        self.assertEqual(run(["specimen", src, "-o", other])[0], 0)
        self.assertEqual(run(["specimen", src, "-o", other])[0], 0)
        self.assertEqual(run(["specimen", src, "-o", page, "--force"])[0], 0)
        self.assert_kept(page + ".bak", "<!doctype html><p>My page</p>")

    def test_from_css_and_from_dtcg_never_replace_a_token_file_silently(self):
        tokens = self.write_doc(base_doc())
        with open(tokens, encoding="utf-8") as fh:
            before = fh.read()
        css = self.write("a.css", ":root{--bg:#fff; /* Page ground. */}")
        self.assertEqual(run(["from-css", css, "--name", "T", "-o", tokens])[0], 2)
        dtcg = self.path("t.dtcg.json")
        self.assertEqual(run(["to-dtcg", tokens, "-o", dtcg])[0], 0)
        self.assertEqual(run(["from-dtcg", dtcg, "-o", tokens])[0], 2)
        self.assert_kept(tokens, before)

    def test_to_dtcg_replaces_its_own_file_but_not_another(self):
        tokens = self.write_doc(base_doc())
        dtcg = self.path("t.dtcg.json")
        self.assertEqual(run(["to-dtcg", tokens, "-o", dtcg])[0], 0)
        self.assertEqual(run(["to-dtcg", tokens, "-o", dtcg])[0], 0)
        other = self.hand("other.json", json.dumps({"color": {"$type": "color", "a": {"$value": "#fff"}}}))
        self.assertEqual(run(["to-dtcg", tokens, "-o", other])[0], 2)

    def test_symbolic_link_target_is_refused(self):
        src = self.write_doc(base_doc())
        real = self.hand("real.css", "/* Generated from tokens.json by ds.py. */\n")
        link = self.path("link.css")
        os.symlink(real, link)
        self.assertEqual(run(["export", src, "--css", link, "--force"])[0], 2)


SHADCN_V3_MIXED = """:root {
  --primary: 222.2 47.4% 11.2%;
  --brand-rgb: 37, 99, 235;
  --ring: 37 99 235;
}
.dark {
  --primary: 210 40% 98%;
  --brand-rgb: 147, 197, 253;
}
.btn { background: hsl(var(--primary)); box-shadow: 0 0 0 2px rgb(var(--brand-rgb) / .5); outline-color: rgb(var(--ring)); }
"""


class ChannelForms(TmpCase):
    """Review finding: from-css then export turned channel triplets into hsl() and hex, and lost .dark."""

    def convert(self, css):
        src = self.write("app.css", css)
        tokens = self.path("tokens.json")
        code, data = run_json(["from-css", src, "--name", "App", "-o", tokens, "--json"])
        self.assertEqual(code, 0, data)
        with open(tokens) as fh:
            return tokens, json.load(fh)

    def export(self, tokens, *extra):
        out = self.path("out-%d.css" % len(os.listdir(self.tmp)))
        self.assertEqual(run(["export", tokens, "--css", out] + list(extra))[0], 0)
        with open(out) as fh:
            return fh.read()

    def test_channels_and_selector_survive_a_round_trip(self):
        tokens, doc = self.convert(SHADCN_V3_MIXED)
        self.assertEqual(doc["meta"]["css"]["channels"]["primary"]["function"], "hsl")
        self.assertEqual(doc["meta"]["css"]["channels"]["brand-rgb"]["separator"], ", ")
        self.assertEqual(doc["meta"]["css"]["themeSelectors"], {"dark": ".dark"})
        css = self.export(tokens)
        self.assertIn("--primary: 222.2 47.4% 11.2%;", css)
        self.assertIn("--brand-rgb: 37, 99, 235;", css)
        self.assertIn("--ring: 37 99 235;", css)
        dark = css[css.index(".dark {"):]
        self.assertIn("--primary: 210 40% 98%;", dark)
        self.assertIn("--brand-rgb: 147, 197, 253;", dark)
        self.assertNotIn("data-theme", css)
        self.assertNotIn("prefers-color-scheme", css)
        # Every var() use in the source still resolves to a valid color after the round trip.
        for fn, name in (("hsl", "primary"), ("rgb", "brand-rgb"), ("rgb", "ring")):
            value = re.search(r"--%s: ([^;]+);" % re.escape(name), css).group(1)
            self.assertIsNotNone(ds.parse_color("%s(%s)" % (fn, value)), name)

    def test_tailwind_wraps_channel_tokens(self):
        tokens, _doc = self.convert(SHADCN_V3_MIXED)
        out = self.path("theme.css")
        self.assertEqual(run(["export", tokens, "--tailwind", out])[0], 0)
        with open(out) as fh:
            text = fh.read()
        self.assertIn("--color-primary: hsl(var(--primary));", text)
        self.assertIn("--color-brand-rgb: rgb(var(--brand-rgb));", text)

    def test_edited_hex_is_written_back_as_channels(self):
        tokens, doc = self.convert(SHADCN_V3_MIXED)
        for tok in doc["color"]["tokens"]:
            if tok["name"] == "brand-rgb":
                tok["value"] = {"light": "#ff0000", "dark": "#00ff00"}
        with open(tokens, "w") as fh:
            json.dump(doc, fh)
        css = self.export(tokens)
        self.assertIn("--brand-rgb: 255, 0, 0;", css)
        self.assertIn("--brand-rgb: 0, 255, 0;", css)

    def test_theme_selector_and_no_media_flags(self):
        doc = base_doc()
        tokens = self.write_doc(doc)
        css = self.export(tokens, "--theme-selector", ".theme-{id}", "--no-media")
        self.assertIn(".theme-dark {", css)
        self.assertIn(".theme-light {", css)
        self.assertNotIn("prefers-color-scheme", css)
        self.assertNotIn("data-theme", css)
        self.assertIn("prefers-color-scheme", self.export(tokens))
        self.assertEqual(run(["export", tokens, "--css", self.path("x.css"), "--theme-selector", ".dark"])[0], 2)

    def test_media_dark_source_keeps_a_media_block(self):
        tokens, doc = self.convert(":root{--bg:#ffffff; /* Page ground. */}\n"
                                   "@media (prefers-color-scheme: dark){:root{--bg:#111111;}}")
        self.assertEqual(doc["meta"]["css"]["mediaThemes"], ["dark"])
        css = self.export(tokens)
        self.assertIn("@media (prefers-color-scheme: dark) {\n  :root {", css)


class ContrastInput(TmpCase):
    """Review finding: malformed pairs crashed the command or fell back to a weaker threshold."""

    def contrast(self, pairs):
        src = self.write_doc(base_doc())
        path = self.write("pairs.json", json.dumps(pairs))
        return run(["contrast", src, "--pairs", path, "--json"])

    def test_unknown_kind_is_refused_not_weakened(self):
        code, text = self.contrast([{"fg": "text-muted", "bg": "bg", "kind": "txt"}])
        self.assertEqual(code, 2)
        self.assertIn("kind", json.loads(text)["error"])

    def test_malformed_entries_are_refused(self):
        for pairs in (["text on bg"], [{"fg": "text"}], [{"fg": 3, "bg": "bg"}], {"pairs": "text on bg"},
                      [{"fg": "text", "bg": "bg", "themes": [1]}]):
            code, text = self.contrast(pairs)
            self.assertEqual(code, 2, pairs)
            self.assertFalse(json.loads(text)["ok"])

    def test_unknown_theme_fails_instead_of_checking_nothing(self):
        code, text = self.contrast([{"fg": "text", "bg": "bg", "themes": ["sepia"]}])
        data = json.loads(text)
        self.assertEqual(code, 1)
        self.assertIn("sepia", data["results"][0]["error"])

    def test_a_single_theme_string_is_one_theme(self):
        code, text = self.contrast([{"fg": "text", "bg": "bg", "themes": "dark"}])
        self.assertEqual(code, 0)
        self.assertEqual([r["theme"] for r in json.loads(text)["results"]], ["dark"])


class Scaffold(TmpCase):
    def test_validate_warns_on_the_init_colors(self):
        src = self.write_doc(base_doc())
        code, data = run_json(["validate", src, "--json"])
        self.assertEqual(code, 0)
        self.assertIn("DS_SCAFFOLD_VALUE", codes(data["findings"], "warning"))
        self.assertEqual(run(["validate", src, "--strict"])[0], 1)

    def test_a_chosen_palette_passes(self):
        doc = base_doc()
        for index, tok in enumerate(doc["color"]["tokens"]):
            tok["value"] = {"light": "#%02x2030" % (index * 20), "dark": "#%02xa0b0" % (index * 20)}
        self.assertEqual(ds.scaffold_findings(doc), [])


class ShadcnRoundTrip(TmpCase):
    def round_trip(self, css):
        src = self.write("globals.css", css)
        tokens = self.path("tokens.json")
        code, report = run_json(["from-css", src, "--name", "Shadcn", "-o", tokens, "--json"])
        self.assertEqual(code, 0, report)
        self.assertEqual(report["report"]["unconverted"], [])
        out_css, out_tw = self.path("tokens.css"), self.path("theme.css")
        self.assertEqual(run(["export", tokens, "--css", out_css, "--tailwind", out_tw])[0], 0)
        with open(tokens) as fh:
            doc = json.load(fh)
        with open(out_css) as fh:
            text = fh.read()
        return doc, text

    def test_v3_hsl_triplets(self):
        doc, text = self.round_trip(SHADCN_V3)
        self.assertEqual([t["id"] for t in doc["color"]["themes"]], ["light", "dark"])
        # Review finding: the triplets stay bare and the .dark selector is kept, so hsl(var(--x)) still resolves.
        self.assertIn("--background: 0 0% 100%;", text)
        dark = text[text.index(".dark {"):]
        self.assertIn("--background: 222.2 84% 4.9%;", dark)
        self.assertNotIn("data-theme", text)
        self.assertNotIn("prefers-color-scheme", text)
        self.assertIn("--radius: 0.5rem;", text)

    def test_v4_oklch_and_theme_aliases(self):
        doc, text = self.round_trip(SHADCN_V4)
        names = [t["name"] for t in doc["color"]["tokens"]]
        self.assertIn("background", names)
        self.assertIn("color-background", names)
        dark = text[text.index(".dark {"):]
        self.assertIn("--background: oklch(0.145 0 0);", dark)
        self.assertIn("--color-background: var(--background);", text)


class Specimen(TmpCase):
    def test_page_is_valid_and_self_contained(self):
        text, findings = ds.build_specimen(rich_doc())
        self.assertEqual(findings, [])
        errors, external = ds.check_html(text)
        self.assertEqual(errors, [])
        self.assertEqual(external, [])
        self.assertTrue(text.startswith("<!doctype html>"))
        self.assertNotIn("http://", text)
        self.assertNotIn("https://", text)
        self.assertNotIn("<script", text)

    def test_page_shows_every_theme_and_family(self):
        text, _ = ds.build_specimen(rich_doc())
        self.assertIn('<section class="theme" data-theme="light">', text)
        self.assertIn('<section class="theme" data-theme="dark">', text)
        self.assertIn("on bg 17.58:1 PASS", text)
        self.assertIn("on bg 15.99:1 PASS", text)
        for h in ("<h2>Color</h2>", "<h2>Type</h2>", "<h2>Spacing</h2>", "<h2>Radius</h2>",
                  "<h2>Shadow</h2>", "<h2>Motion</h2>"):
            self.assertIn(h, text)
        self.assertIn("box-shadow:var(--shadow-md)", text)
        self.assertIn("border-radius:var(--radius-full)", text)
        self.assertIn("width:var(--space-4)", text)
        self.assertIn("font-size:var(--type-display-size)", text)

    def test_page_uses_the_tokens_for_itself(self):
        text, _ = ds.build_specimen(base_doc())
        style = text.split("<style>")[1].split("</style>")[0]
        page = style.split("*{box-sizing:border-box}")[1]
        self.assertIn("body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-sans);", page)
        self.assertIn("padding:var(--space-4)", page)
        self.assertIn("border-radius:var(--radius-md)", page)
        # No raw color in the page's own rules: every color comes from a token.
        self.assertIsNone(ds._A_HEX.search(page))
        self.assertIsNone(ds._A_FUNC.search(page))

    def test_failing_pair_is_marked_in_words(self):
        doc = base_doc()
        doc["color"]["tokens"][4]["value"]["light"] = "#c0c4cc"
        text, _ = ds.build_specimen(doc)
        self.assertIn("FAIL (needs 4.5:1)", text)

    def test_google_fonts_link_is_optional(self):
        doc = base_doc()
        doc["type"]["families"]["sans"] = "\"Public Sans\", system-ui, sans-serif"
        text, _ = ds.build_specimen(doc)
        self.assertEqual(ds.check_html(text)[1], [])
        text, _ = ds.build_specimen(doc, google_fonts=True)
        self.assertEqual(ds.check_html(text)[1],
                         ["https://fonts.googleapis.com/css2?family=Public+Sans&display=swap"])

    def test_escaping(self):
        doc = base_doc()
        doc["name"] = "A <b> & \"C\""
        doc["color"]["tokens"][0]["usage"] = "<script>alert(1)</script>"
        text, _ = ds.build_specimen(doc)
        self.assertEqual(ds.check_html(text)[0], [])
        self.assertNotIn("<script>", text)

    def test_cli(self):
        src = self.write_doc(base_doc())
        out = self.path("specimen.html")
        code, data = run_json(["specimen", src, "-o", out, "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(data["externalRequests"], [])
        with open(out) as fh:
            self.assertEqual(ds.check_html(fh.read()), ([], []))

    def test_sparse_tokens_still_render(self):
        doc = {"name": "Tiny", "color": {"themes": [{"id": "only", "name": "Only"}], "tokens": [
            {"name": "paper", "value": "#fafafa", "usage": "Ground."},
            {"name": "ink", "value": "#111111", "usage": "Text on paper."}]}}
        text, findings = ds.build_specimen(doc)
        self.assertEqual(codes(findings, "error"), [])
        self.assertEqual(ds.check_html(text)[0], [])
        self.assertIn("background:var(--paper)", text)
        self.assertIn("color:var(--ink)", text)


class Audit(TmpCase):
    def setUp(self):
        TmpCase.setUp(self)
        self.write("app/a.css", """
:root{--brand:#0055ff}
/* #999999 in a comment is ignored */
#add .card { color: #FFF; background: #ffffff; padding: 12px 16px; margin: 0 auto;
  border-radius: 6px; font-size: 14px; font-family: Inter, sans-serif;
  transition: opacity 250ms ease; border: 1px solid rgba(0,0,0,.1) }
.b { color: var(--brand); background:#fefefe; gap: 0.75rem }
""")
        self.write("app/B.tsx", """
export const B = () => <div className="p-[13px] bg-[#1d55b0] text-[15px] rounded-[10px] duration-[150ms]"
  style={{ color: '#17191e', fontSize: 18, padding: '4px 8px', transition: 'all 0.3s' }}>
  <a href="#fab">x</a></div>
""")
        self.write("app/i.html", """<html><head><style>.x{color:#abc;margin:3px}</style></head>
<body><p style="color: #abc; font-size: 13px">a</p><svg><path fill="#123456"/></svg></body></html>""")
        self.write("app/node_modules/x/y.css", ".z{color:#010203}")
        self.write("app/notes.txt", "color: #050505")

    def test_inventory(self):
        res = ds.run_audit([self.path("app")])
        self.assertEqual(res["filesScanned"], 3)
        inv = res["inventory"]
        colors = {v["value"]: v["count"] for v in inv["colors"]["values"]}
        self.assertEqual(colors, {"#ffffff": 2, "#fefefe": 1, "rgba(0, 0, 0, 0.1)": 1, "#1d55b0": 1,
                                  "#17191e": 1, "#aabbcc": 2, "#123456": 1})
        self.assertEqual(inv["colors"]["unique"], 7)
        self.assertEqual(inv["colors"]["nearDuplicates"], [["#ffffff", "#fefefe"]])
        sizes = sorted(v["value"] for v in inv["fontSizes"]["values"])
        self.assertEqual(sizes, ["13px", "14px", "15px", "18px"])
        self.assertEqual([v["value"] for v in inv["fontFamilies"]["values"]], ["Inter, sans-serif"])
        spacing = sorted(v["value"] for v in inv["spacing"]["values"])
        self.assertEqual(spacing, ["0.75rem", "12px", "13px", "16px", "3px", "4px", "8px"])
        self.assertEqual(sorted(v["value"] for v in inv["radii"]["values"]), ["10px", "6px"])
        self.assertEqual(sorted(v["value"] for v in inv["durations"]["values"]), ["0.3s", "150ms", "250ms"])
        self.assertEqual(res["tokenDefinitions"], 1)
        self.assertEqual(res["tokenReferences"], 1)
        self.assertEqual(res["rawLiterals"], sum(inv[c]["occurrences"] for c in ds.Inventory.CATS))

    def test_token_match(self):
        res = ds.run_audit([self.path("app")], base_doc())
        colors = {v["value"]: v.get("token") for v in res["inventory"]["colors"]["values"]}
        self.assertEqual(colors["#ffffff"], "bg")
        self.assertEqual(colors["#1d55b0"], "accent")
        self.assertIsNone(colors["#123456"])
        spacing = {v["value"]: v.get("token") for v in res["inventory"]["spacing"]["values"]}
        self.assertEqual(spacing["16px"], "space-3")
        self.assertIsNone(spacing["12px"])  # 12px is a type size, not a spacing token
        self.assertEqual(res["literalsWithToken"] + res["literalsWithoutToken"], res["rawLiterals"])

    def test_cli_exit_codes(self):
        self.assertEqual(run(["audit", self.path("app")])[0], 1)
        code, data = run_json(["audit", self.path("app"), "--inventory", "--json"])
        self.assertEqual(code, 0)
        self.assertGreater(data["rawLiterals"], 0)
        clean = self.write("clean/c.css", ":root{--bg:#fff}.a{color:var(--bg);padding:var(--s)}")
        code, data = run_json(["audit", clean, "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(data["rawLiterals"], 0)
        self.assertEqual(data["tokenReferences"], 2)
        self.assertEqual(run(["audit", self.path("nope")])[0], 2)

    def test_font_face_descriptors_are_not_literals(self):
        # Regression: the specimen of a pack with font files declares @font-face.
        # Its font-family names the face; it cannot be a var() and is not a bypass.
        css = self.write("faces/f.css", """
@font-face { font-family: "Roboto Slab"; src: url("fonts/RobotoSlab.woff2"); font-weight: 100 900; }
@font-face{font-family:'Roboto';src:url(fonts/Roboto.woff2)}
:root { --font-serif: "Roboto Slab", Georgia, serif; }
.h { font-family: var(--font-serif); }
.raw { font-family: Arial, sans-serif; }
code { font-family: inherit; }
""")
        res = ds.run_audit([css])
        families = [v["value"] for v in res["inventory"]["fontFamilies"]["values"]]
        self.assertEqual(families, ["Arial, sans-serif"])
        self.assertEqual(res["rawLiterals"], 1)
        page = self.write("faces/p.html", "<style>@font-face{font-family:\"Lora\";src:url(l.woff2)}"
                                          ".a{font-family:var(--f)}</style><p>x</p>")
        self.assertEqual(ds.run_audit([page])["rawLiterals"], 0)

    def test_generated_specimen_without_mono_audits_clean(self):
        # Regression: the specimen sets code to font-family: inherit when no mono role exists.
        doc = base_doc()
        doc["type"]["families"].pop("mono")
        for group in doc["type"]["groups"]:
            if group.get("family") == "mono":
                group["family"] = "sans"
        out = self.path("spec2/specimen.html")
        self.assertEqual(run(["specimen", self.write("spec2/tokens.json", json.dumps(doc)), "-o", out])[0], 0)
        with open(out, encoding="utf-8") as handle:
            self.assertIn("font-family:inherit", handle.read())
        self.assertEqual(ds.run_audit([out], doc)["inventory"]["fontFamilies"]["values"], [])

    def test_generated_specimen_with_font_files_audits_clean(self):
        doc = rich_doc()
        if not doc["type"].get("fonts"):
            self.skipTest("rich_doc carries no font files")
        out = self.path("spec/specimen.html")
        self.assertEqual(run(["specimen", self.write("spec/tokens.json", json.dumps(doc)), "-o", out])[0], 0)
        res = ds.run_audit([out], doc)
        self.assertEqual(res["inventory"]["fontFamilies"]["values"], [])


class Init(TmpCase):
    def test_scaffold(self):
        target = self.path("brand")
        code, data = run_json(["init", target, "--name", "Acme", "--json"])
        self.assertEqual(code, 0)
        for rel in ("tokens.json", "README.md", "DESIGN.md", "tokens.css", "SOURCE.md",
                    "components/README.md", "assets/README.md"):
            self.assertTrue(os.path.isfile(os.path.join(target, rel)), rel)
        doc = ds.read_json(os.path.join(target, "tokens.json"))
        self.assertEqual(doc["name"], "Acme")
        self.assertEqual(ds.validate_doc(doc), [])
        self.assertTrue(6 <= len(doc["color"]["tokens"]) <= 10)
        self.assertEqual(ds.theme_ids(doc), ["light", "dark"])
        self.assertTrue(5 <= sum(len(g["styles"]) for g in doc["type"]["groups"]) <= 7)
        self.assertEqual(len(doc["spacing"]["tokens"]), 4)
        self.assertEqual(len(doc["radius"]["tokens"]), 3)
        self.assertTrue(doc["shadow"]["tokens"] and doc["motion"]["tokens"])
        self.assertEqual(run(["contrast", os.path.join(target, "tokens.json")])[0], 0)
        with open(os.path.join(target, "README.md")) as fh:
            readme = fh.read()
        for h in ("## Content fundamentals", "## Visual foundations", "## Iconography", "## Usage rules"):
            self.assertIn(h, readme)
        for name in ("`bg`", "`text-muted`", "`space-3`", "`radius-md`", "`duration-fast`"):
            self.assertIn(name, readme)

    def test_does_not_overwrite(self):
        target = self.path("brand")
        self.assertEqual(run(["init", target, "--name", "A"])[0], 0)
        self.assertEqual(run(["init", target, "--name", "B"])[0], 2)
        self.assertEqual(ds.read_json(os.path.join(target, "tokens.json"))["name"], "A")
        self.assertEqual(run(["init", target, "--name", "B", "--force"])[0], 0)
        self.assertEqual(ds.read_json(os.path.join(target, "tokens.json"))["name"], "B")

    def test_rules_in_readme_name_real_tokens(self):
        doc = ds.starter_tokens("X")
        names = set(t["name"] for t in ds.color_tokens(doc))
        for fam in ("spacing", "radius", "shadow", "motion"):
            names |= set(t["name"] for t in doc[fam]["tokens"])
        names |= set(s["name"] for _g, s in ds.type_styles(doc))
        import re
        quoted = set(re.findall(r"`([a-z0-9-]+)`", ds.starter_readme("X")))
        quoted -= {"tokens-json"}
        self.assertTrue(quoted)
        self.assertEqual(sorted(q for q in quoted if q not in names), [])


class Template(unittest.TestCase):
    """brands/_template is a checked-in pack. It must stay valid and fresh."""

    def read(self, name):
        with open(os.path.join(TEMPLATE, name), "r", encoding="utf-8") as fh:
            return fh.read()

    def test_files_exist(self):
        for name in ("README.md", "tokens.json", "DESIGN.md", "PACK.md", "tokens.css", "SOURCE.md"):
            self.assertTrue(os.path.isfile(os.path.join(TEMPLATE, name)), name)

    def test_tokens_are_valid_and_legible(self):
        doc = ds.read_json(os.path.join(TEMPLATE, "tokens.json"))
        self.assertEqual(ds.validate_doc(doc), [])
        results = ds.check_contrast(doc, ds.pairs_from_usage(doc))
        self.assertTrue(results)
        self.assertEqual([r for r in results if not r["pass"]], [])

    def test_generated_files_are_fresh(self):
        doc = ds.read_json(os.path.join(TEMPLATE, "tokens.json"))
        css, _ = ds.build_css(doc)
        self.assertEqual(self.read("tokens.css"), css)
        design, _ = ds.build_design_md(doc, self.read("README.md"))
        self.assertEqual(self.read("DESIGN.md"), design)


class ExamplePack(unittest.TestCase):
    """brands/example-harbor-lantern is the public example pack. It must stay valid, legible and fresh."""

    PACK = os.path.join(ROOT, "brands", "example-harbor-lantern")

    def read(self, name):
        with open(os.path.join(self.PACK, name), "r", encoding="utf-8") as fh:
            return fh.read()

    def test_tokens_are_valid_and_legible(self):
        doc = ds.read_json(os.path.join(self.PACK, "tokens.json"))
        self.assertEqual(ds.validate_doc(doc), [])
        results = ds.check_contrast(doc, ds.pairs_from_usage(doc))
        self.assertTrue(results)
        self.assertEqual([r for r in results if not r["pass"]], [])

    def test_generated_files_are_fresh(self):
        doc = ds.read_json(os.path.join(self.PACK, "tokens.json"))
        css, _ = ds.build_css(doc)
        self.assertEqual(self.read("tokens.css"), css)
        design, _ = ds.build_design_md(doc, self.read("README.md"))
        self.assertEqual(self.read("DESIGN.md"), design)

    def test_pack_holds_no_placeholder(self):
        for name in ("README.md", "SOURCE.md", "DESIGN.md"):
            self.assertNotIn("TODO", self.read(name), name)


class SkillFiles(unittest.TestCase):
    """House rules for the Markdown this skill ships."""

    SKILL = os.path.join(ROOT, "kit", "skills", "design-system")

    def md_files(self):
        out = []
        for base in (self.SKILL, TEMPLATE):
            for root, _dirs, names in os.walk(base):
                out += [os.path.join(root, n) for n in names if n.endswith(".md")]
        return out

    def test_markdown_house_rules(self):
        files = self.md_files()
        self.assertTrue(files)
        for path in files:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            rel = os.path.relpath(path, ROOT)
            self.assertNotIn("<!--", text, rel)
            try:
                text.encode("ascii")
            except UnicodeEncodeError as exc:
                self.fail("%s holds a non-ASCII character at %d" % (rel, exc.start))
            self.assertLessEqual(len(text.splitlines()), 400, rel)
            self.assertNotIn("claude.ai/artifact/", text, rel)

    def test_skill_router_budget_and_links(self):
        import re
        with open(os.path.join(self.SKILL, "SKILL.md"), "r", encoding="utf-8") as fh:
            text = fh.read()
        self.assertLessEqual(len(text.splitlines()), 150)
        self.assertLessEqual(len(text.split()), 1500)
        self.assertTrue(text.startswith("---\nname: design-system\n"))
        self.assertIn("disable-model-invocation: true", text)
        links = set(re.findall(r"\]\(([^)#]+)\)", text))
        for root, _dirs, names in os.walk(self.SKILL):
            for n in names:
                rel = os.path.relpath(os.path.join(root, n), self.SKILL).replace(os.sep, "/")
                # refinement-log.md is the change log of the skill; gdh.py check exempts it too.
                if rel in ("SKILL.md", "refinement-log.md") or "__pycache__" in rel:
                    continue
                self.assertIn(rel, links, "SKILL.md does not link %s" % rel)
        for link in links:
            if not link.startswith("http"):
                self.assertTrue(os.path.exists(os.path.join(self.SKILL, link)), link)
        headings = re.findall(r"(?m)^## (.+)$", text)
        self.assertEqual(headings, ["Before you start", "Procedure", "Tools", "Checks", "Output",
                                    "References", "Sources"])


if __name__ == "__main__":
    unittest.main()
