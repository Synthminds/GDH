#!/usr/bin/env python3
"""GDH engine: check, build, export, doctor, new-tool, new-skill.

Python 3.9 standard library only. The script makes no network call.
It writes only under --root (build, new-tool, new-skill) or --repo (export).
Exit code 0 means pass. Exit code 1 means findings.
"""
import argparse
import datetime
import fnmatch
import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT_DEFAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# One code for each rule. tests/test_gdh.py holds one mutation test for each code.
CODES = {
    "GDH_JSON_INVALID": "A JSON file does not parse.",
    "GDH_KIT_JSON": "kit.json is missing or does not match the registry schema.",
    "GDH_AGENT_REGISTRY": "The agents list in kit.json and the files in kit/agents differ.",
    "GDH_FRONTMATTER": "A SKILL.md has no readable frontmatter block.",
    "GDH_SKILL_NAME": "A skill name is not kebab-case or is longer than 64 characters.",
    "GDH_SKILL_NAME_FOLDER": "A skill name differs from its folder name.",
    "GDH_SKILL_DESCRIPTION": "A skill description is absent or is not 1 to 1024 characters.",
    "GDH_DESCRIPTION_BUDGET": "The model-invoked descriptions exceed budgets.modelDescriptionChars.",
    "GDH_REGISTRY_MISSING_FOLDER": "A registered skill has no folder with a SKILL.md.",
    "GDH_REGISTRY_UNREGISTERED": "A skill folder is not registered in kit.json.",
    "GDH_INVOCATION_FLAG": "disable-model-invocation does not agree with the registered invocation.",
    "GDH_SKILL_SIZE": "A SKILL.md exceeds 150 lines or 1,500 words.",
    "GDH_REFERENCE_SIZE": "A reference file exceeds 400 lines.",
    "GDH_LINK_BROKEN": "A relative Markdown link in kit/ or docs/ does not resolve.",
    "GDH_SKILL_FILE_UNLINKED": "A file in a skill folder is not linked from its SKILL.md.",
    "GDH_ROUTER_INCOMPLETE": "The ask-gdh skill does not name a registered skill.",
    "GDH_ROUTE_USER_SKILL": "A line starts a user-invoked skill as if the host could start it, or the kernel lacks "
                            "the skill handoff route.",
    "GDH_SYMLINK": "The repository holds a symbolic link.",
    "GDH_HTML_COMMENT": "A kit Markdown file holds an HTML comment.",
    "GDH_BASE64": "A kit Markdown file holds a base64 run of 80 or more characters.",
    "GDH_EMOJI": "A kit Markdown file holds an emoji.",
    "GDH_EM_DASH": "A kit Markdown file holds an em dash.",
    "GDH_PRINT_FLOOR": "A kit Markdown file sets 12 pt as the floor for all print or slide text; 12 pt is the body size.",
    "GDH_SECRET": "A file holds a key, a token, an email address or a uuid-like account id.",
    "GDH_PRIVATE_LINK": "A file holds a private Claude link, a workspace, team, organization or account id, or a "
                        "link to another repository of the kit's owner.",
    "GDH_SCRIPT_NETWORK": "A script imports a network module or calls a download program.",
    "GDH_KERNEL_MISSING": "kit/canon/KERNEL.md is absent.",
    "GDH_KERNEL_BUDGET": "KERNEL.md exceeds budgets.kernelLines.",
    "GDH_MOMENTS_BUDGET": "The rendered MOMENTS.md exceeds budgets.momentsChars.",
    "GDH_HOOK_BUDGET": "KERNEL.md and the rendered MOMENTS.md together exceed the SessionStart hook limit.",
    "GDH_MOMENT_SHAPE": "A moment has no 'when', a repeated 'when', or neither start nor offer.",
    "GDH_MOMENT_OFFER_LIMIT": "A moment offers more than 3 skills.",
    "GDH_MOMENT_SKILL_UNKNOWN": "A moment names a skill that is neither registered nor wired.",
    "GDH_MOMENT_START_USER": "A moment starts a skill that is not model-invoked.",
    "GDH_CAPABILITIES_SCHEMA": "capabilities.json is absent or malformed.",
    "GDH_CAPABILITIES_DISCIPLINE": "A discipline in capabilities.json names an unregistered skill.",
    "GDH_TOOL_FIELD": "A tool entry lacks a required field or a field has the wrong type.",
    "GDH_TOOL_ENUM": "A tool entry has a kind, auth or evidence value outside the allowed set.",
    "GDH_LOCAL_CLI": "local-clis.json breaks its schema: a pin, a path, a capability or an exposure flag.",
    "GDH_TOOL_ID": "A tool id differs from its file name or is not kebab-case.",
    "GDH_TOOL_CAPABILITY": "A tool names a capability outside the vocabulary.",
    "GDH_TOOL_DISCIPLINE": "A tool names a discipline that capabilities.json does not hold.",
    "GDH_TOOL_FALLBACK": "A tool fallback is neither an existing tool id nor 'none'.",
    "GDH_TOOL_CARD": "A tool card path is wrong or the card file is absent.",
    "GDH_TOOL_DATE": "A tool verifiedAt value is not an ISO date.",
    "GDH_TOOL_SOURCE": "A tool source is neither an https URL nor 'none'.",
    "GDH_ASSETS_FIELD": "assets.json is malformed or a source lacks a required field.",
    "GDH_ASSETS_DUPLICATE_ID": "Two asset sources share one id.",
    "GDH_ASSETS_DATE": "An asset source verifiedOn value is neither null nor an ISO date.",
    "GDH_ASSETS_URL": "An asset source url is not an https URL.",
    "GDH_BRAND_PACK": "A brand pack lacks README.md or tokens.json.",
    "GDH_BRAND_PUBLIC": "A private brand pack is not git-ignored, or a tracked .gitignore names one.",
    "GDH_BRAND_SCAFFOLD": "A brand pack still holds the starter colors that ds.py init writes.",
    "GDH_EVAL_CASE": "An eval case lacks a field, has a wrong kind, id or skill, or expects the wrong skills.",
    "GDH_GENERATED_DRIFT": "A generated file differs from the build output.",
    "GDH_ACCEPTED_INVALID": "A kit/scan.accepted.json entry is malformed or waives more than one finding.",
}

# Codes whose waiver must name one exact path. A glob would hide every later finding of the kind.
EXACT_WAIVER_CODES = ("GDH_SECRET", "GDH_PRIVATE_LINK", "GDH_SCRIPT_NETWORK", "GDH_SYMLINK", "GDH_BRAND_PUBLIC")
# Codes whose finding carries the sha256 of the matched line. Their waiver must repeat it in 'match'.
LINE_WAIVER_CODES = ("GDH_SECRET", "GDH_PRIVATE_LINK", "GDH_SCRIPT_NETWORK")
GLOB_CHARS = ("*", "?", "[")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

DOCTOR_CODES = {
    "GDH_DOCTOR_STALE": "A tool entry was verified more than 180 days ago.",
    "GDH_DOCTOR_UNTESTED": "A tool entry has the evidence label UNTESTED.",
    "GDH_DOCTOR_NO_CARD": "A tool has no card file.",
    "GDH_DOCTOR_CAPABILITY_NO_TOOL": "A capability has no tool in the catalog.",
    "GDH_DOCTOR_GATE_UNVERIFIED": "A capability that a gate depends on has no VERIFIED tool.",
    "GDH_DOCTOR_NO_EVAL": "A model-invoked skill has no triggering eval case.",
    "GDH_DOCTOR_NO_REFINEMENT_LOG": "A skill has no refinement-log.md.",
}

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}
BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".woff", ".woff2",
    ".ttf", ".otf", ".mp3", ".mp4", ".wav", ".glb", ".gltf", ".bin", ".pyc", ".mov", ".webm",
}
SCRIPT_EXT = {".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs", ".ts", ".mts", ".cts", ".rb", ".pl", ".ps1"}

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HTML_COMMENT_RE = re.compile(r"<!--")
BASE64_RE = re.compile(r"[A-Za-z0-9+/]{80,}")
EM_DASH = chr(0x2014)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")

SECRET_PATTERNS = [
    ("api key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("api key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("api key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("assigned secret", re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|passwd|password)\b\s*[:=]\s*[\"'][A-Za-z0-9_\-/+=.]{20,}[\"']")),
    ("uuid-like id", re.compile(
        r"(?i)(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![0-9a-f])")),
]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.([A-Za-z]{2,})\b")
EMAIL_ALLOWED = {"git@github.com", "git@gitlab.com", "git@bitbucket.org"}
EMAIL_ALLOWED_DOMAINS = ("@example.com", "@example.org", "@example.net")
EMAIL_FILE_TLDS = {"png", "jpg", "jpeg", "svg", "webp", "gif", "css", "js", "json", "md", "html", "avif", "ico"}

NETWORK_PATTERNS = [re.compile(p, re.M) for p in (
    r"urllib\.request",
    r"http\.client",
    # Every import form of a network module. urllib.parse alone makes no call, so it stays allowed.
    r"^\s*(?:import|from)\s+(?:http|socket|requests|httpx|aiohttp|ftplib|smtplib|imaplib|poplib|telnetlib"
    r"|ssl|xmlrpc|websocket|websockets|asyncio\.streams)\b",
    r"^\s*from\s+urllib\s+import\s+[^#\n]*\b(?:request|error)\b",
    r"\b(?:urlopen|create_connection|open_connection)\s*\(",
    r"\b__import__\(\s*['\"](?:urllib|http|socket|ssl|requests)",
    r"\bimport_module\(\s*['\"](?:urllib\.request|http|socket|ssl|requests)",
    r"\brequire\(\s*['\"](?:node:)?(?:https?|net|dgram|tls)['\"]",
    r"\bfrom\s+['\"](?:node:)?(?:https?|net|dgram|tls)['\"]",
    r"\brequests\.(?:get|post|put|delete|request|Session)\b",
    r"\b(?:cur[l]|wge[t])\b",
    r"\bfetch\(",
)]

# Private links and ids. The repository is public, so none may appear outside test fixtures.
PRIVATE_LINK_PATTERNS = [
    ("private Claude link", re.compile(
        r"(?i)\bclaude\.ai/(?:(?:artifacts?|code/artifact|public/artifacts|design/p|code/session|chat|project)/"
        r"|code/session_)[A-Za-z0-9][A-Za-z0-9_-]*")),
    ("workspace, team or account id", re.compile(r"\b(?:wsp|team|ws|acct)_(?=[A-Za-z0-9]*[0-9])[A-Za-z0-9]{6,}\b")),
    ("organization id", re.compile(r"\borg-(?=[A-Za-z0-9]*[0-9])[A-Za-z0-9]{12,}\b")),
]


def sibling_repo_pattern(repository):
    """Match a link to another repository of the kit's owner. Such a repository may be private.

    The kit's own repository stays allowed. A sibling that is public takes an exact-path waiver."""
    match = re.match(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?$", repository or "")
    if not match:
        return None
    owner, own = re.escape(match.group(1)), match.group(2).lower()
    pattern = re.compile(r"(?i)(?:github\.com[/:]|marketplace add\s+)%s/([A-Za-z0-9_.-]+)" % owner)

    def find(line):
        for found in pattern.finditer(line):
            name = found.group(1).lower()
            if name.endswith(".git"):
                name = name[:-4]
            if name.rstrip(".") != own:
                return True
        return False
    return find


# Brand packs that may live in the public tree. Every other pack must be git-ignored.
PUBLIC_BRANDS = ("_template", "example-harbor-lantern")
# kit/hooks/session_start.py prints at most this many characters. tests/test_gdh.py keeps the two equal.
HOOK_LIMIT = 9000

TOOL_KINDS = ("connector", "mcp-stdio", "plugin", "cli", "skill", "library", "artifact-type")
EVIDENCE = ("VERIFIED", "DOCUMENTED", "UNTESTED")
TOOL_STRINGS = ("id", "name", "what", "kind", "install", "auth", "toolPrefix", "firstCall", "fallback",
                "card", "source", "verifiedAt", "evidence", "evidenceNote")
TOOL_BOOLS = ("spendsCredits", "exposes", "readOnly")
TOOL_LISTS = ("capabilities", "disciplines")
ASSET_FIELDS = ("id", "name", "url", "group", "holds", "license", "attribution", "commercialUse", "fetch",
                "risk", "verifiedOn")
CARD_HEADINGS = (
    "What it makes", "Connection and auth", "Cost model", "Call order", "Key tools", "Inputs",
    "Outputs and how to bring them into a project", "Handoffs", "Limits and failure modes", "Best for",
    "Wrong for", "Evidence",
)
CATALOG_START = "[//]: # (gdh-catalog:start)"
CATALOG_END = "[//]: # (gdh-catalog:end)"
BLOCK_START = "[//]: # (gdh-kit:start)"
BLOCK_END = "[//]: # (gdh-kit:end)"
HOST_SKILL_DIRS = {"claude": ".claude/skills", "codex": ".agents/skills", "cursor": ".agents/skills",
                   "agents": ".agents/skills"}
# The only folders whose files export may own, update or remove. A manifest key outside them is refused.
MANAGED_PREFIXES = tuple(sorted(set(
    ["%s/" % d for d in HOST_SKILL_DIRS.values()] + [".claude/agents/"]
    + ["%s/%s/" % (d.rsplit("/", 1)[0], sub) for d in HOST_SKILL_DIRS.values()
       for sub in ("catalogs", "references", "canon")])))
# The only files whose marker block export may own.
MANAGED_BLOCK_FILES = ("AGENTS.md", "CLAUDE.md")
# Claude Code reads CLAUDE.md, not AGENTS.md, when a CLAUDE.md exists. This import loads the block.
CLAUDE_IMPORT = "@AGENTS.md"
MAX_OFFER = 3
NEGATIVE_SKILL = "none"
# Project templates that export never copies: the managed block in AGENTS.md carries their content.
TEMPLATE_SKIP = ("AGENTS.md", "AGENTS-block.md")
STALE_DAYS = 180
# Capabilities that a delivery gate depends on. Kernel rule 14 needs a rendered review of code.
GATE_CAPABILITIES = ("capture",)


# ---------------------------------------------------------------- helpers

def posix(path):
    return path.replace(os.sep, "/")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def read_text(path):
    """Return the text of a file, or None for a binary or unreadable file."""
    try:
        data = read_bytes(path)
    except OSError:
        return None
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def dump_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def iter_files(root, sub=""):
    """Yield repository-relative posix paths of regular files. Symlinks are left out."""
    base = os.path.join(root, sub) if sub else root
    if not os.path.isdir(base) or os.path.islink(base):
        return
    for current, dirs, files in os.walk(base, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not os.path.islink(os.path.join(current, d)))
        for name in sorted(files):
            full = os.path.join(current, name)
            if os.path.islink(full):
                continue
            yield posix(os.path.relpath(full, root))


def is_iso_date(value):
    if not isinstance(value, str) or not ISO_DATE_RE.match(value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return str(json.loads(value))
        except ValueError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(text):
    """Read the simple key: value frontmatter of a SKILL.md. Return (dict or None, body)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return None, text
    front, key = {}, None
    for line in lines[1:end]:
        if not line.strip():
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match and not line[0].isspace():
            key, value = match.group(1), match.group(2).strip()
            front[key] = "" if value in (">", ">-", ">+", "|", "|-", "|+") else unquote(value)
        elif key is not None and line[0].isspace():
            front[key] = (front[key] + " " + line.strip()).strip()
    return front, "\n".join(lines[end + 1:])


def strip_code(text):
    """Remove fenced code blocks and inline code spans."""
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            out.append(re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(out)


def md_links(text):
    """Return the relative link targets of a Markdown text."""
    targets = []
    for match in LINK_RE.finditer(strip_code(text)):
        target = match.group(1).strip("<>")
        if target.startswith("#") or SCHEME_RE.match(target) or "{" in target or "<" in target:
            continue
        target = target.split("#", 1)[0].split("?", 1)[0].replace("%20", " ")
        if target:
            targets.append(target)
    return targets


def resolve_link(root, rel_file, target):
    """Return the repository-relative path a link points at, or None when it leaves the root."""
    if target.startswith("/"):
        return None
    joined = os.path.normpath(os.path.join(os.path.dirname(rel_file), target))
    if joined.startswith("..") or os.path.isabs(joined):
        return None
    return posix(joined)


def has_emoji(text):
    for char in text:
        point = ord(char)
        if 0x1F000 <= point <= 0x1FAFF or 0x2600 <= point <= 0x27BF or point in (0x2B50, 0x2B55, 0x2B1B, 0x2B1C, 0xFE0F):
            return True
    return False


class Report(object):
    def __init__(self):
        self.findings = []
        self._seen = set()

    def add(self, code, path, message, match=None):
        """Record a finding once. 'match' is the sha256 of the matched line, for a one-line waiver."""
        key = (code, path, message)
        if key not in self._seen:
            self._seen.add(key)
            finding = {"code": code, "path": path, "message": message}
            if match:
                finding["match"] = match
            self.findings.append(finding)


def line_digest(line):
    """Return the sha256 that a waiver in kit/scan.accepted.json repeats in its 'match' field."""
    return sha256(line.strip().encode("utf-8"))


def safe_rel(rel):
    """Return True for a plain relative posix path: no drive, no backslash, no '.', '..' or empty part."""
    if not isinstance(rel, str) or not rel or "\\" in rel or "\x00" in rel:
        return False
    if rel.startswith("/") or re.match(r"^[A-Za-z]:", rel):
        return False
    return all(part not in ("", ".", "..") for part in rel.split("/"))


def inside(base, path):
    """Return True when path resolves strictly inside base, after symbolic links are resolved."""
    real_base, real = os.path.realpath(base), os.path.realpath(path)
    try:
        return real != real_base and os.path.commonpath([real_base, real]) == real_base
    except ValueError:
        return False


# ---------------------------------------------------------------- git-ignore rules
# A small reader of .gitignore patterns. It runs no git command, so check works without git.

def ignore_regex(pattern):
    out, index = [], 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            out.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("/**", index) and index + 3 == len(pattern):
            out.append("/.*")
            index += 3
        elif pattern.startswith("**", index):
            out.append(".*")
            index += 2
        elif pattern[index] == "*":
            out.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            out.append("[^/]")
            index += 1
        elif pattern[index] == "[" and "]" in pattern[index + 2:]:
            close = pattern.index("]", index + 2)
            body = pattern[index + 1:close]
            body = "^" + body[1:] if body[:1] in ("!", "^") else body
            out.append("[%s]" % body.replace("\\", "\\\\"))
            index = close + 1
        else:
            out.append(re.escape(pattern[index]))
            index += 1
    return re.compile("^%s$" % "".join(out))


def ignore_rules(root, folders=("", "brands")):
    """Read the .gitignore files of the given folders. Return [(base, anchored, dir_only, negate, regex)]."""
    rules = []
    for base in folders:
        text = read_text(os.path.join(root, base, ".gitignore"))
        for line in (text or "").split("\n"):
            line = line.rstrip("\r").rstrip()
            if not line or line.startswith("#"):
                continue
            negate = line.startswith("!")
            line = line[1:] if negate else line
            line = line[1:] if line.startswith("\\") else line
            dir_only = line.endswith("/")
            line = line.rstrip("/")
            if line:
                rules.append((base, "/" in line, dir_only, negate, ignore_regex(line.lstrip("/"))))
    return rules


def ignore_match(rules, rel, is_dir):
    state = False
    for base, anchored, dir_only, negate, regex in rules:
        if base and not rel.startswith(base + "/"):
            continue
        local = rel[len(base) + 1:] if base else rel
        if dir_only and not is_dir:
            continue
        if regex.match(local if anchored else local.rsplit("/", 1)[-1]):
            state = not negate
    return state


def is_ignored(rules, rel, is_dir):
    """Return True when git would ignore rel. An ignored parent folder ignores everything below it."""
    parts = rel.split("/")
    for depth in range(1, len(parts) + 1):
        if ignore_match(rules, "/".join(parts[:depth]), is_dir or depth < len(parts)):
            return True
    return False


class JsonCache(object):
    """Load each JSON file once. Report a parse failure once."""

    def __init__(self, root, report):
        self.root, self.report, self.cache = root, report, {}

    def __call__(self, rel):
        if rel not in self.cache:
            path = os.path.join(self.root, rel)
            data = None
            if os.path.isfile(path):
                try:
                    data = json.loads(read_bytes(path).decode("utf-8"))
                except (ValueError, UnicodeDecodeError) as error:
                    self.report.add("GDH_JSON_INVALID", rel, "does not parse: %s" % error)
            self.cache[rel] = data
        return self.cache[rel]


def load_kit(root):
    path = os.path.join(root, "kit", "kit.json")
    try:
        data = json.loads(read_bytes(path).decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def kit_problems(kit):
    """Return the schema problems of a kit.json value."""
    problems = []
    for key in ("name", "displayName", "version", "description", "repository", "license"):
        if not isinstance(kit.get(key), str) or not kit.get(key):
            problems.append("'%s' must be a non-empty string" % key)
    budgets = kit.get("budgets")
    for key in ("modelDescriptionChars", "kernelLines", "momentsChars"):
        value = budgets.get(key) if isinstance(budgets, dict) else None
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            problems.append("budgets.%s must be a positive integer" % key)
    skills = kit.get("skills")
    if not isinstance(skills, dict) or not skills:
        problems.append("'skills' must be a non-empty object")
        skills = {}
    for name, entry in skills.items():
        if not isinstance(entry, dict) or entry.get("invocation") not in ("model", "user"):
            problems.append("skill '%s' needs invocation 'model' or 'user'" % name)
        elif not isinstance(entry.get("origin"), str) or not isinstance(entry.get("discipline"), str):
            problems.append("skill '%s' needs string 'origin' and 'discipline'" % name)
    agents = kit.get("agents")
    if not isinstance(agents, list) or any(not isinstance(a, str) for a in agents):
        problems.append("'agents' must be a list of names")
    if not isinstance(kit.get("moments"), list):
        problems.append("'moments' must be a list")
    wired = kit.get("wired")
    if not isinstance(wired, dict):
        problems.append("'wired' must be an object")
        wired = {}
    for wid, entry in wired.items():
        if wid in skills:
            problems.append("wired id '%s' equals a kit skill name" % wid)
        ok = isinstance(entry, dict) and all(isinstance(entry.get(k), str) and entry.get(k) for k in ("name", "what", "source"))
        install = entry.get("install") if isinstance(entry, dict) else None
        if isinstance(install, list):
            ok = ok and bool(install) and all(isinstance(i, str) and i for i in install)
        else:
            ok = ok and isinstance(install, str) and bool(install)
        if not ok:
            problems.append("wired entry '%s' needs name, what, install and source" % wid)
    if not isinstance(kit.get("requires", {}), dict):
        problems.append("'requires' must be an object")
    return problems


def safe_kit(kit):
    """Return a copy of kit.json with the container types that the renderers need."""
    out = dict(kit)
    out["skills"] = {k: v for k, v in (kit.get("skills") or {}).items() if isinstance(v, dict)} \
        if isinstance(kit.get("skills"), dict) else {}
    out["wired"] = {k: v for k, v in (kit.get("wired") or {}).items() if isinstance(v, dict)} \
        if isinstance(kit.get("wired"), dict) else {}
    out["moments"] = [m for m in kit.get("moments") or [] if isinstance(m, dict)] \
        if isinstance(kit.get("moments"), list) else []
    out["agents"] = [a for a in kit.get("agents") or [] if isinstance(a, str)] \
        if isinstance(kit.get("agents"), list) else []
    out["budgets"] = kit.get("budgets") if isinstance(kit.get("budgets"), dict) else {}
    return out


def names_list(value):
    return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []


def load_capabilities(data):
    """Normalize capabilities.json. Return (vocabulary list, disciplines dict) or (None, None)."""
    if not isinstance(data, dict):
        return None, None
    raw = data.get("capabilities")
    vocab = []
    if isinstance(raw, dict):
        vocab = list(raw.keys())
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, str):
                vocab.append(item)
            elif isinstance(item, dict) and isinstance(item.get("id", item.get("name")), str):
                vocab.append(item.get("id", item.get("name")))
    raw = data.get("disciplines")
    disciplines = {}
    if isinstance(raw, dict):
        items = list(raw.items())
    elif isinstance(raw, list):
        items = [(d.get("id", d.get("name", d.get("discipline"))), d) for d in raw if isinstance(d, dict)]
    else:
        return (vocab or None), None
    for name, entry in items:
        if not isinstance(name, str):
            continue
        if isinstance(entry, dict):
            skill = entry.get("skill", entry.get("owner", entry.get("owningSkill")))
            disciplines[name] = {"skill": skill, "capabilities": entry.get("capabilities")}
        else:
            disciplines[name] = {"skill": None, "capabilities": None}
    return (vocab or None), disciplines


def skill_description(root, name):
    text = read_text(os.path.join(root, "kit", "skills", name, "SKILL.md"))
    if text is None:
        return ""
    front, _ = parse_frontmatter(text)
    return (front or {}).get("description", "")


# ---------------------------------------------------------------- build

def moment_ref(name):
    return "`%s`" % name


def render_moments(kit):
    kit = safe_kit(kit)
    lines = [
        "# GDH moments", "",
        "This file is generated from `kit.json`. Run `python3 scripts/gdh.py build` to change it.", "",
        "A moment grants no authority. The kernel and the user rank higher.",
        "In the Claude Code plugin, each skill name carries the prefix `gdh:`.", "",
        "## Start", "",
        "Start the skill before the work. Say so in one line.", "",
    ]
    for moment in kit["moments"]:
        start = names_list(moment.get("start"))
        if start:
            lines.append("- %s. Start %s." % (str(moment.get("when", "")).rstrip("."), ", ".join(map(moment_ref, start))))
    lines += ["", "## Offer", ""]
    for moment in kit["moments"]:
        offer = names_list(moment.get("offer"))
        if offer:
            note = " %s" % moment["note"] if isinstance(moment.get("note"), str) and moment.get("note") else ""
            lines.append("- %s. Offer %s.%s" % (
                str(moment.get("when", "")).rstrip("."), ", ".join(map(moment_ref, offer)), note))
    lines += [
        "", "## How to offer", "",
        "Ask one question with the host question tool. Put the recommended option first. Put Skip last. "
        "Offer once in a session. On a yes, `ask-gdh` loads a user-invoked GDH skill by reading its `SKILL.md`; "
        "the user may also type the command, such as `/gdh:refine-round`. "
        "With no question tool, write one closing line: `Option: <skill>: <what it does>.`",
    ]
    if kit["wired"]:
        lines += ["", "## Wired skills", "",
                  "These skills are not in this kit. Name one only with its install line.", ""]
        for wid, entry in kit["wired"].items():
            install = entry.get("install")
            install = install if isinstance(install, list) else [install]
            lines.append("- `%s`: %s. Install: %s. Source: %s" % (
                wid, str(entry.get("what", "")).rstrip("."),
                ", then ".join("`%s`" % i for i in install), entry.get("source", "")))
    return "\n".join(lines) + "\n"


def first_sentence(text, limit=180):
    text = " ".join(text.split())
    match = re.search(r"\.(?:\s|$)", text)
    if match:
        text = text[:match.start() + 1]
    if len(text) > limit:
        text = text[:limit - 3].rstrip() + "..."
    return text.replace("|", "\\|")


def render_catalog(root, kit):
    kit = safe_kit(kit)
    lines = ["| Skill | Invocation | Discipline | What it does |", "| --- | --- | --- | --- |"]
    for name, entry in kit["skills"].items():
        lines.append("| `%s` | %s | %s | %s |" % (
            name, entry.get("invocation", ""), entry.get("discipline", ""),
            first_sentence(skill_description(root, name))))
    return "\n".join(lines)


def apply_markers(text, start, end, body):
    """Replace the lines between two marker lines. Return (new text, state).

    State is 'ok', 'absent' (no marker) or 'unbalanced'.
    """
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if line.strip() == start]
    ends = [i for i, line in enumerate(lines) if line.strip() == end]
    if not starts and not ends:
        return text, "absent"
    if len(starts) != 1 or len(ends) != 1 or starts[0] > ends[0]:
        return text, "unbalanced"
    new = lines[:starts[0] + 1] + body.split("\n") + lines[ends[0]:]
    return "\n".join(new), "ok"


def marker_body(text, start, end):
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if line.strip() == start]
    ends = [i for i, line in enumerate(lines) if line.strip() == end]
    if len(starts) != 1 or len(ends) != 1 or starts[0] > ends[0]:
        return None
    return "\n".join(lines[starts[0] + 1:ends[0]])


def build_outputs(root, kit):
    """Return ({relative path: text}, [problem strings]) for every generated file."""
    kit_safe = safe_kit(kit)
    common = {
        "name": kit.get("name", "gdh"),
        "displayName": kit.get("displayName", ""),
        "version": kit.get("version", ""),
        "description": kit.get("description", ""),
        "author": kit.get("author", {}),
        "homepage": kit.get("repository", ""),
        "repository": kit.get("repository", ""),
        "license": kit.get("license", ""),
        "keywords": ["design", "design-system", "brand", "dataviz", "motion", "skills"],
    }
    owner = kit.get("author") if isinstance(kit.get("author"), dict) else {"name": str(kit.get("author", ""))}
    codex = dict(common)
    # The Codex manifest names one skills folder and the hooks file, not a list of skill folders.
    codex["skills"] = "./skills/"
    codex["hooks"] = "./hooks/hooks.json"
    codex["interface"] = {
        "displayName": kit.get("displayName", ""),
        "shortDescription": first_sentence(str(kit.get("description", "")), 120),
        "developerName": owner.get("name", ""),
        "category": "Creativity",
        "capabilities": ["Read", "Write"],
    }
    marketplace = "synthminds-%s" % kit.get("name", "gdh")
    outputs = {
        "kit/.claude-plugin/plugin.json": dump_json(common),
        "kit/.codex-plugin/plugin.json": dump_json(codex),
        ".claude-plugin/marketplace.json": dump_json({
            "name": marketplace,
            "owner": owner,
            "description": kit.get("description", ""),
            "plugins": [{"name": kit.get("name", "gdh"), "source": "./kit",
                         "description": kit.get("description", ""), "version": kit.get("version", "")}],
        }),
        ".agents/plugins/marketplace.json": dump_json({
            "name": marketplace,
            "interface": {"displayName": kit.get("displayName", "")},
            "plugins": [{"name": kit.get("name", "gdh"), "source": {"source": "local", "path": "./kit"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "category": "Creativity"}],
        }),
        "kit/canon/MOMENTS.md": render_moments(kit),
    }
    problems = []
    catalog = render_catalog(root, kit)
    for rel in ("README.md", "kit/README.md"):
        text = read_text(os.path.join(root, rel))
        if text is None:
            continue
        new, state = apply_markers(text, CATALOG_START, CATALOG_END, catalog)
        if state == "ok":
            outputs[rel] = new
        elif state == "unbalanced":
            problems.append("%s: catalog markers are unbalanced" % rel)
    return outputs, problems


def drift(root, kit):
    """Return [(relative path, reason)] for generated files that differ from the build output."""
    outputs, problems = build_outputs(root, kit)
    out = [(p.split(":", 1)[0], p.split(": ", 1)[1]) for p in problems]
    for rel, text in sorted(outputs.items()):
        current = read_text(os.path.join(root, rel))
        if current is None:
            out.append((rel, "generated file is absent; run 'gdh.py build'"))
        elif current != text:
            out.append((rel, "differs from the build output; run 'gdh.py build'"))
    return out


def cmd_build(args):
    root = os.path.abspath(args.root)
    kit = load_kit(root)
    if kit is None:
        print("GDH_KIT_JSON kit/kit.json is missing or does not parse")
        return 1
    if args.check:
        drifted = drift(root, kit)
        if args.json:
            print(json.dumps({"ok": not drifted, "drift": [{"path": p, "message": m} for p, m in drifted]}, indent=2))
        else:
            for path, message in drifted:
                print("GDH_GENERATED_DRIFT  %s  %s" % (path, message))
            print("build check: %s" % ("no drift" if not drifted else "%d file(s) drift" % len(drifted)))
        return 1 if drifted else 0
    outputs, problems = build_outputs(root, kit)
    written = []
    for rel, text in sorted(outputs.items()):
        path = os.path.join(root, rel)
        if os.path.islink(path):
            problems.append("%s: is a symbolic link; not written" % rel)
            continue
        if read_text(path) != text:
            write_text(path, text)
            written.append(rel)
    if args.json:
        print(json.dumps({"ok": not problems, "written": written, "problems": problems}, indent=2))
    else:
        for rel in written:
            print("wrote  %s" % rel)
        for problem in problems:
            print("problem  %s" % problem)
        print("build: %d file(s) written, %d unchanged" % (len(written), len(outputs) - len(written)))
    return 1 if problems else 0


# ---------------------------------------------------------------- check

def check_skills(root, kit, report):
    skills = kit["skills"]
    skills_dir = os.path.join(root, "kit", "skills")
    folders = sorted(d for d in os.listdir(skills_dir)
                     if os.path.isdir(os.path.join(skills_dir, d)) and d not in SKIP_DIRS) \
        if os.path.isdir(skills_dir) else []
    for name in skills:
        if not os.path.isfile(os.path.join(skills_dir, name, "SKILL.md")):
            report.add("GDH_REGISTRY_MISSING_FOLDER", "kit/skills/%s" % name, "registered skill has no SKILL.md")
    budget_used = 0
    for folder in folders:
        rel_dir = "kit/skills/%s" % folder
        rel_skill = rel_dir + "/SKILL.md"
        if folder not in skills:
            report.add("GDH_REGISTRY_UNREGISTERED", rel_dir, "folder is not registered in kit.json")
        text = read_text(os.path.join(root, rel_skill))
        if text is None:
            continue
        line_count, word_count = len(text.splitlines()), len(text.split())
        if line_count > 150 or word_count > 1500:
            report.add("GDH_SKILL_SIZE", rel_skill, "%d lines and %d words; the limit is 150 lines and 1,500 words"
                       % (line_count, word_count))
        front, _ = parse_frontmatter(text)
        if front is None:
            report.add("GDH_FRONTMATTER", rel_skill, "no frontmatter block between '---' lines")
        else:
            name = front.get("name", "")
            if not NAME_RE.match(name) or len(name) > 64:
                report.add("GDH_SKILL_NAME", rel_skill, "name '%s' must be kebab-case, 64 characters at most" % name)
            if name != folder:
                report.add("GDH_SKILL_NAME_FOLDER", rel_skill, "name '%s' differs from folder '%s'" % (name, folder))
            description = front.get("description", "")
            if not 1 <= len(description) <= 1024:
                report.add("GDH_SKILL_DESCRIPTION", rel_skill,
                           "description has %d characters; it needs 1 to 1024" % len(description))
            disabled = front.get("disable-model-invocation", "").lower() == "true"
            invocation = skills.get(folder, {}).get("invocation")
            if invocation == "user" and not disabled:
                report.add("GDH_INVOCATION_FLAG", rel_skill, "user-invoked skill needs 'disable-model-invocation: true'")
            if invocation == "model" and disabled:
                report.add("GDH_INVOCATION_FLAG", rel_skill, "model-invoked skill must not disable model invocation")
            if invocation == "model":
                budget_used += len(description)
        linked = set()
        for target in md_links(text):
            resolved = resolve_link(root, rel_skill, target)
            if resolved:
                linked.add(resolved)
        for rel in iter_files(root, rel_dir):
            base = os.path.basename(rel)
            if base in ("SKILL.md", "refinement-log.md"):
                continue
            if rel not in linked:
                report.add("GDH_SKILL_FILE_UNLINKED", rel, "file is not linked from %s" % rel_skill)
    budget = kit["budgets"].get("modelDescriptionChars")
    if isinstance(budget, int) and budget_used > budget:
        report.add("GDH_DESCRIPTION_BUDGET", "kit/kit.json",
                   "model-invoked descriptions use %d characters; the budget is %d" % (budget_used, budget))
    if "ask-gdh" in skills:
        router = "\n".join(read_text(os.path.join(root, rel)) or ""
                           for rel in iter_files(root, "kit/skills/ask-gdh") if rel.endswith(".md"))
        for name in skills:
            if name != "ask-gdh" and not re.search(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(name), router):
                report.add("GDH_ROUTER_INCOMPLETE", "kit/skills/ask-gdh/SKILL.md", "does not name the skill '%s'" % name)
    check_user_skill_routes(root, kit, report)


def check_user_skill_routes(root, kit, report):
    """The host cannot start a user-invoked skill for the model. The kernel states the route once
    (read the skill's SKILL.md, or print the command). A line that starts such a skill by name must carry it."""
    user = sorted((n for n, v in kit["skills"].items() if v.get("invocation") == "user"), key=len, reverse=True)
    if not user:
        return
    command = "/%s:" % (kit.get("name") or "gdh")
    kernel = read_text(os.path.join(root, "kit", "canon", "KERNEL.md"))
    if kernel is not None and not ("SKILL.md" in kernel and command in kernel):
        report.add("GDH_ROUTE_USER_SKILL", "kit/canon/KERNEL.md",
                   "the kernel lacks the skill handoff line: read the skill's SKILL.md, or print `%s<name>`" % command)
    starts = re.compile(r"(?i)\b(?:start|invoke|launch|trigger)s?\s+(?:the\s+)?`(%s)`(?![a-z0-9-])"
                        % "|".join(re.escape(n) for n in user))
    for rel in iter_files(root, "kit"):
        if not rel.endswith(".md") or rel.startswith("kit/templates/") or rel.endswith("refinement-log.md"):
            continue
        for number, line in enumerate((read_text(os.path.join(root, rel)) or "").split("\n"), 1):
            match = starts.search(line)
            if match and "SKILL.md" not in line and command not in line:
                report.add("GDH_ROUTE_USER_SKILL", rel,
                           "line %d starts the user-invoked skill '%s'; say to read its SKILL.md, or print `%s%s`"
                           % (number, match.group(1), command, match.group(1)))


# "12 pt" is the print body size (16 px on a 96 px-per-inch artboard). The smallest print text is 12 px.
# A clause that sets 12 pt as a floor for all text, with no word "body" in it, contradicts the
# minimum-size table in the typography skill.
PRINT_FLOOR_RE = re.compile(
    r"(?:\b(?:under|below|smaller\s+than|less\s+than|at\s+least|minimum(?:\s+of)?|min\.?|floor(?:\s+of)?|"
    r"no\s+less\s+than)\s+12\s?pt\b|\b12\s?pt\s+(?:or\s+more|or\s+larger|or\s+above|and\s+up|minimum|floor)\b)",
    re.I)


def print_floor_clauses(text):
    """Return the clauses that use 12 pt as a floor without naming body text."""
    hits = []
    for line in text.splitlines():
        for clause in re.split(r"(?<=[.;:!?|])\s+|\s+\|\s+", line):
            if PRINT_FLOOR_RE.search(clause) and not re.search(r"\bbody\b", clause, re.I):
                hits.append(clause.strip())
    return hits


def check_markdown(root, report):
    for rel in iter_files(root, "kit"):
        if not rel.endswith(".md"):
            continue
        text = read_text(os.path.join(root, rel))
        if text is None:
            continue
        in_references = "/references/" in rel
        if in_references and len(text.splitlines()) > 400:
            report.add("GDH_REFERENCE_SIZE", rel, "%d lines; the limit is 400" % len(text.splitlines()))
        if HTML_COMMENT_RE.search(text):
            report.add("GDH_HTML_COMMENT", rel, "holds an HTML comment")
        if BASE64_RE.search(text):
            report.add("GDH_BASE64", rel, "holds a base64 run of 80 or more characters")
        if has_emoji(text):
            report.add("GDH_EMOJI", rel, "holds an emoji")
        if EM_DASH in text:
            report.add("GDH_EM_DASH", rel, "holds an em dash")
        if not rel.endswith("refinement-log.md"):
            for clause in print_floor_clauses(text)[:3]:
                report.add("GDH_PRINT_FLOOR", rel, "'%s' sets 12 pt as a floor; write 'body text 12 pt (16 px)' and "
                                                   "take the smallest size from the typography table" % clause[:120])
    for sub in ("kit", "docs"):
        for rel in iter_files(root, sub):
            if not rel.endswith(".md") or rel.startswith("kit/templates/"):
                continue
            text = read_text(os.path.join(root, rel))
            for target in md_links(text or ""):
                resolved = resolve_link(root, rel, target)
                if resolved is None or not os.path.exists(os.path.join(root, resolved)):
                    report.add("GDH_LINK_BROKEN", rel, "link '%s' does not resolve" % target)


def check_repository(root, report):
    try:
        kit = json.loads(read_text(os.path.join(root, "kit", "kit.json")) or "{}")
    except ValueError:
        kit = {}
    sibling = sibling_repo_pattern(kit.get("repository") if isinstance(kit, dict) else None)
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(dirs + files):
            full = os.path.join(current, name)
            if os.path.islink(full):
                report.add("GDH_SYMLINK", posix(os.path.relpath(full, root)), "is a symbolic link")
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(current, d))]
    rules = ignore_rules(root)
    for rel in iter_files(root):
        ext = os.path.splitext(rel)[1].lower()
        if ext in BINARY_EXT:
            continue
        parts = rel.split("/")
        in_fixture = parts[0] in ("tests", "evals") and "fixtures" in parts
        # A git-ignored private brand pack never reaches the public history. It may hold private links.
        private_pack = parts[0] == "brands" and len(parts) > 2 and is_ignored(rules, "/".join(parts[:2]), True)
        text = read_text(os.path.join(root, rel))
        if text is None:
            continue
        lines = text.split("\n")
        if not in_fixture:
            for number, line in enumerate(lines, 1):
                for label, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        report.add("GDH_SECRET", rel, "line %d looks like a secret (%s)" % (number, label),
                                   line_digest(line))
                for match in EMAIL_RE.finditer(line):
                    address = match.group(0).lower()
                    if address in EMAIL_ALLOWED or address.endswith(EMAIL_ALLOWED_DOMAINS) \
                            or match.group(1).lower() in EMAIL_FILE_TLDS:
                        continue
                    report.add("GDH_SECRET", rel, "line %d holds an email address" % number, line_digest(line))
                if private_pack:
                    continue
                for label, pattern in PRIVATE_LINK_PATTERNS:
                    if pattern.search(line):
                        report.add("GDH_PRIVATE_LINK", rel, "line %d holds a %s; use a placeholder such as "
                                   "<artifact link>" % (number, label), line_digest(line))
                if sibling and sibling(line):
                    report.add("GDH_PRIVATE_LINK", rel, "line %d links another repository of the kit's owner, "
                               "which may be private; name the tool without a link, or waive a public one"
                               % number, line_digest(line))
        if ext in SCRIPT_EXT and parts[0] != "tests":
            for pattern in NETWORK_PATTERNS:
                match = pattern.search(text)
                if match:
                    number = text.count("\n", 0, match.start()) + 1
                    report.add("GDH_SCRIPT_NETWORK", rel, "line %d uses a network module or a download program"
                               % number, line_digest(lines[number - 1]))
                    break
    check_brand_ignored(root, rules, report)


def check_brand_ignored(root, rules, report):
    """Every brand pack except the template and the public example must be git-ignored."""
    brands = os.path.join(root, "brands")
    if not os.path.isdir(brands):
        return
    for slug in sorted(os.listdir(brands)):
        folder = os.path.join(brands, slug)
        if slug in PUBLIC_BRANDS or slug in SKIP_DIRS or slug.startswith(".") \
                or not os.path.isdir(folder) or os.path.islink(folder):
            continue
        if not is_ignored(rules, "brands/%s" % slug, True):
            report.add("GDH_BRAND_PUBLIC", "brands/%s" % slug,
                       "brand pack is not git-ignored; restore the 'brands/*' allowlist in .gitignore")
    # A tracked ignore file that names a private pack publishes that name. Use .git/info/exclude instead.
    for base in ("", "brands"):
        rel = (base + "/.gitignore").lstrip("/")
        text = read_text(os.path.join(root, rel)) or ""
        for number, line in enumerate(text.split("\n"), 1):
            entry = line.strip()
            if not entry or entry.startswith("#") or entry.startswith("!"):
                continue
            entry = entry.lstrip("/").rstrip("/")
            name = entry[len("brands/"):] if base == "" and entry.startswith("brands/") else (entry if base else "")
            if name and "/" not in name and not any(c in name for c in GLOB_CHARS) and name not in PUBLIC_BRANDS:
                report.add("GDH_BRAND_PUBLIC", rel, "line %d names the brand folder '%s'; keep the 'brands/*' "
                           "allowlist and put any extra local rule in .git/info/exclude" % (number, name))


def check_canon(root, kit, report):
    kernel = read_text(os.path.join(root, "kit", "canon", "KERNEL.md"))
    limit = kit["budgets"].get("kernelLines")
    if kernel is None:
        report.add("GDH_KERNEL_MISSING", "kit/canon/KERNEL.md", "file is absent")
    elif isinstance(limit, int) and len(kernel.splitlines()) > limit:
        report.add("GDH_KERNEL_BUDGET", "kit/canon/KERNEL.md",
                   "%d lines; the budget is %d" % (len(kernel.splitlines()), limit))
    rendered = render_moments(kit)
    limit = kit["budgets"].get("momentsChars")
    if isinstance(limit, int) and len(rendered) > limit:
        report.add("GDH_MOMENTS_BUDGET", "kit/canon/MOMENTS.md",
                   "%d characters when rendered; the budget is %d" % (len(rendered), limit))
    # The hook prints KERNEL.md, a blank line and MOMENTS.md, then cuts at HOOK_LIMIT.
    # Long kernel lines can push the moments past the cut even when both line budgets pass.
    hook_total = len((kernel or "").strip()) + 2 + len(rendered.strip())
    if hook_total > HOOK_LIMIT:
        report.add("GDH_HOOK_BUDGET", "kit/canon/KERNEL.md",
                   "KERNEL.md and MOMENTS.md print %d characters; the SessionStart hook prints %d"
                   % (hook_total, HOOK_LIMIT))
    seen = set()
    for index, moment in enumerate(kit["moments"]):
        where = "moment %d" % (index + 1)
        when = moment.get("when")
        start, offer = names_list(moment.get("start")), names_list(moment.get("offer"))
        if not isinstance(when, str) or not when.strip() or when in seen or not (start or offer):
            report.add("GDH_MOMENT_SHAPE", "kit/kit.json",
                       "%s needs a unique 'when' and a 'start' or an 'offer'" % where)
        if isinstance(when, str):
            seen.add(when)
        if len(offer) > MAX_OFFER:
            report.add("GDH_MOMENT_OFFER_LIMIT", "kit/kit.json", "%s offers %d skills; the limit is %d"
                       % (where, len(offer), MAX_OFFER))
        for name in start + offer:
            if name not in kit["skills"] and name not in kit["wired"]:
                report.add("GDH_MOMENT_SKILL_UNKNOWN", "kit/kit.json",
                           "%s names '%s', which is neither registered nor wired" % (where, name))
        for name in start:
            if name in kit["wired"] or kit["skills"].get(name, {}).get("invocation") == "user":
                report.add("GDH_MOMENT_START_USER", "kit/kit.json",
                           "%s starts '%s', which is not model-invoked; offer it" % (where, name))
    listed = set(kit["agents"])
    agents_dir = os.path.join(root, "kit", "agents")
    present = set(f[:-3] for f in os.listdir(agents_dir) if f.endswith(".md")) if os.path.isdir(agents_dir) else set()
    for name in sorted(listed - present):
        report.add("GDH_AGENT_REGISTRY", "kit/agents/%s.md" % name, "listed agent has no file")
    for name in sorted(present - listed):
        report.add("GDH_AGENT_REGISTRY", "kit/agents/%s.md" % name, "agent file is not listed in kit.json")


def tool_files(root):
    folder = os.path.join(root, "kit", "catalogs", "tools")
    return sorted(f for f in os.listdir(folder) if f.endswith(".json")) if os.path.isdir(folder) else []


def check_catalogs(root, kit, report, load):
    rel_caps = "kit/catalogs/capabilities.json"
    vocab, disciplines = load_capabilities(load(rel_caps))
    if vocab is None or disciplines is None:
        # A file that does not parse already has GDH_JSON_INVALID.
        if load.cache[rel_caps] is not None or not os.path.isfile(os.path.join(root, rel_caps)):
            report.add("GDH_CAPABILITIES_SCHEMA", rel_caps,
                       "file needs a 'capabilities' vocabulary and a 'disciplines' table")
    for name, entry in (disciplines or {}).items():
        skill, caps = entry.get("skill"), entry.get("capabilities")
        if not isinstance(skill, str) or not isinstance(caps, list) or any(c not in (vocab or []) for c in caps):
            report.add("GDH_CAPABILITIES_SCHEMA", rel_caps,
                       "discipline '%s' needs a 'skill' and 'capabilities' from the vocabulary" % name)
        if isinstance(skill, str) and skill not in kit["skills"]:
            report.add("GDH_CAPABILITIES_DISCIPLINE", rel_caps,
                       "discipline '%s' names the unregistered skill '%s'" % (name, skill))
    files = tool_files(root)
    ids = set(f[:-5] for f in files)
    for name in files:
        rel = "kit/catalogs/tools/%s" % name
        tool = load(rel)
        if tool is None:
            continue
        if not isinstance(tool, dict):
            report.add("GDH_TOOL_FIELD", rel, "entry must be an object")
            continue
        for key in TOOL_STRINGS:
            if not isinstance(tool.get(key), str) or (not tool.get(key) and key != "evidenceNote"):
                report.add("GDH_TOOL_FIELD", rel, "'%s' must be a non-empty string" % key)
        for key in TOOL_BOOLS:
            if not isinstance(tool.get(key), bool):
                report.add("GDH_TOOL_FIELD", rel, "'%s' must be true or false" % key)
        for key in TOOL_LISTS:
            if not isinstance(tool.get(key), list) or any(not isinstance(v, str) for v in tool.get(key)):
                report.add("GDH_TOOL_FIELD", rel, "'%s' must be a list of strings" % key)
        if isinstance(tool.get("kind"), str) and tool["kind"] not in TOOL_KINDS:
            report.add("GDH_TOOL_ENUM", rel, "kind '%s' is not one of %s" % (tool["kind"], ", ".join(TOOL_KINDS)))
        if isinstance(tool.get("evidence"), str) and tool["evidence"] not in EVIDENCE:
            report.add("GDH_TOOL_ENUM", rel, "evidence '%s' is not one of %s" % (tool["evidence"], ", ".join(EVIDENCE)))
        auth = tool.get("auth")
        if isinstance(auth, str) and auth not in ("oauth", "none") and not re.match(r"^env:[A-Za-z_][A-Za-z0-9_]*$", auth):
            report.add("GDH_TOOL_ENUM", rel, "auth '%s' must be oauth, none or env:<NAME>" % auth)
        tool_id = tool.get("id")
        if isinstance(tool_id, str) and (tool_id != name[:-5] or not NAME_RE.match(tool_id)):
            report.add("GDH_TOOL_ID", rel, "id '%s' must be kebab-case and equal the file name" % tool_id)
        for cap in names_list(tool.get("capabilities")):
            if vocab is not None and cap not in vocab:
                report.add("GDH_TOOL_CAPABILITY", rel, "capability '%s' is not in the vocabulary" % cap)
        if disciplines:
            for item in names_list(tool.get("disciplines")):
                if item not in disciplines:
                    report.add("GDH_TOOL_DISCIPLINE", rel, "discipline '%s' is not in capabilities.json" % item)
        fallback = tool.get("fallback")
        if isinstance(fallback, str) and fallback != "none" and (fallback not in ids or fallback == name[:-5]):
            report.add("GDH_TOOL_FALLBACK", rel, "fallback '%s' is neither another tool id nor 'none'" % fallback)
        card = tool.get("card")
        if isinstance(card, str) and card:
            if card != "references/tools/%s.md" % name[:-5]:
                report.add("GDH_TOOL_CARD", rel, "card must be 'references/tools/%s.md'" % name[:-5])
            elif not os.path.isfile(os.path.join(root, "kit", card)):
                report.add("GDH_TOOL_CARD", rel, "card file kit/%s is absent" % card)
        if isinstance(tool.get("verifiedAt"), str) and not is_iso_date(tool["verifiedAt"]):
            report.add("GDH_TOOL_DATE", rel, "verifiedAt '%s' is not an ISO date" % tool["verifiedAt"])
        if isinstance(tool.get("source"), str) and tool["source"] and tool["source"] != "none" \
                and not tool["source"].startswith("https://"):
            report.add("GDH_TOOL_SOURCE", rel, "source must be an https URL, or 'none' for a tool with no "
                                               "public source")
    rel = "kit/catalogs/assets.json"
    assets = load(rel)
    if assets is not None:
        sources = assets.get("sources") if isinstance(assets, dict) else None
        if not isinstance(sources, list):
            report.add("GDH_ASSETS_FIELD", rel, "file needs a 'sources' list")
            sources = []
        seen = set()
        for index, source in enumerate(sources):
            label = source.get("id", "#%d" % index) if isinstance(source, dict) else "#%d" % index
            if not isinstance(source, dict):
                report.add("GDH_ASSETS_FIELD", rel, "source %s must be an object" % label)
                continue
            missing = [k for k in ASSET_FIELDS if k not in source]
            if missing or not isinstance(source.get("id"), str) or not source.get("id"):
                report.add("GDH_ASSETS_FIELD", rel, "source %s lacks: %s" % (label, ", ".join(missing) or "a string id"))
            if source.get("id") in seen:
                report.add("GDH_ASSETS_DUPLICATE_ID", rel, "id '%s' appears more than once" % label)
            seen.add(source.get("id"))
            if source.get("verifiedOn") is not None and not is_iso_date(source.get("verifiedOn")):
                report.add("GDH_ASSETS_DATE", rel, "source %s: verifiedOn must be null or an ISO date" % label)
            if "url" in source and not (isinstance(source["url"], str) and source["url"].startswith("https://")):
                report.add("GDH_ASSETS_URL", rel, "source %s: url must be an https URL" % label)
    elif not os.path.isfile(os.path.join(root, rel)):
        report.add("GDH_ASSETS_FIELD", rel, "file is absent")


def eval_case_files(root):
    folder = os.path.join(root, "evals", "cases", "triggering")
    return sorted(f for f in os.listdir(folder) if f.endswith(".json")) if os.path.isdir(folder) else []


def brand_scaffold(root, tokens_path):
    """Run the design-system scaffold check on one pack. Return a list of messages."""
    script = os.path.join(root, "kit", "skills", "design-system", "scripts", "ds.py")
    if not os.path.isfile(script):
        return []
    try:
        spec = importlib.util.spec_from_file_location("gdh_ds_scaffold", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with open(tokens_path, "r", encoding="utf-8") as handle:
            doc = json.load(handle)
    except (OSError, ValueError, SyntaxError, ImportError):
        return []
    return [item["message"] for item in module.scaffold_findings(doc)]


def check_local_clis(root, report, load):
    """Validate kit/catalogs/local-clis.json with the ask-gdh probe script's own rules."""
    rel = "kit/catalogs/local-clis.json"
    if not os.path.isfile(os.path.join(root, rel)):
        return
    doc = load(rel)
    if doc is None:
        return
    script = os.path.join(root, "kit", "skills", "ask-gdh", "scripts", "local_clis.py")
    try:
        spec = importlib.util.spec_from_file_location("gdh_local_clis", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except (OSError, SyntaxError, ImportError, AttributeError):
        report.add("GDH_LOCAL_CLI", rel, "the validator kit/skills/ask-gdh/scripts/local_clis.py cannot be loaded")
        return
    vocab, disciplines = load_capabilities(load("kit/catalogs/capabilities.json"))
    for finding in module.validate(doc, set(vocab) if vocab else None, set(disciplines) if disciplines else None):
        report.add("GDH_LOCAL_CLI", rel, "%s %s: %s" % (finding["code"], finding["where"], finding["message"]))


def check_brands_and_evals(root, kit, report, load):
    model_skills = set(name for name, entry in kit["skills"].items() if entry.get("invocation") == "model")
    brands = os.path.join(root, "brands")
    if os.path.isdir(brands):
        for slug in sorted(os.listdir(brands)):
            folder = os.path.join(brands, slug)
            if slug == "_template" or slug.startswith(".") or not os.path.isdir(folder) or os.path.islink(folder):
                continue
            for needed in ("README.md", "tokens.json"):
                if not os.path.isfile(os.path.join(folder, needed)):
                    report.add("GDH_BRAND_PACK", "brands/%s" % slug, "brand pack lacks %s" % needed)
            tokens_path = os.path.join(folder, "tokens.json")
            if os.path.isfile(tokens_path) and not os.path.islink(tokens_path):
                for problem in brand_scaffold(root, tokens_path):
                    report.add("GDH_BRAND_SCAFFOLD", "brands/%s/tokens.json" % slug, problem)
    for name in eval_case_files(root):
        rel = "evals/cases/triggering/%s" % name
        case = load(rel)
        if case is None:
            continue
        if not isinstance(case, dict):
            report.add("GDH_EVAL_CASE", rel, "case must be an object")
            continue
        for key in ("id", "skill", "prompt"):
            if not isinstance(case.get(key), str) or not case.get(key).strip():
                report.add("GDH_EVAL_CASE", rel, "'%s' must be a non-empty string" % key)
        if case.get("kind") != "triggering":
            report.add("GDH_EVAL_CASE", rel, "'kind' must be 'triggering'")
        if isinstance(case.get("id"), str) and case["id"] != name[:-5]:
            report.add("GDH_EVAL_CASE", rel, "'id' must equal the file name without .json")
        skill = case.get("skill")
        negative = skill == NEGATIVE_SKILL
        if isinstance(skill, str) and skill.strip() and not negative and skill not in model_skills:
            report.add("GDH_EVAL_CASE", rel, "'skill' must be a model-invoked skill or '%s'" % NEGATIVE_SKILL)
        expect = case.get("expect")
        if expect is None:
            report.add("GDH_EVAL_CASE", rel, "'expect' is absent")
            continue
        fired = expect.get("skills_fired") if isinstance(expect, dict) else None
        if not isinstance(fired, list) or not all(isinstance(item, str) for item in fired):
            report.add("GDH_EVAL_CASE", rel, "'expect.skills_fired' must be a list of skill names")
        elif negative and fired:
            report.add("GDH_EVAL_CASE", rel, "a negative case must expect no skill: 'skills_fired' must be empty")
        elif not negative and isinstance(skill, str) and skill not in fired:
            report.add("GDH_EVAL_CASE", rel, "'expect.skills_fired' must hold the case skill")


def load_accepted(root, report, load):
    rel = "kit/scan.accepted.json"
    data = load(rel)
    if data is None:
        return []
    if not isinstance(data, list):
        report.add("GDH_ACCEPTED_INVALID", rel, "must be a list of {code, path, reason} with known codes")
        return []
    kept = []
    for index, entry in enumerate(data, 1):
        problem = waiver_problem(entry)
        if problem:
            report.add("GDH_ACCEPTED_INVALID", rel, "entry %d: %s" % (index, problem))
        else:
            kept.append(entry)
    return kept


def waiver_problem(entry):
    """Return why a waiver entry is refused, or None. A waiver covers one true false positive."""
    if not isinstance(entry, dict) or entry.get("code") not in CODES:
        return "needs a known 'code'"
    if not all(isinstance(entry.get(k), str) and entry.get(k).strip() for k in ("path", "reason")):
        return "needs a non-empty 'path' and 'reason'"
    code, path = entry["code"], entry["path"]
    if code == "GDH_ACCEPTED_INVALID":
        return "GDH_ACCEPTED_INVALID cannot be waived"
    if re.match(r"^[*?/\[\]!]+$", path):
        return "path '%s' matches the whole repository; name the file" % path
    if code in EXACT_WAIVER_CODES and any(char in path for char in GLOB_CHARS):
        return "%s needs one exact path, not the pattern '%s'" % (code, path)
    match = entry.get("match")
    if match is not None and not (isinstance(match, str) and SHA256_RE.match(match)):
        return "'match' must be the 64-character sha256 that check --json prints"
    if code in LINE_WAIVER_CODES and match is None:
        return "%s needs 'match': the sha256 of the line, as check --json prints it" % code
    return None


def run_check(root):
    """Run every rule. Return (findings, accepted findings)."""
    root = os.path.abspath(root)
    report = Report()
    load = JsonCache(root, report)
    for sub in ("kit", "evals", "brands", ".claude-plugin", ".agents"):
        for rel in iter_files(root, sub):
            if rel.endswith(".json"):
                load(rel)
    raw = load("kit/kit.json")
    if not isinstance(raw, dict):
        if not os.path.isfile(os.path.join(root, "kit", "kit.json")) or raw is not None:
            report.add("GDH_KIT_JSON", "kit/kit.json", "file is absent or is not an object")
        raw = {}
    else:
        for problem in kit_problems(raw):
            report.add("GDH_KIT_JSON", "kit/kit.json", problem)
    kit = safe_kit(raw)
    check_skills(root, kit, report)
    check_markdown(root, report)
    check_repository(root, report)
    check_canon(root, kit, report)
    check_catalogs(root, kit, report, load)
    check_local_clis(root, report, load)
    check_brands_and_evals(root, kit, report, load)
    if raw:
        for path, message in drift(root, raw):
            report.add("GDH_GENERATED_DRIFT", path, message)
    accepted_rules = load_accepted(root, report, load)
    findings, accepted = [], []
    for finding in report.findings:
        rule = next((r for r in accepted_rules if r["code"] == finding["code"]
                     and fnmatch.fnmatchcase(finding["path"], r["path"])
                     and r.get("match") in (None, finding.get("match"))), None)
        if rule:
            accepted.append(dict(finding, reason=rule["reason"]))
        else:
            findings.append(finding)
    order = list(CODES)
    findings.sort(key=lambda f: (order.index(f["code"]), f["path"], f["message"]))
    return findings, accepted


def print_table(rows):
    if not rows:
        return
    width_code = max(len(r["code"]) for r in rows)
    width_path = min(60, max(len(r["path"]) for r in rows))
    for row in rows:
        match = "  (match %s)" % row["match"] if row.get("match") else ""
        print("%s  %s  %s%s" % (row["code"].ljust(width_code), row["path"].ljust(width_path), row["message"], match))


def cmd_check(args):
    if args.codes:
        for code, meaning in list(CODES.items()) + list(DOCTOR_CODES.items()):
            print("%s  %s" % (code.ljust(30), meaning))
        return 0
    findings, accepted = run_check(args.root)
    if args.json:
        print(json.dumps({"ok": not findings, "findings": findings, "accepted": accepted}, indent=2))
    else:
        print_table(findings)
        for row in accepted:
            print("accepted  %s  %s  (%s)" % (row["code"], row["path"], row["reason"]))
        print("check: %d finding(s), %d accepted" % (len(findings), len(accepted)))
    return 1 if findings else 0


# ---------------------------------------------------------------- export

def crosses_symlink(repo, rel):
    current = repo
    for part in rel.split("/"):
        current = os.path.join(current, part)
        if os.path.islink(current):
            return True
    return False


def demote_headings(text):
    out, fenced = [], False
    for line in text.rstrip("\n").split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        out.append("##" + line if not fenced and re.match(r"^#{1,4} ", line) else line)
    return "\n".join(out)


ALIGN_DETAIL = ("Without a confirmed `design/brief.md` it runs the full interview. "
                "With one it re-aligns in a few questions. `--full` forces the full interview.")


def entry_skill(kit):
    """The skill that opens a session: the first skill the first moment starts."""
    for moment in safe_kit(kit)["moments"]:
        for name in names_list(moment.get("start") if isinstance(moment, dict) else None):
            return name
    return "ask-gdh"


def entry_rule(kit):
    name = entry_skill(kit)
    rule = "Start every design-led session with `%s`, before any other GDH skill." % name
    return rule + (" " + ALIGN_DETAIL if name == "align" else "")


def render_block(root, kit, skill_dirs):
    kernel = read_text(os.path.join(root, "kit", "canon", "KERNEL.md")) or ""
    moments = read_text(os.path.join(root, "kit", "canon", "MOMENTS.md")) or render_moments(kit)
    lines = [
        BLOCK_START,
        "## GDH kit %s" % kit.get("version", ""),
        "",
        entry_rule(kit),
        "",
        "`gdh.py export` manages this block. Edit only outside the two marker lines.",
        "Skills: %s (%d skills)." % (
            ", ".join("`%s`" % d for d in skill_dirs), len(safe_kit(kit)["skills"])),
        "The kit folders `catalogs`, `references` and `canon` sit beside each skills folder. "
        "A path that starts with `kit/` in a skill means that folder.",
        "",
        demote_headings(kernel),
        "",
        demote_headings(moments),
        BLOCK_END,
    ]
    return "\n".join(lines)


def render_claude_block():
    """The CLAUDE.md block. Claude Code skips AGENTS.md when CLAUDE.md exists, so CLAUDE.md imports it."""
    return "\n".join([
        BLOCK_START,
        "`gdh.py export` manages this block. Claude Code reads the GDH kernel and moments through this import.",
        CLAUDE_IMPORT,
        BLOCK_END,
    ])


def block_digest(body):
    return sha256((BLOCK_START + "\n" + body + "\n" + BLOCK_END).encode("utf-8"))


def imports_agents(text):
    """Return True when a CLAUDE.md already imports AGENTS.md outside a code block."""
    return any(line.strip() in (CLAUDE_IMPORT, "@./AGENTS.md") for line in strip_code(text).split("\n"))


def cmd_export(args):
    root, repo = os.path.abspath(args.root), os.path.abspath(args.repo)
    kit = load_kit(root)
    if kit is None:
        print("GDH_KIT_JSON kit/kit.json is missing or does not parse")
        return 1
    if not os.path.isdir(repo):
        print("export: --repo %s is not a folder" % repo)
        return 1
    hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
    unknown = [h for h in hosts if h not in HOST_SKILL_DIRS]
    if unknown or not hosts:
        print("export: unknown host(s) %s; choose from %s" % (", ".join(unknown) or "(none)", ", ".join(HOST_SKILL_DIRS)))
        return 1
    skill_dirs = sorted(set(HOST_SKILL_DIRS[h] for h in hosts))
    kit_safe = safe_kit(kit)

    plan = {}
    for skills_dir in skill_dirs:
        base = skills_dir.rsplit("/", 1)[0]
        for name in kit_safe["skills"]:
            for rel in iter_files(root, "kit/skills/%s" % name):
                plan["%s/%s" % (skills_dir, rel[len("kit/skills/"):])] = (read_bytes(os.path.join(root, rel)), "skill")
        for sub in ("catalogs", "references", "canon"):
            for rel in iter_files(root, "kit/%s" % sub):
                plan["%s/%s" % (base, rel[len("kit/"):])] = (read_bytes(os.path.join(root, rel)), "support")
    if "claude" in hosts:
        for rel in iter_files(root, "kit/agents"):
            if rel.endswith(".md"):
                plan[".claude/agents/%s" % os.path.basename(rel)] = (read_bytes(os.path.join(root, rel)), "agent")

    manifest_rel = ".agents/gdh/manifest.json"
    old = {}
    if os.path.isfile(os.path.join(repo, manifest_rel)) and not crosses_symlink(repo, manifest_rel):
        try:
            old = json.loads(read_bytes(os.path.join(repo, manifest_rel)).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            old = {}
    old = old if isinstance(old, dict) else {}

    actions, problems = [], 0
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dry = args.dry_run

    def act(kind, rel, note=""):
        actions.append({"action": kind, "path": rel, "note": note})

    def put(rel, data):
        if not dry:
            path = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as handle:
                handle.write(data)

    def backup(rel):
        target = ".agents/gdh/backups/%s/%s" % (stamp, rel)
        if crosses_symlink(repo, target):
            return False
        put(target, read_bytes(os.path.join(repo, rel)))
        act("backup", rel, target)
        return True

    def owned_table(key, allowed, what):
        """Read one table of the old manifest. The manifest may come from a clone, so trust no key."""
        nonlocal problems
        raw = old.get(key) if isinstance(old.get(key), dict) else {}
        kept = {}
        for rel in sorted(raw, key=str):
            if allowed(rel):
                kept[rel] = raw[rel]
            else:
                act("refused", str(rel), "the old manifest names %s; export does not touch it" % what)
                problems += 1
        return kept

    old_files = owned_table("files", lambda rel: safe_rel(rel) and rel.startswith(MANAGED_PREFIXES),
                            "a path outside the managed folders")
    old_blocks = owned_table("blocks", lambda rel: rel in MANAGED_BLOCK_FILES, "a file that holds no GDH block")
    old_templates = owned_table("templates", safe_rel, "a path outside the project")

    new_files = {}
    for rel in sorted(plan):
        data, kind = plan[rel]
        path = os.path.join(repo, rel)
        if crosses_symlink(repo, rel):
            act("refused", rel, "the path crosses a symbolic link")
            problems += 1
            if rel in old_files:
                new_files[rel] = old_files[rel]
            continue
        digest = sha256(data)
        record = {"sha256": digest, "kind": kind}
        if os.path.isdir(path):
            act("conflict", rel, "a folder is in the way")
            problems += 1
        elif not os.path.exists(path):
            put(rel, data)
            act("write", rel)
            new_files[rel] = record
        else:
            current = sha256(read_bytes(path))
            owned = isinstance(old_files.get(rel), dict)
            if current == digest:
                act("unchanged", rel)
                new_files[rel] = record
            elif owned and old_files[rel].get("sha256") == current:
                put(rel, data)
                act("update", rel)
                new_files[rel] = record
            elif (owned and args.replace_edited) or args.force:
                if backup(rel):
                    put(rel, data)
                    act("update", rel, "a human edit was backed up first")
                    new_files[rel] = record
                else:
                    act("refused", rel, "the backup path crosses a symbolic link")
                    problems += 1
            elif owned:
                act("conflict", rel, "a human edited this GDH file; keep the edit, or use --replace-edited "
                                     "to back it up and replace it")
                problems += 1
                new_files[rel] = old_files[rel]
            else:
                act("conflict", rel, "GDH did not write this file; use --force to back it up and replace it")
                problems += 1

    for rel in sorted(set(old_files) - set(plan)):
        path = os.path.join(repo, rel)
        if crosses_symlink(repo, rel) or not os.path.isfile(path) or not inside(repo, path):
            continue
        if isinstance(old_files[rel], dict) and sha256(read_bytes(path)) == old_files[rel].get("sha256"):
            if not dry:
                os.remove(path)
                parent = os.path.dirname(path)
                while inside(repo, parent) and os.path.isdir(parent) and not os.listdir(parent):
                    os.rmdir(parent)
                    parent = os.path.dirname(parent)
            act("remove", rel, "no longer exported")
        else:
            act("left", rel, "no longer exported, but a human changed it")

    new_templates = dict(old_templates)
    for rel in iter_files(root, "kit/templates/project"):
        target = rel[len("kit/templates/project/"):]
        if target in TEMPLATE_SKIP:
            continue
        if crosses_symlink(repo, target):
            act("refused", target, "the path crosses a symbolic link")
            problems += 1
        elif os.path.lexists(os.path.join(repo, target)):
            act("kept", target, "the file exists; a template never overwrites")
        else:
            data = read_bytes(os.path.join(root, rel))
            put(target, data)
            act("write", target, "template")
            new_templates[target] = {"sha256": sha256(data)}

    new_blocks = dict(old_blocks)

    def known(rel):
        return old_blocks[rel].get("sha256") if isinstance(old_blocks.get(rel), dict) else None

    def manage_block(rel, block, skip=None):
        """Write or update the marker block of one file. skip = (test, note) leaves a file without a block."""
        nonlocal problems
        path = os.path.join(repo, rel)
        if crosses_symlink(repo, rel):
            act("refused", rel, "the path is a symbolic link")
            problems += 1
            return
        if os.path.isdir(path):
            act("conflict", rel, "a folder is in the way")
            problems += 1
            return
        if not os.path.exists(path):
            put(rel, (block + "\n").encode("utf-8"))
            act("write", rel, "managed block")
            new_blocks[rel] = {"sha256": sha256(block.encode("utf-8"))}
            return
        text = read_text(path)
        if text is None:
            act("conflict", rel, "the file is not UTF-8 text")
            problems += 1
            return
        existing = marker_body(text, BLOCK_START, BLOCK_END)
        replaced, state = apply_markers(text, BLOCK_START, BLOCK_END, "\n".join(block.split("\n")[1:-1]))
        if state == "unbalanced":
            act("conflict", rel, "the gdh-kit marker lines are unbalanced; fix them by hand")
            problems += 1
            return
        if state == "absent":
            if skip and skip[0](text):
                act("kept", rel, skip[1])
                new_blocks.pop(rel, None)
                return
            replaced = text.rstrip("\n") + "\n\n" + block + "\n" if text.strip() else block + "\n"
        if replaced == text:
            act("unchanged", rel, "managed block")
        else:
            if existing is not None and block_digest(existing) != known(rel):
                backup(rel)
            put(rel, replaced.encode("utf-8"))
            act("update", rel, "managed block")
        new_blocks[rel] = {"sha256": sha256(block.encode("utf-8"))}

    def drop_block(rel):
        """Remove a block that export no longer writes. Leave it when a human changed it."""
        new_blocks.pop(rel, None)
        path = os.path.join(repo, rel)
        if crosses_symlink(repo, rel) or not os.path.isfile(path):
            return
        text = read_text(path)
        existing = marker_body(text, BLOCK_START, BLOCK_END) if text is not None else None
        if existing is None:
            return
        if block_digest(existing) != known(rel):
            act("left", rel, "the block is no longer exported, but a human changed it")
            return
        lines = text.split("\n")
        start = [i for i, line in enumerate(lines) if line.strip() == BLOCK_START][0]
        end = [i for i, line in enumerate(lines) if line.strip() == BLOCK_END][0]
        before = "\n".join(lines[:start]).rstrip("\n")
        after = "\n".join(lines[end + 1:]).strip("\n")
        rest = "\n\n".join(part for part in (before, after) if part.strip())
        if not rest.strip():
            if not dry:
                os.remove(path)
            act("remove", rel, "managed block no longer exported")
        else:
            put(rel, (rest + "\n").encode("utf-8"))
            act("update", rel, "managed block removed")

    manage_block("AGENTS.md", render_block(root, kit, skill_dirs))
    if "claude" in hosts:
        manage_block("CLAUDE.md", render_claude_block(),
                     (imports_agents, "the file already imports AGENTS.md, so Claude Code reads the GDH block"))
    elif "CLAUDE.md" in old_blocks:
        drop_block("CLAUDE.md")

    manifest = dump_json({
        "kit": kit.get("name", "gdh"), "version": kit.get("version", ""), "hosts": sorted(hosts),
        "files": {k: new_files[k] for k in sorted(new_files)},
        "blocks": {k: new_blocks[k] for k in sorted(new_blocks)},
        "templates": {k: new_templates[k] for k in sorted(new_templates)},
    })
    if crosses_symlink(repo, manifest_rel):
        act("refused", manifest_rel, "the path crosses a symbolic link")
        problems += 1
    elif read_text(os.path.join(repo, manifest_rel)) != manifest:
        put(manifest_rel, manifest.encode("utf-8"))
        act("write", manifest_rel, "ownership manifest")
    else:
        act("unchanged", manifest_rel, "ownership manifest")

    changed = [a for a in actions if a["action"] not in ("unchanged", "kept")]
    if args.json:
        print(json.dumps({"ok": not problems, "dryRun": dry, "actions": actions}, indent=2))
    else:
        for item in changed:
            print("%s  %s%s" % (item["action"].ljust(9), item["path"], "  (%s)" % item["note"] if item["note"] else ""))
        print("export%s: %d change(s), %d unchanged, %d problem(s)" % (
            " (dry run)" if dry else "", len(changed) - problems, len(actions) - len(changed), problems))
    return 1 if problems else 0


# ---------------------------------------------------------------- doctor

def parse_today(value):
    if value:
        if not is_iso_date(value):
            raise SystemExit("--today must be YYYY-MM-DD")
        return datetime.date.fromisoformat(value)
    return datetime.date.today()


def run_doctor(root, today):
    """Return (warnings, info). A warning is {code, path, message}."""
    root = os.path.abspath(root)
    report = Report()
    scratch = Report()
    load = JsonCache(root, scratch)
    kit = safe_kit(load_kit(root) or {})
    vocab, _ = load_capabilities(load("kit/catalogs/capabilities.json"))
    covered, verified = set(), set()
    for name in tool_files(root):
        rel = "kit/catalogs/tools/%s" % name
        tool = load(rel)
        if not isinstance(tool, dict):
            continue
        covered.update(names_list(tool.get("capabilities")))
        if tool.get("evidence") == "VERIFIED":
            verified.update(names_list(tool.get("capabilities")))
        if is_iso_date(tool.get("verifiedAt")):
            age = (today - datetime.date.fromisoformat(tool["verifiedAt"])).days
            if age > STALE_DAYS:
                report.add("GDH_DOCTOR_STALE", rel, "verified %d days ago; verify the entry again" % age)
        if tool.get("evidence") == "UNTESTED":
            report.add("GDH_DOCTOR_UNTESTED", rel, "evidence is UNTESTED; exercise the tool or read its documentation")
        card = tool.get("card") if isinstance(tool.get("card"), str) and tool.get("card") else "references/tools/%s.md" % name[:-5]
        if not os.path.isfile(os.path.join(root, "kit", card)):
            report.add("GDH_DOCTOR_NO_CARD", rel, "card kit/%s is absent" % card)
    for cap in vocab or []:
        if cap not in covered:
            report.add("GDH_DOCTOR_CAPABILITY_NO_TOOL", "kit/catalogs/capabilities.json", "capability '%s' has no tool" % cap)
        elif cap in GATE_CAPABILITIES and cap not in verified:
            report.add("GDH_DOCTOR_GATE_UNVERIFIED", "kit/catalogs/capabilities.json",
                       "capability '%s' backs a gate but no tool for it is VERIFIED; exercise one" % cap)
    with_case = set()
    for name in eval_case_files(root):
        case = load("evals/cases/triggering/%s" % name)
        if isinstance(case, dict) and isinstance(case.get("skill"), str):
            with_case.add(case["skill"])
    for name, entry in kit["skills"].items():
        if entry.get("invocation") == "model" and name not in with_case:
            report.add("GDH_DOCTOR_NO_EVAL", "kit/skills/%s" % name, "model-invoked skill has no triggering eval case")
        if not os.path.isfile(os.path.join(root, "kit", "skills", name, "refinement-log.md")):
            report.add("GDH_DOCTOR_NO_REFINEMENT_LOG", "kit/skills/%s" % name, "refinement-log.md is absent")
    assets = load("kit/catalogs/assets.json")
    sources = assets.get("sources") if isinstance(assets, dict) and isinstance(assets.get("sources"), list) else []
    unverified = sum(1 for s in sources if isinstance(s, dict) and s.get("verifiedOn") is None)
    info = {"today": today.isoformat(), "tools": len(tool_files(root)), "assetSources": len(sources),
            "assetSourcesUnverified": unverified}
    return report.findings, info


def cmd_doctor(args):
    warnings, info = run_doctor(args.root, parse_today(args.today))
    if args.json:
        print(json.dumps({"ok": not warnings, "warnings": warnings, "info": info}, indent=2))
    else:
        print_table(warnings)
        print("asset sources with verifiedOn null: %d of %d (read the license page before use)"
              % (info["assetSourcesUnverified"], info["assetSources"]))
        print("doctor: %d warning(s) on %s" % (len(warnings), info["today"]))
    return 1 if warnings else 0


# ---------------------------------------------------------------- new-tool, new-skill

def cmd_new_tool(args):
    root = os.path.abspath(args.root)
    tool_id = args.id
    errors = []
    if not NAME_RE.match(tool_id) or len(tool_id) > 64:
        errors.append("id must be kebab-case, 64 characters at most")
    if args.kind not in TOOL_KINDS:
        errors.append("--kind must be one of %s" % ", ".join(TOOL_KINDS))
    if args.source != "none" and not args.source.startswith("https://"):
        errors.append("--source must be an https URL, or 'none' for a tool with no public source")
    try:
        caps_data = json.loads(read_bytes(os.path.join(root, "kit", "catalogs", "capabilities.json")).decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        caps_data = None
    vocab, disciplines = load_capabilities(caps_data)
    capabilities = [c.strip() for c in args.capabilities.split(",") if c.strip()]
    if vocab is None:
        errors.append("kit/catalogs/capabilities.json is absent or has no vocabulary")
    else:
        bad = [c for c in capabilities if c not in vocab]
        if bad or not capabilities:
            errors.append("unknown or empty capabilities: %s. Extend the vocabulary through add-design-tool"
                          % (", ".join(bad) or "(none given)"))
    auth = args.auth
    if auth not in ("oauth", "none") and not re.match(r"^env:[A-Za-z_][A-Za-z0-9_]*$", auth):
        errors.append("--auth must be oauth, none or env:<NAME>")
    entry_rel = "kit/catalogs/tools/%s.json" % tool_id
    card_rel = "kit/references/tools/%s.md" % tool_id
    for rel in (entry_rel, card_rel):
        if os.path.lexists(os.path.join(root, rel)):
            errors.append("%s exists; new-tool does not overwrite" % rel)
    if args.fallback != "none" and not os.path.isfile(os.path.join(root, "kit", "catalogs", "tools", args.fallback + ".json")):
        errors.append("--fallback must be an existing tool id or 'none'")
    if errors:
        for error in errors:
            print("new-tool: %s" % error)
        return 1
    today = parse_today(args.today).isoformat()
    entry = {
        "id": tool_id, "name": args.name,
        "what": args.what or "Describe in one line what this tool makes.",
        "kind": args.kind, "capabilities": capabilities,
        "disciplines": [name for name, d in (disciplines or {}).items()
                        if isinstance(d.get("capabilities"), list) and set(d["capabilities"]) & set(capabilities)],
        "install": args.install or "Write the exact install line or the settings location.",
        "auth": auth, "spendsCredits": bool(args.spends), "exposes": bool(args.exposes),
        "readOnly": bool(args.read_only), "toolPrefix": args.prefix or tool_id, "firstCall": "none",
        "fallback": args.fallback, "card": "references/tools/%s.md" % tool_id, "source": args.source,
        "verifiedAt": today, "evidence": "DOCUMENTED",
        "evidenceNote": "Entry written from the source page. No call was exercised.",
    }
    card = ["# %s" % args.name, "",
            "Catalog entry: [%s.json](../../catalogs/tools/%s.json). Source: %s" % (tool_id, tool_id, args.source), ""]
    for heading in CARD_HEADINGS:
        body = "Write this section."
        if heading == "Evidence":
            body = "DOCUMENTED on %s. No call was exercised. Raise the label to VERIFIED only after one real call." % today
        if heading == "Cost model":
            body = "Write this section. Do not write prices here. Tell the agent to read them live."
        card += ["## %s" % heading, "", body, ""]
    write_text(os.path.join(root, entry_rel), dump_json(entry))
    write_text(os.path.join(root, card_rel), "\n".join(card))
    print("wrote  %s" % entry_rel)
    print("wrote  %s" % card_rel)
    print("next: fill the card, make one free or approved call, then run 'gdh.py check'")
    return 0


SKILL_BODY = """
# {name}

State the purpose in one paragraph. State what this skill does not do and which skill does.

## Before you start

- List the inputs this skill needs.
- Read `DESIGN.md`, `design/brief.md` and `design/decisions.md` when they exist.
- Precedence: the user instruction, then the project design system, then this skill.

## Procedure

1. Write the first step.
2. Mark a user decision point with "ASK:".
3. Mark a spend or exposure point with "GATE:".

## Tools

Capabilities: list them from the vocabulary in `kit/catalogs/capabilities.json`.
Read `kit/catalogs/tools/` and pick a tool with the capability.
Check that the tool is present in this session.
Read the tool card. Use the fallback when the tool is absent.

## Checks

Gates: list the checks that block delivery. Use verified numbers only.
Defaults: list the defaults. Write "Default:" before each one.

## Output

List the files this skill writes in the project. Give the closing report format.

## References

None yet. Link each file of this folder here and say when to read it.

## Sources

- Add the title and chapter, or the URL.
"""


def cmd_new_skill(args):
    root = os.path.abspath(args.root)
    name = args.name
    kit = load_kit(root)
    errors = []
    if kit is None or not isinstance(kit.get("skills"), dict):
        errors.append("kit/kit.json is missing or has no skills table")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append("name must be kebab-case, 64 characters at most")
    description = " ".join(args.description.split())
    if not 1 <= len(description) <= 1024:
        errors.append("--description needs 1 to 1024 characters")
    folder = os.path.join(root, "kit", "skills", name)
    if os.path.lexists(folder) or (kit and name in (kit.get("skills") or {})):
        errors.append("skill '%s' exists; new-skill does not overwrite" % name)
    if kit and name in (kit.get("wired") or {}):
        errors.append("'%s' is a wired id" % name)
    case_rel = "evals/cases/triggering/trigger-%s.json" % name
    if args.invocation == "model" and os.path.lexists(os.path.join(root, case_rel)):
        errors.append("%s exists; new-skill does not overwrite" % case_rel)
    if errors:
        for error in errors:
            print("new-skill: %s" % error)
        return 1
    today = parse_today(args.today).isoformat()
    front = ["---", "name: %s" % name, "description: %s" % json.dumps(description, ensure_ascii=False)]
    if args.invocation == "user":
        front.append("disable-model-invocation: true")
    front.append("---")
    write_text(os.path.join(folder, "SKILL.md"), "\n".join(front) + "\n" + SKILL_BODY.format(name=name))
    write_text(os.path.join(folder, "refinement-log.md"),
               "# Refinement log: %s\n\nFormat: `YYYY-MM-DD | observation | change | files`\n\n"
               "%s | skill scaffolded | new skill | SKILL.md\n" % (name, today))
    kit["skills"][name] = {"invocation": args.invocation, "origin": "gdh", "discipline": args.discipline}
    write_text(os.path.join(root, "kit", "kit.json"), dump_json(kit))
    print("wrote  kit/skills/%s/SKILL.md" % name)
    print("wrote  kit/skills/%s/refinement-log.md" % name)
    print("wrote  kit/kit.json")
    if args.invocation == "model":
        write_text(os.path.join(root, case_rel), dump_json({
            "id": "trigger-%s" % name, "kind": "triggering", "skill": name,
            "prompt": "Write a prompt in the words of a user. Do not reuse the words of the description.",
            "expect": {"skills_fired": [name]},
        }))
        print("wrote  %s" % case_rel)
    outputs, _ = build_outputs(root, kit)
    for rel, text in sorted(outputs.items()):
        if read_text(os.path.join(root, rel)) != text and not os.path.islink(os.path.join(root, rel)):
            write_text(os.path.join(root, rel), text)
            print("wrote  %s" % rel)
    print("next: write the skill body, name the skill in ask-gdh, then run 'gdh.py check'")
    return 0


# ---------------------------------------------------------------- command line

def build_parser():
    parser = argparse.ArgumentParser(prog="gdh.py", description="GDH engine. Standard library only. No network.")
    sub = parser.add_subparsers(dest="command")

    def add(name, func, text):
        command = sub.add_parser(name, help=text, description=text)
        command.add_argument("--root", default=ROOT_DEFAULT, help="the GDH repository root (default: this checkout)")
        command.add_argument("--json", action="store_true", help="machine output")
        command.set_defaults(func=func)
        return command

    check = add("check", cmd_check, "Run every rule. Exit 1 on any finding.")
    check.add_argument("--codes", action="store_true", help="list each finding code with its meaning")
    build = add("build", cmd_build, "Write the generated files from kit.json.")
    build.add_argument("--check", action="store_true", help="write nothing; exit 1 on drift")
    export = add("export", cmd_export, "Copy the kit into a project.")
    export.add_argument("--repo", required=True, help="the project folder to write into")
    export.add_argument("--hosts", default="claude,agents", help="comma list of: claude, codex, cursor, agents")
    export.add_argument("--dry-run", action="store_true", help="print the plan; write nothing")
    export.add_argument("--force", action="store_true",
                        help="back up and replace a file that GDH did not write, and every edited GDH file")
    export.add_argument("--replace-edited", action="store_true",
                        help="back up and replace a GDH file that a human edited (default: report a conflict)")
    doctor = add("doctor", cmd_doctor, "Report stale entries, missing cards and missing eval cases.")
    doctor.add_argument("--today", help="YYYY-MM-DD (default: the system date)")
    tool = add("new-tool", cmd_new_tool, "Write a tool catalog entry and a card stub.")
    tool.add_argument("id")
    tool.add_argument("--name", required=True)
    tool.add_argument("--kind", required=True, help="one of: %s" % ", ".join(TOOL_KINDS))
    tool.add_argument("--capabilities", required=True, help="comma list from the capability vocabulary")
    tool.add_argument("--source", required=True, help="https URL, or 'none' for a tool with no public source")
    tool.add_argument("--spends", action="store_true", help="the tool spends credits")
    tool.add_argument("--exposes", action="store_true", help="the tool can publish, share or upload")
    tool.add_argument("--read-only", action="store_true")
    tool.add_argument("--what")
    tool.add_argument("--install")
    tool.add_argument("--auth", default="none")
    tool.add_argument("--prefix")
    tool.add_argument("--fallback", default="none")
    tool.add_argument("--today", help="YYYY-MM-DD (default: the system date)")
    skill = add("new-skill", cmd_new_skill, "Scaffold a skill and register it in kit.json.")
    skill.add_argument("name")
    skill.add_argument("--invocation", required=True, choices=("model", "user"))
    skill.add_argument("--discipline", required=True)
    skill.add_argument("--description", required=True)
    skill.add_argument("--today", help="YYYY-MM-DD (default: the system date)")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
