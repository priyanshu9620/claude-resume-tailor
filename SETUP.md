# SETUP.md — instructions for a Claude Code agent

**You are a Claude Code agent. A user wants the `resume-tailor` skill installed and
working on this machine. Do the steps below, adapting to this OS, and report back.**
This file is about *installation only* — do not tailor any resume here; that happens
later when the user runs the skill.

## Goal

Install the `resume-tailor` plugin (skill) so the user can run `/resume-tailor` in
Claude Code. The skill tailors a one-page LaTeX resume to a job description without
changing its length or formatting.

## Step 1 — Required prerequisite: python3

Check it exists; it's needed by the skill's enforcement scripts (stdlib only):
```bash
command -v python3 || echo "MISSING python3"
```
If missing, tell the user to install it (`brew install python` on macOS;
`sudo apt install python3` on Debian/Ubuntu) and stop until they do.

## Step 2 — Install the plugin (primary method)

Preferred: run these two commands **inside the Claude Code session** (slash commands):
```
/plugin marketplace add priyanshu9620/claude-resume-tailor
/plugin install resume-tailor@priyanshu-skills
```
`/plugin install` opens a details panel — the user picks the scope (choose **user** for
all projects) and confirms.

Non-interactive equivalent (shell, Claude Code ≥ 2.1.292):
```bash
claude plugin marketplace add priyanshu9620/claude-resume-tailor
claude plugin install resume-tailor@priyanshu-skills --scope user
```

If the one-step form is available you may use it instead:
```bash
claude plugin install resume-tailor --marketplace priyanshu9620/claude-resume-tailor --scope user
```

## Step 3 — Fallback if the plugin commands are unavailable (older Claude Code)

Copy the skill in as a plain user-level skill:
```bash
git clone https://github.com/priyanshu9620/claude-resume-tailor /tmp/claude-resume-tailor
mkdir -p ~/.claude/skills
cp -R /tmp/claude-resume-tailor/skills/resume-tailor ~/.claude/skills/
```

## Step 4 — Optional: enable the compile/page-count cross-check

The skill works without this (a character-budget rule guarantees the length). To enable
the extra "still compiles + didn't grow a page" check, install:
```bash
# macOS
brew install tectonic && pip install pypdf
# Debian/Ubuntu: apt install tectonic  (or cargo install tectonic) && pip install pypdf
```
If you skip this, that's fine — `pagecheck.py` self-skips when they're absent.

## Step 5 — Verify

- Tell the user to **restart Claude Code** (plugins/skills load at startup).
- Confirm the skill is present: it should appear as `/resume-tailor` (plain install) or
  `/resume-tailor:resume-tailor` (plugin install).
- Optionally validate the manifests if the repo is cloned locally:
  ```bash
  claude plugin validate /tmp/claude-resume-tailor
  ```

## Step 6 — Report back

Tell the user: which install path you used, whether the optional LaTeX tools were
installed, that they must restart Claude Code, and the exact command to run the skill
(`/resume-tailor` or `/resume-tailor:resume-tailor`). Then stop — do not run the skill
or edit any resume yourself.
