**METADATA_SCREEN_PASS is supported for the frozen inputs as a preparatory engineering screen.** It establishes neither execution readiness nor C13 credit. I found **no critical or high issues, four medium issues, and two low issues**.

Review was read-only. I reproduced `readiness_v5.json` exactly with output redirected to memory. Removing outcome fields from the computation produced the identical report. Presence checks found all 3,000 entries populated in each paired outcome column; no delta magnitudes or signs were analyzed.

| Requested closure | Recomputed result |
|---|---|
| 1. Framing and label | Operative amendment/report use `ENGINEERING_PILOT_SEPARATE`, `METADATA_SCREEN_PASS`, and no C13 credit. Superseded SPEC wording remains. |
| 2. Action identity | **3,000 unique** `(gene, axis, model, held_condition)` actions; zero collisions. ACH-003040’s medium and format contexts remain distinct. |
| 3. Patient separation/quarantine | Six nonempty, distinct PatientIDs; no DEV/EVAL overlap. An independent join through available patient, alias, and Sanger identifiers found no cross-partition component. ACH-003052 contributes no catalogue actions. **2,750** remain; EVAL/format has **500 across two models**. This supports recorded-metadata separation, not comprehensive donor independence or untouched evaluation. |
| 4. Frozen inventory | Exactly **3,000 rows**, zero OUT rows. Deletion and OUT reassignment fail validation. Direct byte changes also fail pins. |
| 5. Screen provenance | Current base-screen joins and replicate agreement pass. `invented_screen` and disagreeing replicates produce `REPAIR_METADATA`. Contrast-context validation remains incomplete. |
| 6. Direct pins | All five declared input digests match and reject altered bytes. The additionally consumed atlas manifest is unpinned. |
| 7. Costs/open witnesses | Unit-node table and host-accounting reference exist; Q*, policies, and evaluator are explicitly open. Complete host attribution is not implemented. |
| 8. Verdict precedence | Improved, but repairable inventory loss can still receive `FAIL_SUBSTRATE`. |
| 9. Per-axis contributors | Format readiness counts actual contributors: two evaluation models. Medium has one and does not satisfy an evaluation-readiness check; it is declared development-only. |
| 10. v2 reconstruction | Disclosure is adequate as a reconstruction, not original-source authentication. Retained v1–v4 sources all reproduce their saved reports exactly. |

The remaining issues are:

1. **Medium — provenance validation does not verify the declared contrast.** The loop checks screen existence, model, and recorded registry cell, but never uses `c_col` to compare `condition_a/b`, nor validates axis-specific held conditions. Loader-level probes with identical screens on both sides, reversed screens, an invented held condition, or an invented axis still pass. My independent condition/orientation join found **zero mismatches in the current pinned inventory**, so this is a validator defect rather than demonstrated corruption. Validate both varying and held conditions, permitted axes, orientation, and distinct screens. [Validation loop](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v5.py:90)

2. **Medium — the patient check permits missing identity.** It removes `None` and empty strings from the overlap calculation without requiring nonempty PatientIDs for every nonquarantined contributor. Blanking ACH-001418’s PatientID through the loader still yields a pass. All six current identities are populated and distinct; retain that result while adding a completeness gate and explicitly limiting the claim to available linkage metadata. [Patient checks](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v5.py:117)

3. **Medium — coverage shortage is treated as demonstrated structural failure.** Removing ACH-001418’s 250 rows fails both frozen inventory and the format minimum, producing `FAIL_SUBSTRATE`. Restoring the frozen rows repairs that case; it does not demonstrate substrate impossibility. Classify incomplete or unresolved inventory as repairable before declaring structural insufficiency. [Verdict precedence](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v5.py:139)

4. **Medium — host-cost attribution remains underspecified.** The table supplies one evaluated node per action, but its host-accounting “hook” is prose and says generation/review calls are shared equally across arms. The referenced contract permits equal allocation for shared E0 production while requiring learning overhead and unresolved costs to receive appropriate attribution. Define which calls are shared and which belong to an arm, and explicitly retain complete attribution as an open witness. This limits future cost comparisons, not the present metadata label. [Cost table](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v5.py:164), [accounting contract](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/pgen005/SPEC.md:14)

5. **Low — the SPEC retains conflicting operative-looking instructions.** The amendment controls framing, but preceding sections still announce GO_REPLAY, propose a pgen005 instantiation, define the old action, treat models as independent sources, and describe held-out evaluation. Mark those sections superseded or consolidate the amended specification. Explicitly preserve the reused-data engineering-evaluation limitation; the amendment does not make previously inspected recordings untouched. [Original instructions](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/pgen006/SPEC.md:3), [amendment](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/pgen006/SPEC.md:54)

6. **Low — the consumed manifest is not directly frozen.** Substituting `{}` for `atlas/v4/manifest.json` in memory skips its entire verification loop and produces the identical passing report. Direct output pins protect the present inventory, but the additional provenance-chain check can disappear silently. Pin the manifest and require its expected entries. [Manifest consumption](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen006_readiness_v5.py:46)

The semantic probes above substituted metadata **after file verification** to isolate validator behavior. They do not bypass the production byte pins: altered bytes in any of the five pinned files were refused.

PGEN006_V5_SCORE: 85