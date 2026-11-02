# Astra xhigh review round 2 — dispositions (score was 82/100)

| # | Sev | Disposition |
|---|---|---|
| H1 | High | FIXED: bootstrap rewritten — one model resample shared by calibration (weighted offset) and analysis; preprocessing mirrors main exactly (offset on unimputed data, fixed pre-offset imputation means); reference sets are the main estimator's corrected-data sets (978/5,027, asserted vs main JSON); identity replicate reproduces point flags on all 456 hits (recorded in boot JSON). New: slope 0.90 [0.82, 0.99]; per-rep medium fraction median 0.64 [0.49, 0.76]; 72% of hits freq ≥0.5. |
| M1 | Med | FIXED: LOO refits A and F per omission and calls flag_hits; actual minimum retention 93.54% (manuscript corrected from ≥94%). |
| M2 | Med | FIXED: validator rewritten to read ARCHIVED tables from the zip, round-trip hit sets by gene on both scales, archive-vs-generations flag identity, bootstrap numeric checks (identity flag, CI contains archived point slope, freq rows/bounds), tight Sanger targets (0.8025/0.6975 ±0.002); manifest = SHA-256 of all entries except VALIDATION.json itself (appended last; verified 0 mismatches after append). 33/33 checks. |
| M3 | Med | FIXED: release README headline (456/LSM7) and generations RELEASE_README (22 calibrators, 7 Humagne controls screen-level, symmetric rule + flag_fdr + HC3 + boot freq) synced; Fig1 format candidate own class (LSM7 annotated), formulation-family/medium-consistent labels; manuscript specifies ratio_A<0.25 in format rule; HPLM closing sentence now cross-system concordance. |
| L1 | Low | FIXED: F/D≥0.5 count 39→34; reference sets 978/5,027; headline prevalence 69%→70% (69.753%). |
| #1 partial | — | Figure/manuscript causal shorthand removed (see M3); "medium-consistent" throughout. |
| #2 partial | — | Resolved via H1. |
| #6 partial | — | Resolved via M3 (figure class + rule documentation). |
| #8 partial | — | HPLM sentence rewritten (concordance, not mechanism). |
| #12 partial | — | Resolved via M2/M3. |

Known unrelated flake: tests/test_tree_cpu.py::test_leader_exit_descendant_tracked
fails intermittently under full-suite load, passes in isolation (pre-existing,
process-timing test from the RSI era; untouched by this work).
