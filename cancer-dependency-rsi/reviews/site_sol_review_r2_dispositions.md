# Site sol review r2 (84/100) — dispositions

Verified locally: Broad gains 135/285 medium-consistent, losses 131/252,
combined 266/537 (49.5%); 34 hits with F/D>=0.5. N1 verified in headless
Chromium: bare root stays at scrollY=0 with no hash rewrite; #gene=ITGB1
lands scrolled on the ITGB1 detail.

- Denominator (partial): Findings §2 now reads "published gains present
  in our audit: 47% (135/285) — 50% (266/537) counting gains and losses".
- Causal wording (partial, high): ch3 headline "points to the dome";
  hero "watch what tracks the medium"; timeline "food signal vs shape
  signal"; F relabelled "Δ dome vs flat" (table) / "Δ dome vs adherent"
  (detail). Guarded by tests/test_site_data.py::test_causal_phrases_stay_out.
- Contrast (partial): .btn.primary:hover now #b02e12 (6.47:1).
- Fallbacks (partial): no-WebGL path rewrites the hover instruction
  (.gl-note) to point at the explorer; reduced-motion formations now
  snap per chapter (morphCur = round(target)) — no animated flight.
- Picking (partial): CPU mirror now replicates shader exactly — morph,
  intro scale/z-offset, idle drift, and mouse repulsion (same smoothstep
  approximation, same 0.24 strength), for both picking and highlight.
- N1 (medium regression): select() takes scroll true/false/"never" plus
  setHash; bare-root init selects SQLE with "never" + no hash rewrite.
- N2 (low): aria-sort/arrow/caption derived from the comparator's real
  direction per column (g/f ascending at dir=1; strength/signed columns
  descending at dir=1).
- N3 (low): header re-render restores focus to the replacement button
  when the removed one held it.
- N4 (low): render suspension only once paper fully covers the viewport
  (paper top <= 0); body cursor cleared on entering paper mode.
