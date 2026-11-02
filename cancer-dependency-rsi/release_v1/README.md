# Release v1 — medium attribution of organoid dependency catalogues

Companion bundle for `manuscript_draft_v2.md` (GOAL v4 deliverables 1–4).
Column definitions and flag rules: see `../generations/RELEASE_README.md`
in the repo, or Methods in the manuscript.

## Contents
- `manuscript_draft_v2.md`, `wetlab_proposal_v1.md`, `goal_v4_finding_review_v1.md`
- `figures/` — fig1 attribution scatters, fig2 weakening (curated BAGEL sets), fig3 catalogue fractions
- `tables/` — per-gene attribution (raw + normalized), held-out contrasts, survivor candidates, run-summary JSONs (incl. LOO robustness, Sanger percentile/depth checks, curated panels)
- `code/` — analysis scripts (run from the repo root `cancer-dependency-rsi/`)

## Inputs needed to reproduce (not redistributed here)
From DepMap 26Q3 (place as in repo): `~/Downloads/ScreenGeneEffect.csv`;
`data/Model.csv`, `data/ModelCondition.csv`, `data/ScreenSequenceMap.csv`,
`data/passports_model_list_20260921.csv`, `data/sequester_patients_v1.json`.
Broad figshare: `data/raw/broad_figshare/organoids_vs_2d_gene_dependency_tests_full.csv`.
Sanger: `data/raw/sanger_supp/supplementary_table_4_revision.xlsx`,
`data/raw/sanger_figshare/{S2_Supplementary_Tables.zip, 07_EssMatrix_bDepletionsB2.Rdata, control-genes_organoids.csv, data_covariates_ALL-organoids.csv}`,
`data/quarantine/07_EssMatrix_qnorm_corrected_logFCs.RData`.

## Run order
Layout: `code/` here contains copies of the repo's `src/` scripts. To run,
place them in `cancer-dependency-rsi/src/` (scripts resolve the repo root
from their own path and expect `data/`, `generations/` siblings), then from
the repo root:
```
.venv/bin/python src/medium_attribution_v2.py
.venv/bin/python src/medium_attribution_v2_heldout.py
.venv/bin/python src/medium_attribution_v2_boot.py
.venv/bin/python src/medium_attribution_v2_loo.py
.venv/bin/python src/sanger_direct_check3.py
.venv/bin/python src/sanger_essdepth.py
.venv/bin/python src/sanger_tables_audit.py
.venv/bin/python src/panels_curated.py
.venv/bin/python src/expression_triangulation.py
.venv/bin/python src/hplm_reverse_test.py
.venv/bin/python src/make_figures.py
.venv/bin/python src/render_pdf.py
.venv/bin/python src/validate_release.py
```
Additional inputs beyond the DepMap list above: `~/Downloads/OmicsProfiles.csv`
and `OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv` (expression);
Rossiter 2021 supplements in `data/raw/hplm_rossiter2021/` (see its README).
Python deps: numpy, pandas, scipy, pyreadr, openpyxl, matplotlib, fpdf2
(statsmodels only for tests).

## Headline numbers
456 differential dependencies (normalized scale, v2r2): 84-86% medium-consistent
(HC3-robust 75-82%), 1 format candidate (LSM7; 0 at 5% FDR). Broad published
gains: 47% medium-consistent overall, 87% of the 55% that replicate. Sanger
headline-18: 8/16 replicate, 5 medium-consistent (sterol/SREBP axis),
3 unresolved (SCAP/DDX3X/ITGB1). Ribosomal weakening persists after global
corrections in both assays; spliceosome complex-wide weakening does not
survive curated gene sets (see correction note in manuscript §3).
