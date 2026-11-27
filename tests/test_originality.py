"""Tests for kit/skills/originality-gate/scripts/originality.py.

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
SCRIPT = os.path.join(ROOT, "kit", "skills", "originality-gate", "scripts", "originality.py")
LIBRARY = os.path.join(ROOT, "kit", "skills", "originality-gate", "references", "generic-fingerprints.json")

_spec = importlib.util.spec_from_file_location("gdh_originality", SCRIPT)
originality = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(originality)

GENERIC = """<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600" rel="stylesheet"></head>
<body class="bg-white font-sans text-slate-900">
<header><nav class="flex"><a>Flowly</a><a>Features</a><a>Pricing</a>
<a class="rounded-xl bg-indigo-600 text-white">Get started</a></nav></header>
<section class="hero text-center"><h1 class="text-6xl bg-gradient-to-r from-indigo-500 via-purple-500
 to-pink-500 bg-clip-text text-transparent">Supercharge your team with AI-powered workflows</h1>
<p class="text-xl">The all-in-one platform to streamline your work. Seamless from day one.</p>
<a class="rounded-xl bg-indigo-600 shadow-lg transition">Start your free trial</a>
<p class="text-sm">No credit card required</p></section>
<section><p class="text-sm">Trusted by teams</p><div class="flex"><img src="a.svg"><img src="b.svg">
<img src="c.svg"><img src="d.svg"><img src="e.svg"></div></section>
<section id="features"><h2 class="text-4xl">Everything you need</h2><div class="grid md:grid-cols-3">
<div class="rounded-2xl shadow-md"><h3 class="text-xl">Automate</h3><p>Effortless automation.</p></div>
<div class="rounded-2xl shadow-md"><h3 class="text-xl">Analyze</h3><p>Lightning fast reports.</p></div>
<div class="rounded-2xl shadow-md"><h3 class="text-xl">Share</h3><p>Built for teams.</p></div></div></section>
<section class="testimonials"><h2>Loved by thousands</h2><blockquote class="rounded-2xl">It changed how we work.</blockquote>
<blockquote class="rounded-2xl">Best tool we bought.</blockquote></section>
<section id="pricing"><h2>Simple, transparent pricing</h2><div class="rounded-2xl"><h3>Free</h3><p>$0/mo</p></div>
<div class="rounded-2xl"><h3>Pro</h3><p>$19/mo</p></div><div class="rounded-2xl"><h3>Team</h3><p>$49/mo</p></div></section>
<section id="faq"><h2>Frequently asked questions</h2><details><summary>Free plan?</summary></details>
<details><summary>Cancel?</summary></details></section>
<section class="bg-indigo-600 text-center"><h2 class="text-3xl">Ready to get started?</h2>
<a class="rounded-xl bg-white text-indigo-600">Get started today</a></section>
<footer><ul><li>Product</li></ul><ul><li>Company</li></ul><ul><li>Legal</li></ul></footer>
</body></html>"""

DISTINCT = """<!doctype html><html><head><style>
body{font-family:"Alegreya Sans",sans-serif;background:#e9eef0;color:#13262b}
.tide{font-family:"Recursive",monospace}
h1{font-size:44px} p{font-size:17px}
.mark{background:#1f5c4a;color:#e9eef0} .buoy{color:#e0a100}
</style></head><body>
<header><a href="/">Harbor Ferry Cooperative</a></header>
<main>
<section class="timeline"><h1>Tonight the 21:40 leaves from Pier 3, two minutes late</h1>
<ol><li>19:10 Pier 1</li><li>20:25 Pier 2</li><li>21:40 Pier 3</li><li>23:05 Pier 1</li></ol></section>
<section class="map"><svg viewBox="0 0 400 200"><path d="M0 100 L400 100" stroke="#1f5c4a"/>
<circle cx="120" cy="100" r="6" fill="#e0a100"/></svg><p>The boat is past the breakwater.</p></section>
<section><table class="tide"><tr><th>Day</th><th>High water</th></tr><tr><td>Mon</td><td>06:12</td></tr></table></section>
<section><p>Crew members own the cooperative.</p><p>Fares stay the same at every hour.</p>
<p>Bikes ride free on the lower deck.</p></section>
</main>
<footer><p>Harbor Ferry Cooperative, Pier 1 office</p></footer>
</body></html>"""


CANONICAL = (
    '<html><body class="bg-gradient-to-br from-purple-600 to-indigo-600"><section class="hero text-center">'
    '<h1 class="text-6xl font-bold">Supercharge your workflow with AI</h1>'
    '<p>Unlock the power of seamless productivity</p><a class="rounded-full">Get started</a></section>'
    '<section class="grid grid-cols-3"><div class="card rounded-xl shadow-lg">Fast</div>'
    '<div class="card rounded-xl shadow-lg">Secure</div><div class="card rounded-xl shadow-lg">Scalable</div>'
    '</section><section>Trusted by logos</section><section class="pricing"><div>Starter</div><div>Pro</div>'
    '<div>Enterprise</div></section></body></html>')


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = originality.main(argv)
    return code, out.getvalue(), err.getvalue()


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-originality-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path


class FingerprintTests(Case):
    def test_generic_skeleton_and_fields(self):
        fp, _skipped = originality.fingerprint([self.write("generic.html", GENERIC)])
        self.assertEqual(fp["skeleton"][:4], ["nav-bar", "hero-centered", "logo-strip", "three-card-row"])
        for archetype in ("testimonial-grid", "pricing-tiers", "faq-accordion", "cta-band", "footer-columns"):
            self.assertIn(archetype, fp["skeleton"])
        self.assertIn("inter", fp["typefaces"])
        self.assertGreaterEqual(fp["gradients"], 1)
        self.assertEqual(fp["dominantRadius"], 16)
        self.assertTrue(fp["motion"]["transition"])
        self.assertIn("supercharge", fp["copyCliches"])
        self.assertEqual(fp["ground"], "light")

    def test_distinct_skeleton(self):
        fp, _skipped = originality.fingerprint([self.write("ferry.html", DISTINCT)])
        self.assertEqual(fp["skeleton"], ["nav-bar", "timeline-rail", "map-led", "data-table",
                                          "prose-block", "footer-simple"])
        self.assertEqual(fp["copyCliches"], [])
        self.assertEqual(fp["gradients"], 0)

    def test_color_forms_normalise_to_one_hex(self):
        forms = ["#3b82f6", "rgb(59, 130, 246)", "rgb(59 130 246 / 50%)", "hsl(217.2 91.2% 59.8%)"]
        self.assertEqual(set(originality.parse_color(f) for f in forms), {"#3b82f6"})
        self.assertEqual(originality.parse_color("#38f"), "#3388ff")
        self.assertTrue(originality.parse_color("oklch(0.62 0.21 260)").startswith("#"))

    def test_dashboard_skeleton(self):
        html = """<body><aside class="sidebar"><nav><a>Home</a></nav></aside><main>
        <header class="topbar"><input></header>
        <div class="kpis"><div><p>Revenue</p><span>$45,231</span></div><div><p>Users</p><span>+2350</span></div>
        <div><p>Sales</p><span>12,234</span></div></div>
        <section class="chart"><canvas></canvas></section><section><table><tr><td>x</td></tr></table></section>
        </main></body>"""
        fp, _skipped = originality.fingerprint([self.write("dash.html", html)])
        self.assertEqual(fp["skeleton"], ["sidebar-nav", "topbar", "kpi-cards", "chart-panel", "data-table"])


class CompareTests(Case):
    def test_identical_is_one(self):
        fp, _ = originality.fingerprint([self.write("generic.html", GENERIC)])
        self.assertEqual(originality.compare(fp, fp)["similarity"], 1.0)

    def test_symmetric(self):
        a, _ = originality.fingerprint([self.write("generic.html", GENERIC)])
        b, _ = originality.fingerprint([self.write("ferry.html", DISTINCT)])
        ab, ba = originality.compare(a, b), originality.compare(b, a)
        self.assertEqual(ab["similarity"], ba["similarity"])
        self.assertEqual(ab["dimensions"], ba["dimensions"])
        self.assertLess(ab["similarity"], 0.5)

    def test_library_is_symmetric(self):
        with open(LIBRARY, "r", encoding="utf-8") as handle:
            archetypes = json.load(handle)["archetypes"]
        self.assertGreaterEqual(len(archetypes), 8)
        for x in archetypes:
            self.assertEqual(originality.compare(x["fingerprint"], x["fingerprint"])["similarity"], 1.0)
            for y in archetypes:
                self.assertEqual(originality.compare(x["fingerprint"], y["fingerprint"])["similarity"],
                                 originality.compare(y["fingerprint"], x["fingerprint"])["similarity"])

    def test_compare_cli(self):
        a = self.write("a.html", GENERIC)
        code, out, _ = run(["compare", a, a, "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["similarity"], 1.0)


class CheckTests(Case):
    def test_generic_is_derivative(self):
        path = self.write("generic.html", GENERIC)
        code, out, _ = run(["check", path, "--json"])
        self.assertEqual(code, 1)
        report = json.loads(out)
        self.assertEqual(report["verdict"], "derivative")
        self.assertEqual(report["nearest"]["id"], "ai-saas-landing")
        self.assertIn("skeleton", report["nearest"]["drivers"])
        self.assertTrue(report["line"].startswith("Originality: derivative (score 0."))
        self.assertEqual(report["findings"][0]["severity"], "high")
        self.assertEqual(set(report["findings"][0]), {"code", "severity", "line", "message"})

    def test_canonical_generic_page_is_derivative(self):
        path = self.write("canonical.html", CANONICAL)
        fp, _ = originality.fingerprint([path])
        self.assertEqual(fp["skeleton"], ["hero-centered", "three-card-row", "logo-strip", "pricing-tiers"])
        for phrase in ("supercharge", "unlock the power", "seamless", "get started", "trusted by"):
            self.assertIn(phrase, fp["copyCliches"])
        code, out, _ = run(["check", path, "--json"])
        self.assertEqual(code, 1)
        report = json.loads(out)
        self.assertEqual(report["verdict"], "derivative")
        self.assertEqual(report["nearest"]["id"], "ai-saas-landing")
        self.assertGreaterEqual(report["nearest"]["genericRun"], 3)
        self.assertIn("STACK_SKELETON_COPY", report["nearest"]["stacking"])
        self.assertIn("STACK_SKELETON_GRADIENT", report["nearest"]["stacking"])

    def test_stacking_rule_overrides_the_average(self):
        path = self.write("canonical.html", CANONICAL)
        code, out, _ = run(["check", path, "--json", "--threshold", "0.99", "--watch", "0.98"])
        self.assertEqual(code, 1)
        report = json.loads(out)
        self.assertEqual(report["verdict"], "derivative")
        self.assertLess(report["score"], 0.99)
        self.assertIn("Stacking rule", report["findings"][0]["message"])

    def test_no_stacking_on_a_short_run(self):
        a, _ = originality.fingerprint([self.write("ferry.html", DISTINCT)])
        b, _ = originality.fingerprint([self.write("canonical.html", CANONICAL)])
        result = originality.compare(a, b)
        self.assertEqual(result["stacking"], [])
        self.assertEqual(result, originality.compare(b, a))

    def test_distinct_is_original(self):
        path = self.write("ferry.html", DISTINCT)
        code, out, _ = run(["check", path, "--json"])
        self.assertEqual(code, 0)
        report = json.loads(out)
        self.assertEqual(report["verdict"], "original")
        self.assertEqual(report["findings"], [])
        self.assertLess(report["score"], originality.DEFAULT_WATCH)

    def test_against_earlier_direction(self):
        path = self.write("ferry.html", DISTINCT)
        earlier = os.path.join(self.tmp, "earlier.json")
        self.assertEqual(run(["fingerprint", path, "-o", earlier])[0], 0)
        code, out, _ = run(["check", path, "--against", earlier, "--json"])
        self.assertEqual(code, 1)
        report = json.loads(out)
        self.assertEqual(report["nearest"]["id"], "earlier")
        self.assertEqual(report["score"], 1.0)

    def test_watch_verdict_has_medium_finding(self):
        path = self.write("ferry.html", DISTINCT)
        code, out, _ = run(["check", path, "--json", "--watch", "0.1", "--threshold", "0.99"])
        self.assertEqual(code, 0)
        report = json.loads(out)
        self.assertEqual(report["verdict"], "watch")
        self.assertEqual(report["findings"][0]["severity"], "medium")

    def test_text_output_has_verdict_line(self):
        code, out, _ = run(["check", self.write("generic.html", GENERIC)])
        self.assertEqual(code, 1)
        self.assertIn("Originality: derivative (score 0.", out)
        self.assertIn("nearest ai-saas-landing)", out)

    def test_usage_errors_exit_two(self):
        self.assertEqual(run(["check", os.path.join(self.tmp, "missing.html")])[0], 2)
        self.assertEqual(run(["fingerprint", self.write("notes.txt", "hello")])[0], 2)
        self.assertEqual(run([])[0], 2)
        self.assertEqual(run(["check", self.write("g.html", GENERIC), "--watch", "0.9", "--threshold", "0.5"])[0], 2)
        self.assertEqual(run(["check", "--bogus"])[0], 2)

    def test_list(self):
        code, out, _ = run(["list", "--json"])
        self.assertEqual(code, 0)
        ids = [item["id"] for item in json.loads(out)["archetypes"]]
        self.assertIn("ai-saas-landing", ids)
        self.assertIn("default-shadcn-admin", ids)


if __name__ == "__main__":
    unittest.main()
