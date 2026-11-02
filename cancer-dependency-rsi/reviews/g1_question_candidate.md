# Gate G1 — candidate identifiable question (DRAFT for sol-high G1 review; not locked)

## Named question (v1 candidate)
**Within the Broad controlled environmental panel (7 models; 5 matched medium + 7 matched format contrasts; 250 selected genes) linked to Layer-A genome-wide traditional↔NextGen dependency data: does measured per-gene environmental sensitivity — magnitude and cross-model heterogeneity of paired medium/format deltas, propagated with donor/model-joint uncertainty — predict transfer degradation of dependency behavior from conventional models to organoids, beyond lineage, baseline dependency strength, and the strongest S3-style expression baseline?**

## Falsifiable alternatives
- H1 (conditional explanation): transfer degradation increases with environmental sensitivity in specific gene-class × context strata (medium-labile vs format-labile may differ), robust to joint-uncertainty propagation and ablation.
- H0/bound: after conditioning, environmental sensitivity explains < δ (δ to be predeclared at Lock 1 from development precision) of transfer degradation — an informative bound redirecting interpretation to lineage/state/platform.
- H-heterogeneity: only heterogeneity (sign-flipping across models), not mean magnitude, predicts degradation — implying model-context-specific rather than gene-intrinsic lability.

## Identifiability basis (measured, 2026-10-28)
- Paired contrasts exist at row level (manifested Chronos matrix 18×1000, 0 missing); direction integrity vs published OLS r=0.91/0.96 (test250).
- Independent units: **7 biological models** for environmental estimand (donor mapping for these 7 to confirm in crosswalk; ACH-003052 lineage gap open). Genes/contrasts are not independent units.
- Heterogeneity dominates (91–98% sign-flipping) ⇒ estimands are conditional/stratified; every claim reports all individual paired changes; no average-only claims.
- Transfer side (Layer-A): genome-wide matrix route pending (portal file set vs figshare result tables — Lock 1 decision with leakage audit of Chronos pre-training). If genome-wide route fails, question narrows to the 250-gene panel using NextGen-vs-traditional published test tables (documented narrowing, broader component unmet).
- Prior art excluded: S1 class-level format/medium effects (controls); S3 20-gene expression transfer (baseline to beat/explain, not the claim).

## What G1 still needs
Crosswalk completion (donors for the 7 models; HCM-SANG↔ACH), assay audit write-up, S3 Zenodo code inspection, sol-high review of provenance+novelty+this question ≥ 90. No adaptive search before G1 passes.
