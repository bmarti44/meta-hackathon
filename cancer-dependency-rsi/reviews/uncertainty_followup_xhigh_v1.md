**Recommendation: no meaningful scientific policy optimization pilot is supported by the current development assets.** Use one unscored evaluator for the frozen external target, and run only algorithmic readiness diagnostics before Lock1. This preserves the biological question and every success criterion; it does not clear G2 or authorize generations.

The four outputs must remain distinct:

- **Scientific inference:** the locked external donor-bootstrap interval, conditional on the 207 genes, six measured Broad models, and fixed measured covariates. Its interpretation requires independent, appropriately sampled donors.
- **Conditional descriptive statistics:** the observed fixed-gene development correlation. With these inputs treated as fixed, it has no justified sampling interval from model resampling.
- **Model-composition stability:** Broad model bootstrap, leave-one-model-out, and specified grouping sensitivities. These describe changes when the measured model composition changes. Unresolved Broad donor identities prevent claiming donor-aware Broad uncertainty.
- **Algorithmic synthetic calibration:** performance against known targets under explicitly generated dependence. A pass establishes neither biological validity nor coverage under the real donor distribution.

**Exact scoring and validity rules**

Set `q=null` and `admissible_for_policy=false` for every current development configuration and every synthetic diagnostic. Never convert null to zero, rank candidates by it, or reward interval width. Retire the old coverage, permutation, and composite-q outputs completely; their numerical values provide no admission evidence.

For prospective scientific inference, use exactly the frozen `confirmatory207 / mean_abs_delta / base_strength` configuration. Preserve donor-equal weighting, endpoint normalization and fallback, average ranks for ties, and the exact rank-residual Pearson operation.

Resample **144 donor clusters**, retaining their nested organoids; recompute donor averaging and endpoint ranks in each draw. Keep Broad lability, consensus ordering, and adjustment covariates fixed. Preserve 5,000 replicates, seed 20261028, and the frozen percentile levels.

Reject malformed membership, unresolved external donor mappings, nonfinite inputs/results, and undefined adjustment operations. Declare a residual degenerate when

`norm(residual) <= 1e-12 * max(1, norm(centered_rank_vector))`.

A degenerate point estimate is invalid. Count every degenerate/nonfinite bootstrap replicate as failed. **More than 250 failures makes the interval INCONCLUSIVE.** Otherwise use successful replicates at the frozen percentile levels; nonfinite endpoints or width ≤0 also make it INCONCLUSIVE. Report failure counts. Do not substitute another interval after failure.

A valid interval is not automatically a biological success; apply the original frozen decision criteria.

**Cheapest useful grouped-dependence fixtures**

Use two synthetic fixtures for the estimator/aggregation kernel, with exact population targets. They need not pretend to be biological rank-displacement observations.

Index 207 genes by the complete factorial:

`a,b ∈ {-1,0,1}; c ∈ {-11,…,11}`.

Set baseline covariate `z=c`, and lability ranks proportional to  
`x=69a+23b+c`.

Define population donor means:

- Null: `μ=0.5+(69b−23a+c)/412`.
- Nonzero: `μ=0.5+(69b+23a+c)/412`.

After rank adjustment for `z`, the exact population partial correlations are **0** and **0.6**, respectively. Both population mean vectors have distinct entries.

For each independent donor generate bounded contributions

`D[d,g]=μ[g]+0.06*(a[g]*U[d]+V[d,c[g]]+E[d,g])`,

where all latent variables are independent symmetric ±1 draws except for their stated sharing. This supplies donor-wide dependence and gene-block dependence while keeping contributions in `[0,1]`.

Generate 144 donors; represent four donors twice to obtain 148 model records. Require exact invariance between the original donor table and the duplicated, correctly nested representation, using identical donor-resampling indices. Separately verify endpoint extraction with deterministic identity/reversal rankings; the contribution fixtures do not validate that extraction.

For each fixture, freeze 100 outer datasets and run the production bootstrap implementation. Require all intervals valid and at least 90/100 intervals to contain the exact target. Report binomial uncertainty. This is a cheap screen for gross algorithmic failure, **not certification of nominal coverage**. Also require deliberately constant/nonfinite fixtures to produce the specified invalid statuses. Freeze arrays, seeds, and thresholds before execution; a failure remains a failure.

**What the narrowed study could establish**

The external association can be informative: it asks whether measured lability tracks donor-averaged displacement beyond measured baseline strength for these fixed genes and Broad models. A sufficiently narrow, valid interval could bound that conditional association. Inclusion of zero alone establishes neither equivalence nor absence of association. Neither result supports causality or generalization to unmeasured genes or Broad models.

The gates **unrepairable by evaluator redesign with the present assets** are the absent independent reserved biological task panels and C9/all-in savings without material host-cost accounting. Reusing existing data or passing synthetic fixtures cannot replace either. Broad donor-aware population inference additionally needs missing provenance; conditioning on the six models avoids that claim without recovering it.

Nine coherent engineering panels, baselines, seeds, precision calculations, remaining deferred gates, and Sol-high ≥90 still require completion. Atlas-component reproduction does not establish C11 full-campaign reproduction. None of these criteria should be waived or relabeled.

**NextSPEC:** create a pre-Lock1 diagnostic-only specification containing the frozen primary configuration reference, null-q rules, invalid rules, the two fixtures above, deterministic extraction/grouping checks, seeds, acceptance thresholds, and existing local resource limits. Run it without Sanger outcome access or generations. Record algorithmic PASS/FAIL separately; keep G2 failed until its actual prerequisites are satisfied.