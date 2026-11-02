**Score: 68/100.** The sealed numerical results reproduce, and the performance verdict correctly remains **FAIL**. I reject certification as a fully compliant frozen execution because of protocol provenance, restart handling, label accessibility, and incomplete verification records. These findings only annotate the sealed results.

Independent read-only verification confirmed:

- All 23 arm/runs contain the same 500 targets, with five nonnegative Fraction probabilities summing exactly to one.
- All 230 episode transcripts contain exactly 20 distinct eligible queries, with no target queries.
- Every sealed prediction reproduces from its transcript. All 200 random transcripts match the prescribed seed serialization, SHA-256 big-endian conversion, and shuffle.
- Every DEV candidate score and selection reproduces: `theta_hat=(4,0,0)`, `L_W`, and `K1`.
- Decimal classification handles both ±0.10 boundaries and signed zero correctly. Fraction arithmetic governs probabilities, acquisition, losses, and selection; float conversion occurs for reporting.
- LOMO excludes the assessed model, shared predictor transcripts are reused as prescribed, candidate order resolves exact ties correctly, and K2–K5 use the correct static score bases.
- Priors contain only permitted D outcomes. The atlas, SPEC, prior-summary, and sealed-file hashes match. The v8 metadata inputs also retain their recorded hashes and six distinct recorded PatientIDs.
- The executor writes and hashes all EVAL predictions before computing aggregate EVAL losses.

The issues are:

1. **High — The frozen protocol omits items 66–79.**  
   [SPEC.md](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/pgen010/SPEC.md:120) ends at item 65, as do the pgen007–pgen009 SPEC files. The [original generated specification](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reviews/xhigh_pgen007_cycle_generate.md:80) contains 79 items, including cost allocation, crash handling, determinism, exhaustive failure labeling, and archival requirements. Consequently, references to items 66, 69, and 74 point outside the actual frozen SPEC. The pre-run PASS 100 did not resolve this provenance gap. Missing rules cannot be silently inserted after execution.

2. **High — The same-cycle restart cannot be certified under the requested items 69/74.**  
   The [ledger](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/experiments.jsonl:187) records an `EXECUTION_FAILURE`, implementation repair, and re-run under pgen010. Accepting its assertion that the first attempt failed before computing any outcomes, zero node charges are reasonable and there is no evidence of outcome-informed retry selection. Nevertheless, original item 74 requires a separately frozen cycle after **any execution failure**; item 69 supplies no zero-outcome exception. Under those rules, this restart was not legitimate. Under the truncated on-disk SPEC, the required exception is simply unspecified. The final “valid execution” description overstates compliance. No original crash traceback or source revision is archived with the cited entry to independently establish the zero-outcome claim.

3. **High — Policies can access the complete label atlas.**  
   [The loader and policy interface](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen010_cycle.py:39) classify all 3,000 rows, including the excluded medium and quarantined outcomes; `labels = nodes` is then passed into policy routines. This violates items 17/57’s requirement that unqueried outcomes and scorer state be inaccessible. **No prohibited predictive use was found:** prior construction uses D only, and `predict` indexes labels only for R. Thus this supports a `LEAKAGE` annotation for prohibited accessibility, not a claim that EVAL labels influenced selection.

4. **Medium — Determinism verification covers only I predictions.**  
   [The recheck](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen010_cycle.py:296) reruns I and compares final probability dictionaries. It neither compares transcripts nor checks L, F, or the 20 random runs. It also does not reconstruct verification from sealed transcripts as original item 70 prescribes. Calling this “determinism exact” for the complete execution is unsupported. This is incomplete verification, **not demonstrated NONDETERMINISM**. The broader independent checks in this review cannot retroactively complete the frozen execution’s check.

5. **Medium — Recheck exclusion needs a defensible accounting boundary.**  
   The scheduled accounting reconciles exactly:

   | Component | Nodes |
   |---|---:|
   | DEV source + EVAL scorer releases | 2,500 |
   | Shared predictor transcripts | 600 |
   | Six policy candidates: 6 × 30 × 20 | 3,600 |
   | Six fixed candidates: 6 × 30 × 20 | 3,600 |
   | EVAL: 23 × 200 | 4,600 |
   | **Scheduled total** | **14,900** |

   Thus `dev_replay=7,200` correctly excludes the separately recorded 600 shared queries. However, the recheck appends another 200 `run_episode` steps and then deletes their charges. Exclusion is defensible for arithmetic verification of already sealed reveals; merely using cached labels does not exempt a fresh policy replay under items 56/58. The implementation does not clearly enforce that distinction. Counting those steps as replay attempts would yield **15,100**. The sealed 14,900 remains unchanged, with this qualification attached.

6. **Medium — Required query-attempt records are missing.**  
   [NODE_LOG](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen010_cycle.py:25) retains only `(kind, key)` in memory and is never archived. It lacks the required arm, episode, step, acquisition score/order position, returned class/failure, and charged cost. EVAL transcripts preserve identities and ordering, but DEV transcripts and complete attempt records are absent. Queries also provide the predictor with classes directly rather than recording the paired observation, including delta and Chronos scores, specified in item 14.

7. **Medium — Failure labeling is incomplete.**  
   [The executor](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen010_cycle.py:328) correctly rejects the performance gate but emits only `BELOW_QSTAR`. `MODEL_REGRESSION` also applies: for ACH-002958, gains are **−0.0004897092278697664 versus I** and **−0.001964353079759548 versus R**. The ledger acknowledges this, but the result’s failure array does not. The closeout must additionally retain the recorded `EXECUTION_FAILURE` and protocol/access annotations above. `NO_GAIN` does not apply because q is positive; `NO_UPDATE` does not apply because I was not selected.

8. **Medium — Model and seed reporting is incomplete under item 52.**  
   The result omits random per-model losses, explicit arm macro losses/model ranges, and random per-model seed ranges. Independently reproduced annotations are:

   | Arm | ACH-001418 | ACH-002958 | Model-macro loss |
   |---|---:|---:|---:|
   | I | 0.380555862 | 0.372627959 | 0.376591910 |
   | L | 0.379334403 | 0.373117668 | 0.376226036 |
   | F | 0.386755799 | 0.381317500 | 0.384036649 |
   | R, seed mean | 0.384092909 | 0.371153315 | 0.377623112 |

   Random seed macro losses range from **0.372115354 to 0.384397253**. Per-model seed ranges are **[0.375168103, 0.398179802]** and **[0.362207570, 0.383144723]**. These are descriptive computational ranges. Recomputed **q=0.00036587483141461784**, far below 0.020.

9. **Medium — Freezing and runtime evidence is incomplete.**  
   Only the all-DEV prior-summary hash is recorded for selected artifacts; there is no separately persisted pre-EVAL commitment binding theta, acquisition rule, summaries, and executor source together. Metadata hashes are available transitively through v8 and currently match, but the executor does not verify that chain. It also records or enforces no Python version. The available interpreter is **3.14.8**, whereas item 42 specifies **3.12**. Matching current shuffles does not establish that the original execution used 3.12.

10. **Medium — Integrity and failure handling are incomplete.**  
    The loader does not validate paired-record fields or linkage, check finite deltas, or enforce all partition subtotals. It classifies `Infinity` as +2 and `-Infinity` as −2; NaN raises an unlabeled exception. Duplicates are skipped while execution continues. Missing predictions would raise rather than receive original item 68’s loss-1 treatment. The present frozen data pass the independent checks, so these are executor defects without an observed numerical effect here.

11. **Medium — Shared cost amounts are not actually allocated per arm.**  
    [Host pricing](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/pgen010_cycle.py:344) reproduces the five receipt charges exactly: **$0.5581148 total**, comprising **$0.470178 sunk calls** and **$0.0879368 pgen010 pre-run review**; metered spend is $0. The frozen `shared_equally` mapping is followed, and no separate host call is established for the loader crash. However, attribution tags do not provide each arm’s allocation or define how the 20 random replicates participate in the allocation denominator. Equal query budgets therefore do not establish equal complete costs. This closeout remains outside the frozen schedule, as instructed.

12. **Low — Cost fallback definitions disagree and are not implemented fully.**  
    The SPEC names same-phase median imputation; `host_cost_estimate.py` uses the maximum receipt cost for matching phase and effort, otherwise campaign maximum. The executor implements neither events fallback nor imputation. All five required receipts contain usage, so this causes no observed pricing error.

13. **Low — “Near-tie degeneracy” understates exact equivalence.**  
    These are structural exact ties: predictor `(4,0,0)` with `(4,3,0)`; policy `L_W=L_V` and `L_U=L_UW=L_UV`; fixed `K0=K4` and `K2=K5`. With selected `wg=wh=0`, W and V are query-independent within each decision, so L selects canonical ascending queries. Tie-breaking is correct and all scheduled candidates are separately charged, but the selected acquisition supplies no adaptive query ordering.

No critical numerical corruption or demonstrated outcome-driven selection was found. The numerical failure is reliable; the claim of fully compliant execution is not.

PGEN010_CLOSEOUT: REJECT
PGEN010_CLOSEOUT_SCORE: 68