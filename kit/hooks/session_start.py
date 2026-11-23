#!/usr/bin/env python3
"""SessionStart hook: print KERNEL.md, then MOMENTS.md.

The output is 9,000 characters at most. When the text is longer, the output ends with a line
that says so, because a silent cut could drop the moments that start `align`.
`gdh.py check` reports GDH_HOOK_BUDGET before that can happen; scripts/gdh.py holds the same limit.
The hook never fails and never blocks. It reads two files beside this script.
It writes nothing and calls no network.
"""
import os
import sys

LIMIT = 9000
CUT_NOTE = ("\n\n[GDH: this text was cut at %d characters. Read canon/KERNEL.md and canon/MOMENTS.md "
            "in the GDH plugin folder in full.]" % LIMIT)


def gather(canon):
    parts = []
    for name in ("KERNEL.md", "MOMENTS.md"):
        try:
            with open(os.path.join(canon, name), "r", encoding="utf-8") as handle:
                text = handle.read().strip()
        except (OSError, ValueError):
            continue
        if text:
            parts.append(text)
    text = "\n\n".join(parts)
    if len(text) > LIMIT:
        text = text[:LIMIT - len(CUT_NOTE)].rstrip() + CUT_NOTE
    return text


def main():
    try:
        canon = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "canon")
        text = gather(canon)
        if text:
            sys.stdout.write(text + "\n")
    except Exception:  # the hook must never fail a session
        pass
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except BaseException:
        code = 0
    sys.exit(code)
