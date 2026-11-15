#!/usr/bin/env python3
"""
Compile a resume .tex with tectonic and report / assert its page count.

Usage:
  pagecheck.py FILE.tex              -> report mode: print "pages=N", exit 0 if it compiles
  pagecheck.py FILE.tex MAXPAGES     -> assert mode: exit 0 if pages <= MAXPAGES else 1

PORTABILITY: this check is BEST-EFFORT. If tectonic or pypdf is not installed on the
machine, it prints "pagecheck=skipped" and exits 0 (non-fatal) — because the real,
engine-independent one-page guarantee is the per-line char budget in validate.py, not
this script. Install tectonic (brew/apt/cargo) + `pip install pypdf` to enable it.

FIDELITY: tectonic uses XeTeX; Overleaf defaults to pdflatex. With font packages like
`times` they can differ by a page, so use this RELATIVELY: get the original's page
count, then assert the tailored file is <= that baseline. This script's job is to
prove the file still COMPILES and did not grow in page count.

Exit 0 = skipped, OR compiled and (report mode / pages <= MAXPAGES)
     1 = compiled but pages > MAXPAGES
     2 = compile failed (prints the tail of tectonic's error)
"""
import os
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: pagecheck.py FILE.tex [max_pages]")
        return 2
    tex = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if shutil.which("tectonic") is None:
        print("pagecheck=skipped (tectonic not installed; char-budget still enforced)")
        return 0
    try:
        from pypdf import PdfReader
    except ImportError:
        print("pagecheck=skipped (pypdf not installed; run: pip install pypdf)")
        return 0

    outdir = tempfile.mkdtemp(prefix="resume_pagecheck_")
    proc = subprocess.run(
        ["tectonic", "--outdir", outdir, tex],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write("COMPILE FAILED (tectonic):\n")
        sys.stderr.write(proc.stderr[-3000:] + "\n")
        print("compile=fail")
        return 2

    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(tex))[0] + ".pdf")
    pages = len(PdfReader(pdf).pages)
    print(f"pages={pages}")
    if max_pages is None:
        return 0
    return 0 if pages <= max_pages else 1


if __name__ == "__main__":
    sys.exit(main())
