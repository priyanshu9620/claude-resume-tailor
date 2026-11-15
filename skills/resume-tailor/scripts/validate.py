#!/usr/bin/env python3
"""
Enforce the formatting + length guardrails between an original resume .tex and an
edited one. Deterministic — the model proposes edits, this script is the guarantee.

Usage:  validate.py ORIGINAL.tex MODIFIED.tex [char_tolerance]

Checks:
  1. Line count is identical (no lines added or removed -> structure stays put).
  2. For every CHANGED line:
       a. the LaTeX skeleton is unchanged (same commands, &, \\, {, }, $, %, ~)
          -> only the human-readable text was touched, never the formatting.
       b. the new line is no longer than the original (+ optional tolerance)
          -> lines can't grow, so nothing wraps and the page can't overflow.

Exit 0 = PASS, 1 = FAIL.
"""
import re
import sys

tok = re.compile(r'\\\\|\\[a-zA-Z@]+|[{}&$%~]')


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: validate.py ORIGINAL.tex MODIFIED.tex [char_tolerance]")
        return 2
    orig_path, mod_path = sys.argv[1], sys.argv[2]
    tol = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    with open(orig_path, encoding="utf-8") as f:
        orig = f.read().splitlines()
    with open(mod_path, encoding="utf-8") as f:
        mod = f.read().splitlines()

    fails = []
    if len(orig) != len(mod):
        fails.append(
            f"line count changed {len(orig)} -> {len(mod)}: "
            "structure must stay identical (no lines added/removed)"
        )
    else:
        for i, (a, b) in enumerate(zip(orig, mod), start=1):
            if a == b:
                continue
            if tok.findall(a) != tok.findall(b):
                fails.append(
                    f"line {i}: LaTeX structure changed "
                    "(commands / & / \\\\ / braces differ) — edit text only"
                )
            if len(b) > len(a) + tol:
                over = len(b) - len(a) - tol
                fails.append(
                    f"line {i}: {over} chars over budget "
                    f"(orig {len(a)} -> new {len(b)}); shorten it"
                )

    if fails:
        print("VALIDATE: FAIL")
        for f in fails:
            print("  - " + f)
        return 1
    print("VALIDATE: PASS (structure preserved, every edit within char budget)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
