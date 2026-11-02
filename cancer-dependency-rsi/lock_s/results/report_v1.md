# External evaluation report — scientific-only track (Lock2 `lock2-scientific-only-v1-ce2b56c295fe`)

**Status:** executed once (2026-10-28T21:35Z) via `src/run_external_eval.py` under run_bounded (24.5 s wall, 385 MB peak RSS, no timeout/kill). Result: [`external_v1.json`](external_v1.json); per-gene displacement: [`external_v1_gene_displacement.csv`](external_v1_gene_displacement.csv). Lock2 commit sha256 `e04d04b8…`; protocol `lock_s/scientific_protocol_v1.json`; passing lock review `reviews/lock_s_high_review_v4.md` (94/100). **C is now consumed**; any further use of C is exploratory.

## Primary (decision) — confirmatory207 / mean_abs_delta / base_strength

| quantity | value |
|---|---|
| partial Spearman ρ (D_g vs L_g, adj. ranked \|AdherentMean\|) | **−0.1458** |
| donor-cluster 95% percentile interval (5,000 reps, 144 donors) | **[−0.1753, −0.1137]** |
| failed replicates | 0 / 5,000 |
| models / donors analysed; exclusions | 148 / 144; none |
| frozen decision (δ = 0.20) | **BOUND** |

**Frozen claim language (BOUND):** within the fixed 207-gene panel and conditional on the 6 measured Broad format models, the panel-wide association between observed format-bundle score lability and donor-averaged organoid displacement from the fixed 2D ordering, beyond baseline strength, is below the predeclared material magnitude 0.20. Observed format lability does not materially track organoid displacement in this panel. Not equivalence for other genes, populations or latent biological sensitivity; association only.

**Additional faithful description (not a new claim):** the interval excludes zero and is entirely negative — the direction is *opposite* to the preregistered positive conjecture. Within this panel, genes whose scores were more labile between Dome and Plastic formats were, if anything, slightly *less* displaced in Sanger organoids beyond baseline strength. This contradicts the conjectured positive environment→transfer link at the panel level, while the magnitude remains below the material threshold.

## Secondary Holm family (FWER 0.05; H0 ρ = 0)

| member | ρ | 95% donor interval | descriptive δ-decision | Holm-adj. p | reject ρ=0 |
|---|---|---|---|---|---|
| S1 null-calibrated displacement | −0.2089 | [−0.2300, −0.1866] | INCONCLUSIVE (straddles −0.20) | 0.0016 | yes |
| S2 TMOD1-alias 208 genes | −0.1449 | [−0.1750, −0.1131] | BOUND | 0.0016 | yes |
| S3 v1_1 library for 13 dual models | −0.1505 | [−0.1784, −0.1148] | BOUND | 0.0016 | yes |
| S4 unadjusted (Spearman) | −0.2169 | [−0.2449, −0.1846] | INCONCLUSIVE (straddles −0.20) | 0.0016 | yes |

All four reject ρ = 0 in the negative direction (p floor 2/5001 per member). Secondaries never override the primary decision. **Caution:** removing the mechanical rank-position component (S1) or the baseline adjustment (S4) moves the estimate to about −0.21, with intervals straddling −0.20. The BOUND therefore depends on the frozen primary definition; it is not robust to these sensitivity definitions with respect to δ (sign is robust).

## Stability (Broad composition / gene blocks; never decision)

- Broad model-cluster bootstrap (2,000): 2.5–97.5% [−0.208, −0.035]; leave-one-model-out range −0.166 … −0.082 (ACH-000178 removal weakest).
- Lineage-cluster bootstraps: all intervals ≤ 0 (e.g. split [−0.209, −0.032]; ACH-003052=Pancreas [−0.186, −0.001]).
- Pathway-block bootstrap over genes (11 blocks): [−0.264, −0.016].
- Interpretation: the negative sign is stable to Broad-model and gene-block composition; the **magnitude** is considerably less certain than the donor interval suggests, because the donor interval conditions on the fixed genes and measured Broad models. Under gene-block resampling the upper tail of |ρ| exceeds 0.20.

## Limitations (disclosed)

- Donor interval is conditional on the fixed 207 genes, the 6 measured Broad models (donors unresolved) and processed measurements; normalization uncertainty (Sanger spline/ComBat within organoid cohort; Broad Chronos) is not propagated.
- Panel genes were selected partly for environment differences (Tier-A tails excluded; class-level selection remains).
- L_g is *observed* score lability (includes measurement noise); no latent sensitivity or causal claim.
- AdherentMean reference ordering derives from processed Broad data and is part of the endpoint definition.
- Retrospective validation; public literature exposure cannot be excluded. Pre-Lock2 access was ID-only (transient text parsing; exposure log).

## Gate implications (proposed; subject to independent review and terminal adjudication)

- **C6 candidate:** a predeclared informative bound (|ρ| < 0.20) plus sign evidence against the positive conjecture. Whether it qualifies as a previously unreported, meaningful finding requires review and the final C1 novelty refresh.
- **C10:** primary + Holm secondaries + stability done; sensitivity to the S1/S4 definitions limits robustness of the bound; no positive-control/assay-sensitivity analysis was preregistered.
- **Unchanged:** C4 (policy freeze), C8, C9, C13 unmet; G2 FAIL. `prediction_improvement`: not evaluated; `policy_improvement`: not started.

## Review addendum (reviews/external_result_high_review_v1.md: 93/100; execution valid; BOUND; C6 PARTIAL)

- LOW correction: the lineage scenario `all_possibly_shared` has a single cluster, so its "interval" is the point value repeated and provides **no** stability evidence; lineage-stability statements rest only on the multi-cluster scenarios.
- Surviving conclusions (C10 documentation): (i) the **sign** (negative, opposite to the positive conjecture) survives all four Holm secondaries and all multi-cluster Broad/lineage and gene-block stability analyses; (ii) the **magnitude bound** |ρ| < 0.20 holds for the frozen primary and S2/S3 only; it does not hold robustly under S1 (null-calibrated), S4 (unadjusted), Broad model-cluster or gene-block resampling, whose ranges cross −0.20. Claims are restricted accordingly.
- No dependency-invariance claim is made: no positive dependency evidence, equivalence evidence or assay-sensitivity analysis supports invariance. Any further outcome-dependent analysis of C is exploratory.
