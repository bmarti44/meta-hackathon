**Code/evidence integrity: 95/100. G2 remains FAIL.** Five code defects are resolved. Withdrawing the contradictory comparison design safely prevents its use, but leaves the original freeze obligation open. No critical implementation issue was found.

I independently ran **34 tests: all passed in 5.20 seconds**. Eighteen tests requiring temporary files were deselected under the read-only filesystem; the ledger retains the reported **52-test pass in 7.47 seconds**. Additional in-memory probes exercised timeout boundaries, evidence domains, resume integrity, extraction behavior, and current evaluator input guards. No edits, Sanger outcome access, downloads, provider changes, pilot, generation, or external evaluation occurred.

Each prior readiness issue:

1. **Medium — scientific timeout: RESOLVED.**  
   [budget.py:58](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/budget.py:58) enforces the scientific ceiling for CPU-heavy jobs before reservation or dispatch. Independent probes accepted 600 seconds and rejected 601 and 1,200 seconds, including through `run_bounded()`. The host reasoning allowance did not bypass this check. An exact named scientific allowance worked only when explicitly present. The new regression is meaningful, though its five-second fixture alone does not establish the production 600-second boundary; the independent probes do.

2. **Medium — evidence study/evaluator compatibility: RESOLVED.**  
   [candidates.py:67](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/candidates.py:67) checks both identities for evidence citations. The regression preserves a legal parent while adding foreign evidence. Independent probes additionally rejected study-only mismatches, evaluator-only mismatches, and missing identities. This verifies the intended OR condition beyond the test’s jointly mismatched fixture.

3. **Medium — contradictory policy comparison: PARTIAL.**  
   [contract.json:97](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/contract.json:97) explicitly makes comparison nonexecutable, with null quality and threshold; [episodes.json:66](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/config/episodes.json:66) prohibits threshold construction and policy decisions. Historical contract and episode bytes are retained and hash-verified. **Withdrawal resolves the immediate misuse risk; it does not resolve the scientific design.** Panel definitions, comparison population/support, baseline procedures, seeds, strongest-baseline interval construction, precision feasibility, and resource matching still require a coherent replacement before freeze.

4. **Low — zero-width decision intervals: RESOLVED.**  
   [confirmatory_estimand.py:48](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/confirmatory_estimand.py:48) rejects `lo >= hi`. All three original zero-width fixtures now return INCONCLUSIVE. Executing the retained old helper reproduced NEGATIVE, BOUND, and SIGNAL, confirming that the regression targets the original defect. The production kernel already rejected nonpositive widths.

5. **Low — raw-scale degeneracy threshold: RESOLVED.**  
   [confirmatory_estimand.py:27](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/confirmatory_estimand.py:27) checks rank variation instead of raw standard deviation. The new tiny-scale regression is effective: retained old extraction rejects it. Independent tied-rank and unequal-donor-group probes preserved profiles at scales `1e-14`, `1e-100`, and `1e100`; constant orderings still failed closed.

6. **Low — model-call resume identity/response integrity: RESOLVED.**  
   [model_call.py:17](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/model_call.py:17) records model, effort, phase, terminal flag, timeout, sandbox, interface, binary, prompt hash, and resolved output identity. Resume verifies retained response bytes. Independent probes rejected changed effort, phase, terminal flag, timeout, binary, prompt, altered/missing response, missing response hash, and legacy incomplete identity. Matching successful and failed receipts reused without reservation or redispatch.

**Additional Low issue — current resume status is stale.** [status.json:21](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/status.json:21) still lists model initialization and memory enforcement as current blockers; it reports zero completed responses and an earlier verification state. These conflict with retained successful consultation/review evidence, the RSS-watchdog implementation, and subsequent tests. Because `cli.py resume` renders this file, this is an operational evidence-navigation defect. It does not authorize a gate bypass.

The frozen diagnostic evidence remains intact. Current `donor_kernel.py` exactly matches v2’s `725d3eac…` hash; `estimators.py` and `donor_calibration.py` also match. Only extraction changed, by the two reviewed helper fixes, and its frozen old bytes remain content-addressed. All 14 retained content-addressed artifacts verified. Both fixture-array hashes match, all 200 dataset records remain identical between v1/v2, and seeds and acceptance thresholds are unchanged. V1 remains FAIL; v2 remains PASS, with 95/100 null and 97/100 nonzero-target coverage. **No full diagnostic rerun was performed.** This remains an algorithmic screen, not biological or nominal-coverage certification.

The original G2 source findings remain binding. Current v4 independently rejected missing/duplicate membership and nonfinite scores, targets, and adjustment inputs while retaining null q. Retired scoring code supplies no admission evidence. Before execution, remaining obligations include:

- **High, UNRESOLVED:** obtain an independently reviewed, meaningful admissible policy task and useful fixed quality endpoint, or follow the prescribed unmet-gate terminal process.
- Complete the replacement comparison specification and final hash bundle. Broad grouping alternatives exist, but their selected execution/integration must be frozen.
- Complete production-runner resume, hidden-outcome invariance, exact-context/common-support replay, full memo reconstruction/charging, and guarded external-access checks at their named gates.
- Preserve independent reserved biological evidence and material host-cost accounting requirements for C9; atlas-component reproduction does not satisfy full C11 campaign reproduction.

The score assesses code/evidence integrity only. It cannot waive the high G2 blocker or grant Lock1.

CODE_INTEGRITY_SCORE:95; G2:FAIL