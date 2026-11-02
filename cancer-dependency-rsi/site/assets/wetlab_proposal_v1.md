# Wet-lab test proposal: is sterol-pathway "organoid-specificity" a medium artifact in your models?

**Ask:** one add-back + one drug-shift experiment in 3–4 organoid models. ~4 weeks, no new CRISPR screen required for the first readout.

## Background in one paragraph
Our genome-wide re-analysis of DepMap 26Q3 (Broad NextGen + Sanger organoid catalogues) finds 84–86% of organoid-vs-2D differential dependencies are consistent with medium effects (reproduced in adherent organoid-medium culture, no dome; bootstrap slope 0.90 [0.82–0.99]), with a single format candidate (LSM7) under symmetric criteria and none at 5% FDR. The strongest class is sterol/mevalonate synthesis (SQLE ΔChronos −0.83, MSMO1 −0.81 vs FBS 2D; adherent reproduces ~100% for SQLE). These are consistency classifications from observational contrasts (adherent comparators cover 6 of 9 lineages, mixed formulations) — which is exactly why the perturbation test below matters. Several appear on Herranz-Ors et al.'s headline "organoid-specific core fitness" list (MVD, IDI1, MBTPS1/2, SCAP). Plasma supplies LDL cholesterol in vivo; organoid media do not. If the dependency is LDL starvation in culture, LDL rescue would support LDL limitation as a contributor in these cultured models; transfer to tumors in patients (whose tumors see plasma LDL) would remain untested by this experiment.

## Experiment 1 — LDL add-back (decisive, cheap)
- Models: 3–4 organoid lines you already grow in OPAC/organoid medium with high mevalonate scores (we can rank your models from public data if ACH/HCM IDs shared).
- Arms (domes, standard passaging): (a) standard medium; (b) + LDL cholesterol (e.g. 50 µg/mL, titrated 10–100); (c) + mevalonate (0.5 mM, pathway bypass control); (d) + 10% FBS adaptation if tolerated.
- Readout at 7–14 days: growth ± SQLE inhibitor (e.g. NB-598 or terbinafine) and ± statin; LDLR/SQLE/HMGCR expression (qPCR/WB) as sterol-starvation markers.
- **Prediction if medium artifact:** LDL add-back abolishes SQLE-inhibitor and most statin sensitivity (≥5× IC50 shift), LDLR expression falls. If sensitivity persists under LDL repletion, the dependency is not explained by LDL limitation in these models and warrants follow-up as candidate biology — also a publishable answer.

## Experiment 2 — matched-medium drug shift (2D control)
- Same models adapted 2–3 passages to: organoid medium adherent vs RPMI+10% FBS adherent.
- Dose-response: SQLE inhibitor, simvastatin/atorvastatin, FASN inhibitor (e.g. TVB-2640) — FASN/ACLY are also medium-attributable in our table (ratios 0.99/0.91).
- **Prediction:** ≥5× potency in organoid medium vs FBS at adherent format (format-independent), mirroring the CRISPR Δ.

## Optional Experiment 3 — mini-screen confirmation
- 1k-gene or focused lipid-library CRISPR in 2 models × (organoid medium ± LDL). Prediction: mevalonate pathway score moves from ≈ −0.50 toward FBS baseline ≈ −0.10; the ribosomal relative weakening seen in organoid media (curated-set median +0.17 Chronos; strongest individual subunits up to +1.2) does *not* respond to LDL — a built-in negative control distinguishing nutrient effects from the separate weakening phenomenon.

## What we provide
Per-gene attribution table for all 17,525 genes (medium-consistent / format / unresolved flags with CIs and bootstrap frequencies), model ranking by predicted effect size, analysis of any resulting screen data, co-authorship on the technical note. Data/code: `generations/medium_attribution_v2_norm.csv`, `manuscript/manuscript_draft_v2.md`.

## Falsification criteria (agreed in advance)
Medium-artifact claim fails if: LDL-replete organoid-medium models retain SQLE-inhibitor IC50 within 2× of LDL-free, in ≥3 of 4 models. We will report either outcome.
