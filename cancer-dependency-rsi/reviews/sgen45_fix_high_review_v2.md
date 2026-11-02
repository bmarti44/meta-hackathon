**The fixes improve safety and reproducibility, but the HIGH envelope issue remains unresolved.** No inferential gate was upgraded.

Read-only verification reproduced TV **0.0136932707**, all **12 atlas CSVs** in memory under the retained fresh interpreter, and eligibility totals **250 patients / 251 lines / 810 files**. All **six ZIP tests passed in both environments**. Independent probes confirmed rejection of excess response bytes, excessive inflation, oversized declarations, and trailing compressed-stream junk. Frozen-content hashing, `--report`, exclusive report creation, and the disabled proof verdict are present.

1. **HIGH — Residual normalization remains unaccounted for.** [src/sgen004_envelope.py:71](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen004_envelope.py:71) uses `delta_norm / resid_norm`. Projection bounds residual movement, but correlation also renormalizes the perturbed residual. The claimed generic inequality fails: a perturbation within that residual ball changes correlation by **1.00003**, exceeding **0.92089**. This is a counterexample to the derivation, not a demonstrated patient-feasible perturbation.

   **Fix:** use a proved normalization bound, such as `min(2, 2*delta_norm/resid_norm)`—here **1.84178**—and handle degenerate residuals explicitly. Retain the disabled proof verdict. `ENVELOPE_TOO_WIDE` remains a defensible failure to certify.

2. **MEDIUM — Stage-specific frozen execution is still missing.** [src/sgen005_upstream.py:58](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen005_upstream.py:58) still merges manifests by path. V1 requires estimator hash `19dcaa…`; the runner selects v2’s `b0b3bc…`. Consequently, v4’s empty substitution list does not establish frozen execution for every stage. The historical artifact verifies correctly, and both versions reproduce identical v1 CSVs.

   **Fix:** materialize dependencies per stage and report expected/actual hashes, stage identity, and substitutions.

3. **MEDIUM — Component success exceeds the executed checks.** [src/sgen005_upstream.py:95](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen005_upstream.py:95) checks C10 numbers anywhere in the document; an incorrect primary row passes if the expected numbers remain in a footer. Eligibility checks three stored totals rather than recomputing exclusions. The synthetic audit contributes only a pathname.

   **Fix:** validate the intended C10 row and fields, recompute eligibility from retained detailed inputs, and validate the audit and its references. Include each result in overall success.

4. **MEDIUM — The inflation regression bypasses decompression.** [tests/test_zipfetch.py:118](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_zipfetch.py:118) changes only directory-side metadata. Local-header consistency rejects it first; instrumentation recorded **zero `decompressobj` calls**. Despite its name, the test supplies no trailing junk and never exercises the 64 MiB declaration cap.

   **Fix:** construct internally consistent malformed archives that reach inflation, and add distinct trailing-junk, declaration-cap, and failed-body budget cases. Independent probes support the implementation, but these committed regressions do not protect it.

5. **LOW — Synthetic-audit evidence references are broken.** [generations/sgen005/synthetic_use_audit.json:5](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen005/synthetic_use_audit.json:5) references nonexistent `lock_s/prelock_validation_v1.json` and absent `status.json:synthetic_calibration`.

   **Fix:** reference the retained `diagnostics/donor_calibration_v2/` results and fixture manifest, plus the actual status fields.

6. **LOW — Fresh installation provenance remains incomplete.** [generations/sgen005/fresh_env_report_v2.json:2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen005/fresh_env_report_v2.json:2) summarizes `uv sync --locked` without retained command, exit, timeout, or installation timing evidence. The fresh environment, matching lockfile/code, and upstream result artifact exist; my fresh-interpreter reproduction supports the reported output equivalence.

   **Fix:** retain structured installation and runner receipts, including interpreter and lockfile identity.

C6 and C10 remain **PARTIAL**; patient-level inference and policy comparison remain unavailable.

SGEN45_FIX_SCORE: 90; C11:PARTIAL