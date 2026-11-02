Independent **gpt-6.1-sol, high** review: **not ready for Lock2**. Scientific-only authorization is adequate.

Review remained read-only: no downloads, edits, archive inspection or real C outcome access. Independent execution used only synthetic arrays. The 60-test pass was verified from the ledger, not independently rerun.

**Verified foundations:** confirmatory207/mean_abs_delta/base_strength matches the contract. Frozen covariates reproduce exactly from Layer A. Cohort membership, donor mapping and library choices match the split: 148 models/144 donors, 133 minLib, 15 v1_1 and 13 alternates. TMOD→TMOD1 is confined to the sensitivity. Static inspection confirms space-delimited parsing, ascending ranks on both sides, donor nesting, null-calibrated sensitivity and the exact four-member Holm family. Production kernels match retained calibration evidence. Exposure logging precedes numerical outcome conversion.

G1 conditioning, AdherentMean provenance, uncertainty limitations and delta wording are preserved. Predictions are adequately registered qualitatively. Claim mapping avoids causal claims, broader equivalence and interpreting INCONCLUSIVE as absence. G2/C4/C8/C9/C13 remain unmet; SCIENTIFIC_RESULT_WITHOUT_RSI_EVIDENCE requires a qualifying independently reviewed result.

**Critical:** none identified.

1. **High — VERIFIED: invalid secondaries can receive significant Holm results.**  
   [src/external_eval.py:143](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:143) computes p despite invalid point/interval status; `:265` permits rejection. A synthetic vector containing 4,600 positive and 400 failed replicates produced p≈0.000435 and Holm-adjusted p≈0.001739 despite exceeding the frozen failure limit. `boot_p` also replaces the stated B denominator with the finite-replicate count.  
   **Fix:** invalid analyses must return null p and false rejection flags. Freeze the failed-replicate denominator rule, preserve all four family slots, and test excessive failures, invalid points and zero-width intervals.

2. **High — VERIFIED: required INCONCLUSIVE paths can crash after C consumption.**  
   [src/external_eval.py:137](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:137) reconstructs replicates after an invalid production result. With synthetic `L=base`, the kernel returned INCONCLUSIVE, but `analysis` raised `ValueError("degenerate rank residuals")`. Degenerate sample/reference orderings can also raise during extraction. Unguarded leave-one-model-out calculations at `:166` can prevent persistence of a completed primary.  
   **Fix:** emit structured invalid results, stop calculations with invalid prerequisites, and isolate stability failures from primary persistence. Retain each failure explicitly.

3. **High — VERIFIED: single execution is not concurrency-safe or durably committed.**  
   [src/external_eval.py:215](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:215) checks marker existence before `:218` writes it; two processes can both proceed. Start and final-result writes lack atomic, durable commitment.  
   **Fix:** acquire execution ownership atomically, fsync the start record before exposure, and commit results without overwriting existing artifacts. Preserve crash adjudication and prohibit silent reruns. Add concurrent-start and interrupted-write fixtures.

4. **High — VERIFIED: the supported CLI bypasses resource enforcement.**  
   [src/cli.py:38](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/cli.py:38) directly invokes evaluation without reservation, watchdog or timeout, contradicting the protocol’s promised bounded 600-second/2-GiB execution.  
   **Fix:** provide a bounded launcher with reserve-before-dispatch accounting, named allocation, RSS monitoring, timeout and reconciliation. Ensure direct invocation cannot silently bypass this execution contract.

5. **Medium — VERIFIED: mandatory commit coverage remains incomplete.**  
   [src/external_eval.py:52](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:52) now covers Layer-A raw files, groupings, composition, ledger and CLI. It does not require budget/launcher dependencies, resource/allocation configuration, numerical environment locks or authoritative scientific provenance bindings.  
   **Fix:** require the complete execution bundle, including `src/budget.py`, relevant configurations and dependency locks; bind contract, split/scope manifests, provenance, preparation code and review evidence. Frozen derived inputs protect current numerical inputs, but do not independently bind their derivation or governing interpretation.

6. **Medium — VERIFIED: accepted secondary exclusions are omitted.**  
   [src/external_eval.py:256](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:256) and `:258` attach exclusion lists only when the threshold is exceeded. Sensitivities accepting one to seven exclusions omit the promised model-level disclosure.  
   **Fix:** always report exclusions and analyzed model/donor counts for every sensitivity.

7. **Low — VERIFIED: access-history wording overstates the technical boundary.**  
   [src/lock_s_prep.py:78](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/lock_s_prep.py:78) transiently decodes/materializes all CSV fields, including LFC text. “Discarded unread” is technically inaccurate. Code and retained records provide no evidence of numerical conversion, inspection, persistence or outcome-driven decisions. The three preparation attempts have the stated dispositions.  
   **Fix:** append a clarification distinguishing transient text parsing from numerical outcome access; preserve historical records.

Resolve these findings and obtain independent re-review before commitment. The sanctioned route’s HTML stop is appropriate and supplies no G2 admission evidence.

LOCK_S_REVIEW_SCORE:78; READY_FOR_LOCK2:NO