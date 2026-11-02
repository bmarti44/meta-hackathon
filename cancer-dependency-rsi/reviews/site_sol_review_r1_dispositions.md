# Site sol review r1 (76/100) — dispositions

All issues independently re-verified locally (MAPK11 flag-0 q=4.2e-36;
7,569 flag-0 genes with q<0.01; HSD17B7/AIRIM flag=2 in top list;
STK38L rA=-34338.1; A/D range 0.500-1.923; contrast 3.33/3.86/3.27:1).

HIGH
- Denominator: FIXED. Hero + OG now read "85% of the 456 differential
  dependencies in our reanalysis".
- Causal language: FIXED. Ch1 headline "Shape changed. So did supper.";
  "observational control"; ch2/scatter use A=D + "medium-consistency
  criteria — an observational consistency label, not causal proof";
  Findings §1 retitled and defines the criteria operationally.
- Preprint status: FIXED. Both copyable citations say "Unpublished draft
  technical note … not yet posted as a preprint; draft PDF contains
  author placeholders"; Downloads labels the PDF a draft.
- Flag-zero label: FIXED. "Below hit threshold"; verdict distinguishes
  significant-but-|Δ|<0.25 from non-significant; fmtQ avoids "q=0.00".

MEDIUM
- Detail off-viewport: FIXED. select() scrolls when the panel is out of
  view; incoming #gene= links scroll to the detail.
- Missing code download: FIXED. release_v1.zip (code + review trail)
  published to assets + Downloads; gene detail links the primary CSV.
- Mouse-only controls: FIXED. Gene names are buttons; sortable headers
  contain buttons and carry aria-sort; rail visibility:hidden on paper.
- Contrast: FIXED. Hot CTA + ticker use #c93318 (5.29:1); unresolved
  badge #8a5f10 (5.64:1); below-threshold badge #6e6249 (5.99:1).
- Fallbacks: FIXED. WebGL failure shows fig1 (inverted, dimmed) and
  hides "live data" caption; reduced-motion now also disables mouse
  repulsion and chapter translations (fades only; morph remains purely
  scroll-driven, no autonomous motion).
- Picking mismatch: FIXED. CPU mirror replicates shader idle drift;
  repulsion softened (0.24, r=0.85) and off under reduced motion; pick
  radius 30px -> 44px; highlight ring uses the same synced mirror.

LOW
- Apex multiValue query params: FIXED + function republished.
- Clipboard false success: FIXED (execCommand result checked; prompt
  fallback with the text).
- top_medium_gains pollution: FIXED in build_site_data.py (filter
  flag==medium_attributable); stats.json rebuilt, genes.json byte-identical
  (md5 ae34708d…). Regression tests: tests/test_site_data.py (4 passed).
- rA sort sign: FIXED (signed ordering for rA and bf).
- Render-behind-paper: FIXED. Ticker returns early in paper mode;
  highlight ring computes a single point instead of 17,525 per frame.
