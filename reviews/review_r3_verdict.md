
codex
The revised text supports 29 resolved findings and six partial fixes. Most scientific safeguards are now explicit. The remaining gaps concern replay support and inputs, selection rules, and stopping limits before Lock 1. I also found a separate risk: allowing individual experiments to be excluded after a protocol breach could bias a comparison.

codex
**Not ready for a ≥90 pass.** I read all five files in full. Of the 35 round-2 findings, **29 are RESOLVED and six PARTIALLY resolved**. The dispositions’ claim that all 35 are fixed is unsupported.

Reviewed snapshots: PLAN `2cc44aefd5d6`, GOAL `4155aaae5e45`, handoff `2814f8f3edcd`. No files edited. This assesses the written execution contract; it does not certify implementation.

Below, P means [PLAN.md](/Users/bmarti44/github/bufferright/research/PLAN.md), G means [GOAL.md](/Users/bmarti44/github/bufferright/research/GOAL.md). Severities in this table are the original round-2 severities. A concrete requirement to supply and freeze a method before execution counts as a planning fix; merely naming a missing method would not.

| R2 | Severity | Verdict | Verified evidence and assessment |
|---|---|---|---|
| 1 | Critical | **RESOLVED** | P Phase 1c: “development-only reconstruction or genuinely independent validation — disclosure never repairs it.” Explicitly includes normalization, target selection and model selection. §10 agrees. |
| 2 | High | **RESOLVED** | P Phase 1a requires provisional partitions “Before importing any outcome-bearing file,” limits permitted contact, quarantines Sanger values and requires an exposure log. |
| 3 | High | **PARTIALLY** | P §0.4.2 correctly requires views “recomputed from admissible history only.” But §0.1 separately mandates an index containing “every attempt… outcome class, quality, cost — no omission,” without explicitly restricting that index to admissible history. These interfaces conflict. |
| 4 | High | **RESOLVED** | P §0.4.1 defines an “ordered parent array,” acyclicity, birth-world membership, immutable contributions, version matching, revealed-parent requirements and union ancestry charging. |
| 5 | High | **RESOLVED** | P §0.3 retains a canonical manifest of “every input artifact”; §0.4.6 permits replay “iff” that manifest matches and makes any differing input unsupported. This supplies the required exact-context alternative. The “parent-local” description remains misleading; see below. |
| 6 | High | **RESOLVED** | P §0.4.5: “Legal actions are recomputed at each step from the revealed prefix”; historical action sequences are explicitly excluded from counterfactual state. |
| 7 | High | **PARTIALLY** | P §0.4.6 adds thresholds and termination rules, but unsupported episodes have their “quality… excluded from means” while policies supposedly remain “paired on identical episode sets.” Policy-specific exclusions violate that pairing. |
| 8 | High | **PARTIALLY** | P §0.4.6 supplies \(J_e\), budget-based ρ, weights and invalid-result treatment. However, its tie-break uses “lower mean cost-to-τ,” while §0.4.3 defines nonattainment as censored. No censored-mean or tie procedure is specified. |
| 9 | High | **RESOLVED** | P §0.1 freezes the “entire generation protocol,” including ranking, extraction, repair and unstick allowances; fixed arms use their own admissible histories. Its exclusion remedy introduces a separate problem below. |
| 10 | Medium | **RESOLVED** | P §0.4.2 requires four independent fields and a “total transition table frozen at Lock 1,” including missing evidence, precedence, recovery and deterministic verification. |
| 11 | Medium | **RESOLVED** | P §0.4.4 adds `refinement`: “exactly 1 parent; mutate/extend a frontier or winner artifact.” |
| 12 | High | **RESOLVED** | P §0.4.1 separates attempt, context, configuration and evaluation identities; repeats require a “prespecified replication/repair with reason.” |
| 13 | Medium | **RESOLVED** | P §0.4.3 limits frontiers to comparable domains and states that a nondominated saturated trajectory remains “frontier-listed but allocation-paused.” Saturation is explicitly not scientific exhaustion. |
| 14 | High | **RESOLVED** | P §0.5.2 permits exhaustive rejection only with a “mathematically necessary condition”; otherwise screen-negative members remain untested. Verdicts are scoped to tested finalists. |
| 15 | Medium | **PARTIALLY** | P §0.5 separates S/P lifecycles, reserves battery resources and retains `PENDING` work. But Phase 4 still fresh-tests a “selected challenger” without an explicit selection rule when replay is inadmissible. |
| 16 | Medium | **RESOLVED** | P §0.5.1.8 requires separate cumulative counters for configurations, attempts, replications, hypothesis inspections, policy candidates, replay episodes and batteries. |
| 17 | High | **RESOLVED** | P §0.5.3: different evaluator versions are “never pooled”; changes require compatibility probes, affected-result invalidation and, when substantive, a new study and evidence. |
| 18 | High | **RESOLVED** | P Phase 4.3 includes fresh comparisons against the incumbent and states: “Promotion requires beating the incumbent” under a locked improvement/noninferiority rule. |
| 19 | High | **RESOLVED** | P Phase 5 charges generation, replay, extraction, reviews, unstick, failures and promotion trials; requires frozen shared-cost allocation, stated deployment count and line-by-line ledger reconciliation. |
| 20 | High | **RESOLVED** | P Phase 5 requires a named resource and units, aggregation, alternative-endpoint justification, practical margin, uncertainty criterion and matching tolerances. Unknown material host costs retain an unresolved gate. |
| 21 | High | **RESOLVED** | P Lock 1 and Phase 5 require independent-block counts, savings estimand, paired estimator, censoring-compatible interval and advance precision feasibility. Transfer from engineering cohorts is explicitly bounded. |
| 22 | High | **RESOLVED** | P Phase 5: “B panels are consumed”; subsequent adaptation requires “new independent B evidence” for another confirmatory claim. |
| 23 | High | **RESOLVED** | P Phase 6 attaches component-level status to claims and atlas decisions, explicitly preserving adaptively reused environmental evidence as “exploratory or justified selection-adjusted.” |
| 24 | High | **RESOLVED** | P Phase 2.1 requires joint resampling of each model’s “entire paired vector,” downstream refitting and reporting conclusions that flip. Independent per-gene error bars are explicitly nonconforming. Donor nesting remains a separate gap below. |
| 25 | High | **RESOLVED** | P Lock 1 requires meaningful dependency strength “for every positive vulnerability claim,” separately from environmental change; Phase 6 repeats the gate. G’s abbreviated C10 does not override this. |
| 26 | Medium | **RESOLVED** | P Phase 2.3 distinguishes verified orientation/preprocessing errors from a correctly measured opposite-direction result, which remains valid evidence. |
| 27 | High | **PARTIALLY** | P §0.6 adds campaign allocations and a no-progress determination. But allocations, retry limits and the terminal-review reserve start at Lock 1; G0/G1 and pre-lock review loops remain outside a bounded stopping mechanism. |
| 28 | Medium | **RESOLVED** | P §0.6 reserves terminal-review resources and permits mechanical `BLOCKED`/`BUDGET_EXHAUSTED` reporting if the call cannot run. Positive completion still requires the mandated review. |
| 29 | High | **RESOLVED** | P §0.3 retains rendered prompts, actual input artifacts, action/observation sequences, selecting policy state/version and environment manifests. Hashes are explicitly “indexes, not substitutes.” |
| 30 | Medium | **PARTIALLY** | P §0.1 and G model routing now share a retrieval contract. However, “index always complete” and “overflow ⇒ generation splits by direction” do not define which complete index each split receives, or how cross-direction dependencies remain accessible. |
| 31 | Medium | **RESOLVED** | P §0.2 explicitly requires conservative maximum reservations, concurrent/retry accounting, persistence before dispatch, interrupted-reservation reconciliation and rejection of unbounded providers, with acceptance tests. |
| 32 | Medium | **RESOLVED** | P Phase 3 labels G3 an interim report with comparison “unperformed” and says it does not establish C13. Phase 4/§9 place the substantive report after a fresh comparison or its documented blocker. |
| 33 | Medium | **RESOLVED** | P Phase 7 requires a dated claim-specific novelty refresh at G7 and terminal determination, without revising consumed confirmatory tests. |
| 34 | Low | **RESOLVED** | The missing §7.3 references are removed. Cost measurability and endpoint requirements now point to Phase 5. |
| 35 | Low | **RESOLVED** | G non-negotiables and P opening distinguish local scientific computation from reasoning through the authorized hosted interface. |

The remaining round-2 defects need these concrete corrections:

1. **High — R2 #3: the exhaustive index can bypass replay filtering.**  
   **Location:** [P §0.1](/Users/bmarti44/github/bufferright/research/PLAN.md:23), §0.4.2.  
   The prefix-only rule and “every attempt… quality… no omission” rule admit incompatible implementations. Filtering catalogs while passing the global outcome-bearing index still exposes future rewards and realized costs. The hidden-outcome test would catch this only if it actually covers every input channel.  
   **Fix:** define “exhaustive” as exhaustive over the episode’s explicitly admissible history. Apply the same filter to indices, retrieved records, prompts, summaries, priorities and unstick packets. Test the complete rendered input and resulting decisions.

2. **High — R2 #7: policy-dependent deletion defeats common-support comparisons.**  
   **Location:** [P §0.4.6](/Users/bmarti44/github/bufferright/research/PLAN.md:59).  
   A policy can complete eight easy episodes, go unsupported on harder episodes, and have the hard episodes removed from its quality mean. Another policy can finish every episode and receive a lower mean. Both can satisfy the stated thresholds. “Supported decisions / all decision points” also has an endogenous denominator because unsupported actions terminate trajectories.  
   **Fix:** define support separately at each operating budget, a fixed episode-level denominator, and one common eligible episode set used by every compared policy. If that common set fails a frozen adequacy threshold, declare the screen inadmissible. Never rank policies using different surviving episode sets.

3. **Medium — R2 #8: the objective’s tie-break is undefined under censoring.**  
   **Location:** [P §§0.4.3–0.4.6](/Users/bmarti44/github/bufferright/research/PLAN.md:48).  
   Ordinary mean cost-to-threshold cannot be computed from unresolved right-censored costs. The plan forbids invented costs but provides no executable alternative. Thus apparently tied challengers can be selected by an improvised rule.  
   **Fix:** freeze an identifiable censored estimand and estimator, including all-censored cases, or remove this tie-break and retain the incumbent on equal primary scores.

4. **Medium — R2 #15: replay failure leaves challenger selection discretionary.**  
   **Location:** [P Phase 4.2–4.3](/Users/bmarti44/github/bufferright/research/PLAN.md:120).  
   “Skip screening conclusion, go fresh” does not determine which of the ≥3 challengers receives the decisive fresh battery. The proposer can choose after inspecting whatever partial evidence exists.  
   **Fix:** require a pre-replay selection/fallback algorithm in the locked policy-generation SPEC. Define finalist counts and disposition of every unselected challenger. If all challengers receive fresh tests, freeze that allocation and promotion procedure instead.

5. **High — R2 #27: the campaign is bounded only after reaching Lock 1.**  
   **Location:** [P §§0.2, 0.6](/Users/bmarti44/github/bufferright/research/PLAN.md:27), Phases 0–2; G autonomy.  
   An unresolved crosswalk, unavailable pairing or repeated review failure can consume unlimited pre-lock consultations. The K-generation rule does not reliably apply before generations exist. A limit created after passing the difficult gates cannot bound attempts to pass those gates.  
   **Fix:** establish bootstrap/audit/review allocations, repeat-failure limits and a terminal-review reserve at Phase 0. Define stopping on repeated pre-lock blockers independently of frontier movement.

6. **Medium — R2 #30: context overflow handling is not executable.**  
   **Location:** [P §0.1](/Users/bmarti44/github/bufferright/research/PLAN.md:23), G model routing.  
   Splitting generation by direction does not make an oversized complete global index smaller. Splitting the index instead can hide failures or parents needed for recombination. No deterministic partition, cross-direction lookup or retrieval budget is specified.  
   **Fix:** define a bounded, deterministic index/retrieval protocol with complete addressability, explicit partitioning, cross-direction access and an auditable overflow outcome. Require it to obey the episode filter above.

Additional issues introduced by v2 or still present:

7. **High — post-breach exclusions permit selective attrition.**  
   **Location:** [P §0.1, generator-protocol freeze](/Users/bmarti44/github/bufferright/research/PLAN.md:22).  
   **Evidence:** discretionary interventions cause a new comparison epoch “or the affected experiments are excluded.”  
   An intervention often follows an observed failure. Dropping affected experiments afterward can selectively remove poor outcomes from one arm. Recording the intervention and charging its costs do not repair biased outcome inclusion. This threatens C8/C9 even with a frozen generator.  
   **Fix:** predeclare outcome-independent exclusion criteria and retain all assigned attempts, failures and costs in the primary comparison. A breach that changes admissible information or treatment should invalidate the affected comparison unless a frozen analysis rule already covers it. Restarting requires appropriately unused evaluation evidence.

8. **High — mandatory model-level resampling can ignore donor dependence.**  
   **Location:** [P Phase 2.1](/Users/bmarti44/github/bufferright/research/PLAN.md:107), Phase 1d.  
   **Evidence:** uncertainty uses “model-level (cluster) resampling”; provenance separately records models and donors.  
   Correct counts and cross-partition donor checks do not ensure correct *within-partition* uncertainty. If multiple models share a donor, resampling models independently treats correlated biological material as independent. Carrying whole gene vectors preserves target covariance while still missing donor covariance. The handoff §8 requires uncertainty at the appropriate donor/biological-model level.  
   **Fix:** select the independent resampling unit from the crosswalk. Resample donors with all nested models, cultures and contrasts, or justify an equivalent dependence model. State the rule for uncertain donor identity and test nested-donor cases.

9. **Medium — causal interpretation lacks the handoff’s explicit restriction.**  
   **Location:** [G ambition 3](/Users/bmarti44/github/bufferright/research/GOAL.md:15), [P Phase 6](/Users/bmarti44/github/bufferright/research/PLAN.md:134).  
   **Evidence:** G distinguishes intervention from association; P requires component evidence labels. Neither execution section explicitly requires identifying assumptions and suitable evidence before treating predictive expression features as causal mediators, as handoff §6 does.  
   A predictive environmental feature, external transfer improvement and an ablation can support association without establishing a mechanism for transfer failure. Calling the result “explanatory” does not supply identification.  
   **Fix:** add a claim-level causal-interpretation gate. Require the estimand, assumptions and identifying evidence for causal or mediation language; otherwise constrain conclusions to intervention effects actually measured and cross-cohort predictive associations.

10. **Medium — “parent-local by construction” contradicts the listed inputs.**  
    **Location:** [P §0.4.6](/Users/bmarti44/github/bufferright/research/PLAN.md:58), §0.1.  
    **Evidence:** refinement is called “parent-local,” but its manifest includes an “episode-view snapshot ID + budget token”; the general proposer also receives history and retrieved records.  
    These inputs change with ordering and budget. Exact matching can preserve replay validity, but the stated construction does not provide parent-locality and may make reordered refinement almost entirely unsupported. This matters for feasibility, not just terminology.  
    **Fix:** either implement a genuinely parent-local refinement interface or describe it as history-dependent exact-context replay. Measure attainable support on actual reordered traces before relying on replay screening; include context overflow and budget changes in that test.

11. **Low — the download limit omits the disk-dependent bound.**  
    **Location:** [P §0.2](/Users/bmarti44/github/bufferright/research/PLAN.md:28), G non-negotiables.  
    **Evidence:** downloads are capped at “20 GiB”; handoff §4 specifies the smaller of 20 GiB and one quarter of available disk.  
    The current host has sufficient space, but a resumed campaign can encounter a different disk envelope.  
    **Fix:** enforce and persist `min(20 GiB, available_disk / 4)` when allocating downloads.

12. **Low — review status overstates independently verified closure.**  
    **Location:** [P opening](/Users/bmarti44/github/bufferright/research/PLAN.md:6), round-2 dispositions.  
    **Evidence:** “35 issues, all verified+fixed” and “ALL 35 CONFIRMED.” Confirmation of the original defects is different from verification that their replacements work together. Six fixes remain partial.  
    **Fix:** distinguish author-claimed fixes from independently verified closure and retain unresolved residuals in the issue ledger.

The rewrite materially improves specification fidelity, especially leakage handling, component-level scientific evidence, joint uncertainty, resource accounting and terminal honesty. Its remaining defects affect faithful replay and defensible policy comparisons—the evidence needed for C8/C9—not merely presentation.

SCORE: 76
tokens used
54,828
**Not ready for a ≥90 pass.** I read all five files in full. Of the 35 round-2 findings, **29 are RESOLVED and six PARTIALLY resolved**. The dispositions’ claim that all 35 are fixed is unsupported.

Reviewed snapshots: PLAN `2cc44aefd5d6`, GOAL `4155aaae5e45`, handoff `2814f8f3edcd`. No files edited. This assesses the written execution contract; it does not certify implementation.

Below, P means [PLAN.md](/Users/bmarti44/github/bufferright/research/PLAN.md), G means [GOAL.md](/Users/bmarti44/github/bufferright/research/GOAL.md). Severities in this table are the original round-2 severities. A concrete requirement to supply and freeze a method before execution counts as a planning fix; merely naming a missing method would not.

| R2 | Severity | Verdict | Verified evidence and assessment |
|---|---|---|---|
| 1 | Critical | **RESOLVED** | P Phase 1c: “development-only reconstruction or genuinely independent validation — disclosure never repairs it.” Explicitly includes normalization, target selection and model selection. §10 agrees. |
| 2 | High | **RESOLVED** | P Phase 1a requires provisional partitions “Before importing any outcome-bearing file,” limits permitted contact, quarantines Sanger values and requires an exposure log. |
| 3 | High | **PARTIALLY** | P §0.4.2 correctly requires views “recomputed from admissible history only.” But §0.1 separately mandates an index containing “every attempt… outcome class, quality, cost — no omission,” without explicitly restricting that index to admissible history. These interfaces conflict. |
| 4 | High | **RESOLVED** | P §0.4.1 defines an “ordered parent array,” acyclicity, birth-world membership, immutable contributions, version matching, revealed-parent requirements and union ancestry charging. |
| 5 | High | **RESOLVED** | P §0.3 retains a canonical manifest of “every input artifact”; §0.4.6 permits replay “iff” that manifest matches and makes any differing input unsupported. This supplies the required exact-context alternative. The “parent-local” description remains misleading; see below. |
| 6 | High | **RESOLVED** | P §0.4.5: “Legal actions are recomputed at each step from the revealed prefix”; historical action sequences are explicitly excluded from counterfactual state. |
| 7 | High | **PARTIALLY** | P §0.4.6 adds thresholds and termination rules, but unsupported episodes have their “quality… excluded from means” while policies supposedly remain “paired on identical episode sets.” Policy-specific exclusions violate that pairing. |
| 8 | High | **PARTIALLY** | P §0.4.6 supplies \(J_e\), budget-based ρ, weights and invalid-result treatment. However, its tie-break uses “lower mean cost-to-τ,” while §0.4.3 defines nonattainment as censored. No censored-mean or tie procedure is specified. |
| 9 | High | **RESOLVED** | P §0.1 freezes the “entire generation protocol,” including ranking, extraction, repair and unstick allowances; fixed arms use their own admissible histories. Its exclusion remedy introduces a separate problem below. |
| 10 | Medium | **RESOLVED** | P §0.4.2 requires four independent fields and a “total transition table frozen at Lock 1,” including missing evidence, precedence, recovery and deterministic verification. |
| 11 | Medium | **RESOLVED** | P §0.4.4 adds `refinement`: “exactly 1 parent; mutate/extend a frontier or winner artifact.” |
| 12 | High | **RESOLVED** | P §0.4.1 separates attempt, context, configuration and evaluation identities; repeats require a “prespecified replication/repair with reason.” |
| 13 | Medium | **RESOLVED** | P §0.4.3 limits frontiers to comparable domains and states that a nondominated saturated trajectory remains “frontier-listed but allocation-paused.” Saturation is explicitly not scientific exhaustion. |
| 14 | High | **RESOLVED** | P §0.5.2 permits exhaustive rejection only with a “mathematically necessary condition”; otherwise screen-negative members remain untested. Verdicts are scoped to tested finalists. |
| 15 | Medium | **PARTIALLY** | P §0.5 separates S/P lifecycles, reserves battery resources and retains `PENDING` work. But Phase 4 still fresh-tests a “selected challenger” without an explicit selection rule when replay is inadmissible. |
| 16 | Medium | **RESOLVED** | P §0.5.1.8 requires separate cumulative counters for configurations, attempts, replications, hypothesis inspections, policy candidates, replay episodes and batteries. |
| 17 | High | **RESOLVED** | P §0.5.3: different evaluator versions are “never pooled”; changes require compatibility probes, affected-result invalidation and, when substantive, a new study and evidence. |
| 18 | High | **RESOLVED** | P Phase 4.3 includes fresh comparisons against the incumbent and states: “Promotion requires beating the incumbent” under a locked improvement/noninferiority rule. |
| 19 | High | **RESOLVED** | P Phase 5 charges generation, replay, extraction, reviews, unstick, failures and promotion trials; requires frozen shared-cost allocation, stated deployment count and line-by-line ledger reconciliation. |
| 20 | High | **RESOLVED** | P Phase 5 requires a named resource and units, aggregation, alternative-endpoint justification, practical margin, uncertainty criterion and matching tolerances. Unknown material host costs retain an unresolved gate. |
| 21 | High | **RESOLVED** | P Lock 1 and Phase 5 require independent-block counts, savings estimand, paired estimator, censoring-compatible interval and advance precision feasibility. Transfer from engineering cohorts is explicitly bounded. |
| 22 | High | **RESOLVED** | P Phase 5: “B panels are consumed”; subsequent adaptation requires “new independent B evidence” for another confirmatory claim. |
| 23 | High | **RESOLVED** | P Phase 6 attaches component-level status to claims and atlas decisions, explicitly preserving adaptively reused environmental evidence as “exploratory or justified selection-adjusted.” |
| 24 | High | **RESOLVED** | P Phase 2.1 requires joint resampling of each model’s “entire paired vector,” downstream refitting and reporting conclusions that flip. Independent per-gene error bars are explicitly nonconforming. Donor nesting remains a separate gap below. |
| 25 | High | **RESOLVED** | P Lock 1 requires meaningful dependency strength “for every positive vulnerability claim,” separately from environmental change; Phase 6 repeats the gate. G’s abbreviated C10 does not override this. |
| 26 | Medium | **RESOLVED** | P Phase 2.3 distinguishes verified orientation/preprocessing errors from a correctly measured opposite-direction result, which remains valid evidence. |
| 27 | High | **PARTIALLY** | P §0.6 adds campaign allocations and a no-progress determination. But allocations, retry limits and the terminal-review reserve start at Lock 1; G0/G1 and pre-lock review loops remain outside a bounded stopping mechanism. |
| 28 | Medium | **RESOLVED** | P §0.6 reserves terminal-review resources and permits mechanical `BLOCKED`/`BUDGET_EXHAUSTED` reporting if the call cannot run. Positive completion still requires the mandated review. |
| 29 | High | **RESOLVED** | P §0.3 retains rendered prompts, actual input artifacts, action/observation sequences, selecting policy state/version and environment manifests. Hashes are explicitly “indexes, not substitutes.” |
| 30 | Medium | **PARTIALLY** | P §0.1 and G model routing now share a retrieval contract. However, “index always complete” and “overflow ⇒ generation splits by direction” do not define which complete index each split receives, or how cross-direction dependencies remain accessible. |
| 31 | Medium | **RESOLVED** | P §0.2 explicitly requires conservative maximum reservations, concurrent/retry accounting, persistence before dispatch, interrupted-reservation reconciliation and rejection of unbounded providers, with acceptance tests. |
| 32 | Medium | **RESOLVED** | P Phase 3 labels G3 an interim report with comparison “unperformed” and says it does not establish C13. Phase 4/§9 place the substantive report after a fresh comparison or its documented blocker. |
| 33 | Medium | **RESOLVED** | P Phase 7 requires a dated claim-specific novelty refresh at G7 and terminal determination, without revising consumed confirmatory tests. |
| 34 | Low | **RESOLVED** | The missing §7.3 references are removed. Cost measurability and endpoint requirements now point to Phase 5. |
| 35 | Low | **RESOLVED** | G non-negotiables and P opening distinguish local scientific computation from reasoning through the authorized hosted interface. |

The remaining round-2 defects need these concrete corrections:

1. **High — R2 #3: the exhaustive index can bypass replay filtering.**  
   **Location:** [P §0.1](/Users/bmarti44/github/bufferright/research/PLAN.md:23), §0.4.2.  
   The prefix-only rule and “every attempt… quality… no omission” rule admit incompatible implementations. Filtering catalogs while passing the global outcome-bearing index still exposes future rewards and realized costs. The hidden-outcome test would catch this only if it actually covers every input channel.  
   **Fix:** define “exhaustive” as exhaustive over the episode’s explicitly admissible history. Apply the same filter to indices, retrieved records, prompts, summaries, priorities and unstick packets. Test the complete rendered input and resulting decisions.

2. **High — R2 #7: policy-dependent deletion defeats common-support comparisons.**  
   **Location:** [P §0.4.6](/Users/bmarti44/github/bufferright/research/PLAN.md:59).  
   A policy can complete eight easy episodes, go unsupported on harder episodes, and have the hard episodes removed from its quality mean. Another policy can finish every episode and receive a lower mean. Both can satisfy the stated thresholds. “Supported decisions / all decision points” also has an endogenous denominator because unsupported actions terminate trajectories.  
   **Fix:** define support separately at each operating budget, a fixed episode-level denominator, and one common eligible episode set used by every compared policy. If that common set fails a frozen adequacy threshold, declare the screen inadmissible. Never rank policies using different surviving episode sets.

3. **Medium — R2 #8: the objective’s tie-break is undefined under censoring.**  
   **Location:** [P §§0.4.3–0.4.6](/Users/bmarti44/github/bufferright/research/PLAN.md:48).  
   Ordinary mean cost-to-threshold cannot be computed from unresolved right-censored costs. The plan forbids invented costs but provides no executable alternative. Thus apparently tied challengers can be selected by an improvised rule.  
   **Fix:** freeze an identifiable censored estimand and estimator, including all-censored cases, or remove this tie-break and retain the incumbent on equal primary scores.

4. **Medium — R2 #15: replay failure leaves challenger selection discretionary.**  
   **Location:** [P Phase 4.2–4.3](/Users/bmarti44/github/bufferright/research/PLAN.md:120).  
   “Skip screening conclusion, go fresh” does not determine which of the ≥3 challengers receives the decisive fresh battery. The proposer can choose after inspecting whatever partial evidence exists.  
   **Fix:** require a pre-replay selection/fallback algorithm in the locked policy-generation SPEC. Define finalist counts and disposition of every unselected challenger. If all challengers receive fresh tests, freeze that allocation and promotion procedure instead.

5. **High — R2 #27: the campaign is bounded only after reaching Lock 1.**  
   **Location:** [P §§0.2, 0.6](/Users/bmarti44/github/bufferright/research/PLAN.md:27), Phases 0–2; G autonomy.  
   An unresolved crosswalk, unavailable pairing or repeated review failure can consume unlimited pre-lock consultations. The K-generation rule does not reliably apply before generations exist. A limit created after passing the difficult gates cannot bound attempts to pass those gates.  
   **Fix:** establish bootstrap/audit/review allocations, repeat-failure limits and a terminal-review reserve at Phase 0. Define stopping on repeated pre-lock blockers independently of frontier movement.

6. **Medium — R2 #30: context overflow handling is not executable.**  
   **Location:** [P §0.1](/Users/bmarti44/github/bufferright/research/PLAN.md:23), G model routing.  
   Splitting generation by direction does not make an oversized complete global index smaller. Splitting the index instead can hide failures or parents needed for recombination. No deterministic partition, cross-direction lookup or retrieval budget is specified.  
   **Fix:** define a bounded, deterministic index/retrieval protocol with complete addressability, explicit partitioning, cross-direction access and an auditable overflow outcome. Require it to obey the episode filter above.

Additional issues introduced by v2 or still present:

7. **High — post-breach exclusions permit selective attrition.**  
   **Location:** [P §0.1, generator-protocol freeze](/Users/bmarti44/github/bufferright/research/PLAN.md:22).  
   **Evidence:** discretionary interventions cause a new comparison epoch “or the affected experiments are excluded.”  
   An intervention often follows an observed failure. Dropping affected experiments afterward can selectively remove poor outcomes from one arm. Recording the intervention and charging its costs do not repair biased outcome inclusion. This threatens C8/C9 even with a frozen generator.  
   **Fix:** predeclare outcome-independent exclusion criteria and retain all assigned attempts, failures and costs in the primary comparison. A breach that changes admissible information or treatment should invalidate the affected comparison unless a frozen analysis rule already covers it. Restarting requires appropriately unused evaluation evidence.

8. **High — mandatory model-level resampling can ignore donor dependence.**  
   **Location:** [P Phase 2.1](/Users/bmarti44/github/bufferright/research/PLAN.md:107), Phase 1d.  
   **Evidence:** uncertainty uses “model-level (cluster) resampling”; provenance separately records models and donors.  
   Correct counts and cross-partition donor checks do not ensure correct *within-partition* uncertainty. If multiple models share a donor, resampling models independently treats correlated biological material as independent. Carrying whole gene vectors preserves target covariance while still missing donor covariance. The handoff §8 requires uncertainty at the appropriate donor/biological-model level.  
   **Fix:** select the independent resampling unit from the crosswalk. Resample donors with all nested models, cultures and contrasts, or justify an equivalent dependence model. State the rule for uncertain donor identity and test nested-donor cases.

9. **Medium — causal interpretation lacks the handoff’s explicit restriction.**  
   **Location:** [G ambition 3](/Users/bmarti44/github/bufferright/research/GOAL.md:15), [P Phase 6](/Users/bmarti44/github/bufferright/research/PLAN.md:134).  
   **Evidence:** G distinguishes intervention from association; P requires component evidence labels. Neither execution section explicitly requires identifying assumptions and suitable evidence before treating predictive expression features as causal mediators, as handoff §6 does.  
   A predictive environmental feature, external transfer improvement and an ablation can support association without establishing a mechanism for transfer failure. Calling the result “explanatory” does not supply identification.  
   **Fix:** add a claim-level causal-interpretation gate. Require the estimand, assumptions and identifying evidence for causal or mediation language; otherwise constrain conclusions to intervention effects actually measured and cross-cohort predictive associations.

10. **Medium — “parent-local by construction” contradicts the listed inputs.**  
    **Location:** [P §0.4.6](/Users/bmarti44/github/bufferright/research/PLAN.md:58), §0.1.  
    **Evidence:** refinement is called “parent-local,” but its manifest includes an “episode-view snapshot ID + budget token”; the general proposer also receives history and retrieved records.  
    These inputs change with ordering and budget. Exact matching can preserve replay validity, but the stated construction does not provide parent-locality and may make reordered refinement almost entirely unsupported. This matters for feasibility, not just terminology.  
    **Fix:** either implement a genuinely parent-local refinement interface or describe it as history-dependent exact-context replay. Measure attainable support on actual reordered traces before relying on replay screening; include context overflow and budget changes in that test.

11. **Low — the download limit omits the disk-dependent bound.**  
    **Location:** [P §0.2](/Users/bmarti44/github/bufferright/research/PLAN.md:28), G non-negotiables.  
    **Evidence:** downloads are capped at “20 GiB”; handoff §4 specifies the smaller of 20 GiB and one quarter of available disk.  
    The current host has sufficient space, but a resumed campaign can encounter a different disk envelope.  
    **Fix:** enforce and persist `min(20 GiB, available_disk / 4)` when allocating downloads.

12. **Low — review status overstates independently verified closure.**  
    **Location:** [P opening](/Users/bmarti44/github/bufferright/research/PLAN.md:6), round-2 dispositions.  
    **Evidence:** “35 issues, all verified+fixed” and “ALL 35 CONFIRMED.” Confirmation of the original defects is different from verification that their replacements work together. Six fixes remain partial.  
    **Fix:** distinguish author-claimed fixes from independently verified closure and retain unresolved residuals in the issue ledger.

The rewrite materially improves specification fidelity, especially leakage handling, component-level scientific evidence, joint uncertainty, resource accounting and terminal honesty. Its remaining defects affect faithful replay and defensible policy comparisons—the evidence needed for C8/C9—not merely presentation.

SCORE: 76
