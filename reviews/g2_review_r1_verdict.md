
codex
**FAIL — do not freeze Lock 1.** The G1-approved association is implementable, but the evaluator can reward defective uncertainty calculations, and several mandatory Lock-1 decisions remain unspecified.

No files were edited. No Sanger outcome values were inspected.

The primary development path reproduces **216 genes, partial ρ = 0.0552525**. Its mean-absolute-contrast operator correctly averages ACH-003040’s two contrasts within that model before averaging across six models. The partial operation is correctly Pearson correlation of rank residuals. The published OLS reproduction also passes: maximum coefficient discrepancy is **1.73×10⁻⁸**.

Six tests passed using the existing environment with filesystem-writing features disabled. The full suite could not run because the read-only sandbox blocks uv’s cache and pytest’s temporary files.

1. **HIGH — OLS receives perfect precision and stability without resampling.**  
   [Evaluator:114](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v1.py:114) reuses the unchanged full-data OLS estimate in every bootstrap replicate; line 123 does the same for leave-one-model-out analysis. Consequently, OLS gets zero interval width and zero LOMO range by construction.

   The Layer-A probe produced:

   | Operator | q | Interval width | LOMO range |
   |---|---:|---:|---:|
   | Approved mean absolute contrast | 0.6813 | 0.2466 | 0.1368 |
   | OLS coefficient magnitude | 0.9586 | 0 | 0 |

   This gives the policy a direct route to apparent improvement through an implementation defect. **Fix:** refit OLS within each properly grouped resample and omission, handling rank-deficient fits explicitly, or retain OLS solely as a reproduction anchor outside the scored search space.

2. **HIGH — “Calibration” does not measure calibration; degenerate estimators can score well.**  
   [Evaluator:126](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v1.py:126) scores how closely the *mean* permuted correlation approaches zero. That does not establish interval coverage, bias, type-I error, or predictive calibration. A severely underdispersed procedure can pass this check. The documented synthetic-null KS assessment is absent from implementation and tests.

   An in-memory zero-coefficient OLS probe was accepted as `success` with **q≈0.851**, although association with a constant predictor is mathematically undefined; numerical residuals generated an apparent correlation.

   **Fix:** invalidate constant or numerically degenerate rank residuals and nonfinite outputs. Validate each uncertainty procedure against frozen null and known-effect probes, including grouped dependence and coverage. Define defensible exchangeability for biological negative controls. q avoids directly rewarding effect magnitude or p-values, but currently rewards artificial sharpness and permits fishing among defective procedures.

3. **HIGH — Confirmatory science is not separated explicitly from development search.**  
   [Contract:22](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:22) refers to a “locked lability operator,” while the legal space contains four operators, three scopes, and three adjustments. G1 approved **mean of absolute contrasts, model-equal weighting, 207 genes, and adjustment for ranked absolute AdherentMean**. It did not authorize choosing their replacements through development optimization.

   Furthermore, `base_plus_organoid_mean` implements adjustment for a **single summed covariate**, rather than simultaneous adjustment for two covariates. Unknown configuration keys are accepted and change `config_id`; adding an unused note creates a different ID for identical science.

   **Fix:** freeze a separate, exact confirmatory configuration and prohibit development winners from altering it. Define exploratory operators precisely, reject unknown scientific fields, and hash canonical scientific configurations. Clarify that the proposed Sanger refit sensitivity cannot introduce quarantined outcomes into development.

4. **HIGH — The uncertainty target remains unresolved despite the correct caveat.**  
   [Contract:36](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:36) specifies a joint model-by-donor bootstrap while calling model resampling stability analysis conditional on the measured six models. It does not identify which interval governs SIGNAL/BOUND/NEGATIVE decisions.

   Broad donors remain unresolved, whereas [PLAN:108](/Users/bmarti44/github/bufferright/research/PLAN.md:108) requires conservative grouping plus a split-assumption sensitivity when donor independence is uncertain. The implementation resamples model IDs independently.

   **Fix:** distinguish the primary conditional inferential interval from environmental-panel stability analyses. Freeze grouping assumptions, resampling construction, interval method, replicate count, failed-replicate rules, and downstream recomputation. Retain the normalization-fitting limitation. Labeling a bootstrap “stability” alone does not justify using it for confirmatory decisions.

5. **HIGH — Mandatory Lock-1 artifacts and specifications are missing.**  
   Against [PLAN:111](/Users/bmarti44/github/bufferright/research/PLAN.md:111), the contract lacks a complete frozen bundle containing:

   - Final observation/donor partitions, overlap dispositions, and split manifests.
   - Explicitly pinned data, identifier, cohort, and preprocessing artifacts.
   - Generator prompts, schemas, retrieval budgets, and protocol version.
   - Frozen episode definitions and budgets; the robustness statistic used for frontier comparisons.
   - Exact secondary hypothesis families and their testing procedures.

   The five listed PLAN/GOAL/code hashes match, but they do not cover these missing artifacts. `partitions_provisional.json` remains provisional and retains the superseded external-data route.

   **Fix:** supply and hash the actual manifests and executable definitions. Also correct [PROTOCOL:3](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/PROTOCOL.md:3): placing the handoff last in the conflict hierarchy cannot authorize overriding the user-designated ground truth.

6. **MEDIUM — Primary eligibility reproduces; sensitivity eligibility does not match its label.**  
   [Evaluator:70](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v1.py:70) applies the low-reference-N filter to every scope. `all250_sensitivity` actually evaluates **242 genes** and drops TMOD through the reference join; it does not implement the TMOD→TMOD1 sensitivity.

   **Fix:** freeze explicit gene lists and alias mappings for each sensitivity, report exclusions, and name scopes according to their actual population. Test membership, rather than only the primary count.

7. **MEDIUM — C5 reproduction anchor passes; broader baseline adequacy is unestablished.**  
   [Baseline reproduction](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/data/baseline_reproduction_ols.json:1) establishes a credible measurement/design reproduction. It does not establish strongest-comparator performance, environmental ablation, or the other listed baseline results.

   Molecular prediction baselines may be inapplicable to the narrowed association question; they should not be imposed mechanically. **Fix:** document applicability and claim downgrades, implement the applicable strength-only/no-lability comparator, and distinguish **C5 anchor reproduced** from completion of the broader baseline requirements. External-outcome reproductions appropriately remain post-Lock-2 work.

8. **HIGH — Policy precision feasibility and the savings estimand are not locked.**  
   [Contract:97](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:97) proposes panel bootstrapping over gene-scope × operator-family tasks. These reuse nested genes and the same biological observations; eight task labels do not establish eight independent blocks. Reused-data labeling is honest, but does not justify the interval.

   The estimand is described as a paired **difference**, while the success criterion is **percentage savings**. Aggregation, strongest-baseline selection, and the corresponding confidence bound remain unspecified. “Check at pilot end” contradicts the required **Lock-1 precision-feasibility result**.

   **Fix:** define the engineering target population, dependence/replication structure, exact savings formula, baseline comparison procedure, censoring-compatible interval, and outcome-free feasibility analysis now. Preserve C9’s unresolved-cost status; reused engineering evidence cannot become reserved biological evidence.

9. **MEDIUM — The τq rule is permissible in principle, but incomplete; support rules lack episode definitions.**  
   [Contract:96](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:96) uses a predeclared development-derived threshold, which is acceptable. However, “final q among completed branches” leaves terminal versus best-so-far quality, invalid terminal nodes, and branches without valid results unresolved. Baseline attainability is unshown.

   The pilot threshold of four common episodes can be a declared engineering choice; it needs justification and a frozen episode list. The text also conflates replay-screen adequacy with fresh Phase-5 panel counts.

   **Fix:** define all τq edge cases and demonstrate baseline attainability. Specify support thresholds by phase and positive-weight ρ, with fixed denominators and the mandatory fresh-rollout fallback.

10. **HIGH — The status rules are not a total deterministic transition table.**  
    [Contract:86](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:86) leaves quartile conventions, ties, empty frontiers, missing sensitivities, “dominant” failures, “named fix,” and “independent configs” undefined. Recoverable and dead predicates can both hold without precedence. Recovery/reactivation rules and evidence-ID requirements are absent.

    **Fix:** implement a total function over admissible evidence, including missing-data cases, conflicts, recovery, and allocation reactivation. Freeze tests for these cases. Since statuses change legal actions, these ambiguities can change treatment assignment.

11. **HIGH — Campaign limits and resource matching remain incomplete.**  
    [Allocations:6](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/config/allocations.json:6) still says the campaign will be refined at Lock 1. The contract supplies selected maxima, but not total/per-phase wall, node, and model-call allocations or finalized no-progress rules.

    Evaluated-node count also omits unequal proposal, replay, review, failed-job, and learning costs. Unknown USD costs are disclosed correctly, but alternative-resource comparisons still require matching tolerances and allocation rules.

    **Fix:** freeze enforceable campaign allocations, shared-E0/history charging, deployment count, learning-overhead treatment, and matching of other material resources.

12. **MEDIUM — Round-5 residuals remain open; required tests are substantially incomplete.**  
    [Binding residuals](/Users/bmarti44/github/bufferright/research/reviews/lock1_residuals.md:3) have these dispositions:

    - **Header scaling:** unresolved and explicitly required **before Lock 1**. No bounded directory implementation/proven campaign bound or oversized-directory fixture is supplied.
    - **Memo namespace:** unresolved. Output-type and arm ownership keys, charging isolation, and execution-order invariance are absent. Its original deadline permits deferral until comparison execution, but an explicit enforceable gate is required.
    - **Replay-order wording — LOW:** fresh-rollout promotion is stated correctly in Phase 4, but §0.4.6’s retention wording still needs its promised replay-only qualification.

    [Current tests](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_lineage_cli.py:6) cover basic lineage rules and a CLI refusal. They do not test explicit cycles/version mismatches, nested donors/folds, partition leakage, hidden-outcome invariance across rendered inputs, arm execution order, unsupported replay, memo reconstruction, calibration coverage, evaluator compatibility, or actual access logging. Reservation concurrency/retries/interruption and resume idempotence are also absent.

    **Fix:** complete G2 acceptance tests. For legitimately later components, record a specific blocking gate and acceptance criteria. Blanket refusal by a CLI skeleton does not verify the eventual guarded execution path.

The G1 narrowing remains defensible, and the primary estimator and OLS reproduction are useful foundations. They do not resolve the evaluator defects or supply the missing freeze decisions.

SCORE: 54
tokens used
72,540
**FAIL — do not freeze Lock 1.** The G1-approved association is implementable, but the evaluator can reward defective uncertainty calculations, and several mandatory Lock-1 decisions remain unspecified.

No files were edited. No Sanger outcome values were inspected.

The primary development path reproduces **216 genes, partial ρ = 0.0552525**. Its mean-absolute-contrast operator correctly averages ACH-003040’s two contrasts within that model before averaging across six models. The partial operation is correctly Pearson correlation of rank residuals. The published OLS reproduction also passes: maximum coefficient discrepancy is **1.73×10⁻⁸**.

Six tests passed using the existing environment with filesystem-writing features disabled. The full suite could not run because the read-only sandbox blocks uv’s cache and pytest’s temporary files.

1. **HIGH — OLS receives perfect precision and stability without resampling.**  
   [Evaluator:114](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v1.py:114) reuses the unchanged full-data OLS estimate in every bootstrap replicate; line 123 does the same for leave-one-model-out analysis. Consequently, OLS gets zero interval width and zero LOMO range by construction.

   The Layer-A probe produced:

   | Operator | q | Interval width | LOMO range |
   |---|---:|---:|---:|
   | Approved mean absolute contrast | 0.6813 | 0.2466 | 0.1368 |
   | OLS coefficient magnitude | 0.9586 | 0 | 0 |

   This gives the policy a direct route to apparent improvement through an implementation defect. **Fix:** refit OLS within each properly grouped resample and omission, handling rank-deficient fits explicitly, or retain OLS solely as a reproduction anchor outside the scored search space.

2. **HIGH — “Calibration” does not measure calibration; degenerate estimators can score well.**  
   [Evaluator:126](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v1.py:126) scores how closely the *mean* permuted correlation approaches zero. That does not establish interval coverage, bias, type-I error, or predictive calibration. A severely underdispersed procedure can pass this check. The documented synthetic-null KS assessment is absent from implementation and tests.

   An in-memory zero-coefficient OLS probe was accepted as `success` with **q≈0.851**, although association with a constant predictor is mathematically undefined; numerical residuals generated an apparent correlation.

   **Fix:** invalidate constant or numerically degenerate rank residuals and nonfinite outputs. Validate each uncertainty procedure against frozen null and known-effect probes, including grouped dependence and coverage. Define defensible exchangeability for biological negative controls. q avoids directly rewarding effect magnitude or p-values, but currently rewards artificial sharpness and permits fishing among defective procedures.

3. **HIGH — Confirmatory science is not separated explicitly from development search.**  
   [Contract:22](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:22) refers to a “locked lability operator,” while the legal space contains four operators, three scopes, and three adjustments. G1 approved **mean of absolute contrasts, model-equal weighting, 207 genes, and adjustment for ranked absolute AdherentMean**. It did not authorize choosing their replacements through development optimization.

   Furthermore, `base_plus_organoid_mean` implements adjustment for a **single summed covariate**, rather than simultaneous adjustment for two covariates. Unknown configuration keys are accepted and change `config_id`; adding an unused note creates a different ID for identical science.

   **Fix:** freeze a separate, exact confirmatory configuration and prohibit development winners from altering it. Define exploratory operators precisely, reject unknown scientific fields, and hash canonical scientific configurations. Clarify that the proposed Sanger refit sensitivity cannot introduce quarantined outcomes into development.

4. **HIGH — The uncertainty target remains unresolved despite the correct caveat.**  
   [Contract:36](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:36) specifies a joint model-by-donor bootstrap while calling model resampling stability analysis conditional on the measured six models. It does not identify which interval governs SIGNAL/BOUND/NEGATIVE decisions.

   Broad donors remain unresolved, whereas [PLAN:108](/Users/bmarti44/github/bufferright/research/PLAN.md:108) requires conservative grouping plus a split-assumption sensitivity when donor independence is uncertain. The implementation resamples model IDs independently.

   **Fix:** distinguish the primary conditional inferential interval from environmental-panel stability analyses. Freeze grouping assumptions, resampling construction, interval method, replicate count, failed-replicate rules, and downstream recomputation. Retain the normalization-fitting limitation. Labeling a bootstrap “stability” alone does not justify using it for confirmatory decisions.

5. **HIGH — Mandatory Lock-1 artifacts and specifications are missing.**  
   Against [PLAN:111](/Users/bmarti44/github/bufferright/research/PLAN.md:111), the contract lacks a complete frozen bundle containing:

   - Final observation/donor partitions, overlap dispositions, and split manifests.
   - Explicitly pinned data, identifier, cohort, and preprocessing artifacts.
   - Generator prompts, schemas, retrieval budgets, and protocol version.
   - Frozen episode definitions and budgets; the robustness statistic used for frontier comparisons.
   - Exact secondary hypothesis families and their testing procedures.

   The five listed PLAN/GOAL/code hashes match, but they do not cover these missing artifacts. `partitions_provisional.json` remains provisional and retains the superseded external-data route.

   **Fix:** supply and hash the actual manifests and executable definitions. Also correct [PROTOCOL:3](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/PROTOCOL.md:3): placing the handoff last in the conflict hierarchy cannot authorize overriding the user-designated ground truth.

6. **MEDIUM — Primary eligibility reproduces; sensitivity eligibility does not match its label.**  
   [Evaluator:70](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v1.py:70) applies the low-reference-N filter to every scope. `all250_sensitivity` actually evaluates **242 genes** and drops TMOD through the reference join; it does not implement the TMOD→TMOD1 sensitivity.

   **Fix:** freeze explicit gene lists and alias mappings for each sensitivity, report exclusions, and name scopes according to their actual population. Test membership, rather than only the primary count.

7. **MEDIUM — C5 reproduction anchor passes; broader baseline adequacy is unestablished.**  
   [Baseline reproduction](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/data/baseline_reproduction_ols.json:1) establishes a credible measurement/design reproduction. It does not establish strongest-comparator performance, environmental ablation, or the other listed baseline results.

   Molecular prediction baselines may be inapplicable to the narrowed association question; they should not be imposed mechanically. **Fix:** document applicability and claim downgrades, implement the applicable strength-only/no-lability comparator, and distinguish **C5 anchor reproduced** from completion of the broader baseline requirements. External-outcome reproductions appropriately remain post-Lock-2 work.

8. **HIGH — Policy precision feasibility and the savings estimand are not locked.**  
   [Contract:97](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:97) proposes panel bootstrapping over gene-scope × operator-family tasks. These reuse nested genes and the same biological observations; eight task labels do not establish eight independent blocks. Reused-data labeling is honest, but does not justify the interval.

   The estimand is described as a paired **difference**, while the success criterion is **percentage savings**. Aggregation, strongest-baseline selection, and the corresponding confidence bound remain unspecified. “Check at pilot end” contradicts the required **Lock-1 precision-feasibility result**.

   **Fix:** define the engineering target population, dependence/replication structure, exact savings formula, baseline comparison procedure, censoring-compatible interval, and outcome-free feasibility analysis now. Preserve C9’s unresolved-cost status; reused engineering evidence cannot become reserved biological evidence.

9. **MEDIUM — The τq rule is permissible in principle, but incomplete; support rules lack episode definitions.**  
   [Contract:96](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:96) uses a predeclared development-derived threshold, which is acceptable. However, “final q among completed branches” leaves terminal versus best-so-far quality, invalid terminal nodes, and branches without valid results unresolved. Baseline attainability is unshown.

   The pilot threshold of four common episodes can be a declared engineering choice; it needs justification and a frozen episode list. The text also conflates replay-screen adequacy with fresh Phase-5 panel counts.

   **Fix:** define all τq edge cases and demonstrate baseline attainability. Specify support thresholds by phase and positive-weight ρ, with fixed denominators and the mandatory fresh-rollout fallback.

10. **HIGH — The status rules are not a total deterministic transition table.**  
    [Contract:86](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:86) leaves quartile conventions, ties, empty frontiers, missing sensitivities, “dominant” failures, “named fix,” and “independent configs” undefined. Recoverable and dead predicates can both hold without precedence. Recovery/reactivation rules and evidence-ID requirements are absent.

    **Fix:** implement a total function over admissible evidence, including missing-data cases, conflicts, recovery, and allocation reactivation. Freeze tests for these cases. Since statuses change legal actions, these ambiguities can change treatment assignment.

11. **HIGH — Campaign limits and resource matching remain incomplete.**  
    [Allocations:6](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/config/allocations.json:6) still says the campaign will be refined at Lock 1. The contract supplies selected maxima, but not total/per-phase wall, node, and model-call allocations or finalized no-progress rules.

    Evaluated-node count also omits unequal proposal, replay, review, failed-job, and learning costs. Unknown USD costs are disclosed correctly, but alternative-resource comparisons still require matching tolerances and allocation rules.

    **Fix:** freeze enforceable campaign allocations, shared-E0/history charging, deployment count, learning-overhead treatment, and matching of other material resources.

12. **MEDIUM — Round-5 residuals remain open; required tests are substantially incomplete.**  
    [Binding residuals](/Users/bmarti44/github/bufferright/research/reviews/lock1_residuals.md:3) have these dispositions:

    - **Header scaling:** unresolved and explicitly required **before Lock 1**. No bounded directory implementation/proven campaign bound or oversized-directory fixture is supplied.
    - **Memo namespace:** unresolved. Output-type and arm ownership keys, charging isolation, and execution-order invariance are absent. Its original deadline permits deferral until comparison execution, but an explicit enforceable gate is required.
    - **Replay-order wording — LOW:** fresh-rollout promotion is stated correctly in Phase 4, but §0.4.6’s retention wording still needs its promised replay-only qualification.

    [Current tests](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_lineage_cli.py:6) cover basic lineage rules and a CLI refusal. They do not test explicit cycles/version mismatches, nested donors/folds, partition leakage, hidden-outcome invariance across rendered inputs, arm execution order, unsupported replay, memo reconstruction, calibration coverage, evaluator compatibility, or actual access logging. Reservation concurrency/retries/interruption and resume idempotence are also absent.

    **Fix:** complete G2 acceptance tests. For legitimately later components, record a specific blocking gate and acceptance criteria. Blanket refusal by a CLI skeleton does not verify the eventual guarded execution path.

The G1 narrowing remains defensible, and the primary estimator and OLS reproduction are useful foundations. They do not resolve the evaluator defects or supply the missing freeze decisions.

SCORE: 54
