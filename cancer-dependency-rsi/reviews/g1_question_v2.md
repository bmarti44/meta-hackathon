> SUPERSEDED (2026-10-28) by v3/v2 successor. Retained for audit trail.

# Gate G1 — narrowed identifiable question v2 (for sol-high re-review)

Supersedes v1 candidate. Incorporates G1 review (56/100) + sol-xhigh unstick (`reviews/unstick_g1.md`): six-model **format** analysis, one fixed endpoint, conditional on the selected panel.

## Primary development estimand (identifiable + joinable TODAY)
**Population:** the **223 genes** = 250-gene selected panel − 26 Tier-A selection-tail genes − 1 attrition (`TMOD`), conditional on the fixed selected panel (no genome-wide generalization).
**Environmental measurement (per gene g):** format-bundle lability
`L_g = mean over the 6 format-contrast models of |mean within-model (Chronos_Dome − Chronos_Plastic)|`
(model-equal-weighted; ACH-003040's two pairs averaged first; bundle = Matrigel-dome vs plastic, medium held fixed within pair; Chronos original units).
**Transfer measurement (per gene g, development/descriptive):** `T_g = |MeanDifference_g|` from the published Broad comparison (NextGen organoids n=94 vs lineage-matched adherent n=433; `organoids_vs_2d_gene_dependency_tests_full.csv`).
**Primary parameter:** partial Spearman association ρ(L, T | baseline strength |AdherentMean|) across the 223 genes. One parameter, one contrast, one target family. No gene-class × genotype × context search at G1.
**Join demonstrated:** 223/224 eligible genes join by symbol (attrition recorded). All inputs are manifested Layer-A files.

## Decision rules (disjoint; δ finalized at Lock 1 with this justification)
- Practical-relevance threshold **δ = 0.20** (candidate): rank associations below 0.20 explain <4% of rank variance and would not change target-trust decisions; S3's own transfer signal (ρ≈0.10–0.15) sits below it and is described by its authors as weak. δ is justified by decision relevance, **not** by our exploratory estimate (which is development evidence, already seen: raw ρ=0.167, partial ρ=0.086 — precisely why Broad-side results can never be confirmatory here).
- Development verdicts: `SIGNAL` (CI entirely > δ) / `BOUND` (CI entirely < δ ⇒ informative bound candidate for Lock 2) / `INCONCLUSIVE` (CI straddles δ). CIs from donor/model-cluster joint bootstrap (Phase 2 finalizes; feasibility widths in `data/precision_feasibility_v1.json`: model-bootstrap 95% CI width ≈0.24 around the raw ρ — a bound at δ=0.20 is precision-feasible only if the confirmatory estimate stays low; a SIGNAL claim at δ=0.20 is **not** feasible on current precision and is not promised).

## Confirmatory external endpoint (defined now, gated — Lock 2)
Sanger analogue: frozen per-gene lability values `L_g` (Broad-measured, locked) vs Sanger organoid dependency behavior for the same 223 genes (continuous corrected LFC ranking endpoint, exact form at Lock 1 after: HCM-SANG↔ACH crosswalk, donor-overlap exclusion vs Broad, duplicate-library rule, preprocessing-independence decision — development-only refit from counts or downgraded independence). One locked claim, evaluated once. If the Sanger route cannot be resolved by Lock 1, the external-transfer component is recorded **unmet** and the claim family narrows to the within-Broad environmental bound (still requiring its own independence justification) — recorded scope change per unstick fallback.

## What is explicitly NOT claimed
No causal explanation of transfer failure; no isolated geometry/serum effects; no genome-wide or unselected-gene generalization; no heterogeneity claim from sign flips; no per-gene discoveries at n=6 models (atlas reports continuous effects + uncertainty per gene, claims stay panel-wide).

## Novelty (one sentence, surviving S1/S2/S3)
S1 measured environmental sensitivity without linking it to transfer, and S3 quantified transfer attenuation without environmental attribution; a panel-conditional, selection-controlled test of whether **measured format lability predicts transfer degradation beyond baseline strength** — or a precision-supported bound showing it does not — is unreported in the searched literature (audit: `reviews/novelty_audit_v1.md`, refreshed at G7).

## Recorded scope reductions vs the ambitious goal (honest)
Genome-wide environmental claims: **dropped** (panel-conditional only). Medium-bundle confirmatory claims: deferred (4 models; secondary/descriptive only). Genotype/state-conditional environmental claims: dropped at current support. These components are recorded unmet unless later independent evidence (e.g., additional public controlled-environment data) reopens them under a new study ID.
