**TV is sound; the partial-Spearman envelope is not established mathematically.** The recorded `ENVELOPE_TOO_WIDE` is nevertheless a defensible failure to certify robustness. No patient-level CI, BOUND decision, or inferential gate was silently upgraded.

I reproduced TV = **0.0136932707**, all **12 atlas CSVs** byte-for-byte in memory, and identical v1 outputs using both estimator versions. The six focused tests passed in both the project environment and retained `/tmp/cdrsi_fresh` environment. Review remained read-only.

1. **High — Unsupported partial-Spearman bound and proof branch.** [src/sgen004_envelope.py:63](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen004_envelope.py:63) divides rank movement by the ordinary rank norm, then applies the result to partial Spearman and permits `ENVELOPE_PROVES_POINT_ROBUSTNESS`. Residualization changes the denominator; unchanged covariates do not preserve residual norms. Calling this a screen does not establish conservativeness.

   **Fix:** derive a bound for normalized rank residuals, handle degenerate residuals, and disable the proof verdict until validated. A valid generic normalization bound here is approximately **1.842**, still vacuous. Independently, perturbations within the TV coordinate box yield partial correlations **−0.3194** and **+0.0234**, supporting `ENVELOPE_TOO_WIDE` for that relaxed screen. These are not demonstrated patient-feasible outcomes.

2. **Medium — Frozen hashes are merged across stages.** [src/sgen005_upstream.py:56](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen005_upstream.py:56) overwrites v1’s estimator hash with v2’s. Consequently, `frozen_substitutions: []` does not mean every stage used its frozen code. `upstream_nuance.json` discloses this honestly, and I verified output equivalence. Separately, [_copy:35](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen005_upstream.py:35) trusts a frozen artifact’s filename without hashing its contents.

   **Fix:** materialize dependencies per stage, verify copied bytes against that stage’s hashes, and record actual hashes and substitutions in the report. The retained frozen estimator currently verifies correctly.

3. **Medium — Promised runner checks remain absent.** [generations/sgen005/SPEC.md:7](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen005/SPEC.md:7) requires executed C10 and eligibility checks. The delivered runner executes atlas builders and CSV comparisons only. The specified synthetic-use audit is also not delivered as an auditable inventory.

   **Fix:** implement these components with explicit acceptance criteria and results. Include them in overall success, and provide an unused report-path argument for repeat execution while preserving exclusive creation.

4. **Medium — Fresh-environment completion is narrower than the mandate.** [fresh_env_report_v1.json:3](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen005/fresh_env_report_v1.json:3) reports the older sgen002 component runner plus six tests. That runner excludes upstream rebuilding, C10 execution, and eligibility execution. Same-host, copied-data limitations are stated honestly, but the full attainable package was not reproduced there. The historical sync’s 900-second bound lacks retained command/exit/timing evidence.

   **Fix:** retain structured installation evidence and execute the completed upstream/component runner under the fresh interpreter, reporting each component separately.

5. **Medium — Excess-body detection exceeds the byte reservation.** [src/zipfetch.py:59](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/zipfetch.py:59) reads `want + 1` after reserving `want`. My probe consumed five bytes with a four-byte ceiling before rejecting the response. Failed attempts correctly consume request allowance.

   **Fix:** reserve the detection byte before dispatch and record failed consumption. Add exact-boundary and failed-attempt regression tests.

6. **Medium — Inflation and compressed-stream consumption remain unchecked.** [src/zipfetch.py:134](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/zipfetch.py:134) decompresses without an output cap, then checks size. A probe reserved **8,352 transferred bytes** while allocating **4 MiB** of output. Another archive passed despite trailing junk inside its declared compressed region.

   **Fix:** bound decompressed output independently, reject oversized declarations before inflation, and require complete stream consumption using `decompressobj` checks. Add regression cases.

The post-90 metadata fixes worked in independent probes: nonzero starting disks, inconsistent local CRC/sizes, mismatched raw filenames, encryption, and ZIP64 sentinels were rejected. The four committed zipfetch tests do not cover most of those hardening branches.

| Gate | Updated snapshot |
|---|---|
| **C6** | **PARTIAL** — novelty component supported; patient-level inference unresolved. The envelope supplies no upgrade. |
| **C10** | **PARTIAL** — archived checks support qualified conclusions; patient-weighted uncertainty and decision robustness remain unverified. |
| **C11** | **PARTIAL** — generated v1 feeds v2 correctly; v1 failure preserved; atlas output equivalence and fresh component tests verified. Stage-specific frozen execution, runner checks, patient intervals, and policy comparison remain incomplete. |

SGEN45_REVIEW_SCORE: 86; C11:PARTIAL