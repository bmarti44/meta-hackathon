**97/100, up from 84. Remaining issues: 0 critical, 0 high, 0 medium, 1 low.**

1. **Low — Known parent exposure can still be suppressed by a broken ancestor link.** Exposure found in an otherwise validated parent is considered only when the entire chain succeeds. Synthetic probe: an untreated current condition → exposed parent → missing grandparent produces `PARENT_CONDITION_DEPENDENCE`, incorrectly blocking a model with another valid eligible sequence. Removing the broken link correctly disqualifies the exposed sequence and retains the model. Check exposure across the validated chain prefix before requiring complete traversal. No currently joined condition has a parent, so published results are unaffected. [Classification logic](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen_v3.py:221)

Requested verification:

| Check | Result |
|---|---|
| Frozen source crosswalk | Correct and non-circular: Avana/Humagne-CD→BROAD; KY→SANGER; Brunello/TKOv3→BROAD/OTHER. Mutating Avana’s condition source to SANGER produces `datasource_library_inconsistent`. |
| Per-sequence audit | **2,976 records = 1,976 eligible + 970 unresolved + 30 disqualified**. Category/reason fields and per-model totals reconcile. All eligible details include replicate/days/pDNA metadata; membership publishes **724 retained components / 729 models**. |
| Classification coverage | Every classification branch tested emits a record. Identical duplicates collapse; conflicting duplicates remain unresolved, including three-record probes. |
| Environment-by-lineage tables | Both explicitly published; independent calculations reproduce V **0.5682 overall / 0.5117 selected**. |
| Join cardinalities | Correctly distinguished: **1,310 joined conditions / 957 distinct eligible-detail conditions**. |
| Retained context | Independently reproduces **1,459 sequences**: SerumFree False **1,455**, True **4**; BROAD **1,459**. Other published context distributions also match. |
| Current-condition exposure | All five exposure fields disqualify despite a broken parent; an accompanying valid sequence retains the model. |
| Exact minimum | **1,458**: MDR **0.14599435**; at 1,457, **0.14604396**. |
| SPEC amendment | Corrected to **132 strata** and minimum **1,458**. |

All seven hashes match, and an in-memory replay reproduces both JSON artifacts exactly. Verdict remains **`A_STILL_UNRESOLVED`**, with **729 models / 724 components**, selected arms **190/86**, and MDR **0.35356277 → 0.3536**. The two disclosed audit-basis gaps remain appropriately unresolved.

Read-only throughout; neither `Gene.csv` nor anything in `~/Downloads` was read.

SGEN012_V3_SCORE: 97