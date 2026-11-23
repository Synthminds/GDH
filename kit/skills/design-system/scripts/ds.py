#!/usr/bin/env python3
"""ds.py: design system tooling for the GDH design-system skill.

Subcommands: init, validate, from-css, from-dtcg, to-dtcg, export, contrast,
design-md, specimen, audit.

The canonical token file is the Claude Design System tokens.json shape:
  color: {"themes": [{"id", "name"}], "tokens": [{"name", "value", "usage"}]}
  type:  {"fonts": [...], "families": {key: stack},
          "groups": [{"name", "family", "styles": [{"name", "fontSize",
                      "lineHeight", "fontWeight"}]}]}
  every other family: {"tokens": [{"name", "value", "usage"}]}

Python 3.9+, standard library only. No network calls. Writes only the paths
given as arguments. Exit code 0 on pass and 1 on findings. --json prints one
JSON object on stdout.
"""

import argparse
import colorsys
import html
import json
import math
import os
import re
import sys
from collections import OrderedDict
from html.parser import HTMLParser

VERSION = "0.1.0"

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
ALIAS_RE = re.compile(r"^\{([^{}]+)\}$")
NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
LENGTH_RE = re.compile(r"^(" + NUM + r")(px|rem|em|%)?$")
ANY_LENGTH_RE = re.compile(r"^(" + NUM + r")([a-zA-Z%]*)$")
TIME_RE = re.compile(r"^(" + NUM + r")(ms|s)$")
HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
FUNC_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9-]*)\((.*)\)$", re.S)

# Caps read from the Design System type's format reference (see tokens-format.md).
CAPS = {"themes": 8, "colors": 600, "families": 12, "typeGroups": 12,
        "typeStyles": 80, "familyTokens": 60}

RESERVED_TOP = {"name", "version", "description", "meta", "$schema"}
LENGTH_FAMILIES = {"spacing", "radius"}

# Only the basic CSS color keywords are converted. Any other named color is
# reported, never guessed.
BASIC_NAMED = {
    "black": "#000000", "silver": "#c0c0c0", "gray": "#808080", "grey": "#808080",
    "white": "#ffffff", "maroon": "#800000", "red": "#ff0000", "purple": "#800080",
    "fuchsia": "#ff00ff", "green": "#008000", "lime": "#00ff00", "olive": "#808000",
    "yellow": "#ffff00", "navy": "#000080", "blue": "#0000ff", "teal": "#008080",
    "aqua": "#00ffff", "orange": "#ffa500", "rebeccapurple": "#663399",
    "transparent": "rgba(0, 0, 0, 0)",
}
CSS_WIDE = {"inherit", "initial", "unset", "revert", "currentcolor", "none", "auto"}


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def fmt_num(x, places=4):
    """Format a float without trailing zeros."""
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, int):
        return str(x)
    s = ("%." + str(places) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s


def read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh, object_pairs_hook=OrderedDict)


def write_text(path, text):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def head_marked(path):
    """True when the head of the file holds the note that ds.py writes into CSS and HTML outputs."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(600).decode("utf-8", "replace")
    except (IOError, OSError):
        return False
    return "ds.py" in head and ("Generated from" in head or 'name="generator" content="ds.py' in head)


def dtcg_owned(path):
    """True when the file is a DTCG file that to-dtcg wrote: its root $extensions.gdh names the format."""
    try:
        data = read_json(path)
    except (IOError, OSError, ValueError):
        return False
    ext = data.get("$extensions") if isinstance(data, dict) else None
    gdh = ext.get("gdh") if isinstance(ext, dict) else None
    return isinstance(gdh, dict) and gdh.get("format") == GDH_FORMAT


def flat_owned(ids):
    """Return a check: True when the file is a flat JSON of the export shape for these theme ids."""
    def check(path):
        try:
            data = read_json(path)
        except (IOError, OSError, ValueError):
            return False
        return isinstance(data, dict) and bool(data) and set(data) <= set(ids or ["default"]) and all(
            isinstance(v, dict) and all(not isinstance(x, (dict, list)) for x in v.values()) for v in data.values())
    return check


def never_owned(_path):
    """Token files are finished by hand (usage notes), so an existing one is never replaced silently."""
    return False


class WriteRefused(Exception):
    pass


def safe_write(path, writer, force=False, owner_check=None):
    """Write a file only when it is absent or ds.py wrote it. With force, copy the old file to
    <path>.bak first. Return the backup path or None. Raise WriteRefused otherwise."""
    if os.path.islink(path):
        raise WriteRefused("%s is a symbolic link; ds.py does not write through links" % path)
    if os.path.exists(path):
        if not os.path.isfile(path):
            raise WriteRefused("%s exists and is not a file" % path)
        owned = (owner_check or head_marked)(path)
        if not owned and not force:
            raise WriteRefused("%s exists and ds.py did not write it. Pass --force to replace a file ds.py "
                               "did not write; the old file is kept as %s.bak" % (path, path))
        if not owned:
            backup = path + ".bak"
            with open(path, "rb") as src, open(backup, "wb") as dst:
                dst.write(src.read())
            writer(path)
            return backup
    writer(path)
    return None


def write_json(path, obj):
    write_text(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def finding(code, level, path, message, hint):
    return OrderedDict([("code", code), ("level", level), ("path", path),
                        ("message", message), ("hint", hint)])


def has_errors(findings):
    return any(f["level"] == "error" for f in findings)


def match_paren(text, open_idx):
    """Return the index of the parenthesis that closes text[open_idx]."""
    depth = 0
    for i in range(open_idx, len(text)):
        ch = text[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def split_top(text, sep=","):
    """Split on a separator that is outside parentheses and quotes."""
    parts, depth, cur, quote = [], 0, [], None
    for ch in text:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            cur.append(ch)
        elif ch == "(":
            depth += 1
            cur.append(ch)
        elif ch == ")":
            depth -= 1
            cur.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def split_ws_top(text):
    """Split on whitespace that is outside parentheses and quotes."""
    parts, depth, cur, quote = [], 0, [], None
    for ch in text.strip():
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            cur.append(ch)
        elif ch == "(":
            depth += 1
            cur.append(ch)
        elif ch == ")":
            depth -= 1
            cur.append(ch)
        elif ch.isspace() and depth == 0:
            if cur:
                parts.append("".join(cur))
                cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return parts


# --------------------------------------------------------------------------
# Color math
# --------------------------------------------------------------------------

def _srgb_to_linear(c):
    sign = -1.0 if c < 0 else 1.0
    c = abs(c)
    if c <= 0.04045:
        return sign * c / 12.92
    return sign * ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c):
    sign = -1.0 if c < 0 else 1.0
    c = abs(c)
    if c <= 0.0031308:
        return sign * 12.92 * c
    return sign * (1.055 * (c ** (1.0 / 2.4)) - 0.055)


def _cbrt(x):
    return -((-x) ** (1.0 / 3.0)) if x < 0 else x ** (1.0 / 3.0)


def oklab_to_srgb(L, a, b):
    """OKLab to gamma-encoded sRGB. Components may fall outside 0..1."""
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return (_linear_to_srgb(r), _linear_to_srgb(g), _linear_to_srgb(bl))


def srgb_to_oklab(r, g, b):
    r, g, b = _srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = _cbrt(l), _cbrt(m), _cbrt(s)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def oklch_to_srgb(L, C, H):
    h = math.radians(H)
    return oklab_to_srgb(L, C * math.cos(h), C * math.sin(h))


def srgb_to_oklch(r, g, b):
    L, a, bb = srgb_to_oklab(r, g, b)
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360.0
    return (L, C, H)


def hsl_to_srgb(h, s, l):
    h = (h % 360.0) / 360.0
    if s == 0:
        return (l, l, l)
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q

    def chan(t):
        t = t % 1.0
        if t < 1.0 / 6:
            return p + (q - p) * 6 * t
        if t < 0.5:
            return q
        if t < 2.0 / 3:
            return p + (q - p) * (2.0 / 3 - t) * 6
        return p
    return (chan(h + 1.0 / 3), chan(h), chan(h - 1.0 / 3))


class Color(object):
    """A parsed color. rgb holds gamma-encoded sRGB floats, not clipped."""

    def __init__(self, rgb, alpha=1.0, kind="hex", native=None):
        self.rgb = tuple(rgb)
        self.alpha = max(0.0, min(1.0, alpha))
        self.kind = kind          # hex | rgb | hsl | oklch | oklab | named
        self.native = native      # (L, C, H) for oklch input

    @property
    def clipped(self):
        return any(c < -0.0005 or c > 1.0005 for c in self.rgb)

    def rgb01(self):
        return tuple(max(0.0, min(1.0, c)) for c in self.rgb)

    def rgb255(self):
        return tuple(int(round(c * 255)) for c in self.rgb01())

    def hex6(self):
        return "#%02x%02x%02x" % self.rgb255()

    def to_css(self):
        """A literal in sRGB: hex when opaque, rgba() otherwise."""
        if self.alpha >= 0.9995:
            return self.hex6()
        r, g, b = self.rgb255()
        return "rgba(%d, %d, %d, %s)" % (r, g, b, fmt_num(self.alpha, 3))

    def oklab(self):
        return srgb_to_oklab(*self.rgb)

    def oklch(self):
        if self.native is not None:
            return self.native
        return srgb_to_oklch(*self.rgb)

    def same_as(self, other, tol=0.002):
        return (all(abs(a - b) <= tol for a, b in zip(self.rgb, other.rgb))
                and abs(self.alpha - other.alpha) <= tol)


def _alpha_tok(tok):
    if tok is None:
        return 1.0
    tok = tok.strip().lower()
    if tok == "none":
        return 0.0
    if tok.endswith("%"):
        return float(tok[:-1]) / 100.0
    return float(tok)


def _hue_tok(tok):
    tok = tok.strip().lower()
    if tok == "none":
        return 0.0
    for unit, mult in (("deg", 1.0), ("grad", 0.9), ("rad", 180.0 / math.pi), ("turn", 360.0)):
        if tok.endswith(unit):
            return float(tok[:-len(unit)]) * mult
    return float(tok)


def _chan_args(body):
    """Split a color function body into channel tokens and an alpha token."""
    alpha = None
    if "/" in body:
        body, alpha = body.split("/", 1)
    parts = [p for p in re.split(r"[\s,]+", body.strip()) if p]
    if alpha is None and len(parts) == 4:
        alpha = parts.pop()
    return parts, alpha


def parse_color(value, allow_named=False):
    """Parse a color literal. Return a Color, or None when it is not one.

    Accepts hex (3, 4, 6, 8 digits), rgb(), rgba(), hsl(), hsla(), oklch() and
    oklab(). A function that nests another function is not a literal.
    """
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s:
        return None
    if HEX_RE.match(s):
        h = s[1:]
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255.0 if len(h) == 8 else 1.0
        return Color((r, g, b), a, "hex")
    low = s.lower()
    if allow_named and low in BASIC_NAMED:
        c = parse_color(BASIC_NAMED[low])
        c.kind = "named"
        return c
    m = FUNC_RE.match(s)
    if not m:
        return None
    fn, body = m.group(1).lower(), m.group(2)
    if "(" in body or ")" in body:
        return None
    try:
        parts, alpha = _chan_args(body)
        if len(parts) != 3:
            return None
        a = _alpha_tok(alpha)
        if fn in ("rgb", "rgba"):
            chans = []
            for p in parts:
                p = p.lower()
                if p == "none":
                    chans.append(0.0)
                elif p.endswith("%"):
                    chans.append(float(p[:-1]) / 100.0)
                else:
                    chans.append(float(p) / 255.0)
            return Color(chans, a, "rgb")
        if fn in ("hsl", "hsla"):
            h = _hue_tok(parts[0])
            sat = float(parts[1].rstrip("%")) / 100.0
            lig = float(parts[2].rstrip("%")) / 100.0
            return Color(hsl_to_srgb(h, max(0.0, min(1.0, sat)), max(0.0, min(1.0, lig))), a, "hsl")
        if fn == "oklch":
            L = _pct(parts[0], 1.0)
            C = _pct(parts[1], 0.4)
            H = _hue_tok(parts[2])
            return Color(oklch_to_srgb(L, C, H), a, "oklch", native=(L, C, H % 360.0))
        if fn == "oklab":
            L = _pct(parts[0], 1.0)
            aa = _pct(parts[1], 0.4)
            bb = _pct(parts[2], 0.4)
            return Color(oklab_to_srgb(L, aa, bb), a, "oklab")
    except (ValueError, IndexError):
        return None
    return None


def _pct(tok, scale):
    tok = tok.strip().lower()
    if tok == "none":
        return 0.0
    if tok.endswith("%"):
        return float(tok[:-1]) / 100.0 * scale
    return float(tok)


def relative_luminance(rgb):
    """WCAG 2.x relative luminance of gamma-encoded sRGB in 0..1."""
    out = []
    for c in rgb:
        c = max(0.0, min(1.0, c))
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def composite(fg, bg_rgb):
    """Composite a color with alpha over an opaque ground."""
    a = fg.alpha
    f = fg.rgb01()
    return tuple(f[i] * a + bg_rgb[i] * (1 - a) for i in range(3))


def contrast_ratio(fg, bg):
    """WCAG 2.x contrast ratio of two Color objects. bg must be opaque."""
    bg_rgb = bg.rgb01()
    fg_rgb = composite(fg, bg_rgb)
    l1, l2 = relative_luminance(fg_rgb), relative_luminance(bg_rgb)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------------------
# color-mix()
# --------------------------------------------------------------------------

_MIX_PCT = re.compile(r"^(" + NUM + r")%$")


def _mix_arg(arg):
    """Split one color-mix argument into (color text, percentage or None)."""
    toks = split_ws_top(arg)
    pct = None
    rest = []
    for t in toks:
        m = _MIX_PCT.match(t)
        if m and pct is None:
            pct = float(m.group(1))
        else:
            rest.append(t)
    return " ".join(rest), pct


def mix_colors(space, c1, p1, c2, p2, hue_method="shorter"):
    """Mix two Color objects the way CSS color-mix() does.

    Return (Color, None) or (None, reason).
    """
    if p1 is None and p2 is None:
        p1 = p2 = 50.0
    elif p1 is None:
        p1 = 100.0 - p2
    elif p2 is None:
        p2 = 100.0 - p1
    total = p1 + p2
    if total <= 0:
        return None, "percentages sum to zero"
    alpha_mult = min(1.0, total / 100.0)
    w1, w2 = p1 / total, p2 / total
    a1, a2 = c1.alpha, c2.alpha
    alpha = a1 * w1 + a2 * w2

    def premix(x1, x2):
        if alpha <= 0:
            return 0.0
        return (x1 * a1 * w1 + x2 * a2 * w2) / alpha

    if space == "srgb":
        rgb = tuple(premix(c1.rgb[i], c2.rgb[i]) for i in range(3))
        return Color(rgb, alpha * alpha_mult, "rgb"), None
    if space == "srgb-linear":
        lin1 = [_srgb_to_linear(c) for c in c1.rgb]
        lin2 = [_srgb_to_linear(c) for c in c2.rgb]
        rgb = tuple(_linear_to_srgb(premix(lin1[i], lin2[i])) for i in range(3))
        return Color(rgb, alpha * alpha_mult, "rgb"), None
    if space == "oklab":
        l1, l2 = c1.oklab(), c2.oklab()
        lab = tuple(premix(l1[i], l2[i]) for i in range(3))
        return Color(oklab_to_srgb(*lab), alpha * alpha_mult, "oklab"), None
    if space == "oklch":
        if hue_method != "shorter":
            return None, "hue method '%s' is not supported" % hue_method
        L1, C1, H1 = c1.oklch()
        L2, C2, H2 = c2.oklch()
        # A color with no chroma or no opacity has no hue of its own.
        miss1 = C1 < 1e-4 or a1 <= 0
        miss2 = C2 < 1e-4 or a2 <= 0
        if miss1 and miss2:
            H = 0.0
        elif miss1:
            H = H2
        elif miss2:
            H = H1
        else:
            d = H2 - H1
            if d > 180:
                d -= 360
            elif d < -180:
                d += 360
            H = (H1 + d * w2) % 360.0
        if a1 <= 0:
            L, C = L2, C2
        elif a2 <= 0:
            L, C = L1, C1
        else:
            L, C = premix(L1, L2), premix(C1, C2)
        return Color(oklch_to_srgb(L, C, H), alpha * alpha_mult, "oklch", native=(L, C, H)), None
    return None, "color space '%s' is not supported" % space


def resolve_color_mix(text):
    """Replace every color-mix() in text with a literal sRGB color.

    Return (new text, list of (expression, literal), error or None).
    """
    computed = []
    guard = 0
    while True:
        guard += 1
        if guard > 50:
            return text, computed, "color-mix() nesting is too deep"
        low = text.lower()
        idx = low.rfind("color-mix(")
        if idx < 0:
            return text, computed, None
        close = match_paren(text, idx + len("color-mix"))
        if close < 0:
            return text, computed, "unbalanced parentheses in color-mix()"
        expr = text[idx:close + 1]
        inner = text[idx + len("color-mix("):close]
        args = [a.strip() for a in split_top(inner)]
        if len(args) != 3:
            return text, computed, "color-mix() needs a color space and two colors"
        head = args[0].lower().split()
        if len(head) < 2 or head[0] != "in":
            return text, computed, "color-mix() has no 'in <space>' part"
        space = head[1]
        hue_method = "shorter"
        if len(head) >= 4 and head[-1] == "hue":
            hue_method = head[2]
        cols = []
        for arg in args[1:]:
            ctext, pct = _mix_arg(arg)
            col = parse_color(ctext, allow_named=True)
            if col is None:
                return text, computed, "color-mix() operand '%s' is not a literal color" % ctext
            cols.append((col, pct))
        result, err = mix_colors(space, cols[0][0], cols[0][1], cols[1][0], cols[1][1], hue_method)
        if result is None:
            return text, computed, err
        literal = result.to_css()
        computed.append((expr, literal))
        text = text[:idx] + literal + text[close + 1:]


# --------------------------------------------------------------------------
# calc() for single-unit expressions
# --------------------------------------------------------------------------

_CALC_TOK = re.compile(r"\s*(?:(" + NUM + r")([a-zA-Z%]*)|([-+*/()]))")


def eval_calc(expr):
    """Evaluate a calc() body that uses one unit. Return 'value+unit' or None."""
    toks = []
    pos = 0
    expr = expr.strip()
    while pos < len(expr):
        m = _CALC_TOK.match(expr, pos)
        if not m:
            return None
        if m.group(3):
            toks.append(m.group(3))
        else:
            toks.append((float(m.group(1)), m.group(2)))
        pos = m.end()
    state = {"i": 0}

    def peek():
        return toks[state["i"]] if state["i"] < len(toks) else None

    def take():
        t = peek()
        state["i"] += 1
        return t

    def atom():
        t = take()
        if t == "(":
            v = add()
            if take() != ")":
                raise ValueError("paren")
            return v
        if t == "-":
            v = atom()
            return (-v[0], v[1])
        if isinstance(t, tuple):
            return t
        raise ValueError("token")

    def mul():
        v = atom()
        while peek() in ("*", "/"):
            op = take()
            r = atom()
            if op == "*":
                if v[1] and r[1]:
                    raise ValueError("unit * unit")
                v = (v[0] * r[0], v[1] or r[1])
            else:
                if r[1] or r[0] == 0:
                    raise ValueError("divide by unit")
                v = (v[0] / r[0], v[1])
        return v

    def add():
        v = mul()
        while peek() in ("+", "-"):
            op = take()
            r = mul()
            if v[1] != r[1]:
                raise ValueError("mixed units")
            v = (v[0] + r[0] if op == "+" else v[0] - r[0], v[1])
        return v

    try:
        val = add()
        if state["i"] != len(toks):
            return None
    except (ValueError, TypeError, IndexError):
        return None
    return fmt_num(val[0], 4) + val[1]


def resolve_calc(text):
    """Replace calc() parts that reduce to one value. Return (text, ok)."""
    guard = 0
    while "calc(" in text.lower():
        guard += 1
        if guard > 20:
            return text, False
        idx = text.lower().rfind("calc(")
        close = match_paren(text, idx + 4)
        if close < 0:
            return text, False
        val = eval_calc(text[idx + 5:close])
        if val is None:
            return text, False
        text = text[:idx] + val + text[close + 1:]
    return text, True


# --------------------------------------------------------------------------
# Token document access
# --------------------------------------------------------------------------

def family_keys(doc):
    """Top-level keys that hold token families, in file order."""
    return [k for k, v in doc.items()
            if k not in RESERVED_TOP and isinstance(v, (dict, list))]


def theme_ids(doc):
    color = doc.get("color")
    if not isinstance(color, dict):
        return []
    out = []
    for t in color.get("themes") or []:
        if isinstance(t, dict) and isinstance(t.get("id"), str):
            out.append(t["id"])
    return out


def color_tokens(doc):
    color = doc.get("color")
    if not isinstance(color, dict) or not isinstance(color.get("tokens"), list):
        return []
    return [t for t in color["tokens"] if isinstance(t, dict) and isinstance(t.get("name"), str)]


def color_raw(token, theme):
    """The raw value of a color token in one theme, or None."""
    v = token.get("value")
    if isinstance(v, dict):
        return v.get(theme)
    return v


def resolve_color(doc, name, theme, _seen=None):
    """Follow aliases. Return (Color or None, literal text or None, error or None)."""
    index = {t["name"]: t for t in color_tokens(doc)}
    seen = _seen or []
    cur = name
    while True:
        if cur in seen:
            return None, None, "alias cycle: " + " -> ".join(seen + [cur])
        seen.append(cur)
        tok = index.get(cur)
        if tok is None:
            return None, None, "no color token named '%s'" % cur
        raw = color_raw(tok, theme)
        if raw is None:
            return None, None, "token '%s' has no value in theme '%s'" % (cur, theme)
        if not isinstance(raw, str):
            return None, None, "token '%s' value is not a string" % cur
        m = ALIAS_RE.match(raw.strip())
        if m:
            cur = m.group(1).strip()
            continue
        col = parse_color(raw)
        if col is None:
            return None, raw, "value '%s' is not a color literal" % raw
        return col, raw.strip(), None


def list_family_tokens(doc, fam):
    block = doc.get(fam)
    if isinstance(block, dict) and isinstance(block.get("tokens"), list):
        return [t for t in block["tokens"] if isinstance(t, dict)]
    return []


def type_styles(doc):
    """Yield (group, style) pairs of the type family."""
    typ = doc.get("type")
    if not isinstance(typ, dict):
        return
    for g in typ.get("groups") or []:
        if not isinstance(g, dict):
            continue
        for s in g.get("styles") or []:
            if isinstance(s, dict):
                yield g, s


# --------------------------------------------------------------------------
# validate
# --------------------------------------------------------------------------

def _looks_like_dtcg(block):
    """True when a family block is a name-to-value map instead of a list."""
    if not isinstance(block, dict):
        return False
    if isinstance(block.get("tokens"), list):
        return False
    stack = [block]
    while stack:
        node = stack.pop()
        if not isinstance(node, dict):
            continue
        if "$value" in node or "$type" in node:
            return True
        if "value" in node and not isinstance(node.get("value"), (dict, list)):
            return True
        stack.extend(v for v in node.values() if isinstance(v, dict))
    return False


def _check_scalar_value(value):
    return isinstance(value, (str, int, float)) and not isinstance(value, bool)


def _is_length(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    return isinstance(value, str) and bool(LENGTH_RE.match(value.strip()))


def _check_color_literal(raw, path, names, self_name, out):
    """Check one color value string. Append findings to out."""
    s = raw.strip()
    low = s.lower()
    m = ALIAS_RE.match(s)
    if m:
        target = m.group(1).strip()
        if target == self_name:
            out.append(finding("COLOR_ALIAS_SELF", "error", path,
                               "The token aliases itself.",
                               "Point the alias at another color token or write a literal color."))
        elif target not in names:
            out.append(finding("COLOR_ALIAS_MISSING", "error", path,
                               "Alias target '%s' is not a color token. The page drops this value." % target,
                               "Add a color token named '%s' or fix the alias name." % target))
        return
    if "{" in s or "}" in s:
        out.append(finding("COLOR_ALIAS_SYNTAX", "error", path,
                           "The value '%s' is not a whole alias." % s,
                           "Write the alias as \"{token-name}\" with nothing around it."))
        return
    if "var(" in low:
        out.append(finding("COLOR_VAR", "error", path,
                           "var() is not read by the page. The value drops.",
                           "Write an alias \"{token-name}\" or the literal color. Run from-css to resolve var() chains."))
        return
    if "color-mix(" in low:
        out.append(finding("COLOR_MIX", "error", path,
                           "color-mix() is not read by the page. The value drops.",
                           "Write the mixed result as a literal color. Run from-css to compute it."))
        return
    if HEX_RE.match(s):
        return
    fm = FUNC_RE.match(s)
    if fm:
        fn, body = fm.group(1).lower(), fm.group(2)
        if "(" in body:
            out.append(finding("COLOR_NESTED_FUNCTION", "error", path,
                               "The color function nests another function.",
                               "Write plain numbers inside %s()." % fn))
            return
        if fn in ("rgb", "rgba", "hsl", "hsla", "oklch"):
            if parse_color(s) is None:
                out.append(finding("COLOR_SYNTAX", "error", path,
                                   "'%s' does not parse as %s()." % (s, fn),
                                   "Give three channels and an optional alpha."))
            return
        out.append(finding("COLOR_FUNCTION_UNLISTED", "warning", path,
                           "%s() is not on the documented list of accepted color values." % fn,
                           "Convert it to hex, rgb(), hsl() or oklch()."))
        return
    if s.startswith("#"):
        out.append(finding("COLOR_HEX", "error", path,
                           "'%s' is not a hex color." % s,
                           "Use 3, 4, 6 or 8 hex digits after #."))
        return
    if re.match(r"^[a-zA-Z]+$", s):
        out.append(finding("COLOR_NAMED", "error", path,
                           "Named color '%s' is not read by the page. The value drops." % s,
                           "Write the color as hex."))
        return
    out.append(finding("COLOR_VALUE", "error", path,
                       "'%s' is not an accepted color value." % s,
                       "Use hex, rgb(), rgba(), hsl(), oklch() or an alias \"{token-name}\"."))


def _alias_cycles(doc, out):
    themes = theme_ids(doc) or [None]
    toks = color_tokens(doc)
    index = {t["name"]: t for t in toks}
    reported = set()
    for i, tok in enumerate(toks):
        for th in themes:
            seen = [tok["name"]]
            cur = tok
            while True:
                raw = color_raw(cur, th) if th is not None else cur.get("value")
                if not isinstance(raw, str):
                    break
                m = ALIAS_RE.match(raw.strip())
                if not m:
                    break
                nxt = m.group(1).strip()
                if nxt == seen[-1] or nxt not in index:
                    break
                if nxt in seen:
                    key = tuple(sorted(seen))
                    if key not in reported:
                        reported.add(key)
                        out.append(finding("COLOR_ALIAS_CYCLE", "error", "color.tokens[%d]" % i,
                                           "Aliases form a cycle: %s." % " -> ".join(seen + [nxt]),
                                           "Give one token in the cycle a literal color."))
                    break
                seen.append(nxt)
                cur = index[nxt]


def validate_doc(doc):
    """Check a tokens document against the Claude Design System grammar."""
    out = []
    if not isinstance(doc, dict):
        return [finding("ROOT_NOT_OBJECT", "error", "$", "The file is not a JSON object.",
                        "Write an object with color, type and other families.")]
    fams = family_keys(doc)
    if not fams:
        out.append(finding("NO_FAMILIES", "error", "$", "The file holds no token family.",
                           "Add at least a color family. Run init to scaffold one."))
    if len(fams) > CAPS["families"]:
        out.append(finding("CAP_FAMILIES", "error", "$",
                           "%d families. The cap is %d." % (len(fams), CAPS["families"]),
                           "Merge small families."))
    if "$value" in doc or any(isinstance(v, dict) and "$value" in v for v in doc.values()):
        pass  # reported per family below
    names_seen = {}

    def check_name(name, path):
        if not isinstance(name, str) or not NAME_RE.match(name):
            out.append(finding("NAME_INVALID", "error", path,
                               "Name %r does not match [A-Za-z0-9][A-Za-z0-9_.-]{0,63}." % (name,),
                               "Start with a letter or digit. Use letters, digits, dot, dash and underscore. 64 characters at most."))
            return
        if name in names_seen:
            out.append(finding("NAME_DUPLICATE", "error", path,
                               "Name '%s' is already used at %s." % (name, names_seen[name]),
                               "Names are unique across all families except type. Rename one token."))
        else:
            names_seen[name] = path

    def check_usage(tok, path):
        usage = tok.get("usage")
        if not isinstance(usage, str) or not usage.strip():
            out.append(finding("USAGE_MISSING", "warning", path,
                               "The token has no usage note.",
                               "Add a usage note that says where the token is used. A text color names the grounds it reads on."))

    for fam in fams:
        block = doc[fam]
        if isinstance(block, list):
            out.append(finding("FAMILY_SHAPE", "error", fam,
                               "The family is a bare list.",
                               "Wrap it: {\"tokens\": [...]}."))
            continue
        if fam != "type" and _looks_like_dtcg(block):
            out.append(finding("DTCG_MAP", "error", fam,
                               "The family is a name-to-value map (DTCG or W3C style). The page cannot read it: "
                               "the family shows empty and its entries are lost at the first token edit.",
                               "Convert it to a list with: ds.py from-dtcg <file> -o tokens.json"))
            continue
        if fam == "type":
            _validate_type(block, out)
            continue
        toks = block.get("tokens")
        if not isinstance(toks, list):
            out.append(finding("FAMILY_SHAPE", "error", fam,
                               "The family has no \"tokens\" list.",
                               "Use {\"tokens\": [{\"name\", \"value\", \"usage\"}]}."))
            continue
        if fam == "color":
            _validate_color(doc, block, out, check_name, check_usage)
            continue
        if len(toks) > CAPS["familyTokens"]:
            out.append(finding("CAP_FAMILY_TOKENS", "error", fam,
                               "%d tokens. The cap for this family is %d." % (len(toks), CAPS["familyTokens"]),
                               "Remove unused tokens or split the family."))
        if "themes" in block:
            out.append(finding("THEMES_OUTSIDE_COLOR", "warning", fam,
                               "Only the color family holds themes.",
                               "Remove \"themes\" from this family."))
        for i, tok in enumerate(toks):
            path = "%s.tokens[%d]" % (fam, i)
            if not isinstance(tok, dict):
                out.append(finding("TOKEN_SHAPE", "error", path, "The token is not an object.",
                                   "Use {\"name\", \"value\", \"usage\"}."))
                continue
            check_name(tok.get("name"), path)
            check_usage(tok, path)
            val = tok.get("value")
            if isinstance(val, dict):
                out.append(finding("VALUE_PER_THEME_OUTSIDE_COLOR", "warning", path,
                                   "A per-theme value is documented for color only.",
                                   "Use one value, or add one token for each theme."))
                continue
            if not _check_scalar_value(val) or (isinstance(val, str) and not val.strip()):
                out.append(finding("VALUE_MISSING", "error", path, "The token has no value.",
                                   "Give a string or a number."))
                continue
            if isinstance(val, str):
                low = val.lower()
                if "var(" in low:
                    out.append(finding("VALUE_VAR", "error", path,
                                       "var() is not read by the page.",
                                       "Write the resolved value. Run from-css to resolve var() chains."))
                    continue
                if "color-mix(" in low:
                    out.append(finding("VALUE_COLOR_MIX", "error", path,
                                       "color-mix() is not read by the page.",
                                       "Write the mixed result as a literal color."))
                    continue
            if fam in LENGTH_FAMILIES and not _is_length(val):
                out.append(finding("LENGTH_INVALID", "error", path,
                                   "'%s' is not a length in px, rem, em or %%, or a number." % val,
                                   "Write a value such as 8px, 0.5rem or 50%."))
    return out


SCAFFOLD_SHARE = 0.5   # Default: half or more of the starter colors unchanged means the scaffold is the brand.


def scaffold_findings(doc):
    """Warn when the starter colors from init are still in place: the scaffold is not a brand."""
    if not isinstance(doc, dict):
        return []
    starter = OrderedDict((t["name"], t["value"]) for t in starter_tokens("x")["color"]["tokens"])
    same = [t.get("name") for t in color_tokens(doc)
            if isinstance(t, dict) and t.get("name") in starter and _same_json(t.get("value"), starter[t["name"]])]
    if not same or len(same) < SCAFFOLD_SHARE * len(starter):
        return []
    return [finding("DS_SCAFFOLD_VALUE", "warning", "color",
                    "%d of %d starter colors from init are unchanged: %s." % (len(same), len(starter), ", ".join(same)),
                    "Replace each starter value with a choice from the brief, or confirm it with the owner and "
                    "record the decision. The scaffold is not a brand.")]


def _validate_color(doc, block, out, check_name, check_usage):
    themes = block.get("themes")
    ids = []
    if not isinstance(themes, list) or not themes:
        out.append(finding("THEMES_MISSING", "error", "color.themes",
                           "The color family has no themes list.",
                           "Add \"themes\": [{\"id\": \"light\", \"name\": \"Light\"}]."))
    else:
        if len(themes) > CAPS["themes"]:
            out.append(finding("CAP_THEMES", "error", "color.themes",
                               "%d themes. The cap is %d." % (len(themes), CAPS["themes"]),
                               "Remove a theme."))
        for i, th in enumerate(themes):
            path = "color.themes[%d]" % i
            if not isinstance(th, dict) or not isinstance(th.get("id"), str) or not th.get("id"):
                out.append(finding("THEME_SHAPE", "error", path, "The theme has no id.",
                                   "Use {\"id\": \"dark\", \"name\": \"Dark\"}."))
                continue
            if th["id"] in ids:
                out.append(finding("THEME_DUPLICATE", "error", path,
                                   "Theme id '%s' is used twice." % th["id"], "Rename one theme."))
            ids.append(th["id"])
            if not isinstance(th.get("name"), str) or not th.get("name"):
                out.append(finding("THEME_NAME_MISSING", "warning", path,
                                   "The theme has no display name.", "Add \"name\"."))
    toks = block.get("tokens")
    if len(toks) > CAPS["colors"]:
        out.append(finding("CAP_COLORS", "error", "color.tokens",
                           "%d colors. The cap is %d." % (len(toks), CAPS["colors"]),
                           "Remove unused colors."))
    names = set(t.get("name") for t in toks if isinstance(t, dict) and isinstance(t.get("name"), str))
    for i, tok in enumerate(toks):
        path = "color.tokens[%d]" % i
        if not isinstance(tok, dict):
            out.append(finding("TOKEN_SHAPE", "error", path, "The token is not an object.",
                               "Use {\"name\", \"value\", \"usage\"}."))
            continue
        name = tok.get("name")
        check_name(name, path)
        check_usage(tok, path)
        val = tok.get("value")
        if isinstance(val, str):
            if not val.strip():
                out.append(finding("VALUE_MISSING", "error", path, "The color has no value.",
                                   "Give a color literal or an alias."))
            else:
                _check_color_literal(val, path, names, name, out)
        elif isinstance(val, dict):
            for key, sub in val.items():
                spath = "%s.value.%s" % (path, key)
                if ids and key not in ids:
                    out.append(finding("COLOR_THEME_UNKNOWN", "error", spath,
                                       "'%s' is not a theme id." % key,
                                       "Use one of: %s." % ", ".join(ids)))
                if not isinstance(sub, str) or not sub.strip():
                    out.append(finding("VALUE_MISSING", "error", spath, "The theme value is empty.",
                                       "Give a color literal or an alias."))
                else:
                    _check_color_literal(sub, spath, names, name, out)
            for tid in ids:
                if tid not in val:
                    out.append(finding("COLOR_THEME_VALUE_MISSING", "warning", "%s.value" % path,
                                       "No value for theme '%s'." % tid,
                                       "Fill every theme, or use one string for all themes."))
        else:
            out.append(finding("VALUE_MISSING", "error", path, "The color has no value.",
                               "Give a string or a per-theme object."))
    _alias_cycles(doc, out)


def _validate_type(block, out):
    if not isinstance(block, dict):
        out.append(finding("TYPE_SHAPE", "error", "type", "The type family is not an object.",
                           "Use {\"fonts\": [], \"families\": {}, \"groups\": []}."))
        return
    if isinstance(block.get("tokens"), list) or _looks_like_dtcg(block):
        out.append(finding("TYPE_SHAPE", "error", "type",
                           "The type family is not a token list or a name-to-value map.",
                           "Use {\"fonts\": [...], \"families\": {key: stack}, \"groups\": [{\"name\", \"family\", \"styles\": [...]}]}."))
        return
    fonts = block.get("fonts", [])
    if not isinstance(fonts, list):
        out.append(finding("TYPE_FONTS_SHAPE", "error", "type.fonts", "fonts is not a list.",
                           "Use a list of {\"family\", \"file\", \"weight\", \"style\"}."))
        fonts = []
    for i, f in enumerate(fonts):
        path = "type.fonts[%d]" % i
        if not isinstance(f, dict) or not isinstance(f.get("family"), str) or not f.get("family"):
            out.append(finding("TYPE_FONT_SHAPE", "error", path, "The font has no family name.",
                               "Add \"family\"."))
            continue
        if not isinstance(f.get("file"), str) or not f.get("file"):
            out.append(finding("TYPE_FONT_FILE_MISSING", "warning", path,
                               "Font '%s' names no file. A named font without a file gets replaced." % f["family"],
                               "Add the font file under fonts/ and set \"file\"."))
    families = block.get("families")
    if not isinstance(families, dict) or not families:
        out.append(finding("TYPE_FAMILIES_MISSING", "error", "type.families",
                           "The type family has no families map.",
                           "Add \"families\": {\"sans\": \"<font stack>\"}."))
        families = {}
    for key, stack in families.items():
        if not isinstance(stack, str) or not stack.strip():
            out.append(finding("TYPE_FAMILY_STACK", "error", "type.families.%s" % key,
                               "The family has no font stack.", "Give a CSS font-family stack."))
        elif "var(" in stack.lower():
            out.append(finding("VALUE_VAR", "error", "type.families.%s" % key,
                               "var() is not read by the page.", "Write the font stack."))
    groups = block.get("groups")
    if not isinstance(groups, list) or not groups:
        out.append(finding("TYPE_GROUPS_MISSING", "error", "type.groups",
                           "The type family has no groups list.",
                           "Add \"groups\": [{\"name\", \"family\", \"styles\": [...]}]."))
        return
    if len(groups) > CAPS["typeGroups"]:
        out.append(finding("CAP_TYPE_GROUPS", "error", "type.groups",
                           "%d groups. The cap is %d." % (len(groups), CAPS["typeGroups"]),
                           "Merge groups."))
    total = 0
    seen_styles = {}
    for gi, g in enumerate(groups):
        gpath = "type.groups[%d]" % gi
        if not isinstance(g, dict):
            out.append(finding("TYPE_GROUP_SHAPE", "error", gpath, "The group is not an object.",
                               "Use {\"name\", \"family\", \"styles\": [...]}."))
            continue
        if not isinstance(g.get("name"), str) or not g.get("name"):
            out.append(finding("TYPE_GROUP_NAME", "error", gpath, "The group has no name.", "Add \"name\"."))
        fam = g.get("family")
        if not isinstance(fam, str) or fam not in families:
            out.append(finding("TYPE_GROUP_FAMILY", "error", gpath + ".family",
                               "Group family %r is not a key of type.families." % (fam,),
                               "Use one of: %s." % (", ".join(families.keys()) or "(add a family first)")))
        styles = g.get("styles")
        if not isinstance(styles, list) or not styles:
            out.append(finding("TYPE_STYLES_MISSING", "error", gpath + ".styles",
                               "The group has no styles.",
                               "Add styles: {\"name\", \"fontSize\", \"lineHeight\", \"fontWeight\"}."))
            continue
        for si, s in enumerate(styles):
            spath = "%s.styles[%d]" % (gpath, si)
            total += 1
            if not isinstance(s, dict):
                out.append(finding("TYPE_STYLE_SHAPE", "error", spath, "The style is not an object.",
                                   "Use {\"name\", \"fontSize\", \"lineHeight\", \"fontWeight\"}."))
                continue
            name = s.get("name")
            if not isinstance(name, str) or not NAME_RE.match(name):
                out.append(finding("NAME_INVALID", "error", spath,
                                   "Style name %r does not match [A-Za-z0-9][A-Za-z0-9_.-]{0,63}." % (name,),
                                   "Rename the style."))
            elif name in seen_styles:
                out.append(finding("TYPE_STYLE_DUPLICATE", "error", spath,
                                   "Style name '%s' is already used at %s." % (name, seen_styles[name]),
                                   "Style names are unique inside the type family."))
            else:
                seen_styles[name] = spath
            fs = s.get("fontSize")
            if fs is None:
                out.append(finding("TYPE_FONT_SIZE_MISSING", "error", spath, "The style has no fontSize.",
                                   "Add a length such as 16px or 1rem."))
            elif not _is_length(fs):
                out.append(finding("TYPE_FONT_SIZE", "error", spath + ".fontSize",
                                   "'%s' is not a length in px, rem, em or %%, or a number." % fs,
                                   "Write a value such as 16px or 1rem."))
            lh = s.get("lineHeight")
            if lh is None:
                out.append(finding("TYPE_LINE_HEIGHT_MISSING", "warning", spath,
                                   "The style has no lineHeight.", "Add a number such as 1.5 or a length."))
            elif not _is_length(lh):
                out.append(finding("TYPE_LINE_HEIGHT", "error", spath + ".lineHeight",
                                   "'%s' is not a number or a length." % lh, "Write a value such as 1.5."))
            fw = s.get("fontWeight")
            if fw is None:
                out.append(finding("TYPE_FONT_WEIGHT_MISSING", "warning", spath,
                                   "The style has no fontWeight.", "Add a weight from 1 to 1000."))
            else:
                ok = False
                if isinstance(fw, (int, float)) and not isinstance(fw, bool):
                    ok = 1 <= fw <= 1000
                elif isinstance(fw, str):
                    ok = fw.strip().lower() in ("normal", "bold") or (
                        fw.strip().isdigit() and 1 <= int(fw.strip()) <= 1000)
                if not ok:
                    out.append(finding("TYPE_FONT_WEIGHT", "error", spath + ".fontWeight",
                                       "'%s' is not a font weight." % fw,
                                       "Use a number from 1 to 1000, or normal or bold."))
            ls = s.get("letterSpacing")
            if ls is not None and not _is_length(ls) and not (isinstance(ls, str) and ls.strip() == "normal"):
                out.append(finding("TYPE_LETTER_SPACING", "error", spath + ".letterSpacing",
                                   "'%s' is not a length." % ls, "Write a value such as 0.05em."))
            if not isinstance(s.get("usage"), str) or not s.get("usage").strip():
                out.append(finding("USAGE_MISSING", "warning", spath,
                                   "The style has no usage note.",
                                   "Say where the style is used."))
    if total > CAPS["typeStyles"]:
        out.append(finding("CAP_TYPE_STYLES", "error", "type.groups",
                           "%d styles. The cap is %d." % (total, CAPS["typeStyles"]),
                           "Remove unused styles."))


# --------------------------------------------------------------------------
# CSS reading (from-css)
# --------------------------------------------------------------------------

_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
_MARK_RE = re.compile(r"\x00(\d+)\x00")


def _mask_comments(text):
    comments = []

    def repl(m):
        comments.append(m.group(0)[2:-2].strip())
        return "\x00%d\x00" % (len(comments) - 1)
    return _COMMENT_RE.sub(repl, text), comments


def _find_block_end(text, open_idx):
    depth, quote = 0, None
    i = open_idx
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 1
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _iter_rules(text):
    """Yield (prelude, body or None) for each rule or statement at one level."""
    i, n = 0, len(text)
    start = 0
    quote = None
    depth = 0
    while i < n:
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 1
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == ";" and depth == 0:
            yield text[start:i], None, i
            start = i + 1
        elif ch == "{" and depth == 0:
            end = _find_block_end(text, i)
            if end < 0:
                return
            yield text[start:i], text[i + 1:end], end
            i = end
            start = end + 1
        i += 1
    tail = text[start:]
    if tail.strip():
        yield tail, None, n


def _clean(text):
    return _MARK_RE.sub(" ", text).strip()


_THEME_ATTR = re.compile(
    r"\[\s*(?:data-(?:theme|mode|color-scheme|color-mode|bs-theme|scheme)|theme|color-scheme)\s*[~|^$*]?=\s*[\"']?([A-Za-z0-9_-]+)[\"']?\s*\]")
_THEME_CLASS = re.compile(r"\.(dark|light)(?![A-Za-z0-9_-])|\.theme-([A-Za-z0-9_-]+)|\.([A-Za-z0-9_]+)-theme(?![A-Za-z0-9_-])|\.(?:dark|light)-mode")
_ROOTISH = re.compile(r":root|:host|\bhtml\b|\bbody\b|\*|:where\(\s*\)|:is\(\s*\)|&")


def _selector_scope(selector):
    """Classify one selector. Return ('base', None), ('theme', id) or ('skip', None)."""
    results = []
    for part in split_top(selector):
        part = part.strip()
        if not part:
            continue
        work = re.sub(r":not\([^()]*(?:\([^()]*\))?[^()]*\)", "", part)
        work = re.sub(r":(?:where|is)\(([^()]*)\)", r"\1", work)
        tid = None
        m = _THEME_ATTR.search(work)
        if m:
            tid = m.group(1)
            work = _THEME_ATTR.sub("", work)
        m = _THEME_CLASS.search(work)
        if m:
            if tid is None:
                tid = m.group(1) or m.group(2) or m.group(3)
                if tid is None:
                    tid = "dark" if "dark" in m.group(0) else "light"
            work = _THEME_CLASS.sub("", work)
        rest = _ROOTISH.sub("", work)
        rest = re.sub(r"[\s>+~,]", "", rest)
        if rest:
            results.append(("skip", None))
        elif tid:
            results.append(("theme", tid.lower()))
        else:
            results.append(("base", None))
    return results


def _context_scope(contexts):
    """Return (theme id or None, skip reason or None) for the at-rule stack."""
    theme = None
    for ctx in contexts:
        low = ctx.lower()
        if low.startswith("@media"):
            m = re.search(r"prefers-color-scheme\s*:\s*(dark|light)", low)
            if m:
                theme = m.group(1)
                rest = re.sub(r"\(?\s*prefers-color-scheme\s*:\s*(dark|light)\s*\)?", "", low[6:])
                rest = rest.replace("screen", "").replace("all", "").replace("and", "").strip(" ()")
                if rest:
                    return None, "inside %s" % ctx.strip()
            else:
                return None, "inside %s" % ctx.strip()
        elif low.startswith(("@supports", "@layer", "@scope")):
            continue
        elif low.startswith("@container"):
            return None, "inside %s" % ctx.strip()
    return theme, None


def _declarations(body, comments):
    """Yield (property, value, usage) for declarations at the top of a block."""
    pieces = []
    for prelude, sub, _end in _iter_rules(body):
        if sub is None:
            pieces.append(prelude)
        else:
            pieces.append(None)  # a nested rule ends any trailing-comment link
    prev = None
    out = []
    for piece in pieces:
        if piece is None:
            prev = None
            continue
        # A comment on the same line, right after the previous declaration, is its usage note.
        lead = piece.split("\n", 1)[0]
        m = _MARK_RE.search(lead)
        if m and prev is not None and not _MARK_RE.sub("", lead[:m.start()]).strip():
            out[prev] = (out[prev][0], out[prev][1], comments[int(m.group(1))])
        text = _clean(piece)
        if ":" not in text:
            continue
        prop, val = text.split(":", 1)
        prop = prop.strip()
        val = re.sub(r"\s+", " ", val).strip()
        val = re.sub(r"\s*!important$", "", val)
        if not prop or not val:
            prev = None
            continue
        out.append((prop, val, ""))
        prev = len(out) - 1
    # A trailing comment after the last declaration with no semicolon is handled above only
    # when a later piece exists; check the tail explicitly.
    return out


class CssVars(object):
    """Custom properties read from CSS, by scope."""

    def __init__(self):
        self.base = OrderedDict()            # name -> (value, usage)
        self.themes = OrderedDict()          # id -> OrderedDict(name -> (value, usage))
        self.skipped = []                    # {"name","value","scope","reason"}
        self.fonts = []                      # @font-face entries
        self.order = []                      # first-seen name order
        self.text = ""                       # all CSS text, comments removed
        self.theme_selectors = OrderedDict() # theme id -> the source selector, such as ".dark"
        self.media_themes = []               # theme ids set by @media (prefers-color-scheme)

    def _note(self, name):
        if name not in self.order:
            self.order.append(name)

    def add(self, scope, tid, name, value, usage):
        if scope == "base":
            old = self.base.get(name)
            self.base[name] = (value, usage or (old[1] if old else ""))
        else:
            block = self.themes.setdefault(tid, OrderedDict())
            old = block.get(name)
            block[name] = (value, usage or (old[1] if old else ""))
        self._note(name)


def _read_font_face(body, comments, store):
    decls = dict((p.lower(), v) for p, v, _u in _declarations(body, comments))
    family = decls.get("font-family", "").strip().strip("\"'")
    if not family:
        return
    entry = OrderedDict([("family", family)])
    m = re.search(r"url\(\s*[\"']?([^\"')]+)[\"']?\s*\)", decls.get("src", ""))
    if m and not m.group(1).startswith("data:"):
        entry["file"] = m.group(1)
    if decls.get("font-weight"):
        entry["weight"] = decls["font-weight"]
    if decls.get("font-style"):
        entry["style"] = decls["font-style"]
    if entry not in store.fonts:
        store.fonts.append(entry)


def _walk_css(text, comments, contexts, parent_sel, store):
    for prelude, body, _end in _iter_rules(text):
        pre = _clean(prelude)
        if body is None:
            continue
        low = pre.lower()
        if low.startswith("@font-face"):
            _read_font_face(body, comments, store)
            continue
        if low.startswith(("@keyframes", "@-webkit-keyframes", "@property", "@counter-style", "@page")):
            continue
        if low.startswith("@theme"):
            for prop, val, usage in _declarations(body, comments):
                if prop.startswith("--") and val.lower() != "initial":
                    store.add("base", None, prop[2:], val, usage)
            continue
        if low.startswith("@"):
            _walk_css(body, comments, contexts + [pre], parent_sel, store)
            continue
        selector = pre
        if parent_sel:
            selector = pre.replace("&", parent_sel) if "&" in pre else parent_sel + " " + pre
        decls = [(p, v, u) for p, v, u in _declarations(body, comments) if p.startswith("--")]
        if decls:
            ctx_theme, ctx_skip = _context_scope(contexts)
            scopes = _selector_scope(selector)
            kinds = set(k for k, _t in scopes)
            for prop, val, usage in decls:
                name = prop[2:]
                if ctx_skip:
                    store.skipped.append(OrderedDict([("name", name), ("value", val),
                                                      ("scope", selector), ("reason", ctx_skip)]))
                    continue
                if "base" in kinds:
                    if ctx_theme:
                        store.add("theme", ctx_theme, name, val, usage)
                        if ctx_theme not in store.media_themes:
                            store.media_themes.append(ctx_theme)
                    else:
                        store.add("base", None, name, val, usage)
                elif "theme" in kinds:
                    parts = [p.strip() for p in split_top(selector) if p.strip()]
                    for index, (kind, tid) in enumerate(scopes):
                        if kind == "theme":
                            store.add("theme", tid, name, val, usage)
                            if not ctx_theme and index < len(parts):
                                store.theme_selectors.setdefault(tid, parts[index])
                else:
                    store.skipped.append(OrderedDict([
                        ("name", name), ("value", val), ("scope", selector),
                        ("reason", "scoped to a selector that is not the root or a theme")]))
        # Nested rules inside a style rule.
        if "{" in body:
            _walk_css(body, comments, contexts, selector, store)


def read_css(texts):
    store = CssVars()
    clean_all = []
    for text in texts:
        masked, comments = _mask_comments(text)
        clean_all.append(_MARK_RE.sub(" ", masked))
        _walk_css(masked, comments, [], "", store)
    store.text = "\n".join(clean_all)
    return store


def subst_vars(text, env, stack=None):
    """Replace var() references. Return (text, error or None)."""
    stack = stack or []
    guard = 0
    while True:
        guard += 1
        if guard > 200:
            return text, "var() expansion did not end"
        idx = text.find("var(")
        if idx < 0:
            return text, None
        close = match_paren(text, idx + 3)
        if close < 0:
            return text, "unbalanced parentheses in var()"
        inner = text[idx + 4:close]
        parts = split_top(inner)
        ref = parts[0].strip()
        fallback = ",".join(parts[1:]).strip() if len(parts) > 1 else None
        name = ref[2:] if ref.startswith("--") else ref
        if name in stack:
            return text, "var() cycle: " + " -> ".join(stack + [name])
        if name in env:
            sub, err = subst_vars(env[name], env, stack + [name])
            if err:
                if fallback is None:
                    return text, err
                sub, err = subst_vars(fallback, env, stack)
                if err:
                    return text, err
        elif fallback is not None:
            sub, err = subst_vars(fallback, env, stack)
            if err:
                return text, err
        else:
            return text, "var(--%s) is not defined in the files given" % name
        text = text[:idx] + sub + text[close + 1:]


_TRIPLET_HSL = re.compile(r"^" + NUM + r"(?:deg)?[\s,]+" + NUM + r"%[\s,]+" + NUM + r"%$")
_TRIPLET_NUM = re.compile(r"^" + NUM + r"%?[\s,]+" + NUM + r"%?[\s,]+" + NUM + r"%?$")
_EASE_WORDS = {"ease", "ease-in", "ease-out", "ease-in-out", "linear", "step-start", "step-end"}


def _channel_usage(css_text):
    """Map a property name to the color function that wraps it, e.g. rgb(var(--x))."""
    usage = {}
    for m in re.finditer(r"\b(rgba?|hsla?|oklch)\(\s*var\(\s*--([A-Za-z0-9_-]+)", css_text):
        usage.setdefault(m.group(2), m.group(1).lower())
    return usage


def _looks_like_shadow(value):
    if value.strip().lower() == "none":
        return False
    for layer in split_top(value):
        toks = split_ws_top(layer)
        lengths = [t for t in toks if ANY_LENGTH_RE.match(t)]
        if len(lengths) < 2:
            return False
        if not any(parse_color(t, allow_named=True) for t in toks if not ANY_LENGTH_RE.match(t)):
            return False
    return True


def _is_motion_value(value):
    v = value.strip().lower()
    if TIME_RE.match(v) or v in _EASE_WORDS:
        return True
    if v.startswith(("cubic-bezier(", "steps(", "linear(")):
        return True
    toks = split_ws_top(v)
    return len(toks) > 1 and any(TIME_RE.match(t) for t in toks) and all(
        TIME_RE.match(t) or t in _EASE_WORDS or t.startswith(("cubic-bezier(", "steps(")) or re.match(r"^[a-z-]+$", t)
        for t in toks)


def classify_property(name, value):
    """Sort one resolved property into a family. Return (family, role).

    family: color handled by the caller. Roles for type: family, size,
    line-height, weight, tracking.
    """
    n = name.lower()
    v = value.strip()
    low = v.lower()
    is_len = bool(ANY_LENGTH_RE.match(v))
    if "gradient(" in low:
        return "gradient", None
    if re.search(r"shadow|elevation|glow", n) or _looks_like_shadow(v):
        return "shadow", None
    if re.search(r"line-height|leading|(^|-)lh(-|$)", n):
        return "type", "line-height"
    if re.search(r"letter-spacing|tracking", n):
        return "type", "tracking"
    if re.search(r"font-weight|(^|-)weight(-|$)|(^|-)fw(-|$)", n):
        return "type", "weight"
    if re.search(r"font-size|(^|-)fs(-|$)|^text-|type-size|(^|-)size-text|^type-.+-size$", n) and is_len:
        return "type", "size"
    if re.search(r"font|typeface", n) and not is_len:
        return "type", "family"
    if re.search(r"duration|delay|ease|easing|transition|motion|animat|timing|speed", n) or _is_motion_value(v):
        return "motion", None
    if re.search(r"radius|rounded|corner", n):
        return "radius", None
    if re.search(r"border-width|stroke|outline-width|(^|-)border(-|$)", n) and is_len:
        return "stroke", None
    if re.search(r"space|spacing|gap|gutter|inset|pad|margin|indent", n):
        return "spacing", None
    if re.search(r"opacity|alpha", n):
        return "opacity", None
    if re.search(r"width|height|max|min|container|breakpoint|screen|measure|z-index|(^|-)z(-|$)|layer|aspect|size", n):
        return "layout", None
    if is_len:
        return "size", None
    return "other", None


def _theme_name(tid):
    return " ".join(w.capitalize() for w in re.split(r"[-_]+", tid) if w) or tid


def _norm_ws(text):
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text


def css_to_tokens(texts, name, base_theme=None, file_names=None, no_alias=False):
    """Convert CSS custom properties to a tokens document and a report."""
    store = read_css(texts)
    report = OrderedDict([("converted", OrderedDict()), ("unconverted", []), ("computed", []),
                          ("assumed", []), ("skipped", store.skipped)])
    explicit = list(store.themes.keys())
    if base_theme is None:
        if "light" in explicit and "dark" not in explicit:
            base_theme = "dark"
            report["assumed"].append("The root block is treated as theme 'dark' because only a 'light' theme block exists.")
        else:
            base_theme = "light"
            if "light" not in explicit:
                report["assumed"].append("The root block is treated as theme 'light'. Pass --base-theme to change it.")
    themes = [base_theme] + [t for t in explicit if t != base_theme]

    def env_for(tid):
        env = OrderedDict((k, v[0]) for k, v in store.base.items())
        for k, v in store.themes.get(tid, {}).items():
            env[k] = v[0]
        return env

    envs = OrderedDict((t, env_for(t)) for t in themes)
    usage_of = {}
    for k, v in store.base.items():
        usage_of[k] = v[1]
    for block in store.themes.values():
        for k, v in block.items():
            if v[1] and not usage_of.get(k):
                usage_of[k] = v[1]
    chan = _channel_usage(store.text)
    form_of = OrderedDict()    # name -> (color function, separator) of a bare channel triplet

    def unconv(pname, value, theme, reason):
        report["unconverted"].append(OrderedDict([("name", pname), ("value", value),
                                                  ("theme", theme), ("reason", reason)]))

    def computed(pname, theme, src, lit):
        for entry in report["computed"]:
            if entry["name"] == pname and entry["from"] == src and entry["to"] == lit:
                if theme not in entry["themes"]:
                    entry["themes"].append(theme)
                return
        report["computed"].append(OrderedDict([("name", pname), ("themes", [theme]),
                                               ("from", src), ("to", lit)]))

    notes_of = {}

    def resolve(pname, tid):
        """Return (resolved text, color literal or None, error or None)."""
        env = envs[tid]
        raw = env.get(pname)
        notes = notes_of.setdefault((pname, tid), [])
        if raw is None:
            return None, None, "not defined in theme '%s'" % tid
        text, err = subst_vars(raw, env, [pname])
        if err:
            return None, None, err
        text, mixes, err = resolve_color_mix(text)
        if err:
            return None, None, err
        text, _ok = resolve_calc(text)
        text = _norm_ws(text)
        notes.extend(mixes)
        # A color literal as written.
        col = parse_color(text)
        if col is not None:
            return text, text, None
        named = parse_color(text, allow_named=True)
        if named is not None:
            lit = named.to_css()
            notes.append((text, lit))
            return text, lit, None
        # A bare channel triplet such as "8 38 44" or "210 40% 98%".
        if _TRIPLET_NUM.match(text):
            fn = chan.get(pname)
            if fn is None and _TRIPLET_HSL.match(text):
                fn = "hsl"
                note = "'%s' is read as an hsl() triplet because of its percent signs." % pname
                if note not in report["assumed"]:
                    report["assumed"].append(note)
            if fn is None and re.search(r"(^|-)rgb($|-)", pname.lower()):
                fn = "rgb"
            if fn is not None:
                lit_text = "%s(%s)" % (fn.rstrip("a") if fn in ("rgba", "hsla") else fn, text)
                col = parse_color(lit_text)
                if col is not None:
                    lit = col.to_css() if fn.startswith("rgb") else lit_text
                    notes.append((text, lit))
                    # Keep the channel form, so export writes "222.2 47.4% 11.2%" back and the
                    # project's hsl(var(--x)) and rgb(var(--x) / .5) uses still resolve.
                    form_of.setdefault(pname, (fn.rstrip("a"), ", " if "," in text else " "))
                    return text, lit, None
            return text, None, "bare number triplet; no rgb(), hsl() or oklch() wrapper was found for it"
        return text, None, None

    resolved = OrderedDict()   # name -> {theme: (text, color literal, error)}
    for pname in store.order:
        resolved[pname] = OrderedDict()
        for tid in themes:
            if pname in envs[tid]:
                resolved[pname][tid] = resolve(pname, tid)

    # First pass: decide the family of each property.
    family_of = OrderedDict()
    role_of = {}
    for pname in store.order:
        per = resolved[pname]
        if not per:
            continue
        first_tid = base_theme if base_theme in per else next(iter(per))
        text, lit, err = per[first_tid]
        if not NAME_RE.match(pname):
            unconv(pname, envs[first_tid].get(pname), None,
                   "name does not match [A-Za-z0-9][A-Za-z0-9_.-]{0,63}")
            continue
        if err and text is None:
            unconv(pname, envs[first_tid].get(pname), first_tid, err)
            continue
        if lit is not None or any(p[1] is not None for p in per.values()):
            family_of[pname] = "color"
            continue
        if err:
            unconv(pname, envs[first_tid].get(pname), first_tid, err)
            continue
        if "var(" in text.lower():
            unconv(pname, envs[first_tid].get(pname), first_tid, "var() could not be resolved")
            continue
        fam, role = classify_property(pname, text)
        if fam == "other" and re.match(r"^[a-zA-Z]+$", text) and text.lower() not in CSS_WIDE:
            unconv(pname, text, first_tid,
                   "bare keyword; if it is a named color, write its hex in the source")
            continue
        family_of[pname] = fam
        role_of[pname] = role

    doc = OrderedDict([("name", name), ("version", "0.1.0")])
    doc["meta"] = OrderedDict([("source", OrderedDict([
        ("tool", "ds.py from-css"), ("files", list(file_names or []))]))])
    color_names = [n for n, f in family_of.items() if f == "color"]

    # Colors.
    ctoks = []
    for pname in color_names:
        per = resolved[pname]
        values = OrderedDict()
        for tid in themes:
            if tid not in per:
                unconv(pname, None, tid, "no value in theme '%s'" % tid)
                continue
            text, lit, err = per[tid]
            raw = envs[tid][pname].strip()
            m = re.match(r"^var\(\s*--([A-Za-z0-9_.-]+)\s*\)$", raw)
            if m and not no_alias and m.group(1) in color_names and m.group(1) != pname:
                values[tid] = "{%s}" % m.group(1)
            elif lit is not None:
                values[tid] = lit
                for src, to in notes_of.get((pname, tid), []):
                    computed(pname, tid, src, to)
            else:
                unconv(pname, raw, tid, err or "value is not a color in this theme")
        if not values:
            continue
        uniq = set(values.values())
        value = next(iter(uniq)) if (len(uniq) == 1 and len(values) == len(themes)) else values
        ctoks.append(OrderedDict([("name", pname), ("value", value), ("usage", usage_of.get(pname, ""))]))
    if ctoks:
        doc["color"] = OrderedDict([
            ("themes", [OrderedDict([("id", t), ("name", _theme_name(t))]) for t in themes]),
            ("tokens", ctoks)])
        report["converted"]["color"] = len(ctoks)
    css_meta = OrderedDict()
    kept = set(t["name"] for t in ctoks)
    channels = OrderedDict((n, OrderedDict([("function", fn), ("separator", sep)]))
                           for n, (fn, sep) in form_of.items() if n in kept)
    if channels:
        css_meta["channels"] = channels
        report["assumed"].append("Channel triplets keep their form on export: %s." % ", ".join(channels))
    if store.theme_selectors:
        css_meta["themeSelectors"] = OrderedDict((t, sel) for t, sel in store.theme_selectors.items() if t in themes)
    if store.media_themes:
        css_meta["mediaThemes"] = [t for t in store.media_themes if t in themes]
    if css_meta:
        doc["meta"]["css"] = css_meta

    def base_text(pname):
        per = resolved[pname]
        tid = base_theme if base_theme in per else next(iter(per))
        text = per[tid][0]
        for other, (otext, _l, _e) in per.items():
            if other != tid and otext is not None and otext != text:
                unconv(pname, otext, other,
                       "theme override dropped: only the color family holds per-theme values")
        return text

    # Type.
    sizes = [n for n in store.order if family_of.get(n) == "type" and role_of.get(n) == "size"]
    fams = [n for n in store.order if family_of.get(n) == "type" and role_of.get(n) == "family"]
    used = set()
    type_misc = []

    def key_of(size_name):
        m = re.match(r"^type-(.+)-size$", size_name)
        if m:
            return m.group(1)
        return re.sub(r"^(?:font-size|text|fs|type-size)-", "", size_name)

    def companion(size_name, kind):
        key = key_of(size_name)
        own = {"line-height": "type-%s-line-height", "weight": "type-%s-weight",
               "tracking": "type-%s-letter-spacing"}[kind] % key
        if re.match(r"^type-.+-size$", size_name) and family_of.get(own) == "type":
            return own
        cands = {
            "line-height": ["%s--line-height" % size_name, "line-height-%s" % key, "leading-%s" % key, "lh-%s" % key],
            "weight": ["%s--font-weight" % size_name, "font-weight-%s" % key, "weight-%s" % key, "fw-%s" % key],
            "tracking": ["%s--letter-spacing" % size_name, "letter-spacing-%s" % key, "tracking-%s" % key],
        }[kind]
        for c in cands:
            if c in family_of and family_of[c] == "type":
                return c
        return None

    def as_number(text):
        try:
            f = float(text)
        except (TypeError, ValueError):
            return text
        return int(f) if f == int(f) else f

    if fams and sizes:
        families = OrderedDict((n, base_text(n)) for n in fams)
        body_key = next((k for k in families if re.search(r"body|sans|base|text", k)), fams[0])
        head_key = next((k for k in families if re.search(r"display|heading|head|title|serif", k) and k != body_key), None)
        groups = OrderedDict()
        for sname in sizes:
            own = re.match(r"^type-(.+)-size$", sname)
            style = OrderedDict([("name", own.group(1) if own else sname), ("fontSize", base_text(sname))])
            lh = companion(sname, "line-height")
            fw = companion(sname, "weight")
            ls = companion(sname, "tracking")
            if lh:
                style["lineHeight"] = as_number(base_text(lh))
                used.add(lh)
            if fw:
                style["fontWeight"] = as_number(base_text(fw))
                used.add(fw)
            if ls:
                style["letterSpacing"] = base_text(ls)
                used.add(ls)
            if usage_of.get(sname):
                style["usage"] = usage_of[sname]
            is_head = bool(re.search(r"(^|-)(h[1-6]|display|heading|title|hero)(-|$)", sname))
            gname, gfam = ("Headings", head_key) if (is_head and head_key) else ("Text", body_key)
            groups.setdefault((gname, gfam), []).append(style)
        doc["type"] = OrderedDict([
            ("fonts", store.fonts), ("families", families),
            ("groups", [OrderedDict([("name", g[0]), ("family", g[1]), ("styles", st)])
                        for g, st in groups.items()])])
        report["converted"]["type"] = len(sizes)
        report["assumed"].append(
            "Type styles are grouped by name. Group families: %s. Check each group's family." %
            ", ".join("%s uses %s" % (g[0], g[1]) for g in groups))
        type_misc = [n for n in store.order if family_of.get(n) == "type"
                     and role_of.get(n) not in ("size", "family") and n not in used]
    else:
        type_misc = [n for n in store.order if family_of.get(n) == "type"]
        if sizes and not fams:
            report["assumed"].append(
                "No font family property was found. Font sizes are written to the 'font' family as plain tokens.")
        if store.fonts:
            report["assumed"].append("@font-face rules were found but no type family was written. Add the fonts by hand.")
    for n in type_misc:
        family_of[n] = "font"

    # Every other family.
    order = []
    for n in store.order:
        fam = family_of.get(n)
        if fam and fam not in ("color", "type") and fam not in order:
            order.append(fam)
    for fam in order:
        toks = []
        for pname in store.order:
            if family_of.get(pname) != fam:
                continue
            text = base_text(pname)
            if fam in LENGTH_FAMILIES and not LENGTH_RE.match(text):
                unconv(pname, text, None,
                       "'%s' is not a length in px, rem, em or %% for the %s family" % (text, fam))
                continue
            if "var(" in text.lower() or "color-mix(" in text.lower():
                unconv(pname, text, None, "the value still holds var() or color-mix()")
                continue
            toks.append(OrderedDict([("name", pname), ("value", text), ("usage", usage_of.get(pname, ""))]))
            for per_tid in resolved[pname]:
                for src, to in notes_of.get((pname, per_tid), []):
                    computed(pname, per_tid, src, to)
                break
        if toks:
            doc[fam] = OrderedDict([("tokens", toks)])
            report["converted"][fam] = len(toks)
    if "other" in report["converted"]:
        report["assumed"].append("Properties with no clear family are in 'other'. Move or remove them.")
    return doc, report


# --------------------------------------------------------------------------
# DTCG conversion (to-dtcg, from-dtcg)
# --------------------------------------------------------------------------

GDH_FORMAT = "claude-design-system-tokens"
_DTCG_KEY_BAD = re.compile(r"[.{}$\s]")
_GENERIC_FONTS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-serif",
                  "ui-sans-serif", "ui-monospace", "ui-rounded", "emoji", "math", "fangsong",
                  "inherit", "initial", "unset"}


def _dtcg_key(name, taken):
    key = _DTCG_KEY_BAD.sub("-", str(name)) or "token"
    base, n = key, 2
    while key in taken:
        key = "%s-%d" % (base, n)
        n += 1
    taken.add(key)
    return key


def _round(x, places=6):
    r = round(float(x), places)
    return int(r) if r == int(r) else r


def color_to_dtcg(raw):
    """A color literal as a DTCG 2025.10 color object, or None."""
    col = parse_color(raw)
    if col is None:
        return None
    if col.kind == "oklch":
        L, C, H = col.native
        obj = OrderedDict([("colorSpace", "oklch"), ("components", [_round(L), _round(C), _round(H, 4)])])
    else:
        obj = OrderedDict([("colorSpace", "srgb"), ("components", [_round(c) for c in col.rgb01()])])
    if col.alpha < 0.9995:
        obj["alpha"] = _round(col.alpha, 4)
    obj["hex"] = col.hex6()
    return obj


def color_from_dtcg(value):
    """A DTCG color value as a CSS literal. Return (literal or None, note or None)."""
    if isinstance(value, str):
        return (value, None) if parse_color(value) else (None, "string '%s' is not a color literal" % value)
    if not isinstance(value, dict):
        return None, "color value is not an object"
    space = value.get("colorSpace")
    comps = value.get("components")
    alpha = value.get("alpha", 1)
    try:
        nums = [0.0 if c == "none" else float(c) for c in comps]
        alpha = float(alpha)
    except (TypeError, ValueError):
        return None, "color components are not numbers"
    if len(nums) != 3:
        return None, "color needs three components"
    if space == "srgb":
        return Color(nums, alpha, "rgb").to_css(), None
    if space == "oklch":
        text = "oklch(%s %s %s%s)" % (fmt_num(nums[0], 6), fmt_num(nums[1], 6), fmt_num(nums[2], 4),
                                      "" if alpha >= 0.9995 else " / %s" % fmt_num(alpha, 4))
        return text, None
    if space == "hsl":
        text = "hsl(%s %s%% %s%%%s)" % (fmt_num(nums[0], 4), fmt_num(nums[1], 4), fmt_num(nums[2], 4),
                                        "" if alpha >= 0.9995 else " / %s" % fmt_num(alpha, 4))
        return text, None
    if space == "oklab":
        return Color(oklab_to_srgb(*nums), alpha, "oklab").to_css(), "oklab converted to sRGB"
    hexv = value.get("hex")
    if isinstance(hexv, str) and parse_color(hexv):
        col = parse_color(hexv)
        col.alpha = alpha
        return col.to_css(), "color space '%s' is not converted; the hex fallback was used" % space
    return None, "color space '%s' is not supported and there is no hex fallback" % space


def dim_to_dtcg(raw):
    if isinstance(raw, bool) or not isinstance(raw, str):
        return None
    m = LENGTH_RE.match(raw.strip())
    if not m or m.group(2) not in ("px", "rem"):
        return None
    return OrderedDict([("value", _round(m.group(1))), ("unit", m.group(2))])


def dim_from_dtcg(value):
    if isinstance(value, dict) and "value" in value:
        return "%s%s" % (fmt_num(float(value["value"]), 6), value.get("unit", ""))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value
    return None


def parse_shadow(raw):
    """Parse a box-shadow string into DTCG shadow layers, or None."""
    if not isinstance(raw, str) or not raw.strip() or raw.strip().lower() == "none":
        return None
    layers = []
    for layer in split_top(raw):
        toks = split_ws_top(layer)
        inset = False
        dims, color = [], None
        for t in toks:
            if t.lower() == "inset":
                inset = True
            elif re.match(r"^" + NUM + r"(px|rem)?$", t):
                m = re.match(r"^(" + NUM + r")(px|rem)?$", t)
                if m.group(2) is None and float(m.group(1)) != 0:
                    return None
                dims.append(OrderedDict([("value", _round(m.group(1))), ("unit", m.group(2) or "px")]))
            elif color is None and color_to_dtcg(t) is not None:
                color = color_to_dtcg(t)
            else:
                return None
        if color is None or not 2 <= len(dims) <= 4:
            return None
        zero = OrderedDict([("value", 0), ("unit", "px")])
        obj = OrderedDict([("color", color), ("offsetX", dims[0]), ("offsetY", dims[1]),
                           ("blur", dims[2] if len(dims) > 2 else zero),
                           ("spread", dims[3] if len(dims) > 3 else zero)])
        if inset:
            obj["inset"] = True
        layers.append(obj)
    return layers[0] if len(layers) == 1 else layers


def shadow_from_dtcg(value):
    layers = value if isinstance(value, list) else [value]
    out = []
    for layer in layers:
        if not isinstance(layer, dict):
            return None
        col, _note = color_from_dtcg(layer.get("color"))
        if col is None:
            return None
        parts = []
        if layer.get("inset"):
            parts.append("inset")
        for key in ("offsetX", "offsetY", "blur", "spread"):
            d = dim_from_dtcg(layer.get(key, {"value": 0, "unit": "px"}))
            if d is None:
                return None
            d = str(d)
            parts.append("0" if re.match(r"^0(px|rem)?$", d) else d)
        if parts[-1] == "0":
            parts.pop()
        parts.append(col)
        out.append(" ".join(parts))
    return ", ".join(out)


def stack_to_list(stack):
    return [p.strip().strip("\"'") for p in split_top(stack) if p.strip()]


def list_to_stack(names):
    if isinstance(names, str):
        return names
    out = []
    for n in names:
        n = str(n)
        out.append(n if (n.lower() in _GENERIC_FONTS or re.match(r"^[A-Za-z0-9_-]+$", n)) else '"%s"' % n)
    return ", ".join(out)


def _generic_to_dtcg(fam, raw):
    """Map one non-color token value to (DTCG type or None, DTCG value)."""
    if isinstance(raw, bool):
        return None, raw
    if isinstance(raw, (int, float)):
        return "number", raw
    if not isinstance(raw, str):
        return None, raw
    s = raw.strip()
    d = dim_to_dtcg(s)
    if d is not None:
        return "dimension", d
    m = TIME_RE.match(s)
    if m:
        return "duration", OrderedDict([("value", _round(m.group(1))), ("unit", m.group(2))])
    m = re.match(r"^cubic-bezier\(\s*(" + NUM + r")\s*,\s*(" + NUM + r")\s*,\s*(" + NUM + r")\s*,\s*(" + NUM + r")\s*\)$", s)
    if m:
        return "cubicBezier", [_round(g) for g in m.groups()]
    if fam == "shadow":
        sh = parse_shadow(s)
        if sh is not None:
            return "shadow", sh
    c = color_to_dtcg(s)
    if c is not None:
        return "color", c
    return None, raw


def _style_to_dtcg(style, family_key):
    val = OrderedDict()
    val["fontFamily"] = "{type.family.%s}" % family_key
    fs = style.get("fontSize")
    val["fontSize"] = dim_to_dtcg(fs) if dim_to_dtcg(fs) is not None else fs
    if "fontWeight" in style:
        val["fontWeight"] = style["fontWeight"]
    if "lineHeight" in style:
        val["lineHeight"] = style["lineHeight"]
    if "letterSpacing" in style:
        ls = style["letterSpacing"]
        val["letterSpacing"] = dim_to_dtcg(ls) if dim_to_dtcg(ls) is not None else ls
    return val


def claude_to_dtcg(doc):
    """Convert a Claude-shape tokens document to a DTCG document."""
    notes = []
    out = OrderedDict()
    top = OrderedDict((k, v) for k, v in doc.items() if k in RESERVED_TOP or not isinstance(v, (dict, list)))
    if isinstance(doc.get("name"), str):
        out["$description"] = doc["name"]
    root_ext = OrderedDict([("format", GDH_FORMAT), ("top", top), ("families", family_keys(doc))])
    out["$extensions"] = OrderedDict([("gdh", root_ext)])
    color_keys = {}
    taken = set()
    for tok in color_tokens(doc):
        color_keys[tok["name"]] = _dtcg_key(tok["name"], taken)

    def color_value(raw):
        if not isinstance(raw, str):
            return raw
        m = ALIAS_RE.match(raw.strip())
        if m:
            target = m.group(1).strip()
            return "{color.%s}" % color_keys.get(target, target)
        obj = color_to_dtcg(raw)
        return obj if obj is not None else raw

    for fam in family_keys(doc):
        block = doc[fam]
        if not isinstance(block, dict):
            notes.append("Family '%s' is not an object and was skipped." % fam)
            continue
        if fam == "type":
            out["type"] = _type_to_dtcg(block, root_ext)
            continue
        group = OrderedDict()
        extra = OrderedDict((k, v) for k, v in block.items() if k not in ("tokens", "themes"))
        if isinstance(extra.get("note"), str):
            group["$description"] = extra["note"]
        gext = OrderedDict()
        if extra:
            gext["extra"] = extra
        if fam == "color":
            root_ext["themes"] = block.get("themes", [])
            group["$type"] = "color"
        if gext:
            group["$extensions"] = OrderedDict([("gdh", gext)])
        ids = theme_ids(doc)
        ftaken = set()
        for tok in block.get("tokens") or []:
            if not isinstance(tok, dict) or not isinstance(tok.get("name"), str):
                continue
            name = tok["name"]
            raw = tok.get("value")
            node = OrderedDict()
            ext = OrderedDict([("name", name), ("value", raw)])
            if fam == "color":
                key = color_keys[name]
                first = raw
                if isinstance(raw, dict):
                    first = raw.get(ids[0]) if ids and ids[0] in raw else next(iter(raw.values()), None)
                    ext["modes"] = OrderedDict((k, color_value(v)) for k, v in raw.items())
                node["$type"] = "color"
                node["$value"] = color_value(first)
                if isinstance(node["$value"], str) and not ALIAS_RE.match(node["$value"]):
                    notes.append("Color '%s' is not a literal; its value is passed through as text." % name)
            else:
                key = _dtcg_key(name, ftaken)
                dtype, dval = _generic_to_dtcg(fam, raw)
                if dtype:
                    node["$type"] = dtype
                else:
                    notes.append("%s token '%s' has no DTCG type; its value is passed through as text." % (fam, name))
                node["$value"] = dval
            if "usage" in tok:
                node["$description"] = tok["usage"]
            tok_extra = OrderedDict((k, v) for k, v in tok.items() if k not in ("name", "value", "usage"))
            if tok_extra:
                ext["extra"] = tok_extra
            node["$extensions"] = OrderedDict([("gdh", ext)])
            group[key] = node
        out[fam] = group
    return out, notes


def _type_to_dtcg(block, root_ext):
    group = OrderedDict()
    extra = OrderedDict((k, v) for k, v in block.items() if k not in ("fonts", "families", "groups"))
    gext = OrderedDict([("fonts", block.get("fonts", []))])
    if extra:
        gext["extra"] = extra
    group["$extensions"] = OrderedDict([("gdh", gext)])
    fam_group = OrderedDict([("$type", "fontFamily")])
    fam_keys = {}
    taken = set()
    for key, stack in (block.get("families") or {}).items():
        dk = _dtcg_key(key, taken)
        fam_keys[key] = dk
        fam_group[dk] = OrderedDict([
            ("$value", stack_to_list(stack) if isinstance(stack, str) else stack),
            ("$extensions", OrderedDict([("gdh", OrderedDict([("name", key), ("value", stack)]))]))])
    group["family"] = fam_group
    style_group = OrderedDict()
    gtaken = set()
    for g in block.get("groups") or []:
        if not isinstance(g, dict):
            continue
        gk = _dtcg_key(g.get("name", "group"), gtaken)
        node = OrderedDict([("$type", "typography")])
        if isinstance(g.get("note"), str):
            node["$description"] = g["note"]
        node["$extensions"] = OrderedDict([("gdh", OrderedDict(
            (k, v) for k, v in g.items() if k != "styles"))])
        staken = set(["$type", "$description", "$extensions"])
        for s in g.get("styles") or []:
            if not isinstance(s, dict):
                continue
            sk = _dtcg_key(s.get("name", "style"), staken)
            snode = OrderedDict([("$value", _style_to_dtcg(s, fam_keys.get(g.get("family"), g.get("family"))))])
            if "usage" in s:
                snode["$description"] = s["usage"]
            snode["$extensions"] = OrderedDict([("gdh", OrderedDict([("name", s.get("name")), ("value", s)]))])
            node[sk] = snode
        style_group[gk] = node
    group["style"] = style_group
    return group


def _is_token_node(node):
    if not isinstance(node, dict):
        return False
    if "$value" in node:
        return True
    return "value" in node and not isinstance(node.get("value"), dict) or (
        "value" in node and "type" in node)


def _walk_dtcg(node, path, inherited, out):
    if not isinstance(node, dict):
        return
    if _is_token_node(node):
        legacy = "$value" not in node
        out.append(OrderedDict([
            ("path", list(path)),
            ("type", node.get("$type", node.get("type") if legacy else None) or inherited),
            ("value", node.get("value") if legacy else node.get("$value")),
            ("description", node.get("$description", node.get("description", node.get("comment")))),
            ("ext", (node.get("$extensions") or {}).get("gdh") if isinstance(node.get("$extensions"), dict) else None),
        ]))
        return
    t = node.get("$type", inherited)
    for k, v in node.items():
        if k.startswith("$"):
            continue
        _walk_dtcg(v, path + [k], t, out)


def _infer_dtcg_type(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, dict):
        if "colorSpace" in value:
            return "color"
        if "value" in value and "unit" in value:
            return "duration" if value.get("unit") in ("ms", "s") else "dimension"
        if "fontFamily" in value or "fontSize" in value:
            return "typography"
        if "offsetX" in value:
            return "shadow"
        return None
    if isinstance(value, str):
        s = value.strip()
        if parse_color(s):
            return "color"
        if ANY_LENGTH_RE.match(s) and not re.match(r"^" + NUM + r"$", s):
            return "duration" if TIME_RE.match(s) else "dimension"
        if s.startswith("cubic-bezier("):
            return "cubicBezier"
    return None


def _safe_name(path):
    name = re.sub(r"[^A-Za-z0-9_.-]", "-", "-".join(str(p) for p in path)).strip("-")
    name = re.sub(r"-{2,}", "-", name)[:64]
    if not name or not NAME_RE.match(name):
        name = ("t-" + name)[:64]
    return name


def _generic_family(dtype, path):
    joined = "-".join(str(p).lower() for p in path)
    if dtype == "color":
        return "color"
    if dtype == "shadow":
        return "shadow"
    if dtype in ("duration", "cubicBezier", "transition"):
        return "motion"
    if dtype == "dimension":
        if re.search(r"radius|radii|rounded|corner", joined):
            return "radius"
        if re.search(r"space|spacing|gap|inset|padding|margin", joined):
            return "spacing"
        if re.search(r"font-?size|text-?size|line-?height|letter-?spacing", joined):
            return "font"
        if re.search(r"border|stroke", joined):
            return "stroke"
        return "size"
    if dtype in ("fontFamily", "fontWeight"):
        return "font"
    first = re.sub(r"[^A-Za-z0-9_-]", "-", str(path[0])) if path else "other"
    return first if (len(path) > 1 and first not in ("color", "type")) else "other"


def dtcg_to_claude(dtcg, name=None, theme_id="light", theme_files=None):
    """Convert a DTCG document to the Claude shape. Return (doc, report)."""
    report = OrderedDict([("converted", OrderedDict()), ("unconverted", []), ("notes", [])])
    root_ext = None
    if isinstance(dtcg, dict) and isinstance(dtcg.get("$extensions"), dict):
        root_ext = dtcg["$extensions"].get("gdh")
    if isinstance(root_ext, dict) and root_ext.get("format") == GDH_FORMAT:
        if theme_files:
            report["notes"].append("--theme files are ignored for a file written by to-dtcg; it carries its own themes.")
        doc = _own_dtcg_to_claude(dtcg, root_ext, report)
        if name:
            doc["name"] = name
        return doc, report
    flat = []
    _walk_dtcg(dtcg, [], None, flat)
    by_path = {".".join(t["path"]): t for t in flat}
    for t in flat:
        if t["type"] is None:
            t["type"] = _infer_dtcg_type(t["value"])
    names = {}
    taken = {}
    for t in flat:
        n = _safe_name(t["path"])
        if n in taken:
            report["unconverted"].append(OrderedDict([
                ("name", ".".join(t["path"])), ("reason", "name '%s' collides with %s" % (n, taken[n]))]))
            t["skip"] = True
            continue
        taken[n] = ".".join(t["path"])
        names[".".join(t["path"])] = n

    def deref(value, depth=0):
        """Follow an alias to its target token. Return (token or None, value)."""
        if isinstance(value, str):
            m = ALIAS_RE.match(value.strip())
            if m and depth < 20:
                key = m.group(1).strip()
                key = key[:-len(".$value")] if key.endswith(".$value") else key
                target = by_path.get(key)
                if target is None:
                    return None, None
                tok, val = deref(target["value"], depth + 1)
                return (tok or target), (val if tok else target["value"])
        return None, value

    for t in flat:
        if t["type"] is None:
            target, _val = deref(t["value"])
            if target is not None:
                t["type"] = target["type"]

    has_typo = any(t["type"] == "typography" and not t.get("skip") for t in flat)
    doc = OrderedDict([("name", name or (dtcg.get("$description") if isinstance(dtcg, dict) and isinstance(dtcg.get("$description"), str) else "Imported tokens")),
                       ("version", "0.1.0"),
                       ("meta", OrderedDict([("source", OrderedDict([("tool", "ds.py from-dtcg")]))]))])
    families = OrderedDict()
    type_families = OrderedDict()
    type_styles_out = []

    def unconv(t, reason):
        report["unconverted"].append(OrderedDict([("name", ".".join(t["path"])), ("reason", reason)]))

    def literal(t, dtype, value):
        """Return a Claude value for a DTCG value, or None."""
        target, val = deref(value)
        if isinstance(value, str) and ALIAS_RE.match(value.strip()) and target is None:
            return None, "alias target not found"
        value = val
        if dtype == "color":
            lit, note = color_from_dtcg(value)
            if note and lit:
                report["notes"].append("%s: %s" % (".".join(t["path"]), note))
            return lit, note
        if dtype in ("dimension", "duration"):
            d = dim_from_dtcg(value)
            return d, None if d is not None else "not a dimension"
        if dtype == "cubicBezier":
            if isinstance(value, list) and len(value) == 4:
                return "cubic-bezier(%s)" % ", ".join(fmt_num(float(v), 4) for v in value), None
            return (value, None) if isinstance(value, str) else (None, "not a cubic bezier")
        if dtype == "shadow":
            if isinstance(value, str):
                return value, None
            s = shadow_from_dtcg(value)
            return s, None if s else "shadow could not be written as text"
        if dtype == "fontFamily":
            return list_to_stack(value), None
        if dtype == "transition" and isinstance(value, dict):
            parts = []
            for key in ("duration", "timingFunction", "delay"):
                if key in value:
                    sub, _ = literal(t, "cubicBezier" if key == "timingFunction" else "duration", value[key])
                    if sub is None:
                        return None, "transition part '%s' not converted" % key
                    parts.append(str(sub))
            return " ".join(parts), None
        if isinstance(value, (str, int, float)) and not isinstance(value, bool):
            return value, None
        return None, "composite type '%s' is not converted" % dtype

    for t in flat:
        if t.get("skip"):
            continue
        dtype = t["type"]
        pname = names[".".join(t["path"])]
        usage = t["description"] if isinstance(t["description"], str) else ""
        if dtype == "typography":
            target, val = deref(t["value"])
            if not isinstance(val, dict):
                unconv(t, "typography value is not an object")
                continue
            style = OrderedDict([("name", pname)])
            ff = val.get("fontFamily")
            ftarget, fval = deref(ff)
            if ftarget is not None:
                fkey = names.get(".".join(ftarget["path"]), _safe_name(ftarget["path"]))
                type_families.setdefault(fkey, list_to_stack(fval))
            elif ff is not None:
                stack = list_to_stack(ff)
                fkey = _safe_name([stack_to_list(stack)[0].lower().replace(" ", "-")]) if stack else "family"
                type_families.setdefault(fkey, stack)
            else:
                unconv(t, "typography has no fontFamily")
                continue
            for key, kind in (("fontSize", "dimension"), ("lineHeight", None),
                              ("fontWeight", None), ("letterSpacing", "dimension")):
                if key in val:
                    sub, err = literal(t, kind, val[key])
                    if sub is None:
                        unconv(t, "%s: %s" % (key, err))
                    else:
                        style[key] = sub
            style["usage"] = usage
            type_styles_out.append((fkey, style))
            continue
        if dtype == "fontFamily" and has_typo:
            lit, err = literal(t, dtype, t["value"])
            if lit is not None:
                type_families.setdefault(pname, lit)
            continue
        if dtype in ("border", "gradient", "strokeStyle"):
            unconv(t, "composite type '%s' is not converted" % dtype)
            continue
        fam = _generic_family(dtype, t["path"])
        if fam == "color":
            target, _val = deref(t["value"])
            if target is not None and target["type"] == "color" and not target.get("skip"):
                value = "{%s}" % names[".".join(target["path"])]
            else:
                value, err = literal(t, "color", t["value"])
                if value is None:
                    unconv(t, err)
                    continue
        else:
            value, err = literal(t, dtype, t["value"])
            if value is None:
                unconv(t, err or "value not converted")
                continue
            if fam in LENGTH_FAMILIES and not _is_length(value):
                fam = "size"
        families.setdefault(fam, []).append(OrderedDict([("name", pname), ("value", value), ("usage", usage)]))

    themes = [OrderedDict([("id", theme_id), ("name", _theme_name(theme_id))])]
    for tid, other in (theme_files or []):
        odoc, orep = dtcg_to_claude(other, theme_id=tid)
        themes.append(OrderedDict([("id", tid), ("name", _theme_name(tid))]))
        ovals = {tok["name"]: tok["value"] for tok in color_tokens(odoc)}
        for tok in families.get("color", []):
            base = tok["value"] if not isinstance(tok["value"], dict) else None
            if not isinstance(tok["value"], dict):
                tok["value"] = OrderedDict([(theme_id, base)])
            if tok["name"] in ovals:
                tok["value"][tid] = ovals[tok["name"]]
            else:
                tok["value"][tid] = tok["value"][theme_id]
        known = set(tok["name"] for tok in families.get("color", []))
        for n in ovals:
            if n not in known:
                report["unconverted"].append(OrderedDict([
                    ("name", n), ("reason", "color exists only in theme file '%s'" % tid)]))
        for u in orep["unconverted"]:
            report["unconverted"].append(OrderedDict([("name", u["name"]), ("reason", "theme '%s': %s" % (tid, u["reason"]))]))
    for tok in families.get("color", []):
        if isinstance(tok["value"], dict) and len(set(tok["value"].values())) == 1:
            tok["value"] = next(iter(tok["value"].values()))
    if "color" in families:
        doc["color"] = OrderedDict([("themes", themes), ("tokens", families.pop("color"))])
        report["converted"]["color"] = len(doc["color"]["tokens"])
    if type_styles_out:
        groups = OrderedDict()
        for fkey, style in type_styles_out:
            groups.setdefault(fkey, []).append(style)
        doc["type"] = OrderedDict([("fonts", []), ("families", type_families),
                                   ("groups", [OrderedDict([("name", "Text %s" % k if len(groups) > 1 else "Text"),
                                                            ("family", k), ("styles", st)])
                                               for k, st in groups.items()])])
        report["converted"]["type"] = len(type_styles_out)
        report["notes"].append("Type groups are made from the font family of each style. Rename the groups.")
    for fam, toks in families.items():
        doc[fam] = OrderedDict([("tokens", toks)])
        report["converted"][fam] = len(toks)
    return doc, report


def _same_json(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def _own_dtcg_to_claude(dtcg, root_ext, report):
    """Rebuild a document that to-dtcg wrote. Edited $value fields win over stored text."""
    doc = OrderedDict()
    top = root_ext.get("top") or {}
    for k, v in top.items():
        doc[k] = v
    key_to_name = {}
    cgroup = dtcg.get("color") if isinstance(dtcg.get("color"), dict) else {}
    for key, node in cgroup.items():
        if isinstance(node, dict) and "$value" in node:
            ext = (node.get("$extensions") or {}).get("gdh") or {}
            key_to_name[key] = ext.get("name", key)

    def color_back(value):
        if isinstance(value, str):
            m = ALIAS_RE.match(value.strip())
            if m:
                key = m.group(1).strip()
                key = key[len("color."):] if key.startswith("color.") else key
                return "{%s}" % key_to_name.get(key, key)
            return value
        lit, note = color_from_dtcg(value)
        return lit

    def forward_color(raw, ids):
        first = raw
        if isinstance(raw, dict):
            first = raw.get(ids[0]) if ids and ids[0] in raw else next(iter(raw.values()), None)
        if isinstance(first, str):
            m = ALIAS_RE.match(first.strip())
            if m:
                rev = {v: k for k, v in key_to_name.items()}
                return "{color.%s}" % rev.get(m.group(1).strip(), m.group(1).strip())
            obj = color_to_dtcg(first)
            return obj if obj is not None else first
        return first

    order = [f for f in (root_ext.get("families") or []) if f in dtcg]
    order += [k for k in dtcg if not k.startswith("$") and k not in order]
    themes = root_ext.get("themes") or []
    ids = [t.get("id") for t in themes if isinstance(t, dict)]
    for fam in order:
        group = dtcg[fam]
        if not isinstance(group, dict):
            continue
        if fam == "type":
            doc["type"] = _own_type_back(group, report)
            continue
        gext = (group.get("$extensions") or {}).get("gdh") or {}
        block = OrderedDict()
        if fam == "color":
            block["themes"] = themes
        for k, v in (gext.get("extra") or {}).items():
            block[k] = v
        toks = []
        for key, node in group.items():
            if key.startswith("$") or not isinstance(node, dict) or "$value" not in node:
                continue
            ext = (node.get("$extensions") or {}).get("gdh") or {}
            tname = ext.get("name", key)
            if "value" in ext:
                raw = ext["value"]
                if fam == "color":
                    expect = forward_color(raw, ids)
                else:
                    expect = _generic_to_dtcg(fam, raw)[1]
                if _same_json(expect, node["$value"]):
                    value = raw
                else:
                    report["notes"].append("%s.%s: $value was edited; the edited value is used." % (fam, key))
                    value = color_back(node["$value"]) if fam == "color" else _own_generic_back(node)
            else:
                value = color_back(node["$value"]) if fam == "color" else _own_generic_back(node)
            if value is None:
                report["unconverted"].append(OrderedDict([("name", "%s.%s" % (fam, key)), ("reason", "value not converted")]))
                continue
            tok = OrderedDict([("name", tname), ("value", value)])
            if "$description" in node:
                tok["usage"] = node["$description"]
            for k, v in (ext.get("extra") or {}).items():
                tok[k] = v
            toks.append(tok)
        block["tokens"] = toks
        doc[fam] = block
        report["converted"][fam] = len(toks)
    return doc


def _own_generic_back(node):
    dtype, value = node.get("$type"), node["$value"]
    if dtype in ("dimension", "duration"):
        return dim_from_dtcg(value)
    if dtype == "cubicBezier" and isinstance(value, list):
        return "cubic-bezier(%s)" % ", ".join(fmt_num(float(v), 4) for v in value)
    if dtype == "shadow":
        return value if isinstance(value, str) else shadow_from_dtcg(value)
    if dtype == "color":
        return color_from_dtcg(value)[0]
    if isinstance(value, (str, int, float)) and not isinstance(value, bool):
        return value
    return None


def _own_type_back(group, report):
    gext = (group.get("$extensions") or {}).get("gdh") or {}
    block = OrderedDict([("fonts", gext.get("fonts", []))])
    families = OrderedDict()
    key_to_fam = {}
    for key, node in (group.get("family") or {}).items():
        if key.startswith("$") or not isinstance(node, dict) or "$value" not in node:
            continue
        ext = (node.get("$extensions") or {}).get("gdh") or {}
        fname = ext.get("name", key)
        key_to_fam[key] = fname
        raw = ext.get("value")
        if isinstance(raw, str) and _same_json(stack_to_list(raw), node["$value"]):
            families[fname] = raw
        else:
            families[fname] = list_to_stack(node["$value"])
    block["families"] = families
    groups = []
    for gkey, gnode in (group.get("style") or {}).items():
        if gkey.startswith("$") or not isinstance(gnode, dict):
            continue
        ext = (gnode.get("$extensions") or {}).get("gdh") or {}
        g = OrderedDict((k, v) for k, v in ext.items())
        g.setdefault("name", gkey)
        styles = []
        for skey, snode in gnode.items():
            if skey.startswith("$") or not isinstance(snode, dict) or "$value" not in snode:
                continue
            sext = (snode.get("$extensions") or {}).get("gdh") or {}
            raw = sext.get("value")
            rev = {v: k for k, v in key_to_fam.items()}
            if isinstance(raw, dict) and _same_json(
                    _style_to_dtcg(raw, rev.get(g.get("family"), g.get("family"))), snode["$value"]):
                styles.append(raw)
                continue
            val = snode["$value"]
            style = OrderedDict([("name", sext.get("name", skey))])
            for key in ("fontSize", "lineHeight", "fontWeight", "letterSpacing"):
                if key in val:
                    v = val[key]
                    style[key] = dim_from_dtcg(v) if isinstance(v, dict) else v
            if "$description" in snode:
                style["usage"] = snode["$description"]
            if isinstance(raw, dict):
                for k, v in raw.items():
                    if k not in style and k not in ("fontSize", "lineHeight", "fontWeight", "letterSpacing"):
                        style[k] = v
            report["notes"].append("type.style.%s.%s: $value was edited; the edited value is used." % (gkey, skey))
            styles.append(style)
        g["styles"] = styles
        groups.append(g)
    block["groups"] = groups
    for k, v in (gext.get("extra") or {}).items():
        block[k] = v
    report["converted"]["type"] = sum(len(g["styles"]) for g in groups)
    return block


# --------------------------------------------------------------------------
# export: CSS, Tailwind v4, flat JSON
# --------------------------------------------------------------------------

GENERATED_NOTE = "Generated from %s by ds.py. Edit the token file, then run export again."


def css_var(name):
    return "--" + re.sub(r"[^A-Za-z0-9_-]", "-", str(name))


def font_var(key):
    key = re.sub(r"[^A-Za-z0-9_-]", "-", str(key))
    return "--" + key if key.startswith("font-") else "--font-" + key


def type_var(style_name, part):
    return "--type-%s-%s" % (re.sub(r"[^A-Za-z0-9_-]", "-", str(style_name)), part)


def _color_css_value(raw):
    if not isinstance(raw, str):
        return None
    m = ALIAS_RE.match(raw.strip())
    if m:
        return "var(%s)" % css_var(m.group(1).strip())
    return raw.strip()


def _type_decls(doc):
    decls = []
    typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
    for key, stack in (typ.get("families") or {}).items():
        decls.append((font_var(key), stack))
    for _g, s in type_styles(doc):
        name = s.get("name")
        for field, part in (("fontSize", "size"), ("lineHeight", "line-height"),
                            ("fontWeight", "weight"), ("letterSpacing", "letter-spacing")):
            if s.get(field) is not None:
                decls.append((type_var(name, part), s[field]))
    return decls


def _other_decls(doc):
    out = []
    for fam in family_keys(doc):
        if fam in ("color", "type"):
            continue
        toks = [(css_var(t["name"]), t.get("value")) for t in list_family_tokens(doc, fam)
                if isinstance(t.get("name"), str) and _check_scalar_value(t.get("value"))]
        if toks:
            out.append((fam, toks))
    return out


def css_meta(doc):
    meta = doc.get("meta") if isinstance(doc.get("meta"), dict) else {}
    css = meta.get("css") if isinstance(meta.get("css"), dict) else {}
    return css


def channel_value(raw, form):
    """Write a color literal back as a bare channel triplet, such as '222.2 47.4% 11.2%' or '37, 99, 235'."""
    fn = str(form.get("function") or "rgb").lower()
    sep = form.get("separator") if form.get("separator") in (" ", ", ") else " "
    text = raw.strip()
    m = re.match(r"^(rgba?|hsla?|oklch)\((.*)\)$", text, re.I)
    if m and m.group(1).lower().rstrip("a") == fn:
        parts = [p for p in re.split(r"[\s,]+", m.group(2).split("/")[0].strip()) if p]
        return sep.join(parts)
    col = parse_color(text, allow_named=True)
    if col is None:
        return None
    if fn == "hsl":
        r, g, b = col.rgb01()
        hue, light, sat = colorsys.rgb_to_hls(r, g, b)
        return sep.join([fmt_num(hue * 360.0, 1), fmt_num(sat * 100.0, 1) + "%", fmt_num(light * 100.0, 1) + "%"])
    if fn == "oklch":
        L, C, H = col.oklch()
        return sep.join([fmt_num(L * 100.0, 2) + "%", fmt_num(C, 4), fmt_num(H, 2)])
    return sep.join(str(c) for c in col.rgb255())


def build_css(doc, source_name="tokens.json", theme_selector=None, media=True):
    """Return (css text, findings).

    theme_selector: a selector with {id}, such as '.{id}' or '[data-theme="{id}"]'. Without it, the
    selectors recorded by from-css (meta.css.themeSelectors) are used, else [data-theme="<id>"].
    media: write the prefers-color-scheme block for a dark theme. It is left out when the source themes
    were class-based.
    """
    findings = []
    ids = theme_ids(doc)
    meta = css_meta(doc)
    channels = meta.get("channels") if isinstance(meta.get("channels"), dict) else {}
    recorded = meta.get("themeSelectors") if isinstance(meta.get("themeSelectors"), dict) else {}
    media_themes = meta.get("mediaThemes") if isinstance(meta.get("mediaThemes"), list) else []
    lines = ["/* " + GENERATED_NOTE % source_name + " */"]
    typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
    for f in typ.get("fonts") or []:
        if isinstance(f, dict) and f.get("family") and f.get("file"):
            lines.append("@font-face {")
            lines.append('  font-family: "%s";' % f["family"])
            lines.append('  src: url("%s");' % f["file"])
            if f.get("weight"):
                lines.append("  font-weight: %s;" % f["weight"])
            if f.get("style"):
                lines.append("  font-style: %s;" % f["style"])
            lines.append("  font-display: swap;")
            lines.append("}")
    seen = {}

    def note_var(var, where):
        if var in seen and seen[var] != where:
            findings.append(finding("CSS_NAME_COLLISION", "error", where,
                                    "CSS variable %s is produced twice (%s and %s)." % (var, seen[var], where),
                                    "Rename one token."))
        seen[var] = where

    def color_block(theme, indent):
        out = []
        for tok in color_tokens(doc):
            raw = color_raw(tok, theme) if theme is not None else tok.get("value")
            val = _color_css_value(raw)
            if val is None:
                continue
            form = channels.get(tok["name"])
            if isinstance(form, dict) and not val.startswith("var("):
                bare = channel_value(val, form)
                if bare is None:
                    findings.append(finding("CSS_CHANNEL_FORM", "error", "color." + tok["name"],
                                            "%s cannot be written as %s channels." % (val, form.get("function")),
                                            "Write the value as a color literal."))
                    continue
                val = bare
            out.append("%s%s: %s;" % (indent, css_var(tok["name"]), val))
        return out

    lines.append(":root {")
    first = ids[0] if ids else None
    if color_tokens(doc):
        lines.append("  /* color%s */" % (" (theme: %s)" % first if first else ""))
        for tok in color_tokens(doc):
            note_var(css_var(tok["name"]), "color." + tok["name"])
        lines.extend(color_block(first, "  "))
    tdecls = _type_decls(doc)
    if tdecls:
        lines.append("  /* type */")
        for var, val in tdecls:
            note_var(var, "type")
            lines.append("  %s: %s;" % (var, val))
    for fam, toks in _other_decls(doc):
        lines.append("  /* %s */" % fam)
        for var, val in toks:
            note_var(var, fam + "." + var[2:])
            lines.append("  %s: %s;" % (var, val))
    lines.append("}")
    for tid in ids:
        if theme_selector:
            selector = theme_selector.replace("{id}", tid)
        elif recorded:
            # Keep the source selectors. A theme with no selector of its own lived in :root or @media.
            selector = recorded.get(tid)
            if selector is None:
                continue
        else:
            selector = '[data-theme="%s"]' % tid
        lines.append("%s {" % selector)
        lines.extend(color_block(tid, "  "))
        lines.append("}")
    class_based = bool(recorded) and "dark" not in media_themes
    if media and not class_based and "dark" in ids and ids[0] != "dark":
        guard = ":root" if (recorded or media_themes) and not theme_selector else ":root:not([data-theme])"
        lines.append("@media (prefers-color-scheme: dark) {")
        lines.append("  %s {" % guard)
        lines.extend(color_block("dark", "    "))
        lines.append("  }")
        lines.append("}")
    return "\n".join(lines) + "\n", findings


def _strip_prefix(name, prefixes):
    for p in prefixes:
        if name.startswith(p) and len(name) > len(p):
            return name[len(p):]
    return name


def build_tailwind(doc, source_name="tokens.json"):
    """A Tailwind v4 theme file. Colors point at the variables in tokens.css."""
    lines = ["/* " + GENERATED_NOTE % source_name + " Import tokens.css before this file. */"]
    ctoks = color_tokens(doc)
    if ctoks:
        lines.append("@theme inline {")
        channels = css_meta(doc).get("channels") or {}
        for tok in ctoks:
            short = _strip_prefix(css_var(tok["name"])[2:], ["color-"])
            form = channels.get(tok["name"]) if isinstance(channels, dict) else None
            if isinstance(form, dict):
                lines.append("  --color-%s: %s(var(%s));" % (short, form.get("function") or "rgb", css_var(tok["name"])))
            else:
                lines.append("  --color-%s: var(%s);" % (short, css_var(tok["name"])))
        lines.append("}")
    body = []
    typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
    for key, stack in (typ.get("families") or {}).items():
        body.append("  %s: %s;" % (font_var(key), stack))
    for _g, s in type_styles(doc):
        short = _strip_prefix(re.sub(r"[^A-Za-z0-9_-]", "-", str(s.get("name"))), ["text-"])
        if s.get("fontSize") is not None:
            body.append("  --text-%s: %s;" % (short, s["fontSize"]))
            if s.get("lineHeight") is not None:
                body.append("  --text-%s--line-height: %s;" % (short, s["lineHeight"]))
            if s.get("fontWeight") is not None:
                body.append("  --text-%s--font-weight: %s;" % (short, s["fontWeight"]))
            if s.get("letterSpacing") is not None:
                body.append("  --text-%s--letter-spacing: %s;" % (short, s["letterSpacing"]))
    for fam, toks in _other_decls(doc):
        for var, val in toks:
            n = var[2:]
            if fam == "spacing":
                body.append("  --spacing-%s: %s;" % (_strip_prefix(n, ["spacing-", "space-"]), val))
            elif fam == "radius":
                body.append("  --radius-%s: %s;" % (_strip_prefix(n, ["radius-", "rounded-"]), val))
            elif fam == "shadow":
                body.append("  --shadow-%s: %s;" % (_strip_prefix(n, ["shadow-"]), val))
            elif isinstance(val, str) and (val.strip().lower() in _EASE_WORDS or val.strip().startswith(("cubic-bezier(", "steps(", "linear("))):
                body.append("  --ease-%s: %s;" % (_strip_prefix(n, ["ease-", "easing-"]), val))
            else:
                body.append("  %s: %s;" % (var, val))
    if body:
        lines.append("@theme {")
        lines.extend(body)
        lines.append("}")
    return "\n".join(lines) + "\n"


def build_flat(doc):
    """One flat name-to-literal map per theme. Aliases are resolved."""
    ids = theme_ids(doc) or ["default"]
    out = OrderedDict()
    for tid in ids:
        flat = OrderedDict()
        for tok in color_tokens(doc):
            col, lit, err = resolve_color(doc, tok["name"], tid)
            if lit is not None:
                flat[tok["name"]] = lit
        typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
        for key, stack in (typ.get("families") or {}).items():
            flat["type.family.%s" % key] = stack
        for g, s in type_styles(doc):
            for field in ("fontSize", "lineHeight", "fontWeight", "letterSpacing"):
                if s.get(field) is not None:
                    flat["type.%s.%s" % (s.get("name"), field)] = s[field]
            flat["type.%s.fontFamily" % s.get("name")] = (typ.get("families") or {}).get(g.get("family"), g.get("family"))
        for fam in family_keys(doc):
            if fam in ("color", "type"):
                continue
            for t in list_family_tokens(doc, fam):
                if isinstance(t.get("name"), str) and _check_scalar_value(t.get("value")):
                    flat[t["name"]] = t["value"]
        out[tid] = flat
    return out


# --------------------------------------------------------------------------
# contrast
# --------------------------------------------------------------------------

AA_NORMAL = 4.5
AA_LARGE = 3.0
_PAIR_HEAD = re.compile(r"\b(large text|text|borders?|outlines?|focus rings?|rings?|icons?|controls?)\s+on\s+", re.I)
_PAIR_NAME = re.compile(r"[`{]?([A-Za-z0-9][A-Za-z0-9_.-]*)[`}]?")
_PAIR_SEP = re.compile(r"\s*(?:,\s*and\s+|,\s*or\s+|,\s*|\s+and\s+|\s+or\s+)")


def pairs_from_usage(doc):
    """Read text-on-ground pairs from usage notes such as "Text on bg and surface."."""
    names = set(t["name"] for t in color_tokens(doc))
    pairs = []
    for tok in color_tokens(doc):
        usage = tok.get("usage")
        if not isinstance(usage, str):
            continue
        for m in _PAIR_HEAD.finditer(usage):
            word = m.group(1).lower()
            kind = "large" if word.startswith("large") else ("text" if word == "text" else "ui")
            pos = m.end()
            while True:
                nm = _PAIR_NAME.match(usage, pos)
                if not nm:
                    break
                cand = nm.group(1)
                while cand and cand not in names and cand[-1] in ".-_":
                    cand = cand[:-1]
                if cand not in names or cand == tok["name"]:
                    break
                entry = OrderedDict([("fg", tok["name"]), ("bg", cand), ("kind", kind)])
                if entry not in pairs:
                    pairs.append(entry)
                pos = nm.start() + usage[nm.start():].index(cand) + len(cand)
                if pos < len(usage) and usage[pos] in "`}":
                    pos += 1
                sep = _PAIR_SEP.match(usage, pos)
                if not sep:
                    break
                pos = sep.end()
    return pairs


def pairs_from_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    pairs = []
    if text.lstrip().startswith(("[", "{")):
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("pairs", [])
        if not isinstance(data, list):
            raise ValueError("the pairs file must hold a list of {fg, bg, kind, themes} objects")
        for index, item in enumerate(data):
            where = "pair %d" % (index + 1)
            if not isinstance(item, dict):
                raise ValueError("%s is not an object with fg and bg" % where)
            for key in ("fg", "bg"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    raise ValueError("%s needs a token name or a color in '%s'" % (where, key))
            kind = item.get("kind", "text")
            if kind not in PAIR_KINDS:
                # An unknown kind must not fall back to the weaker 3:1 threshold.
                raise ValueError("%s has kind %r; use one of %s" % (where, kind, ", ".join(PAIR_KINDS)))
            entry = OrderedDict([("fg", item["fg"].strip()), ("bg", item["bg"].strip()), ("kind", kind)])
            themes = item.get("themes")
            if themes is not None:
                if isinstance(themes, str):
                    themes = [themes]
                if not isinstance(themes, list) or not themes or not all(isinstance(t, str) for t in themes):
                    raise ValueError("%s: themes must be a list of theme ids" % where)
                entry["themes"] = list(themes)
            pairs.append(entry)
        return pairs
    for line in text.splitlines():
        line = line.strip()
        if not line or line == "#" or line.startswith("# "):
            continue
        m = re.match(r"^(\S+)\s+on\s+(\S+)(?:\s+(text|large|ui))?$", line)
        if not m:
            raise ValueError("pairs line not understood: %r. Use: <fg> on <bg> [text|large|ui]" % line)
        pairs.append(OrderedDict([("fg", m.group(1)), ("bg", m.group(2)), ("kind", m.group(3) or "text")]))
    return pairs


PAIR_KINDS = ("text", "large", "ui")


def _floor2(x):
    return math.floor(x * 100 + 1e-9) / 100.0


def check_contrast(doc, pairs):
    """Return a list of results, one for each pair in each theme."""
    results = []
    ids = theme_ids(doc) or [None]
    for pair in pairs:
        unknown = [t for t in (pair.get("themes") or []) if t not in ids]
        for tid in unknown:
            # A pair limited to a theme that does not exist checks nothing. Report it, do not pass it.
            results.append(OrderedDict([("theme", tid), ("fg", pair["fg"]), ("bg", pair["bg"]),
                                        ("kind", pair.get("kind", "text")), ("required", AA_NORMAL),
                                        ("ratio", None), ("pass", False),
                                        ("error", "theme '%s' is not in the token file (themes: %s)"
                                         % (tid, ", ".join(str(i) for i in ids)))]))
        for tid in ids:
            if pair.get("themes") and tid not in pair["themes"]:
                continue
            kind = pair.get("kind", "text")
            if kind not in PAIR_KINDS:
                results.append(OrderedDict([("theme", tid), ("fg", pair["fg"]), ("bg", pair["bg"]), ("kind", kind),
                                            ("required", AA_NORMAL), ("ratio", None), ("pass", False),
                                            ("error", "unknown kind %r; use one of %s" % (kind, ", ".join(PAIR_KINDS)))]))
                continue
            required = AA_NORMAL if kind == "text" else AA_LARGE
            res = OrderedDict([("theme", tid), ("fg", pair["fg"]), ("bg", pair["bg"]), ("kind", kind),
                               ("required", required)])
            fg, fg_lit, ferr = _resolve_any(doc, pair["fg"], tid)
            bg, bg_lit, berr = _resolve_any(doc, pair["bg"], tid)
            res["fgValue"], res["bgValue"] = fg_lit, bg_lit
            if fg is None or bg is None:
                res.update([("ratio", None), ("pass", False), ("error", ferr or berr)])
            elif bg.alpha < 0.9995:
                res.update([("ratio", None), ("pass", False),
                            ("error", "ground '%s' is not opaque; the ratio depends on what is under it" % pair["bg"])])
            else:
                ratio = contrast_ratio(fg, bg)
                res["ratio"] = _floor2(ratio)
                res["passNormalText"] = ratio >= AA_NORMAL
                res["passLargeText"] = ratio >= AA_LARGE
                res["pass"] = ratio >= required
            results.append(res)
    return results


def _resolve_any(doc, ref, tid):
    """Resolve a token name or a color literal."""
    lit = parse_color(ref)
    if lit is not None and ref not in set(t["name"] for t in color_tokens(doc)):
        return lit, ref, None
    return resolve_color(doc, ref, tid)


# --------------------------------------------------------------------------
# Roles: which tokens the specimen page and DESIGN.md use for themselves
# --------------------------------------------------------------------------

_ROLE_NAMES = {
    "bg": ["bg", "background", "bg-primary", "bg-page", "bg-base", "page", "canvas", "base", "color-bg",
           "color-background", "surface-page"],
    "surface": ["surface", "bg-surface", "surface-raised", "bg-raised", "bg-secondary", "card", "panel",
                "color-surface"],
    "text": ["text", "fg", "fg-primary", "foreground", "text-primary", "ink", "body", "color-text",
             "on-bg", "on-surface"],
    "muted": ["text-muted", "fg-muted", "muted", "text-secondary", "fg-secondary", "fg-meta",
              "color-text-muted"],
    "border": ["border", "border-default", "line", "divider", "outline", "border-subtle", "color-border"],
    "accent": ["accent", "primary", "brand", "link", "color-accent", "color-primary"],
}


def _length_px(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        m = LENGTH_RE.match(value.strip())
        if m:
            n = float(m.group(1))
            return n * 16 if m.group(2) in ("rem", "em") else n
    return None


def pick_roles(doc):
    """Map page roles to token names. A role with no token is absent."""
    roles = {}
    ctoks = color_tokens(doc)
    names = [t["name"] for t in ctoks]
    low = {n.lower(): n for n in names}
    for role, cands in _ROLE_NAMES.items():
        for c in cands:
            if c in low:
                roles[role] = low[c]
                break
    ids = theme_ids(doc)
    tid = ids[0] if ids else None
    cols = {}
    for n in names:
        col, _lit, _err = resolve_color(doc, n, tid)
        if col is not None and col.alpha >= 0.9995:
            cols[n] = col
    if "bg" not in roles and cols:
        roles["bg"] = max(cols, key=lambda n: relative_luminance(cols[n].rgb01()))
    if "text" not in roles and cols and "bg" in roles and roles["bg"] in cols:
        bg = cols[roles["bg"]]
        roles["text"] = max((n for n in cols if n != roles["bg"]),
                            key=lambda n: contrast_ratio(cols[n], bg), default=None)
        if roles["text"] is None:
            del roles["text"]
    typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
    fams = list((typ.get("families") or {}).keys())
    if fams:
        roles["font"] = next((k for k in fams if re.search(r"sans|body|text|base", k.lower())), fams[0])
        mono = next((k for k in fams if re.search(r"mono|code", k.lower())), None)
        if mono:
            roles["mono"] = mono
    styles = [s for _g, s in type_styles(doc) if isinstance(s.get("name"), str)]
    by_size = sorted((s for s in styles if _length_px(s.get("fontSize")) is not None),
                     key=lambda s: _length_px(s["fontSize"]))
    if by_size:
        named = {s["name"].lower(): s["name"] for s in styles}
        roles["style-body"] = named.get("body") or min(
            by_size, key=lambda s: abs(_length_px(s["fontSize"]) - 16))["name"]
        roles["style-small"] = by_size[0]["name"]
        roles["style-title"] = by_size[-1]["name"]
        if len(by_size) >= 3:
            roles["style-heading"] = by_size[-2]["name"]
    sp = sorted(((_length_px(t.get("value")), t["name"]) for t in list_family_tokens(doc, "spacing")
                 if isinstance(t.get("name"), str) and _length_px(t.get("value")) is not None))
    if sp:
        roles["space-s"] = sp[0][1]
        roles["space-m"] = sp[len(sp) // 2][1]
        roles["space-l"] = sp[-1][1]
    rd = sorted(((_length_px(t.get("value")), t["name"]) for t in list_family_tokens(doc, "radius")
                 if isinstance(t.get("name"), str) and _length_px(t.get("value")) is not None))
    if rd:
        roles["radius"] = rd[(len(rd) - 1) // 2][1]
    return roles


# --------------------------------------------------------------------------
# design-md
# --------------------------------------------------------------------------

def _yaml_scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return fmt_num(v, 6) if isinstance(v, float) else str(v)
    return json.dumps(str(v))


def _yaml_key(k):
    k = str(k)
    return k if re.match(r"^[A-Za-z0-9_-]+$", k) else json.dumps(k)


def _yaml_map(d, indent=0):
    lines = []
    pad = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            if not v:
                lines.append("%s%s: {}" % (pad, _yaml_key(k)))
            else:
                lines.append("%s%s:" % (pad, _yaml_key(k)))
                lines.extend(_yaml_map(v, indent + 1))
        else:
            lines.append("%s%s: %s" % (pad, _yaml_key(k), _yaml_scalar(v)))
    return lines


def readme_sections(text):
    """Split a README into (intro, {lower title: body}) on level 1 and 2 headings."""
    intro, sections, cur, buf = [], OrderedDict(), None, []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,2})\s+(.*?)\s*#*\s*$", line)
        if m:
            if cur is None:
                intro = buf
            else:
                sections[cur] = "\n".join(buf).strip()
            cur, buf = m.group(2).strip().lower(), []
        else:
            buf.append(line)
    if cur is None:
        intro = buf
    else:
        sections[cur] = "\n".join(buf).strip()
    return "\n".join(intro).strip(), sections


def _md_cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def _shift_headings(body):
    """Push headings one level down so a README section nests under a DESIGN.md section."""
    out, in_code = [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#{2,5}\s", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def build_design_md(doc, readme_text=None, source_name="tokens.json", readme_name="README.md"):
    """Return (markdown, findings)."""
    findings = []
    name = doc.get("name") if isinstance(doc.get("name"), str) else "Design system"
    intro, sections = ("", OrderedDict())
    if readme_text:
        intro, sections = readme_sections(readme_text)
        todo = len(re.findall(r"\bTODO\b", readme_text))
        if todo:
            findings.append(finding("README_TODO", "warning", readme_name,
                                    "The README holds %d TODO marker(s)." % todo,
                                    "Replace every TODO with a real rule before you publish the system."))
    desc = doc.get("description") if isinstance(doc.get("description"), str) else ""
    if not desc and intro:
        para = intro.split("\n\n")[0].replace("\n", " ").strip()
        if "TODO" not in para:
            desc = para
    if not desc:
        desc = "%s design system." % name
    ids = theme_ids(doc)
    first = ids[0] if ids else None
    front = OrderedDict([("name", name), ("description", desc)])
    if doc.get("version") is not None:
        front["version"] = str(doc["version"])
    colors = OrderedDict()
    for tok in color_tokens(doc):
        col, lit, err = resolve_color(doc, tok["name"], first)
        if col is not None:
            colors[tok["name"]] = col.hex6() if col.alpha >= 0.9995 else col.to_css()
    front["colors"] = colors
    typo = OrderedDict()
    typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
    fams = typ.get("families") or {}
    for g, s in type_styles(doc):
        entry = OrderedDict()
        if g.get("family") in fams:
            entry["fontFamily"] = fams[g["family"]]
        for field in ("fontSize", "fontWeight", "lineHeight", "letterSpacing"):
            if s.get(field) is not None:
                entry[field] = s[field]
        typo[s.get("name")] = entry
    front["typography"] = typo
    front["spacing"] = OrderedDict((t["name"], t["value"]) for t in list_family_tokens(doc, "spacing")
                                   if isinstance(t.get("name"), str) and _check_scalar_value(t.get("value")))
    front["rounded"] = OrderedDict((t["name"], t["value"]) for t in list_family_tokens(doc, "radius")
                                   if isinstance(t.get("name"), str) and _check_scalar_value(t.get("value")))
    out = ["---"] + _yaml_map(front) + ["---", "", "# %s" % name, ""]
    out += ["## Overview", ""]
    out += [intro if intro else desc, ""]
    if "content fundamentals" in sections:
        out += ["### Content fundamentals", "", _shift_headings(sections["content fundamentals"]), ""]

    def token_table(fam, toks):
        rows = ["| Token | Value | Use |", "| --- | --- | --- |"]
        for t in toks:
            rows.append("| `%s` | `%s` | %s |" % (t.get("name"), _md_cell(t.get("value")), _md_cell(t.get("usage") or "")))
        return rows

    out += ["## Colors", ""]
    if ids:
        out += ["Themes: %s. The front matter lists the `%s` theme." % (", ".join("`%s`" % i for i in ids), first), ""]
    head = "| Token | " + " | ".join(ids or ["Value"]) + " | Use |"
    out += [head, "| --- | " + " | ".join("---" for _ in (ids or [1])) + " | --- |"]
    for tok in color_tokens(doc):
        cells = []
        for tid in (ids or [None]):
            raw = color_raw(tok, tid) if tid is not None else tok.get("value")
            col, lit, err = resolve_color(doc, tok["name"], tid) if tid is not None else (None, raw, None)
            if isinstance(raw, str) and ALIAS_RE.match(raw.strip()) and lit:
                cells.append("`%s` = `%s`" % (raw.strip(), lit))
            else:
                cells.append("`%s`" % _md_cell(raw))
        out.append("| `%s` | %s | %s |" % (tok["name"], " | ".join(cells), _md_cell(tok.get("usage") or "")))
    out.append("")
    pairs = pairs_from_usage(doc)
    if pairs:
        results = check_contrast(doc, pairs)
        out += ["Contrast of the pairs named in the usage notes (WCAG 2.x ratio):", "",
                "| Pair | Theme | Ratio | Required | Result |", "| --- | --- | --- | --- | --- |"]
        for r in results:
            ratio = "%.2f:1" % r["ratio"] if r.get("ratio") is not None else "not computed"
            out.append("| `%s` on `%s` | %s | %s | %s:1 (%s) | %s |" % (
                r["fg"], r["bg"], r["theme"], ratio, fmt_num(r["required"], 1), r["kind"],
                "pass" if r["pass"] else "FAIL"))
        out.append("")
    out += ["## Typography", ""]
    if fams:
        out += ["| Family | Stack |", "| --- | --- |"]
        out += ["| `%s` | %s |" % (k, _md_cell(v)) for k, v in fams.items()]
        out.append("")
    fonts = [f for f in typ.get("fonts") or [] if isinstance(f, dict)]
    if fonts:
        out.append("Font files: " + "; ".join(
            "%s (%s)" % (f.get("family"), f.get("file") or "no file") for f in fonts) + ".")
        out.append("")
    if typo:
        out += ["| Style | Group | Size | Line height | Weight | Use |", "| --- | --- | --- | --- | --- | --- |"]
        for g, s in type_styles(doc):
            out.append("| `%s` | %s | %s | %s | %s | %s |" % (
                s.get("name"), _md_cell(g.get("name", "")), s.get("fontSize", ""), s.get("lineHeight", ""),
                s.get("fontWeight", ""), _md_cell(s.get("usage") or "")))
        out.append("")
    titles = OrderedDict([("spacing", "Layout"), ("shadow", "Elevation"), ("radius", "Shapes"), ("motion", "Motion")])
    for fam, title in titles.items():
        toks = list_family_tokens(doc, fam)
        if toks:
            out += ["## %s" % title, ""] + token_table(fam, toks) + [""]
    for fam in family_keys(doc):
        if fam in ("color", "type") or fam in titles:
            continue
        toks = list_family_tokens(doc, fam)
        if toks:
            out += ["## %s" % fam.capitalize(), ""] + token_table(fam, toks) + [""]
    if "visual foundations" in sections:
        out += ["## Visual foundations", "", _shift_headings(sections["visual foundations"]), ""]
    if "iconography" in sections:
        out += ["## Iconography", "", _shift_headings(sections["iconography"]), ""]
    out += ["## Components", ""]
    if "components" in sections:
        out += [_shift_headings(sections["components"]), ""]
    else:
        out += ["No component rules are recorded in the brand book. Build components from the tokens above.", ""]
    out += ["## Do's and Don'ts", ""]
    rules = sections.get("usage rules") or sections.get("do's and don'ts") or sections.get("rules")
    if rules:
        out += [_shift_headings(rules), ""]
    else:
        out += ["- Use a named token for every color, size, space, radius and duration.",
                "- Do not add a raw value. Add a token to the token file first.", ""]
    out += ["## Source", "",
            "This file is generated from `%s`%s by `ds.py design-md`. Edit those files, then generate it again." % (
                source_name, " and `%s`" % readme_name if readme_text else ""), ""]
    return "\n".join(out), findings


# --------------------------------------------------------------------------
# specimen
# --------------------------------------------------------------------------

def _e(text):
    return html.escape(str(text), quote=True)


_SYSTEM_FONTS = {"arial", "helvetica", "helvetica neue", "georgia", "times", "times new roman", "courier",
                 "courier new", "menlo", "consolas", "monaco", "segoe ui", "liberation mono", "sf pro text",
                 "sf mono", "sfmono-regular", "blinkmacsystemfont", "tahoma", "verdana", "trebuchet ms"}


def _google_fonts_href(doc):
    typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
    with_file = set(f.get("family") for f in typ.get("fonts") or [] if isinstance(f, dict) and f.get("file"))
    names = []
    for stack in (typ.get("families") or {}).values():
        if not isinstance(stack, str):
            continue
        faces = stack_to_list(stack)
        if not faces:
            continue
        n = faces[0]  # only the first face of a stack is the brand face
        if n.lower() in _GENERIC_FONTS or n.startswith("-") or n in with_file or n.lower() in _SYSTEM_FONTS:
            continue
        if n not in names:
            names.append(n)
    if not names:
        return None
    return "https://fonts.googleapis.com/css2?" + "&".join(
        "family=" + n.replace(" ", "+") for n in names) + "&display=swap"


def build_specimen(doc, google_fonts=False, source_name="tokens.json"):
    """Return (html text, findings). The page styles itself with the tokens."""
    findings = []
    css, cfind = build_css(doc, source_name)
    findings.extend(cfind)
    roles = pick_roles(doc)
    ids = theme_ids(doc)
    name = doc.get("name") if isinstance(doc.get("name"), str) else "Design system"
    missing = []

    def v(role, fallback=None):
        if role in roles:
            return "var(%s)" % css_var(roles[role])
        return fallback

    def decl(prop, value):
        return "%s:%s;" % (prop, value) if value else ""

    def style_decl(role):
        if role not in roles:
            return ""
        n = roles[role]
        return "font-size:var(%s);line-height:var(%s, normal);font-weight:var(%s, inherit);" % (
            type_var(n, "size"), type_var(n, "line-height"), type_var(n, "weight"))

    for role, label in (("bg", "a ground color"), ("text", "a text color"), ("font", "a font family"),
                        ("space-m", "spacing tokens"), ("radius", "radius tokens")):
        if role not in roles:
            missing.append(label)
    border = v("border") or v("muted") or v("text")
    page = []
    page.append("*{box-sizing:border-box}")
    page.append("body{margin:0;%s%s%s%s}" % (
        decl("background", v("bg")), decl("color", v("text")),
        decl("font-family", "var(%s)" % font_var(roles["font"]) if "font" in roles else None),
        style_decl("style-body")))
    page.append("main{max-width:72rem;margin:0 auto;%s}" % decl("padding", v("space-l")))
    page.append("h1{margin:0;%s}" % style_decl("style-title"))
    page.append("h2{%s%s}" % (style_decl("style-heading"), decl("margin", "%s 0 %s" % (v("space-l") or "0", v("space-m") or "0")) if v("space-l") else ""))
    page.append("h3{margin:0;%s}" % style_decl("style-body"))
    page.append("p{margin:0}")
    page.append(".meta,.usage,.note{%s%s}" % (decl("color", v("muted")), style_decl("style-small")))
    page.append("code,.mono{%s}" % decl("font-family", "var(%s)" % font_var(roles["mono"]) if "mono" in roles else "inherit"))
    page.append(".theme{%s%s%s%s%s}" % (
        decl("background", v("bg")), decl("color", v("text")), decl("padding", v("space-l")),
        decl("border", "1px solid %s" % border if border else None), decl("border-radius", v("radius"))))
    page.append(".theme+.theme{%s}" % decl("margin-top", v("space-l")))
    page.append(".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(13rem,1fr));%s}" % decl("gap", v("space-m")))
    page.append(".card{%s%s%s%s}" % (
        decl("background", v("surface") or v("bg")), decl("border", "1px solid %s" % border if border else None),
        decl("border-radius", v("radius")), decl("padding", v("space-m"))))
    page.append(".chip{height:4rem;%s%s%s}" % (
        decl("border", "1px solid %s" % border if border else None), decl("border-radius", v("radius")),
        decl("margin-bottom", v("space-s"))))
    page.append(".badge{display:inline-block;white-space:nowrap;border:1px solid currentColor;%s%s%s}" % (
        decl("border-radius", v("radius")), decl("padding", "0 %s" % v("space-s") if v("space-s") else None),
        decl("margin-top", v("space-s"))))
    page.append(".fail{font-weight:700;text-decoration:underline}")
    page.append("table{border-collapse:collapse;width:100%}")
    page.append("th,td{text-align:left;vertical-align:top;%s%s}" % (
        decl("padding", v("space-s")), decl("border-bottom", "1px solid %s" % border if border else None)))
    page.append(".row{display:flex;align-items:baseline;flex-wrap:wrap;%s%s%s}" % (
        decl("gap", v("space-m")), decl("padding", "%s 0" % v("space-s") if v("space-s") else None),
        decl("border-bottom", "1px solid %s" % border if border else None)))
    page.append(".row .meta{flex:0 0 14rem}")
    page.append(".bar{height:1rem;%s%s}" % (decl("background", v("accent") or v("text")), decl("border-radius", v("radius"))))
    page.append(".box{width:6rem;height:6rem;%s%s}" % (
        decl("background", v("surface") or v("bg")), decl("border", "1px solid %s" % border if border else None)))
    page.append(".sample{overflow-wrap:anywhere;min-width:0;flex:1 1 20rem}")

    pairs = pairs_from_usage(doc)
    results = check_contrast(doc, pairs) if pairs else []
    by_fg = {}
    for r in results:
        by_fg.setdefault((r["theme"], r["fg"]), []).append(r)

    def badge(r):
        if r.get("ratio") is None:
            return '<span class="badge fail">on %s: not computed</span>' % _e(r["bg"])
        return '<span class="badge%s">on %s %.2f:1 %s</span>' % (
            "" if r["pass"] else " fail", _e(r["bg"]), r["ratio"],
            "PASS" if r["pass"] else "FAIL (needs %s:1)" % fmt_num(r["required"], 1))

    body = []
    body.append("<main>")
    body.append("<h1>%s</h1>" % _e(name))
    ver = doc.get("version")
    body.append('<p class="meta">Token specimen%s. Generated from %s by ds.py. Every color, size and space on this page is a token.</p>' % (
        " for version %s" % _e(ver) if ver is not None else "", _e(source_name)))
    if missing:
        body.append('<p class="note">The token file has no %s. The page uses browser defaults there.</p>' % _e(", ".join(missing)))
    body.append("<h2>Color</h2>")
    for tid in (ids or [None]):
        tname = next((t.get("name") for t in (doc.get("color") or {}).get("themes", [])
                      if isinstance(t, dict) and t.get("id") == tid), tid)
        attr = ' data-theme="%s"' % _e(tid) if tid is not None else ""
        body.append('<section class="theme"%s>' % attr)
        body.append("<h3>Theme: %s</h3>" % _e(tname or "default"))
        body.append('<div class="grid">')
        for tok in color_tokens(doc):
            raw = color_raw(tok, tid) if tid is not None else tok.get("value")
            col, lit, err = resolve_color(doc, tok["name"], tid) if tid is not None else (parse_color(raw), raw, None)
            shown = raw if isinstance(raw, str) else ""
            if isinstance(raw, str) and ALIAS_RE.match(raw.strip()) and lit:
                shown = "%s = %s" % (raw.strip(), lit)
            body.append('<div class="card">')
            body.append('<div class="chip" style="background:var(%s)"></div>' % css_var(tok["name"]))
            body.append('<h3 class="mono">%s</h3>' % _e(tok["name"]))
            body.append('<p class="meta mono">%s</p>' % _e(shown if col is not None or shown else "no value in this theme"))
            if tok.get("usage"):
                body.append('<p class="usage">%s</p>' % _e(tok["usage"]))
            for r in by_fg.get((tid, tok["name"]), []):
                body.append(badge(r))
            body.append("</div>")
        body.append("</div>")
        theme_results = [r for r in results if r["theme"] == tid]
        if theme_results:
            body.append("<table><thead><tr><th>Pair</th><th>Sample</th><th>Ratio</th><th>Needs</th><th>Result</th></tr></thead><tbody>")
            for r in theme_results:
                sample = '<span style="color:var(%s);background:var(%s)">Sample 123</span>' % (
                    css_var(r["fg"]), css_var(r["bg"]))
                body.append("<tr><td class=\"mono\">%s on %s</td><td>%s</td><td>%s</td><td>%s:1 (%s)</td><td%s>%s</td></tr>" % (
                    _e(r["fg"]), _e(r["bg"]), sample,
                    "%.2f:1" % r["ratio"] if r.get("ratio") is not None else "not computed",
                    fmt_num(r["required"], 1), _e(r["kind"]),
                    "" if r["pass"] else ' class="fail"', "PASS" if r["pass"] else "FAIL"))
            body.append("</tbody></table>")
        elif not pairs:
            body.append('<p class="note">No contrast pairs. Add usage notes such as "Text on bg." to the text colors.</p>')
        body.append("</section>")
    typ = doc.get("type") if isinstance(doc.get("type"), dict) else {}
    fams = typ.get("families") or {}
    if any(True for _ in type_styles(doc)):
        body.append("<h2>Type</h2>")
        for g in typ.get("groups") or []:
            if not isinstance(g, dict):
                continue
            body.append("<h3>%s <span class=\"meta mono\">%s</span></h3>" % (
                _e(g.get("name", "")), _e(fams.get(g.get("family"), g.get("family", "")))))
            for s in g.get("styles") or []:
                if not isinstance(s, dict):
                    continue
                n = s.get("name")
                st = "font-family:var(%s);font-size:var(%s);line-height:var(%s, normal);font-weight:var(%s, normal);letter-spacing:var(%s, normal)" % (
                    font_var(g.get("family")), type_var(n, "size"), type_var(n, "line-height"),
                    type_var(n, "weight"), type_var(n, "letter-spacing"))
                body.append('<div class="row"><div class="meta"><span class="mono">%s<br>%s / %s / %s</span><br>%s</div><div class="sample" style="%s">%s</div></div>' % (
                    _e(n), _e(s.get("fontSize", "")), _e(s.get("lineHeight", "")), _e(s.get("fontWeight", "")),
                    _e(s.get("usage") or ""),
                    _e(st), _e(s.get("sample") or "%s: Sphinx of black quartz, judge my vow. 0123456789" % n)))
    sp = list_family_tokens(doc, "spacing")
    if sp:
        body.append("<h2>Spacing</h2>")
        for t in sp:
            body.append('<div class="row"><div class="meta mono">%s<br>%s</div><div class="sample"><div class="bar" style="width:var(%s)"></div><p class="usage">%s</p></div></div>' % (
                _e(t.get("name")), _e(t.get("value")), css_var(t.get("name")), _e(t.get("usage") or "")))
    rd = list_family_tokens(doc, "radius")
    if rd:
        body.append("<h2>Radius</h2>")
        body.append('<div class="grid">')
        for t in rd:
            body.append('<div><div class="box" style="border-radius:var(%s)"></div><h3 class="mono">%s</h3><p class="meta mono">%s</p><p class="usage">%s</p></div>' % (
                css_var(t.get("name")), _e(t.get("name")), _e(t.get("value")), _e(t.get("usage") or "")))
        body.append("</div>")
    sh = list_family_tokens(doc, "shadow")
    if sh:
        body.append("<h2>Shadow</h2>")
        body.append('<div class="grid">')
        for t in sh:
            body.append('<div><div class="box" style="border:0;box-shadow:var(%s)"></div><h3 class="mono">%s</h3><p class="meta mono">%s</p><p class="usage">%s</p></div>' % (
                css_var(t.get("name")), _e(t.get("name")), _e(t.get("value")), _e(t.get("usage") or "")))
        body.append("</div>")
    for fam in family_keys(doc):
        if fam in ("color", "type", "spacing", "radius", "shadow"):
            continue
        toks = list_family_tokens(doc, fam)
        if not toks:
            continue
        body.append("<h2>%s</h2>" % _e(fam.capitalize()))
        body.append("<table><thead><tr><th>Token</th><th>Value</th><th>Use</th></tr></thead><tbody>")
        for t in toks:
            body.append('<tr><td class="mono">%s</td><td class="mono">%s</td><td>%s</td></tr>' % (
                _e(t.get("name")), _e(t.get("value")), _e(t.get("usage") or "")))
        body.append("</tbody></table>")
    body.append("</main>")
    head = ['<!doctype html>', '<html lang="en">', "<head>", '<meta charset="utf-8">',
            '<meta name="generator" content="ds.py specimen">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>%s specimen</title>" % _e(name)]
    if google_fonts:
        href = _google_fonts_href(doc)
        if href:
            head.append('<link rel="stylesheet" href="%s">' % _e(href))
        else:
            findings.append(finding("SPECIMEN_NO_WEB_FONT", "warning", "type.families",
                                    "No family needs a web font link.", "Remove --google-fonts."))
    head.append("<style>\n%s%s\n</style>" % (css, "\n".join(page)))
    head.append("</head>")
    doc_html = "\n".join(head + ["<body>"] + body + ["</body>", "</html>"]) + "\n"
    return doc_html, findings


class _HtmlCheck(HTMLParser):
    VOID = {"meta", "link", "br", "hr", "img", "input", "source", "area", "base", "col", "embed", "track", "wbr"}

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack, self.errors, self.external, self.tags = [], [], [], 0

    def handle_starttag(self, tag, attrs):
        self.tags += 1
        for k, val in attrs:
            if k in ("src", "href") and val and re.match(r"^(https?:)?//", val):
                self.external.append(val)
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append("unexpected </%s>" % tag)
        else:
            self.stack.pop()


def check_html(text):
    """Return (errors, external urls) for a generated page."""
    p = _HtmlCheck()
    p.feed(text)
    p.close()
    errors = list(p.errors)
    if p.stack:
        errors.append("unclosed: %s" % ", ".join(p.stack))
    external = list(p.external)
    external += re.findall(r"url\(\s*[\"']?((?:https?:)?//[^\"')]+)", text)
    external += re.findall(r"@import\s+[\"']?((?:https?:)?//[^\"';]+)", text)
    return errors, external


# --------------------------------------------------------------------------
# audit: the visual inventory
# --------------------------------------------------------------------------

AUDIT_EXT = {".css": "css", ".scss": "css", ".less": "css", ".html": "html", ".htm": "html",
             ".vue": "html", ".svelte": "html", ".jsx": "jsx", ".tsx": "jsx"}
AUDIT_SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", "vendor", "coverage",
                   ".cache", ".turbo", "__pycache__", ".venv"}
_A_HEX = re.compile(r"(?<![&\w])#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-zA-Z_-])")
_A_FUNC = re.compile(r"\b(rgba?|hsla?|oklch|oklab|lab|lch|hwb)\(([^()]*)\)", re.I)
_A_LEN = re.compile(r"(?<![\w.#-])(" + NUM + r")(px|rem|em)\b")
_A_TIME = re.compile(r"(?<![\w.#-])(" + NUM + r")(ms|s)\b")
_A_DECL = re.compile(r"(?:^|[;{\s])(--[\w-]+|[a-zA-Z-]+)\s*:\s*([^;{}]+)")
_A_FONT_FACE = re.compile(r"@font-face\s*\{[^{}]*\}", re.I)
_A_CSS_WIDE = {"inherit", "initial", "unset", "revert", "revert-layer"}
_A_SPACING_PROP = re.compile(r"^(margin|padding|gap|row-gap|column-gap|grid-gap|inset|top|right|bottom|left)(-|$)")
_A_ARBITRARY = re.compile(r"(?<![\w-])([a-z][a-z0-9-]*)-\[([^\]\s]+)\]")
_A_TW_SPACE = re.compile(r"^-?(p|m|gap|space|inset|top|right|bottom|left|w|h|size|min-w|min-h|max-w|max-h)([xytrblse])?(-[xy])?$")
_A_JS_PROP = re.compile(r"\b(fontSize|fontFamily|borderRadius|transitionDuration|animationDuration|transition|"
                        r"margin\w*|padding\w*|gap|rowGap|columnGap)\s*:\s*(?:([\"'`])(.*?)\2|(" + NUM + r"))")


def _norm_color(text):
    col = parse_color(text)
    if col is None:
        return re.sub(r"\s+", " ", text.strip().lower())
    return col.to_css()


def _norm_len(num, unit):
    return fmt_num(float(num), 4) + unit


class Inventory(object):
    CATS = ("colors", "fontSizes", "fontFamilies", "spacing", "radii", "durations")

    def __init__(self):
        self.counts = OrderedDict((c, {}) for c in self.CATS)
        self.files = OrderedDict()
        self.token_definitions = 0
        self.token_references = 0

    def add(self, cat, value, path):
        self.counts[cat][value] = self.counts[cat].get(value, 0) + 1
        self.files[path] = self.files.get(path, 0) + 1

    def scan_value(self, prop, value, path):
        """Count the literals in one declaration value."""
        prop = prop.lower()
        self.token_references += value.count("var(")
        for m in _A_HEX.finditer(value):
            self.add("colors", _norm_color(m.group(0)), path)
        for m in _A_FUNC.finditer(value):
            if "var(" not in m.group(0):
                self.add("colors", _norm_color(m.group(0)), path)
        if prop in ("font-size", "fontsize"):
            for m in _A_LEN.finditer(value):
                self.add("fontSizes", _norm_len(m.group(1), m.group(2)), path)
            if re.match(r"^" + NUM + r"$", value.strip()):
                self.add("fontSizes", _norm_len(value.strip(), "px"), path)
        elif prop in ("font-family", "fontfamily"):
            if "var(" not in value and value.strip().strip(";").strip().lower() not in _A_CSS_WIDE:
                self.add("fontFamilies", re.sub(r"\s+", " ", value.strip().strip(";")), path)
        elif prop.startswith("border-radius") or prop.endswith("radius"):
            for m in _A_LEN.finditer(value):
                self.add("radii", _norm_len(m.group(1), m.group(2)), path)
            if re.match(r"^" + NUM + r"$", value.strip()) and float(value) != 0:
                self.add("radii", _norm_len(value.strip(), "px"), path)
        elif _A_SPACING_PROP.match(prop) or re.match(r"^(margin|padding|gap|rowgap|columngap)", prop):
            for m in _A_LEN.finditer(value):
                if float(m.group(1)) != 0:
                    self.add("spacing", _norm_len(m.group(1), m.group(2)), path)
            if re.match(r"^" + NUM + r"$", value.strip()) and float(value) != 0:
                self.add("spacing", _norm_len(value.strip(), "px"), path)
        if prop.startswith(("transition", "animation")):
            for m in _A_TIME.finditer(value):
                if float(m.group(1)) != 0:
                    self.add("durations", _norm_len(m.group(1), m.group(2)), path)

    def scan_css(self, text, path):
        text = _COMMENT_RE.sub(" ", text)
        # An @font-face block declares a face: its font-family names the face and cannot be
        # a token reference. Its descriptors are not literals that bypass tokens.
        text = _A_FONT_FACE.sub(" ", text)
        for m in _A_DECL.finditer(text):
            prop, value = m.group(1), m.group(2).strip()
            if prop.startswith("--"):
                self.token_definitions += 1
                self.token_references += value.count("var(")
                continue
            self.scan_value(prop, value, path)

    def scan_arbitrary(self, text, path):
        """Tailwind arbitrary values such as p-[13px] or bg-[#fff]."""
        for m in _A_ARBITRARY.finditer(text):
            util, val = m.group(1), m.group(2).replace("_", " ")
            if "var(" in val or val.startswith("--"):
                self.token_references += 1
                continue
            if _A_HEX.fullmatch(val) or _A_FUNC.fullmatch(val):
                self.add("colors", _norm_color(val), path)
                continue
            lm = re.match(r"^(" + NUM + r")(px|rem|em)$", val)
            tm = re.match(r"^(" + NUM + r")(ms|s)$", val)
            if lm:
                if util == "text":
                    self.add("fontSizes", _norm_len(lm.group(1), lm.group(2)), path)
                elif util.startswith("rounded"):
                    self.add("radii", _norm_len(lm.group(1), lm.group(2)), path)
                elif _A_TW_SPACE.match(util):
                    self.add("spacing", _norm_len(lm.group(1), lm.group(2)), path)
            elif tm and util in ("duration", "delay"):
                self.add("durations", _norm_len(tm.group(1), tm.group(2)), path)

    def scan_html(self, text, path):
        for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.S | re.I):
            self.scan_css(m.group(1), path)
        rest = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
        for m in re.finditer(r"\bstyle\s*=\s*([\"'])(.*?)\1", rest, re.S):
            self.scan_css(m.group(2), path)
        for m in re.finditer(r"\b(?:fill|stroke|color|bgcolor|stop-color)\s*=\s*[\"'](#[0-9a-fA-F]{3,8})[\"']", rest):
            self.add("colors", _norm_color(m.group(1)), path)
        self.scan_arbitrary(rest, path)

    def scan_jsx(self, text, path):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        text = re.sub(r"(?m)^\s*//.*$", " ", text)
        consumed = []
        for m in _A_JS_PROP.finditer(text):
            prop = m.group(1)
            value = m.group(3) if m.group(3) is not None else m.group(4)
            key = {"transitionDuration": "transition-duration", "animationDuration": "animation-duration",
                   "borderRadius": "border-radius", "fontSize": "font-size",
                   "fontFamily": "font-family"}.get(prop, prop.lower())
            self.scan_value(key, value, path)
            consumed.append((m.start(), m.end()))
        rest = list(text)
        for a, b in consumed:
            for i in range(a, b):
                rest[i] = " "
        rest = "".join(rest)
        for m in re.finditer(r"[\"'`\[:(\s]#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-zA-Z_-])", rest):
            before = rest[max(0, m.start() - 24):m.start() + 1]
            if re.search(r"(?:href|to|id|htmlFor|for|key|aria-[a-z]+|data-[a-z-]+)\s*=\s*\{?\s*[\"'`]$", before):
                continue  # a link target or an id, not a color
            self.add("colors", _norm_color("#" + m.group(1)), path)
        for m in _A_FUNC.finditer(rest):
            if "var(" not in m.group(0) and re.search(r"\d", m.group(2)):
                self.add("colors", _norm_color(m.group(0)), path)
        self.token_references += rest.count("var(--")
        self.scan_arbitrary(re.sub(r"-\[#[0-9a-fA-F]{3,8}\]", "-[]", rest), path)


def audit_paths(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = sorted(d for d in dirs if d not in AUDIT_SKIP_DIRS)
                for n in sorted(names):
                    ext = os.path.splitext(n)[1].lower()
                    if ext in AUDIT_EXT and not n.endswith((".min.css", ".min.js")):
                        files.append(os.path.join(root, n))
        elif os.path.isfile(p):
            files.append(p)
        else:
            raise IOError("no such file or folder: %s" % p)
    return files


def near_duplicate_colors(values, threshold=0.02):
    """Group colors that sit close together in OKLab."""
    cols = [(v, parse_color(v)) for v in values]
    cols = [(v, c) for v, c in cols if c is not None]
    groups, used = [], set()
    for i, (v, c) in enumerate(cols):
        if v in used:
            continue
        group = [v]
        la = c.oklab()
        for w, d in cols[i + 1:]:
            if w in used:
                continue
            lb = d.oklab()
            dist = math.sqrt(sum((la[k] - lb[k]) ** 2 for k in range(3)))
            if dist <= threshold and abs(c.alpha - d.alpha) < 0.01:
                group.append(w)
                used.add(w)
        if len(group) > 1:
            used.add(v)
            groups.append(group)
    return groups


def run_audit(paths, tokens_doc=None):
    inv = Inventory()
    files = audit_paths(paths)
    for f in files:
        kind = AUDIT_EXT.get(os.path.splitext(f)[1].lower(), "css")
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except (IOError, OSError):
            continue
        if kind == "css":
            inv.scan_css(text, f)
        elif kind == "html":
            inv.scan_html(text, f)
        else:
            inv.scan_jsx(text, f)
    result = OrderedDict([("filesScanned", len(files)),
                          ("tokenDefinitions", inv.token_definitions),
                          ("tokenReferences", inv.token_references)])
    total = 0
    cats = OrderedDict()
    for cat in inv.CATS:
        values = sorted(inv.counts[cat].items(), key=lambda kv: (-kv[1], kv[0]))
        occ = sum(n for _v, n in values)
        total += occ
        cats[cat] = OrderedDict([("unique", len(values)), ("occurrences", occ),
                                 ("values", [OrderedDict([("value", v), ("count", n)]) for v, n in values])])
    cats["colors"]["nearDuplicates"] = near_duplicate_colors([v["value"] for v in cats["colors"]["values"]])
    result["rawLiterals"] = total
    result["inventory"] = cats
    result["files"] = [OrderedDict([("file", f), ("literals", n)]) for f, n in
                       sorted(inv.files.items(), key=lambda kv: (-kv[1], kv[0]))]
    if tokens_doc is not None:
        token_colors = {}
        for tid in (theme_ids(tokens_doc) or [None]):
            for tok in color_tokens(tokens_doc):
                col, lit, err = resolve_color(tokens_doc, tok["name"], tid)
                if col is not None:
                    token_colors.setdefault(col.to_css(), tok["name"])
        token_vals = {"fontSizes": {}, "spacing": {}, "radii": {}, "durations": {}, "fontFamilies": {}}
        for fam in family_keys(tokens_doc):
            cat = {"spacing": "spacing", "radius": "radii", "motion": "durations"}.get(fam)
            if cat is None:
                continue
            for t in list_family_tokens(tokens_doc, fam):
                if isinstance(t.get("value"), str) and isinstance(t.get("name"), str):
                    token_vals[cat].setdefault(t["value"].strip(), t["name"])
        for _g, s in type_styles(tokens_doc):
            if isinstance(s.get("fontSize"), str):
                token_vals["fontSizes"].setdefault(s["fontSize"].strip(), s.get("name"))
        matched = 0
        for cat, data in cats.items():
            for entry in data["values"]:
                name = token_colors.get(entry["value"]) if cat == "colors" else token_vals.get(cat, {}).get(entry["value"])
                if name:
                    entry["token"] = name
                    matched += entry["count"]
        result["literalsWithToken"] = matched
        result["literalsWithoutToken"] = total - matched
    return result


# --------------------------------------------------------------------------
# init: a small first system
# --------------------------------------------------------------------------

def starter_tokens(name):
    """A neutral first system. Every value is a starter default, not a brand decision."""
    def c(n, light, dark, usage):
        return OrderedDict([("name", n), ("value", OrderedDict([("light", light), ("dark", dark)])), ("usage", usage)])

    def t(n, value, usage):
        return OrderedDict([("name", n), ("value", value), ("usage", usage)])

    def s(n, size, lh, weight, usage):
        return OrderedDict([("name", n), ("fontSize", size), ("lineHeight", lh), ("fontWeight", weight), ("usage", usage)])

    doc = OrderedDict([("name", name), ("version", "0.1.0")])
    doc["color"] = OrderedDict([
        ("themes", [OrderedDict([("id", "light"), ("name", "Light")]),
                    OrderedDict([("id", "dark"), ("name", "Dark")])]),
        ("tokens", [
            c("bg", "#ffffff", "#111318", "Page ground."),
            c("surface", "#f3f4f6", "#1c1f26", "Raised ground for cards, panels and inputs."),
            c("border", "#7c828d", "#7b8290", "Control outlines and dividers. Border on bg and surface."),
            c("text", "#17191e", "#eceef2", "Headings and body copy. Text on bg and surface."),
            c("text-muted", "#565c68", "#a8aeb9", "Secondary copy and captions. Text on bg and surface."),
            c("accent", "#1d55b0", "#8fb4ff",
              "The one primary action in a view, links and the focus ring. Text on bg and surface."),
            c("on-accent", "#ffffff", "#0c1a33", "Label of a filled accent control. Text on accent."),
            c("danger", "#b3261e", "#ffb4ab",
              "Error text and destructive actions. Always pair it with a word or an icon. Text on bg and surface."),
        ])])
    doc["type"] = OrderedDict([
        ("fonts", []),
        ("families", OrderedDict([
            ("sans", "system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif"),
            ("mono", "ui-monospace, SFMono-Regular, Menlo, Consolas, \"Liberation Mono\", monospace")])),
        ("groups", [
            OrderedDict([("name", "Headings"), ("family", "sans"), ("styles", [
                s("display", "40px", 1.1, 700, "One hero headline in a view."),
                s("heading", "28px", 1.2, 700, "Page and section titles."),
                s("title", "20px", 1.3, 600, "Card titles and dialog titles.")])]),
            OrderedDict([("name", "Text"), ("family", "sans"), ("styles", [
                s("body", "16px", 1.5, 400, "All running text. The base size."),
                s("small", "14px", 1.45, 400, "Secondary text, table cells and form help."),
                s("caption", "12px", 1.4, 500, "Labels, captions and metadata. Never for running text.")])]),
            OrderedDict([("name", "Code"), ("family", "mono"), ("styles", [
                s("code", "14px", 1.5, 400, "Code, identifiers and numbers that must align.")])]),
        ])])
    doc["spacing"] = OrderedDict([("tokens", [
        t("space-1", "4px", "Gap between an icon and its label."),
        t("space-2", "8px", "Gap inside a control; gap between related items."),
        t("space-3", "16px", "Padding of cards and inputs; gap between form fields."),
        t("space-4", "32px", "Gap between sections; page gutter on wide screens."),
    ])])
    doc["radius"] = OrderedDict([("tokens", [
        t("radius-sm", "4px", "Tags, chips and small controls."),
        t("radius-md", "8px", "Buttons, inputs and cards."),
        t("radius-full", "999px", "Pills and avatars."),
    ])])
    doc["shadow"] = OrderedDict([("tokens", [
        t("shadow-sm", "0 1px 2px rgba(23, 25, 30, 0.08)", "Inputs and resting cards."),
        t("shadow-md", "0 4px 12px rgba(23, 25, 30, 0.12)", "Menus, popovers and raised cards."),
    ])])
    doc["motion"] = OrderedDict([("tokens", [
        t("duration-fast", "120ms", "Hover and press feedback on controls."),
        t("duration-base", "200ms", "Menus, dialogs and panels that enter or leave."),
        t("ease-standard", "cubic-bezier(0.2, 0, 0, 1)", "Default easing for every transition. No springs."),
    ])])
    return doc


def starter_readme(name):
    return """%(name)s is a design system. TODO: Replace this paragraph. Say in two or three sentences what the brand is, who it serves, and the one feeling every surface must carry.

## Content fundamentals

- TODO: Name the voice in three adjectives. Give one sentence of proof for each.
- TODO: State the casing for headings, buttons and labels.
- TODO: State the person (we, you) and the emoji policy.
- TODO: Paste three real lines of copy: a headline, a button label and an error message.

## Visual foundations

### Color

- Use `bg` for the page ground and `surface` for raised ground.
- Set headings and body copy in `text`. Set secondary copy in `text-muted`.
- Use `accent` for the one primary action in a view, for links and for the focus ring.
- Set the label of a filled `accent` control in `on-accent`.
- Use `danger` for errors and destructive actions. Pair it with a word or an icon.
- Draw control outlines and dividers in `border`.
- Switch theme with `data-theme="light"` or `data-theme="dark"` on the root element.

### Type

- Set running text in `body`. Use `small` for secondary text and `caption` for labels.
- Use `display` once in a view. Use `heading` for page and section titles and `title` for cards.
- Set code and aligned numbers in `code`.
- TODO: Name the brand typefaces and add their files under `fonts/`. The starter uses system fonts.

### Spacing, shape and depth

- Space with `space-1` to `space-4` only. Use `space-3` inside cards and `space-4` between sections.
- Round controls and cards with `radius-md`. Use `radius-sm` for tags and `radius-full` for pills.
- Keep surfaces flat. Use `shadow-sm` for resting cards and `shadow-md` for menus and popovers.

### Motion

- Use `duration-fast` for hover and press feedback and `duration-base` for panels that enter or leave.
- Ease every transition with `ease-standard`. Do not use springs or bounces.
- Remove motion when the user asks for reduced motion.

## Iconography

- TODO: Name the icon set, the stroke weight and the sizes. State the license and where the files live.
- Do not redraw a logo. Use the supplied files under `assets/`.

## Usage rules

- Take every color, size, space, radius and duration from a token in `tokens.json`.
- Add a token before you use a new value. Give it a usage note.
- Keep each text and ground pair at 4.5:1 or more in every theme. Large text and outlines need 3:1.
- Do not show a status by color alone.
- TODO: Add the brand's own do and do not rules.
""" % {"name": name}


def starter_source(name):
    return """# Sources for %(name)s

This file records where each value in the pack came from. A value with no source is not a brand fact.

| Part | Source | Date read | Status |
| --- | --- | --- | --- |
| Color tokens | ds.py init starter defaults | TODO | INFERRED: replace with brand values |
| Type styles and families | ds.py init starter defaults | TODO | INFERRED: replace with brand values |
| Spacing, radius, shadow, motion | ds.py init starter defaults | TODO | INFERRED: replace with brand values |
| README brand book | TODO | TODO | TODO |
| Logo and other assets | TODO | TODO | TODO |

## INFERRED values

List every value that was estimated, sampled by eye or chosen by the agent. Ask the owner to confirm each one.

- All starter token values. They come from the scaffold, not from the brand.

## Confirmed by the owner

- TODO: Move a line here when the owner confirms it. Add the date.
""" % {"name": name}


COMPONENTS_NOTE = """# Components

Put one folder here for each component: `components/<Name>/README.md` and `components/<Name>/preview.html`.

- The README says when to use the component and what the consumer provides: props, children, container and data.
- The preview shows every state: default, hover, focus, active or selected, disabled, error, loading and empty where they apply.
- The preview takes every value from the tokens.

Read `references/components.md` in the design-system skill for the full contract.
"""

ASSETS_NOTE = """# Assets

Put brand files here in one folder for each group: `assets/Logos/`, `assets/Icons/`, `assets/Imagery/`.

Record every file in the table below before you use it. Copy a supplied file. Never redraw or approximate a mark.

| File | Group | What it is | Source | License | Attribution | Date added |
| --- | --- | --- | --- | --- | --- | --- |

A file with no source and no license line is not cleared for use.
"""


def cmd_init(args):
    target = args.dir
    files = OrderedDict()
    doc = starter_tokens(args.name)
    readme = starter_readme(args.name)
    files["tokens.json"] = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    files["README.md"] = readme
    design, _f = build_design_md(doc, readme)
    files["DESIGN.md"] = design
    css, _f = build_css(doc)
    files["tokens.css"] = css
    files["SOURCE.md"] = starter_source(args.name)
    files[os.path.join("components", "README.md")] = COMPONENTS_NOTE
    files[os.path.join("assets", "README.md")] = ASSETS_NOTE
    existing = [p for p in files if os.path.exists(os.path.join(target, p))]
    if existing and not args.force:
        return fail(args, "init would overwrite: %s. Pass --force to replace them." % ", ".join(existing))
    for rel, text in files.items():
        write_text(os.path.join(target, rel), text)
    findings = validate_doc(doc)
    payload = OrderedDict([("ok", not has_errors(findings)), ("dir", target),
                           ("written", [os.path.join(target, p) for p in files]), ("findings", findings)])
    lines = ["Wrote %d files to %s" % (len(files), target)] + ["  " + p for p in files]
    lines.append("Next: replace the starter values and every TODO, then run validate and contrast.")
    return emit(args, payload, lines, 1 if has_errors(findings) else 0)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def emit(args, payload, lines, code):
    if getattr(args, "json", False):
        sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write("\n".join(lines) + "\n")
    return code


def fail(args, message, code=2):
    if getattr(args, "json", False):
        sys.stdout.write(json.dumps({"ok": False, "error": message}, indent=2) + "\n")
    else:
        sys.stderr.write("ds.py: %s\n" % message)
    return code


def format_findings(findings):
    lines = []
    for f in findings:
        lines.append("%s %s at %s" % (f["level"].upper(), f["code"], f["path"]))
        lines.append("  %s" % f["message"])
        lines.append("  Fix: %s" % f["hint"])
    return lines


def load_tokens(args, path):
    try:
        return read_json(path), None
    except (IOError, OSError) as exc:
        return None, fail(args, "cannot read %s: %s" % (path, exc))
    except ValueError as exc:
        return None, fail(args, "%s is not valid JSON: %s" % (path, exc))


def guarded(args, path, writer, owner_check, backups):
    """Run safe_write for one output. Return None on success, or the exit code of a refusal."""
    try:
        backup = safe_write(path, writer, getattr(args, "force", False), owner_check)
    except WriteRefused as exc:
        return fail(args, str(exc), 2)
    if backup:
        backups.append(backup)
    return None


def cmd_validate(args):
    doc, err = load_tokens(args, args.tokens)
    if doc is None:
        return err
    findings = validate_doc(doc) + scaffold_findings(doc)
    errors = [f for f in findings if f["level"] == "error"]
    warnings = [f for f in findings if f["level"] == "warning"]
    bad = bool(errors) or (args.strict and bool(warnings))
    payload = OrderedDict([("ok", not bad), ("file", args.tokens), ("errors", len(errors)),
                           ("warnings", len(warnings)), ("findings", findings)])
    lines = format_findings(findings)
    lines.append("%s: %d error(s), %d warning(s)" % (args.tokens, len(errors), len(warnings)))
    return emit(args, payload, lines, 1 if bad else 0)


def cmd_from_css(args):
    texts = []
    for p in args.css:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                texts.append(fh.read())
        except (IOError, OSError) as exc:
            return fail(args, "cannot read %s: %s" % (p, exc))
    doc, report = css_to_tokens(texts, args.name, base_theme=args.base_theme,
                                file_names=[os.path.basename(p) for p in args.css], no_alias=args.no_alias)
    if len(family_keys(doc)) == 0:
        return fail(args, "no custom property could be converted", 1)
    backups = []
    refused = guarded(args, args.output, lambda path: write_json(path, doc), never_owned, backups)
    if refused is not None:
        return refused
    findings = validate_doc(doc)
    bad = bool(report["unconverted"]) or has_errors(findings)
    payload = OrderedDict([("ok", not bad), ("output", args.output), ("backups", backups), ("report", report),
                           ("findings", findings)])
    lines = ["Wrote %s" % args.output] + ["Kept the old file as %s" % b for b in backups]
    lines.append("Converted: " + ", ".join("%s %d" % kv for kv in report["converted"].items()))
    for c in report["computed"]:
        lines.append("COMPUTED %s (%s): %s -> %s" % (c["name"], ", ".join(c["themes"]), c["from"], c["to"]))
    for a in report["assumed"]:
        lines.append("ASSUMED %s" % a)
    for s in report["skipped"]:
        lines.append("SKIPPED --%s in '%s': %s" % (s["name"], s["scope"], s["reason"]))
    for u in report["unconverted"]:
        lines.append("NOT CONVERTED --%s%s = %s: %s" % (
            u["name"], " (%s)" % u["theme"] if u.get("theme") else "", u["value"], u["reason"]))
    errs = [f for f in findings if f["level"] == "error"]
    lines.extend(format_findings(errs))
    lines.append("%d not converted, %d skipped, %d validation error(s), %d warning(s). Usage notes are yours to write." % (
        len(report["unconverted"]), len(report["skipped"]), len(errs), len(findings) - len(errs)))
    return emit(args, payload, lines, 1 if bad else 0)


def cmd_from_dtcg(args):
    dtcg, err = load_tokens(args, args.dtcg)
    if dtcg is None:
        return err
    theme_files = []
    for spec in args.theme or []:
        if "=" not in spec:
            return fail(args, "--theme needs id=file, got %r" % spec)
        tid, path = spec.split("=", 1)
        other, err = load_tokens(args, path)
        if other is None:
            return err
        theme_files.append((tid, other))
    doc, report = dtcg_to_claude(dtcg, name=args.name, theme_id=args.theme_id, theme_files=theme_files)
    if not family_keys(doc):
        return fail(args, "no token could be converted", 1)
    backups = []
    refused = guarded(args, args.output, lambda path: write_json(path, doc), never_owned, backups)
    if refused is not None:
        return refused
    findings = validate_doc(doc)
    bad = bool(report["unconverted"]) or has_errors(findings)
    payload = OrderedDict([("ok", not bad), ("output", args.output), ("backups", backups), ("report", report),
                           ("findings", findings)])
    lines = ["Wrote %s" % args.output] + ["Kept the old file as %s" % b for b in backups] + [
             "Converted: " + ", ".join("%s %d" % kv for kv in report["converted"].items())]
    lines += ["NOTE %s" % n for n in report["notes"]]
    lines += ["NOT CONVERTED %s: %s" % (u["name"], u["reason"]) for u in report["unconverted"]]
    lines.extend(format_findings([f for f in findings if f["level"] == "error"]))
    return emit(args, payload, lines, 1 if bad else 0)


def cmd_to_dtcg(args):
    doc, err = load_tokens(args, args.tokens)
    if doc is None:
        return err
    findings = validate_doc(doc)
    if has_errors(findings):
        errs = [f for f in findings if f["level"] == "error"]
        payload = OrderedDict([("ok", False), ("findings", errs)])
        return emit(args, payload, format_findings(errs) + ["Nothing written. Fix the token file first."], 1)
    out, notes = claude_to_dtcg(doc)
    backups = []
    refused = guarded(args, args.output, lambda path: write_json(path, out), dtcg_owned, backups)
    if refused is not None:
        return refused
    payload = OrderedDict([("ok", True), ("output", args.output), ("backups", backups), ("notes", notes)])
    lines = ["Wrote %s (DTCG 2025.10 object forms; themes are kept under $extensions.gdh)" % args.output]
    lines += ["Kept the old file as %s" % b for b in backups]
    lines += ["NOTE %s" % n for n in notes]
    return emit(args, payload, lines, 0)


def cmd_export(args):
    if not (args.css or args.tailwind or args.flat_json):
        return fail(args, "give at least one of --css, --tailwind, --json-out")
    doc, err = load_tokens(args, args.tokens)
    if doc is None:
        return err
    findings = [f for f in validate_doc(doc) if f["level"] == "error"]
    src = os.path.basename(args.tokens)
    written = []
    if args.theme_selector and "{id}" not in args.theme_selector:
        return fail(args, "--theme-selector needs {id} where the theme id goes, such as '.{id}'")
    if not findings:
        css, cfind = build_css(doc, src, theme_selector=args.theme_selector, media=not args.no_media)
        findings.extend(cfind)
    if findings:
        payload = OrderedDict([("ok", False), ("findings", findings)])
        return emit(args, payload, format_findings(findings) + ["Nothing written. Fix the token file first."], 1)
    outputs = []
    if args.css:
        outputs.append((args.css, lambda path: write_text(path, css), head_marked))
    if args.tailwind:
        tailwind = build_tailwind(doc, src)
        outputs.append((args.tailwind, lambda path: write_text(path, tailwind), head_marked))
    if args.flat_json:
        flat = build_flat(doc)
        outputs.append((args.flat_json, lambda path: write_json(path, flat), flat_owned(theme_ids(doc))))
    # Check every target before the first write, so a refusal leaves no half-written export.
    if not args.force:
        for path, _writer, check in outputs:
            if os.path.lexists(path) and (os.path.islink(path) or not os.path.isfile(path) or not check(path)):
                return fail(args, "%s exists and ds.py did not write it. Pass --force to replace a file ds.py "
                                  "did not write; the old file is kept as %s.bak. Nothing written." % (path, path), 2)
    backups = []
    for path, writer, check in outputs:
        refused = guarded(args, path, writer, check, backups)
        if refused is not None:
            return refused
        written.append(path)
    payload = OrderedDict([("ok", True), ("written", written), ("backups", backups)])
    return emit(args, payload, ["Wrote %s" % w for w in written] + ["Kept the old file as %s" % b for b in backups], 0)


def cmd_contrast(args):
    doc, err = load_tokens(args, args.tokens)
    if doc is None:
        return err
    try:
        pairs = pairs_from_file(args.pairs) if args.pairs else pairs_from_usage(doc)
    except (IOError, OSError, ValueError, KeyError, TypeError) as exc:
        return fail(args, "cannot read pairs: %s" % exc)
    if not pairs:
        payload = OrderedDict([("ok", False), ("pairs", 0), ("results", []),
                               ("error", "no pairs found")])
        return emit(args, payload, [
            "No pairs found. Write usage notes such as \"Text on bg and surface.\" on the text colors,",
            "or pass --pairs with lines of the form: <fg> on <bg> [text|large|ui]"], 1)
    results = check_contrast(doc, pairs)
    fails = [r for r in results if not r["pass"]]
    if not results:
        fails = [OrderedDict([("error", "no check ran")])]
    payload = OrderedDict([("ok", not fails), ("pairs", len(pairs)), ("checked", len(results)),
                           ("failed", len(fails)), ("thresholds", OrderedDict([("text", AA_NORMAL), ("large", AA_LARGE), ("ui", AA_LARGE)])),
                           ("results", results)])
    lines = []
    for r in results:
        if r.get("ratio") is None:
            lines.append("FAIL  %-8s %s on %s: %s" % (r["theme"], r["fg"], r["bg"], r.get("error")))
            continue
        lines.append("%s  %-8s %s on %s  %.2f:1  needs %s:1 (%s)  normal text %s, large text %s" % (
            "PASS" if r["pass"] else "FAIL", r["theme"], r["fg"], r["bg"], r["ratio"],
            fmt_num(r["required"], 1), r["kind"],
            "pass" if r["passNormalText"] else "fail", "pass" if r["passLargeText"] else "fail"))
    lines.append("%d pair(s), %d check(s), %d failed. Thresholds: 4.5:1 normal text; 3:1 large text and control outlines." % (
        len(pairs), len(results), len(fails)))
    return emit(args, payload, lines, 1 if fails else 0)


DESIGN_MD_MARK = "by `ds.py design-md`"


def design_md_replaceable(path):
    """Return True when path is absent, was written by design-md, or is the unfilled project template."""
    if not os.path.lexists(path):
        return True
    if os.path.islink(path) or not os.path.isfile(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except (IOError, OSError, UnicodeDecodeError):
        return False
    if DESIGN_MD_MARK in text:
        return True
    front = re.match(r"\A---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    return bool(front and re.search(r"(?m)^status:\s*[\"']?template[\"']?\s*$", front.group(1)))


def cmd_design_md(args):
    doc, err = load_tokens(args, args.tokens)
    if doc is None:
        return err
    findings = [f for f in validate_doc(doc) if f["level"] == "error"]
    if findings:
        payload = OrderedDict([("ok", False), ("findings", findings)])
        return emit(args, payload, format_findings(findings) + ["Nothing written. Fix the token file first."], 1)
    readme = None
    if args.readme:
        try:
            with open(args.readme, "r", encoding="utf-8") as fh:
                readme = fh.read()
        except (IOError, OSError) as exc:
            return fail(args, "cannot read %s: %s" % (args.readme, exc))
    if not getattr(args, "force", False) and not design_md_replaceable(args.output):
        return fail(args, "%s exists and was not written by ds.py design-md. A hand-written DESIGN.md holds "
                          "rules that tokens cannot rebuild. Write to another path and merge by hand, "
                          "or pass --force to replace it (the old file is kept as %s.bak)."
                    % (args.output, args.output))
    text, findings = build_design_md(doc, readme, os.path.basename(args.tokens),
                                     os.path.basename(args.readme) if args.readme else "README.md")
    backups = []
    refused = guarded(args, args.output, lambda path: write_text(path, text), design_md_replaceable, backups)
    if refused is not None:
        return refused
    payload = OrderedDict([("ok", True), ("output", args.output), ("backups", backups), ("findings", findings)])
    return emit(args, payload, ["Wrote %s" % args.output] + ["Kept the old file as %s" % b for b in backups] +
                format_findings(findings), 0)


def cmd_specimen(args):
    doc, err = load_tokens(args, args.tokens)
    if doc is None:
        return err
    findings = [f for f in validate_doc(doc) if f["level"] == "error"]
    if findings:
        payload = OrderedDict([("ok", False), ("findings", findings)])
        return emit(args, payload, format_findings(findings) + ["Nothing written. Fix the token file first."], 1)
    text, findings = build_specimen(doc, google_fonts=args.google_fonts, source_name=os.path.basename(args.tokens))
    errors, external = check_html(text)
    for e in errors:
        findings.append(finding("SPECIMEN_HTML", "error", args.output, e, "Report this as a ds.py defect."))
    backups = []
    refused = guarded(args, args.output, lambda path: write_text(path, text), head_marked, backups)
    if refused is not None:
        return refused
    bad = has_errors(findings)
    payload = OrderedDict([("ok", not bad), ("output", args.output), ("backups", backups),
                           ("externalRequests", external), ("findings", findings)])
    lines = ["Wrote %s" % args.output] + ["Kept the old file as %s" % b for b in backups] + [
             "External requests: %s" % (", ".join(external) if external else "none")]
    return emit(args, payload, lines + format_findings(findings), 1 if bad else 0)


def cmd_audit(args):
    tokens_doc = None
    if args.tokens:
        tokens_doc, err = load_tokens(args, args.tokens)
        if tokens_doc is None:
            return err
    try:
        result = run_audit(args.paths, tokens_doc)
    except (IOError, OSError) as exc:
        return fail(args, str(exc))
    code = 0 if (args.inventory or result["rawLiterals"] == 0) else 1
    result = OrderedDict([("ok", code == 0)] + list(result.items()))
    lines = ["Files scanned: %d" % result["filesScanned"],
             "Token definitions (custom properties): %d. Token references (var()): %d." % (
                 result["tokenDefinitions"], result["tokenReferences"]),
             "Raw literals that bypass tokens: %d" % result["rawLiterals"]]
    labels = OrderedDict([("colors", "colors"), ("fontSizes", "font sizes"), ("fontFamilies", "font families"),
                          ("spacing", "spacing values"), ("radii", "radius values"), ("durations", "durations")])
    for cat, label in labels.items():
        data = result["inventory"][cat]
        lines.append("  %d unique %s in %d use(s)" % (data["unique"], label, data["occurrences"]))
        for entry in data["values"][:args.top]:
            lines.append("    %4d  %s%s" % (entry["count"], entry["value"],
                                            "  (token %s exists)" % entry["token"] if entry.get("token") else ""))
        if len(data["values"]) > args.top:
            lines.append("    ... %d more (use --json for all)" % (len(data["values"]) - args.top))
    groups = result["inventory"]["colors"]["nearDuplicates"]
    if groups:
        lines.append("Near-duplicate colors (merge candidates):")
        for g in groups[:args.top]:
            lines.append("    " + "  ".join(g))
    if "literalsWithToken" in result:
        lines.append("Literals that match an existing token value: %d. Literals with no token: %d." % (
            result["literalsWithToken"], result["literalsWithoutToken"]))
    for entry in result["files"][:args.top]:
        lines.append("  %4d  %s" % (entry["literals"], entry["file"]))
    return emit(args, result, lines, code)


def build_parser():
    p = argparse.ArgumentParser(
        prog="ds.py", description="Design system tooling for the Claude Design System tokens.json shape.")
    p.add_argument("--version", action="version", version="ds.py " + VERSION)
    sub = p.add_subparsers(dest="command")

    def add(name, func, help_text):
        sp = sub.add_parser(name, help=help_text, description=help_text)
        sp.add_argument("--json", action="store_true", help="print one JSON object on stdout")
        sp.set_defaults(func=func)
        return sp

    sp = add("init", cmd_init, "Scaffold a small first system in a folder.")
    sp.add_argument("dir")
    sp.add_argument("--name", required=True)
    sp.add_argument("--force", action="store_true", help="replace existing files")

    sp = add("validate", cmd_validate, "Check a tokens.json against the Claude Design System grammar.")
    sp.add_argument("tokens")
    sp.add_argument("--strict", action="store_true", help="fail on warnings too")

    sp = add("from-css", cmd_from_css, "Read CSS custom properties and write a tokens.json.")
    sp.add_argument("css", nargs="+")
    sp.add_argument("--name", required=True)
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--base-theme", help="theme id of the :root block (default: light)")
    sp.add_argument("--no-alias", action="store_true", help="write literals instead of {alias} values")
    sp.add_argument("--force", action="store_true",
                    help="replace an existing file that ds.py did not write; the old file is kept as <path>.bak")

    sp = add("from-dtcg", cmd_from_dtcg, "Convert a W3C Design Tokens (DTCG) file to the Claude shape.")
    sp.add_argument("dtcg")
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--name")
    sp.add_argument("--theme-id", default="light", help="theme id of the main file (default: light)")
    sp.add_argument("--theme", action="append", metavar="ID=FILE", help="another DTCG file that holds one more theme")
    sp.add_argument("--force", action="store_true",
                    help="replace an existing file that ds.py did not write; the old file is kept as <path>.bak")

    sp = add("to-dtcg", cmd_to_dtcg, "Convert a Claude-shape tokens.json to a DTCG file.")
    sp.add_argument("tokens")
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--force", action="store_true",
                    help="replace an existing file that ds.py did not write; the old file is kept as <path>.bak")

    sp = sub.add_parser("export", help="Write tokens.css, a Tailwind v4 theme and a flat JSON.",
                        description="Write tokens.css, a Tailwind v4 theme and a flat JSON.")
    sp.add_argument("tokens")
    sp.add_argument("--css", help="output path for tokens.css")
    sp.add_argument("--tailwind", help="output path for a Tailwind v4 @theme file")
    sp.add_argument("--json", dest="flat_json", metavar="OUT.json", help="output path for the flat JSON")
    sp.add_argument("--report-json", dest="json", action="store_true", help="print one JSON object on stdout")
    sp.add_argument("--theme-selector", metavar="SELECTOR",
                    help="selector for each theme block, with {id}, such as '.{id}' (default: the selectors "
                         "from-css recorded, else [data-theme=\"{id}\"])")
    sp.add_argument("--no-media", action="store_true", help="leave out the prefers-color-scheme block")
    sp.add_argument("--force", action="store_true",
                    help="replace an existing file that ds.py did not write; the old file is kept as <path>.bak")
    sp.set_defaults(func=cmd_export)

    sp = add("contrast", cmd_contrast, "WCAG 2.x contrast of text-on-ground pairs in every theme.")
    sp.add_argument("tokens")
    sp.add_argument("--pairs", help="pairs file: JSON list or lines '<fg> on <bg> [text|large|ui]'")

    sp = add("design-md", cmd_design_md, "Write a DESIGN.md with YAML front matter from the tokens.")
    sp.add_argument("tokens")
    sp.add_argument("--readme", help="brand book to take prose sections from")
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--force", action="store_true",
                    help="replace an existing DESIGN.md that ds.py did not write (default: refuse)")

    sp = add("specimen", cmd_specimen, "Write one self-contained HTML specimen page.")
    sp.add_argument("tokens")
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--google-fonts", action="store_true",
                    help="add one Google Fonts link for the families named in the tokens")
    sp.add_argument("--force", action="store_true",
                    help="replace an existing file that ds.py did not write; the old file is kept as <path>.bak")

    sp = add("audit", cmd_audit, "Count raw color, size and duration literals that bypass tokens.")
    sp.add_argument("paths", nargs="+")
    sp.add_argument("--tokens", help="mark literals that match a value in this tokens.json")
    sp.add_argument("--inventory", action="store_true", help="measure only; exit 0 even when literals exist")
    sp.add_argument("--top", type=int, default=12, help="values to list for each category (default 12)")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
