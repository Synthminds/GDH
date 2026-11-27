#!/usr/bin/env python3
"""originality.py: fingerprint a design and measure how close it sits to generic templates.

A fingerprint is a small JSON summary of a design file set: the ordered section
archetypes (the layout skeleton), the typeface families, the number of distinct
font sizes, the palette, the hue spread, gradient and effect use, corner radii,
shadows, motion and generic marketing phrases.

  originality.py fingerprint <path>... [-o out.json] [--json]
  originality.py compare <a> <b> [--json]
  originality.py check <path>... [--against <file or folder>]... [--library <file>]
                 [--threshold 0.75] [--watch 0.60] [--json]
  originality.py list [--library <file>] [--json]

`compare` and `--against` take fingerprint JSON files, library files or design files.
A design file is fingerprinted on the fly.

The parse is static. It reads source text with regular expressions and
html.parser. It renders nothing. A low score does not prove original work, and
a high score is a lead for a reviewer, not a verdict on its own.

Python 3.9+, standard library only. No network calls. Writes only the path given to -o.
Exit codes: 0 pass, 1 derivative verdict, 2 usage error or no file read.
"""

import argparse
import colorsys
import json
import math
import os
import re
import sys
from collections import Counter, OrderedDict
from html.parser import HTMLParser

VERSION = "0.1.0"
SCHEMA = 1
NOTE = ("Heuristic only. The fingerprint reads source text and renders nothing. "
        "Run the human tests before you write the verdict.")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LIBRARY = os.path.join(os.path.dirname(HERE), "references", "generic-fingerprints.json")

DEFAULT_THRESHOLD = 0.75
DEFAULT_WATCH = 0.60
MAX_BYTES = 2 * 1024 * 1024
EXTENSIONS = (".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".svg")
SKIP_DIRS = ("node_modules", "dist", "build", "__pycache__")

# Dimension weights. Default: these weights are a GDH starting value, not a measured result.
WEIGHTS = OrderedDict([
    ("skeleton", 0.36),
    ("palette", 0.14),
    ("type", 0.12),
    ("gradient", 0.08),
    ("copy", 0.07),
    ("radius", 0.07),
    ("effects", 0.06),
    ("shadow", 0.03),
    ("motion", 0.03),
    ("fontSizes", 0.02),
    ("hueSpread", 0.02),
])

# Stacking rules. Default: a GDH starting value, not a measured result.
# A shared run of generic sections, in order, of this length or more starts the rules.
STACK_RUN = 3
# The run plus this many marketing phrases on each side is derivative.
STACK_CLICHES = 2
# The run plus a gradient on each side whose chromatic mass sits this much in the violet band is derivative.
STACK_VIOLET_SHARE = 0.5
VIOLET_BINS = (7, 8, 9, 10)

# ---------------------------------------------------------------------------
# Vocabulary

SECTION_TAGS = {"header", "nav", "section", "footer", "aside", "article", "form"}
SKIP_TAGS = {"script", "style", "head", "meta", "link", "title", "template", "noscript"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
             "source", "track", "wbr", "param"}
SECTION_WORDS = {
    "hero", "banner", "jumbotron", "features", "pricing", "plans", "tiers",
    "testimonials", "reviews", "faq", "faqs", "accordion", "logos", "clients",
    "partners", "brands", "cta", "stats", "metrics", "footer", "navbar", "sidebar",
    "topbar", "kpis", "bento", "gallery", "team", "contact", "newsletter",
    "steps", "timeline", "map", "section", "showcase",
}
WRAPPER_MARKERS = {"section", "header", "footer", "aside", "nav", "main"}
CAROUSEL_WORDS = {"carousel", "slider", "swiper", "embla", "splide", "glide", "slick", "marquee"}
CENTER_CLASSES = {"text-center", "items-center", "mx-auto", "justify-center", "place-items-center",
                  "text-align-center", "centered", "center"}
TWO_COL_RE = re.compile(r"(?:^|:)(?:grid-cols-2|columns-2|flex-row|md:flex-row|lg:flex-row)$")
SPAN_RE = re.compile(r"(?:^|:)(?:col-span-[2-9]|row-span-[2-9]|col-span-full)$")

ARCHETYPE_FAMILY = {
    "nav-bar": "nav", "topbar": "nav", "sidebar-nav": "nav",
    "hero-centered": "hero", "hero-split": "hero", "hero-media": "hero", "hero-plain": "hero",
    "three-card-row": "cards", "card-grid": "cards", "bento-grid": "cards",
    "logo-strip": "proof", "testimonial-grid": "proof", "testimonial-carousel": "proof",
    "pull-quote": "proof", "stat-row": "proof",
    "pricing-tiers": "pricing", "faq-accordion": "faq",
    "cta-band": "cta", "form-block": "cta",
    "footer-columns": "footer", "footer-simple": "footer",
    "kpi-cards": "data", "chart-panel": "data", "data-table": "data",
    "media-text-split": "media", "media-gallery": "media",
}

ARCHETYPES = sorted(set(ARCHETYPE_FAMILY) | {"prose-block", "content-block", "steps-list",
                                             "timeline-rail", "map-led"})

GENERIC_FAMILIES = {"sans-serif", "serif", "monospace", "cursive", "fantasy", "system-ui",
                    "ui-sans-serif", "ui-serif", "ui-monospace", "-apple-system",
                    "blinkmacsystemfont", "inherit", "initial", "unset", "var"}
TYPE_CLASS = {
    "default-sans": ["inter", "roboto", "arial", "helvetica", "helvetica neue", "segoe ui",
                     "open sans", "system-ui", "(default)", "noto sans", "lato"],
    "second-wave-sans": ["geist", "space grotesk", "dm sans", "poppins", "manrope",
                         "plus jakarta sans", "outfit", "sora", "montserrat", "satoshi",
                         "general sans", "cal sans"],
    "second-wave-serif": ["instrument serif", "fraunces", "playfair display", "dm serif display",
                          "newsreader", "lora", "cormorant garamond"],
    "default-mono": ["geist mono", "jetbrains mono", "fira code", "ibm plex mono", "menlo",
                     "sf mono", "roboto mono", "space mono"],
}
FAMILY_TO_CLASS = {name: cls for cls, names in TYPE_CLASS.items() for name in names}

# Matched in lower case on visible text. No entry contains another, so one phrase counts once.
COPY_CLICHES = [
    "unlock the power", "unlock your", "harness the power", "unleash", "supercharge", "seamless",
    "revolutionize", "reimagine", "next-generation", "next generation", "next-level", "next level",
    "level up", "cutting-edge", "all-in-one", "all in one place", "game-changer", "game changer",
    "streamline your", "boost productivity", "boost your productivity", "effortless", "empower your",
    "elevate your", "transform the way", "the future of", "like never before", "made simple",
    "without the hassle", "take control of", "ai-powered", "powered by ai", "built for teams",
    "built for modern", "for the modern", "trusted by", "loved by", "join thousands",
    "join the waitlist", "no credit card required", "start your free trial", "get started",
    "simple, transparent pricing", "everything you need", "in minutes, not", "blazing fast",
    "lightning fast", "at scale", "scale with confidence", "world-class", "best-in-class",
    "say goodbye to", "work smarter",
]

# Section archetypes that make up generic templates. Navigation bars, plain footers and
# subject-led blocks (timeline, map, prose) are left out: they carry no template signal.
GENERIC_SECTIONS = {
    "sidebar-nav", "topbar", "hero-centered", "hero-split", "three-card-row", "card-grid",
    "bento-grid", "logo-strip", "testimonial-grid", "testimonial-carousel", "stat-row",
    "pricing-tiers", "faq-accordion", "cta-band", "footer-columns", "kpi-cards", "chart-panel",
    "data-table", "media-text-split",
}

TW_FAMILIES = {
    "slate": "#64748b", "gray": "#6b7280", "zinc": "#71717a", "neutral": "#737373",
    "stone": "#78716c", "red": "#ef4444", "orange": "#f97316", "amber": "#f59e0b",
    "yellow": "#eab308", "lime": "#84cc16", "green": "#22c55e", "emerald": "#10b981",
    "teal": "#14b8a6", "cyan": "#06b6d4", "sky": "#0ea5e9", "blue": "#3b82f6",
    "indigo": "#6366f1", "violet": "#8b5cf6", "purple": "#a855f7", "fuchsia": "#d946ef",
    "pink": "#ec4899", "rose": "#f43f5e",
}
TW_STEP_LIGHTNESS = {"50": 0.97, "100": 0.94, "200": 0.87, "300": 0.77, "400": 0.65,
                     "500": 0.55, "600": 0.46, "700": 0.38, "800": 0.29, "900": 0.22, "950": 0.13}
TW_COLOR_RE = re.compile(r"^(?:bg|text|from|via|to|border|ring|fill|stroke|shadow|outline|decoration|divide)-"
                         r"(white|black|(%s)-(50|[1-9]00|950))(?:/\d+)?$" % "|".join(TW_FAMILIES))
TW_SIZES = {"text-xs": "12px", "text-sm": "14px", "text-base": "16px", "text-lg": "18px",
            "text-xl": "20px", "text-2xl": "24px", "text-3xl": "30px", "text-4xl": "36px",
            "text-5xl": "48px", "text-6xl": "60px", "text-7xl": "72px", "text-8xl": "96px",
            "text-9xl": "128px"}
TW_RADIUS = {"rounded-none": 0, "rounded-sm": 2, "rounded": 4, "rounded-md": 6, "rounded-lg": 8,
             "rounded-xl": 12, "rounded-2xl": 16, "rounded-3xl": 24, "rounded-full": 9999}
TW_FONTS = {"font-sans": "(default)", "font-serif": "(default serif)", "font-mono": "(default mono)"}

NAMED_COLORS = {"white": "#ffffff", "black": "#000000", "red": "#ff0000", "blue": "#0000ff",
                "green": "#008000", "gray": "#808080", "grey": "#808080", "orange": "#ffa500",
                "purple": "#800080", "yellow": "#ffff00", "navy": "#000080", "teal": "#008080"}

COLOR_RE = re.compile(
    r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b"
    r"|\brgba?\([^)]*\)|\bhsla?\([^)]*\)|\boklch\([^)]*\)")
BARE_HSL_RE = re.compile(r"^\s*(-?[\d.]+)(?:deg)?\s+([\d.]+)%\s+([\d.]+)%\s*(?:/\s*[\d.%]+\s*)?$")
DECL_RE = re.compile(r"([-a-zA-Z]+)\s*:\s*([^;{}]+)")
RULE_RE = re.compile(r"([^{}@]+)\{([^{}]*)\}")
FONT_IMPORT_RE = re.compile(r"fonts\.googleapis\.com/css2?\?([^\"')\s>]+)")
NEXT_FONT_RE = re.compile(r"import\s*\{([^}]*)\}\s*from\s*[\"']next/font/(?:google|local)[\"']")
GEIST_RE = re.compile(r"from\s*[\"']geist/font/(sans|mono)[\"']")
PRICE_RE = re.compile(r"[$€£]\s?\d+|/\s?mo\b|per month|/month")
NUMBER_RE = re.compile(r"^\s*[+\-$€£]?\s?\d[\d.,]*\s*(?:%|\+|x|k|m|b|ms|s)?\+?\s*$", re.I)
STYLE_ATTR_JSX_RE = re.compile(r"style=\{\{([^}]*)\}\}")


# ---------------------------------------------------------------------------
# Color helpers

def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def _hex(r, g, b):
    return "#%02x%02x%02x" % tuple(int(round(_clamp(c) * 255)) for c in (r, g, b))


def _num(text, scale=1.0):
    text = text.strip()
    if text.endswith("%"):
        return float(text[:-1]) / 100.0
    return float(text) / scale


def parse_color(text):
    """Return '#rrggbb' or None. Alpha is dropped."""
    text = text.strip().lower()
    if text in NAMED_COLORS:
        return NAMED_COLORS[text]
    try:
        if text.startswith("#"):
            digits = text[1:]
            if len(digits) in (3, 4):
                digits = "".join(c * 2 for c in digits[:3])
            return "#" + digits[:6] if len(digits) >= 6 else None
        inner = text[text.index("(") + 1:text.rindex(")")].replace(",", " ").replace("/", " ")
        parts = inner.split()
        if text.startswith("rgb") and len(parts) >= 3:
            vals = [_num(p, 255.0) if not p.endswith("%") else _num(p) for p in parts[:3]]
            return _hex(*vals)
        if text.startswith("hsl") and len(parts) >= 3:
            hue = float(parts[0].replace("deg", "")) / 360.0
            r, g, b = colorsys.hls_to_rgb(hue % 1.0, _num(parts[2]), _num(parts[1]))
            return _hex(r, g, b)
        if text.startswith("oklch") and len(parts) >= 3:
            return _oklch_to_hex(_num(parts[0]), float(parts[1].rstrip("%")) if not parts[1].endswith("%")
                                 else _num(parts[1]) * 0.4, float(parts[2].replace("deg", "")))
    except (ValueError, IndexError):
        return None
    return None


def _oklch_to_hex(lightness, chroma, hue):
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    l3, m3, s3 = l_ ** 3, m_ ** 3, s_ ** 3
    lin = (4.0767416621 * l3 - 3.3077115913 * m3 + 0.2309699292 * s3,
           -1.2684380046 * l3 + 2.6097574011 * m3 - 0.3413193965 * s3,
           -0.0041960863 * l3 - 0.7034186147 * m3 + 1.7076147010 * s3)

    def gamma(c):
        c = _clamp(c)
        return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return _hex(*(gamma(c) for c in lin))


def tailwind_hex(family, step):
    if family == "white":
        return "#ffffff"
    if family == "black":
        return "#000000"
    base = TW_FAMILIES[family]
    r, g, b = (int(base[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
    hue, _light, sat = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hue, TW_STEP_LIGHTNESS[step], sat)
    return _hex(r, g, b)


def hls_of(hexcode):
    r, g, b = (int(hexcode[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
    return colorsys.rgb_to_hls(r, g, b)


def is_chromatic(hexcode):
    _h, light, sat = hls_of(hexcode)
    return sat >= 0.25 and 0.12 <= light <= 0.92


def luminance(hexcode):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(hexcode[i:i + 2], 16) / 255.0) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def to_px(value):
    value = value.strip().lower()
    match = re.match(r"^(-?[\d.]+)(px|rem|em|%)?$", value)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2) or "px"
    if unit in ("rem", "em"):
        number *= 16
    if unit == "%":
        return 9999.0 if number >= 50 else None
    return number


# ---------------------------------------------------------------------------
# HTML tree

class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "text")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent
        self.text = []

    def elements(self):
        return [c for c in self.children if isinstance(c, Node)]

    def walk(self):
        for child in self.elements():
            yield child
            for sub in child.walk():
                yield sub

    def classes(self):
        raw = (self.attrs.get("class") or "") + " " + (self.attrs.get("classname") or "")
        return [c for c in raw.split() if c and "{" not in c and "}" not in c]

    def words(self):
        toks = set()
        for item in self.classes() + [self.attrs.get("id") or ""]:
            item = item.split(":")[-1].lower()
            toks.add(item)
            toks.update(t for t in re.split(r"[-_/\s]+", item) if t)
        return toks

    def all_text(self):
        parts = list(self.text)
        for child in self.elements():
            if child.tag not in SKIP_TAGS:
                parts.append(child.all_text())
        return " ".join(p for p in parts if p)

    def count(self, *tags):
        return sum(1 for n in self.walk() if n.tag in tags)


class TreeBuilder(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = Node("#root")
        self.stack = [self.root]
        self.styles = []
        self.inline = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = {k.lower(): (v or "") for k, v in attrs}
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if attrs.get("style"):
            self.inline.append((node, attrs["style"]))
        if tag == "style":
            self._in_style = True
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS and self.stack[-1].tag == tag.lower():
            self.stack.pop()

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "style":
            self._in_style = False
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)
            return
        text = data.strip()
        if text:
            self.stack[-1].text.append(text)


# ---------------------------------------------------------------------------
# Section archetypes

class Context:
    def __init__(self, rules):
        self.rules = rules
        self.emitted = []


def node_decls(node, rules):
    decls = {}
    for key in [node.tag] + ["." + c.split(":")[-1] for c in node.classes()] + (
            ["#" + node.attrs["id"]] if node.attrs.get("id") else []):
        decls.update(rules.get(key, {}))
    for name, value in DECL_RE.findall(node.attrs.get("style") or ""):
        decls[name.lower()] = value.strip().lower()
    return decls


def is_candidate(node):
    if node.tag in SECTION_TAGS:
        return True
    return node.tag in ("div", "main", "ul") and bool(node.words() & SECTION_WORDS)


def candidates_below(node, markers_only=False):
    if markers_only:
        return sum(1 for n in node.walk() if n.tag in WRAPPER_MARKERS)
    return sum(1 for n in node.walk() if is_candidate(n))


def has_content(node):
    return bool(node.all_text().strip()) or node.count("img", "svg", "video", "picture", "canvas") > 0 \
        or node.tag in ("img", "svg", "video", "picture", "canvas")


def collect(node, ctx, out):
    buffer = []

    def flush():
        if not buffer:
            return
        if len(buffer) == 1:
            out.append(buffer[0])
        else:
            group = Node("group", {}, node)
            group.children = list(buffer)
            out.append(group)
        del buffer[:]

    for child in node.elements():
        if child.tag in SKIP_TAGS or child.tag in ("br", "hr", "meta", "link"):
            continue
        inner = candidates_below(child)
        if is_candidate(child):
            flush()
            if candidates_below(child, True) >= 2 and child.tag not in ("form",):
                collect(child, ctx, out)
            else:
                out.append(child)
        elif inner >= 1 or child.tag in ("main", "body", "html"):
            flush()
            collect(child, ctx, out)
        elif has_content(child):
            buffer.append(child)
    flush()


def centered(block, rules):
    nodes = [block] + [n for n in block.walk()][:12]
    for n in nodes:
        classes = {c.split(":")[-1] for c in n.classes()}
        if classes & CENTER_CLASSES:
            return True
        decls = node_decls(n, rules)
        if decls.get("text-align") == "center" or decls.get("align-items") == "center" \
                or "auto" in decls.get("margin", "") and n is block:
            return True
    return False


def two_columns(block, rules):
    for n in [block] + list(block.walk()):
        classes = n.classes()
        if any(TWO_COL_RE.search(c) for c in classes):
            return True
        decls = node_decls(n, rules)
        cols = decls.get("grid-template-columns", "")
        if cols and len(cols.split()) == 2 or "repeat(2" in cols:
            return True
    return False


def repeated_group(block):
    """Return (count, has_span) for the largest group of similar sibling items."""
    best, span = 0, False
    for n in [block] + list(block.walk()):
        kids = [k for k in n.elements() if k.tag not in SKIP_TAGS]
        if len(kids) < 2:
            continue
        tags = Counter(k.tag for k in kids)
        tag, number = tags.most_common(1)[0]
        similar = [k for k in kids if k.tag == tag and (k.count("h2", "h3", "h4", "h5", "p", "li") or k.all_text())]
        if len(similar) >= 2 and len(similar) > best and tag not in ("a", "span", "button", "img", "br", "li", "p"):
            best = len(similar)
            span = any(any(SPAN_RE.search(c) for c in k.classes()) or
                       "span" in (k.attrs.get("style") or "") for k in kids)
    return best, span


def classify(block, ctx):
    rules = ctx.rules
    words = block.words()
    text = block.all_text().lower()
    word_count = len(text.split())
    tag = block.tag
    media = block.count("img", "picture", "video") + (1 if tag in ("img", "picture", "video") else 0)
    headings1 = block.count("h1") + (1 if tag == "h1" else 0)
    buttons = block.count("a", "button")
    group, span = repeated_group(block)
    small_numbers = 0
    for n in [block] + list(block.walk()):
        for piece in n.text:
            if NUMBER_RE.match(piece) and re.search(r"\d", piece):
                small_numbers += 1
    dashboard = any(a in ("sidebar-nav", "topbar") for a in ctx.emitted)

    if tag == "footer" or "footer" in words:
        columns = block.count("ul", "ol")
        return "footer-columns" if columns >= 2 or group >= 3 else "footer-simple"
    if tag == "aside" or "sidebar" in words:
        return "sidebar-nav"
    if tag == "nav" or ((tag == "header" or words & {"navbar", "topbar", "header"}) and not headings1
                        and word_count < 40):
        return "topbar" if dashboard or "topbar" in words else "nav-bar"
    if words & {"faq", "faqs", "accordion"} or block.count("details") >= 2 or "frequently asked" in text:
        return "faq-accordion"
    if words & {"pricing", "plans", "tiers"} or len(PRICE_RE.findall(text)) >= 2:
        return "pricing-tiers"
    deep_words = set(words)
    for n in block.walk():
        deep_words |= n.words()
    if words & {"testimonials", "testimonial", "reviews"} or block.count("blockquote") >= 2 \
            or ("what our" in text and "say" in text):
        return "testimonial-carousel" if deep_words & CAROUSEL_WORDS else "testimonial-grid"
    if words & {"logos", "clients", "partners", "brands"} or "trusted by" in text \
            or (media >= 4 and word_count < 25):
        return "logo-strip"
    if "timeline" in words:
        return "timeline-rail"
    if "map" in words:
        return "map-led"
    if headings1:
        if two_columns(block, rules) and (media or block.count("svg", "canvas")):
            return "hero-split"
        decls = node_decls(block, rules)
        if "url(" in decls.get("background-image", "") + decls.get("background", ""):
            return "hero-media"
        if centered(block, rules):
            return "hero-centered"
        return "hero-plain"
    if words & {"kpi", "kpis"} or (small_numbers >= 3 and word_count < 80
                                    and block.count("h2", "h3", "h4") < 3):
        return "kpi-cards" if dashboard or words & {"kpi", "kpis"} else "stat-row"
    if block.count("table") or "table" in words or tag == "table":
        return "data-table"
    if block.count("canvas") or words & {"chart"} or "recharts" in deep_words:
        return "chart-panel"
    if "steps" in words or (block.count("ol") and block.count("li") >= 3 and group < 3):
        return "steps-list"
    if span or "bento" in deep_words:
        return "bento-grid"
    if group == 3:
        return "three-card-row"
    if group >= 4:
        return "card-grid"
    if block.count("blockquote") == 1 or tag == "blockquote":
        return "pull-quote"
    if media and two_columns(block, rules):
        return "media-text-split"
    if block.count("input", "textarea", "select") >= 2 or tag == "form":
        return "form-block" if word_count >= 6 or block.count("input", "textarea", "select") >= 2 else "cta-band"
    if words & {"cta", "newsletter", "signup"} or (1 <= buttons <= 3 and word_count < 45 and
                                                    block.count("h2", "h3", "h2") and not media):
        return "cta-band"
    if media >= 3:
        return "media-gallery"
    if block.count("p") >= 3 or word_count >= 120:
        return "prose-block"
    return "content-block"


def skeleton_of(root, rules):
    body = root
    for n in root.walk():
        if n.tag == "body":
            body = n
            break
    ctx = Context(rules)
    blocks = []
    collect(body, ctx, blocks)
    result = []
    for block in blocks:
        name = classify(block, ctx)
        ctx.emitted.append(name)
        if result and result[-1] == name and name in ("content-block", "prose-block"):
            continue
        result.append(name)
    return result


# ---------------------------------------------------------------------------
# Fingerprint

class Collector:
    def __init__(self):
        self.colors = Counter()
        self.families = Counter()
        self.sizes = set()
        self.radii = Counter()
        self.gradients = 0
        self.blur = 0
        self.shadows = 0
        self.glows = 0
        self.transition = False
        self.animation = False
        self.blobs = 0
        self.skeleton = []
        self.text = []
        self.ground = None
        self.files = []

    def add_color(self, raw, weight=1):
        hexcode = parse_color(raw)
        if hexcode:
            self.colors[hexcode] += weight
        return hexcode


def parse_css(css, col):
    """Read declarations from CSS text. Return simple-selector rules for the tree."""
    rules = {}
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    if "@keyframes" in css:
        col.animation = True
    for selectors, body in RULE_RE.findall(css):
        decls = {name.lower(): value.strip().lower() for name, value in DECL_RE.findall(body)}
        read_decls(decls, col)
        for selector in selectors.split(","):
            selector = selector.strip()
            last = re.split(r"[\s>+~]+", selector)[-1] if selector else ""
            last = last.split(":")[0]
            if re.match(r"^[.#]?[a-zA-Z][\w-]*$", last):
                rules.setdefault(last, {}).update(decls)
            if col.ground is None and re.match(r"^(html|body|:root)$", selector.split(":")[0] if selector != ":root"
                                               else selector):
                for key in ("background-color", "background", "--background", "--bg"):
                    if key in decls:
                        ground = ground_from(decls[key])
                        if ground:
                            col.ground = ground
                            break
    return rules


def ground_from(value):
    match = COLOR_RE.search(value)
    hexcode = parse_color(match.group(0)) if match else None
    if not hexcode:
        bare = BARE_HSL_RE.match(value)
        if bare:
            hexcode = parse_color("hsl(%s %s%% %s%%)" % bare.groups())
        elif value.strip() in NAMED_COLORS:
            hexcode = NAMED_COLORS[value.strip()]
    if not hexcode:
        return None
    return "dark" if luminance(hexcode) < 0.2 else "light"


def read_decls(decls, col):
    for name, value in decls.items():
        if name.startswith("--"):
            bare = BARE_HSL_RE.match(value)
            if bare:
                col.add_color("hsl(%s %s%% %s%%)" % bare.groups())
        for match in COLOR_RE.findall(value):
            col.add_color(match)
        if name in ("color", "background-color", "background", "border-color", "fill", "stroke") \
                and value.strip() in NAMED_COLORS:
            col.add_color(value.strip())
        if "gradient(" in value:
            col.gradients += value.count("gradient(")
        if name == "font-family":
            for family in value.split(","):
                family = family.strip().strip("'\"").lower()
                if family and family not in GENERIC_FAMILIES and not family.startswith("var("):
                    col.families[family] += 1
        if name == "font-size":
            size = value.split()[0] if value.split() else ""
            if size and not size.startswith("var("):
                col.sizes.add(size)
        if name == "font" and re.search(r"\d", value):
            match = re.search(r"([\d.]+(?:px|rem|em|pt))", value)
            if match:
                col.sizes.add(match.group(1))
        if name == "border-radius":
            first = value.split()[0] if value.split() else ""
            px = to_px(first)
            if px is not None:
                col.radii[int(px)] += 1
        if name in ("box-shadow", "filter", "text-shadow"):
            if name == "box-shadow" and value.strip() not in ("none", "0", "initial"):
                col.shadows += 1
                parts = value.split()
                if len(parts) >= 3 and parts[0] in ("0", "0px") and parts[1] in ("0", "0px"):
                    col.glows += 1
            if "drop-shadow" in value:
                col.shadows += 1
            if name == "filter" and re.search(r"blur\(\s*(?:[3-9]\d|\d{3,})px", value):
                col.blobs += 1
        if name in ("backdrop-filter", "-webkit-backdrop-filter") and "blur" in value:
            col.blur += 1
        if name.startswith("transition") and value.strip() not in ("none",):
            col.transition = True
        if name.startswith("animation") and value.strip() not in ("none",):
            col.animation = True


def read_classes(node, col):
    for raw in node.classes():
        cls = raw.split(":")[-1]
        dark_variant = raw.startswith("dark:")
        match = TW_COLOR_RE.match(cls)
        if match:
            family = match.group(2) or match.group(1)
            step = match.group(3) or "500"
            hexcode = tailwind_hex(family, step)
            if not dark_variant:
                col.colors[hexcode] += 1
        elif re.match(r"^(?:bg|text|from|via|to|border)-\[(#[0-9a-fA-F]{3,8}|rgb[^\]]+|hsl[^\]]+)\]$", cls):
            col.add_color(cls[cls.index("[") + 1:-1].replace("_", " "))
        if cls in TW_SIZES:
            col.sizes.add(TW_SIZES[cls])
        elif re.match(r"^text-\[\d", cls):
            col.sizes.add(cls[6:-1])
        if cls in TW_RADIUS:
            col.radii[TW_RADIUS[cls]] += 1
        elif re.match(r"^rounded-\[[\d.]+(px|rem)\]$", cls):
            px = to_px(cls[8:-1])
            if px is not None:
                col.radii[int(px)] += 1
        if re.match(r"^bg-(?:gradient|linear|radial|conic)-", cls):
            col.gradients += 1
        if re.match(r"^backdrop-blur", cls):
            col.blur += 1
        if re.match(r"^(?:shadow|drop-shadow)(?:-(?:sm|md|lg|xl|2xl|inner))?$", cls):
            col.shadows += 1
        if re.match(r"^shadow-(%s)-" % "|".join(TW_FAMILIES), cls):
            col.glows += 1
        if re.match(r"^blur-(?:2xl|3xl|\[)", cls):
            col.blobs += 1
        if re.match(r"^(?:transition|duration-|ease-)", cls):
            col.transition = True
        if re.match(r"^animate-(?!none)", cls):
            col.animation = True
        if cls in TW_FONTS:
            col.families[TW_FONTS[cls]] += 1
        elif re.match(r"^font-\['?([^\]]+)'?\]$", cls):
            col.families[cls[6:-1].strip("'").replace("_", " ").lower()] += 1


def fingerprint_html(text, col, is_markup=True):
    builder = TreeBuilder()
    try:
        builder.feed(text)
        builder.close()
    except Exception:  # html.parser can raise on broken markup; keep what was read
        pass
    rules = {}
    for css in builder.styles:
        rules.update(parse_css(css, col))
    for node, style in builder.inline:
        read_decls({n.lower(): v.strip().lower() for n, v in DECL_RE.findall(style)}, col)
    for body in STYLE_ATTR_JSX_RE.findall(text):
        decls = {}
        for name, value in re.findall(r"([a-zA-Z]+)\s*:\s*[\"']([^\"']+)[\"']", body):
            decls[re.sub(r"([A-Z])", r"-\1", name).lower()] = value.lower()
        read_decls(decls, col)
    for query in FONT_IMPORT_RE.findall(text):
        for family in re.findall(r"family=([^:&]+)", query):
            col.families[family.replace("+", " ").lower()] += 1
    for names in NEXT_FONT_RE.findall(text):
        for name in names.split(","):
            name = name.strip().split(" as ")[0].strip()
            if name:
                col.families[name.replace("_", " ").lower()] += 1
    for kind in GEIST_RE.findall(text):
        col.families["geist" if kind == "sans" else "geist mono"] += 1
    if re.search(r"<motion\.|\b(?:initial|animate|whileInView)=\{", text):
        col.animation = True
    for node in builder.root.walk():
        read_classes(node, col)
        words = node.words()
        if words & {"blob", "orb", "glow", "aurora"}:
            col.blobs += 1
        if col.ground is None and node.tag in ("html", "body"):
            for cls in node.classes():
                match = TW_COLOR_RE.match(cls)
                if match and cls.startswith("bg-") and ":" not in cls:
                    col.ground = "dark" if luminance(tailwind_hex(match.group(2) or match.group(1),
                                                                  match.group(3) or "500")) < 0.2 else "light"
    if col.ground is None:
        for node in builder.root.walk():
            cls_list = [c for c in node.classes() if ":" not in c]
            if "min-h-screen" in cls_list or node.tag in ("main",):
                for cls in cls_list:
                    match = TW_COLOR_RE.match(cls)
                    if match and cls.startswith("bg-"):
                        hexcode = tailwind_hex(match.group(2) or match.group(1), match.group(3) or "500")
                        col.ground = "dark" if luminance(hexcode) < 0.2 else "light"
                        break
            if col.ground:
                break
    if is_markup:
        col.skeleton.extend(skeleton_of(builder.root, rules))
        col.text.append(builder.root.all_text())


def fingerprint_svg(text, col):
    for match in re.findall(r"(?:fill|stroke|stop-color)\s*=\s*[\"']([^\"']+)[\"']", text):
        col.add_color(match)
    col.gradients += len(re.findall(r"<(?:linear|radial)Gradient\b", text))
    for css in re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.S):
        parse_css(css, col)


def gather(paths):
    files, skipped = [], []
    for path in paths:
        if os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS)
                for name in sorted(filenames):
                    if name.lower().endswith(EXTENSIONS):
                        files.append(os.path.join(dirpath, name))
        elif os.path.isfile(path):
            if path.lower().endswith(EXTENSIONS):
                files.append(path)
            else:
                skipped.append((path, "extension not read"))
        else:
            skipped.append((path, "not found"))
    return files, skipped


def fingerprint(paths):
    files, skipped = gather(paths)
    col = Collector()
    read = []
    for path in files:
        try:
            if os.path.getsize(path) > MAX_BYTES:
                skipped.append((path, "larger than 2 MB"))
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError as error:
            skipped.append((path, str(error)))
            continue
        lower = path.lower()
        if lower.endswith((".css", ".scss")):
            parse_css(text, col)
        elif lower.endswith(".svg"):
            fingerprint_svg(text, col)
        else:
            fingerprint_html(text, col)
        read.append(path)
    return build_fingerprint(col, read), skipped


def hue_stats(colors):
    chroma = [(hls_of(h)[0] * 360.0, n) for h, n in colors.items() if is_chromatic(h)]
    total = sum(colors.values()) or 1
    chroma_weight = sum(n for _h, n in chroma)
    bins = [0.0] * 12
    for hue, weight in chroma:
        position = hue / 30.0 - 0.5
        low = int(math.floor(position)) % 12
        frac = position - math.floor(position)
        bins[low] += weight * (1 - frac)
        bins[(low + 1) % 12] += weight * frac
    if chroma_weight:
        bins = [round(b / chroma_weight, 4) for b in bins]
    hues = sorted(set(round(h, 1) for h, _n in chroma))
    spread = None
    dominant = None
    if hues:
        gaps = [(hues[(i + 1) % len(hues)] - hues[i]) % 360 for i in range(len(hues))]
        spread = round(360.0 - max(gaps), 1) if len(hues) > 1 else 0.0
        x = sum(math.cos(math.radians(h)) * n for h, n in chroma)
        y = sum(math.sin(math.radians(h)) * n for h, n in chroma)
        dominant = round(math.degrees(math.atan2(y, x)) % 360, 1)
    return {"hueHistogram": bins, "chromaShare": round(chroma_weight / float(total), 4),
            "hueSpread": spread, "dominantHue": dominant}


def build_fingerprint(col, read):
    text = " ".join(col.text).lower()
    text = re.sub(r"\s+", " ", text)
    cliches = sorted(set(p for p in COPY_CLICHES if p in text))
    families = sorted(col.families, key=lambda f: (-col.families[f], f))
    radii = sorted(col.radii.items(), key=lambda kv: (-kv[1], kv[0]))
    palette = [h for h, _n in sorted(col.colors.items(), key=lambda kv: (-kv[1], kv[0]))][:24]
    stats = hue_stats(col.colors)
    return OrderedDict([
        ("schema", SCHEMA),
        ("tool", "originality.py %s" % VERSION),
        ("files", [os.path.basename(p) for p in read]),
        ("skeleton", col.skeleton),
        ("typefaces", families),
        ("fontSizeCount", len(col.sizes)),
        ("palette", palette),
        ("ground", col.ground or "unknown"),
        ("chromaShare", stats["chromaShare"]),
        ("hueHistogram", stats["hueHistogram"]),
        ("hueSpread", stats["hueSpread"]),
        ("dominantHue", stats["dominantHue"]),
        ("gradients", col.gradients),
        ("backdropBlur", col.blur),
        ("decorBlobs", col.blobs),
        ("glowShadows", col.glows),
        ("radii", [r for r, _n in radii]),
        ("dominantRadius", radii[0][0] if radii else None),
        ("shadowCount", col.shadows),
        ("motion", OrderedDict([("transition", col.transition), ("animation", col.animation)])),
        ("copyCliches", cliches),
    ])


# ---------------------------------------------------------------------------
# Compare

def _lcs(a, b):
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            table[i + 1][j + 1] = table[i][j] + 1 if x == y else max(table[i][j + 1], table[i + 1][j])
    return table[-1][-1]


def _multiset_jaccard(a, b):
    ca, cb = Counter(a), Counter(b)
    union = sum((ca | cb).values())
    return sum((ca & cb).values()) / float(union) if union else 1.0


def _seq_sim(a, b):
    if not a and not b:
        return 1.0
    lcs = 2.0 * _lcs(a, b) / (len(a) + len(b))
    return 0.6 * lcs + 0.4 * _multiset_jaccard(a, b)


def generic_run(a, b):
    """Length of the longest ordered run of generic sections that both skeletons share."""
    ga = [x for x in a.get("skeleton") or [] if x in GENERIC_SECTIONS]
    gb = [x for x in b.get("skeleton") or [] if x in GENERIC_SECTIONS]
    return _lcs(ga, gb), ga, gb


def sim_skeleton(a, b):
    sa, sb = a.get("skeleton") or [], b.get("skeleton") or []
    if not sa or not sb:
        return None
    fa = [ARCHETYPE_FAMILY.get(x, x) for x in sa]
    fb = [ARCHETYPE_FAMILY.get(x, x) for x in sb]
    whole = 0.6 * _seq_sim(sa, sb) + 0.4 * _seq_sim(fa, fb)
    run, ga, gb = generic_run(a, b)
    # Share of the shorter generic run found in order in the other; a run shorter than STACK_RUN counts less.
    contained = run / float(min(len(ga), len(gb))) * min(1.0, run / float(STACK_RUN)) if ga and gb else 0.0
    score = max(whole, 0.5 * whole + 0.5 * contained)
    if run >= STACK_RUN:
        score = max(score, min(1.0, 0.75 + 0.08 * (run - STACK_RUN)))
    return score


def type_classes(families):
    names = families or ["(default)"]
    return set(FAMILY_TO_CLASS.get(f, "own:" + f) for f in names)


def sim_type(a, b):
    fa = set(a.get("typefaces") or ["(default)"])
    fb = set(b.get("typefaces") or ["(default)"])
    exact = len(fa & fb) / float(len(fa | fb))
    ca, cb = type_classes(fa), type_classes(fb)
    klass = len(ca & cb) / float(len(ca | cb))
    return max(exact, 0.7 * klass)


def sim_palette(a, b):
    ha, hb = a.get("hueHistogram") or [0] * 12, b.get("hueHistogram") or [0] * 12
    ca, cb = a.get("chromaShare") or 0.0, b.get("chromaShare") or 0.0
    if not any(ha) and not any(hb):
        hue = 1.0
    elif not any(ha) or not any(hb):
        hue = 0.0
    else:
        hue = sum(min(x, y) for x, y in zip(ha, hb))
    neutral = 1.0 - abs(ca - cb)
    ga, gb = a.get("ground", "unknown"), b.get("ground", "unknown")
    ground = 1.0 if ga == gb else (0.5 if "unknown" in (ga, gb) else 0.0)
    return 0.55 * hue + 0.2 * neutral + 0.25 * ground


def sim_hue_spread(a, b):
    sa, sb = a.get("hueSpread"), b.get("hueSpread")
    if sa is None and sb is None:
        return 1.0
    if sa is None or sb is None:
        return 0.0
    return 1.0 - min(abs(sa - sb), 180.0) / 180.0


def _presence(x, y):
    if not x and not y:
        return 1.0
    if not x or not y:
        return 0.0
    return 0.6 + 0.4 * min(x, y) / float(max(x, y))


def sim_gradient(a, b):
    return _presence(a.get("gradients", 0), b.get("gradients", 0))


def sim_effects(a, b):
    keys = ("backdropBlur", "decorBlobs", "glowShadows")
    return sum(_presence(a.get(k, 0), b.get(k, 0)) for k in keys) / len(keys)


def radius_bucket(value):
    if value is None:
        return "none"
    if value <= 0:
        return "square"
    if value <= 6:
        return "small"
    if value <= 12:
        return "medium"
    if value < 999:
        return "large"
    return "pill"


BUCKET_ORDER = ["square", "small", "medium", "large", "pill"]


def sim_radius(a, b):
    da, db = radius_bucket(a.get("dominantRadius")), radius_bucket(b.get("dominantRadius"))
    if da == db:
        dominant = 1.0
    elif "none" in (da, db):
        dominant = 0.5 if "square" in (da, db) else 0.0
    else:
        distance = abs(BUCKET_ORDER.index(da) - BUCKET_ORDER.index(db))
        dominant = 0.5 if distance == 1 else 0.0
    ba = set(radius_bucket(r) for r in a.get("radii") or []) or {"none"}
    bb = set(radius_bucket(r) for r in b.get("radii") or []) or {"none"}
    return 0.5 * dominant + 0.5 * len(ba & bb) / float(len(ba | bb))


def shadow_bucket(count):
    return 0 if not count else (1 if count <= 3 else 2)


def sim_shadow(a, b):
    return 1.0 - abs(shadow_bucket(a.get("shadowCount", 0)) - shadow_bucket(b.get("shadowCount", 0))) / 2.0


def sim_motion(a, b):
    ma, mb = a.get("motion") or {}, b.get("motion") or {}
    keys = ("transition", "animation")
    return sum(1.0 for k in keys if bool(ma.get(k)) == bool(mb.get(k))) / len(keys)


def sim_font_sizes(a, b):
    x, y = a.get("fontSizeCount", 0), b.get("fontSizeCount", 0)
    return 1.0 - abs(x - y) / float(max(x, y, 1))


def sim_copy(a, b):
    ca, cb = set(a.get("copyCliches") or []), set(b.get("copyCliches") or [])
    if not ca and not cb:
        return None
    if not ca or not cb:
        return 0.0
    overlap = len(ca & cb) / float(min(len(ca), len(cb)))
    return max(overlap, 0.5)


def violet_gradient(fp):
    bins = fp.get("hueHistogram") or []
    share = sum(bins[i] for i in VIOLET_BINS if i < len(bins))
    return fp.get("gradients", 0) >= 1 and share >= STACK_VIOLET_SHARE


def stacking(a, b):
    """Return the stacking rules both fingerprints meet. Each one makes the pair derivative."""
    run, _ga, _gb = generic_run(a, b)
    rules = []
    if run < STACK_RUN:
        return run, rules
    if len(a.get("copyCliches") or []) >= STACK_CLICHES and len(b.get("copyCliches") or []) >= STACK_CLICHES:
        rules.append("STACK_SKELETON_COPY")
    if violet_gradient(a) and violet_gradient(b):
        rules.append("STACK_SKELETON_GRADIENT")
    return run, rules


SIMILARITY = OrderedDict([
    ("skeleton", sim_skeleton), ("palette", sim_palette), ("type", sim_type),
    ("gradient", sim_gradient), ("effects", sim_effects), ("radius", sim_radius),
    ("copy", sim_copy), ("shadow", sim_shadow), ("motion", sim_motion),
    ("fontSizes", sim_font_sizes), ("hueSpread", sim_hue_spread),
])


def compare(a, b):
    dims = OrderedDict()
    total, weight_sum = 0.0, 0.0
    for name, func in SIMILARITY.items():
        value = func(a, b)
        if value is None:
            dims[name] = None
            continue
        value = round(_clamp(value), 4)
        dims[name] = value
        total += WEIGHTS[name] * value
        weight_sum += WEIGHTS[name]
    score = round(total / weight_sum, 4) if weight_sum else 0.0
    drivers = sorted((n for n, v in dims.items() if v is not None and v >= 0.6),
                     key=lambda n: (-WEIGHTS[n] * dims[n], n))[:3]
    run, rules = stacking(a, b)
    return OrderedDict([("similarity", score), ("dimensions", dims), ("drivers", drivers),
                        ("genericRun", run), ("stacking", rules)])


# ---------------------------------------------------------------------------
# Library and references

def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_library(path):
    doc = load_json(path)
    entries = []
    for item in doc.get("archetypes", []):
        entries.append({"id": item["id"], "name": item.get("name", item["id"]), "source": "library",
                        "fingerprint": item["fingerprint"]})
    return doc, entries


def load_reference(path):
    """Return a list of {id, name, source, fingerprint} from a file or a folder."""
    out = []
    if os.path.isdir(path):
        json_files = []
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            json_files.extend(os.path.join(dirpath, f) for f in sorted(filenames) if f.endswith(".json"))
        if json_files:
            for item in json_files:
                out.extend(load_reference(item))
            return out
        fp, _skipped = fingerprint([path])
        if fp["files"]:
            out.append({"id": os.path.basename(os.path.normpath(path)), "name": path, "source": path,
                        "fingerprint": fp})
        return out
    if path.lower().endswith(".json"):
        doc = load_json(path)
        if isinstance(doc, dict) and "archetypes" in doc:
            for item in doc["archetypes"]:
                out.append({"id": item["id"], "name": item.get("name", item["id"]), "source": path,
                            "fingerprint": item["fingerprint"]})
        elif isinstance(doc, dict) and "skeleton" in doc:
            label = os.path.splitext(os.path.basename(path))[0]
            out.append({"id": label, "name": label, "source": path, "fingerprint": doc})
        return out
    fp, _skipped = fingerprint([path])
    if fp["files"]:
        label = os.path.splitext(os.path.basename(path))[0]
        out.append({"id": label, "name": path, "source": path, "fingerprint": fp})
    return out


def verdict_for(score, threshold, watch):
    if score >= threshold:
        return "derivative"
    if score >= watch:
        return "watch"
    return "original"


def findings_for(verdict, score, nearest):
    """One finding for a derivative (high) or watch (medium) verdict; none for original."""
    if verdict == "original" or not nearest:
        return []
    dims = nearest["dimensions"]
    drivers = ", ".join("%s %.2f" % (d, dims[d]) for d in nearest["drivers"]) or "no single dimension"
    code, severity = ("ORIG_DERIVATIVE", "high") if verdict == "derivative" else ("ORIG_WATCH", "medium")
    rules = nearest.get("stacking") or []
    stacked = (" Stacking rule %s: a shared run of %d generic sections." % (", ".join(rules), nearest["genericRun"])
               if rules else "")
    message = ("Similarity %.2f to %s (%s). Driven by %s.%s Run the originality-gate human tests "
               "and rebuild the driving parts from the subject." % (score, nearest["id"], nearest["source"],
                                                                    drivers, stacked))
    return [OrderedDict([("code", code), ("severity", severity), ("line", None), ("message", message)])]


def verdict_line(verdict, score, nearest):
    return "Originality: %s (score %.2f, nearest %s)" % (verdict, score, nearest)


# ---------------------------------------------------------------------------
# CLI

def cmd_fingerprint(args):
    fp, skipped = fingerprint(args.paths)
    if not fp["files"]:
        print("originality.py: no file read. Pass HTML, CSS, JSX, TSX or SVG paths.", file=sys.stderr)
        for path, reason in skipped:
            print("  skipped %s: %s" % (path, reason), file=sys.stderr)
        return 2
    payload = json.dumps(fp, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload + "\n")
    if args.json:
        print(payload)
    else:
        print("fingerprint: %d file(s)%s" % (len(fp["files"]), ", wrote " + args.output if args.output else ""))
        print("skeleton: %s" % (" > ".join(fp["skeleton"]) or "(none)"))
        print("typefaces: %s" % (", ".join(fp["typefaces"]) or "(none declared)"))
        print("font sizes: %d; palette: %d colors, ground %s, hue spread %s"
              % (fp["fontSizeCount"], len(fp["palette"]), fp["ground"], fp["hueSpread"]))
        print("gradients %d; backdrop blur %d; blobs %d; glow %d; shadows %d; radius %s"
              % (fp["gradients"], fp["backdropBlur"], fp["decorBlobs"], fp["glowShadows"],
                 fp["shadowCount"], fp["dominantRadius"]))
        print("motion: transition %s, animation %s" % (fp["motion"]["transition"], fp["motion"]["animation"]))
        print("copy cliches: %s" % (", ".join(fp["copyCliches"]) or "none"))
        for path, reason in skipped:
            print("skipped %s: %s" % (path, reason))
        print(NOTE)
    return 0


def _single(path):
    refs = load_reference(path)
    if not refs:
        raise ValueError("no fingerprint in %s" % path)
    return refs[0]


def cmd_compare(args):
    try:
        a, b = _single(args.a), _single(args.b)
    except (OSError, ValueError) as error:
        print("originality.py: %s" % error, file=sys.stderr)
        return 2
    result = compare(a["fingerprint"], b["fingerprint"])
    if args.json:
        out = OrderedDict([("a", a["id"]), ("b", b["id"])])
        out.update(result)
        print(json.dumps(out, indent=2))
    else:
        print("compare %s and %s: similarity %.2f" % (a["id"], b["id"], result["similarity"]))
        for name, value in result["dimensions"].items():
            print("  %-10s %s" % (name, "n/a" if value is None else "%.2f" % value))
        print("drivers: %s" % (", ".join(result["drivers"]) or "none"))
    return 0


def cmd_check(args):
    fp, skipped = fingerprint(args.paths)
    if not fp["files"]:
        print("originality.py: no file read. Pass HTML, CSS, JSX, TSX or SVG paths.", file=sys.stderr)
        for path, reason in skipped:
            print("  skipped %s: %s" % (path, reason), file=sys.stderr)
        return 2
    try:
        library_doc, references = load_library(args.library)
        for path in args.against or []:
            found = load_reference(path)
            if not found:
                print("originality.py: no fingerprint in %s" % path, file=sys.stderr)
                return 2
            references.extend(found)
    except (OSError, ValueError, KeyError) as error:
        print("originality.py: %s" % error, file=sys.stderr)
        return 2
    matches = []
    for ref in references:
        result = compare(fp, ref["fingerprint"])
        matches.append(OrderedDict([("id", ref["id"]), ("name", ref["name"]), ("source", ref["source"]),
                                    ("similarity", result["similarity"]),
                                    ("dimensions", result["dimensions"]), ("drivers", result["drivers"]),
                                    ("genericRun", result["genericRun"]), ("stacking", result["stacking"])]))
    matches.sort(key=lambda m: (-m["similarity"], m["id"]))
    nearest = matches[0] if matches else None
    score = nearest["similarity"] if nearest else 0.0
    verdict = verdict_for(score, args.threshold, args.watch)
    if verdict != "derivative":
        stacked = [m for m in matches if m["stacking"]]
        if stacked:
            nearest = stacked[0]
            score = nearest["similarity"]
            verdict = "derivative"
    line = verdict_line(verdict, score, nearest["id"] if nearest else "none")
    findings = findings_for(verdict, score, nearest)
    if args.json:
        print(json.dumps(OrderedDict([
            ("verdict", verdict), ("score", score), ("nearest", nearest), ("findings", findings),
            ("threshold", args.threshold), ("watch", args.watch), ("line", line),
            ("library", OrderedDict([("version", library_doc.get("version")),
                                     ("archetypes", len(library_doc.get("archetypes", [])))])),
            ("matches", [OrderedDict([("id", m["id"]), ("source", m["source"]),
                                      ("similarity", m["similarity"])]) for m in matches]),
            ("fingerprint", fp), ("skipped", [{"path": p, "reason": r} for p, r in skipped]),
            ("note", NOTE)]), indent=2))
    else:
        print("originality check: %d file(s); library %s (%d archetypes); %d other fingerprint(s)"
              % (len(fp["files"]), library_doc.get("version"), len(library_doc.get("archetypes", [])),
                 len(references) - len(library_doc.get("archetypes", []))))
        print("skeleton: %s" % (" > ".join(fp["skeleton"]) or "(none)"))
        if nearest:
            print("nearest: %s, %s (%s), similarity %.2f" % (nearest["id"], nearest["name"],
                                                            nearest["source"], score))
            dims = nearest["dimensions"]
            print("drivers: %s" % (", ".join("%s %.2f" % (d, dims[d]) for d in nearest["drivers"]) or "none"))
            print("generic run: %d; stacking: %s" % (nearest["genericRun"], ", ".join(nearest["stacking"]) or "none"))
            print("next: %s" % ", ".join("%s %.2f" % (m["id"], m["similarity"]) for m in matches[1:4]))
        for path, reason in skipped:
            print("skipped %s: %s" % (path, reason))
        print(line)
        print(NOTE)
    return 1 if verdict == "derivative" else 0


def cmd_list(args):
    try:
        doc, entries = load_library(args.library)
    except (OSError, ValueError, KeyError) as error:
        print("originality.py: %s" % error, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"version": doc.get("version"), "archetypes": [
            {"id": item["id"], "name": item.get("name"), "description": item.get("description")}
            for item in doc.get("archetypes", [])]}, indent=2))
    else:
        print("generic library %s" % doc.get("version"))
        for item in doc.get("archetypes", []):
            print("%-30s %s" % (item["id"], item.get("name", "")))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="originality.py", description=__doc__.split("\n")[0])
    parser.add_argument("--version", action="version", version="originality.py " + VERSION)
    sub = parser.add_subparsers(dest="command")
    fp = sub.add_parser("fingerprint", help="write the fingerprint of a design")
    fp.add_argument("paths", nargs="+")
    fp.add_argument("-o", "--output", help="path of the fingerprint JSON file to write")
    fp.add_argument("--json", action="store_true", help="print the fingerprint JSON on stdout")
    cp = sub.add_parser("compare", help="compare two fingerprints or designs")
    cp.add_argument("a")
    cp.add_argument("b")
    cp.add_argument("--json", action="store_true", help="print one JSON object on stdout")
    ck = sub.add_parser("check", help="compare a design with the generic library and other fingerprints")
    ck.add_argument("paths", nargs="+")
    ck.add_argument("--against", action="append", help="fingerprint file, library file, design file or folder")
    ck.add_argument("--library", default=DEFAULT_LIBRARY, help="generic library file")
    ck.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="similarity at or above which the verdict is derivative (default 0.75)")
    ck.add_argument("--watch", type=float, default=DEFAULT_WATCH,
                    help="similarity at or above which the verdict is watch (default 0.60)")
    ck.add_argument("--json", action="store_true", help="print one JSON object on stdout")
    ls = sub.add_parser("list", help="list the generic archetypes")
    ls.add_argument("--library", default=DEFAULT_LIBRARY)
    ls.add_argument("--json", action="store_true")
    return parser


def main(argv=None):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exit_:
        return 0 if exit_.code == 0 else 2
    if not args.command:
        parser.print_usage(sys.stderr)
        return 2
    if args.command == "check" and not 0.0 < args.watch <= args.threshold <= 1.0:
        print("originality.py: need 0 < --watch <= --threshold <= 1", file=sys.stderr)
        return 2
    handler = {"fingerprint": cmd_fingerprint, "compare": cmd_compare,
               "check": cmd_check, "list": cmd_list}[args.command]
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
