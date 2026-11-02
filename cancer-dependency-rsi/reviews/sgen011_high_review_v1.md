Read-only review complete. **The current `NEITHER_PASSES` decision is supported, but the specification and accounting need corrections.** Found **0 critical, 1 high, 5 medium, and 2 low issues**.

1. **High — The feasibility contract does not fully specify the scientific test.** [sgen011 SPEC](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen011/SPEC.md:27) names “patient-level Spearman” without defining the two variables, patient aggregation, gene/context hypothesis family, or nuisance envelope. The observed Lock-S magnitude supplies the threshold without a scientific justification for either new design. Pooled Fisher-z precision does not establish within-lineage overlap or identifiability. The authority explicitly requires these conditions. Treat `precision_A.pass` as an optimistic calculation, not established feasibility.

2. **Medium — A’s precision calculation includes organoids.** [sgen011_screen.py](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen011_screen.py:90) uses all 1,106 models and 1,068 components for the **cell-line** design. Restricting A to cell lines gives **1,095 models, 1,058 SIDP identifiers, and 1,057 linked components**, with MDR **0.0860810**, rather than **0.0856375**. This does not change the present rejection.

3. **Medium — B’s locked pass rule omits required identity safeguards.** [SPEC](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen011/SPEC.md:42) makes B depend only on precision, assuming sgen010 establishes everything necessary. The authority additionally requires an authoritative crosswalk and **renewed component-level exclusion checks**. These must remain explicit prerequisites, particularly when adding unresolved organoids.

4. **Medium — Several pgen005 witnesses are prematurely checked.** [WITNESSES.md](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/pgen005/WITNESSES.md:5) substitutes an identified pool for actual disjoint development/reserved panels, an existing replay world for faithful replay of the new task, and campaign pricing for complete task/arm cost attribution. Those are prerequisites, not completed witnesses. The explicit “rollout gate NOT passed” prevents immediate unauthorized execution, but these boxes should remain pending.

5. **Medium — Identity-critical derived inputs are neither verified nor recorded as hashed inputs.** [sgen011_screen.py](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen011_screen.py:57) trusts `established_pool_v4.json` and `screen_v7.json` while checking only the two raw CSV hashes. It imports pooled component counts and substitutes DepMap PatientID counts for subset components. Current values independently match, but the executable does not enforce the identity/exclusion artifact version it claims to use. Pin those artifacts or reconstruct and validate their assignments/components.

6. **Medium — Events fallback still violates the required usage-reconstruction rule.** [host_cost_estimate.py](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/host_cost_estimate.py:89) unconditionally takes the last usage record; it neither establishes cumulative semantics nor reconstructs independent turns. It also discards reservation ID, phase, and effort. An in-memory two-turn example costs **$0.009**, while this fallback returns **$0.006**. Reconstruct usage or impute missing usage, and retain reservation attribution. **No v4 CSV row uses this fallback**, so this defect does not alter v4’s current total.

7. **Low — Aggregation rounds before reconciliation.** [host_cost_estimate.py](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/host_cost_estimate.py:73) rounds receipt costs before selecting maxima and summing. Exact receipt costs plus exact matching maxima total **$32.9458340**; the rounded CSV sums to **$32.9461**. Both display as **$32.95**, but the authority requires unrounded reconciliation. Preserve full precision through aggregation.

8. **Low — Accounting labels and the ledger’s priced subtotal are inaccurate.** [v4 report](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/host_cost_estimate_v4.json:6) calls all **63** rows “priced,” although **57 are receipt-priced and six imputed**. [The ledger entry](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/experiments.jsonl:94) retains `priced_only_usd: 26.7`; v4’s receipt-priced subtotal is **$26.8108510**, reflecting the added v2 consultation. Report receipt-priced, imputed, and accounted counts separately.

The independent provenance audit inspected **all 48 Model.csv columns**, including free-text comments and the additional derivation, treatment, engineering, resistance, and model-type fields. **No supplied field explicitly establishes the actual screening format/medium per ScreenID.** `CRISPRScreenMap.csv` contains only `ScreenID` and `ModelID`. I found no screened-environment record that the SPEC wrongly rejects as onboarding metadata. All six reported field-population counts reproduce; `PlateCoating` is populated entirely with the literal value `None`.

The precision arithmetic reproduces under the stated Fisher-z approximation:

| Population | Components | MDR, α=.05 | MDR, α=.01 |
|---|---:|---:|---:|
| Whole established pool | 1,068 | 0.0856375 | — |
| Lung | 119 | 0.2544084 | 0.3070656 |
| Lymphoid | 90 | 0.2916434 | 0.3508293 |
| CNS/Brain | 84 | 0.3016077 | 0.3624614 |
| Esophagus/Stomach | 72 | 0.3250391 | 0.3896715 |
| Head and Neck | 69 | 0.3318015 | 0.3974855 |
| Established organoids | 11 | 0.7575797 | — |

Independent reconstruction confirms **1,106 models / 1,069 SIDP / 1,068 linked components**, and the five lineage component counts equal the reported PatientID counts here. The calculated sample-size boundary is **365.9715499**, hence **366**. At 365 patients MDR is **0.1461930**; at 366 it is **0.1459944**.

Cost v4 correctly implements phase-plus-effort maximum selection for this single-model campaign:

- Five xhigh imputations use **$1.021883**, displayed as **$1.0219**.
- One high imputation uses **$1.025568**, displayed as **$1.0256**.
- No campaign-maximum fallback is needed.
- Exact receipt subtotal: **$26.8108510**.
- Exact imputation subtotal: **$6.1349830**.
- Exact phase totals: **$18.9897408 + $13.9560932 = $32.9458340**.

The six unpriced reservations are complete **at v4’s creation cutoff**. The current review reservation came afterward; the first consultation’s receipt and usage arrived later at approximately **12:52:45 UTC**. Neither makes the frozen snapshot erroneous. All 57 receipt-priced rows match their retained event usage.

The Boolean decision rule is applied correctly: A fails provenance; B fails precision; outcome generation is rejected. pgen005 preserves the conditional specification-only authorization, savings threshold, sensitivity requirements, comparator rules, matching constraints, and original C9 limitation. I found no rollout smuggled into its authorization.

Ledger ordering also checks out: the matching pgen005 SPEC lock precedes the sgen011 SPEC lock in ledger order at **12:50:55.933776 UTC**; the screen artifact was created at approximately **12:51:33.489 UTC** and recorded afterward. Both SPEC hashes match their lock records.

SGEN011_SCORE: 82