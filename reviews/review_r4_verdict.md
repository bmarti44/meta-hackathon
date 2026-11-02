
codex
**Below 90. Eleven of the 12 prior findings are RESOLVED; one remains PARTIALLY resolved. Four additional findings remain open, including two high-severity issues.**

I read all four requested files in full. No files edited. Reviewed snapshots: PLAN `aaed9c882a47`, GOAL `5a0e393ac767`, handoff `2814f8f3edcd`, round-3 verdict `330c932ed695`. These verdicts assess the written execution contract.

The 12 requested verdicts follow.

| Item | Verdict | Quoted evidence and assessment |
|---|---|---|
| **R2 #3 — history-index leakage** | **RESOLVED** | [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) defines history as “**exhaustive over the episode’s admissible history**” and applies filtering to “**every input channel**.” The acceptance test covers “**complete rendered input and resulting decisions**.” This closes the previous conflicting index requirement. |
| **R2 #7 — policy-dependent support deletion** | **RESOLVED** | [PLAN:60](/Users/bmarti44/github/bufferright/research/PLAN.md:60) defines the common set as episodes supported for “**every compared policy at that ρ**,” with a “**fixed episode-level denominator**.” All policies use the same intersection; inadequate support invalidates the screen. |
| **R2 #8 — censored tie-break** | **RESOLVED** | [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) specifies “**restricted-mean cost-to-τ**” as `mean_e min(C_e(τ), B_ep)`, with “**censored episodes contribute B_ep**.” That defines an identifiable restricted endpoint, including all-nonattainment cases. Challenger ordering has a separate defect below. |
| **R2 #15 — discretionary fallback selection** | **RESOLVED** | [PLAN:121](/Users/bmarti44/github/bufferright/research/PLAN.md:121) requires fallback order “**recorded before any replay output exists**” and testing until a frozen allocation is spent. Every challenger receives a recorded disposition. The original discretionary fallback is closed. |
| **R2 #27 — unbounded pre-lock work** | **RESOLVED** | [PLAN:29](/Users/bmarti44/github/bufferright/research/PLAN.md:29) creates Phase-0 “**pre-lock budgets**,” review-round caps, repeat-failure limits and an untouchable terminal reserve. [PLAN:90](/Users/bmarti44/github/bufferright/research/PLAN.md:90) explicitly applies stopping assessment “**before Lock 1 too**.” Later parenthetical Lock-1 references are stale, but no longer remove the earlier binding allocation. |
| **R2 #30 — context overflow** | **PARTIALLY** | [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) adds deterministic partitioning, cross-direction ID lookup and retrieval budgets. However, “**each split receiving the complete ID directory**” leaves an unbounded mandatory input. Partitioning “**by direction**” also leaves a single large direction unbounded. The overflow mechanism can itself overflow. |
| **R3 #7 — exclusion bias** | **RESOLVED** | [PLAN:22](/Users/bmarti44/github/bufferright/research/PLAN.md:22) retains “**all assigned attempts, failures, and costs**,” permits only predeclared outcome-independent exclusions, and says an information/treatment-changing breach “**invalidates the affected comparison**.” Charging and logging explicitly do not repair biased inclusion. |
| **R3 #8 — donor nesting** | **RESOLVED** | [PLAN:108](/Users/bmarti44/github/bufferright/research/PLAN.md:108) resamples donors with “**all its nested models, cultures, contrasts, and every gene’s paired vector together**.” It also specifies conservative uncertain-donor grouping, sensitivity analysis, few-cluster qualification and nested-donor fixtures. This resolves the uncertainty-resampling defect; predictive folds remain a separate issue below. |
| **R3 #9 — causal gate** | **RESOLVED** | [PLAN:136](/Users/bmarti44/github/bufferright/research/PLAN.md:136) requires a “**causal estimand + identifying assumptions + evidence suitable under those assumptions**,” applies the gate at both locks and manuscript review, and otherwise restricts interpretation to measured interventions and predictive associations. |
| **R3 #10 — parent-local wording and feasibility** | **RESOLVED** | [PLAN:59](/Users/bmarti44/github/bufferright/research/PLAN.md:59) correctly calls the method “**history-dependent exact-context replay**.” It requires measuring attainable support on reordered traces, including overflow and budget variation, before relying on screening. |
| **R3 #11 — download bound** | **RESOLVED** | [PLAN:28](/Users/bmarti44/github/bufferright/research/PLAN.md:28) requires `min(20 GiB, available_disk/4)`, “**computed and persisted at each allocation**.” [GOAL:35](/Users/bmarti44/github/bufferright/research/GOAL.md:35) agrees. |
| **R3 #12 — closure overstatement** | **RESOLVED** | [PLAN:6](/Users/bmarti44/github/bufferright/research/PLAN.md:6) distinguishes “**Author dispositions claimed all fixed**” from independent round-3 findings and states closure requires later confirmation. It no longer presents author dispositions as independently verified closure. |

**R2 #30 remains medium severity.** Close it by specifying a token-bounded directory protocol: deterministic pagination or searchable ID lookup, bounded subdivisions within large directions, reserved space for instructions and retrieved records, and explicit handling when no legal rendering fits. Alternatively, enforce a campaign-size bound with a worst-case token calculation proving every mandatory rendering fits. Add fixtures where both the directory and one direction independently exceed context capacity.

I found four additional issues.

1. **HIGH — Predictive folds are not required to preserve donor groups.**

   **Evidence:** [PLAN:109](/Users/bmarti44/github/bufferright/research/PLAN.md:109) requires preprocessing and tuning “**inside development folds only**.” The explicit overlap test at [PLAN:112](/Users/bmarti44/github/bufferright/research/PLAN.md:112) is “**donor overlap A/B/C fails build**.” Donor nesting at [PLAN:108](/Users/bmarti44/github/bufferright/research/PLAN.md:108) governs uncertainty resampling, rather than fold construction.

   A row-level development split could place model D1 in training and model D2 from the same donor in validation. It would satisfy the stated across-layer overlap check and the new donor bootstrap requirement. Nevertheless, its predictive score could measure recognition of shared biological material rather than generalization to unseen donors. That score can influence baseline selection, policy rewards and the quality threshold.

   The blocked-evaluation requirement in [handoff:255](/Users/bmarti44/github/bufferright/research/cancer_rsi_handoff.txt:255) needs an explicit implementation inside predictive evaluation, as well as between A/B/C.

   **Fix:** Require fold manifests matched to the generalization claim. For unseen-donor prediction, keep every conservatively linked donor’s models, cultures and repeated observations in one fold, including nested tuning folds. Specify additional lineage/target/pathway blocking where claimed. Add a fixture with distinct model IDs sharing one donor. Preserve legitimate within-model environmental contrasts separately.

2. **HIGH — Duplicate rejection has no declared arm or episode scope.**

   **Evidence:** [PLAN:44](/Users/bmarti44/github/bufferright/research/PLAN.md:44) says “**same config new context = duplicate configuration**,” rejected unless replication is authorized. [PLAN:53](/Users/bmarti44/github/bufferright/research/PLAN.md:53) rejects duplicate `config_id` values and feeds rejection information back next round. Neither defines the lookup’s scope.

   A runner consulting the global ledger could reject a configuration in arm B because arm A already executed it. Reversing arm execution order could reverse which arm receives the rejection. Likewise, an unrevealed historical node could affect legal choices through duplicate detection without its outcome ever appearing in a prompt.

   This creates interference between arms and an information channel through hidden artifact existence. Filtering rendered records does not prevent it. It also conflicts with fresh evaluation across panels: the text distinguishes `evaluation_id` by data and split, yet its blanket configuration rule can reject the same scientific configuration on genuinely new evidence.

   **Fix:** Define duplicate eligibility against the arm’s episode-admissible history, with explicit study/panel/split scope. Permit the required symmetric evaluations across arms and independent panels under a frozen rule. A global artifact store may retain bytes, but hidden global membership must not change an arm’s observations or legal actions. Test that adding hidden or other-arm configurations—and reversing execution order—does not change either arm’s behavior.

3. **MEDIUM — The replay winner rule cannot resolve tied challengers above the incumbent.**

   **Evidence:** [PLAN:121](/Users/bmarti44/github/bufferright/research/PLAN.md:121) fresh-tests the “**top-1 challenger by J (ties per §0.4.6)**.” The final tie-break at [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) is “**incumbent retained**.”

   Suppose two challengers have identical J, attainment and restricted-mean cost, and both outperform the incumbent. “Incumbent retained” neither orders those challengers nor identifies the promised top-one fresh-test candidate. Applying it literally would retain an inferior incumbent; choosing a challenger introduces discretion.

   **Fix:** Add a total ordering frozen before replay, such as the pre-listed challenger order followed by immutable candidate ID. Apply incumbent retention only when the incumbent belongs to the tied best set. This is separate from the now-resolved censoring calculation and fallback-selection defects.

4. **MEDIUM — Deterministic replay-state reconstruction is asserted without reconciling LLM-produced state.**

   **Evidence:** [PLAN:55](/Users/bmarti44/github/bufferright/research/PLAN.md:55) requires “**All recomputation is deterministic**” and “**replayable bit-for-bit given the same revealed outcomes**.” Yet [PLAN:85](/Users/bmarti44/github/bufferright/research/PLAN.md:85) inserts a “**sol-xhigh direction summary + ranked proposal**,” and [PLAN:47](/Users/bmarti44/github/bufferright/research/PLAN.md:47) requires summaries and priorities to be reconstructed from admissible history.

   Freezing prompts, model ID and effort does not specify how repeated state reconstruction obtains identical summary and proposal bytes. Reinvoking the model can change those inputs even when admissible history is unchanged. That affects policy decisions, exact-context support and the interpretation of hidden-outcome invariance failures. Deterministic verification of catalog classifications does not settle free-text summaries or rankings.

   **Fix:** Define the reconstruction mechanism before comparison: deterministic transformations, or immutable memoized model outputs keyed by canonical admissible-state content and protocol version. Specify cache-miss behavior, costs and support treatment. Verify repeated reconstruction produces identical rendered inputs without another stochastic model call.

The remaining findings affect C4, C8 and C9: the plan still permits ambiguous isolation and scoring behavior in the experiments intended to demonstrate policy improvement. No critical finding identified; **two high and three medium findings remain open**.

SCORE: 86
tokens used
65,476
**Below 90. Eleven of the 12 prior findings are RESOLVED; one remains PARTIALLY resolved. Four additional findings remain open, including two high-severity issues.**

I read all four requested files in full. No files edited. Reviewed snapshots: PLAN `aaed9c882a47`, GOAL `5a0e393ac767`, handoff `2814f8f3edcd`, round-3 verdict `330c932ed695`. These verdicts assess the written execution contract.

The 12 requested verdicts follow.

| Item | Verdict | Quoted evidence and assessment |
|---|---|---|
| **R2 #3 — history-index leakage** | **RESOLVED** | [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) defines history as “**exhaustive over the episode’s admissible history**” and applies filtering to “**every input channel**.” The acceptance test covers “**complete rendered input and resulting decisions**.” This closes the previous conflicting index requirement. |
| **R2 #7 — policy-dependent support deletion** | **RESOLVED** | [PLAN:60](/Users/bmarti44/github/bufferright/research/PLAN.md:60) defines the common set as episodes supported for “**every compared policy at that ρ**,” with a “**fixed episode-level denominator**.” All policies use the same intersection; inadequate support invalidates the screen. |
| **R2 #8 — censored tie-break** | **RESOLVED** | [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) specifies “**restricted-mean cost-to-τ**” as `mean_e min(C_e(τ), B_ep)`, with “**censored episodes contribute B_ep**.” That defines an identifiable restricted endpoint, including all-nonattainment cases. Challenger ordering has a separate defect below. |
| **R2 #15 — discretionary fallback selection** | **RESOLVED** | [PLAN:121](/Users/bmarti44/github/bufferright/research/PLAN.md:121) requires fallback order “**recorded before any replay output exists**” and testing until a frozen allocation is spent. Every challenger receives a recorded disposition. The original discretionary fallback is closed. |
| **R2 #27 — unbounded pre-lock work** | **RESOLVED** | [PLAN:29](/Users/bmarti44/github/bufferright/research/PLAN.md:29) creates Phase-0 “**pre-lock budgets**,” review-round caps, repeat-failure limits and an untouchable terminal reserve. [PLAN:90](/Users/bmarti44/github/bufferright/research/PLAN.md:90) explicitly applies stopping assessment “**before Lock 1 too**.” Later parenthetical Lock-1 references are stale, but no longer remove the earlier binding allocation. |
| **R2 #30 — context overflow** | **PARTIALLY** | [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) adds deterministic partitioning, cross-direction ID lookup and retrieval budgets. However, “**each split receiving the complete ID directory**” leaves an unbounded mandatory input. Partitioning “**by direction**” also leaves a single large direction unbounded. The overflow mechanism can itself overflow. |
| **R3 #7 — exclusion bias** | **RESOLVED** | [PLAN:22](/Users/bmarti44/github/bufferright/research/PLAN.md:22) retains “**all assigned attempts, failures, and costs**,” permits only predeclared outcome-independent exclusions, and says an information/treatment-changing breach “**invalidates the affected comparison**.” Charging and logging explicitly do not repair biased inclusion. |
| **R3 #8 — donor nesting** | **RESOLVED** | [PLAN:108](/Users/bmarti44/github/bufferright/research/PLAN.md:108) resamples donors with “**all its nested models, cultures, contrasts, and every gene’s paired vector together**.” It also specifies conservative uncertain-donor grouping, sensitivity analysis, few-cluster qualification and nested-donor fixtures. This resolves the uncertainty-resampling defect; predictive folds remain a separate issue below. |
| **R3 #9 — causal gate** | **RESOLVED** | [PLAN:136](/Users/bmarti44/github/bufferright/research/PLAN.md:136) requires a “**causal estimand + identifying assumptions + evidence suitable under those assumptions**,” applies the gate at both locks and manuscript review, and otherwise restricts interpretation to measured interventions and predictive associations. |
| **R3 #10 — parent-local wording and feasibility** | **RESOLVED** | [PLAN:59](/Users/bmarti44/github/bufferright/research/PLAN.md:59) correctly calls the method “**history-dependent exact-context replay**.” It requires measuring attainable support on reordered traces, including overflow and budget variation, before relying on screening. |
| **R3 #11 — download bound** | **RESOLVED** | [PLAN:28](/Users/bmarti44/github/bufferright/research/PLAN.md:28) requires `min(20 GiB, available_disk/4)`, “**computed and persisted at each allocation**.” [GOAL:35](/Users/bmarti44/github/bufferright/research/GOAL.md:35) agrees. |
| **R3 #12 — closure overstatement** | **RESOLVED** | [PLAN:6](/Users/bmarti44/github/bufferright/research/PLAN.md:6) distinguishes “**Author dispositions claimed all fixed**” from independent round-3 findings and states closure requires later confirmation. It no longer presents author dispositions as independently verified closure. |

**R2 #30 remains medium severity.** Close it by specifying a token-bounded directory protocol: deterministic pagination or searchable ID lookup, bounded subdivisions within large directions, reserved space for instructions and retrieved records, and explicit handling when no legal rendering fits. Alternatively, enforce a campaign-size bound with a worst-case token calculation proving every mandatory rendering fits. Add fixtures where both the directory and one direction independently exceed context capacity.

I found four additional issues.

1. **HIGH — Predictive folds are not required to preserve donor groups.**

   **Evidence:** [PLAN:109](/Users/bmarti44/github/bufferright/research/PLAN.md:109) requires preprocessing and tuning “**inside development folds only**.” The explicit overlap test at [PLAN:112](/Users/bmarti44/github/bufferright/research/PLAN.md:112) is “**donor overlap A/B/C fails build**.” Donor nesting at [PLAN:108](/Users/bmarti44/github/bufferright/research/PLAN.md:108) governs uncertainty resampling, rather than fold construction.

   A row-level development split could place model D1 in training and model D2 from the same donor in validation. It would satisfy the stated across-layer overlap check and the new donor bootstrap requirement. Nevertheless, its predictive score could measure recognition of shared biological material rather than generalization to unseen donors. That score can influence baseline selection, policy rewards and the quality threshold.

   The blocked-evaluation requirement in [handoff:255](/Users/bmarti44/github/bufferright/research/cancer_rsi_handoff.txt:255) needs an explicit implementation inside predictive evaluation, as well as between A/B/C.

   **Fix:** Require fold manifests matched to the generalization claim. For unseen-donor prediction, keep every conservatively linked donor’s models, cultures and repeated observations in one fold, including nested tuning folds. Specify additional lineage/target/pathway blocking where claimed. Add a fixture with distinct model IDs sharing one donor. Preserve legitimate within-model environmental contrasts separately.

2. **HIGH — Duplicate rejection has no declared arm or episode scope.**

   **Evidence:** [PLAN:44](/Users/bmarti44/github/bufferright/research/PLAN.md:44) says “**same config new context = duplicate configuration**,” rejected unless replication is authorized. [PLAN:53](/Users/bmarti44/github/bufferright/research/PLAN.md:53) rejects duplicate `config_id` values and feeds rejection information back next round. Neither defines the lookup’s scope.

   A runner consulting the global ledger could reject a configuration in arm B because arm A already executed it. Reversing arm execution order could reverse which arm receives the rejection. Likewise, an unrevealed historical node could affect legal choices through duplicate detection without its outcome ever appearing in a prompt.

   This creates interference between arms and an information channel through hidden artifact existence. Filtering rendered records does not prevent it. It also conflicts with fresh evaluation across panels: the text distinguishes `evaluation_id` by data and split, yet its blanket configuration rule can reject the same scientific configuration on genuinely new evidence.

   **Fix:** Define duplicate eligibility against the arm’s episode-admissible history, with explicit study/panel/split scope. Permit the required symmetric evaluations across arms and independent panels under a frozen rule. A global artifact store may retain bytes, but hidden global membership must not change an arm’s observations or legal actions. Test that adding hidden or other-arm configurations—and reversing execution order—does not change either arm’s behavior.

3. **MEDIUM — The replay winner rule cannot resolve tied challengers above the incumbent.**

   **Evidence:** [PLAN:121](/Users/bmarti44/github/bufferright/research/PLAN.md:121) fresh-tests the “**top-1 challenger by J (ties per §0.4.6)**.” The final tie-break at [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) is “**incumbent retained**.”

   Suppose two challengers have identical J, attainment and restricted-mean cost, and both outperform the incumbent. “Incumbent retained” neither orders those challengers nor identifies the promised top-one fresh-test candidate. Applying it literally would retain an inferior incumbent; choosing a challenger introduces discretion.

   **Fix:** Add a total ordering frozen before replay, such as the pre-listed challenger order followed by immutable candidate ID. Apply incumbent retention only when the incumbent belongs to the tied best set. This is separate from the now-resolved censoring calculation and fallback-selection defects.

4. **MEDIUM — Deterministic replay-state reconstruction is asserted without reconciling LLM-produced state.**

   **Evidence:** [PLAN:55](/Users/bmarti44/github/bufferright/research/PLAN.md:55) requires “**All recomputation is deterministic**” and “**replayable bit-for-bit given the same revealed outcomes**.” Yet [PLAN:85](/Users/bmarti44/github/bufferright/research/PLAN.md:85) inserts a “**sol-xhigh direction summary + ranked proposal**,” and [PLAN:47](/Users/bmarti44/github/bufferright/research/PLAN.md:47) requires summaries and priorities to be reconstructed from admissible history.

   Freezing prompts, model ID and effort does not specify how repeated state reconstruction obtains identical summary and proposal bytes. Reinvoking the model can change those inputs even when admissible history is unchanged. That affects policy decisions, exact-context support and the interpretation of hidden-outcome invariance failures. Deterministic verification of catalog classifications does not settle free-text summaries or rankings.

   **Fix:** Define the reconstruction mechanism before comparison: deterministic transformations, or immutable memoized model outputs keyed by canonical admissible-state content and protocol version. Specify cache-miss behavior, costs and support treatment. Verify repeated reconstruction produces identical rendered inputs without another stochastic model call.

The remaining findings affect C4, C8 and C9: the plan still permits ambiguous isolation and scoring behavior in the experiments intended to demonstrate policy improvement. No critical finding identified; **two high and three medium findings remain open**.

SCORE: 86
