---
name: resume-tailor
description: >-
  Tailor a one-page LaTeX resume/CV to a specific job description WITHOUT changing
  its length or formatting. Use whenever the user wants to adapt, customize, tweak,
  or "update my resume/CV for this job/JD/role", align a resume to a posting, or
  insert role keywords. The user pastes the JD text and their resume LaTeX each run
  (no fixed file). The skill rewrites only existing content, never fabricates, keeps
  every edit within the original character budget, preserves all LaTeX structure,
  and verifies the output still compiles to exactly ONE page.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*)
---

# Resume Tailor

Adapt a resume's wording to a job description so it passes keyword/ATS screens —
**without lengthening it, breaking its formatting, or inventing anything.**

## Inputs (ask for both every run — nothing is fixed)

1. **The job description** — the user pastes the raw JD text they copied from the job site.
2. **The resume LaTeX** — the user pastes their full `.tex` source (any person, any template).

If either is missing, ask for it before doing anything else. Never assume a previous
run's resume or JD.

## HARD RULES — guardrails (never break these)

1. **Truthfulness.** Only rephrase content the resume *already* supports. A JD keyword
   with no basis in the person's real experience goes in the **Gaps** report — it is
   **never** inserted. Synonym/voice swaps that stay true are fine
   (e.g. "analyzed data" → "performed data analysis"). Do not invent skills, tools,
   employers, metrics, or dates.
2. **Length cap.** Every rewritten line must be **≤ its original character count**.
   Shorter is fine; longer is forbidden. This is what keeps lines from wrapping and
   the resume from spilling to a second page.
3. **Formatting lock.** Edit only the *text* inside existing slots — `\item` bullets,
   the headline/title line, and role/title text. Never touch macros, `&`, `\\`,
   `\hline`, `\cellcolor`, tabular preambles, `\begin`/`\end`, section bars, geometry,
   or the preamble. The line count must stay identical (no added/removed lines).
4. **No growth.** The tailored `.tex` must compile and render in **no more pages than
   the original**. (Absolute "1 page" is guaranteed by rule 2, not by the compiler —
   see the fidelity note below.)
5. **Enforcement is automated, not trusted to judgement.** Rules 2–4 are checked by
   the scripts below. If a check fails, fix and re-check — do **not** hand back output
   that failed a check.
6. **Always deliver the full code first, then the exact changes.** Your reply must
   contain the COMPLETE updated `.tex` in one copy-paste code block FIRST, then a
   precise list of every change (per-line old → new). Never return only a description,
   and never withhold the code waiting for approval — the user judges from the
   delivered code and reprompts (e.g. "revert line 123", "also work in on-call").

> **Why rule 2 is the real one-page guarantee:** `tectonic` uses XeTeX, but Overleaf
> defaults to pdflatex, and with font packages (e.g. `times`) they can differ by a
> whole page — so the compiler's *absolute* page count is not faithful to the user's
> Overleaf. The per-line char budget IS engine-independent: if no line grows, the
> layout cannot grow past the original's one page in any engine. The compile check is
> used *relatively* (tailored ≤ original) and to confirm it still builds.

## Workflow

1. Collect the JD and the resume LaTeX (ask if missing). Preflight: confirm `python3`
   exists (`command -v python3`). `tectonic` + `pypdf` are optional — without them the
   compile check self-skips and the char-budget alone still guarantees length.
2. **Parse the JD** into a weighted keyword set: must-haves, nice-to-haves, hard
   skills, soft skills, and recurring ATS/role terms (repeated terms = higher weight).
3. Write the pasted resume to a working file and establish the baseline page count:
   ```
   WORK=$(mktemp -d /tmp/resume-tailor.XXXX)
   # write the pasted LaTeX to $WORK/original.tex
   python3 ${CLAUDE_SKILL_DIR}/scripts/pagecheck.py "$WORK/original.tex"
   ```
   This prints `pages=B` — the baseline. If it does not compile, tell the user the
   input itself is broken and stop. (B may read as 2 even for a resume that is 1 page
   in Overleaf — that's the XeTeX/pdflatex gap; use B only as the relative baseline.)
4. **Map** each JD keyword to resume lines and classify:
   - ✓ already present (leave alone)
   - ~ surfaceable — an existing TRUE line can be rephrased to use the JD's wording
   - ✗ gap — no basis in the resume → Gaps report, never inserted
5. **Propose capped rewrites** for the ~ lines. For each: old → new, char delta,
   keyword(s) worked in. Keep each new line ≤ the old line's length.
6. Write the edited file to `$WORK/tailored.tex` and **enforce**:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py "$WORK/original.tex" "$WORK/tailored.tex"
   python3 ${CLAUDE_SKILL_DIR}/scripts/pagecheck.py "$WORK/tailored.tex" "$B"
   ```
   where `$B` is the baseline page count from step 3 (tailored must be ≤ baseline).
   If either fails, shorten the offending lines and repeat until both pass.
7. **Deliver the full updated `.tex` in your reply** — the complete file in one
   copy-paste code block, so the user has the result in hand immediately. (Offer to
   also save it to a file.)
8. **Then state exactly what changed** so the user can judge and reprompt: a per-line
   old → new list with char deltas, the keyword coverage, the Gaps list, and the check
   results. Do NOT gate the code behind an approval step — the user reviews the
   delivered output and reprompts for any change (revert a line, add a keyword, etc.).

## Output / report format

Order matters: **the full updated LaTeX comes first, the change list second.**

- **Updated LaTeX** (the COMPLETE file in one code block, ready to paste into Overleaf).
- **Exactly what changed:** a per-line old → new list with char deltas (so the user can
  judge each edit and reprompt).
- **Keyword coverage:** X of Y JD keywords now present (list which, and where).
- **Gaps (not inserted):** JD keywords with no basis in the resume, with a one-line
  note on each (ignore / worth genuinely acquiring).
- **Checks:** `validate.py PASS` (structure + char budget) + `pagecheck.py` tailored
  pages ≤ baseline. Remind the user to open it in Overleaf for the final visual confirm.

## Notes

- The validators are the guarantee; the model proposes, the scripts enforce. Never
  skip them, and never present output that failed them.
- `tectonic` downloads LaTeX packages on first compile (needs internet once).
- Keep the user's original untouched — only the working copies in `$WORK` are edited.
