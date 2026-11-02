Read-only review: I reproduced `evidence_report_v2.json` in memory, excluding timing, but found five issues.

1. **High — C10 accepts contradictory decision fields.** [src/sgen008_checks.py:53](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen008_checks.py:53) checks only whether the magnitude field contains `BOUND`. Replacing it with `**no (NOT_BOUND)**` or `**no (BOUND rejected)**` still passes. Changing the sign field to `no` also passes.
   
   **Fix:** parse and compare affirmative sign/magnitude decisions and the exact decision token against the locked result; add negative fixtures for these contradictions.

2. **Medium — C-patient completeness does not affect eligibility success.** [src/sgen008_checks.py:96](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen008_checks.py:96) omits the required 142 C patients from its acceptance condition. Removing the first C model produces 141 patients and still passes; an empty cohort produces zero and still passes.
   
   **Fix:** require complete cohort membership and identity resolution, plus exactly 142 unique patients. Add truncated/empty-cohort rejection fixtures.

3. **Medium — Exposure exclusions are copied constants.** [src/sgen008_checks.py:88](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen008_checks.py:88) hard-codes Broad7. Tracing input reads confirms eligibility never opens the split manifest required by SPEC. The constant currently matches that manifest, but the check cannot detect divergence.
   
   **Fix:** derive exposed model IDs from the authoritative split manifest, validate cohort consistency, and record input hashes.

4. **High — Fresh evidence does not establish the completed frozen battery.** [evidence_report_v2.json:31](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen008/evidence_report_v2.json:31) says upstream/point/figure/OLS runners were invoked separately in fresh evidence; [fresh_env_evidence_v1.json:2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen008/fresh_env_evidence_v1.json:2) records only the sgen008 checker. The retained fresh upstream script also predates the current per-stage frozen-code verification. Neither cited reproduction runner executes OLS.
   
   **Fix:** execute the completed component battery under the fresh interpreter and retain individual commands, source/report hashes, results, and aggregate acceptance.

5. **Medium — Structured installation evidence remains incomplete.** [fresh_env_evidence_v1.json:2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen008/fresh_env_evidence_v1.json:2) lacks installation exit/timing evidence and an interpreter hash required by SPEC. Attempt records remain outside the generation directory.
   
   **Fix:** retain installation and execution records separately, including elapsed times, interpreter identity/hash, logs, and both failed/successful reports.

Verified positives: swapped endpoints, duplicate Primary rows, and the supplied footer decoy are rejected. Original-input totals reproduce **252 matched lines / 251 patients / 250 eligible patients / 251 eligible lines / 810 files**, with **142 C patients**. The calibration fixture manifest is authentic: specification/array hashes match the retained results, whose records confirm **95/100** and **97/100** coverage. Historical frozen code is retained where current code differs. Diagnostic-only qualifications remain intact.

The first fresh attempt is honestly preserved at `/tmp/cdrsi_fresh/generations/sgen008/fresh_evidence_report.json` with `implemented_pass: false`; the successful second report is separate. Interval/policy components remain explicitly unavailable; no label upgrade is warranted.

SGEN008_SCORE: 80