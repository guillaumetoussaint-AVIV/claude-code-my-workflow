# CLAUDE.MD — K2

**Project:** K2 — *On the Economy of Housing Sustainability: Why Demography Matters*
**Institution:** Université Paris Dauphine–PSL
**Field:** Regional science / urban economics / housing & real-estate finance
**Target venue:** *Regional Science Policy & Practice* (RSPP) — profile in [`journal-profiles.md`](.claude/references/journal-profiles.md)
**Stage:** R&R — major revision **resubmitted**, awaiting the editor's verdict
**Branch:** main

The paper studies how population aging redistributes housing wealth across age cohorts and across
space in France, 2012–2022. Housing values for the full stock are imputed with a mass-appraisal
model (XGBoost; 42 models over 14 regional strata); the distributional question is then estimated
at EPCI level on log differences, with Spatial Durbin Models carrying the headline results.

---

## Scope Discipline

**Do exactly what was asked — nothing adjacent.** Do not add README files, build scripts,
`.gitignore` edits, helper utilities, or extra tooling that was not requested. If an addition
looks valuable, **list it as a suggestion at the end** and let the user decide.

A request for a figure is a request for a figure. Delivering a figure plus a README plus a build
script plus gitignore edits means the user now has to review four things to accept one, and the
usual outcome is that all four get thrown away.

**Before adding anything not named in the request, ask.** One line is cheaper than a revert.

---

## Working Agreement

- **Plan first, then contract.** Non-trivial work enters plan mode and the plan is saved to
  `quality_reports/plans/`. Once a plan is approved, coordinate the rest autonomously — come back
  only for genuine ambiguity or a decision that is the user's to make.
- **Elevated check-in cadence — first few sessions only.** While the workflow is still being
  learned, surface intermediate state more often than contractor mode would normally warrant.
  *Revisit this line once the workflow feels familiar; it is meant to expire.*
- **Don't make the user repeat themselves.** A decision made once is recorded in
  `quality_reports/decisions/` and honoured thereafter. A correction becomes a `[LEARN]` entry
  (see *How we remember*). If you are about to ask something that was already settled, read the
  decision record instead.
- **Visuals ship publication-ready or not at all.** Anything with a figure number on it is held to
  submission standard — no placeholder axes, no default palettes, no unlabelled units.
- **Rigour over speed.** A slower answer that is checked beats a fast one that is plausible.

---

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** — compile, render, or re-derive and confirm the output at the end of every task
- **Sources of truth are per-artifact** — see the table below; there is no single global source
- **Quality gates** — nothing ships below 80/100
- **[LEARN] tags** — when corrected, save `[LEARN:category] wrong → right` to [MEMORY.md](MEMORY.md)

Cross-session context lives in [MEMORY.md](MEMORY.md); past plans, specs, and session logs are in [quality_reports/](quality_reports/).

---

## Artifacts and Sources of Truth

| Artifact | Source of truth | Location | Tracked? |
|---|---|---|---|
| **Manuscript** | `K2_Without_Authors - V2 - Corrections - Final.docx` | repo root | no — deliberately untracked |
| **Response to referees** | `Retours K2.docx` | repo root | no |
| **Referee reports + EiC letter** | `RSPP - Retours.docx` | repo root | no |
| **Earlier drafts** | `Article_without_authors*.docx`, `K2 … Corrections.docx` | repo root | no |
| **Conference deck** | `Slides/*.tex` (Beamer) | `Slides/` | yes |
| **Bibliography** | `Bibliography_base.bib` | repo root | yes |
| **Analysis code** | arriving from another machine → `scripts/R/` | `scripts/R/` | yes |
| **Supporting literature** | `*.pdf` at root (Yang 2009, Carozzi 2019, …) | repo root | no |

**The `.docx` files stay untracked and are never added to `.gitignore`.** That is a standing
instruction, not an oversight — leaving them visible-but-untracked is deliberate.

**Word is authoritative for the manuscript.** The submission pipeline takes Word, and so do
co-authors and referees. There is no LaTeX copy of the paper and none is planned.

---

## How to Edit a Word Manuscript

The machine has no Pandoc and no Word automation, so manuscript work follows a strict protocol:

1. **Extract, don't guess.** Convert `.docx` → text before reasoning about it. A `.docx` is a zip;
   `word/document.xml` holds the body, `word/comments.xml` holds review comments. Write the
   extractor to the session scratchpad, never into the repo.
2. **Deliver edits as exact find-and-replace blocks.** Quote the *verbatim* existing sentence, then
   the replacement. The user applies them in Word, where track-changes and co-author comments live.
3. **Never silently reflow.** Do not rewrite a paragraph that was not in scope to make it read
   better. Changed text is changed on purpose, and is flagged as such.
4. **Whole-section rewrites are labelled as such**, with a one-line rationale naming the referee
   comment or defect they answer.
5. **The author writes the load-bearing prose.** Abstract, contribution paragraph, and the
   interpretation of results are written by the user, not drafted and accepted — see
   [`writing-with-ai.md`](.claude/rules/writing-with-ai.md), which explains why this is not
   negotiable for an external-facing document.
6. **Record what was accepted.** Every accepted substantive edit gets a line in
   `quality_reports/decisions/` — this is how round 3 remembers what round 2 decided.
7. **Never edit a `.docx` in place.** It is the user's working copy, and Word may have it open.

---

## Commands

```bash
# Repo health — run after ANY change. Also runs in pre-commit and CI.
# NEVER pipe it (`| tail`) to read the result: a pipeline returns the LAST
# command's status, so a failing suite reads as exit 0 and the verdict line is
# truncated away. Redirect, then read $? and the file.
./scripts/backtest.sh > /tmp/bt.log 2>&1; echo "EXIT=$?"; tail -5 /tmp/bt.log

# Quality score (accepts .tex, .qmd, and .R)
python scripts/quality_score.py Slides/K2_Conference.tex

# Palette sync (LaTeX ↔ SCSS name contract)
./scripts/check-palette-sync.sh
```

```bash
# Beamer, 3-pass with bibtex (Git Bash). MiKTeX is being installed; on Windows the
# TEXINPUTS separator is ';' not ':'. Confirmed empirically at install time.
cd Slides
TEXINPUTS="../Preambles;" xelatex -interaction=nonstopmode K2_Conference.tex
BIBINPUTS=".." bibtex K2_Conference
TEXINPUTS="../Preambles;" xelatex -interaction=nonstopmode K2_Conference.tex
TEXINPUTS="../Preambles;" xelatex -interaction=nonstopmode K2_Conference.tex
```

> **⚠ The backtest FAILS on this machine, and did so before any K2 change (baseline `9d371f0`).**
> Three of ten gates fail; **two are bugs in the checkers on Windows, not defects in this repo.**
> A new session must not assume its own edit caused this — compare against the baseline first.
>
> | Gate | Why it fails here | A real defect? |
> |---|---|---|
> | `ledger-coverage` | compares `os.path.relpath()` output (backslashes) against `git ls-files` output (forward slashes), so every tracked hook reads as "not tracked by git" | **No** — false failure. `git ls-files .claude/hooks/` lists all 8. |
> | `hook-battery` | feeds events as `python3 hook.py < file`; under Git Bash + the pyenv-win Python shim **stdin arrives empty**, so deny-cases emit nothing and allow-controls pass *vacuously* | **No** — but the suite proves nothing here. The hooks themselves work when driven by a **pipe**, which is how Claude Code invokes them. |
> | `staleness` | `guide/` and `docs/` HTML are stamped for a different source hash than the `.qmd`; re-rendering needs Quarto, which is not installed | Pre-existing upstream drift |
>
> **Consequence:** `./scripts/install-hooks.sh` would install a pre-commit hook that blocks every
> commit. It has **not** been run. Until those two bugs are fixed, gate on the four checks that do
> work here and that read our files: `surface-sync`, `links`, `derived-counts`, `repo-hygiene`.

**Toolchain status (2026-09-14).** Installed: Python 3.10.8, git, gh. Being installed: MiKTeX
(XeLaTeX). **Not installed:** R, Quarto, Pandoc. Do not write a command that assumes a tool this
line does not list — check first, and say so plainly if the tool is missing rather than emitting a
recipe that cannot run.

**Palette contract:** colour names in `Preambles/header.tex` must match SCSS variable names in
`Quarto/theme-template.scss`. Enforced by `check-palette-sync.sh` inside the backtest, so the
contract holds even though Quarto itself is dormant here. See [`Preambles/README.md`](Preambles/README.md).

---

## Dormant Machinery

This repo forks a **teaching** workflow: Beamer lectures mirrored to Quarto RevealJS and published
to GitHub Pages. K2 has no lectures and no HTML slides — conference talks are Beamer PDF.

**Not in use:** `Quarto/`, `docs/`, `guide/`, `scripts/sync_to_docs.sh`, `/deploy`, `/qa-quarto`,
`/translate-to-quarto`, `/create-lecture`, `/syllabus`, `/scaffold-exercises`, `/respond-to-eval`,
plus the two parked rules [`beamer-quarto-sync.md`](.claude/rules/beamer-quarto-sync.md) and
[`single-source-of-truth.md`](.claude/rules/single-source-of-truth.md).

**None of it is deleted, and deleting it would be a mistake:** `docs/index.html`,
`docs/workflow-guide.html`, `guide/workflow-guide.qmd`, and `guide/workflow-guide.html` are
*scanned surfaces* for `scripts/check-surface-sync.py`. Removing them fails the backtest. Parked,
reversible, and visible — which is the point.

---

## How we verify

- [`verification-ladder.md`](.claude/references/verification-ladder.md) — the seven rungs, from *qualify the checker* to the external oracle, and how the review loop converges.
- [`external-oracle-process.md`](.claude/references/external-oracle-process.md) — running an independent frontier-model referee and adjudicating what it returns.
- [`provenance-and-ground-truth.md`](.claude/references/provenance-and-ground-truth.md) — naming and pinning your oracles, classifying divergence, and the clean-room boundary.
- [`review-fencing.md`](.claude/rules/review-fencing.md) — reviewer independence is a property of the environment, not an instruction.
- [`replication-protocol.md`](.claude/rules/replication-protocol.md) — every number in the paper traces to the code that produced it.

**The binding constraint for K2:** the manuscript reports figures produced on another machine.
Until the analysis code lands in `scripts/R/`, numeric claims can only be checked for *internal
consistency*. A claim checked against the paper's own table is **not** a verified claim and must be
reported as such — see [`/credible-claims`](.claude/skills/credible-claims/SKILL.md).

**How we write** — [`writing-with-ai.md`](.claude/rules/writing-with-ai.md): internal vs external-facing documents, and the human-readable standard for anything with your name on it. The manuscript is external-facing; `/humanize` and `/voice-profile` apply to every paragraph that reaches it.

**The laws** — [`research-agent-laws.md`](.claude/references/research-agent-laws.md): 21 laws for running agents on research infrastructure, each paid for by a real incident.

## How we remember

- [`progress-reports.md`](.claude/rules/progress-reports.md) — GitHub issues as defect memory, `quality_reports/` as work memory, `MEMORY.md` as lesson memory.
- [`issue-ledger.md`](.claude/rules/issue-ledger.md) — the evidence standard an issue must meet, and the seven-section closure comment.
- [`repo-hygiene.md`](.claude/rules/repo-hygiene.md) — **scratch must not become main.** Enforced by `check-repo-hygiene.py` on every commit.
- `quality_reports/decisions/` — the answer to "didn't we already decide this?"

Nothing clears work until it has a row in [`quality_reports/qualification/LEDGER.md`](quality_reports/qualification/LEDGER.md) — run [`/vaccinate`](.claude/skills/vaccinate/SKILL.md) to put one there.

---

## Folder Structure

```
K2/
├── CLAUDE.MD                    # This file
├── MEMORY.md                    # Committed lessons ([LEARN] entries)
├── .claude/                     # Rules, skills, agents, hooks, references
├── Bibliography_base.bib        # Centralized bibliography (drives Beamer citations)
├── *.docx                       # Manuscript, referee reports, response — UNTRACKED
├── *.pdf                        # Supporting literature — UNTRACKED
├── Figures/                     # Figures for the deck
├── Preambles/header.tex         # Shared LaTeX preamble + palette
├── Slides/                      # Beamer .tex conference decks
├── scripts/                     # Repo gates + R analysis code (incoming)
├── quality_reports/             # Plans, specs, session logs, decisions, audits
├── explorations/                # Research sandbox (see rules)
├── templates/                   # Session log, spec, decision-record templates
├── master_supporting_docs/      # Archived papers and prior slides
└── Quarto/ docs/ guide/         # DORMANT — see "Dormant Machinery"
```

---

## Quality Thresholds (advisory)

| Score | Checkpoint | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | Submission / conference | Ready to leave the building |
| 95 | Excellence | Aspirational |

Enforced by `/commit` (halts + asks for override) **and** — once you run `./scripts/install-hooks.sh` — by a real git pre-commit hook (`.githooks/pre-commit`) that runs the full backtest gate suite plus the quality (≥80) gate on every commit. Bypass sparingly with `SKIP_QUALITY_GATE=1` or `--no-verify`.

---

## Skills Quick Reference

The full table lives in [README.md](README.md#skills-claudeskills). The ones that matter for K2:

- **R&R / manuscript:** `/review-paper --peer RSPP` `/seven-pass-review` `/respond-to-referees` `/adjudicate-review` `/verify-claims` `/proofread` `/humanize` `/voice-profile` `/submission-disclosures`
- **Slides:** `/compile-latex` `/visual-audit` `/slide-excellence` `/new-diagram` `/extract-tikz` `/teach-from-paper`
- **Data / reproducibility:** `/audit-reproducibility` `/diagnose` `/review-r` `/replication-package` `/capture-environment` `/differential-audit`
- **Research / writing:** `/lit-review` `/interview-me` `/credible-claims` `/challenge`
- **Verification / rigor:** `/vaccinate` `/oracle-review` `/deep-audit` `/blast-radius` `/verify-artifact`
- **Meta / workflow:** `/commit` `/learn` `/checkpoint` `/context-status` `/promote-memory` `/coauthor-brief`

---

## Beamer Macros

Defined in `Preambles/header.tex`. Deck-specific environments get added to this table as the
conference deck defines them.

| Macro / environment | Effect | Use case |
| --- | --- | --- |
| `\transitionslide{Title}` | Full-bleed `primary-blue` section break | Between the paper's main moves |
| `\key{...}` | Gold bold | The one number on a slide that matters |
| `\good{...}` / `\bad{...}` | Green / red | Signed effects, expected vs observed |
| `\muted{...}` | Grey | Sources, caveats, axis notes |
| `dag-node`, `observed-edge`, … | TikZ styles | Mechanism diagrams |

---

## Current Project State

| Artifact | State | Next action |
| --- | --- | --- |
| Manuscript (V2) | Resubmitted to RSPP, awaiting verdict | Anticipate round-2 objections |
| Response to referees | Drafted and submitted with V2 | Audit the answered-by-argument replies |
| Analysis code | On another machine | Import to `scripts/R/`, then `/audit-reproducibility` |
| `Bibliography_base.bib` | Populated from the manuscript reference list | `/validate-bib --semantic` when there is a network pass |
| Conference deck | Not started | Build after MiKTeX is verified |
| Toolchain | MiKTeX installing; R / Quarto / Pandoc absent | Compile `Slides/HelloWorld.tex` to prove the chain |

---

## Known Open Items

- **Moran (1950) is mis-attributed** in the manuscript reference list to *Journal of Regional
  Science*; it is *Biometrika* 37(1/2), 17–23. Corrected in `Bibliography_base.bib`; **not yet
  corrected in the `.docx`.**
- **Takáts's given name** renders as "El Hod" in the reference list; it is Előd. Same status.
- **A number to settle when the code lands:** the results section reports the summed direct effects
  as a **5.01%** decrease, while Table 4's three direct effects (−0.241, −0.180, −0.084) give
  ≈4.70% under the caption's own `exp(ΔX × β) − 1` formula. Unresolved — it needs the code, not a
  guess.
