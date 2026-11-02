# Novelty audit v3 — exact-claim refresh and interpretive-consequence dossier (C1 / C6)

Date: 2026-10-28 (post-Lock2). Supersedes v2 for the locked claim. It does not replace v1/v2 provenance.

## 1. Exact locked claim (frozen; no renaming)

> Across the fixed 207-gene confirmatory panel (Broad minipool test genes minus Tier-A selection tails, TMOD and low-reference-N genes, restricted to genes present in Sanger Table 6), the partial Spearman association is **ρ = −0.146 (donor 95% interval −0.175 to −0.114; BOUND under δ = 0.20)**. It relates **observed format-bundle score lability** (equal-weight mean over 6 Broad models of within-model mean |Chronos_Dome − Chronos_Plastic|) to **donor-averaged normalized displacement** of each gene's within-panel dependency rank from the fixed Broad 2D consensus ordering (AdherentMean), measured in 148 independently filtered Sanger organoid models from 144 donors (Broad-overlap donors excluded). The association is adjusted for ranked |AdherentMean|.
>
> Conditional on fixed genes, the 6 measured Broad models and processed measurements. Association only.

## 2. Searches (dated, reproducible)

| search | date | result |
|---|---|---|
| Europe PMC REST, 6 queries (`reviews/novelty_refresh_v3_search_FAILED_503.json`) | 2026-10-28 | all HTTP 503: **not executed** (no inference drawn) |
| NCBI PubMed E-utilities, 6 queries (`reviews/novelty_refresh_v3b_pubmed.json`) | 2026-10-28 | P1 format-lability×transfer: 0; P2 minipool×environment: 0; P3 cell-line→organoid dependency transfer: 12 (none relevant: antiviral CRISPR, reviews, unrelated); P4 NextGen DepMap 2026: 1 (= S1); P5 condition-dependent essentiality in organoid CRISPR screens: 2 (S1; gastric neuron–tumour organoid metabolic study); P6 Sanger organoid CRISPR 2026: 0 |
| Prior Europe PMC searches (v1, 3 queries) and full-text reads | 2026-10-28 | preserved in v1/v2 |
| Full-text re-read of cached primary sources S1/S2/S3 (`data/papers/PMC13581591.xml`, `PMC13581617.xml`, `PMC13664187.xml`) | 2026-10-28 | matrix below |

Search queries use title/abstract fields. Absence of hits is **not** proof of novelty. Bioinformatic preprints and supplement-only analyses may be missed.

## 3. Claim-by-prior matrix

| component of the locked relationship | S1 Broad NextGen (Nature 2026) | S2 Sanger organoid biobank (Nature 2026) | S3 October transfer study (Biology 2026) | intervening work found |
|---|---|---|---|---|
| Measured paired format/medium effects on dependencies (minipool, 250 genes, 7 models, 18 screens) | **Reported**: per-gene OLS (7 format genes q<0.05, e.g. ITGB1, ITGAV), class-level variance (integrin, actin regulation for format; lipid for medium) | — | — | none |
| Genome-wide 3D organoid vs 2D adherent differential dependency | **Reported** (94 vs 433, MeanDifference tests; source of AdherentMean) | — | — | none |
| Organoid dependency landscape / biomarkers, external Sanger cohort | Broad organoids only | **Reported** (dependency/biomarker maps; notes culture conditions "may ... alter gene dependencies", untested) | used as validation cohort | none |
| Cell-line→organoid transfer of dependency information | not as a transfer estimand | — | **Reported**: expression-based models rank *organoids per gene* for 20 preselected genes; weak/attenuated rank transfer | none |
| **Measured format lability (per gene) joined to an external organoid endpoint** | **not done**: minipool effects are not related to any external organoid ranking | not done | not done (predictors are expression features, not environmental sensitivity) | none found |
| **Within-organoid gene-rank displacement from a fixed 2D ordering, donor-averaged, panel-wide** | not done | not done | not done (S3 ranks organoids within gene, explicitly "not ranking genes within an individual organoid") | none found |
| Baseline-strength-adjusted partial association + donor-cluster bound with predeclared δ | — | — | — | none found |

**Conclusion (bounded):** no located source reports the substantive relationship. That relationship is whether measured paired format lability tracks external within-organoid displacement beyond reference strength in this panel. S1 supplies the predictor's ingredients and conjectures environment-shaped dependencies. S3 supplies a different transfer estimand. S2 supplies the external cohort. The locked result is therefore a **previously unreported, precisely bounded test**, under the stated search limits. This is not a claim that "nobody has tested" anything related.

## 4. Why this resolves the predeclared uncertainty

The G1-approved uncertainty (g1_question_v3; contract `question`) asked whether measured environmental (format) sensitivity explains dependency-transfer failure into an independent organoid cohort beyond baseline strength. Two plausible readings competed:

- (a) environment-labile genes are those whose 2D rank fails to transfer (positive association: lability as a transfer warning);
- (b) environment lability measured in a few paired models does not carry over to population-level organoid displacement.

The design pre-registered a positive conjecture and a material magnitude δ = 0.20 (justification: smallest panel-wide rank association considered material for this conditional question). The single locked test excluded |ρ| ≥ 0.20 in the frozen primary definition. Its interval was entirely negative. This discriminates between (a) and (b) for this panel: (a) receives no support. The small observed relationship runs opposite. The preregistered outcome categories (SIGNAL/BOUND/NEGATIVE/INCONCLUSIVE) were fixed before access, so the bound is not an arbitrary post-hoc small association.

## 5. Interpretive consequence (scope-limited statement)

**Within this 207-gene panel, greater measured format lability supplies no support for greater organoid rank displacement beyond reference strength. The observed relationship points in the opposite direction. Interpretation of a target's organoid relevance therefore requires direct transfer/context evidence rather than treating paired-format score lability as a sufficient transfer warning.**

Consequences for the atlas: per-gene lability values (S1 minipool) should not be read as predicting which genes' 2D dependency ranks fail to hold in patient-derived organoids. The atlas therefore reports environment evidence and external transfer evidence as separate components (atlas v2).

Not inferred: target-ranking utility, biological invariance or equivalence, latent environmental sensitivity, causation/mediation, clinical validity, or generalization to genes outside the panel, other environments (medium), other organoid cohorts or the genome.

## 6. Robustness limits carried into the claim (see C10 table)

The sign is robust. The magnitude bound holds for the frozen primary (and S2/S3) only. S1 (null-calibrated), S4 (unadjusted), Broad model-cluster and gene-block ranges cross −0.20. The claim is stated as a primary-definition bound with a robust negative direction, not as a definition-independent magnitude bound.
