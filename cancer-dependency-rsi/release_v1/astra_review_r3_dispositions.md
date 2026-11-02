# Astra xhigh review round 3 — dispositions (score was 89/100)

| # | Sev | Disposition |
|---|---|---|
| 1 | Med | FIXED: `weighted_offset()` uses nansum with gene-specific denominators (zero fallback); identity check now routes through the weighted path with all-one dual weights and still reproduces point flags on all 456 hits. MAU2 frequency 0.0067 → **0.48** (matches reviewer's corrected 72/150); slope median/CI unchanged to 3 dp (0.898 [0.816, 0.988]); freq≥0.5 = 329/456. Regression test added (`test_weighted_offset_ignores_missing_pairs`, failed before fix). |
| 2 | Med | FIXED: wet-lab proposal + cover email synchronized (84–86% medium-consistent, LSM7/none-at-FDR, hedged transfer language, curated ribosomal description, "these are consistency classifications" caveat in proposal). Internal finding review labeled SUPERSEDED (source + release copy). |
| 3 | Low | FIXED: PDF caption (render_pdf.py) uses formulation-family wording; generations RELEASE_README F_dome definition fixed; manuscript "fixed medium" (0 instances left) and "medium-created" (0 left) replaced. PDF regenerated (33/33 validation incl. archived-content checks). |

Tests: 105 passed, 1 skipped (incl. 6 medium-attribution tests).
