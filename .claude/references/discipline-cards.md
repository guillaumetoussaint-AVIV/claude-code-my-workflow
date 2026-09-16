# Discipline Cards

Short reference cards naming each discipline's dominant paper-type frequencies, top journals, preregistration norms, and method conventions. Read by `/research-ideation`, `/interview-me`, `/preregister`, and the `editor` agent (in `/review-paper --peer`) when the user gives a `paper_type` or domain hint without specifying a target journal.

**Scope.** Three cards ship: **economics**, **political science**, and **regional science & urban economics** (added 2026-09-14 by owner ask — see the card's own note). Other social sciences (psychology, sociology, public health) are deferred indefinitely (owner-set scope, 2026-06-10: econ + closely related fields — do not build without an explicit owner ask). To add your own discipline, copy a card section, fill the four fields (paper-type frequencies, journals, preregistration norms, method conventions), and reference the new short-name from `journal-profiles.md` and `methods-referee.md`.

**Maintenance.** When you add a journal profile to `journal-profiles.md`, cross-reference it here. When you add a paper type to `methods-referee.md`, cross-reference it here.

---

## Economics (`econ`)

**Paper-type frequencies (rough share of empirical work in top-5 journals).**

| Type | Share | Notes |
|---|---|---|
| Reduced-form | ~55% | DiD, IV, RD, event study, synthetic control. The dominant mode. |
| Structural | ~20% | DSGE, GE, IO empirical. Concentrated in macro / IO / labour. |
| Theory + empirics | ~15% | Theory-paper-with-empirical-test or empirical-paper-with-theory-section. |
| Descriptive | ~5% | Measurement / data-construction. Often the AEA P&P route. |
| Formal-theory | ~5% | Pure theory (micro, IO, contracts). More common in ECMA / TE / JET. |

**Dominant journals (shipped in `journal-profiles.md`).** AER, QJE, JPE, ECMA, ReStud. AEA P&P (proceedings) for descriptive / measurement work.

**Preregistration norms.**
- **Field experiments / RCTs:** mandatory in the **AEA RCT Registry** since 2018 for AEA-journal submission. Use `/preregister --style aea-rct`.
- **Lab experiments:** OSF / AsPredicted increasingly common; not yet uniformly required.
- **Observational / archival:** preregistration uncommon; pre-analysis plans appearing in some applied-micro corners.
- **Replication packages:** AEA Data and Code Availability Policy enforced; complete deposit at openICPSR.

**Method conventions.**
- Significance stars: AEA journals do **NOT** use stars in tables (AEA style guidance). Other journals (e.g., ReStud, JPubE) still allow them.
- Standard-error reporting: clustered SEs at treatment-assignment level expected; Conley / spatial SEs required for spatial data.
- Code: R, Stata, Python, Julia all accepted; replication packages must be self-contained and deterministic (`set.seed`).

**Cross-references.** `methods-referee.md` paper types: reduced-form, structural, theory+empirics, descriptive, formal-theory. `journal-profiles.md`: AER, QJE, JPE, ECMA, ReStud.

---

## Political Science (`poli-sci`)

**Paper-type frequencies (rough share of empirical work in top-3 journals).**

| Type | Share | Notes |
|---|---|---|
| Reduced-form | ~40% | Causal inference (DiD, IV, RD), observational identification. Strongest at AJPS. |
| Survey-experiment | ~25% | Vignette, conjoint, list-experiment, factorial. Strong at AJPS, JOP; rising at APSR. |
| Formal-theory | ~15% | Game-theoretic, mechanism-design, formal political theory. Strongest at APSR. |
| Descriptive | ~10% | Cross-national / historical / case-study description. |
| Theory + empirics | ~10% | Formal theory with empirical test of equilibrium predictions. |

**Dominant journals (shipped in `journal-profiles.md`).** APSR, AJPS, JOP. Subfield outlets (IO, World Politics, JOP-research-notes track) also strong.

**Preregistration norms.**
- **Survey experiments / lab experiments / field experiments:** OSF or AsPredicted increasingly expected. **AJPS Replication Policy** (since 2015) makes replication archive mandatory at acceptance, but preregistration itself is a community norm not a hard requirement.
- **Observational:** PAP (preanalysis plan) appearing in applied work; not yet uniform.
- **AEA RCT Registry** is for econ; political-science field experiments more often use OSF or EGAP's repository (egap.org) — though EGAP merged its registry into OSF in 2022.

**Method conventions.**
- Significance stars: ARE used (typical floor 0.05/0.01/0.001). APSA Style Manual governs citations.
- Standard-error reporting: clustered SEs at subject level for survey experiments, robust SEs (HC2 or HC3) standard.
- Replication archive: AJPS Replication Policy requires deposit before acceptance; APSR and JOP recommend.
- Code: R is dominant; Stata still common in IR / comparative; Python rising for text-as-data work.

**Cross-references.** `methods-referee.md` paper types: reduced-form, formal-theory, survey-experiment, theory+empirics, descriptive (structural is rare in poli-sci). `journal-profiles.md`: APSR, AJPS, JOP.

---

## Regional Science & Urban Economics (`regional-sci`)

> **Added 2026-09-14 by owner ask** (this fork's owner, for the K2 project). The scope note above
> reserves new disciplines for "an explicit owner ask" and limits them to "econ + closely related
> fields" — regional science is adjacent to econ and was requested directly, so both conditions
> hold. Recorded here rather than assumed.

**Paper-type frequencies (rough share of empirical work in the field's applied journals).**

| Type | Share | Notes |
|---|---|---|
| Reduced-form | ~40% | Regional panels, spatial panels, first-difference and cross-section designs. |
| Descriptive / measurement | ~30% | Markedly higher than in econ. Building a regional indicator, an accessibility index, small-area estimates, or an imputed stock variable is a publishable contribution in its own right. |
| Theory + empirics | ~15% | New economic geography, agglomeration, spatial equilibrium with an empirical test. |
| Structural | ~10% | Quantitative spatial equilibrium models; concentrated in the economics-facing journals. |
| Formal-theory | ~5% | Pure spatial theory. Rare in the policy-facing outlets. |

**Dominant journals.** `RSPP` ships in `journal-profiles.md`. The wider set, none of which is
profiled yet: *Journal of Regional Science*, *Papers in Regional Science*, *Regional Science and
Urban Economics*, *Journal of Urban Economics*, *Annals of Regional Science*, *Regional Studies*,
*Urban Studies*, *Journal of Housing Economics*, *Housing Studies*, *Environment and Planning A*.
The field spans an economics wing (RSUE, JUE) and a planning/geography wing (Regional Studies,
Urban Studies, EPA) whose refereeing tastes differ substantially — the economics wing presses on
identification, the planning wing on conceptual framing and policy reading.

**Preregistration norms.** Effectively none. The empirical work is overwhelmingly observational
and administrative-data-based, so there is no registry analogue to the AEA RCT Registry. Data and
code availability statements are increasingly expected at acceptance; a full deposit is not yet
uniformly enforced.

**Reporting conventions** *(what these venues expect to see on the page — not advice on what to estimate)*.

- **Significance stars ARE used**, unlike AEA-imprint journals. A `+` or `†` marker for 10% is
  common and accepted.
- **Spatial units are named and justified.** Referees ask which administrative tier the analysis
  sits at and why — in France, commune / EPCI / département / région; elsewhere NUTS, MSA, LAU.
  The modifiable areal unit problem is a live objection, not a formality.
- **For spatial models, the weight matrix is part of the result.** Contiguity order or distance
  band, and whether it is row-standardised, belong in the table note; papers that omit it get
  asked. Where a model's coefficients are not directly interpretable, decomposed effects are
  reported alongside them.
- **Maps are evidence and are held to figure standards** — projection, class breaks, legend units,
  and the source line all get reviewed. A choropleth with unexplained bins draws comment.
- **Code:** R dominates (`sf`, `spdep`, `spatialreg`); Stata and Python are both common; GIS
  outputs (QGIS, ArcGIS) appear in the planning wing.

**Cross-references.** `methods-referee.md` paper types: reduced-form, descriptive,
theory+empirics, structural. `journal-profiles.md`: RSPP — including its paper-type note that a
paper built on an *imputed* dependent variable should be refereed as `descriptive` first.

---

## How skills consume these cards

- **`/research-ideation`** — when the user names a topic without a discipline, the skill may infer one from context (citation style, vocabulary). The card supplies the default `paper_type` distribution to bias hypothesis generation.
- **`/interview-me`** — Phase 1 paper-type question uses the card's frequency table to order the option list (most-likely-first per discipline).
- **`/preregister`** — `--style` defaults to the card's preregistration-norms suggestion (e.g., `osf` for poli-sci, `aea-rct` for econ field experiments).
- **`editor`** (`/review-paper --peer`) — when the user gives `--peer` without naming a specific journal but with a discipline hint, the editor uses the card's "Dominant journals" list as the candidate set and asks for clarification.

---

## Adding a new discipline card

Copy this template:

```markdown
## [Discipline name] (`short-slug`)

**Paper-type frequencies.**
| Type | Share | Notes |
|---|---|---|
| ... |

**Dominant journals (shipped in `journal-profiles.md`).** [list]. [Optional: subfield outlets.]

**Preregistration norms.**
- [registry conventions per study type]

**Method conventions.**
- [significance stars / SE conventions / replication norms / dominant code language]

**Cross-references.** `methods-referee.md` paper types: [list]. `journal-profiles.md`: [list].
```

Then:

1. Add the card section above (alphabetically by short-slug).
2. Add concrete journal profiles to `journal-profiles.md` for at least the top-3 journals.
3. Add paper types to `methods-referee.md` if your field uses categories not already there (e.g., qualitative-case-study for sociology, mixed-methods for public health).
4. Cross-reference the new short-slug from `/research-ideation` and `/interview-me` if those skills should respect the new defaults.

---

## Where this file lives

- **File:** `.claude/references/discipline-cards.md`
- **Schema parallel:** `.claude/references/journal-profiles.md` (per-journal) and `.claude/references/audit-pet-peeves.md` (living-catalogue format).
- **Consumed by:** `/research-ideation`, `/interview-me`, `/preregister`, `editor` agent.
