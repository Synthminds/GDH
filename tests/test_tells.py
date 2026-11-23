"""Tests for kit/skills/design-critique/scripts/tells.py.

Run: python3 -m unittest discover -s tests
"""

import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TELLS_PATH = os.path.join(ROOT, "kit", "skills", "design-critique", "scripts", "tells.py")

_spec = importlib.util.spec_from_file_location("gdh_tells", TELLS_PATH)
tells = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tells)

ROCKET = "\U0001F680"
BOLT = "\u26A1"

TOKENS = {
    "name": "Brand",
    "color": {
        "themes": [{"id": "light", "name": "Light"}],
        "tokens": [
            {"name": "violet", "value": "#8b5cf6", "usage": "Brand."},
            {"name": "blue", "value": {"light": "#3b82f6"}, "usage": "Brand."},
            {"name": "status-ok", "value": "#0a7d33", "usage": "Success text."},
        ],
    },
    "type": {
        "fonts": [],
        "families": {"sans": "Inter, system-ui, sans-serif"},
        "groups": [{"name": "Text", "family": "sans", "styles": [
            {"name": "eyebrow", "fontSize": "12px", "lineHeight": 1.2, "fontWeight": 600},
            {"name": "body", "fontSize": "16px", "lineHeight": 1.5, "fontWeight": 400},
        ]}],
    },
    "radius": {"tokens": [{"name": "radius", "value": "16px", "usage": "Every surface."}]},
    "shadow": {"tokens": [{"name": "glow-md", "value": "0 0 40px rgba(139, 92, 246, 0.5)", "usage": "Focus."}]},
}


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-tells-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def tokens(self, data=None):
        return self.write("tokens.json", json.dumps(TOKENS if data is None else data))

    def scan(self, name, text, **kwargs):
        path = self.write(name, text)
        return tells.run_scan([path], **kwargs)

    def codes(self, result):
        return [f["code"] for f in result["findings"]]

    def required(self, result):
        return [f["code"] for f in result["brandRequired"]]

    def cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = tells.main(argv)
        return code, out.getvalue(), err.getvalue()


class RuleTable(Case):
    def test_every_rule_has_severity_and_hint(self):
        self.assertGreaterEqual(len(tells.RULES), 15)
        for code, (severity, what, hint) in tells.RULES.items():
            self.assertTrue(code.startswith("TELL_"))
            self.assertIn(severity, tells.SEVERITIES)
            self.assertTrue(what.endswith("."))
            self.assertGreater(len(hint), 20)

    def test_list_flag_prints_each_code(self):
        code, out, _ = self.cli(["--list"])
        self.assertEqual(code, 0)
        for rule in tells.RULES:
            self.assertIn(rule, out)

    def test_list_json(self):
        code, out, _ = self.cli(["--list", "--json"])
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(data["listVersion"], tells.LIST_VERSION)
        self.assertEqual(len(data["rules"]), len(tells.RULES))

    def test_script_is_ascii_and_offline(self):
        with open(TELLS_PATH, "rb") as handle:
            raw = handle.read()
        raw.decode("ascii")
        text = raw.decode("ascii")
        for needle in ("urllib", "http.client", "import socket", "import requests", "subprocess"):
            self.assertNotIn(needle, text)


class Helpers(Case):
    def test_parse_color_forms(self):
        self.assertEqual(tells.to_hex(tells.parse_color("#abc")), "#aabbcc")
        self.assertEqual(tells.to_hex(tells.parse_color("#8B5CF6")), "#8b5cf6")
        self.assertEqual(tells.to_hex(tells.parse_color("rgb(139, 92, 246)")), "#8b5cf6")
        self.assertEqual(tells.to_hex(tells.parse_color("rgba(139 92 246 / 50%)")), "#8b5cf6")
        self.assertEqual(tells.to_hex(tells.parse_color("hsl(0, 100%, 50%)")), "#ff0000")
        self.assertEqual(tells.to_hex(tells.parse_color("purple")), "#800080")
        self.assertIsNone(tells.parse_color("var(--x)"))
        self.assertIsNone(tells.parse_color("inset"))

    def test_oklch_parses_to_a_purple(self):
        rgb = tells.parse_color("oklch(0.6 0.25 300)")
        hue = tells.hsl_of(rgb)[0]
        self.assertTrue(240 <= hue <= 300, hue)

    def test_parse_css_nested_comments_and_lines(self):
        css = "/* note { } */\n.a { color: red; }\n@media (min-width: 600px) {\n  .b {\n    border-radius: 8px\n  }\n}\n"
        rules = tells.parse_css(css)
        selectors = [r[0] for r in rules]
        self.assertIn(".a", selectors)
        self.assertTrue(any(s.endswith(".b") and s.startswith("@media") for s in selectors))
        nested = [r for r in rules if r[0].endswith(".b")][0]
        self.assertEqual(nested[1][0][0], "border-radius")
        self.assertEqual(nested[1][0][2], 5)

    def test_parse_css_keeps_semicolons_inside_urls(self):
        rules = tells.parse_css(".a { background: url(data:image/png;base64,AAAA); color: #111; }")
        props = [d[0] for d in rules[0][1]]
        self.assertEqual(props, ["background", "color"])

    def test_base_class_strips_variants(self):
        self.assertEqual(tells.base_class("md:hover:from-purple-600"), "from-purple-600")
        self.assertEqual(tells.base_class("bg-[url(https://x.test/a:b)]"), "bg-[url(https://x.test/a:b)]")
        self.assertEqual(tells.base_class("!rounded-xl"), "rounded-xl")


class PurpleGradient(Case):
    def test_css_purple_to_blue_is_found(self):
        result = self.scan("a.css", ".hero { background: linear-gradient(135deg, #6366f1, #a855f7, #3b82f6); }")
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))
        self.assertEqual(result["findings"][0]["severity"], "high")
        self.assertEqual(result["findings"][0]["line"], 1)

    def test_named_and_rgb_stops(self):
        result = self.scan("a.css", ".x { background-image: radial-gradient(circle, purple, rgb(59, 130, 246)); }")
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_blue_to_cyan_is_not_found(self):
        result = self.scan("a.css", ".x { background: linear-gradient(#2563eb, #06b6d4); }")
        self.assertNotIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_green_and_gray_gradients_are_not_found(self):
        result = self.scan("a.css", ".x { background: linear-gradient(#0b6e63, #b7e4c7); }\n"
                                     ".y { background: linear-gradient(#111, #333); }")
        self.assertEqual(self.codes(result), [])

    def test_pure_blue_is_not_indigo(self):
        result = self.scan("a.css", ".x { background: linear-gradient(blue, navy); }")
        self.assertEqual(self.codes(result), [])

    def test_purple_to_orange_is_not_the_default_look(self):
        result = self.scan("a.css", ".x { background: linear-gradient(#7c3aed, #f97316); }")
        self.assertNotIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_tailwind_gradient(self):
        result = self.scan("a.tsx", '<div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />')
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_tailwind_variant_prefix_and_v4_name(self):
        result = self.scan("a.html", '<div class="md:bg-linear-to-br md:from-purple-600 md:to-blue-600"></div>')
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_tailwind_other_hues_pass(self):
        result = self.scan("a.html", '<div class="bg-gradient-to-r from-emerald-400 to-cyan-500"></div>')
        self.assertEqual(self.codes(result), [])

    def test_tailwind_stops_without_gradient_class_pass(self):
        result = self.scan("a.html", '<div class="from-purple-600 to-blue-600"></div>')
        self.assertEqual(self.codes(result), [])

    def test_css_variable_stops_resolve_inside_the_scan(self):
        css = ":root { --a: #7c3aed; --b: #2563eb; }\n.x { background: linear-gradient(var(--a), var(--b)); }"
        result = self.scan("a.css", css)
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_unresolved_variables_are_not_guessed(self):
        result = self.scan("a.css", ".x { background: linear-gradient(var(--brand-1), var(--brand-2)); }")
        self.assertEqual(self.codes(result), [])

    def test_token_colors_alone_do_not_make_a_brand_gradient(self):
        # Review finding: stops that are token colors (or plain ramp steps) are not a brand gradient.
        result = self.scan("a.css", ".x { background: linear-gradient(90deg, #8b5cf6, #3b82f6); }",
                           tokens=self.tokens())
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_gradient_token_with_the_same_stops_is_brand_required(self):
        data = json.loads(json.dumps(TOKENS))
        data["gradient"] = [{"name": "brand", "value": "linear-gradient(90deg, {violet}, {blue})", "usage": "Hero."}]
        result = self.scan("a.css", ".x { background: linear-gradient(90deg, #8b5cf6, #3b82f6); }",
                           tokens=self.tokens(data))
        self.assertNotIn("TELL_PURPLE_GRADIENT", self.codes(result))
        self.assertIn("TELL_PURPLE_GRADIENT", self.required(result))
        self.assertIn("tokens.json", result["brandRequired"][0]["source"])
        self.assertNotIn("hint", result["brandRequired"][0])
        other = self.scan("b.css", ".x { background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); }",
                          tokens=self.tokens(data))
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(other))

    def test_off_token_stops_stay_a_finding(self):
        result = self.scan("a.css", ".x { background: linear-gradient(90deg, #6d28d9, #1d4ed8); }",
                           tokens=self.tokens())
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))

    def test_design_md_prescribes_a_gradient(self):
        design = self.write("DESIGN.md", "# Brand\n\n## Color\nHero grounds use the violet to blue gradient.\n")
        result = self.scan("a.tsx", '<div className="bg-gradient-to-r from-violet-500 to-blue-500" />', design=design)
        self.assertEqual(self.codes(result), [])
        self.assertIn("DESIGN.md line 4", result["brandRequired"][0]["source"])

    def test_design_md_ban_is_not_a_prescription(self):
        design = self.write("DESIGN.md", "# Brand\n\nNever use a gradient.\n")
        result = self.scan("a.tsx", '<div className="bg-gradient-to-r from-violet-500 to-blue-500" />', design=design)
        self.assertIn("TELL_PURPLE_GRADIENT", self.codes(result))


class GradientText(Case):
    def test_css_background_clip_text(self):
        css = "h1 { background: linear-gradient(#0b6e63, #f59e0b); -webkit-background-clip: text; color: transparent; }"
        result = self.scan("a.css", css)
        self.assertEqual(self.codes(result), ["TELL_GRADIENT_TEXT"])

    def test_tailwind_bg_clip_text(self):
        result = self.scan("a.jsx", '<h1 className="bg-clip-text text-transparent bg-gradient-to-r from-amber-400 '
                                    'to-red-500">Ship</h1>')
        self.assertIn("TELL_GRADIENT_TEXT", self.codes(result))

    def test_bg_clip_text_alone_passes(self):
        result = self.scan("a.jsx", '<h1 className="bg-clip-text">Ship</h1>')
        self.assertEqual(self.codes(result), [])

    def test_brand_required_by_design_md(self):
        design = self.write("DESIGN.md", "# Brand\n\n## Type\nHeadlines use the brand gradient.\n")
        result = self.scan("a.jsx", '<h1 className="bg-clip-text text-transparent">Ship</h1>', design=design)
        self.assertEqual(self.codes(result), [])
        self.assertEqual(self.required(result), ["TELL_GRADIENT_TEXT"])

    def test_do_not_section_keeps_the_finding(self):
        design = self.write("DESIGN.md", "# Brand\n\n## Do not\n- Gradient text on headings.\n\n## Type\nSerif.\n")
        result = self.scan("a.jsx", '<h1 className="bg-clip-text text-transparent">Ship</h1>', design=design)
        self.assertEqual(self.codes(result), ["TELL_GRADIENT_TEXT"])

    def test_prohibition_ends_at_the_next_heading(self):
        design = self.write("DESIGN.md", "# Brand\n\n## Avoid\n- Stock photos.\n\n## Type\nGradient headlines "
                                         "are the signature.\n")
        result = self.scan("a.jsx", '<h1 className="bg-clip-text text-transparent">Ship</h1>', design=design)
        self.assertEqual(self.codes(result), [])


class Glass(Case):
    def test_two_uses_pass(self):
        css = ".a { backdrop-filter: blur(8px); }\n.b { backdrop-filter: blur(8px); }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_three_uses_are_found(self):
        css = ".a { backdrop-filter: blur(8px); }\n.b { -webkit-backdrop-filter: blur(8px); backdrop-filter: " \
              "blur(8px); }\n.c { backdrop-filter: blur(4px) saturate(1.2); }"
        result = self.scan("a.css", css)
        self.assertEqual(self.codes(result), ["TELL_GLASS_EVERYWHERE"])
        self.assertIn("3 time(s) in the scan", result["findings"][0]["message"])

    def test_tailwind_backdrop_blur(self):
        html = '<nav class="backdrop-blur"></nav><div class="backdrop-blur-md"></div><aside class="lg:backdrop-blur-xl">' \
               '</aside><p class="backdrop-blur-none"></p>'
        result = self.scan("a.html", html)
        self.assertEqual(self.codes(result), ["TELL_GLASS_EVERYWHERE"])

    def test_counts_across_files(self):
        one = self.write("one.css", ".a { backdrop-filter: blur(8px); }\n.b { backdrop-filter: blur(8px); }")
        two = self.write("two.html", '<div class="backdrop-blur-sm"></div>')
        result = tells.run_scan([one, two])
        self.assertEqual(self.codes(result).count("TELL_GLASS_EVERYWHERE"), 2)

    def test_brand_required_by_design_md(self):
        design = self.write("DESIGN.md", "# Brand\n\nSurfaces are glass with a backdrop blur.\n")
        css = ".a{backdrop-filter:blur(8px)}.b{backdrop-filter:blur(8px)}.c{backdrop-filter:blur(8px)}"
        result = self.scan("a.css", css, design=design)
        self.assertEqual(self.codes(result), [])
        self.assertEqual(self.required(result), ["TELL_GLASS_EVERYWHERE"])

    def test_no_glass_sentence_is_a_ban(self):
        design = self.write("DESIGN.md", "# Brand\n\nNo glass. No blur.\n")
        css = ".a{backdrop-filter:blur(8px)}.b{backdrop-filter:blur(8px)}.c{backdrop-filter:blur(8px)}"
        self.assertEqual(self.codes(self.scan("a.css", css, design=design)), ["TELL_GLASS_EVERYWHERE"])


class Glow(Case):
    def test_colored_zero_offset_shadow(self):
        result = self.scan("a.css", ".card { box-shadow: 0 0 40px rgba(139, 92, 246, 0.5); }")
        self.assertEqual(self.codes(result), ["TELL_GLOW_SHADOW"])

    def test_second_layer_is_checked(self):
        result = self.scan("a.css", ".card { box-shadow: 0 1px 2px rgba(0,0,0,.1), 0 0 24px 4px #22d3ee; }")
        self.assertEqual(self.codes(result), ["TELL_GLOW_SHADOW"])

    def test_elevation_shadow_passes(self):
        result = self.scan("a.css", ".card { box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06); }")
        self.assertEqual(self.codes(result), [])

    def test_gray_halo_and_focus_ring_pass(self):
        css = ".a { box-shadow: 0 0 30px rgba(0,0,0,.2); }\n.b:focus { box-shadow: 0 0 0 3px #2563eb; }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_text_shadow_and_drop_shadow(self):
        css = "h1 { text-shadow: 0 0 20px #f0f; }\n.i { filter: drop-shadow(0 0 12px #a855f7); }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_GLOW_SHADOW", "TELL_GLOW_SHADOW"])

    def test_tailwind_colored_shadow(self):
        result = self.scan("a.html", '<button class="shadow-lg shadow-purple-500/50">Go</button>')
        self.assertEqual(self.codes(result), ["TELL_GLOW_SHADOW"])

    def test_tailwind_neutral_shadow_passes(self):
        result = self.scan("a.html", '<button class="shadow-md shadow-black/10">Go</button>')
        self.assertEqual(self.codes(result), [])

    def test_tailwind_arbitrary_shadow(self):
        result = self.scan("a.html", '<div class="shadow-[0_0_30px_rgba(168,85,247,0.6)]"></div>')
        self.assertEqual(self.codes(result), ["TELL_GLOW_SHADOW"])

    def test_jsx_style_object(self):
        result = self.scan("a.tsx", '<div style={{ boxShadow: "0 0 32px #7c3aed" }} />')
        self.assertEqual(self.codes(result), ["TELL_GLOW_SHADOW"])

    def test_glow_token_makes_it_brand_required(self):
        result = self.scan("a.css", ".card { box-shadow: 0 0 40px rgba(139, 92, 246, 0.5); }", tokens=self.tokens())
        self.assertEqual(self.codes(result), [])
        self.assertIn("glow-md", result["brandRequired"][0]["source"])


class EmojiIcon(Case):
    def test_emoji_alone_in_an_element(self):
        result = self.scan("a.html", "<div><span>%s</span><h3>Fast builds</h3></div>" % ROCKET)
        self.assertEqual(self.codes(result), ["TELL_EMOJI_ICON"])
        self.assertTrue(all(ord(ch) < 128 for ch in result["findings"][0]["evidence"]))

    def test_emoji_leading_a_label(self):
        result = self.scan("a.jsx", "const items = [{ icon: '%s', title: 'Fast builds' }]" % BOLT)
        self.assertEqual(self.codes(result), ["TELL_EMOJI_ICON"])

    def test_emoji_inside_a_sentence_passes(self):
        result = self.scan("a.html", "<p>We launched it %s last week and it held.</p>" % ROCKET)
        self.assertEqual(self.codes(result), [])

    def test_css_content(self):
        result = self.scan("a.css", ".li::before { content: \"%s\"; }" % BOLT)
        self.assertEqual(self.codes(result), ["TELL_EMOJI_ICON"])

    def test_design_md_can_require_emoji(self):
        design = self.write("DESIGN.md", "# Brand\n\nList markers are emoji from the approved set.\n")
        result = self.scan("a.html", "<li><span>%s</span> Fast</li>" % ROCKET, design=design)
        self.assertEqual(self.codes(result), [])
        self.assertEqual(self.required(result), ["TELL_EMOJI_ICON"])

    def test_emoji_policy_none_is_a_ban(self):
        design = self.write("DESIGN.md", "# Brand\n\nEmoji policy: none.\n")
        result = self.scan("a.html", "<li><span>%s</span> Fast</li>" % ROCKET, design=design)
        self.assertEqual(self.codes(result), ["TELL_EMOJI_ICON"])


class LeftBorder(Case):
    def test_css_rounded_box_with_side_bar(self):
        result = self.scan("a.css", ".note { border-left: 4px solid #2563eb; border-radius: 8px; padding: 16px; }")
        self.assertEqual(self.codes(result), ["TELL_LEFT_BORDER_CARD"])

    def test_card_selector_without_radius(self):
        result = self.scan("a.css", ".callout-card { border-left-width: 3px; border-left-color: #f59e0b; }")
        self.assertEqual(self.codes(result), ["TELL_LEFT_BORDER_CARD"])

    def test_logical_property(self):
        result = self.scan("a.css", ".tip { border-inline-start: 4px solid teal; border-radius: 12px; }")
        self.assertEqual(self.codes(result), ["TELL_LEFT_BORDER_CARD"])

    def test_blockquote_and_plain_rule_pass(self):
        css = "blockquote { border-left: 4px solid #999; border-radius: 4px; }\n.toc a { border-left: 2px solid #ccc; }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_full_border_passes(self):
        css = ".card { border: 4px solid #111; border-left: 4px solid #111; border-radius: 8px; }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_tailwind(self):
        result = self.scan("a.html", '<div class="border-l-4 border-blue-500 rounded-lg p-4">Note</div>')
        self.assertEqual(self.codes(result), ["TELL_LEFT_BORDER_CARD"])

    def test_tailwind_without_rounding_passes(self):
        result = self.scan("a.html", '<div class="border-l-4 border-blue-500 p-4">Note</div>')
        self.assertEqual(self.codes(result), [])

    def test_apply_directive(self):
        result = self.scan("a.css", ".alert { @apply rounded-xl border-l-4 p-4; }")
        self.assertEqual(self.codes(result), ["TELL_LEFT_BORDER_CARD"])

    def test_brand_required_by_design_md(self):
        design = self.write("DESIGN.md", "# Brand\n\nNotices carry a 4 px left border in the status color.\n")
        result = self.scan("a.html", '<div class="border-l-4 rounded-lg">Note</div>', design=design)
        self.assertEqual(self.required(result), ["TELL_LEFT_BORDER_CARD"])


HERO = """<main>
<section class="py-24 text-center">
  <h1 class="text-6xl font-bold">Ship the report</h1>
  <p>Weekly numbers, written for you.</p>
</section>
<section class="grid md:grid-cols-3 gap-8">
  <div class="rounded-md border p-6"><h3>Collect</h3></div>
  <div class="rounded-md border p-6"><h3>Check</h3></div>
  <div class="rounded-md border p-6"><h3>Send</h3></div>
</section>
</main>
"""


class HeroThreeCards(Case):
    def test_centered_hero_then_three_columns(self):
        result = self.scan("a.html", HERO)
        self.assertEqual(self.codes(result), ["TELL_HERO_THREE_CARDS"])
        self.assertIn("share one class string", result["findings"][0]["message"])
        self.assertEqual(result["findings"][0]["line"], 3)

    def test_left_aligned_hero_passes(self):
        self.assertEqual(self.codes(self.scan("a.html", HERO.replace(" text-center", ""))), [])

    def test_no_three_column_grid_passes(self):
        self.assertEqual(self.codes(self.scan("a.html", HERO.replace("md:grid-cols-3", "md:grid-cols-2"))), [])

    def test_css_driven_layout(self):
        html = """<html><head><style>
.hero { text-align: center }
.features { display: grid; grid-template-columns: repeat(3, 1fr) }
body { font-family: "Source Serif 4", serif }
</style></head><body>
<header class="hero"><h1>Ship the report</h1></header>
<div class="features"><article class="f">A</article><article class="f">B</article><article class="f">C</article></div>
</body></html>"""
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_HERO_THREE_CARDS"])

    def test_jsx_map(self):
        jsx = """export default function Page() {
  return (<>
    <section className="text-center"><h1 className="text-5xl">Ship the report</h1></section>
    <div className="grid grid-cols-3">{items.map((i) => (<Card key={i.id} {...i} />))}</div>
  </>);
}"""
        result = self.scan("a.tsx", jsx)
        self.assertEqual(self.codes(result), ["TELL_HERO_THREE_CARDS"])

    def test_brand_required_by_design_md(self):
        design = self.write("DESIGN.md", "# Brand\n\nThe home page opens with a centered title and a three-column "
                                         "service row.\n")
        result = self.scan("a.html", HERO, design=design)
        self.assertEqual(self.required(result), ["TELL_HERO_THREE_CARDS"])


class Eyebrow(Case):
    PAGE = """<section><p class="text-xs uppercase tracking-widest">Platform</p><h2>One inbox</h2></section>
<section><p class="text-xs uppercase tracking-widest">Pricing</p><h2>Two plans</h2></section>
<section><h2>Questions</h2></section>
"""

    def test_label_above_most_headings(self):
        result = self.scan("a.html", self.PAGE)
        self.assertEqual(self.codes(result), ["TELL_EYEBROW_EVERY_HEADING"])

    def test_one_label_among_many_headings_passes(self):
        page = '<p class="eyebrow">New</p><h2>A</h2><h2>B</h2><h2>C</h2><h2>D</h2>'
        self.assertEqual(self.codes(self.scan("a.html", page)), [])

    def test_class_name_and_css_rule(self):
        page = """<style>.tag-line { text-transform: uppercase; letter-spacing: .18em }
body { font-family: "Source Serif 4", serif }</style>
<span class="tag-line">Platform</span><h2>One inbox</h2>
<div class="kicker">Pricing</div>
<h2>Two plans</h2>"""
        self.assertEqual(self.codes(self.scan("a.html", page)), ["TELL_EYEBROW_EVERY_HEADING"])

    def test_plain_paragraph_before_heading_passes(self):
        page = "<p>Intro text.</p><h2>A</h2><p>More text.</p><h2>B</h2>"
        self.assertEqual(self.codes(self.scan("a.html", page)), [])

    def test_jsx_map_counts_as_repeated(self):
        jsx = """{sections.map((s) => (
  <section key={s.id}><p className="uppercase tracking-wider text-sm">{s.kicker}</p><h2>{s.title}</h2></section>
))}"""
        self.assertEqual(self.codes(self.scan("a.tsx", jsx)), ["TELL_EYEBROW_EVERY_HEADING"])

    def test_type_style_named_eyebrow_is_brand_required(self):
        result = self.scan("a.html", self.PAGE, tokens=self.tokens())
        self.assertEqual(self.codes(result), [])
        self.assertIn("eyebrow", result["brandRequired"][0]["source"])

    def test_design_md_overline(self):
        design = self.write("DESIGN.md", "# Brand\n\nSection titles carry an overline in tracked capitals.\n")
        result = self.scan("a.html", self.PAGE, design=design)
        self.assertEqual(self.required(result), ["TELL_EYEBROW_EVERY_HEADING"])


class UniformRadius(Case):
    CSS = "\n".join(".e%d { border-radius: 16px; }" % i for i in range(7))

    def test_one_large_radius_everywhere(self):
        result = self.scan("a.css", self.CSS)
        self.assertEqual(self.codes(result), ["TELL_UNIFORM_RADIUS"])
        self.assertEqual(result["findings"][0]["severity"], "low")

    def test_varied_radii_pass(self):
        css = ".a{border-radius:4px}.b{border-radius:4px}.c{border-radius:8px}.d{border-radius:8px}" \
              ".e{border-radius:16px}.f{border-radius:16px}.g{border-radius:2px}"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_small_uniform_radius_passes(self):
        self.assertEqual(self.codes(self.scan("a.css", self.CSS.replace("16px", "4px"))), [])

    def test_few_uses_pass(self):
        self.assertEqual(self.codes(self.scan("a.css", ".a{border-radius:24px}.b{border-radius:24px}")), [])

    def test_pills_and_variables_are_ignored(self):
        css = self.CSS + "\n.pill { border-radius: 9999px; }\n.av { border-radius: 50%; }\n.t { border-radius: " \
                         "var(--radius-lg); }"
        result = self.scan("a.css", css)
        self.assertIn("7 of 7", result["findings"][0]["message"])

    def test_tailwind_classes(self):
        html = "".join('<div class="rounded-2xl p-4"></div>' for _ in range(6)) + '<img class="rounded-full">'
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_UNIFORM_RADIUS"])

    def test_style_block_counts_matched_elements(self):
        cards = "".join('<div class="card">x</div>' for _ in range(3))
        html = ("<style>.card { border-radius: 28px; } button, input, .nav { border-radius: 28px; }</style>"
                '<nav class="nav">n</nav><button>b</button>' + cards)
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_UNIFORM_RADIUS"])
        one_card = html.replace(cards, '<div class="card">x</div>')
        self.assertEqual(self.codes(self.scan("a.html", one_card)), [])
        # A stylesheet has no markup, so each selector counts once.
        self.assertEqual(self.codes(self.scan("a.css", ".card { border-radius: 28px; } "
                                                       "button, input, .nav { border-radius: 28px; }")), [])

    def test_single_radius_token_is_brand_required(self):
        result = self.scan("a.css", self.CSS, tokens=self.tokens())
        self.assertEqual(self.codes(result), [])
        self.assertEqual(self.required(result), ["TELL_UNIFORM_RADIUS"])

    def test_two_radius_tokens_keep_the_finding(self):
        data = json.loads(json.dumps(TOKENS))
        data["radius"]["tokens"].append({"name": "radius-sm", "value": "4px", "usage": "Controls."})
        result = self.scan("a.css", self.CSS, tokens=self.tokens(data))
        self.assertEqual(self.codes(result), ["TELL_UNIFORM_RADIUS"])


class DefaultFont(Case):
    def test_inter_only(self):
        result = self.scan("a.css", "body { font-family: Inter, system-ui, sans-serif; }")
        self.assertEqual(self.codes(result), ["TELL_DEFAULT_FONT_ONLY"])

    def test_system_stack_only(self):
        css = "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_DEFAULT_FONT_ONLY"])

    def test_a_chosen_face_passes(self):
        css = "body { font-family: Inter, sans-serif; }\nh1 { font-family: 'Source Serif 4', serif; }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_code_font_is_not_a_choice(self):
        css = "body { font-family: Arial, sans-serif; }\ncode, pre { font-family: 'JetBrains Mono', monospace; }\n" \
              ".num { font-family: ui-monospace, Menlo, monospace; }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_DEFAULT_FONT_ONLY"])

    def test_font_shorthand(self):
        self.assertEqual(self.codes(self.scan("a.css", "body { font: 16px/1.5 Helvetica, Arial, sans-serif; }")),
                         ["TELL_DEFAULT_FONT_ONLY"])

    def test_google_fonts_link_and_next_font(self):
        html = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">'
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_DEFAULT_FONT_ONLY"])
        tsx = 'import { Inter } from "next/font/google";\nconst inter = Inter({ subsets: ["latin"] });'
        self.assertEqual(self.codes(self.scan("b.tsx", tsx)), ["TELL_DEFAULT_FONT_ONLY"])
        tsx = 'import { Inter, Bricolage_Grotesque } from "next/font/google";'
        self.assertEqual(self.codes(self.scan("c.tsx", tsx)), [])

    def test_unresolved_variable_is_not_guessed(self):
        self.assertEqual(self.codes(self.scan("a.css", "body { font-family: var(--font-body); }")), [])

    def test_variable_resolves_inside_the_scan(self):
        css = ":root { --font-body: Inter, sans-serif; }\nbody { font-family: var(--font-body); }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_DEFAULT_FONT_ONLY"])

    def test_styled_document_with_no_family(self):
        html = '<html><body class="p-8"><h1 class="text-4xl">Hello</h1></body></html>'
        result = self.scan("a.html", html)
        self.assertEqual(self.codes(result), ["TELL_DEFAULT_FONT_ONLY"])
        self.assertIn("No font family is declared", result["findings"][0]["message"])

    def test_fragment_with_no_family_passes(self):
        self.assertEqual(self.codes(self.scan("a.html", '<div class="p-8">Hello</div>')), [])

    def test_tokens_family_is_brand_required(self):
        result = self.scan("a.css", "body { font-family: Inter, system-ui, sans-serif; }", tokens=self.tokens())
        self.assertEqual(self.codes(result), [])
        self.assertIn("type.families.sans", result["brandRequired"][0]["source"])

    def test_design_md_names_the_font(self):
        design = self.write("DESIGN.md", "# Brand\n\n## Type\nInter carries all text. It is the product voice.\n")
        result = self.scan("a.css", "body { font-family: Inter, sans-serif; }", design=design)
        self.assertEqual(self.required(result), ["TELL_DEFAULT_FONT_ONLY"])

    def test_design_md_that_replaces_the_font_keeps_the_finding(self):
        design = self.write("DESIGN.md", "# Brand\n\n## Type\nUse Fraunces instead of Inter.\n")
        result = self.scan("a.css", "body { font-family: Inter, sans-serif; }", design=design)
        self.assertEqual(self.codes(result), ["TELL_DEFAULT_FONT_ONLY"])


class StatRow(Case):
    def test_gradient_stat_row(self):
        html = "".join('<div><div class="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r '
                       'from-amber-400 to-red-500">%s</div><p>label</p></div>' % n for n in ("99.9%", "10k+", "24/7"))
        result = self.scan("a.html", html)
        self.assertIn("TELL_GRADIENT_STAT_ROW", self.codes(result))
        self.assertNotIn("TELL_STAT_ROW", self.codes(result))

    def test_plain_stat_row_is_low(self):
        html = '<div class="stat">42</div><div class="stat">3x</div><div class="stat">$2M</div>'
        result = self.scan("a.html", html)
        # A stat row with no source in view is also a set of invented figures.
        self.assertEqual(sorted(self.codes(result)), ["TELL_INVENTED_STAT", "TELL_STAT_ROW"])
        row = [f for f in result["findings"] if f["code"] == "TELL_STAT_ROW"][0]
        self.assertEqual(row["severity"], "low")

    def test_two_numbers_pass(self):
        html = '<div class="text-6xl">42</div><div class="text-6xl">7</div>'
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_small_numbers_in_a_table_pass(self):
        html = "<td>42</td><td>17</td><td>9</td><td>3</td>"
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_css_class_marks_big_and_gradient(self):
        html = """<style>.n { font-size: 3rem; background: linear-gradient(#f59e0b, #dc2626); background-clip: text;
color: transparent } body { font-family: "Fraunces", serif }</style>
<b class="n">120</b><b class="n">48</b><b class="n">7</b>"""
        result = self.scan("a.html", html)
        self.assertIn("TELL_GRADIENT_STAT_ROW", self.codes(result))

    def test_brand_required_by_design_md(self):
        design = self.write("DESIGN.md", "# Brand\n\nThe report page opens with a stat band of three sourced "
                                         "figures.\n")
        html = '<div class="stat">42</div><div class="stat">3x</div><div class="stat">$2M</div>'
        result = self.scan("a.html", html, design=design)
        self.assertEqual(self.required(result), ["TELL_STAT_ROW"])

    def test_status_token_does_not_count_as_a_stat_token(self):
        html = '<div class="stat">42</div><div class="stat">3x</div><div class="stat">$2M</div>'
        result = self.scan("a.html", html, tokens=self.tokens())
        self.assertEqual(sorted(self.codes(result)), ["TELL_INVENTED_STAT", "TELL_STAT_ROW"])


class Sprawl(Case):
    def test_font_size_sprawl(self):
        css = "\n".join(".s%d { font-size: %dpx; }" % (i, 11 + i) for i in range(9))
        result = self.scan("a.css", css)
        self.assertEqual(self.codes(result), ["TELL_FONT_SIZE_SPRAWL"])
        self.assertIn("9 distinct", result["findings"][0]["message"])

    def test_font_size_limit_flag(self):
        css = "\n".join(".s%d { font-size: %dpx; }" % (i, 11 + i) for i in range(9))
        path = self.write("a.css", css)
        self.assertEqual(self.codes(tells.run_scan([path], max_font_sizes=9)), [])

    def test_eight_sizes_pass_and_units_merge(self):
        css = ".a{font-size:16px}.b{font-size:1rem}.c{font-size:12pt}.d{font-size:1.25rem}.e{font-size:20px}" \
              ".f{font-size:var(--step-2)}.g{font-size:1em}.h{font-size:inherit}"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_token_sizes_do_not_count(self):
        css = "\n".join(".s%d { font-size: %dpx; }" % (i, 11 + i) for i in range(9))
        result = self.scan("a.css", css, tokens=self.tokens())
        self.assertEqual(self.codes(result), [])

    def test_tailwind_arbitrary_sizes_count(self):
        html = "".join('<p class="text-[%dpx]">x</p>' % (11 + i) for i in range(9))
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_FONT_SIZE_SPRAWL"])

    def test_color_sprawl(self):
        css = "\n".join(".c%d { color: #%02x3040; }" % (i, 16 * i) for i in range(13))
        result = self.scan("a.css", css)
        self.assertEqual(self.codes(result), ["TELL_COLOR_SPRAWL"])

    def test_custom_property_definitions_are_tokens(self):
        css = ":root {\n" + "\n".join("  --c%d: #%02x3040;" % (i, 16 * i) for i in range(13)) + "\n}\n" \
              ".a { color: var(--c1); }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_token_colors_do_not_count(self):
        css = "\n".join(".c%d { color: #%02x3040; }" % (i, 16 * i) for i in range(12)) + \
              "\n.t1{color:#8b5cf6}.t2{color:#3b82f6}.t3{color:rgb(10,125,51)}"
        path = self.write("a.css", css)
        self.assertEqual(self.codes(tells.run_scan([path])), ["TELL_COLOR_SPRAWL"])
        self.assertEqual(self.codes(tells.run_scan([path], tokens=self.tokens())), [])

    def test_sprawl_is_never_brand_required(self):
        design = self.write("DESIGN.md", "# Brand\n\nUse many colors and many font sizes.\n")
        css = "\n".join(".c%d { color: #%02x3040; }" % (i, 16 * i) for i in range(13))
        self.assertEqual(self.codes(self.scan("a.css", css, design=design)), ["TELL_COLOR_SPRAWL"])


class Content(Case):
    def test_lorem(self):
        result = self.scan("a.html", "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>")
        self.assertEqual(self.codes(result), ["TELL_LOREM"])
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_placeholder_copy(self):
        html = "<h3>Feature One</h3>\n<h2>Your headline here</h2>\n<p>John Doe, Acme Inc.</p>"
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_PLACEHOLDER_COPY"] * 3)

    def test_real_copy_passes(self):
        html = "<h3>Feature flags for one tenant</h3><p>Step by step, the tide table fills in.</p><b>Step 2</b>"
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_invented_statistics(self):
        samples = [
            "<p>Trusted by 10,000+ companies worldwide</p>",
            "<p>Join 50k+ happy developers</p>",
            "<p>99.9% uptime, always</p>",
            "<p>Teams ship 10x faster</p>",
            "<p>Rated 4.9/5 by our users</p>",
            "<p>$2M saved in the first year</p>",
            "<p>Loved by over 500 teams</p>",
        ]
        for index, sample in enumerate(samples):
            result = self.scan("s%d.html" % index, sample)
            self.assertEqual(self.codes(result), ["TELL_INVENTED_STAT"], sample)

    def test_sourced_figure_and_placeholder_pass(self):
        html = '<p data-source="orders-2026">Trusted by 10,000+ companies</p>\n' \
               "<p>Trusted by [CUSTOMER COUNT] companies</p>\n" \
               "<p>99.9% uptime <cite>status page, 2026</cite></p>"
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_plain_numbers_pass(self):
        html = "<p>The 8:10 sailing leaves from Pier 2. Version 4.2 adds 3 routes.</p>"
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_content_tells_are_never_brand_required(self):
        design = self.write("DESIGN.md", "# Brand\n\nLorem ipsum is fine. Stat rows show 10,000+ users.\n")
        html = "<p>Lorem ipsum dolor sit amet</p>\n<p>Trusted by 10,000+ companies</p>\n<h3>Feature One</h3>"
        result = self.scan("a.html", html, design=design, tokens=self.tokens())
        self.assertEqual(sorted(self.codes(result)), ["TELL_INVENTED_STAT", "TELL_LOREM", "TELL_PLACEHOLDER_COPY"])


CLEAN = """<!doctype html>
<html lang="en">
<head>
<style>
:root { --ink: #14212b; --chalk: #f7f5ef; --amber: #ffb000; --radius-control: 2px; --radius-sheet: 10px; }
body { font-family: "Overpass", "Helvetica Neue", Arial, sans-serif; color: var(--ink); background: var(--chalk); }
.board { display: grid; grid-template-columns: 7ch 1fr auto; row-gap: 12px; }
.next { font-size: 3rem; font-variant-numeric: tabular-nums; }
.status { border: 1px solid var(--ink); border-radius: var(--radius-control); }
.sheet { border-radius: var(--radius-sheet); box-shadow: 0 2px 12px rgba(20, 33, 43, 0.12); }
</style>
</head>
<body>
<main>
  <h1 class="next">Next boat 7:40</h1>
  <p>On time from Pier 2. The 8:10 is cancelled for wind.</p>
  <table class="board"><tr><td>7:40</td><td>Pier 2</td><td class="status">On time</td></tr></table>
  <a href="/ticket">Show my ticket</a>
</main>
</body>
</html>
"""


class Cli(Case):
    def test_clean_page_exits_zero(self):
        path = self.write("clean.html", CLEAN)
        code, out, _ = self.cli([path])
        self.assertEqual(code, 0, out)
        self.assertIn("0 high, 0 medium, 0 low", out)
        self.assertIn("does not prove distinctive work", out)

    def test_findings_exit_one(self):
        path = self.write("a.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        code, out, _ = self.cli([path])
        self.assertEqual(code, 1)
        self.assertIn("HIGH   TELL_PURPLE_GRADIENT", out)
        self.assertIn("fix:", out)

    def test_fail_on_threshold(self):
        path = self.write("a.css", ".note { border-left: 4px solid #2563eb; border-radius: 8px; }")
        self.assertEqual(self.cli([path])[0], 1)
        self.assertEqual(self.cli([path, "--fail-on", "high"])[0], 0)
        self.assertEqual(self.cli([path, "--fail-on", "medium"])[0], 1)

    def test_brand_required_does_not_fail(self):
        path = self.write("a.css", ".card { box-shadow: 0 0 40px rgba(139, 92, 246, 0.5); }")
        code, out, _ = self.cli([path, "--tokens", self.tokens()])
        self.assertEqual(code, 0)
        self.assertIn("brand-required (not findings):", out)
        self.assertIn("1 brand-required", out)

    def test_json_shape(self):
        path = self.write("a.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        code, out, _ = self.cli([path, "--json"])
        data = json.loads(out)
        self.assertEqual(code, 1)
        self.assertEqual(data["tool"], "tells.py")
        self.assertEqual(data["listVersion"], tells.LIST_VERSION)
        self.assertEqual(data["scanned"], 1)
        self.assertEqual(data["summary"], {"high": 1, "medium": 0, "low": 0, "brandRequired": 0})
        self.assertIn("heuristic", data["note"])
        finding = data["findings"][0]
        for key in ("code", "severity", "path", "line", "message", "evidence", "hint"):
            self.assertIn(key, finding)

    def test_allow_moves_a_finding_to_required(self):
        path = self.write("a.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        code, out, _ = self.cli([path, "--allow", "TELL_PURPLE_GRADIENT", "--json"])
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(data["findings"], [])
        self.assertIn("user", data["brandRequired"][0]["source"])

    def test_allow_refuses_content_gates_and_unknown_codes(self):
        path = self.write("a.html", "<p>Lorem ipsum dolor sit amet</p>")
        code, _, err = self.cli([path, "--allow", "TELL_LOREM"])
        self.assertEqual(code, 2)
        self.assertIn("content gate", err)
        self.assertEqual(self.cli([path, "--allow", "TELL_NOPE"])[0], 2)

    def test_usage_errors(self):
        self.assertEqual(self.cli([])[0], 2)
        self.assertEqual(self.cli([os.path.join(self.tmp, "absent.css")])[0], 2)
        path = self.write("a.css", ".a{}")
        self.assertEqual(self.cli([path, "--tokens", os.path.join(self.tmp, "absent.json")])[0], 2)
        bad = self.write("bad.json", "{not json")
        self.assertEqual(self.cli([path, "--tokens", bad])[0], 2)

    def test_scan_that_reads_no_file_does_not_pass(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        code, _, err = self.cli([empty])
        self.assertEqual(code, 2)
        self.assertIn("no file was scanned", err)
        # Markup only inside a dot folder or a vendor folder is skipped, so nothing is read.
        hidden = os.path.join(self.tmp, "hidden")
        self.write("hidden/.storybook/a.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        self.write("hidden/node_modules/pkg/b.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        self.assertEqual(self.cli([hidden])[0], 2)
        self.assertEqual(self.cli([hidden, "--json"])[0], 2)

    def test_oversize_file_alone_does_not_pass(self):
        big = self.write("big.css", "/* pad */\n" * (tells.MAX_BYTES // 10 + 10))
        code, out, err = self.cli([big])
        self.assertEqual(code, 2)
        self.assertIn("Skipped: %s" % big, out)
        self.assertIn("skipped: %s" % big, err)
        small = self.write("small.css", ".a { color: var(--text); }")
        # Decision: a partial scan is incomplete, so it exits 2 and names the skipped file.
        code, out, err = self.cli([big, small])
        self.assertEqual(code, 2)
        self.assertIn("incomplete scan", err)
        self.assertIn(big, err)
        data = json.loads(self.cli([big, small, "--json"])[1])
        self.assertFalse(data["complete"])
        self.assertEqual(data["scanned"], 1)

    def test_folder_scan_skips_vendor_folders(self):
        self.write("src/a.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        self.write("src/b.tsx", '<div className="p-4" />')
        self.write("src/readme.md", "linear-gradient(#7c3aed, #2563eb)")
        self.write("node_modules/pkg/c.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        self.write("dist/d.css", ".x { background: linear-gradient(#7c3aed, #2563eb); }")
        result = tells.run_scan([self.tmp])
        self.assertEqual(result["scanned"], 2)
        self.assertEqual(self.codes(result), ["TELL_PURPLE_GRADIENT"])

    def test_generic_page_trips_many_rules(self):
        html = """<html><head><style>
body { font-family: Inter, sans-serif }
.hero { text-align: center; background: linear-gradient(135deg, #6366f1, #a855f7, #3b82f6) }
.card { border-radius: 16px; backdrop-filter: blur(12px); box-shadow: 0 0 40px rgba(139,92,246,.5);
  border-left: 4px solid #8b5cf6 }
.nav { border-radius: 16px; backdrop-filter: blur(8px) } .modal { border-radius: 16px; backdrop-filter: blur(20px) }
.btn { border-radius: 16px } .input { border-radius: 16px } .badge { border-radius: 16px }
.grid { display: grid; grid-template-columns: repeat(3, 1fr) }
.eyebrow { text-transform: uppercase; letter-spacing: .2em }
</style></head><body>
<section class="hero"><p class="eyebrow">Introducing</p><h1>Build faster</h1><p>Lorem ipsum dolor sit amet.</p>
<p>Trusted by 10,000+ companies worldwide</p></section>
<p class="eyebrow">Features</p><h2>Everything you need</h2>
<div class="grid"><div class="card"><span>%s</span><h3>Feature One</h3></div>
<div class="card"><span>%s</span><h3>Feature Two</h3></div><div class="card"><h3>Feature Three</h3></div></div>
</body></html>""" % (ROCKET, BOLT)
        result = self.scan("slop.html", html)
        found = set(self.codes(result))
        expected = {"TELL_PURPLE_GRADIENT", "TELL_GLASS_EVERYWHERE", "TELL_GLOW_SHADOW", "TELL_EMOJI_ICON",
                    "TELL_LEFT_BORDER_CARD", "TELL_HERO_THREE_CARDS", "TELL_EYEBROW_EVERY_HEADING",
                    "TELL_UNIFORM_RADIUS", "TELL_DEFAULT_FONT_ONLY", "TELL_LOREM", "TELL_PLACEHOLDER_COPY",
                    "TELL_INVENTED_STAT"}
        self.assertEqual(expected - found, set())
        severities = [f["severity"] for f in result["findings"]]
        self.assertEqual(severities, sorted(severities, key=lambda s: -tells.RANK[s]))


class InventedStatLayouts(Case):
    """Review finding: figures split from their label by tags, or held in a JS data array, were missed."""

    def test_sibling_elements(self):
        html = "<div><span>10,000+</span><p>customers</p></div>\n<div><b>99.9%</b>\n<i>uptime</i></div>\n" \
               "<div><strong>10x</strong> <em>faster</em></div>"
        result = self.scan("a.html", html)
        self.assertEqual(self.codes(result), ["TELL_INVENTED_STAT"] * 3)
        self.assertEqual(sorted(f["line"] for f in result["findings"]), [1, 2, 4])

    def test_jsx_data_array(self):
        tsx = 'const stats = [\n  {value: "10,000+", label: "customers"},\n  {value: "99.9%", label: "uptime"},\n' \
              '  {value: "4.9/5", label: "rating"},\n];\nexport const Row = () => stats.map(s => <Stat {...s} />);\n'
        result = self.scan("stats.tsx", tsx)
        self.assertEqual(self.codes(result), ["TELL_INVENTED_STAT"] * 3)

    def test_sourced_data_object_and_sibling_source_pass(self):
        tsx = '[{value: "99.9%", label: "uptime", source: "status page, 2026"}]'
        self.assertEqual(self.codes(self.scan("a.tsx", tsx)), [])
        html = "<div><span>99.9%</span><p>uptime</p><cite>Status page, 2026</cite></div>"
        self.assertEqual(self.codes(self.scan("b.html", html)), [])

    def test_prose_attribution_is_a_source(self):
        html = "<p>98% client retention, according to the 2025 member survey.</p>\n" \
               "<p>Members rated it 4.8/5 in the 2025 member survey.</p>"
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_stat_row_styled_through_a_descendant_selector(self):
        html = """<style>.metric strong { font-size: 56px }</style>
<div class="metric"><strong>120</strong><span>brands launched</span></div>
<div class="metric"><strong>14</strong><span>years of practice</span></div>
<div class="metric"><strong>98%</strong><span>client retention</span></div>"""
        codes = self.codes(self.scan("a.html", html))
        self.assertIn("TELL_STAT_ROW", codes)
        self.assertIn("TELL_INVENTED_STAT", codes)

    def test_stat_row_with_a_source_is_not_invented(self):
        html = '<div class="stat">42</div><div class="stat">3x</div><div class="stat">$2M</div>' \
               '<p>Source: 2026 annual report.</p>'
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_STAT_ROW"])


class SecondWave(Case):
    """Review finding: the scan was blind to the second-wave defaults the tell list names."""

    def test_second_wave_face_alone(self):
        for face in sorted(tells.SECOND_WAVE_FAMILIES):
            result = self.scan("a.css", "body { font-family: '%s', sans-serif; }" % face)
            self.assertEqual(self.codes(result), ["TELL_SECOND_WAVE_FONT"], face)
            self.assertEqual(result["findings"][0]["severity"], "low")

    def test_second_wave_face_with_a_default_body(self):
        css = "body { font-family: Inter, sans-serif } h1 { font-family: 'Instrument Serif', serif }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_SECOND_WAVE_FONT"])

    def test_second_wave_face_beside_a_chosen_face_passes(self):
        css = "body { font-family: 'Source Serif 4', serif } h1 { font-family: 'Space Grotesk', sans-serif }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_second_wave_face_from_the_tokens_is_brand_required(self):
        data = json.loads(json.dumps(TOKENS))
        data["type"]["families"] = {"sans": "Geist, sans-serif"}
        result = self.scan("a.css", "body { font-family: Geist, sans-serif }", tokens=self.tokens(data))
        self.assertEqual(self.required(result), ["TELL_SECOND_WAVE_FONT"])

    def test_cream_and_terracotta_with_stock_type(self):
        css = "body { background: #f4efe6; color: #1f1b16; font-family: 'Fraunces', serif }\n" \
              ".btn { background: #c2410c; color: #fff }"
        result = self.scan("a.css", css)
        self.assertIn("TELL_SECOND_WAVE_PALETTE", self.codes(result))
        self.assertIn("warm-editorial", [f["message"] for f in result["findings"]
                                         if f["code"] == "TELL_SECOND_WAVE_PALETTE"][0])

    def test_near_black_with_one_orange_accent(self):
        css = ":root { --bg: #0e0f11; --accent: #ff6a1a }\nbody { background: var(--bg); font-family: Inter }\n" \
              ".cta { background: var(--accent) }"
        self.assertIn("TELL_SECOND_WAVE_PALETTE", self.codes(self.scan("a.css", css)))

    def test_near_black_with_acid_green(self):
        css = "body { background: #0b0b0c; font-family: Geist } .tag { color: #a3e635 }"
        self.assertIn("TELL_SECOND_WAVE_PALETTE", self.codes(self.scan("a.css", css)))

    def test_cream_with_a_chosen_face_passes(self):
        # The tide-card case: a paper ground and a buoy red traced to the subject, with a chosen face.
        css = "body { background: #eeeae0; font-family: 'Source Serif 4', serif } .w { color: #b43a1e }"
        self.assertNotIn("TELL_SECOND_WAVE_PALETTE", self.codes(self.scan("a.css", css)))

    def test_near_black_with_two_accent_families_passes(self):
        css = "body { background: #0e0f11; font-family: Inter } .a { color: #ff6a1a } .b { color: #2f6bff }"
        self.assertNotIn("TELL_SECOND_WAVE_PALETTE", self.codes(self.scan("a.css", css)))

    def test_palette_from_tokens_is_brand_required(self):
        data = json.loads(json.dumps(TOKENS))
        data["color"]["tokens"] += [{"name": "ground", "value": "#f4efe6", "usage": "Page."},
                                    {"name": "clay", "value": "#c2410c", "usage": "Accent."}]
        css = "body { background: #f4efe6; font-family: Inter } .btn { background: #c2410c }"
        result = self.scan("a.css", css, tokens=self.tokens(data))
        self.assertIn("TELL_SECOND_WAVE_PALETTE", self.required(result))

    def test_accent_word_in_a_headline(self):
        self.assertIn("TELL_ACCENT_WORD", self.codes(self.scan("a.html", "<h1>Slow design, <em>quietly</em> done</h1>")))
        html = '<h2>Built for <span class="italic text-orange-600">teams</span> that care</h2>'
        self.assertIn("TELL_ACCENT_WORD", self.codes(self.scan("b.html", html)))
        css = "<style>.hl { color: #c2410c }</style><h1>Make <span class=\"hl\">every</span> run count</h1>"
        self.assertIn("TELL_ACCENT_WORD", self.codes(self.scan("c.html", css)))

    def test_accent_word_passes_when_plain(self):
        html = "<h1>Next boat <span>7:40</span></h1><h2><em>Whole headline</em></h2><p>An <em>emphasised</em> word.</p>"
        self.assertNotIn("TELL_ACCENT_WORD", self.codes(self.scan("a.html", html)))

    def test_fake_sequence_outside_an_ordered_list(self):
        html = "<div><span>01</span><h3>Observe</h3></div><div><span>02</span><h3>Evaluate</h3></div>" \
               "<div><span>03</span><h3>Deploy</h3></div>"
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_FAKE_SEQUENCE"])
        tsx = 'const items = [{n: "01", t: "Plan"}, {n: "02", t: "Build"}, {n: "03", t: "Ship"}];'
        self.assertEqual(self.codes(self.scan("b.tsx", tsx)), ["TELL_FAKE_SEQUENCE"])

    def test_sequence_inside_an_ordered_list_and_times_pass(self):
        html = "<ol><li><span>01</span> Plan</li><li><span>02</span> Build</li><li><span>03</span> Ship</li></ol>" \
               "<td>08:12</td><td>01:30</td><p>Version 02</p>"
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_arrow_on_every_link(self):
        html = "<a href=a>Read more \u2192</a><a href=b>See pricing \u2192</a><button>Start \u2192</button>"
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_ARROW_EVERY_LINK"])
        css = 'a::after { content: "\\2192"; margin-left: .25em }'
        self.assertEqual(self.codes(self.scan("b.css", css)), ["TELL_ARROW_EVERY_LINK"])

    def test_one_arrow_passes(self):
        html = "<a href=a>Next page \u2192</a><a href=b>Pricing</a><a href=c>Docs</a>"
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_reveal_on_every_section(self):
        css = "section { opacity: 0; transform: translateY(24px); transition: all .6s }\n" \
              "section.in-view { opacity: 1; transform: none }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_REVEAL_EVERY_SECTION"])
        tsx = "".join('<motion.section initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} />\n'
                      for _ in range(3))
        self.assertEqual(self.codes(self.scan("b.tsx", tsx)), ["TELL_REVEAL_EVERY_SECTION"])

    def test_one_modal_fade_passes(self):
        css = ".modal { opacity: 0; transform: translateY(8px) } .modal.open { opacity: 1; transform: none }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_mono_labels(self):
        css = ".label { font-family: 'JetBrains Mono', monospace; font-size: 12px; text-transform: uppercase;" \
              " letter-spacing: .12em }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_MONO_LABELS"])
        html = '<p class="font-mono text-xs uppercase">Evals</p><p class="font-mono text-xs uppercase">Deploy</p>'
        self.assertEqual(self.codes(self.scan("b.html", html)), ["TELL_MONO_LABELS"])

    def test_mono_for_code_and_data_passes(self):
        css = "code, pre { font-family: monospace; font-size: 13px; text-transform: uppercase }\n" \
              "table { font-family: 'IBM Plex Mono', monospace; font-size: 14px }"
        self.assertEqual(self.codes(self.scan("a.css", css)), [])

    def test_middot_meta(self):
        html = "<p>May 2026 \u00b7 6 min read \u00b7 Design</p><p>Case study &middot; Fintech</p>"
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_MIDDOT_META"])
        self.assertEqual(self.codes(self.scan("b.html", "<p>Pier 2 \u00b7 On time</p>")), [])

    def test_eyebrow_with_letter_spacing_below_one(self):
        # letter-spacing: 0.12em is positive; the old check read the leading 0 as zero.
        page = "<style>.label { text-transform: uppercase; letter-spacing: 0.12em }</style>" \
               '<p class="label">A</p><h2>One</h2><p class="label">B</p><h2>Two</h2>'
        self.assertEqual(self.codes(self.scan("a.html", page)), ["TELL_EYEBROW_EVERY_HEADING"])

    def test_glass_counts_each_selector_in_a_list(self):
        css = ".card { backdrop-filter: blur(12px) }\n.nav, .footer { backdrop-filter: blur(12px) }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_GLASS_EVERYWHERE"])

    def test_new_rules_are_listed(self):
        for code in ("TELL_SECOND_WAVE_FONT", "TELL_SECOND_WAVE_PALETTE", "TELL_ACCENT_WORD", "TELL_FAKE_SEQUENCE",
                     "TELL_ARROW_EVERY_LINK", "TELL_REVEAL_EVERY_SECTION", "TELL_MONO_LABELS", "TELL_MIDDOT_META"):
            self.assertIn(code, tells.RULES)


class BrandRequiredByValue(Case):
    """Review finding: a token NAME that holds a pattern word silenced real glass, glow and gradient findings."""

    SAAS = ('<style>.a { backdrop-filter: blur(12px) } .b { backdrop-filter: blur(12px) }'
            ' .c { backdrop-filter: blur(12px) }\n.d { box-shadow: 0 0 40px rgba(139, 92, 246, 0.5) }\n'
            '.e { background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899) }</style>\n'
            '<div class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 shadow-purple-500/50"></div>')

    def run_with(self, tokens):
        return self.scan("a.html", self.SAAS, tokens=self.tokens(tokens))

    def test_scrim_and_focus_ring_names_do_not_hide_glass_and_glow(self):
        data = {"color": {"tokens": [{"name": "glass-overlay", "value": "rgba(0, 0, 0, 0.4)", "usage": "Scrim."}]},
                "shadow": {"tokens": [{"name": "shadow-glow-focus", "value": "0 0 0 3px #2563eb", "usage": "Focus."}]}}
        codes = self.codes(self.run_with(data))
        self.assertIn("TELL_GLASS_EVERYWHERE", codes)
        self.assertEqual(codes.count("TELL_GLOW_SHADOW"), 2)
        self.assertEqual(self.required(self.run_with(data)), [])

    def test_ramp_tokens_do_not_make_a_brand_gradient(self):
        data = {"color": {"tokens": [{"name": "indigo-500", "value": "#6366f1", "usage": "Ramp."},
                                     {"name": "purple-500", "value": "#a855f7", "usage": "Ramp."},
                                     {"name": "pink-500", "value": "#ec4899", "usage": "Ramp."}]}}
        result = self.run_with(data)
        self.assertEqual(self.codes(result).count("TELL_PURPLE_GRADIENT"), 2)
        self.assertNotIn("TELL_PURPLE_GRADIENT", self.required(result))

    def test_matching_values_are_brand_required(self):
        data = {"color": {"tokens": [{"name": "indigo-500", "value": "#6366f1", "usage": "Ramp."},
                                     {"name": "purple-500", "value": "#a855f7", "usage": "Ramp."},
                                     {"name": "pink-500", "value": "#ec4899", "usage": "Ramp."}]},
                "gradient": {"tokens": [{"name": "brand", "value": "linear-gradient(90deg, {indigo-500}, "
                                                                   "{purple-500}, {pink-500})", "usage": "Hero."}]},
                "blur": {"tokens": [{"name": "surface", "value": "blur(12px)", "usage": "Glass."}]},
                "shadow": {"tokens": [{"name": "halo", "value": "0 0 40px rgba(139, 92, 246, 0.5)", "usage": "CTA."}]}}
        result = self.run_with(data)
        required = self.required(result)
        self.assertEqual(required.count("TELL_PURPLE_GRADIENT"), 2)
        self.assertIn("TELL_GLASS_EVERYWHERE", required)
        self.assertIn("TELL_GLOW_SHADOW", required)
        # The Tailwind colored shadow has no matching token value, so it stays a finding.
        self.assertEqual(self.codes(result), ["TELL_GLOW_SHADOW"])

    def test_a_blur_token_of_another_size_keeps_the_glass_finding(self):
        data = {"blur": {"tokens": [{"name": "scrim", "value": "blur(4px)", "usage": "Modal scrim."}]}}
        self.assertIn("TELL_GLASS_EVERYWHERE", self.codes(self.run_with(data)))


class ColorUnits(Case):
    """Review finding: hsl hue in turn, rad or grad was read as degrees or dropped."""

    def test_hue_units(self):
        purple = tells.parse_color("hsl(270deg 80% 60%)")
        for text in ("hsl(0.75turn 80% 60%)", "hsl(300grad 80% 60%)", "hsl(4.71239rad 80% 60%)", "hsl(270 80% 60%)"):
            got = tells.parse_color(text)
            self.assertIsNotNone(got, text)
            self.assertEqual(tells.to_hex(got), tells.to_hex(purple), text)
        self.assertEqual(tells.to_hex(tells.parse_color("oklch(0.6 0.2 0.8turn)")),
                         tells.to_hex(tells.parse_color("oklch(0.6 0.2 288)")))

    def test_turn_gradient_is_found(self):
        css = ".x { background: linear-gradient(hsl(0.75turn 80% 55%), hsl(0.62turn 80% 55%)); }"
        self.assertEqual(self.codes(self.scan("a.css", css)), ["TELL_PURPLE_GRADIENT"])

    def test_parity_with_the_design_system_parser(self):
        # Each skill folder ships alone, so the color math is not shared. This test keeps the copies in step.
        spec = importlib.util.spec_from_file_location(
            "gdh_ds_parity", os.path.join(ROOT, "kit", "skills", "design-system", "scripts", "ds.py"))
        ds = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ds)
        for text in ("#7c3aed", "rgb(37 99 235)", "hsl(0.75turn 80% 60%)", "hsl(300grad 80% 60%)",
                     "hsl(4.71239rad 80% 60%)", "oklch(0.62 0.19 300)", "rebeccapurple"):
            ours = tells.to_hex(tells.parse_color(text))
            theirs = ds.parse_color(text, allow_named=True).hex6()
            self.assertEqual(ours, theirs, text)


class EmojiInMessages(Case):
    """Review finding: an emoji at the end of a chat message was reported as an icon."""

    def test_emoji_ending_a_sentence_is_content(self):
        html = "<p class=\"msg\">My order came today, the jars are perfect %s</p>\n" \
               "<p class=\"msg\">%s thanks for packing them so well today</p>" % (ROCKET, BOLT)
        self.assertEqual(self.codes(self.scan("a.html", html)), [])

    def test_emoji_beside_a_short_label_is_still_an_icon(self):
        html = "<h3>%s Launch faster</h3>" % ROCKET
        self.assertEqual(self.codes(self.scan("a.html", html)), ["TELL_EMOJI_ICON"])
        self.assertEqual(self.codes(self.scan("b.tsx", 'const f = [{icon: "%s", t: "Fast"}];' % BOLT)),
                         ["TELL_EMOJI_ICON"])


class ScanCompleteness(Case):
    """Review finding: the scan passed on input it never read."""

    def test_large_single_file_page_is_scanned_after_data_uris_are_removed(self):
        blob = "A" * (tells.MAX_BYTES + 1000)
        html = '<img src="data:image/png;base64,%s">\n<p>Lorem ipsum dolor sit amet</p>' % blob
        path = self.write("page.html", html)
        code, out, _ = self.cli([path, "--json"])
        data = json.loads(out)
        self.assertEqual(code, 1)
        self.assertEqual(data["scanned"], 1)
        self.assertTrue(data["complete"])
        self.assertIn("TELL_LOREM", [f["code"] for f in data["findings"]])

    def test_dot_folder_is_reported_and_scanned_when_named(self):
        self.write("proj/src/a.css", ".a { color: var(--ink); }")
        self.write("proj/.site/index.html", "<p>Lorem ipsum dolor sit amet</p>")
        code, out, _ = self.cli([os.path.join(self.tmp, "proj"), "--json"])
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(data["leftOut"], [os.path.join(self.tmp, "proj", ".site")])
        code, out, _ = self.cli([os.path.join(self.tmp, "proj")])
        self.assertIn("Folders left out", out)
        self.assertEqual(self.cli([os.path.join(self.tmp, "proj", ".site")])[0], 1)

    def test_only_a_dot_folder_exits_two_and_names_it(self):
        self.write("site/.site/index.html", "<p>Lorem ipsum dolor sit amet</p>")
        code, _, err = self.cli([os.path.join(self.tmp, "site")])
        self.assertEqual(code, 2)
        self.assertIn(".site", err)


class RepositoryFiles(unittest.TestCase):
    """Smoke tests on real files of this repository: a generic fixture and the example brand specimen."""

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = tells.main(list(argv))
        return code, out.getvalue()

    def test_generic_fixture_is_flagged(self):
        fixture = os.path.join(ROOT, "tests", "fixtures", "generic-landing.html")
        code, out = self.run_cli(fixture, "--json")
        self.assertEqual(code, 1)
        found = set(f["code"] for f in json.loads(out)["findings"])
        for expected in ("TELL_PURPLE_GRADIENT", "TELL_GRADIENT_TEXT", "TELL_GLOW_SHADOW", "TELL_LOREM",
                         "TELL_HERO_THREE_CARDS", "TELL_EYEBROW_EVERY_HEADING", "TELL_DEFAULT_FONT_ONLY"):
            self.assertIn(expected, found)

    def test_example_brand_specimen_is_clean(self):
        pack = os.path.join(ROOT, "brands", "example-harbor-lantern")
        code, out = self.run_cli(os.path.join(pack, "specimen.html"), "--tokens", os.path.join(pack, "tokens.json"),
                                 "--design", os.path.join(pack, "DESIGN.md"), "--json")
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(out)["findings"], [])

    def test_example_brand_sample_is_clean_without_a_default_face(self):
        pack = os.path.join(ROOT, "brands", "example-harbor-lantern")
        code, out = self.run_cli(os.path.join(pack, "sample.html"), os.path.join(pack, "specimen.html"),
                                 "--tokens", os.path.join(pack, "tokens.json"),
                                 "--design", os.path.join(pack, "DESIGN.md"), "--json")
        self.assertEqual(code, 0, out)
        data = json.loads(out)
        self.assertEqual(data["findings"], [])
        self.assertNotIn("TELL_DEFAULT_FONT_ONLY", [item["code"] for item in data["brandRequired"]])


if __name__ == "__main__":
    unittest.main()
