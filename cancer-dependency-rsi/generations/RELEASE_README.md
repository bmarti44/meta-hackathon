# Release: medium-attribution tables (GOAL v4 deliverable 1/4)

Per-gene decomposition of organoid-vs-2D differential CRISPR dependencies
(DepMap 26Q3) into medium / format / unresolved. Development patients;
held-out-patient confirmation in the `*_heldout_*` files.

## Files
- `generations/medium_attribution_v2_norm.csv` — primary table (dynamic-range-normalized Chronos)
- `generations/medium_attribution_v2_raw.csv` — raw Chronos scale
- `generations/medium_attribution_v2_heldout_{norm,raw}.csv` — reserved-patient contrasts
- `generations/medium_attribution_v2.json`, `..._heldout.json` — run summaries (ns, slopes, fractions, published-catalogue joins)
- Code: `src/medium_attribution_v2.py`, `src/medium_attribution_v2_heldout.py` (v1: `src/medium_attribution.py`)
- Manuscript: `manuscript/manuscript_draft_v2.md`; wet-lab proposal: `manuscript/wetlab_proposal_v1.md`

## Columns (one row per gene)
| column | meaning |
|---|---|
| `D_org` | dome + organoid medium vs adherent FBS 2D, lineage-adjusted Δ (negative = stronger dependency in organoids) |
| `A_adh` | adherent + organoid medium vs FBS 2D (formulation family, no dome) |
| `F_dome` | dome vs adherent within the organoid formulation family (individual formulations differ) |
| `S_tsm` | CNS Tumor-Stem-Media vs FBS (unrelated serum-free context) |
| `D_org_humagne_only` | D from Humagne-CD screens only, filtered at screen level before aggregation (sensitivity; 7 FBS models — underpowered) |
| `*_se`, `*_p`, `*_q` | standard error, p-value, BH q per contrast |
| `ratio_A`, `ratio_A_lo/hi` | A/D reproduction ratio with 90% delta-method CI |
| `ratio_F` | F/D ratio |
| `flag` | `medium_attributable` / `format_candidate` / `unresolved` / `not_a_hit` |
| `serumfree_support` | S same sign as D |

Hit rule: `D_org_q < 0.01` and `|D_org| ≥ 0.25`. Primary `flag` (symmetric
nominal-p): medium = same-sign A, `ratio_A ≥ 0.5`, `A_adh_p < 0.05`,
`ratio_A_lo > 0`, F not dominant by the mirror criteria; format = same-sign F,
`F_dome_p < 0.05`, `ratio_F ≥ 0.5`, `ratio_F_lo > 0`, `ratio_A < 0.25`.
`flag_fdr` = strict variant requiring `F_dome_q < 0.05` for format evidence.
`*_se_hc3` columns give HC3 robust SEs. `medium_attribution_v2_boot_freq.csv`
gives per-hit bootstrap medium-flag frequencies (joint calibration+analysis
resampling, B=150).

## Caveats
A_adh rests on 9 models (mixed organoid formulations); library bias removed
via a 22-model development-only Avana–Humagne-CD offset; CPD/doublings are recorded for 1 of
1,241 screens, so no per-doubling correction is possible in 26Q3.

## Sanger-side files (deliverables 2-3)
- `generations/sanger_direct_check_v3.json` — within-model percentiles, organoid table 6 vs 930 2D lines (code `src/sanger_direct_check3.py`; v1/v2 superseded — wrong matrix).
- `generations/sanger_essdepth_v1.json` — reference-essential depth per assay (0.63x compression in Sanger organoids).
