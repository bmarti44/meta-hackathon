Improved from 84, but still below the ≥90 acceptance bar.

1. **HIGH — Secondary estimates still accept numeric prefixes.** [sgen009_trace.py:83](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:83) accepts `null-calibrated −0.209E3`, `−0.209e+3`, and `−0.209oops` as `−0.209`. Each corruption produced actual `main()` exit 0 and `pass: true`. Enumerate labeled assertions and validate their complete tokens.

2. **HIGH — Count patterns can skip corrupted occurrences.** [sgen009_trace.py:92](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:92) still permits incorrect assertions when their syntax escapes the regex. Independently changing the abstract to `(1,480 models,`, limitations to `**1,420 patients**`, or the abstract panel to `fixed 2.07e3-gene panel` produced exit 0 and `pass: true`. Other correct occurrences satisfy the checker. Capture every contextual assertion before validating its full numeric token.

3. **HIGH — Malformed primary assertions can disappear from validation.** [sgen009_trace.py:53](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:53) ignores the Results estimate after changing it to `ρ ≈ −0.999`. The bracket parser likewise ignores a Results interval changed to `[−0.999, −0.888)` or `[NaN, NaN]`. Each independently produced exit 0 and `pass: true`. Require each primary assertion to parse successfully, including its delimiter syntax.

4. **MEDIUM — The conflicting reproduction citation remains.** [reproducibility_report.md:12](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reproducibility_report.md:12) still names `fresh_env_evidence_v3.json` as the figure report of record. It contains no figure hash and records a different sgen002 digest. The new line 15 correctly cites sgen002 v3 with its matching hash; replace the stale citation.

Verified: all six built-in fixtures reject; ordinary abstract count corruptions, integer/no-space/exponent rho corruptions, integer/reversed intervals, swapped secondaries, atlas 70/80, and both LOMO extrema corruptions reject. All five inventory, three artifact, and five atlas input/code hashes match. Atlas inventory entries identify runner and manifest. In-memory regeneration exactly matches retained v10. The packet uses one `mktemp` directory and four distinct report paths.

Review was read-only; manuscript substitutions and report writes were intercepted in memory. Full reproduction runners were not executed.

SGEN009_FIX3_SCORE: 87