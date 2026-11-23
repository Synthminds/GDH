#!/usr/bin/env python3
"""tells.py: heuristic scan for generic AI-output tells.

A tell is a visual habit that marks work as generic AI output. This script
reads HTML, CSS, JSX, TSX and Tailwind class strings and reports each tell
with a code, a severity and a fix hint.

  tells.py <path>... [--tokens tokens.json] [--design DESIGN.md]
           [--allow CODE] [--max-font-sizes N] [--max-colors N]
           [--fail-on high|medium|low] [--json]
  tells.py --list

Precedence: a pattern that the design system prescribes is reported as
"brand-required". It is never a finding and it never changes the exit code.
Content tells (placeholder text, unsourced figures) are never brand-required.

The scan is a heuristic. It reads source text and does not render a page.
A clean scan does not prove distinctive work.

Python 3.9+, standard library only. No network calls. No file writes.
Exit code 0 on pass, 1 on findings, 2 on a usage error or an incomplete scan (no file read, or a
file skipped as too large or unreadable).
"""

import argparse
import colorsys
import json
import math
import os
import re
import sys
from collections import Counter, OrderedDict

VERSION = "0.1.0"
LIST_VERSION = "2026-11-23"
NOTE = ("This scan is a heuristic. It reads source text and does not render the page. "
        "A clean scan does not prove distinctive work.")

SEVERITIES = ("high", "medium", "low")
RANK = {"high": 3, "medium": 2, "low": 1}

# code: (severity, what it is, fix hint)
RULES = OrderedDict([
    ("TELL_PURPLE_GRADIENT", ("high", "A purple or indigo to blue gradient.",
     "Derive the palette from the subject. Use one flat brand color, or a gradient whose stops are design tokens.")),
    ("TELL_GRADIENT_TEXT", ("high", "Gradient-filled text.",
     "Set the text in one solid token color. Carry emphasis with size, weight or position.")),
    ("TELL_GLASS_EVERYWHERE", ("medium", "Backdrop blur on many surfaces.",
     "Keep blur for one layer that must separate from moving content. Give the other surfaces a solid token color.")),
    ("TELL_GLOW_SHADOW", ("medium", "A colored glow shadow with no offset.",
     "Use an elevation token with an offset and a blur, or remove the shadow.")),
    ("TELL_EMOJI_ICON", ("medium", "An emoji used as an icon.",
     "Use one icon set with one stroke weight, or an authored SVG. Record the icon source in the asset manifest.")),
    ("TELL_LEFT_BORDER_CARD", ("medium", "A one-sided accent bar on a rounded box.",
     "Mark the state with an icon and a label, a full border or a tinted ground. Remove the side bar.")),
    ("TELL_HERO_THREE_CARDS", ("medium", "A centered hero followed by three equal columns.",
     "Rebuild the structure from the content. Open with the most characteristic thing in the subject. "
     "Give unequal content unequal space.")),
    ("TELL_EYEBROW_EVERY_HEADING", ("medium", "A small label above most headings.",
     "Delete each label that carries no information. Keep a label only where it names a real category.")),
    ("TELL_UNIFORM_RADIUS", ("low", "One large corner radius on almost every element.",
     "Set radius tokens by role: control, card, sheet. Make a nested radius smaller than its parent.")),
    ("TELL_DEFAULT_FONT_ONLY", ("medium", "A default family is the only typeface.",
     "Choose a text face for this subject and test it with real copy. Load it and record its license. "
     "Then run the typography skill.")),
    ("TELL_GRADIENT_STAT_ROW", ("medium", "A row of big gradient numbers with small labels.",
     "Show a figure only when it has a source and helps a decision. Set it in a solid token color with its context.")),
    ("TELL_STAT_ROW", ("low", "A row of big numbers with small labels.",
     "Keep the row only when each figure has a source and a comparison. Otherwise replace it with real content.")),
    ("TELL_FONT_SIZE_SPRAWL", ("low", "Many distinct font sizes that are not tokens.",
     "Map each size to a step of the type scale. Remove the sizes that have no role.")),
    ("TELL_COLOR_SPRAWL", ("low", "Many distinct colors that are not tokens.",
     "Map each color to a semantic token. Remove the colors that have no role.")),
    ("TELL_SECOND_WAVE_FONT", ("low", "A second-wave face with only default faces beside it.",
     "Find the reason for this face in the brief. With no reason, choose a face for this subject "
     "and run the typography skill.")),
    ("TELL_SECOND_WAVE_PALETTE", ("medium", "A second-wave template palette with a stock face.",
     "Take the ground and the accent from the subject's world. Decide light or dark from the use scene.")),
    ("TELL_ACCENT_WORD", ("low", "One headline word set apart by italic, a second face or a second color.",
     "Let the whole headline carry the weight. Drop the styled word.")),
    ("TELL_FAKE_SEQUENCE", ("low", "Numbered markers 01, 02, 03 outside an ordered list.",
     "Number only real steps, in an ordered list. Remove the markers from items that have no order.")),
    ("TELL_ARROW_EVERY_LINK", ("low", "An arrow on every link or button.",
     "Keep an arrow only where direction is the message. Let the link text name the action.")),
    ("TELL_REVEAL_EVERY_SECTION", ("medium", "A fade and slide-up reveal on every section.",
     "Remove the reveal. Keep one authored motion that answers user input or explains a change.")),
    ("TELL_MONO_LABELS", ("low", "Monospace small uppercase labels with no code in view.",
     "Set labels in the text face. Keep monospace for code, data and measurement.")),
    ("TELL_MIDDOT_META", ("low", "Meta strings joined with middle dots.",
     "Write the meta line as a short sentence, or drop the parts that carry no information.")),
    ("TELL_LOREM", ("high", "Placeholder Latin text.",
     "Use real copy from the brief. Mark a missing fact with a bracketed label such as [PRICE].")),
    ("TELL_PLACEHOLDER_COPY", ("medium", "Generic placeholder copy or an invented name.",
     "Write copy that is specific to this product. Ask the user for a missing name or fact.")),
    ("TELL_INVENTED_STAT", ("high", "A specific figure with no source in view.",
     "Confirm the figure and its source with the user. Otherwise replace it with a labelled placeholder.")),
])

# Tells about invented content are a kernel gate. No design system can require them.
NEVER_BRAND_REQUIRED = {"TELL_LOREM", "TELL_PLACEHOLDER_COPY", "TELL_INVENTED_STAT",
                        "TELL_FONT_SIZE_SPRAWL", "TELL_COLOR_SPRAWL"}

MARKUP_EXT = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".mdx", ".js", ".ts"}
CSS_EXT = {".css", ".scss", ".less", ".pcss"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", ".nuxt", ".svelte-kit", "__pycache__",
             ".venv", "coverage", "out", ".turbo", ".cache"}
MAX_BYTES = 2000000

DEFAULT_MAX_FONT_SIZES = 8
DEFAULT_MAX_COLORS = 12
GLASS_THRESHOLD = 3
RADIUS_MIN_USES = 6
RADIUS_SHARE = 0.8
RADIUS_LARGE_PX = 12.0
EYEBROW_MIN = 2
EYEBROW_SHARE = 0.5
STAT_MIN = 3

DEFAULT_FAMILIES = {
    "inter", "roboto", "arial", "helvetica", "helvetica neue", "open sans", "system-ui", "-apple-system",
    "blinkmacsystemfont", "segoe ui", "sans-serif", "ui-sans-serif",
}
# The faces agents reach for once they are told to avoid Inter. Keep this set equal to the list in
# references/tells.md section 3 and refresh both together.
SECOND_WAVE_DATE = "2026-11-23"
SECOND_WAVE_FAMILIES = {
    "geist", "space grotesk", "dm sans", "poppins", "manrope", "plus jakarta sans", "instrument serif",
    "fraunces", "playfair display",
}
# Second-wave template palettes. OKLCH bands, dated with SECOND_WAVE_DATE. Default: the bands are a rule
# of thumb. The mood-board script holds the same looks in KNOWN_DEFAULTS; tests keep the two in step.
# id: (ground side, ground test, accent hue bands in OKLCH degrees, name)
SECOND_WAVE_LOOKS = OrderedDict([
    ("warm-editorial", ("light", "cream", ((20.0, 60.0),), "cream ground with a terracotta or orange accent")),
    ("night-signal", ("dark", "near-black", ((15.0, 45.0), (110.0, 150.0)),
                      "near-black ground with one vermilion, orange or acid-green accent")),
])
ACCENT_MIN_CHROMA = 0.08
ARROW_CHARS = u"\u2192\u2197\u279c\u27f6\u2794\u2b95\u21aa\u203a\u00bb"
ARROW_CSS_RE = re.compile(r"\\0*(?:2192|2197|279c|27f6|2794|2b95|21aa|203a|00bb|bb)\b|->|" +
                          "[" + ARROW_CHARS + "]", re.I)
ARROW_TEXT_RE = re.compile(r"&rarr;|&#8594;|&#x2192;|&rsaquo;|&raquo;|->|[" + ARROW_CHARS + "]", re.I)
ARROW_MIN = 3
REVEAL_MIN = 3
MONO_MIN = 2
MIDDOT_RE = re.compile(u"\\s(?:\u00b7|&middot;|&#183;|&#xb7;)\\s", re.I)
MIDDOT_MIN = 2
SEQUENCE_MIN = 3
DATA_URI_RE = re.compile(r"data:[\w.+/-]+(?:;[\w.+/=-]+)*,[A-Za-z0-9+/=%._~-]{64,}")
GENERIC_FAMILIES = {"sans-serif", "serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif",
                    "ui-serif", "ui-monospace", "ui-rounded", "inherit", "initial", "unset", "revert"}
MONO_HINTS = ("mono", "courier", "consolas", "menlo", "sfmono", "sf mono", "code")

NAMED_COLORS = {
    "purple": (128, 0, 128), "indigo": (75, 0, 130), "violet": (238, 130, 238), "blueviolet": (138, 43, 226),
    "mediumpurple": (147, 112, 219), "rebeccapurple": (102, 51, 153), "darkviolet": (148, 0, 211),
    "slateblue": (106, 90, 205), "mediumslateblue": (123, 104, 238), "blue": (0, 0, 255),
    "royalblue": (65, 105, 225), "dodgerblue": (30, 144, 255), "deepskyblue": (0, 191, 255),
    "magenta": (255, 0, 255), "fuchsia": (255, 0, 255), "hotpink": (255, 105, 180), "deeppink": (255, 20, 147),
    "pink": (255, 192, 203), "cyan": (0, 255, 255), "aqua": (0, 255, 255), "teal": (0, 128, 128),
    "red": (255, 0, 0), "orange": (255, 165, 0), "yellow": (255, 255, 0), "green": (0, 128, 0),
    "lime": (0, 255, 0), "navy": (0, 0, 128), "white": (255, 255, 255), "black": (0, 0, 0),
    "gray": (128, 128, 128), "grey": (128, 128, 128), "silver": (192, 192, 192),
}

TW_PURPLE = {"indigo", "violet", "purple"}
TW_NEAR_PURPLE = {"blue", "sky", "cyan", "indigo", "violet", "purple", "fuchsia", "pink"}
TW_NEUTRAL = {"black", "white", "gray", "slate", "zinc", "neutral", "stone", "transparent", "current", "inherit"}
TW_FAMILIES = {"slate", "gray", "zinc", "neutral", "stone", "red", "orange", "amber", "yellow", "lime", "green",
               "emerald", "teal", "cyan", "sky", "blue", "indigo", "violet", "purple", "fuchsia", "pink", "rose",
               "black", "white"}
TW_BLUR_PX = {"xs": 4.0, "sm": 4.0, "": 8.0, "md": 12.0, "lg": 16.0, "xl": 24.0, "2xl": 40.0, "3xl": 64.0}
TW_RADIUS_PX = {"none": 0.0, "xs": 2.0, "sm": 2.0, "": 4.0, "md": 6.0, "lg": 8.0, "xl": 12.0, "2xl": 16.0,
                "3xl": 24.0, "4xl": 32.0}

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")
FUNC_COLOR_RE = re.compile(r"\b(rgba?|hsla?|oklch)\(\s*([^()]*)\)", re.I)
COLOR_TOKEN_RE = re.compile(
    r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-fA-F])"
    r"|\b(?:rgba?|hsla?|oklch)\([^()]*\)"
    r"|var\(\s*--[\w-]+"
    r"|\b[a-zA-Z]{3,20}\b", re.I)
GRADIENT_RE = re.compile(r"(?:repeating-)?(?:linear|radial|conic)-gradient\(", re.I)
LENGTH_RE = re.compile(r"(?<![\w.#-])(-?\d*\.?\d+)(px|rem|em|pt)?(?![\w.%])")
CLASS_ATTR_RE = re.compile(
    r"""\b(?:class|className)\s*=\s*(?:"([^"]*)"|'([^']*)'|\{\s*`([^`]*)`\s*\}|\{\s*"([^"]*)"\s*\}|\{\s*'([^']*)'\s*\})""")
CLASS_FN_RE = re.compile(r"\b(?:cn|clsx|classnames|classNames|twMerge|twJoin|cva|tw)\s*\(")
STRING_RE = re.compile(r"""("([^"\\\n]*)"|'([^'\\\n]*)'|`([^`\\]*)`)""")
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style\s*>", re.I | re.S)
STYLE_ATTR_RE = re.compile(r"""\bstyle\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
JSX_STYLE_RE = re.compile(
    r"""\b(backdropFilter|WebkitBackdropFilter|borderRadius|fontSize|boxShadow|textShadow|fontFamily|borderLeft"""
    r"""|background|backgroundImage)\s*:\s*(?:(-?\d+(?:\.\d+)?)|"([^"\n]*)"|'([^'\n]*)'|`([^`\n]*)`)""")
ELEMENT_TEXT_RE = re.compile(r"<([A-Za-z][\w.-]*)\b([^<>]*)>([^<>]{1,90})</\1\s*>")
HEADING_RE = re.compile(r"<h([12])\b", re.I)
EYEBROW_NAME_RE = re.compile(r"(?:^|[\s_-])(eyebrow|kicker|overline|pretitle|pre-title|section-label|label-caps)"
                             r"(?:$|[\s_-])", re.I)
EYEBROW_COMPONENT_RE = re.compile(r"<(Eyebrow|Kicker|Overline)\b[^<>]*>[^<>]{0,90}</\1\s*>\s*<(?:h[1-4]|Heading|Title)\b")
STAT_TEXT_RE = re.compile(r"^[$\u20ac\u00a3]?\d[\d.,]*\s?(?:%|\+|x|X|k|K|M|B|bn|ms|s|h|/7|/5)?\+?$")
STAT_NAME_RE = re.compile(r"(?:^|[\s_-])(stat|stats|metric|kpi|number|figure|counter)(?:$|[\s_-])", re.I)

LOREM_RE = re.compile(r"lorem\s+ipsum|dolor\s+sit\s+amet|consectetur\s+adipisc", re.I)
PLACEHOLDER_RES = [
    re.compile(r"\b(?:your|my)\s+(?:headline|title|text|tagline|subtitle|company|brand|logo|name|content)\s+"
               r"(?:goes\s+)?here\b", re.I),
    re.compile(r">\s*(?:Feature|Benefit|Service|Card|Item)\s+(?:One|Two|Three|[1-9])\s*<"),
    re.compile(r">\s*(?:Card title|Section title|Title goes here|Description goes here|Placeholder text|"
               r"Heading goes here|Subheading goes here)\s*<", re.I),
    re.compile(r"\b(?:John|Jane)\s+(?:Doe|Smith)\b"),
    re.compile(r"\b(?:Acme|Example)\s+(?:Inc|Corp|Corporation|Co|Ltd|LLC)\b\.?"),
]
STAT_RES = [
    re.compile(r"\b\d[\d,.]*\s?[kKmMbB]?\+\s+(?:\w+\s+)?(?:users|customers|companies|teams|developers|clients|"
               r"downloads|businesses|brands|countries|reviews|stars|members|creators|students|projects)\b", re.I),
    re.compile(r"\b(?:trusted|loved|used|chosen|relied\s+on)\s+by\s+(?:over\s+|more\s+than\s+)?\d", re.I),
    re.compile(r"\b\d{1,3}(?:\.\d+)?\s?%\s+(?:[a-z]+\s+)?(?:uptime|faster|more|less|fewer|increase|growth|"
               r"satisfaction|reduction|boost|cheaper|higher|lower|retention|accuracy|conversion|savings|"
               r"of\s+(?:users|customers|teams|people))\b", re.I),
    re.compile(r"\b\d+(?:\.\d+)?x\s+(?:faster|more|cheaper|better|productivity|roi|return)\b", re.I),
    re.compile(r"\b[45]\.\d\s*(?:/|out\s+of)\s*5\b"),
    re.compile(r"[$\u20ac\u00a3]\s?\d[\d,.]*\s?[kKmMbB]?\+?\s+(?:saved|in\s+revenue|raised|processed|in\s+savings)\b", re.I),
]
SOURCE_HINT_RE = re.compile(
    r"data-source\s*=|<cite\b|\bsource\s*:|\[[A-Z][A-Z0-9 _-]{2,}\]|\baccording\s+to\b"
    r"|\b(?:in|from|per)\s+(?:the|our|a|an)\s+(?:[\w-]+\s+){0,3}(?:survey|report|study|census|audit|filing|"
    r"dataset|poll|benchmark)\b", re.I)
SOURCE_HINT_LOOKAHEAD = 400
STAT_VALUE_KEYS = r"(?:value|stat|number|figure|metric|count|amount|kpi)"
STAT_LABEL_KEYS = r"(?:label|title|caption|description|desc|text|name|unit|suffix)"
JS_OBJECT_RE = re.compile(r"\{[^{}]{4,400}\}")

NEGATION_RE = re.compile(
    r"\b(?:no|not|never|avoid|avoids|avoided|don't|dont|do\s+not|does\s+not|without|ban|bans|banned|forbid|"
    r"forbids|forbidden|prohibit|prohibits|prohibited|instead\s+of|rather\s+than|except|remove|removed|none|"
    r"nothing|zero|nor|neither)\b", re.I)
PROHIBIT_HEADING_RE = re.compile(r"\b(?:do\s+not|don't|don'ts|donts|avoid|never|anti|not\s+allowed|misuse|"
                                 r"forbidden|prohibited|banned)\b", re.I)

DESIGN_KEYWORDS = {
    "TELL_PURPLE_GRADIENT": [r"gradient"],
    "TELL_GRADIENT_TEXT": [r"gradient[- ](?:text|headline|headlines|heading|headings|title|titles|wordmark|type)",
                           r"text[- ]gradient",
                           r"(?:headline|heading|title)s?\s+(?:use|uses|in|with|take|takes)\s+(?:the\s+|a\s+)?"
                           r"(?:brand\s+)?gradient"],
    "TELL_GLASS_EVERYWHERE": [r"glass", r"backdrop[- ]blur", r"frosted"],
    "TELL_GLOW_SHADOW": [r"glow"],
    "TELL_EMOJI_ICON": [r"emoji"],
    "TELL_LEFT_BORDER_CARD": [r"left[- ]border", r"border-left", r"accent[- ](?:bar|stripe|rule)",
                              r"side[- ](?:bar|stripe)", r"left[- ](?:rule|stripe|bar|edge)"],
    "TELL_HERO_THREE_CARDS": [r"three[- ](?:card|cards|column|columns|up)", r"3[- ](?:card|cards|column|columns|up)"],
    "TELL_EYEBROW_EVERY_HEADING": [r"eyebrow", r"overline", r"kicker"],
    "TELL_UNIFORM_RADIUS": [r"(?:one|single|uniform|same)\s+(?:corner\s+)?radius"],
    "TELL_GRADIENT_STAT_ROW": [r"stat[- ](?:row|band|strip)", r"metric[- ](?:row|band|strip)", r"big[- ]number"],
    "TELL_STAT_ROW": [r"stat[- ](?:row|band|strip)", r"metric[- ](?:row|band|strip)", r"big[- ]number"],
    "TELL_SECOND_WAVE_PALETTE": [r"\bcream\b", r"terracotta", r"near[- ]black"],
    "TELL_ACCENT_WORD": [r"(?:italic|accent|colou?red)\s+(?:headline\s+)?word", r"accent[- ]word"],
    "TELL_FAKE_SEQUENCE": [r"numbered\s+(?:markers|labels|sections|items)", r"section\s+numbers?"],
    "TELL_ARROW_EVERY_LINK": [r"arrows?\s+on\s+(?:every|each|all)?\s*(?:links?|buttons?|ctas?)",
                              r"(?:links?|buttons?|ctas?)\s+(?:end|ends|carry|carries)\s+(?:with\s+)?(?:an\s+)?arrow"],
    "TELL_REVEAL_EVERY_SECTION": [r"(?:scroll|section)[- ]reveal", r"(?:fade|slide)[- ]?(?:in|up)\s+on\s+scroll",
                                  r"reveal\s+on\s+scroll"],
    "TELL_MONO_LABELS": [r"mono(?:space)?\s+(?:labels?|kickers?|captions?|eyebrows?)",
                         r"labels?\s+(?:are\s+|in\s+|use\s+)(?:a\s+|the\s+)?mono"],
    "TELL_MIDDOT_META": [r"middle[- ]dots?", r"middot", r"interpunct"],
}
# A token NAME alone prescribes only these patterns, which have no single value to compare. Gradient,
# glass and glow need a token VALUE that matches what the page uses: a scrim named "glass-overlay" or a
# focus ring named "shadow-glow-focus" must not hide real glass or glow.
TOKEN_KEYWORDS = {
    "TELL_GRADIENT_TEXT": ["gradient-text", "text-gradient", "gradienttext", "textgradient"],
    "TELL_LEFT_BORDER_CARD": ["accent-bar", "border-left", "left-border"],
    "TELL_EYEBROW_EVERY_HEADING": ["eyebrow", "overline", "kicker"],
    "TELL_GRADIENT_STAT_ROW": ["stat", "metric", "kpi"],
    "TELL_STAT_ROW": ["stat", "metric", "kpi"],
}


# ---------------------------------------------------------------- color

def clamp01(value):
    return max(0.0, min(1.0, value))


def oklch_to_rgb(lightness, chroma, hue):
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    l3, m3, s3 = l_ ** 3, m_ ** 3, s_ ** 3
    lin = (4.0767416621 * l3 - 3.3077115913 * m3 + 0.2309699292 * s3,
           -1.2684380046 * l3 + 2.6097574011 * m3 - 0.3413193965 * s3,
           -0.0041960863 * l3 - 0.7034186147 * m3 + 1.7076147010 * s3)
    out = []
    for c in lin:
        c = clamp01(c)
        out.append(12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055)
    return tuple(clamp01(c) for c in out)


def rgb_to_oklch(rgb):
    """Return (lightness 0-1, chroma, hue in degrees) for an sRGB color with parts from 0 to 1."""
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    l_ = 0.4122214708 * lin[0] + 0.5363325363 * lin[1] + 0.0514459929 * lin[2]
    m_ = 0.2119034982 * lin[0] + 0.6806995451 * lin[1] + 0.1073969566 * lin[2]
    s_ = 0.0883024619 * lin[0] + 0.2817188376 * lin[1] + 0.6299787005 * lin[2]
    l_, m_, s_ = [math.copysign(abs(v) ** (1.0 / 3.0), v) for v in (l_, m_, s_)]
    lightness = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return lightness, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360.0


HUE_UNITS = (("grad", 0.9), ("turn", 360.0), ("rad", 180.0 / math.pi), ("deg", 1.0))


def parse_hue(text):
    """Return a CSS hue in degrees. Accepts deg, grad, rad and turn, or a bare number."""
    text = text.strip().lower()
    for unit, factor in HUE_UNITS:
        if text.endswith(unit):
            return (float(text[:-len(unit)]) * factor) % 360.0
    return float(text) % 360.0


def _number(text, scale=1.0):
    text = text.strip()
    if text.endswith("%"):
        return float(text[:-1]) / 100.0 * scale
    return float(text)


def parse_color(text):
    """Return (r, g, b) with parts from 0 to 1, or None when the text is not a literal color."""
    if not text:
        return None
    text = text.strip()
    low = text.lower()
    if low in NAMED_COLORS:
        return tuple(c / 255.0 for c in NAMED_COLORS[low])
    if low.startswith("#"):
        digits = low[1:]
        if not re.match(r"^[0-9a-f]+$", digits) or len(digits) not in (3, 4, 6, 8):
            return None
        if len(digits) in (3, 4):
            digits = "".join(ch * 2 for ch in digits)
        return tuple(int(digits[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    match = FUNC_COLOR_RE.match(low)
    if not match:
        return None
    name = match.group(1)
    parts = [p for p in re.split(r"[\s,/]+", match.group(2).strip()) if p]
    try:
        if name.startswith("rgb") and len(parts) >= 3:
            return tuple(clamp01(_number(p, 255.0) / 255.0) for p in parts[:3])
        if name.startswith("hsl") and len(parts) >= 3:
            hue = parse_hue(parts[0])
            sat, light = _number(parts[1] if parts[1].endswith("%") else parts[1] + "%"), \
                _number(parts[2] if parts[2].endswith("%") else parts[2] + "%")
            r, g, b = colorsys.hls_to_rgb(hue / 360.0, clamp01(light), clamp01(sat))
            return (r, g, b)
        if name == "oklch" and len(parts) >= 3:
            light = _number(parts[0])
            chroma = _number(parts[1], 0.4)
            hue = parse_hue(parts[2])
            return oklch_to_rgb(light, chroma, hue)
    except ValueError:
        return None
    return None


def to_hex(rgb):
    return "#%02x%02x%02x" % tuple(int(round(clamp01(c) * 255)) for c in rgb)


def hsl_of(rgb):
    hue, light, sat = colorsys.rgb_to_hls(*rgb)
    return hue * 360.0, sat, light


def is_chromatic(rgb, min_sat=0.25):
    _, sat, light = hsl_of(rgb)
    return sat >= min_sat and 0.10 < light < 0.95


def is_purple_run(colors):
    """True when the chromatic stops include indigo, violet or purple and all sit between blue and pink."""
    stops = [hsl_of(c) for c in colors if is_chromatic(c)]
    if not stops:
        return False

    def purple(hue, sat):
        # Pure CSS blue sits at 240 degrees with full saturation. It is blue, not indigo.
        return 232.0 <= hue <= 300.0 and not (abs(hue - 240.0) < 0.5 and sat > 0.98)

    return any(purple(h, s) for h, s, _ in stops) and all(195.0 <= h <= 340.0 for h, _, _ in stops)


# ---------------------------------------------------------------- text helpers

def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def snippet(text, limit=110):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


def balanced(text, open_index):
    """Return the index after the parenthesis that closes text[open_index]."""
    depth = 0
    for index in range(open_index, len(text)):
        ch = text[index]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    return len(text)


def strip_css_comments(text):
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)


def parse_css(text, base_line=1):
    """Return a list of (selector, [(prop, value, line)], line). Nested blocks carry the full selector path."""
    text = strip_css_comments(text)
    rules, stack, buf = [], [], []
    line, buf_line, paren, quote = base_line, base_line, 0, None

    def flush_decl():
        raw = "".join(buf).strip()
        if raw and stack:
            if raw.startswith("@apply"):
                stack[-1][1].append(("@apply", raw[6:].strip(), buf_line))
            elif ":" in raw:
                prop, value = raw.split(":", 1)
                stack[-1][1].append((prop.strip().lower(), value.strip(), buf_line))

    for ch in text:
        if ch == "\n":
            line += 1
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
            continue
        if ch == "(":
            paren += 1
        elif ch == ")":
            paren = max(0, paren - 1)
        if paren == 0 and ch == "{":
            prelude = " ".join("".join(buf).split())
            path = " ".join([s[0] for s in stack] + [prelude]).strip()
            stack.append((path, [], buf_line))
            buf = []
        elif paren == 0 and ch == "}":
            flush_decl()
            buf = []
            if stack:
                rules.append(stack.pop())
        elif paren == 0 and ch == ";":
            flush_decl()
            buf = []
        else:
            if not buf or not "".join(buf).strip():
                if not ch.isspace():
                    buf_line = line
            buf.append(ch)
    return rules


def to_px(number, unit):
    value = float(number)
    if unit in ("rem", "em"):
        return value * 16.0
    if unit == "pt":
        return value * 4.0 / 3.0
    return value


def positive_length(value):
    """True when a letter-spacing or similar value is a length above zero."""
    match = re.match(r"^\s*(-?\d*\.?\d+)", value)
    return bool(match) and float(match.group(1)) > 0.0


def first_length_px(value):
    match = LENGTH_RE.search(value)
    if not match:
        return None
    return to_px(match.group(1), match.group(2) or "px")


def selector_classes(selector):
    return set(re.findall(r"\.([A-Za-z_][\w-]*)", selector))


def markup_counts(text):
    """Count the elements of an HTML file by tag and by class. Style and script blocks are skipped."""
    body = re.sub(r"(?is)<(style|script)\b.*?</\1\s*>", "", text)
    counts = Counter()
    for match in re.finditer(r"<([A-Za-z][A-Za-z0-9-]*)\b([^>]*)>", body):
        counts[("tag", match.group(1).lower())] += 1
        attr = re.search(r"""\bclass(?:Name)?\s*=\s*(?:"([^"]*)"|'([^']*)')""", match.group(2))
        if attr:
            for name in set((attr.group(1) if attr.group(1) is not None else attr.group(2)).split()):
                counts[("class", name.lower())] += 1
    return counts


def split_top(value, sep=","):
    parts, depth, cur = [], 0, []
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def base_class(token):
    """Strip Tailwind variant prefixes such as md: and hover: from one class."""
    depth, last = 0, -1
    for index, ch in enumerate(token):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth = max(0, depth - 1)
        elif ch == ":" and depth == 0:
            last = index
    return token[last + 1:].lstrip("!")


def family_names(stack):
    names = []
    for part in split_top(stack):
        name = part.strip().strip("\"'").strip().lower()
        if name:
            names.append(name)
    return names


def is_mono_stack(names):
    if not names:
        return False
    first = names[0]
    return first in ("monospace", "ui-monospace") or any(hint in first for hint in MONO_HINTS)


# ---------------------------------------------------------------- design system sources

class DesignSources(object):
    """What the design system prescribes. Built from tokens.json and DESIGN.md."""

    def __init__(self):
        self.token_names = []      # (lower name, family, original name)
        self.token_values = []     # (lower value, original name)
        self.colors = {}           # hex -> token name
        self.color_by_name = {}    # lower token name -> hex
        self.sizes_px = set()
        self.families = {}         # lower family -> source text
        self.radius_px = []
        self.vars = {}             # custom property name without dashes -> value
        self.design_lines = []     # (line number, lower sentence, prohibited)
        self.tokens_path = None
        self.design_path = None

    # tokens.json ------------------------------------------------------
    def load_tokens(self, path):
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        self.tokens_path = path
        if isinstance(data, dict):
            for family, node in data.items():
                self._walk(node, str(family), str(family))
            type_node = data.get("type")
            if isinstance(type_node, dict):
                families = type_node.get("families")
                if isinstance(families, dict):
                    for key, stack in families.items():
                        if isinstance(stack, str):
                            for name in family_names(stack):
                                self.families.setdefault(name, "type.families.%s" % key)
                for font in type_node.get("fonts") or []:
                    if isinstance(font, dict) and isinstance(font.get("family"), str):
                        self.families.setdefault(font["family"].strip().lower(), "type.fonts")
        else:
            self._walk(data, "root", "root")

    def _record(self, name, value, family):
        low_name = str(name).lower()
        self.token_names.append((low_name, family, str(name)))
        values = []
        if isinstance(value, str):
            values = [value]
        elif isinstance(value, dict):
            values = [v for v in value.values() if isinstance(v, str)]
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            values = [str(value)]
        for text in values:
            self.token_values.append((text.lower(), str(name)))
            self.vars[low_name] = text
            rgb = parse_color(text)
            if rgb is not None:
                self.colors.setdefault(to_hex(rgb), str(name))
                self.color_by_name.setdefault(low_name, to_hex(rgb))
            for match in HEX_RE.finditer(text):
                inner = parse_color(match.group(0))
                if inner is not None:
                    self.colors.setdefault(to_hex(inner), str(name))
            px = first_length_px(text) if re.match(r"^\s*-?\d*\.?\d+(px|rem|em|pt)?\s*$", text) else None
            if px is not None:
                if family.lower().startswith("radius") or "radius" in low_name:
                    self.radius_px.append(px)
                if family.lower() in ("type", "font-size", "fontsize", "text") or "font-size" in low_name \
                        or "fontsize" in low_name or low_name.startswith("text-"):
                    self.sizes_px.add(round(px, 2))

    def _walk(self, node, family, path):
        if isinstance(node, list):
            for item in node:
                self._walk(item, family, path)
        elif isinstance(node, dict):
            if "name" in node and ("value" in node or "fontSize" in node):
                self._record(node["name"], node.get("value"), family)
                size = node.get("fontSize")
                if isinstance(size, (str, int, float)) and not isinstance(size, bool):
                    px = first_length_px(str(size))
                    if px is not None:
                        self.sizes_px.add(round(px, 2))
            elif "$value" in node:
                self._record(path, node["$value"], family)
            for key, value in node.items():
                if key in ("usage", "description", "$description"):
                    continue
                if isinstance(value, (dict, list)):
                    self._walk(value, family, "%s.%s" % (path, key))
                elif isinstance(value, (str, int, float)) and not isinstance(value, bool) \
                        and "name" not in node and "$value" not in node and key not in ("id", "version"):
                    self._record("%s.%s" % (path, key), value, family)

    # DESIGN.md --------------------------------------------------------
    def load_design(self, path):
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        self.design_path = path
        prohibit_level = None
        fenced = False
        for number, raw in enumerate(text.split("\n"), 1):
            line = raw.strip()
            if line.startswith("```") or line.startswith("~~~"):
                fenced = not fenced
                continue
            if fenced or not line:
                continue
            heading = re.match(r"^(#{1,6})\s+(.*)$", line)
            if heading:
                level = len(heading.group(1))
                if prohibit_level is not None and level <= prohibit_level:
                    prohibit_level = None
                if PROHIBIT_HEADING_RE.search(heading.group(2)):
                    prohibit_level = level
                continue
            body = re.sub(r"^(?:[-*+]|\d+\.)\s+", "", line)
            for sentence in re.split(r"(?<=[.;!?])\s+", body):
                sentence = sentence.strip()
                if sentence:
                    prohibited = prohibit_level is not None or bool(NEGATION_RE.search(sentence))
                    self.design_lines.append((number, sentence.lower(), prohibited))

    def design_mentions(self, patterns):
        """Return 'DESIGN.md line N' for the first sentence that prescribes one of the patterns."""
        compiled = [re.compile(p, re.I) for p in patterns]
        for number, sentence, prohibited in self.design_lines:
            if prohibited:
                continue
            if any(p.search(sentence) for p in compiled):
                return "%s line %d" % (os.path.basename(self.design_path), number)
        return None

    def token_named(self, keywords):
        for low, _family, original in self.token_names:
            joined = re.sub(r"[^a-z0-9]+", "-", low)
            parts = joined.split("-")
            for keyword in keywords:
                if "-" in keyword:
                    hit = keyword in joined
                else:
                    hit = any(part == keyword or part == keyword + "s" or
                              (len(keyword) >= 5 and part.startswith(keyword)) for part in parts)
                if hit:
                    return "%s token \"%s\"" % (os.path.basename(self.tokens_path), original)
        return None

    def token_value_has(self, needle):
        for value, original in self.token_values:
            if needle in value:
                return "%s token \"%s\"" % (os.path.basename(self.tokens_path), original)
        return None

    def _label(self, original):
        return "%s token \"%s\"" % (os.path.basename(self.tokens_path), original)

    def color_of(self, text):
        """Resolve a literal color, a var(--name) or a {token.ref} to a hex, or None."""
        text = text.strip()
        ref = re.match(r"^\{([^{}]+)\}$", text) or re.match(r"^var\(\s*--([\w-]+)", text)
        if ref:
            name = ref.group(1).lower()
            for candidate in (name, name.split(".")[-1], re.sub(r"^(?:color|clr|c)-", "", name)):
                if candidate in self.color_by_name:
                    return self.color_by_name[candidate]
            return None
        rgb = parse_color(text)
        return to_hex(rgb) if rgb is not None else None

    def tailwind_color(self, family_shade):
        """Resolve a Tailwind palette step such as indigo-500 against the token names, or None."""
        key = family_shade.lower()
        for name, hexv in self.color_by_name.items():
            parts = re.split(r"[.\s/]+", name)
            if name == key or parts[-1] == key or name.endswith("-" + key):
                return hexv
        return None

    def gradient_token(self, hexes):
        """Return the source of a gradient token whose stops equal the observed stops, else None."""
        wanted = [h.lower() for h in hexes]
        for value, original in self.token_values:
            for match in GRADIENT_RE.finditer(value):
                end = balanced(value, match.end() - 1)
                stops = []
                for part in split_top(value[match.end():end - 1]):
                    head = re.match(r"^(\{[^{}]+\}|var\([^()]*\)|#[0-9a-f]+|(?:rgba?|hsla?|oklch)\([^()]*\)|[a-z]+)",
                                    part.strip())
                    hexv = self.color_of(head.group(1)) if head else None
                    if hexv:
                        stops.append(hexv)
                if stops and stops == wanted:
                    return self._label(original)
        return None

    def shadow_token(self, layer):
        """Return the source of a shadow token that holds this exact layer, else None."""
        want = re.sub(r"\s+", "", layer.lower())
        for value, original in self.token_values:
            layers = [re.sub(r"\s+", "", part) for part in split_top(value)]
            if want and want in layers:
                return self._label(original)
        return None

    def blur_token(self, px_values):
        """Return the source of a blur token when every observed blur radius equals a token blur radius."""
        token_px = {}
        for value, original in self.token_values:
            for match in re.finditer(r"blur\(\s*(-?\d*\.?\d+)(px|rem|em)?\s*\)", value):
                token_px.setdefault(round(to_px(match.group(1), match.group(2) or "px"), 2), original)
        if not px_values or not token_px:
            return None
        if all(px is not None and round(px, 2) in token_px for px in px_values):
            return self._label(token_px[round(px_values[0], 2)])
        return None

    def resolve_var(self, name):
        name = name.lower().lstrip("-")
        for candidate in (name, re.sub(r"^(?:color|clr|c)-", "", name)):
            if candidate in self.vars:
                return self.vars[candidate]
        return None

    @property
    def loaded(self):
        return bool(self.tokens_path or self.design_path)


# ---------------------------------------------------------------- scan

class Scan(object):
    def __init__(self, sources, max_font_sizes, max_colors, allow):
        self.sources = sources
        self.max_font_sizes = max_font_sizes
        self.max_colors = max_colors
        self.allow = set(allow or [])
        self.raw = []            # candidate findings before the brand-required split
        self.files = 0
        self.glass = []          # (path, line)
        self.radius = []         # (px, path, line)
        self.font_sizes = {}     # px -> (path, line)
        self.colors = {}         # hex -> (path, line)
        self.families = []       # (first name, names, path, line)
        self.font_unknown = False
        self.html_docs = []      # (path, has style signal)
        self.css_vars = {}
        self.facts = {"gradient_text": set(), "eyebrow": set(), "big": set(), "three_col": set(),
                      "center": set(), "center_tags": False, "big_desc": [], "accent_classes": set()}
        self.blur_px = []        # blur radius in px at each glass use, None when unknown
        self.grounds = []        # (hex, path, line) of page grounds
        self.accents = []        # (hex, path, line) of every literal color, custom properties included
        self.invented_lines = set()   # (path, line) already reported as TELL_INVENTED_STAT
        self.counts = Counter()       # per-scan counters for the second-wave rules
        self.first_at = {}            # code -> (path, line, evidence) of the first sighting
        self.markup = None            # element counts by class and tag of the HTML file being scanned

    def add(self, code, path, line, message, evidence="", ctx=None):
        self.raw.append({"code": code, "path": path, "line": line, "message": message,
                         "evidence": snippet(evidence), "ctx": ctx or {}})

    # ---- CSS ----------------------------------------------------------
    def css_pass(self, path, css, base_line):
        for selector, decls, rule_line in parse_css(css, base_line):
            self.handle_rule(path, selector, decls, rule_line)

    def handle_rule(self, path, selector, decls, rule_line):
        props = {}
        for prop, value, line in decls:
            props[prop] = (value, line)
        classes = selector_classes(selector)
        low_sel = selector.lower()
        is_font_face = low_sel.strip().startswith("@font-face")

        clip = props.get("background-clip") or props.get("-webkit-background-clip")
        if clip and re.search(r"\btext\b", clip[0]):
            self.facts["gradient_text"] |= classes
            self.add("TELL_GRADIENT_TEXT", path, clip[1],
                     "Text is filled with a background through background-clip.", "%s { background-clip: %s }"
                     % (selector, clip[0]))
        uppercase = "text-transform" in props and "uppercase" in props["text-transform"][0].lower()
        if uppercase and "letter-spacing" in props and positive_length(props["letter-spacing"][0]):
            self.facts["eyebrow"] |= classes
        if "text-align" in props and "center" in props["text-align"][0].lower():
            self.facts["center"] |= classes
            if re.search(r"(?:^|[\s,>+~])(?:h1|header|body|main|section)\b", low_sel) or "hero" in low_sel:
                self.facts["center_tags"] = True
        columns = props.get("grid-template-columns")
        if columns and (re.search(r"repeat\(\s*3\s*,", columns[0]) or
                        re.match(r"^\s*(?:minmax\([^)]*\)|1fr)(?:\s+(?:minmax\([^)]*\)|1fr)){2}\s*$", columns[0])):
            self.facts["three_col"] |= classes

        # A selector list such as ".nav, .footer, .modal" styles three surfaces, not one.
        surfaces = max(1, len(split_top(selector.split("{")[-1]))) if not low_sel.startswith("@") else 1

        blur_line, blur_px = None, None
        for prop in ("backdrop-filter", "-webkit-backdrop-filter"):
            if prop in props and "blur(" in props[prop][0].lower():
                blur_line = props[prop][1]
                match = re.search(r"blur\(\s*(-?\d*\.?\d+)(px|rem|em)?\s*\)", props[prop][0].lower())
                blur_px = to_px(match.group(1), match.group(2) or "px") if match else None
        if blur_line is not None:
            for _ in range(surfaces):
                self.glass.append((path, blur_line))
                self.blur_px.append(blur_px)

        self.second_wave_rule(path, selector, low_sel, props, decls, uppercase)

        radius_value = None
        for prop, value, line in decls:
            if prop.startswith("--"):
                self.css_vars[prop[2:].lower()] = value
                self.note_accents(path, value, line)
                continue
            if prop == "@apply":
                self.class_string(path, value, line)
                continue
            if prop in ("background", "background-color"):
                self.note_ground(path, low_sel, value, line)
            if prop == "border-radius":
                radius_value = value
                for _ in range(self.radius_weight(selector, surfaces)):
                    self.note_radius(path, value, line)
            elif prop == "font-size":
                self.note_font_size(path, value, line)
                px = first_length_px(value) if not value.lower().startswith(("var(", "clamp(", "calc(")) else None
                if px is not None and px >= 32.0:
                    self.facts["big"] |= classes
                    # ".metric strong { font-size: 56px }": the big element is a tag inside a class.
                    for part in split_top(selector.split("{")[-1]):
                        last = re.match(r"^(.*?)[\s>]+([a-z][a-z0-9]*)$", part.strip())
                        if last and selector_classes(last.group(1)):
                            self.facts["big_desc"].append((selector_classes(last.group(1)), last.group(2)))
            elif prop == "font-family":
                if is_font_face:
                    names = family_names(value)
                    if names:
                        self.families.append((names[0], names, path, line))
                elif not re.search(r"(?:^|[\s,])(?:code|pre|kbd|samp|tt)\b", low_sel):
                    self.note_family(path, value, line)
            elif prop == "font":
                match = re.search(r"\d(?:px|rem|em|pt|%)(?:\s*/\s*[\d.]+\w*)?\s+(.+)$", value)
                if match:
                    self.note_family(path, match.group(1), line)
            elif prop in ("box-shadow", "text-shadow"):
                self.check_shadow(path, selector, prop, value, line)
            elif prop == "filter" and "drop-shadow(" in value:
                for match in re.finditer(r"drop-shadow\(", value):
                    end = balanced(value, match.end() - 1)
                    self.check_shadow(path, selector, "drop-shadow", value[match.end():end - 1], line)
            if not prop.startswith("--"):
                self.note_colors(path, value, line)
                self.note_accents(path, value, line)

        self.check_left_border(path, selector, props, radius_value)

    def note_accents(self, path, value, line):
        for match in COLOR_TOKEN_RE.finditer(value):
            token = match.group(0)
            if token.lower().startswith("var(") or not (token.startswith("#") or "(" in token):
                continue
            rgb = parse_color(token)
            if rgb is not None:
                self.accents.append((to_hex(rgb), path, line))

    def note_ground(self, path, low_sel, value, line):
        """Record the page ground: a background on html, body, :root or main."""
        parts = [p.strip() for p in split_top(low_sel.split("{")[-1])]
        if not any(re.match(r"^(?:html|body|:root|main)$", p) for p in parts):
            return
        low = value.strip().lower()
        ref = re.match(r"^var\(\s*--([\w-]+)", low)
        if ref:
            low = self.css_vars.get(ref.group(1)) or self.sources.resolve_var(ref.group(1)) or ""
        token = COLOR_TOKEN_RE.search(low)
        rgb = parse_color(token.group(0)) if token else None
        if rgb is not None:
            self.grounds.append((to_hex(rgb), path, line))

    def sight(self, code, path, line, evidence, weight=1):
        self.counts[code] += weight
        self.first_at.setdefault(code, (path, line, evidence))

    def second_wave_rule(self, path, selector, low_sel, props, decls, uppercase):
        """CSS signals for the second-wave tells: arrows, reveals, mono labels and accent words."""
        content = props.get("content")
        if content and re.search(r"::?(?:after|before)", low_sel) and ARROW_CSS_RE.search(content[0]) and \
                re.search(r"(?:^|[\s,>+~])(?:a|button)\b|link|btn|cta|button|more", low_sel):
            self.sight("TELL_ARROW_EVERY_LINK", path, content[1], "%s { content: %s }" % (selector, content[0]),
                       ARROW_MIN)
        opacity = props.get("opacity")
        transform = props.get("transform") or props.get("translate")
        if opacity and transform and re.match(r"^0(?:\.0+)?$", opacity[0].strip()) and \
                re.search(r"translate|^\s*-?\d", transform[0].lower()) and \
                re.search(r"(?:^|[\s,>+~])section\b|reveal|data-aos|fade|animate|in-view|inview|scroll", low_sel):
            self.sight("TELL_REVEAL_EVERY_SECTION", path, opacity[1],
                       "%s { opacity: 0; transform: %s }" % (selector, transform[0]), REVEAL_MIN)
        family = props.get("font-family")
        if family and not re.search(r"(?:^|[\s,>+~.])(?:code|pre|kbd|samp|tt|mono)\b", low_sel):
            stack = family[0]
            ref = re.match(r"^var\(\s*--([\w-]+)", stack.strip())
            if ref:
                stack = self.css_vars.get(ref.group(1).lower()) or self.sources.resolve_var(ref.group(1)) or ""
            size = props.get("font-size")
            small = size is not None and (first_length_px(size[0]) or 99.0) <= 14.0
            if is_mono_stack(family_names(stack)) and uppercase and (small or "letter-spacing" in props):
                self.sight("TELL_MONO_LABELS", path, family[1], "%s { font-family: %s }" % (selector, family[0]),
                           MONO_MIN)
        if re.search(r"\bh[12]\b[^,]*[\s>]+(?:em|i|span|strong|b)\b", low_sel) and \
                any(p in props for p in ("color", "font-style", "font-family", "background")):
            self.sight("TELL_ACCENT_WORD", path, decls[0][2] if decls else 1, selector)
        if any(p in props for p in ("color", "font-style", "font-family")):
            italic = "font-style" in props and "italic" in props["font-style"][0].lower()
            if italic or "color" in props or "font-family" in props:
                self.facts["accent_classes"] |= selector_classes(selector.split("{")[-1])

    def radius_weight(self, selector, surfaces):
        """Count the elements that a radius rule rounds. A rule in an HTML file's style block counts each
        element of its markup that a simple class or tag selector matches. Any other selector counts once."""
        if self.markup is None or selector.lower().startswith("@") or selector.startswith("["):
            return surfaces
        total = 0
        for part in split_top(selector.split("{")[-1]):
            simple = re.match(r"^(\.)?([A-Za-z][A-Za-z0-9_-]*)$", part.strip())
            if not simple:
                total += 1
                continue
            kind = "class" if simple.group(1) else "tag"
            total += max(1, self.markup.get((kind, simple.group(2).lower()), 0))
        return max(1, total)

    def note_radius(self, path, value, line):
        low = value.strip().lower()
        if low.startswith("var(") or low in ("inherit", "initial", "unset"):
            return
        parts = low.split()
        if not parts or "%" in parts[0]:
            return
        px = first_length_px(low)
        if px is None or px == 0.0 or px >= 999.0:
            return
        self.radius.append((round(px, 2), path, line))

    def note_font_size(self, path, value, line):
        low = value.strip().lower()
        if not low or low.startswith("var(") or low in ("inherit", "initial", "unset", "smaller", "larger"):
            return
        if low.startswith(("clamp(", "calc(", "min(", "max(")):
            if "var(" in low:
                return
            key = "expr:" + re.sub(r"\s+", "", low)
            self.font_sizes.setdefault(key, (path, line))
            return
        match = re.match(r"^(-?\d*\.?\d+)(px|rem|pt)$", low)
        if match:
            self.font_sizes.setdefault(round(to_px(match.group(1), match.group(2)), 2), (path, line))

    def note_family(self, path, value, line):
        low = value.strip()
        match = re.match(r"^var\(\s*--([\w-]+)", low)
        if match:
            resolved = self.css_vars.get(match.group(1).lower()) or self.sources.resolve_var(match.group(1))
            if not resolved:
                self.font_unknown = True
                return
            low = resolved
        names = family_names(low)
        if not names or is_mono_stack(names):
            return
        if names[0] in ("inherit", "initial", "unset", "revert"):
            return
        self.families.append((names[0], names, path, line))

    def note_colors(self, path, value, line):
        for match in COLOR_TOKEN_RE.finditer(value):
            token = match.group(0)
            if token.lower().startswith("var(") or not (token.startswith("#") or "(" in token):
                continue
            rgb = parse_color(token)
            if rgb is not None:
                self.colors.setdefault(to_hex(rgb), (path, line))

    def check_shadow(self, path, selector, prop, value, line):
        for layer in split_top(value):
            low = layer.lower()
            if "inset" in low or low == "none":
                continue
            color = None
            rest = low
            for match in COLOR_TOKEN_RE.finditer(low):
                token = match.group(0)
                if token.startswith("var("):
                    resolved = self.css_vars.get(token[4:].strip().lstrip("-")) or \
                        self.sources.resolve_var(token[4:].strip())
                    candidate = parse_color(resolved) if resolved else None
                else:
                    candidate = parse_color(token)
                if candidate is not None:
                    color = candidate
                    rest = low.replace(token, " ")
                    break
            rest = re.sub(r"(?:rgba?|hsla?|oklch|var)\([^()]*\)?", " ", rest)
            lengths = [to_px(m.group(1), m.group(2) or "px") for m in LENGTH_RE.finditer(rest)]
            if len(lengths) < 3 or color is None:
                continue
            if lengths[0] == 0.0 and lengths[1] == 0.0 and lengths[2] >= 8.0 and is_chromatic(color, 0.3):
                self.add("TELL_GLOW_SHADOW", path, line,
                         "A %s layer has no offset, a blur of %g px and a saturated color." % (prop, lengths[2]),
                         "%s { %s: %s }" % (selector, prop, layer), {"value": layer, "hex": to_hex(color)})

    def check_left_border(self, path, selector, props, radius_value):
        low_sel = selector.lower()
        if "blockquote" in low_sel:
            return
        width, line = None, None
        for prop in ("border-left", "border-inline-start"):
            if prop in props:
                value, line = props[prop]
                if "none" in value.lower().split():
                    return
                width = first_length_px(value)
        for prop in ("border-left-width", "border-inline-start-width"):
            if prop in props:
                value, line = props[prop]
                width = first_length_px(value)
        if width is None or width < 2.0:
            return
        if "border" in props and first_length_px(props["border"][0]) is not None \
                and first_length_px(props["border"][0]) >= width:
            return
        rounded = False
        if radius_value is not None:
            rounded = radius_value.strip().lower().startswith("var(") or (first_length_px(radius_value) or 0.0) > 0.0
        boxed = bool(re.search(r"card|callout|alert|notice|panel|tile|box|banner|note|tip", low_sel))
        if rounded or boxed:
            self.add("TELL_LEFT_BORDER_CARD", path, line,
                     "A %g px bar on one side of a %s." % (width, "rounded box" if rounded else "boxed block"),
                     "%s { border-left: %g px }" % (selector, width))

    # ---- Tailwind class strings --------------------------------------
    def class_string(self, path, classes, line):
        tokens = [base_class(t) for t in classes.split() if t]
        if not tokens:
            return {}
        token_set = set(tokens)
        info = {"tokens": token_set}

        has_direction = any(re.match(r"^bg-(?:gradient-to-|linear-to-|linear-\d|radial|conic)", t) for t in tokens)
        stops, stop_colors, steps = [], [], []
        for token in tokens:
            match = re.match(r"^(?:from|via|to)-(.+)$", token)
            if not match:
                continue
            value = match.group(1)
            arbitrary = re.match(r"^\[(.+)\]$", value)
            if arbitrary:
                rgb = parse_color(arbitrary.group(1).replace("_", " "))
                if rgb is not None:
                    stop_colors.append(rgb)
                continue
            family = value.split("-")[0]
            if family in TW_FAMILIES:
                stops.append(family)
                steps.append(value.split("/")[0])
        if has_direction and (stops or stop_colors):
            chroma_families = [f for f in stops if f not in TW_NEUTRAL]
            by_family = bool(chroma_families) and any(f in TW_PURPLE for f in chroma_families) and \
                all(f in TW_NEAR_PURPLE for f in chroma_families)
            by_color = bool(stop_colors) and is_purple_run(stop_colors)
            if (by_family and (not stop_colors or by_color)) or (by_color and not chroma_families):
                self.add("TELL_PURPLE_GRADIENT", path, line,
                         "A gradient runs through %s." % ", ".join(chroma_families or ["purple stops"]),
                         classes, {"hexes": [to_hex(c) for c in stop_colors], "classes": True, "steps": steps})

        if "bg-clip-text" in token_set and "text-transparent" in token_set:
            info["gradient_text"] = True
            self.add("TELL_GRADIENT_TEXT", path, line, "Text is filled with a background through bg-clip-text.", classes)

        for token in tokens:
            match = re.match(r"^backdrop-blur(?:-(?!none$|0$)([\w\[\].-]+))?$", token)
            if match:
                size = match.group(1) or ""
                arbitrary = re.match(r"^\[(.+)\]$", size)
                self.glass.append((path, line))
                self.blur_px.append(first_length_px(arbitrary.group(1)) if arbitrary else TW_BLUR_PX.get(size))
                break

        if "font-mono" in token_set and "uppercase" in token_set and \
                any(re.match(r"^text-(?:xs|sm|\[\d)", t) for t in tokens):
            self.sight("TELL_MONO_LABELS", path, line, classes)

        for token in tokens:
            match = re.match(r"^(?:drop-)?shadow-\[(.+)\]$", token)
            if match:
                parts = match.group(1).replace("_", " ")
                self.check_shadow(path, "class", "shadow", parts, line)
                continue
            match = re.match(r"^shadow-([a-z]+)-\d{2,3}(?:/\d+)?$", token)
            if match and match.group(1) in TW_FAMILIES and match.group(1) not in TW_NEUTRAL:
                self.add("TELL_GLOW_SHADOW", path, line, "A shadow takes the color %s." % match.group(1), classes,
                         {"value": token})

        left = [t for t in tokens if re.match(r"^border-[ls]-(?:[2-9]|\[[^\]]+\])$", t)]
        rounded = [t for t in tokens if re.match(r"^rounded(?:-|$)", t) and not t.endswith(("-none", "-[0]", "-[0px]"))]
        if left and rounded:
            self.add("TELL_LEFT_BORDER_CARD", path, line, "A side bar (%s) sits on a rounded box (%s)."
                     % (left[0], rounded[0]), classes)

        for token in tokens:
            match = re.match(r"^rounded(?:-(?:t|r|b|l|tl|tr|bl|br|s|e|ss|se|es|ee))?(?:-(.+))?$", token)
            if match:
                size = match.group(1) or ""
                if size in ("full",):
                    continue
                arbitrary = re.match(r"^\[(.+)\]$", size)
                if arbitrary:
                    self.note_radius(path, arbitrary.group(1), line)
                elif size in TW_RADIUS_PX and TW_RADIUS_PX[size] > 0.0:
                    self.radius.append((TW_RADIUS_PX[size], path, line))
                continue
            match = re.match(r"^text-\[(-?\d*\.?\d+(?:px|rem|pt))\]$", token)
            if match:
                self.note_font_size(path, match.group(1), line)
                continue
            match = re.match(r"^font-\[(.+)\]$", token)
            if match and not re.match(r"^\d+$", match.group(1)):
                self.note_family(path, match.group(1).replace("_", " "), line)
                continue
            match = re.match(r"^(?:bg|text|border|from|via|to|fill|stroke|ring|outline|decoration|accent|caret|divide)"
                             r"-\[(.+)\]$", token)
            if match:
                rgb = parse_color(match.group(1).replace("_", " "))
                if rgb is not None:
                    self.colors.setdefault(to_hex(rgb), (path, line))

        info["eyebrow"] = "uppercase" in token_set and any(re.match(r"^tracking-(?:wide|wider|widest|\[)", t)
                                                           for t in tokens)
        info["big"] = any(re.match(r"^text-[3-9]xl$", t) for t in tokens)
        info["center"] = "text-center" in token_set
        info["three_col"] = "grid-cols-3" in token_set
        return info

    # ---- markup -------------------------------------------------------
    def markup_pass(self, path, text):
        class_spans = []      # (offset, class string, info)
        for match in CLASS_ATTR_RE.finditer(text):
            value = next((g for g in match.groups() if g is not None), "")
            value = re.sub(r"\$\{[^}]*\}", " ", value)
            info = self.class_string(path, value, line_of(text, match.start()))
            class_spans.append((match.start(), value, info))
        for match in CLASS_FN_RE.finditer(text):
            end = balanced(text, match.end() - 1)
            for inner in STRING_RE.finditer(text[match.end():end]):
                value = inner.group(2) or inner.group(3) or inner.group(4) or ""
                if value.strip():
                    offset = match.end() + inner.start()
                    info = self.class_string(path, value, line_of(text, offset))
                    class_spans.append((offset, value, info))

        self.check_hero(path, text, class_spans)
        self.check_eyebrows(path, text)
        self.check_stats(path, text)
        self.check_accent_word(path, text)
        self.check_sequence(path, text)
        self.check_arrows(path, text)
        self.check_reveals(path, text)
        self.check_middots(path, text)
        for match in re.finditer(r"<(?:html|body|main)\b([^<>]*)>", text, re.I):
            for token in self.element_classes(match.group(1)).split():
                color = re.match(r"^bg-\[(.+)\]$", base_class(token))
                rgb = parse_color(color.group(1).replace("_", " ")) if color else None
                if rgb is not None:
                    self.grounds.append((to_hex(rgb), path, line_of(text, match.start())))

        if re.search(r"<html\b|<body\b", text, re.I):
            styled = bool(class_spans) or bool(STYLE_BLOCK_RE.search(text)) or "stylesheet" in text.lower()
            self.html_docs.append((path, styled))
        for match in re.finditer(r"fonts\.googleapis\.com/css2?\?([^\"'\s>]+)", text):
            for family in re.findall(r"family=([^&:;\"']+)", match.group(1)):
                name = family.replace("+", " ").strip().lower()
                if name:
                    self.families.append((name, [name], path, line_of(text, match.start())))
        for match in re.finditer(r"import\s*\{([^}]*)\}\s*from\s*[\"']next/font/google[\"']", text):
            for name in match.group(1).split(","):
                name = name.strip().split(" as ")[0].replace("_", " ").strip().lower()
                if name:
                    self.families.append((name, [name], path, line_of(text, match.start())))

    def element_classes(self, attrs):
        match = CLASS_ATTR_RE.search(attrs)
        if not match:
            return ""
        return next((g for g in match.groups() if g is not None), "")

    def check_hero(self, path, text, class_spans):
        h1 = re.search(r"<h1\b[^<>]*>", text, re.I)
        if not h1:
            return
        start = max(0, h1.start() - 1200)
        window = text[start:h1.end()]
        centered = bool(re.search(r"text-align\s*:\s*center", window, re.I)) or self.facts["center_tags"]
        for offset, value, info in class_spans:
            if start <= offset <= h1.end():
                tokens = info.get("tokens", set())
                if info.get("center") or tokens & self.facts["center"]:
                    centered = True
        if not centered:
            return
        grid_at = None
        for offset, value, info in class_spans:
            if offset > h1.end() and (info.get("three_col") or info.get("tokens", set()) & self.facts["three_col"]):
                grid_at = offset
                break
        if grid_at is None:
            inline = re.search(r"grid-template-columns\s*:\s*repeat\(\s*3\s*,", text[h1.end():], re.I)
            if inline:
                grid_at = h1.end() + inline.start()
        if grid_at is None:
            return
        after = [value.strip() for offset, value, _ in class_spans if grid_at < offset < grid_at + 6000 and value.strip()]
        equal = any(count >= 3 for count in Counter(after).values()) or ".map(" in text[grid_at:grid_at + 400]
        self.add("TELL_HERO_THREE_CARDS", path, line_of(text, h1.start()),
                 "A centered h1 is followed by a three-column grid%s." %
                 (" whose children share one class string" if equal else ""),
                 text[h1.start():h1.start() + 100])

    def check_eyebrows(self, path, text):
        headings = len(HEADING_RE.findall(text))
        count, first = 0, None
        pattern = re.compile(r"<([A-Za-z][\w.-]*)\b([^<>]*)>([^<>]{1,90})</\1\s*>\s*<h[1-4]\b")
        for match in pattern.finditer(text):
            if match.group(1).lower() in ("h1", "h2", "h3", "h4", "a", "button", "li", "option"):
                continue
            classes = self.element_classes(match.group(2))
            tokens = set(base_class(t) for t in classes.split())
            is_eyebrow = bool(EYEBROW_NAME_RE.search(classes)) or bool(tokens & self.facts["eyebrow"]) or \
                ("uppercase" in tokens and any(re.match(r"^tracking-(?:wide|wider|widest|\[)", t) for t in tokens)) or \
                bool(re.search(r"text-transform\s*:\s*uppercase", match.group(2), re.I))
            if not is_eyebrow:
                continue
            weight = 3 if ".map(" in text[max(0, match.start() - 400):match.start()] else 1
            count += weight
            if first is None:
                first = match
        for match in EYEBROW_COMPONENT_RE.finditer(text):
            weight = 3 if ".map(" in text[max(0, match.start() - 400):match.start()] else 1
            count += weight
            if first is None:
                first = match
        if first is None or count < EYEBROW_MIN:
            return
        if headings and float(count) / headings < EYEBROW_SHARE:
            return
        self.add("TELL_EYEBROW_EVERY_HEADING", path, line_of(text, first.start()),
                 "A small label sits above %d heading(s); the file holds %d h1 and h2 heading(s)." % (count, headings),
                 first.group(0))

    def big_by_ancestor(self, text, match):
        """True when CSS such as '.metric strong { font-size: 56px }' makes this element big."""
        tag = match.group(1).lower()
        before = text[max(0, match.start() - 300):match.start()]
        for classes, desc_tag in self.facts["big_desc"]:
            if desc_tag != tag:
                continue
            for attrs in re.findall(r"<[A-Za-z][\w.-]*\b([^<>]*)>", before):
                if set(self.element_classes(attrs).split()) & classes:
                    return True
        return False

    def check_stats(self, path, text):
        hits, gradient = [], False
        for match in ELEMENT_TEXT_RE.finditer(text):
            content = match.group(3).strip()
            if not STAT_TEXT_RE.match(content) or not re.search(r"\d", content):
                continue
            classes = self.element_classes(match.group(2))
            tokens = set(base_class(t) for t in classes.split())
            big = any(re.match(r"^text-[3-9]xl$", t) for t in tokens) or bool(tokens & self.facts["big"]) or \
                bool(STAT_NAME_RE.search(classes)) or self.big_by_ancestor(text, match)
            if not big:
                continue
            hits.append(match)
            if ("bg-clip-text" in tokens and "text-transparent" in tokens) or tokens & self.facts["gradient_text"]:
                gradient = True
        if len(hits) < STAT_MIN:
            return
        code = "TELL_GRADIENT_STAT_ROW" if gradient else "TELL_STAT_ROW"
        self.add(code, path, line_of(text, hits[0].start()),
                 "%d big numbers sit in one file as a stat row%s." % (len(hits), " with gradient fills" if gradient else ""),
                 hits[0].group(0))
        # A stat row is a set of claims. With no source in view, each figure is an invented fact.
        end = min(len(text), hits[-1].end() + SOURCE_HINT_LOOKAHEAD)
        if not SOURCE_HINT_RE.search(text[max(0, hits[0].start() - 200):end]):
            self.invented(path, line_of(text, hits[0].start()),
                          "%d figures in a stat row have no source in view." % len(hits), hits[0].group(0))

    def invented(self, path, line, message, evidence):
        if (path, line) in self.invented_lines:
            return
        self.invented_lines.add((path, line))
        self.add("TELL_INVENTED_STAT", path, line, message, evidence)

    def check_accent_word(self, path, text):
        """One styled word inside an h1 or h2: an em or i, or a span with its own color, face or style."""
        for heading in re.finditer(r"<(h[12])\b[^<>]*>(.*?)</\1\s*>", text, re.I | re.S):
            inner = heading.group(2)
            for word in re.finditer(r"<(em|i|span|strong|b)\b([^<>]*)>([^<>]{1,40})</\1\s*>", inner, re.I):
                tag, attrs = word.group(1).lower(), word.group(2)
                rest = (inner[:word.start()] + inner[word.end():])
                if not re.search(r"[A-Za-z]{2,}", re.sub(r"<[^<>]*>", " ", rest)):
                    continue
                tokens = set(base_class(t) for t in self.element_classes(attrs).split())
                styled = tag in ("em", "i") or bool(re.search(r"style\s*=", attrs, re.I)) or \
                    bool(tokens & self.facts["accent_classes"]) or \
                    any(re.match(r"^(?:italic|font-serif|font-display|text-(?!xs|sm|base|lg|[2-9]?xl|center|left|"
                                 r"right|balance|pretty|wrap|nowrap)[a-z]+-\d{2,3}|text-\[#|bg-clip-text)", t)
                        for t in tokens)
                if styled:
                    self.sight("TELL_ACCENT_WORD", path, line_of(text, heading.start()), heading.group(0))
                    return

    def check_sequence(self, path, text):
        """Two-digit markers 01, 02, 03 on items outside an ordered list."""
        ordered = [(m.start(), m.end()) for m in re.finditer(r"<ol\b.*?</ol\s*>", text, re.I | re.S)]
        seen, first = set(), None
        pattern = re.compile(r">\s*[\[(]?\s*(0[1-9])\s*[\])]?\s*(?:[./\u2014-]\s*)?(?=<|\s[A-Za-z]|$)"
                             r"|[\"'`](0[1-9])[\"'`]")
        for match in pattern.finditer(text):
            if any(start <= match.start() < end for start, end in ordered):
                continue
            seen.add(match.group(1) or match.group(2))
            if first is None:
                first = match
        if first is not None and len(seen) >= SEQUENCE_MIN and "01" in seen:
            self.add("TELL_FAKE_SEQUENCE", path, line_of(text, first.start()),
                     "Numbered markers %s sit outside an ordered list." % ", ".join(sorted(seen)[:5]),
                     text[first.start():first.start() + 60])

    def check_arrows(self, path, text):
        links = list(re.finditer(r"<(a|button|Link)\b[^<>]*>(.*?)</\1\s*>", text, re.S))
        arrowed = [m for m in links if ARROW_TEXT_RE.search(re.sub(r"<(?!/?svg)[^<>]*>", " ", m.group(2))) or
                   re.search(r"<(?:ArrowRight|ArrowUpRight|ChevronRight|MoveRight)\w*\b|arrow-right|arrow-up-right",
                             m.group(2))]
        for match in arrowed:
            self.sight("TELL_ARROW_EVERY_LINK", path, line_of(text, match.start()), match.group(0))

    def check_reveals(self, path, text):
        reveal = re.compile(r"initial\s*=\s*\{\{\s*opacity\s*:\s*0\s*,\s*[xy]\s*:\s*-?\d+|data-aos\s*=\s*[\"'](?:fade|slide)"
                            r"|\bclass(?:Name)?\s*=\s*[\"'][^\"']*\b(?:reveal|fade-up|fade-in-up|animate-on-scroll)\b")
        for match in reveal.finditer(text):
            self.sight("TELL_REVEAL_EVERY_SECTION", path, line_of(text, match.start()), match.group(0))

    def check_middots(self, path, text):
        for match in re.finditer(r">([^<>]{3,160})<", text):
            node = match.group(1)
            if MIDDOT_RE.search(node) and len(node.split()) <= 16:
                self.sight("TELL_MIDDOT_META", path, line_of(text, match.start()), node.strip())

    def stat_text_pass(self, path, text):
        """Find figures split across elements, and figures in JS data arrays."""
        if "<" in text:
            stripped, origin = [], []
            for match in re.finditer(r"<[^<>]*>|[^<]+|<", text):
                if match.group(0).startswith("<") and len(match.group(0)) > 1:
                    stripped.append(" ")
                    origin.append(match.start())
                else:
                    stripped.append(match.group(0))
                    origin.extend(range(match.start(), match.end()))
            flat = "".join(stripped)
            flat = re.sub(r"&nbsp;|&#160;", lambda m: " " * len(m.group(0)), flat) if "&" in flat else flat
            for pattern in STAT_RES:
                for match in pattern.finditer(flat):
                    start, stop = origin[min(match.start(), len(origin) - 1)], origin[min(match.end() - 1, len(origin) - 1)]
                    window = text[start:min(len(text), stop + SOURCE_HINT_LOOKAHEAD)]
                    lines = text[text.rfind("\n", 0, start) + 1:start]
                    if SOURCE_HINT_RE.search(window) or SOURCE_HINT_RE.search(lines):
                        continue
                    self.invented(path, line_of(text, start), "A specific figure has no source in view.",
                                  " ".join(match.group(0).split()))
        for obj in JS_OBJECT_RE.finditer(text):
            body = obj.group(0)
            value = re.search(STAT_VALUE_KEYS + r"\s*:\s*[\"'`]([^\"'`]{1,20})[\"'`]", body, re.I)
            label = re.search(STAT_LABEL_KEYS + r"\s*:\s*[\"'`]([^\"'`]{1,60})[\"'`]", body, re.I)
            if not value or not label or not re.search(r"\d", value.group(1)) or SOURCE_HINT_RE.search(body) or \
                    re.search(r"\bsource\w*\s*:", body, re.I):
                continue
            joined = "%s %s" % (value.group(1).strip(), label.group(1).strip())
            if any(p.search(joined) for p in STAT_RES):
                self.invented(path, line_of(text, obj.start()), "A figure in a data object has no source.", joined)

    # ---- content ------------------------------------------------------
    def content_pass(self, path, text):
        lorem = list(LOREM_RE.finditer(text))
        if lorem:
            lorem_lines = sorted(set(line_of(text, m.start()) for m in lorem))
            self.add("TELL_LOREM", path, lorem_lines[0],
                     "Placeholder Latin text appears on %d line(s)." % len(lorem_lines),
                     text[lorem[0].start():lorem[0].start() + 60])
        seen = set()
        for pattern in PLACEHOLDER_RES:
            for match in pattern.finditer(text):
                line = line_of(text, match.start())
                if line not in seen:
                    seen.add(line)
                    self.add("TELL_PLACEHOLDER_COPY", path, line, "Generic placeholder copy or an invented name.",
                             match.group(0).strip("<> "))
        lines = text.split("\n")
        for pattern in STAT_RES:
            for match in pattern.finditer(text):
                line = line_of(text, match.start())
                if SOURCE_HINT_RE.search(lines[line - 1]):
                    continue
                self.invented(path, line, "A specific figure has no source in view.", match.group(0))
        self.stat_text_pass(path, text)
        for number, raw in enumerate(lines, 1):
            index = emoji_icon_index(raw)
            if index is not None:
                self.add("TELL_EMOJI_ICON", path, number, "An emoji sits where an icon belongs.",
                         raw.strip().encode("ascii", "backslashreplace").decode("ascii"))

    def gradient_pass(self, path, text):
        for match in GRADIENT_RE.finditer(text):
            end = balanced(text, match.end() - 1)
            args = text[match.end():end - 1]
            colors, hexes, unresolved = [], [], 0
            for token_match in COLOR_TOKEN_RE.finditer(args):
                token = token_match.group(0)
                if token.lower().startswith("var("):
                    name = token[4:].strip()
                    resolved = self.css_vars.get(name.lstrip("-").lower()) or self.sources.resolve_var(name)
                    rgb = parse_color(resolved) if resolved else None
                    if rgb is None:
                        unresolved += 1
                        continue
                else:
                    rgb = parse_color(token)
                if rgb is not None:
                    colors.append(rgb)
                    hexes.append(to_hex(rgb))
            if colors and is_purple_run(colors):
                self.add("TELL_PURPLE_GRADIENT", path, line_of(text, match.start()),
                         "A gradient runs through purple, indigo or violet stops (%s)." % ", ".join(hexes[:4]),
                         text[match.start():min(end, match.start() + 110)], {"hexes": hexes})

    # ---- files --------------------------------------------------------
    def scan_file(self, path, text, ext):
        self.files += 1
        if ext in CSS_EXT:
            self.css_pass(path, text, 1)
        else:
            self.markup = markup_counts(text)
            for match in STYLE_BLOCK_RE.finditer(text):
                self.css_pass(path, match.group(1), line_of(text, match.start(1)))
            for match in STYLE_ATTR_RE.finditer(text):
                value = match.group(1) if match.group(1) is not None else match.group(2)
                self.css_pass(path, "[inline style]{%s}" % value, line_of(text, match.start()))
            pseudo = []
            for match in JSX_STYLE_RE.finditer(text):
                prop = re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), match.group(1)).lstrip("-")
                prop = prop.replace("webkit-", "-webkit-")
                number = match.group(2)
                value = (number + "px") if number is not None else next(
                    (g for g in match.groups()[2:] if g is not None), "")
                pseudo.append((prop, value, line_of(text, match.start())))
            for prop, value, line in pseudo:
                self.handle_rule(path, "[style object]", [(prop, value, line)], line)
            self.markup = None

    def second_pass(self, path, text, ext):
        self.gradient_pass(path, text)
        if ext not in CSS_EXT:
            self.markup_pass(path, text)
        self.content_pass(path, text)

    # ---- aggregate ----------------------------------------------------
    def aggregate(self):
        if len(self.glass) >= GLASS_THRESHOLD:
            by_file = OrderedDict()
            for path, line in self.glass:
                by_file.setdefault(path, []).append(line)
            for path, lines in by_file.items():
                self.add("TELL_GLASS_EVERYWHERE", path, lines[0],
                         "Backdrop blur appears %d time(s) in this file and %d time(s) in the scan."
                         % (len(lines), len(self.glass)), "backdrop blur at line(s) %s"
                         % ", ".join(str(n) for n in sorted(set(lines))[:8]), {"blurs": list(self.blur_px)})

        if len(self.radius) >= RADIUS_MIN_USES:
            counts = Counter(px for px, _, _ in self.radius)
            value, uses = counts.most_common(1)[0]
            share = float(uses) / len(self.radius)
            if value >= RADIUS_LARGE_PX and share >= RADIUS_SHARE:
                first = next(item for item in self.radius if item[0] == value)
                self.add("TELL_UNIFORM_RADIUS", first[1], first[2],
                         "%d of %d radius uses are %g px." % (uses, len(self.radius), value),
                         "radius %g px" % value, {"px": value})

        firsts = [item for item in self.families]
        stock_type = False
        if firsts and not self.font_unknown:
            names = set(item[0] for item in firsts)
            if names <= DEFAULT_FAMILIES:
                stock_type = True
                item = firsts[0]
                self.add("TELL_DEFAULT_FONT_ONLY", item[2], item[3],
                         "Every declared family starts with a default: %s." % ", ".join(sorted(names)),
                         "font-family: %s" % ", ".join(item[1][:4]), {"families": sorted(names)})
            elif names <= DEFAULT_FAMILIES | SECOND_WAVE_FAMILIES:
                stock_type = True
                wave = sorted(names & SECOND_WAVE_FAMILIES)
                item = next(i for i in firsts if i[0] in SECOND_WAVE_FAMILIES)
                self.add("TELL_SECOND_WAVE_FONT", item[2], item[3],
                         "The faces are %s; %s is on the second-wave list of %s." % (
                             ", ".join(sorted(names)), " and ".join(wave), SECOND_WAVE_DATE),
                         "font-family: %s" % ", ".join(item[1][:4]), {"families": wave})
        elif not firsts and not self.font_unknown:
            for path, styled in self.html_docs:
                if styled:
                    stock_type = True
                    self.add("TELL_DEFAULT_FONT_ONLY", path, 1,
                             "No font family is declared. The page renders in a browser or framework default.",
                             "no font-family in the scan", {"families": []})
                    break
        self.check_palette(stock_type)

        for code, minimum in (("TELL_ARROW_EVERY_LINK", ARROW_MIN), ("TELL_REVEAL_EVERY_SECTION", REVEAL_MIN),
                              ("TELL_MONO_LABELS", MONO_MIN), ("TELL_MIDDOT_META", MIDDOT_MIN),
                              ("TELL_ACCENT_WORD", 1)):
            if self.counts[code] >= minimum:
                path, line, evidence = self.first_at[code]
                self.add(code, path, line, SIGHT_MESSAGES[code] % self.counts[code], evidence)

        sizes = {k: v for k, v in self.font_sizes.items()
                 if not (isinstance(k, float) and k in self.sources.sizes_px)}
        if len(sizes) > self.max_font_sizes:
            listed = sorted(k for k in sizes if isinstance(k, float))
            first = sizes[listed[0]] if listed else list(sizes.values())[0]
            self.add("TELL_FONT_SIZE_SPRAWL", first[0], first[1],
                     "%d distinct literal font sizes; the limit is %d." % (len(sizes), self.max_font_sizes),
                     "sizes in px: %s" % ", ".join("%g" % k for k in listed[:14]))

        colors = {k: v for k, v in self.colors.items() if k not in self.sources.colors}
        if len(colors) > self.max_colors:
            listed = sorted(colors)
            first = colors[listed[0]]
            self.add("TELL_COLOR_SPRAWL", first[0], first[1],
                     "%d distinct literal colors outside tokens; the limit is %d." % (len(colors), self.max_colors),
                     "colors: %s" % ", ".join(listed[:14]))

    def check_palette(self, stock_type):
        """A second-wave template palette: the ground and every accent fall in one known look."""
        if not self.grounds or not stock_type:
            return
        ground_hex, path, line = self.grounds[0]
        ground = rgb_to_oklch(parse_color(ground_hex))
        accents = []
        for hexv, _p, _l in self.accents:
            lightness, chroma, hue = rgb_to_oklch(parse_color(hexv))
            if chroma >= ACCENT_MIN_CHROMA and 0.25 < lightness < 0.9:
                accents.append((hexv, hue))
        if not accents:
            return
        for look, (side, test, bands, name) in SECOND_WAVE_LOOKS.items():
            if not ground_matches(ground, test):
                continue
            hues = [hue for _h, hue in accents]
            for low, high in bands:
                if all(low <= hue <= high for hue in hues):
                    hexes = sorted(set([ground_hex] + [h for h, _ in accents]))
                    self.add("TELL_SECOND_WAVE_PALETTE", path, line,
                             "The palette is the %s look (%s): ground %s, accent %s, with stock type."
                             % (look, name, ground_hex, ", ".join(sorted(set(h for h, _ in accents))[:3])),
                             "ground %s" % ground_hex, {"hexes": hexes, "look": look})
                    return

    # ---- brand-required -------------------------------------------------
    def prescribed_by(self, item):
        code, ctx, src = item["code"], item["ctx"], self.sources
        if code in self.allow:
            return "user (--allow %s)" % code
        if code in NEVER_BRAND_REQUIRED or not src.loaded:
            return None
        if src.tokens_path:
            if code == "TELL_PURPLE_GRADIENT":
                # Required only when a gradient token holds these exact stops. Stops that are plain token
                # colors or ramp steps (indigo-500, purple-500) are not a brand gradient.
                hexes = list(ctx.get("hexes") or [])
                steps = ctx.get("steps") or []
                if steps:
                    resolved = [src.tailwind_color(step) for step in steps]
                    if any(h is None for h in resolved):
                        return None
                    hexes = hexes + resolved
                if hexes:
                    hit = src.gradient_token(hexes)
                    if hit:
                        return hit
                return None
            elif code == "TELL_GLOW_SHADOW":
                hit = src.shadow_token(str(ctx.get("value", "")))
                if hit:
                    return hit
            elif code == "TELL_GLASS_EVERYWHERE":
                hit = src.blur_token(ctx.get("blurs") or [])
                if hit:
                    return hit
            elif code == "TELL_SECOND_WAVE_PALETTE":
                hexes = ctx.get("hexes") or []
                if hexes and all(h in src.colors for h in hexes):
                    return "%s colors %s" % (os.path.basename(src.tokens_path),
                                             ", ".join("\"%s\"" % src.colors[h] for h in hexes[:3]))
            elif code == "TELL_SECOND_WAVE_FONT":
                for name in ctx.get("families") or []:
                    if name in src.families:
                        return "%s %s names \"%s\"" % (os.path.basename(src.tokens_path), src.families[name], name)
            elif code == "TELL_UNIFORM_RADIUS":
                ordinary = sorted(set(px for px in src.radius_px if 0.0 < px < 999.0))
                if len(ordinary) == 1 and abs(ordinary[0] - float(ctx.get("px", -1))) < 0.01:
                    return "%s radius family holds one value" % os.path.basename(src.tokens_path)
            elif code == "TELL_DEFAULT_FONT_ONLY":
                for name in ctx.get("families") or []:
                    if name in src.families:
                        return "%s %s names \"%s\"" % (os.path.basename(src.tokens_path), src.families[name], name)
            if code in TOKEN_KEYWORDS:
                hit = src.token_named(TOKEN_KEYWORDS[code])
                if hit:
                    return hit
        if src.design_path:
            if code in ("TELL_DEFAULT_FONT_ONLY", "TELL_SECOND_WAVE_FONT"):
                names = [n for n in (ctx.get("families") or []) if n not in GENERIC_FAMILIES and len(n) > 2]
                if names:
                    hit = src.design_mentions([r"(?<![\w-])%s(?![\w-])" % re.escape(n) for n in names])
                    if hit:
                        return hit
            elif code in DESIGN_KEYWORDS:
                hit = src.design_mentions(DESIGN_KEYWORDS[code])
                if hit:
                    return hit
        return None

    def result(self):
        self.aggregate()
        findings, required = [], []
        for item in self.raw:
            severity, _, hint = RULES[item["code"]]
            source = self.prescribed_by(item)
            base = OrderedDict([("code", item["code"]), ("severity", severity), ("path", item["path"]),
                                ("line", item["line"]), ("message", item["message"]),
                                ("evidence", item["evidence"])])
            if source:
                base["source"] = source
                required.append(base)
            else:
                base["hint"] = hint
                findings.append(base)
        findings.sort(key=lambda f: (-RANK[f["severity"]], f["path"], f["line"], f["code"]))
        required.sort(key=lambda f: (f["path"], f["line"], f["code"]))
        return findings, required


SIGHT_MESSAGES = {
    "TELL_ARROW_EVERY_LINK": "An arrow sits on links or buttons (weight %d; a CSS ::after arrow on links counts as all).",
    "TELL_REVEAL_EVERY_SECTION": "A fade and slide-up reveal is set on sections (weight %d; one CSS rule on "
                                 "every section counts as all).",
    "TELL_MONO_LABELS": "Small uppercase labels are set in a monospace face (weight %d).",
    "TELL_MIDDOT_META": "%d short text runs join their parts with middle dots.",
    "TELL_ACCENT_WORD": "A headline sets one word apart with italic, a second face or a second color (%d).",
}


def ground_matches(oklch, test):
    """True when an OKLCH ground is cream (light, warm, slightly tinted) or near-black."""
    lightness, chroma, hue = oklch
    if test == "cream":
        return lightness >= 0.9 and 0.008 <= chroma <= 0.06 and 50.0 <= hue <= 110.0
    if test == "near-black":
        return lightness <= 0.25
    return False


EMOJI_ICON_MAX_WORDS = 3


def is_emoji(ch):
    point = ord(ch)
    return 0x1F000 <= point <= 0x1FAFF or 0x2600 <= point <= 0x27BF or point in (0x2B50, 0x2B55)


def emoji_icon_index(line):
    """Return the index of an emoji used as an icon, else None.

    An emoji is an icon when it sits at the edge of an element or a string whose other text is a short
    label (three words or fewer), or in CSS content. An emoji at the edge of a sentence, such as the end
    of a chat message, is content.
    """
    for index, ch in enumerate(line):
        if not is_emoji(ch):
            continue
        if re.search(r"content\s*:", line[:index]):
            return index
        before = line[:index].rstrip()
        after = line[index + 1:].lstrip(u"\ufe0f\u200d ").lstrip()
        at_edge = not before or before[-1] in ">\"'`{(" or not after or after[0] in "<\"'`})"
        if not at_edge:
            continue
        left = max(before.rfind(c) for c in ">\"'`{(") + 1 if before else 0
        stops = [i for i in (after.find(c) for c in "<\"'`})") if i >= 0]
        segment = before[left:] + " " + (after[:min(stops)] if stops else after)
        words = re.findall(r"[^\W\d_]{2,}", "".join(c for c in segment if not is_emoji(c)))
        if len(words) <= EMOJI_ICON_MAX_WORDS:
            return index
    return None


# ---------------------------------------------------------------- CLI

def collect_files(paths, left_out=None):
    """Return (files, missing). Vendor folders and dot folders inside a given folder are left out and
    listed in left_out. A dot folder given directly is scanned."""
    out, missing = [], []
    for path in paths:
        if os.path.isdir(path):
            for current, dirs, files in os.walk(path):
                kept = []
                for name in sorted(dirs):
                    if name in SKIP_DIRS or name.startswith("."):
                        if left_out is not None and name != ".git":
                            left_out.append(os.path.join(current, name))
                    else:
                        kept.append(name)
                dirs[:] = kept
                for name in sorted(files):
                    ext = os.path.splitext(name)[1].lower()
                    if ext in MARKUP_EXT or ext in CSS_EXT:
                        out.append(os.path.join(current, name))
        elif os.path.isfile(path):
            out.append(path)
        else:
            missing.append(path)
    return out, missing


def read_source(path):
    """Read a file for the scan. Inlined data: URIs are replaced by a short placeholder, so a single-file
    page with embedded images stays under the size limit. Return (text, None) or (None, reason)."""
    size = os.path.getsize(path)
    if size > MAX_BYTES * 20:
        return None, "larger than %d bytes" % (MAX_BYTES * 20)
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    if len(text) > MAX_BYTES:
        text = DATA_URI_RE.sub(lambda m: m.group(0).split(",", 1)[0] + ",GDH-DATA-URI", text)
    if len(text) > MAX_BYTES:
        return None, "larger than %d bytes after data: URIs are removed" % MAX_BYTES
    return text, None


def run_scan(paths, tokens=None, design=None, allow=None, max_font_sizes=DEFAULT_MAX_FONT_SIZES,
             max_colors=DEFAULT_MAX_COLORS):
    """Scan the paths. Return a result dict. Raises ValueError on unreadable inputs."""
    sources = DesignSources()
    if tokens:
        try:
            sources.load_tokens(tokens)
        except (OSError, ValueError) as error:
            raise ValueError("cannot read tokens file %s: %s" % (tokens, error))
    if design:
        try:
            sources.load_design(design)
        except OSError as error:
            raise ValueError("cannot read design file %s: %s" % (design, error))
    for code in allow or []:
        if code not in RULES:
            raise ValueError("unknown code for --allow: %s" % code)
        if code in ("TELL_LOREM", "TELL_PLACEHOLDER_COPY", "TELL_INVENTED_STAT"):
            raise ValueError("%s is a content gate and cannot be allowed" % code)
    left_out = []
    files, missing = collect_files(paths, left_out)
    if missing:
        raise ValueError("no such file or folder: %s" % ", ".join(missing))
    scan = Scan(sources, max_font_sizes, max_colors, allow)
    loaded, skipped, reasons = [], [], OrderedDict()
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        try:
            text, reason = read_source(path)
        except OSError as error:
            text, reason = None, "unreadable: %s" % error.strerror
        if text is None:
            skipped.append(path)
            reasons[path] = reason
            continue
        loaded.append((path, text, ext))
    for path, text, ext in loaded:
        scan.scan_file(path, text, ext)
    for path, text, ext in loaded:
        scan.second_pass(path, text, ext)
    findings, required = scan.result()
    summary = OrderedDict((level, sum(1 for f in findings if f["severity"] == level)) for level in SEVERITIES)
    summary["brandRequired"] = len(required)
    return OrderedDict([
        ("tool", "tells.py"), ("version", VERSION), ("listVersion", LIST_VERSION),
        ("scanned", scan.files), ("skipped", skipped), ("skipReasons", reasons), ("leftOut", left_out),
        ("complete", bool(scan.files) and not skipped),
        ("designSystem", OrderedDict([("tokens", tokens), ("design", design)])),
        ("findings", findings), ("brandRequired", required), ("summary", summary), ("note", NOTE),
    ])


def format_text(result):
    lines = ["tells.py, list %s: scanned %d file(s)" % (result["listVersion"], result["scanned"])]
    if not result["designSystem"]["tokens"] and not result["designSystem"]["design"]:
        lines.append("No design system given. Pass --tokens and --design so that required patterns are not findings.")
    for item in result["findings"]:
        lines.append("%-6s %s  %s:%d" % (item["severity"].upper(), item["code"], item["path"], item["line"]))
        lines.append("       %s" % item["message"])
        if item["evidence"]:
            lines.append("       seen: %s" % item["evidence"])
        lines.append("       fix: %s" % item["hint"])
    if result["brandRequired"]:
        lines.append("brand-required (not findings):")
        for item in result["brandRequired"]:
            lines.append("       %s  %s:%d  source: %s" % (item["code"], item["path"], item["line"], item["source"]))
    summary = result["summary"]
    lines.append("Summary: %d high, %d medium, %d low; %d brand-required"
                 % (summary["high"], summary["medium"], summary["low"], summary["brandRequired"]))
    if result["skipped"]:
        lines.append("Skipped: %s" % ", ".join(result["skipped"]))
        for path, reason in result["skipReasons"].items():
            lines.append("       %s: %s" % (path, reason))
    if result["leftOut"]:
        lines.append("Folders left out (vendor or dot folders; name one to scan it): %s" % ", ".join(result["leftOut"]))
    lines.append(result["note"])
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tells.py",
        description="Heuristic scan for generic AI-output tells in HTML, CSS, JSX, TSX and Tailwind classes.")
    parser.add_argument("paths", nargs="*", help="files or folders to scan")
    parser.add_argument("--tokens", help="tokens.json of the design system")
    parser.add_argument("--design", help="DESIGN.md of the design system")
    parser.add_argument("--allow", action="append", default=[], metavar="CODE",
                        help="report this code as required by the user; repeat for more codes")
    parser.add_argument("--max-font-sizes", type=int, default=DEFAULT_MAX_FONT_SIZES,
                        help="distinct literal font sizes allowed (default %d)" % DEFAULT_MAX_FONT_SIZES)
    parser.add_argument("--max-colors", type=int, default=DEFAULT_MAX_COLORS,
                        help="distinct literal colors allowed outside tokens (default %d)" % DEFAULT_MAX_COLORS)
    parser.add_argument("--fail-on", choices=SEVERITIES, default="low",
                        help="lowest severity that sets exit code 1 (default low)")
    parser.add_argument("--json", action="store_true", help="print one JSON object on stdout")
    parser.add_argument("--list", action="store_true", help="print the rule list and exit")
    parser.add_argument("--version", action="version", version="tells.py %s (list %s)" % (VERSION, LIST_VERSION))
    return parser


def main(argv=None):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as stop:
        return int(stop.code or 0)
    if args.list:
        rules = [OrderedDict([("code", code), ("severity", sev), ("what", what), ("hint", hint)])
                 for code, (sev, what, hint) in RULES.items()]
        if args.json:
            print(json.dumps(OrderedDict([("listVersion", LIST_VERSION), ("rules", rules)]), indent=2))
        else:
            print("tells.py rule list %s" % LIST_VERSION)
            for rule in rules:
                print("%-6s %-28s %s" % (rule["severity"].upper(), rule["code"], rule["what"]))
        return 0
    if not args.paths:
        sys.stderr.write("tells.py: give at least one file or folder\n")
        return 2
    try:
        result = run_scan(args.paths, args.tokens, args.design, args.allow, args.max_font_sizes, args.max_colors)
    except ValueError as error:
        sys.stderr.write("tells.py: %s\n" % error)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result))
    if not result["scanned"]:
        # A scan that read no file proves nothing. An empty folder, a folder whose markup sits only in
        # dot folders or vendor folders, or a file over the size limit must not pass as clean.
        sys.stderr.write("tells.py: no file was scanned%s%s. Give the markup or CSS files to check.\n" % (
            "; skipped: %s" % ", ".join(result["skipped"]) if result["skipped"] else "",
            "; left out: %s" % ", ".join(result["leftOut"]) if result["leftOut"] else ""))
        return 2
    if result["skipped"]:
        # A partial scan is not a pass either: the gate cannot judge a file it did not read.
        sys.stderr.write("tells.py: incomplete scan; %d file(s) not read: %s. Split or shrink them, or pass "
                         "only the files to judge.\n" % (len(result["skipped"]), ", ".join(result["skipped"])))
        return 2
    threshold = RANK[args.fail_on]
    return 1 if any(RANK[f["severity"]] >= threshold for f in result["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
