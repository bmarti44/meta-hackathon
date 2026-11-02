> SUPERSEDED (2026-10-28) by v3/v2 successor. Retained for audit trail.

# Novelty audit v1 — 2026-10-28 (Phase 1f; refresh required at G7 + terminal determination)

## Method
Full-text reads (Europe PMC XML, `data/papers/`): S1 PMC13581591, S2 PMC13581617, S3 PMC13664187. Dated Europe PMC searches 2026-10-28 (queries preserved in session record): culture/CRISPR/dependency/organoid (7 hits), culture-conditions transfer (14 hits), medium/essentiality 2025–2026 (176 hits, top reviewed). **Absence of a search hit is not proof of novelty** — claims below are candidates pending G1 review.

## Already established (controls / priors — NOT novelty)
1. **S1 (Broad NextGen):** class-level environmental effects in the 250-gene minipool — integrin/actin classes vary by **format** (plastic vs dome), lipid-metabolism class by **medium** (RPMI-FBS vs OPAC), via OLS on 18 screens/7 models. Also: 147 genome-scale NextGen screens, biomarker dependencies, CDK6/CDKN2A-GBM work.
2. **S2 (Sanger biobank):** 162-organoid dependency map, biomarker associations, organoid-specific essentials.
3. **S3 (Oct 2026 transfer study):** expression-only Elastic Net (20 genes) transfer quantification 2D→organoids (Broad-94 ρ=0.15, Sanger-148 ρ=0.10), beyond-lineage checks. **Explicitly did not disentangle** state/geometry/medium/lineage/platform contributions. Generic transfer prediction is therefore closed as a novelty claim.
4. Adjacent: murine MYC 3D-vs-2D fitness programs (PMC12055005, 2025) — different system, no human dependency-transfer estimand.

## Residual uncertainty (the gap)
Nobody has tested whether **measured** per-gene environmental sensitivity (paired medium/format deltas with proper joint uncertainty and heterogeneity) **explains which dependencies fail to transfer** — i.e., whether environment-labile genes are exactly where 2D→organoid relationships (dependency levels and/or biomarker associations) degrade, beyond lineage and baseline strength. S1 measured sensitivity (7 models, class-level report); S3 measured transfer failure (20 genes, no environmental attribution). The link, with correct independent-unit counting and heterogeneity-aware estimands, is unreported in the searched literature.

Our audit adds a sharpening fact: per-gene average deltas hide extreme heterogeneity (91–98% of test genes flip sign across model pairs). Any credible claim must therefore be **conditional** (which genes × which model contexts) — class-average or mean-effect versions are likely unidentifiable/misleading at n=7 models. Precision-supported **refutations/bounds** (e.g., "average environmental sensitivity does not explain transfer degradation beyond X") are acceptable G1 targets.

## Candidate claim ledger (exploratory; Lock 1 will bound the family)
- **CL-1 (primary candidate):** Among the 250 panel genes, transfer degradation of dependency behavior (traditional→NextGen organoid, Layer-A genome-wide data) increases with measured environmental sensitivity magnitude/heterogeneity, conditional on lineage + baseline dependency strength. *Falsifier:* no association (or reversed) under joint-uncertainty propagation and strongest-baseline controls. *Needs:* Layer-A genome-wide import, joint bootstrap, matched controls.
- **CL-2 (conditional form):** The CL-1 association is concentrated in specific gene classes/contexts (e.g., medium-labile lipid genes vs format-labile adhesion genes behave differently in transfer). *Risk:* n=7 models ⇒ classes, not genes, may be the finest honest resolution.
- **CL-3 (bound/refutation candidate):** After conditioning, environmental sensitivity explains < δ of transfer degradation (informative bound redirecting interpretation toward lineage/state/platform). Qualifies only with predeclared δ + sufficient precision.
- **Excluded as novelty:** re-deriving S1 class effects; re-running S3's 20-gene transfer; any average-effect "environment matters" statement without heterogeneity/conditioning.

## Open items for G1 gate
S1/S2 supplement + author-code deep read; Zenodo S3 code inspection; Layer-A genome-wide route decision; crosswalk completion; sol-high review of this audit + provenance (G1 gate requires ≥ 90).
