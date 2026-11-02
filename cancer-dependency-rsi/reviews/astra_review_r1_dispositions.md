# Astra xhigh review round 1 — dispositions (score was 68/100)

All 12 issues independently spot-verified against artifacts/code before fixing
(verification log: session 2026-10-30; every numeric claim reproduced).

| # | Sev | Disposition |
|---|---|---|
| 1 | High | FIXED (language+analysis): flags renamed "medium-consistent" in text; formulation-family wording; categorical in-vivo claim removed; common-support sensitivity added (6 lineages/38 domes: slope 0.89, median ratio 0.89, 90% ratio≥0.5). Residual confounding stated as limitation. |
| 2 | High | FIXED: HC3 SEs shipped + HC3 flag sensitivity (82%/75%); joint bootstrap over calibration+analysis models (B=150): slope 0.90 [0.81,0.98], per-hit flag frequencies released (71% ≥0.5). Fractions now reported with these ranges. |
| 3 | High | FIXED (language): ribosomal relative weakening = finding; depletion kinetics demoted to testable hypothesis; cross-matrix processing caveat incl. nonessential medians; Chronos-rescaling tautology stated. |
| 4 | Med | FIXED (code): Humagne sensitivity now screen-filtered → 7 FBS controls, corr 0.78, slope 0.83. |
| 5 | Med | FIXED (code): reserved excluded before offset/filter/imputation (22 dev duals); held-out uses disjoint reserved FBS baseline (78): slope 0.96, r 0.97, 100% sign. |
| 6 | Med | FIXED: symmetric nominal-p primary rule (+ ratio_F CI) → 1 format candidate (LSM7); strict-FDR variant released as flag_fdr (0 format); "none detected at 5% FDR" wording; Neiswender 7 format genes incl ITGB1 acknowledged (verified in paper text). |
| 7 | Med | FIXED: title scoped to "reproduced"; unconditional (47%/52%) and conditional (87%/86%) fractions both reported; Sanger 5/16 in-table stated. |
| 8 | Med | FIXED: "relatively more essential in RPMI"; direction-separated enrichment (gains-only OR 4.38, prevalence 4.21, p=0.007); OR labeled; dialyzed-serum caveat (not an LDL-removal reversal). |
| 9 | Med | FIXED (code+text): t5 collapsed within model (178 profiles→162); medians 0.802/0.698; wording = depletion-call prevalence, not threshold robustness. |
| 10 | Med | FIXED: direction-split panel counts (ribosomal 13 losses/2 gains of 38; spliceosome 5/2 of 35 — updated on regenerated table); low-ratio published gains now list COASY/LSM7/UTP4 too; "medium-consistent" counts exact (5 medium + 3 unresolved); SCAP failing criterion = nominal A significance (p=0.057). |
| 11 | Low | FIXED: export %.6g; ATG14 round-trip preserved (validator re-derives hit counts from exported CSV). |
| 12 | Low | FIXED: release README complete run order + inputs + layout note; sanger_essdepth.py added as generator for sanger_essdepth_v1.json. |

New headline numbers (v2r2, normalized): 249 gains / 207 losses; medium-consistent
85.9%/83.6% (HC3 81.5%/75.4%); format candidates 1 symmetric / 0 FDR;
slopes A 0.84/0.86, F 0.18/0.17; bootstrap slope CI [0.81,0.98];
held-out disjoint slope 0.96. Changes vs r1-reviewed version are from
dev-only calibration (22 vs 27 models) and the symmetric format rule.
