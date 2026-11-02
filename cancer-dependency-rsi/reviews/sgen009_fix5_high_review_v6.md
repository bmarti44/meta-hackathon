The requested fixes hold: 80 targeted rejection probes passed, covering slash counts, `[NaN, NaN]`, `[,]`, malformed `label≈` secondaries, and repeated punctuation. Three enumeration gaps remain:

- **P2 — FDR counts still skip malformed occurrences.** Appending `(999/7 and 8 FDR` or `(7 and 999/8 FDR` to an otherwise passing input leaves every claim passing. Capture complete tokens for each labeled occurrence before validating them. [sgen009_trace.py:119](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:119)

- **P2 — Model counts depend on preceding whitespace.** `148/2 Sanger organoid models` at the beginning of a line is omitted; the same assertion following a space is rejected. The literal leading space prevents complete enumeration across line breaks. [sgen009_trace.py:110](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:110)

- **P2 — Malformed LOMO ranges disappear.** Appending `(-0.999oops...-0.888oops)` leaves every claim passing because neither endpoint regex matches. Enumerate complete range occurrences and validate both endpoints together. [sgen009_trace.py:104](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen009_trace.py:104)

Validation used in-memory inputs with expectations from `traceability_v17.json`. No files changed.

SGEN009_FIX5_SCORE: 91