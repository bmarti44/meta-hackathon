**METADATA_SCREEN_PASS is supported for the frozen inputs.** Found **0 critical, 0 high, 2 medium, and 1 low issue** within scope.

Read-only reproduction matched `readiness_v6.json` exactly. Removing outcome fields produced the identical report; no outcome magnitudes or deltas were analyzed.

1. **Medium — screen orientation is not validated against provenance.** Reversing `screen_a/b` still yields `METADATA_SCREEN_PASS` for both axes. A permitted but incorrect held condition, or relabeling a format pair as medium, also passes. Declared labels are checked, but `c_col` is unused. Compare each screen’s actual varying and held conditions with the declaration. The unchanged inventory has **zero mismatches** under an independent metadata join. [Validation](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v6.py:95)

2. **Medium — sufficiently large inventory loss still receives a structural verdict.** Removing ACH-001418’s 250 rows correctly yields `REPAIR_METADATA`. However, removing all 750 EVAL/format rows yields `FAIL_SUBSTRATE`, despite the failed inventory check and repairability by row restoration. `full_cov` counts the remaining rows; it does not establish complete inventory. Require inventory completeness before declaring structural insufficiency. [Precedence](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v6.py:159)

3. **Low — whitespace PatientIDs pass completeness.** `PatientID=""` correctly fails, but `"   "` yields `METADATA_SCREEN_PASS`. Normalize IDs before completeness and overlap checks. All six current nonquarantined IDs are populated and distinct; this supports separation in recorded linkage metadata only. [Patient gate](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v6.py:135)

Requested verification:

| Check | Result |
|---|---|
| Contrast rejection | Identical screens, invented held condition/axis, and reversed declared labels fail. Reversed actual screens pass incorrectly. |
| Frozen orientation | Declared labels enforce Dome/Plastic and OPAC/RPMI-FBS order; provenance orientation remains unchecked. |
| Patient completeness | Empty ID fails; whitespace caveat above. |
| Verdict precedence | Specified 250-row restoration case returns `REPAIR_METADATA`; larger-loss caveat above. |
| Costs/witnesses | Shared substrate/E0 and evaluator construction are distinguished from arm-specific generation/review/unstick calls. Cycle-lock witnesses remain explicitly open. |
| SPEC header | Supersession, engineering framing, no C13 credit, and reused-data limitation are preserved. |
| Manifest | Directly pinned; all six pins match. Pin mismatches and empty manifests are refused. |

Confirmed **2,750 catalogue actions**: DEV/format **1,000**, DEV/medium **1,000**, EVAL/format **500**, EVAL/medium **250**.

Semantic probes substituted metadata after verification to isolate validator behavior; they do not bypass production byte pins.

PGEN006_V6_SCORE: 91