# Gate G2 round-2 dispositions — unreviewed remediation checkpoint

2026-10-28. Round 2 scored **74/100, FAIL**. Lock 1 remains a draft. This document is the lead's disposition, not a passing independent review. No policy optimization, pilot, policy cycle, or external evaluation has run.

| Round-2 issue | Lead disposition and evidence |
|---|---|
| 1 OLS artificial precision | Reviewer resolved. OLS remains a reproduction anchor only. |
| 2 Calibration/degeneracy | **CONFIRMED, PARTIAL safety repair.** `evaluator_v3.py` counts nonfinite bootstrap statistics as failures, rejects null-bootstrap failures, and refuses legacy null coverage below 0.90. Every draft result also carries `admissible_for_policy=false`; passing this diagnostic cannot certify calibration. Freedman–Lane gene exchangeability, nonzero-effect/grouped calibration, and an appropriate uncertainty target remain unresolved. Required xhigh consultation retained in `reviews/prompts/g2_unstick_xhigh_1.txt`. Do not start pilot. |
| 3 Confirmatory/development separation | Reviewer resolved. Confirmatory config is unchanged. |
| 4 Uncertainty target | **CONFIRMED, OPEN.** Donor decision interval is specified. Exact conservative Broad grouping and donor-bootstrap synthetic acceptance gate remain to be frozen; no outcome access is authorized by this checkpoint. |
| 5 Artifacts/hierarchy | **CONFIRMED, OPEN.** Contract hash list remains a historical draft and is not a valid lock. Regenerate the entire bundle only after remediation and G2 pass; never reinterpret stale hashes as a completed freeze. |
| 6 Scope eligibility | Reviewer resolved membership; runtime safety repaired below. |
| 7 Baseline adequacy | Reviewer resolved for narrowed association question. Exact authors' OLS check passes; worst discrepancy across all environmental terms is 1.7316e-8, including interaction. Previous STATUS claim <1e-8 for all terms is corrected. |
| 8 Savings design | **CONFIRMED, OPEN.** Panel242 primary/sensitivity contradiction, exact baseline action procedures, seeds, strongest-baseline bootstrap construction, and executable precision calculation need one coherent specification before freeze. C9 remains unresolved independently of this. |
| 9 Threshold/support | **CONFIRMED, OPEN.** Reconcile Phase-5 population/admissibility with issue 8; retain E0 threshold edge-case rules. |
| 10 Direction status | **CONFIRMED+FIXED, awaiting independent re-review.** Require one failure class to dominate rather than combining two; a later valid success resets the conceptual failures that define `dead`. Regression fixtures cover both counterexamples. |
| 11 Budget concurrency | **CONFIRMED+FIXED in implemented dimensions, awaiting re-review.** Advisory file lock covers read/check/fsynced append, with separate-process and thread contention fixtures. Enforce total/phase node, model-call and wall maxima, terminal call reserve, CPU slots, aggregate reserved memory. Validate actuals and prevent duplicate reconciliation; overruns are recorded and charged. Interrupted reservations remain outstanding. This is not certification of all G0 resource acceptance tests: CPU-heavy dispatch currently fails closed if macOS rejects its address-space limit; scientific peak-RSS enforcement still needs a working acceptance test. Historical unledgered work remains an accounting gap. |
| 12 Deferred acceptance tests | **CONFIRMED, PARTIAL.** Actual concurrent-reservation tests replace the sequential-only claim. Full runner memo charging/reconstruction, hidden-outcome invariance, exact-context replay, guarded external access, synthetic confirmatory bootstrap, compatibility acceptance and production resume tests still need their named gates. |
| New nonfinite inputs | **CONFIRMED+FIXED, awaiting re-review.** Validate raw arrays/covariates before ranking; all +/-inf and NaN fixtures reject. Unadjusted estimator validates raw values too. |
| New frozen membership | **CONFIRMED+FIXED, awaiting re-review.** v3 rejects missing frozen members and duplicated source/frozen indices instead of silently intersecting. |
| New generator/lineage mismatch | **CONFIRMED, PARTIAL.** DAG validator accepts parent objects with nonempty contributions and legacy recorded IDs, rejects duplicate parents, checks repair citations, and traverses both forms. Single-object schema versus proposer list envelope remains to be versioned coherently before generation. |

## Evaluator provenance and invalidation

Original v2 source is retained byte-for-byte at `src/evaluator_v2.py` and `artifacts/sha256/dda3e2ffcc5dd386ebfe7486a35e073756601bf3a947b7ad30c8215d32506360` (hash verified). v3 is an **unapproved safety draft**, not a frozen replacement. All v1/v2 q scores are inadmissible for future optimization; no policy decisions relied on them. Draft diagnostics never enter a replay world. Raw-input validation also changes `estimators.py`; contract hashes must therefore be regenerated at the actual lock.

The fixed safety probe specification is committed to the experiment ledger before its 12 Layer-A diagnostic evaluations. It compares the same six E0 roots, same seed, two evaluator versions. It is a readiness diagnostic, not a research generation or C13 evidence. Results, code hashes, wall/CPU and peak RSS are retained separately.

## Execution blocker

Required Sol-xhigh consultation could not start: both installed Codex 0.165.0 and 0.164.0 return `failed to initialize in-process app-server client: Operation not permitted (os error 1)`. Neither returned a model response. Failed attempts are retained and charged conservatively as dispatched model-call attempts; separately metered spend is $0; host costs remain unknown. No permission escalation or restriction bypass was attempted. The first wrapper reconciliation defect was corrected and the failed reservation explicitly reconciled.

Smallest next step: run the retained xhigh consultation through an authorized host terminal using the resume command in STATUS.md. Then implement its legal uncertainty design, finish the OPEN items above, run the acceptance suite, and obtain Sol-high G2 >=90 with zero unresolved high/critical issues **before** freezing or running E0.
