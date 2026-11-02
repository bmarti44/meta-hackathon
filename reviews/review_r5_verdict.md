
codex
**All five round-4 findings are resolved at the planning level. No high or critical issue remains open.** This is approval of the written execution contract, not evidence that its tests or scientific gates have passed.

I read all four requested documents in full. No edits made. Reviewed PLAN SHA-256: `5e4e6051bd2e…`.

| Round-4 item | Verdict | Quoted evidence and assessment |
|---|---|---|
| **R2#30 — context overflow** | **RESOLVED** | [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) requires a “**bounded directory header**,” subdivisions with “**fixed row/token caps**,” and reserved space for instructions and retrieved records. It explicitly requires directory-overflow and single-direction-overflow fixtures “**both rendering legally**.” These are concrete acceptance requirements addressing both previous failure cases. See the implementation caveat below. |
| **Donor-grouped predictive folds — high** | **RESOLVED** | [PLAN:109](/Users/bmarti44/github/bufferright/research/PLAN.md:109) keeps every conservatively linked donor’s observations in one fold, “**including nested tuning folds**.” The shared-donor/distinct-model fixture must fail the build if observations straddle folds. This governs predictive evaluation separately from donor resampling and preserves legitimate within-model contrasts. |
| **Arm-scoped dedup — high** | **RESOLVED** | [PLAN:44](/Users/bmarti44/github/bufferright/research/PLAN.md:44) limits duplicate eligibility to “**the acting arm’s episode-admissible history**,” permits genuinely new evaluations, and prohibits global membership from changing observations, rejections or legal actions. Hidden-configuration and reversed-execution-order tests directly target the former interference channel. |
| **Total ordering of tied challengers — medium** | **RESOLVED** | [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) adds “**earlier position in the SPEC’s pre-listed candidate order**,” followed by “**lexicographically smaller immutable candidate ID**.” Thus two challengers tied above the incumbent remain deterministically ordered. |
| **Deterministic reconstruction of LLM state — medium** | **RESOLVED** | [PLAN:55](/Users/bmarti44/github/bufferright/research/PLAN.md:55) defines “**immutable memoized output**” keyed by admissible state and protocol version. Reconstruction “**reads the memo — never re-invokes the model**”; a replay cache miss becomes unsupported. The required reconstruction test checks identical rendered bytes and zero additional model calls. |

The earlier-world charging clarification also closes the substantive loophole it targets. [PLAN:130](/Users/bmarti44/github/bufferright/research/PLAN.md:130) charges “**the production cost of every history it reads**,” specifies symmetric access rules, and prohibits consuming another arm’s outcomes. Together with ancestry accounting and the frozen allocation rule, this prevents historical information from being treated as free merely because its production preceded deployment.

I found **no additional high or critical defect** after checking specification fidelity, independence, confirmatory selection, replay support, comparison fairness and terminal criteria. In particular:

- [PLAN:136](/Users/bmarti44/github/bufferright/research/PLAN.md:136) prevents external transfer validation from laundering an adaptively selected environmental effect into independent confirmation.
- [PLAN:128](/Users/bmarti44/github/bufferright/research/PLAN.md:128) makes the comparison estimand, censoring-compatible interval and precision-feasibility result mandatory at Lock 1. Their numerical specification remains legitimate pre-lock work.
- [PLAN:131](/Users/bmarti44/github/bufferright/research/PLAN.md:131) retains the unresolved cost gate when material host-model costs cannot be measured. Execution can produce an honest non-complete result; completion is not guaranteed by the plan.

Three residuals deserve attention:

1. **MEDIUM — Header implementation and narrowing semantics.** [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) describes a header containing a partition list. That list itself grows as partitions multiply. The overflow fixture must therefore exercise an oversized **partition directory**, not merely an oversized list of node IDs. Implement bounded navigation or an equivalent proven campaign bound. The fallback that narrows index scope must preserve the frozen access rules and complete addressability; logging alone cannot authorize a protocol change. **Does not block bootstrap or auditing; must be settled before Lock 1.** The explicit bounded-rendering requirement is why the original planning finding now closes.

2. **MEDIUM — Memo namespace and cross-arm charging need explicit implementation treatment.** [PLAN:55](/Users/bmarti44/github/bufferright/research/PLAN.md:55) gives a state/protocol cache key, while [PLAN:130](/Users/bmarti44/github/bufferright/research/PLAN.md:130) charges creation to the producing arm. Define how distinct output types and arm ownership are represented. A global cache must not let whichever arm runs second receive free generation or different remaining resources. Existing isolation and allocation requirements prohibit that outcome; the memo implementation must demonstrate compliance. **Does not block independent preliminary work; blocks comparison execution until verified.**

3. **LOW — Replay “retain incumbent” wording is broader than necessary.** [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) associates retention with the incumbent ordering first, whereas [PLAN:121](/Users/bmarti44/github/bufferright/research/PLAN.md:121) still requires selecting a challenger for fresh testing. Interpret the former as replay ordering only; final retention follows the fresh comparison. **Nonblocking:** Phase 4 explicitly says replay superiority never substitutes for fresh evidence.

The plan is sufficiently constrained to proceed through its staged gates. The residuals require implementation discipline, not a redesign or relaxation of the specification.

SCORE: 92
tokens used
62,388
**All five round-4 findings are resolved at the planning level. No high or critical issue remains open.** This is approval of the written execution contract, not evidence that its tests or scientific gates have passed.

I read all four requested documents in full. No edits made. Reviewed PLAN SHA-256: `5e4e6051bd2e…`.

| Round-4 item | Verdict | Quoted evidence and assessment |
|---|---|---|
| **R2#30 — context overflow** | **RESOLVED** | [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) requires a “**bounded directory header**,” subdivisions with “**fixed row/token caps**,” and reserved space for instructions and retrieved records. It explicitly requires directory-overflow and single-direction-overflow fixtures “**both rendering legally**.” These are concrete acceptance requirements addressing both previous failure cases. See the implementation caveat below. |
| **Donor-grouped predictive folds — high** | **RESOLVED** | [PLAN:109](/Users/bmarti44/github/bufferright/research/PLAN.md:109) keeps every conservatively linked donor’s observations in one fold, “**including nested tuning folds**.” The shared-donor/distinct-model fixture must fail the build if observations straddle folds. This governs predictive evaluation separately from donor resampling and preserves legitimate within-model contrasts. |
| **Arm-scoped dedup — high** | **RESOLVED** | [PLAN:44](/Users/bmarti44/github/bufferright/research/PLAN.md:44) limits duplicate eligibility to “**the acting arm’s episode-admissible history**,” permits genuinely new evaluations, and prohibits global membership from changing observations, rejections or legal actions. Hidden-configuration and reversed-execution-order tests directly target the former interference channel. |
| **Total ordering of tied challengers — medium** | **RESOLVED** | [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) adds “**earlier position in the SPEC’s pre-listed candidate order**,” followed by “**lexicographically smaller immutable candidate ID**.” Thus two challengers tied above the incumbent remain deterministically ordered. |
| **Deterministic reconstruction of LLM state — medium** | **RESOLVED** | [PLAN:55](/Users/bmarti44/github/bufferright/research/PLAN.md:55) defines “**immutable memoized output**” keyed by admissible state and protocol version. Reconstruction “**reads the memo — never re-invokes the model**”; a replay cache miss becomes unsupported. The required reconstruction test checks identical rendered bytes and zero additional model calls. |

The earlier-world charging clarification also closes the substantive loophole it targets. [PLAN:130](/Users/bmarti44/github/bufferright/research/PLAN.md:130) charges “**the production cost of every history it reads**,” specifies symmetric access rules, and prohibits consuming another arm’s outcomes. Together with ancestry accounting and the frozen allocation rule, this prevents historical information from being treated as free merely because its production preceded deployment.

I found **no additional high or critical defect** after checking specification fidelity, independence, confirmatory selection, replay support, comparison fairness and terminal criteria. In particular:

- [PLAN:136](/Users/bmarti44/github/bufferright/research/PLAN.md:136) prevents external transfer validation from laundering an adaptively selected environmental effect into independent confirmation.
- [PLAN:128](/Users/bmarti44/github/bufferright/research/PLAN.md:128) makes the comparison estimand, censoring-compatible interval and precision-feasibility result mandatory at Lock 1. Their numerical specification remains legitimate pre-lock work.
- [PLAN:131](/Users/bmarti44/github/bufferright/research/PLAN.md:131) retains the unresolved cost gate when material host-model costs cannot be measured. Execution can produce an honest non-complete result; completion is not guaranteed by the plan.

Three residuals deserve attention:

1. **MEDIUM — Header implementation and narrowing semantics.** [PLAN:23](/Users/bmarti44/github/bufferright/research/PLAN.md:23) describes a header containing a partition list. That list itself grows as partitions multiply. The overflow fixture must therefore exercise an oversized **partition directory**, not merely an oversized list of node IDs. Implement bounded navigation or an equivalent proven campaign bound. The fallback that narrows index scope must preserve the frozen access rules and complete addressability; logging alone cannot authorize a protocol change. **Does not block bootstrap or auditing; must be settled before Lock 1.** The explicit bounded-rendering requirement is why the original planning finding now closes.

2. **MEDIUM — Memo namespace and cross-arm charging need explicit implementation treatment.** [PLAN:55](/Users/bmarti44/github/bufferright/research/PLAN.md:55) gives a state/protocol cache key, while [PLAN:130](/Users/bmarti44/github/bufferright/research/PLAN.md:130) charges creation to the producing arm. Define how distinct output types and arm ownership are represented. A global cache must not let whichever arm runs second receive free generation or different remaining resources. Existing isolation and allocation requirements prohibit that outcome; the memo implementation must demonstrate compliance. **Does not block independent preliminary work; blocks comparison execution until verified.**

3. **LOW — Replay “retain incumbent” wording is broader than necessary.** [PLAN:58](/Users/bmarti44/github/bufferright/research/PLAN.md:58) associates retention with the incumbent ordering first, whereas [PLAN:121](/Users/bmarti44/github/bufferright/research/PLAN.md:121) still requires selecting a challenger for fresh testing. Interpret the former as replay ordering only; final retention follows the fresh comparison. **Nonblocking:** Phase 4 explicitly says replay superiority never substitutes for fresh evidence.

The plan is sufficiently constrained to proceed through its staged gates. The residuals require implementation discipline, not a redesign or relaxation of the specification.

SCORE: 92
