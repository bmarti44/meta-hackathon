The counts and Witness A reproduce exactly. The claim that all 1,361 screened models are donor-disjoint from cohort C is stronger than the identity evidence supports. I found no actual C-overlapping model, including through additional alias checks.

Read-only verification included independent recomputation and rerunning all three scripts with writes redirected into memory. Every generated JSON matched its stored artifact.

Independent results:

- **Witness A:** 148/148 models resolved, 142 nonempty patients, zero unresolved or ambiguous matches. Executing the original pandas-based Witness-A code produced the same complete patient map.
- **DepMap:** 2,554 models, 2,315 PatientIDs; 1,604 screens covering 1,361 models and 1,305 PatientIDs. No screened ModelID was missing from Model.csv; no PatientID was empty.
- **Screened organoids:** 108 models, 102 PatientIDs.
- **C overlaps:** zero on the five implemented keys. Broader checks using aliases, RRIDs, CCLE identifiers, and other identifier columns also found zero.

The key populations explain why five zeroes provide uneven assurance:

| v3 comparison | DepMap populated rows | Usable C-side values | Whole-table positive control | C matches |
|---|---:|---:|---:|---:|
| ModelID ↔ BROAD_ID (`ACH-…`) | 2,554 | **0** | 1,739 shared IDs | 0 |
| SangerModelID ↔ model_id (`SIDM…`) | 1,220 | 148 | 1,218 shared IDs | 0 |
| COSMICID ↔ COSMIC_ID, numeric normalization | 977 | **0** | 973 shared IDs | 0 |
| Normalized names and synonyms | 2,554 | 223 | 1,696 shared canonical names | 0 |
| HCMIID ↔ HCMI | 215 | 51 | 19 shared IDs | 0 |

Thus SIDM, names, and HCMI connect globally. **BROAD_ID and COSMIC are vacuous for C**, because their C-side sets are empty. The original donor_ID-to-COSMIC comparison also mixed individual-level and sample-level identifiers; numeric normalization alone cannot repair that semantic mismatch.

Issues found, ordered by severity:

1. **High — Unresolved target identities are counted as proven disjoint.**  
   [The exclusion logic](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v3.py:135) treats every nonmatch as eligible. Even with broader matching than v3 implements, **252 screened models remain unlinked to Passports**, including **97/108 organoids**. These represent 240 DepMap PatientIDs; 236 have no Passports crosswalk through any of their DepMap models.

   A C patient could therefore have another screened model absent from the Passports snapshot, carrying unrecognized identifiers or a different PatientID. None of the implemented keys excludes that route. Because the observed overlap union is empty, `overlap_patients` is also empty: patient-level propagation excludes nobody.

   `bridge_full_coverage` measures C-to-Passports coverage, while its accompanying text claims broader patient-level disjointness. Report these models as **identity unresolved**, and restrict any established pool to adequately reconciled identities. This need not destroy the discriminator: identifier-only matching finds 1,108 screened models with an unambiguous Passports patient assignment, already above the numerical threshold.

2. **Medium — PatientID partitions are not reconciled across registries.**  
   [Patient-strict exclusion](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v3.py:136) propagates only through identical DepMap PatientID strings. The supplied metadata demonstrate that those partitions differ from Passports: `SIDP00357` connects through BROAD_ID to U-118 MG and 1321N1, which have different DepMap PatientIDs. Among screened models matched directly through BROAD_ID, there are **1,049 DepMap PatientIDs versus 1,050 Passports patients**.

   These discrepancies do not demonstrate C leakage or establish a corrected biological patient count. They do show that “1,305 PatientIDs” should not be presented as independently verified biological patients without identity reconciliation.

3. **Medium — v1/v2 accounting departs from the locked protocol.**  
   The original SPEC hash reconstructs exactly, and the amended SPEC matches its ledger hash. Available file times support both locks preceding their corresponding scripts.

   However, [the original rule](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen010/SPEC.md:37) says either verdict is a used discriminator result. [The ledger](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/experiments.jsonl:69) instead records v1 as “verdict not used.” Its entry and v2’s share a timestamp after both reports existed. v2 also introduced Passports and a changed bridge without a prior amendment, then recorded the additional `POOL_IDENTIFIED_BRIDGE_PARTIAL` label.

   Supersession is disclosed; I found no evidence of concealment. Nevertheless, this is an adaptive repair rather than execution entirely under the original lock. The v3 amendment is properly recorded before v3 execution. **The numerical thresholds themselves remained unchanged and were applied correctly to the computed counts.**

4. **Medium — Bridge integrity is protected by aggregate counts, not locked identities.**  
   [v3 validates hashes only for the two DepMap files](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v3.py:54). It does not enforce the acquired Passports hash or a cohort hash; its reproduction guard compares counts against an unhashed prior JSON. Recording the newly computed Passports hash afterward does not enforce the intended input version.

   In an in-memory negative probe, reassigning one C patient to an existing non-C Passports patient preserved all four Witness-A counts. v3 still returned success and `POOL_IDENTIFIED`, while incorrectly excluding `ACH-000001`. **The current map is correct**, but the guard does not establish identity-level reproducibility. Pin the bridge inputs and validate the resulting mapping, rather than relying solely on four counts.

5. **Low — A specified metadata summary is missing.**  
   [SPEC method 1](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen010/SPEC.md:19) requires a `DepmapModelType` distribution. None of the three reports supplies it; they report `ModelType` and `GrowthPattern`. This does not affect the threshold calculation.

6. **Low — “No outcomes anywhere” needs narrower wording.**  
   No dependency-outcome file was accessed in the instrumented executions, and the scripts contain no network calls or dependency-matrix access. Their reads are confined to the stipulated metadata and prior metadata reports.

   However, the loaded metadata contain **146 populated `PatientTreatmentResponse` values**, **41 `prior_therapy_outcome` values**, and **24 tumour-regression scores**. These clinical fields are parsed but unused. Claims of **no dependency-outcome access** are supported; literal claims that no outcome data were touched are not.

7. **Low — v3’s two outputs are not transactional.**  
   [The map is exclusively created first](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v3.py:99), before subsequent computation and [report creation](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v3.py:187). An interruption or later failure can leave an orphan map that prevents an ordinary rerun. Compute and validate both artifacts before committing the output pair.

No critical issue was found. The generation establishes a reproducible metadata screen with zero observed C matches; it does not yet establish unconditional donor disjointness for the entire reported pool.

SGEN010_SCORE: 68