The rejection guarantee remains incomplete. Each corruption below independently produced `main()` exit **0** and **`pass: true`**.

1. **HIGH — Counts still escape complete-token validation.** [sgen009_trace.py:100](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:100) accepts `148/2 Sanger organoid models` and `/ 142/2 patients` by skipping those occurrences. It also accepts `999/250 panel genes` by extracting the suffix `250`. Capture complete digit-leading tokens in labeled contexts, then validate them.

2. **HIGH — Nonnumeric intervals disappear.** [sgen009_trace.py:82](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:82) ignores the Results interval after substitution with `[NaN, NaN]` or `[,]`. The valid abstract interval keeps the claim passing. Require every interval assertion to parse.

3. **HIGH — Malformed secondary delimiters hide additional assertions.** [sgen009_trace.py:89](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:89) accepts adding `null-calibrated≈ −0.999` alongside the existing correct assertion. The malformed occurrence is never captured. Enumerate label occurrences before validating their syntax and complete tokens.

4. **MEDIUM — Punctuation stripping masks token corruption.** [sgen009_trace.py:62](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:62) accepts abstract `ρ = −0.146,,` and `ρ = −0.146,);`. Secondary `null-calibrated −0.209,,,` likewise passes. Unrestricted `rstrip()` alters malformed tokens before `NUM` fullmatching.

Verified: in-memory regeneration exactly matches retained v15; all ten built-in fixtures reject; all three artifact and five inventory hashes match. The reproduction-report digest and figure hashes match their citations; the previous conflicting figure citation is corrected.

Review remained read-only: manuscript reads and report writes were intercepted in memory. Full reproduction runners were not executed.

SGEN009_FIX4_SCORE: 87