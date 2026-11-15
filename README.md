# resume-tailor

A [Claude Code](https://claude.com/claude-code) skill that **tailors a one-page LaTeX
resume to a specific job description** — working the JD's keywords into your existing
bullets **without changing the length or formatting**, so it never spills to a second
page and never breaks your template.

You paste two things each run: the **job description** and your **resume LaTeX**. It
returns the updated LaTeX plus a report of what changed and which keywords it couldn't
honestly cover.

## What makes it safe (the guardrails)

- **Never fabricates.** It only rephrases what your resume already supports. JD keywords
  with no basis in your experience go into a **Gaps** list — never silently inserted.
- **Can't grow the page.** Every rewritten line must be **≤ its original character
  length**, enforced by a deterministic script (`validate.py`). If no line grows, the
  layout can't overflow — in any LaTeX engine.
- **Can't break formatting.** Only the text inside bullets/headlines is editable; macros,
  table structure, `&`, `\\`, `\hline`, and the preamble are locked (also checked by
  `validate.py`).
- **Still compiles.** If `tectonic` is installed it compiles the result and checks the
  page count didn't increase; if not, it skips that check and relies on the char budget.

> The model *proposes* edits; the scripts *enforce* the rules. Output that fails a check
> is never handed back.

## Install

### Easiest — let Claude set it up for you

Open this repo in Claude Code (or just paste the repo URL) and say:

> **"Read SETUP.md from github.com/priyanshu9620/claude-resume-tailor and set it up."**

[`SETUP.md`](SETUP.md) is written for a Claude Code agent — it checks prerequisites,
installs the plugin, optionally enables the LaTeX page-check, and verifies the result.

### Option A — one command (recommended, manual)

In a Claude Code session:
```
/plugin marketplace add priyanshu9620/claude-resume-tailor
/plugin install resume-tailor@priyanshu-skills
```
Or from your shell (Claude Code ≥ 2.1.292):
```bash
claude plugin install resume-tailor --marketplace priyanshu9620/claude-resume-tailor --scope user
```
Then restart Claude Code and run `/resume-tailor:resume-tailor`.

### Option B — plain skill copy (no marketplace)

```bash
git clone https://github.com/priyanshu9620/claude-resume-tailor
mkdir -p ~/.claude/skills
cp -R claude-resume-tailor/skills/resume-tailor ~/.claude/skills/
```
Restart Claude Code and run `/resume-tailor`.

## Prerequisites

- **Required:** `python3` (used by the enforcement scripts; stdlib only).
- **Optional:** `tectonic` + `pypdf` enable the compile/page-count cross-check.
  ```bash
  brew install tectonic      # macOS (or apt / cargo on Linux)
  pip install pypdf
  ```
  Without them the skill still works — the compile check self-skips and the character
  budget alone guarantees the length.

## Usage

1. Run `/resume-tailor` (or `/resume-tailor:resume-tailor` if installed as a plugin).
2. Paste the **job description** when asked.
3. Paste your **resume LaTeX** when asked.
4. Review the proposed per-line edits + the Gaps list, approve, and copy the updated
   LaTeX back into Overleaf. Give it a final glance there to confirm one page.

## A note on honesty

Keyword-matching helps you pass ATS/keyword screens, but an interviewer will ask you to
back up what's on the page. This tool deliberately **won't invent** skills or experience —
it aligns your true content to the JD's language and tells you, separately, which JD
keywords you'd need to genuinely acquire.

## License

MIT
