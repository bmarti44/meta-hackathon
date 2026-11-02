# C9 adjudication under the 2026-10-29 user amendment (sgen014 workstream 3)

## Amended evidence rule applied
GOAL.md amendment (sha f4ea241a...): estimated-cost basis is admissible C9
cost evidence prospectively. Recorded figures (estimator v7,
ledger/host_cost_estimate_v7.json, micro-review 100):
- Estimated list-price equivalent: $34.1806698 across 66 accounted calls
  (61 receipt-priced $29.0675698 + 5 imputed $5.1131000; 0 events-priced).
- Actual metered spend: $0 (subscription auth; additional_api_spend_cap_usd=0).
- These are distinct quantities; the estimate is never metered billing.

## Remaining C9 requirements (unchanged by amendment)
C9 = "learned policy meets preregistered practical-improvement criterion vs
strongest fixed baseline, end-to-end incl. overhead." Status per element:
- Cost evidence rule: SATISFIABLE under amended basis (was structurally blocked).
- Preregistered criterion: exists in pgen005 SPEC (S>=20% one-sided 95% LB at
  locked Q*, incl. 2x/4x imputation sensitivity) but Q* itself not yet
  numerically instantiated (witness open).
- Learned policy + strongest-fixed comparison: NEVER RUN. No qualifying
  scientific task instantiated (sgen011 NEITHER_PASSES; sgen012
  A_STILL_UNRESOLVED; sgen013 FAIL). No policy cycle has executed.
- Matching witnesses (nodes/calls/wall): untested (no comparison exists).
=> C9 remains UNMET empirically. The amendment removes the evidence-rule
block only; it certifies no savings and no policy improvement.

## What would satisfy C9 from here
A qualifying scientific task (per pgen005 witness list) + >=2 genuine
improvement cycles with fresh rollouts + final frozen comparison meeting the
preregistered criterion under the estimated-cost basis.
