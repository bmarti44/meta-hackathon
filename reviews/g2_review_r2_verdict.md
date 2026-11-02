
codex
**FAIL — Lock 1 is not safe to freeze or start the pilot.** The remediation makes substantial progress, but defective uncertainty can still earn high quality, reservation concurrency remains unsafe, and several frozen specifications conflict.

**Verification:** 14 tests passed. Four tests requiring filesystem writes could not run in this read-only sandbox. The primary estimate reproduces exactly: **partial ρ = 0.0552525147**. Frozen scope memberships and prompt hashes reproduce. No files were edited; no Sanger outcome values were inspected.

1. **OLS artificial precision — RESOLVED.**  
   OLS is excluded from `LEGAL_OPERATORS`; attempts to score it return invalid. It remains a reproduction anchor. See [evaluator_v2.py:31](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:31).

2. **Calibration and degeneracy — PARTIALLY; HIGH remains.**  
   Constant-input guards and an interval-coverage calculation replace the former permuted-mean check. However, calibration failure merely forfeits 40% of q; defective sharpness and stability can still earn nearly **0.60**.

   My outcome-free synthetic probe used independent target values and six nearly identical model profiles:

   | Probe | Valid | Null coverage | Interval width | q |
   |---|---|---:|---:|---:|
   | Actual primary configuration | Yes | 72% | 0.23897 | 0.35068 |
   | Synthetic independent target, nearly identical models | Yes | **12%** | **0.00332** | **0.59610** |

   Thus, a procedure failing its own nominal 95% coverage check substantially outranks the primary configuration. Other actual E0 roots remain valid with coverage of **64–80%**.

   The calibration also permutes residuals across genes without a frozen justification for gene exchangeability or preservation of pathway dependence. Known-effect and grouped-dependence acceptance tests are absent. Moreover, bootstrap nonfinite returns are discarded without incrementing `fails`, and null-bootstrap `ff` is ignored. See [evaluator_v2.py:120](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:120).

   **Required:** define the coverage target and defensible probe-generating process, then impose an uncertainty-adequacy requirement before precision can improve q. Counting coverage is progress; accepting severe undercoverage remains unsafe.

3. **Confirmatory versus development configuration — RESOLVED.**  
   The separate confirmatory configuration fixes the approved scope, operator, adjustment, and endpoint independently of development winners. Two-covariate adjustment now uses two simultaneous columns. Unknown scientific keys are rejected, and the quarantined refit is restricted to Lock-2 evaluation. See [contract.json:126](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:126) and [evaluator_v2.py:95](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:95).

4. **Uncertainty target — PARTIALLY.**  
   The central ambiguity is repaired: donor-cluster percentile bootstrap governs decisions; Broad resampling is stability only. Replicates, seed, conditional target, and excessive-failure disposition are specified.

   The conservative Broad sensitivity still lacks an exact model-to-cluster mapping. “Same-lineage models” leaves a grouping choice after freezing. There is also no named acceptance gate for synthetic verification of the confirmatory donor bootstrap and downstream recomputation. Freeze the grouping artifact and gate that verification before Lock-2 execution. See [contract.json:133](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:133).

5. **Mandatory artifacts and hierarchy — PARTIALLY.**  
   Actual split/data manifests, prompts, episodes, allocations, secondary-family definitions, and the corrected hierarchy now exist. The listed data-manifest hashes and prompt hashes match.

   The recorded `PROTOCOL.md` hash is stale:

   - Recorded: `2fabf349…`
   - Actual: `2fa5149f…`

   More materially, the engineering panel definitions conflict, and the frozen generator schema is incompatible with the lineage interface, detailed below. These prevent treating the bundle as a coherent frozen specification. See [contract.json:105](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:105).

6. **Sensitivity eligibility and TMOD alias — RESOLVED.**  
   I independently regenerated membership in memory and verified all four complete sets: **216, 207, 242, and 208**. The filtered population is honestly named, and the alias sensitivity adds Broad `TMOD` with reference mapping to `TMOD1`. See [make_gene_scopes.py:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/make_gene_scopes.py:23). Runtime enforcement of those frozen sets has a separate defect below.

7. **Baseline adequacy — RESOLVED for the narrowed claims.**  
   Strength-only, unadjusted, and partial associations are recorded separately; molecular prediction baselines are explicitly inapplicable to this association estimand. C5 reproduction remains distinguished from predictive superiority or policy-baseline performance. See [baselines_dev.json:2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/data/baselines_dev.json:2).

8. **Savings estimand and precision feasibility — PARTIALLY.**  
   Recording C9 as unachievable-by-design is an acceptable disposition. The engineering comparison now defines a savings ratio, restricted-mean endpoint, execution-level replication, and separate biological limitations.

   Its design is still incomplete:

   - The contract includes `panel242_reference_filtered` in the nine primary task panels; the episode artifact says it is excluded from primary panels.
   - “The 2 fixed baselines” does not identify both baseline procedures.
   - Four rollout seeds are promised without their values or an exact seed-generation rule.
   - “Bootstrap max-statistic” lacks the construction needed to reproduce the strongest-baseline bound.
   - `precision_feasibility_now` describes a future pilot-based calculation, not a current result or executable frozen calculation.

   These restrict reproducibility of the descriptive engineering comparison; they do not require pretending C9 is attainable. See [contract.json:93](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:93).

9. **τq and support rules — PARTIALLY.**  
   Best-so-far quality, zero-valid branches, insufficient valid branches, and E0 attainability are now defined. Pilot support has a fixed denominator and an explicit fallback.

   The comparison population remains contradictory, while the contract’s Phase-5 “≥8 fresh panels” condition is not reconciled with the episode artifact’s primary-versus-sensitivity panel wording. Freeze one consistent population and admissibility rule. See [episodes.json:63](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/config/episodes.json:63).

10. **Deterministic status rules — PARTIALLY.**  
    Quartiles, ties, empty evidence, precedence, and saturation expiry now have executable conventions. Two defects remain:

    - The docstring requires **one failure class** to exceed 50%; implementation sums `implementation_failure` and `invalid_result`. A probe with one of each plus one success returns `recoverable`, although neither class dominates.
    - Two historical conceptual failures make a direction permanently `dead`, even after a later valid success. Recomputing over all history does not provide a recovery transition.

    These statuses affect allocation and legal actions. The current tests do not establish the claimed complete recovery behavior. See [status_rules.py:63](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/status_rules.py:63).

11. **Campaign allocations and reservation enforcement — PARTIALLY; HIGH remains.**  
    Numerical allocations, matching tolerances, overhead treatment, E0 charging, and terminal reserves are now documented.

    Reservation remains a non-atomic **read → check → append** operation. In a deterministic in-memory concurrency probe using the actual `reserve()` function, two callers each reserved **$0.60 against a $1 cap**, both successfully. Fsync does not serialize that transaction. The claimed concurrency test performs sequential reservations.

    Also, `budget.py` does not enforce campaign or phase node/model-call limits, cumulative wall allocations, or CPU-job concurrency. The allocation file’s “enforcement” claim exceeds the implementation. Reconciliation additionally lacks validation against duplicate reconciliation and invalid actual costs. See [budget.py:22](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/budget.py:22) and [allocations.json:55](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/config/allocations.json:55).

12. **Round-5 residuals and acceptance tests — PARTIALLY.**  
    History paging addresses the oversized directory requirement, and its 100,000-entry fixture passes. Memo keys include output type and arm ownership; basic order and charging checks pass. Replay-order wording is qualified.

    Named later gates for replay, memo reconstruction, access logging, and hidden-outcome invariance are reasonable deferrals. However, concurrency is incorrectly marked **DONE**, calibration lacks the necessary acceptance tests, and the deferred evaluator-compatibility requirement has no actual frozen probe set. The memo requirement to “construct MemoStore” also needs acceptance criteria verifying its use for every relevant generated artifact and charge. See [contract.json:160](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:160).

Three additional defects were reproduced:

- **HIGH — Nonfinite inputs can score successfully.** Replacing one target value with `+inf`, or one adjustment covariate with `+inf`, still returned `valid=True`, with q around **0.596**. Pandas ranking turns infinities into finite ranks before validation. Validate original arrays before ranking. See [estimators.py:53](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/estimators.py:53).

- **HIGH — Frozen membership silently changes at evaluation.** Removing one primary gene from the development delta table produced a valid **215-gene** result under the unchanged `primary216` configuration ID; q became **0.54613**. The evaluator intersects the frozen list with available rows instead of requiring exact membership. Fail closed on missing or duplicated members and report explicit exclusions. See [evaluator_v2.py:71](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:71).

- **MEDIUM — Generator and lineage parent representations disagree.** The frozen schema requires parent objects containing `attempt_id` and `contribution`; `validate_node()` expects hashable parent IDs. A schema-compliant refinement raises **`TypeError: ... unhashable type: 'dict'`**. The proposer also requests a JSON list while the named schema defines a single object. Freeze a consistent interface and test schema output through lineage validation. See [candidate_schema_v1.json:3](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/prompts/candidate_schema_v1.json:3) and [lineage.py:19](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/lineage.py:19).

The blocking repairs are the evaluator’s uncertainty acceptance and input invariants, atomic reservation and allocation enforcement, and a consistent frozen comparison/interface specification. Legitimate later tests can remain behind explicit gates.

SCORE: 74
tokens used
87,755
**FAIL — Lock 1 is not safe to freeze or start the pilot.** The remediation makes substantial progress, but defective uncertainty can still earn high quality, reservation concurrency remains unsafe, and several frozen specifications conflict.

**Verification:** 14 tests passed. Four tests requiring filesystem writes could not run in this read-only sandbox. The primary estimate reproduces exactly: **partial ρ = 0.0552525147**. Frozen scope memberships and prompt hashes reproduce. No files were edited; no Sanger outcome values were inspected.

1. **OLS artificial precision — RESOLVED.**  
   OLS is excluded from `LEGAL_OPERATORS`; attempts to score it return invalid. It remains a reproduction anchor. See [evaluator_v2.py:31](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:31).

2. **Calibration and degeneracy — PARTIALLY; HIGH remains.**  
   Constant-input guards and an interval-coverage calculation replace the former permuted-mean check. However, calibration failure merely forfeits 40% of q; defective sharpness and stability can still earn nearly **0.60**.

   My outcome-free synthetic probe used independent target values and six nearly identical model profiles:

   | Probe | Valid | Null coverage | Interval width | q |
   |---|---|---:|---:|---:|
   | Actual primary configuration | Yes | 72% | 0.23897 | 0.35068 |
   | Synthetic independent target, nearly identical models | Yes | **12%** | **0.00332** | **0.59610** |

   Thus, a procedure failing its own nominal 95% coverage check substantially outranks the primary configuration. Other actual E0 roots remain valid with coverage of **64–80%**.

   The calibration also permutes residuals across genes without a frozen justification for gene exchangeability or preservation of pathway dependence. Known-effect and grouped-dependence acceptance tests are absent. Moreover, bootstrap nonfinite returns are discarded without incrementing `fails`, and null-bootstrap `ff` is ignored. See [evaluator_v2.py:120](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:120).

   **Required:** define the coverage target and defensible probe-generating process, then impose an uncertainty-adequacy requirement before precision can improve q. Counting coverage is progress; accepting severe undercoverage remains unsafe.

3. **Confirmatory versus development configuration — RESOLVED.**  
   The separate confirmatory configuration fixes the approved scope, operator, adjustment, and endpoint independently of development winners. Two-covariate adjustment now uses two simultaneous columns. Unknown scientific keys are rejected, and the quarantined refit is restricted to Lock-2 evaluation. See [contract.json:126](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:126) and [evaluator_v2.py:95](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:95).

4. **Uncertainty target — PARTIALLY.**  
   The central ambiguity is repaired: donor-cluster percentile bootstrap governs decisions; Broad resampling is stability only. Replicates, seed, conditional target, and excessive-failure disposition are specified.

   The conservative Broad sensitivity still lacks an exact model-to-cluster mapping. “Same-lineage models” leaves a grouping choice after freezing. There is also no named acceptance gate for synthetic verification of the confirmatory donor bootstrap and downstream recomputation. Freeze the grouping artifact and gate that verification before Lock-2 execution. See [contract.json:133](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:133).

5. **Mandatory artifacts and hierarchy — PARTIALLY.**  
   Actual split/data manifests, prompts, episodes, allocations, secondary-family definitions, and the corrected hierarchy now exist. The listed data-manifest hashes and prompt hashes match.

   The recorded `PROTOCOL.md` hash is stale:

   - Recorded: `2fabf349…`
   - Actual: `2fa5149f…`

   More materially, the engineering panel definitions conflict, and the frozen generator schema is incompatible with the lineage interface, detailed below. These prevent treating the bundle as a coherent frozen specification. See [contract.json:105](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:105).

6. **Sensitivity eligibility and TMOD alias — RESOLVED.**  
   I independently regenerated membership in memory and verified all four complete sets: **216, 207, 242, and 208**. The filtered population is honestly named, and the alias sensitivity adds Broad `TMOD` with reference mapping to `TMOD1`. See [make_gene_scopes.py:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/make_gene_scopes.py:23). Runtime enforcement of those frozen sets has a separate defect below.

7. **Baseline adequacy — RESOLVED for the narrowed claims.**  
   Strength-only, unadjusted, and partial associations are recorded separately; molecular prediction baselines are explicitly inapplicable to this association estimand. C5 reproduction remains distinguished from predictive superiority or policy-baseline performance. See [baselines_dev.json:2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/data/baselines_dev.json:2).

8. **Savings estimand and precision feasibility — PARTIALLY.**  
   Recording C9 as unachievable-by-design is an acceptable disposition. The engineering comparison now defines a savings ratio, restricted-mean endpoint, execution-level replication, and separate biological limitations.

   Its design is still incomplete:

   - The contract includes `panel242_reference_filtered` in the nine primary task panels; the episode artifact says it is excluded from primary panels.
   - “The 2 fixed baselines” does not identify both baseline procedures.
   - Four rollout seeds are promised without their values or an exact seed-generation rule.
   - “Bootstrap max-statistic” lacks the construction needed to reproduce the strongest-baseline bound.
   - `precision_feasibility_now` describes a future pilot-based calculation, not a current result or executable frozen calculation.

   These restrict reproducibility of the descriptive engineering comparison; they do not require pretending C9 is attainable. See [contract.json:93](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:93).

9. **τq and support rules — PARTIALLY.**  
   Best-so-far quality, zero-valid branches, insufficient valid branches, and E0 attainability are now defined. Pilot support has a fixed denominator and an explicit fallback.

   The comparison population remains contradictory, while the contract’s Phase-5 “≥8 fresh panels” condition is not reconciled with the episode artifact’s primary-versus-sensitivity panel wording. Freeze one consistent population and admissibility rule. See [episodes.json:63](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/config/episodes.json:63).

10. **Deterministic status rules — PARTIALLY.**  
    Quartiles, ties, empty evidence, precedence, and saturation expiry now have executable conventions. Two defects remain:

    - The docstring requires **one failure class** to exceed 50%; implementation sums `implementation_failure` and `invalid_result`. A probe with one of each plus one success returns `recoverable`, although neither class dominates.
    - Two historical conceptual failures make a direction permanently `dead`, even after a later valid success. Recomputing over all history does not provide a recovery transition.

    These statuses affect allocation and legal actions. The current tests do not establish the claimed complete recovery behavior. See [status_rules.py:63](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/status_rules.py:63).

11. **Campaign allocations and reservation enforcement — PARTIALLY; HIGH remains.**  
    Numerical allocations, matching tolerances, overhead treatment, E0 charging, and terminal reserves are now documented.

    Reservation remains a non-atomic **read → check → append** operation. In a deterministic in-memory concurrency probe using the actual `reserve()` function, two callers each reserved **$0.60 against a $1 cap**, both successfully. Fsync does not serialize that transaction. The claimed concurrency test performs sequential reservations.

    Also, `budget.py` does not enforce campaign or phase node/model-call limits, cumulative wall allocations, or CPU-job concurrency. The allocation file’s “enforcement” claim exceeds the implementation. Reconciliation additionally lacks validation against duplicate reconciliation and invalid actual costs. See [budget.py:22](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/budget.py:22) and [allocations.json:55](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/config/allocations.json:55).

12. **Round-5 residuals and acceptance tests — PARTIALLY.**  
    History paging addresses the oversized directory requirement, and its 100,000-entry fixture passes. Memo keys include output type and arm ownership; basic order and charging checks pass. Replay-order wording is qualified.

    Named later gates for replay, memo reconstruction, access logging, and hidden-outcome invariance are reasonable deferrals. However, concurrency is incorrectly marked **DONE**, calibration lacks the necessary acceptance tests, and the deferred evaluator-compatibility requirement has no actual frozen probe set. The memo requirement to “construct MemoStore” also needs acceptance criteria verifying its use for every relevant generated artifact and charge. See [contract.json:160](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:160).

Three additional defects were reproduced:

- **HIGH — Nonfinite inputs can score successfully.** Replacing one target value with `+inf`, or one adjustment covariate with `+inf`, still returned `valid=True`, with q around **0.596**. Pandas ranking turns infinities into finite ranks before validation. Validate original arrays before ranking. See [estimators.py:53](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/estimators.py:53).

- **HIGH — Frozen membership silently changes at evaluation.** Removing one primary gene from the development delta table produced a valid **215-gene** result under the unchanged `primary216` configuration ID; q became **0.54613**. The evaluator intersects the frozen list with available rows instead of requiring exact membership. Fail closed on missing or duplicated members and report explicit exclusions. See [evaluator_v2.py:71](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/evaluator_v2.py:71).

- **MEDIUM — Generator and lineage parent representations disagree.** The frozen schema requires parent objects containing `attempt_id` and `contribution`; `validate_node()` expects hashable parent IDs. A schema-compliant refinement raises **`TypeError: ... unhashable type: 'dict'`**. The proposer also requests a JSON list while the named schema defines a single object. Freeze a consistent interface and test schema output through lineage validation. See [candidate_schema_v1.json:3](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/prompts/candidate_schema_v1.json:3) and [lineage.py:19](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/lineage.py:19).

The blocking repairs are the evaluator’s uncertainty acceptance and input invariants, atomic reservation and allocation enforcement, and a consistent frozen comparison/interface specification. Legitimate later tests can remain behind explicit gates.

SCORE: 74
