# sgen011-C — metadata-only identifiability discriminator, framings A vs B (ledger-locked)

Authority: sol-xhigh consult v2 2026-10-29 (SGEN011: C). Metadata only; no
dependency outcomes anywhere in inputs. Inputs are the sgen010 hash-pinned
files + established_pool_v4.json assignments.

## Population
Established pool: 1,106 models / 1,069 confirmed SIDP / 1,068 linked patient
components (components are the independence unit). 11 organoids established;
97 screened organoids identity-unresolved and INELIGIBLE.

## Framings under test
A (cell-line association): environment-associated dependency question across
measured culture environments in cell lines. REQUIRES metadata to establish
the SCREENING environment per model (format/medium actually screened in).
GrowthPattern/OnboardedMedia are onboarding annotations; per xhigh they do
not by themselves establish experimental format or screening medium.
B (organoid): Lock-S-adjacent organoid design on established organoids only.

## Computations (fixed before probing)
1. Provenance audit (A): does any supplied metadata field record the actual
   screening format/medium per ScreenID? CRISPRScreenMap fields enumerated;
   Model.csv environment-adjacent fields enumerated with population rates in
   the established pool. PASS requires a field that denotes screened-in
   environment (not onboarding/default), populated for >=90% of established
   screened models.
2. Effective size (A): linked patient components overall and within the
   largest 5 lineages, split by the candidate environment variable if (1)
   passes; attainable precision for a patient-level Spearman estimand:
   SE = 1/sqrt(n-3) on Fisher-z scale; minimum detectable |rho| at 80% power,
   two-sided alpha=.05 (single primary family; FWER note if split by lineage:
   alpha/5). PASS requires min detectable |rho| <= 0.146 (the Lock-S observed
   magnitude) in the primary pooled analysis.
3. Effective size (B): established organoid patient components n; same
   precision computation. PASS requires n giving min detectable |rho| <= 0.146.
4. Confounding screen (A, descriptive): association of candidate environment
   variable with lineage (Cramer's V) on metadata only; reported, not gated,
   unless (1) passes.

## Decision rule (fixed)
- A passes iff (1) provenance PASS and (2) precision PASS.
- B passes iff (3) precision PASS (identity already established by sgen010).
- Both pass -> prefer B (xhigh). Only A -> A with narrow associative reading.
  Only B -> B. Neither -> NEITHER_PASSES: outcome generation rejected; next
  capital = identity crosswalk for unresolved organoids and/or screening-
  environment provenance source.
- Unsupported nuisance assumptions -> unresolved feasibility (counts as fail).
Gate advanced: C3/C4 design support only. No outcome access in this generation.

## Amendment v2 (2026-10-29; responds to sol-high review v1, 82, 1 high)
- SCOPE NARROWED (high): this screen tests NECESSARY conditions only
  (provenance existence + optimistic Fisher-z precision bound). It does NOT
  specify or validate a scientific test: no estimand variables, aggregation,
  hypothesis family, or nuisance envelope is defined here, and pooled
  precision does not establish identifiability or within-lineage overlap.
  precision_A "pass" is relabeled an optimistic bound, never feasibility.
  The 0.146 threshold is a screen convention (designs unable to detect
  Lock-S-magnitude correlations are rejected early), NOT a justified target
  effect for either new design; a future lock must justify its own margin.
- A precision restricted to Cell Line models (organoids excluded).
- B pass additionally requires: authoritative identity crosswalk for any
  organoid beyond the 11 established AND renewed component-level C-exclusion
  checks. Precision alone never passes B.
- Derived inputs (established_pool_v4.json, screen_v7.json) hash-pinned and
  enforced by the executable; patient components reconstructed from pinned
  assignments, not imported as trusted counts.
Decision rule and verdict labels unchanged.

## Close-out (lead, 2026-10-29)
NEITHER_PASSES sustained through review arc 82 -> 91 -> 96 (estimator
micro-review 100). A fails provenance (no screened-environment record in
supplied metadata; pooled precision is an optimistic bound only). B fails
all three executable gates. Outcome generation rejected on current metadata.
Next capital: (i) authoritative crosswalk for 97 unresolved organoids +
renewed exclusion, and/or (ii) screening-environment provenance source;
B additionally needs ~366 organoid patients, exceeding all 108 screened
organoids, so B at Lock-S effect scale is infeasible in DepMap 26Q3 alone.
