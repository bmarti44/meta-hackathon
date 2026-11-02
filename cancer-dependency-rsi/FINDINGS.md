# Findings: environment-conditional dependency laws (2026-10-29 direct phase)

## The bounded claim
Dependencies reported as "3D/organoid-specific" for sterol/mevalonate
synthesis are, in every dataset available here, **medium-formulation
effects, not 3D-format effects**:

- Fully paired minipool 2×2 (6 models): Dome−Plastic at fixed medium =
  −0.011 (mevalonate mean ΔChronos); Serum-free−Serum at fixed format =
  −0.266. (`generations/recomb12_minipool2x2.json`)
- Formulation gradient across 924 screens (centered pathway score):
  FBS media −0.10; Tumor Stem Media (B27) −0.21; OPAC:Ad+++ −0.50;
  Breast Organoid Media −0.52. Effect present in **adherent** TSM screens
  (−0.18) — format-independent. (`generations/recomb5.json`)
- Formulation class alone predicts per-screen mevalonate score at
  patient-held-out R²=0.58 (expression adds nothing: 0.575→0.578);
  effect survives essential-depth/days adjustment (−0.40 → −0.38) and
  lineage adjustment (−0.39); homogeneous across all 8 evaluable
  lineages (−0.36…−0.59, all CIs exclude 0).
  (`generations/recomb7.json`, `recomb14.json`, `recomb16_lineageadj.json`,
  `generations/formulation_atlas_v2.csv`)
- **Held-out confirmation** (sequestered patients, single run):
  org_defined − FBS = −0.396 [−0.431, −0.356] vs dev −0.399.
  (`generations/recomb11_heldout.json`)
- Near-universal: 73/77 dev organoid models score ≤ −0.35; the four
  weakest (−0.24…−0.35) remain shifted vs the FBS baseline (−0.10);
  SQLE/HMGCR/LDLR copy number does not distinguish them.
- Internal control: LDLR dependency vanishes in defined media
  (−0.107 → −0.012) while LDLR expression rises (+1.0 logTPM) — sterol
  starvation physiology; SREBP machinery (SCAP/MBTPS1/SREBF2) gains
  dependency; pathway expression up (+0.37 logTPM).
- Genome-wide: MSMO1 and SQLE are the #1/#2 dependency gains in
  organoid-defined vs FBS media (−1.02 each, patient-boot CIs exclude 0).
  (`generations/recomb6.json`, `generations/formulation_atlas_v1.csv`)
- Cross-system: mevalonate genes sit at within-model essentiality
  percentile 0.44 in Broad 2D-FBS models, 0.22 in Broad organoids, and
  0.25 in Sanger organoids (independent LFC assay, n=162; exploratory
  reuse of spent-cohort assay for a new gene-set question).
  (`generations/recomb21_sanger_mev.json`)

## Secondary laws (same machinery)
- Gains in organoid-defined media: heme (−0.32), OXPHOS C1/C4
  (−0.19/−0.13), FA synthesis (−0.15), folate (−0.15).
- Losses: iron handling (+0.20), redox/GSH (+0.16), spliceosome
  (uncentered −1.96 → −1.20) and ribosome (−2.22 → −1.79) weakening.
  Per-formulation cut: ONLY the two dome formulations show it (TSM
  spheroids do not) — dome-format/formulation-family associated,
  format-vs-medium unresolvable in current data (perfectly confounded).
  Not explained by essential-depth, screen days, proliferation-program
  expression (coef 0.748->0.739), target expression (0.7475->0.7438),
  or lineage composition; screen duration within library also fails
  (14d screens are slightly MORE negative). Suspension-vs-adherent at
  fixed RPMI+FBS (solid lineages) shows no splice effect (-0.002).
  Loss tail is enriched for stable-complex subunits (top-200:
  spliceosome 8% vs 1.1% background) but half-life does not explain
  genome-wide variance. Opposite
  attribution to the gain side; mechanism open (protein-turnover/
  depletion-dynamics hypothesis pending).
- Wnt secretion/signaling (FZD5, LGR4, WLS, PORCN) gains only in
  OPAC:Ad+++ (−0.24 score), consistent with absence of exogenous Wnt
  in that formulation.

## Prior-art boundary (what is NOT novel)
- NextGen paper (Nature 2026) reported HALLMARK_CHOLESTEROL_HOMEOSTASIS
  as top organoid-vs-2D enrichment (OR 28.6) and SQLE serum effect
  (coef −0.555, FDR 0.039, minipool). Colon CSC spheroid cholesterol
  essentiality: Oncogene 2021.
- **Correction (2026-10-29):** the medium-vs-format decomposition is
  NOT novel. Neiswender et al., Nature 2026 (DOI
  10.1038/s41586-026-10843-7) ran the same 7-model/18-screen minipool
  2x2, fit format/medium/interaction terms, named SQLE/MSMO1 as
  medium-sensitive (lipid genes q=1.5e-4) and concluded "growth format
  does not significantly affect CRISPR screen outcomes under serum-free
  conditions." Our recomb12 is a re-analysis of that same dataset (only
  SQLE/MSMO1 among sterol genes are in the 1,000-gene library; per-model
  format contrasts range ~-0.8..+1.2, so it is weak evidence on its own).
  LDLR/SREBP switch is textbook sterol-starvation physiology; Wnt-secretion
  claim conflicts with NextGen's minipool result (FZD5/WLS not sensitive).
- Plausibly new (scope, not concept): genome-scale pathway coverage,
  formulation gradient, TSM adherent = spheroid (-0.25/-0.25,
  library-matched), heme gain, held-out replication. Library-matched
  check (Humagne-CD only): FBS -0.03, TSM -0.25, organoid media -0.53;
  essentiality-matched gene-set null z=-16.

## Correction (2026-10-29)
Earlier "medium lability (134 models, split-half 0.83)" paired screens
across ModelConditionIDs with mostly missing FormulationID strings
(only 6 adherent models have >=2 annotated formulations). That number
measures reproducible between-screen variability, not medium lability.
It also implies part of minipool format-L may be gene-specific
measurement variance. The formulation laws above do not depend on it.

## Negative results retained
- Minipool format lability → organoid displacement: small real
  association (Broad dev −0.053, held-out −0.076, frozen estimand),
  below 0.20 materiality — claim terminated per kill criterion.
- Query policies cannot beat known formulation labels (saturated task).
- Sol-xhigh honest review: NOT_PROMISING 18/100 for the full GOAL
  (~1%); policy thread dead on 7-model atlas (q=0.00037 vs 0.020).

## GOAL v4 deliverables 1–3 (2026-10-29, medium_attribution_v2)

Per-gene attribution table (17,524 genes; library-offset corrected from 27
dual-library FBS models; lineage-adjusted; raw + dynamic-range-normalized
scales; dev patients: 68 dome + 9 adherent organoid-medium models vs 207
FBS-adherent models in 9 lineages):
`generations/medium_attribution_v2_{raw,norm}.csv`, code
`src/medium_attribution_v2.py`.

- Hits (norm scale, q<0.01, |Δ|≥0.25): 240 gains, 209 losses.
  **Medium-attributable: 85% of gains, 84% of losses; format-candidate: 0
  genes** (either scale). Slopes of adherent-same-medium effect on
  dome effect: 0.88 (gains), 0.90 (losses); dome-vs-adherent at fixed
  medium: 0.14/0.14; CNS serum-free (TSM): 0.54 gains, −0.04 losses —
  gains are partly generic serum-free effects, losses are
  organoid-formulation-family-specific.
- **Correction to "losses" bullet above:** the spliceosome/ribosome
  weakening is NOT dome-format-specific. It reproduces in adherent
  models in the same formulation family (splice panel raw Δ: dome
  +0.90, adherent +0.64, format-at-fixed-medium +0.13, TSM −0.03).
  Format-vs-medium is resolved in favor of medium for losses too
  (caveat: n=9 adherent models, mixed formulations).
- **Doubling/dynamic-range (deliverable 3, Broad side):** common-essential
  depth is identical across conditions (median essential Chronos: FBS
  −1.375, dome −1.376, org-adherent −1.405, TSM −1.390; compression
  ratio 1.0006) despite longer dome screens (24 vs 21 days). The
  weakening is therefore not global dynamic-range compression: median
  common-essential Δ is +0.035 while spliceosome/ribosome panels sit at
  +0.90/+0.64. CPD is recorded for 1 of 1,241 screens, so a true
  per-doubling correction is impossible in this release; complex-specific
  depletion kinetics (slow-turnover stable complexes) remain the open
  mechanism. Neither 2026 paper reports or corrects for this weakening.
- **Published catalogues (deliverable 2):** Broad figshare
  organoids-vs-2D gains (FDR<0.05, Δ<−0.25; n=285): 55% replicate under
  lineage adjustment on dev patients; of replicating hits **87% are
  medium-attributable, 0% format**. Strictest published gains (n=17):
  16 medium, 1 unresolved. Published losses (n=252): 61% replicate, 85%
  medium. Sanger/Herranz-Ors "organoid core fitness" exclusives (n=97):
  20 replicate as Broad differential hits (14 gains, 6 losses — i.e. 6
  are *weakened* in Broad organoids); 14 medium, 6 unresolved. Their
  headline 18 (exclusive, non-common-essential): 8 replicate, all gains;
  5 medium-attributable (MVD, IDI1, MBTPS1, MBTPS2, PNKP), 3 unresolved
  (SCAP ratio 0.86 but CI straddles criterion; DDX3X, ITGB1 ratio <0.3).
- Named medium-attributable targets (norm Δ, adherent ratio): SQLE
  (−0.84, 1.07), MSMO1 (−0.81, 0.67), FASN (−0.42, 0.99), ACLY (−0.41,
  0.91), ALAS1/FECH (heme; −0.39/−0.37), FZD5/LGR4/WLS (Wnt; ratios
  0.9–1.07, TSM ≈ 0 — formulation-family, conflicts with NextGen
  minipool per prior note).
- **Held-out confirmation** (25 reserved-patient domes, 5 adherent;
  `generations/medium_attribution_v2_heldout.json`): dev→held-out Δ
  slope 0.97, corr 0.98, same-sign 100% among medium-attributable hits;
  held-out adherent reproduction slope 0.88.
- Limitation: Humagne-CD-only sensitivity is underpowered (5 FBS models
  in organoid lineages); library handling rests on the 27-model offset.
- **Sanger assay direct check** (`src/sanger_direct_check3.py`,
  `generations/sanger_direct_check_v3.json`, `sanger_essdepth_v1.json`;
  v1/v2 scripts used the cell-line-only EssMatrix — superseded):
  organoid LFC (supp. table 6, 162 models) vs Sanger 2D lines (930).
  Mevalonate within-model percentile 0.099 in organoids vs 0.394 in 2D
  lines (cross-system gain confirmation, independent assay). Sanger
  organoid screens are globally depletion-compressed (reference-essential
  median LFC −0.96 vs −1.52, 0.63×). Depth-scaled, spliceosome weakening
  disappears (1.53 vs 1.45 ×essential-depth); ribosome keeps a residue
  (1.31 vs 1.63). In Broad Chronos (per-screen rescaled) only the
  complex-specific residue is visible. Unified reading: the weakening is
  a depletion-kinetics/doublings artifact class (slow-turnover complexes
  lag when doublings are fewer), associated with the slow-growth
  organoid-formulation condition; exact mechanism still needs
  CPD-recorded screens. Headline-18 within Sanger: ITGB1 (−0.233) and
  GNA13 (−0.238) show the largest organoid-vs-2D percentile shifts —
  ITGB1 remains the best non-medium candidate across both assays.

## Decisive next experiments (require new data)
1. Paired-format genome-wide screens at fixed medium in >=20 models
   (separates dome architecture from dome-medium family for the
   spliceosome loss; currently perfectly confounded).
2. Lipid add-back (LDL/cholesterol/B27 titration) in OPAC-grown models:
   predicts mevalonate dependency score returns toward FBS baseline
   (-0.50 -> -0.10) and LDLR dependency reappears.
3. Doubling-resolved screens (CPD recorded) in domes: predicts
   spliceosome/ribosome Chronos recovers when scored per doubling
   if depletion dynamics drive the loss; subcomplex heterogeneity
   (U2/U5/RBM39 vs U1/U2AF) predicts only partial recovery.
4. Statin/SQLE-inhibitor dose-response in matched FBS vs defined
   media: predicts >=5x potency shift in defined media.
- **LOO robustness** (`generations/medium_attribution_v2_loo.json`): dropping any one of the 9 adherent models, A-on-D slope over hits stays 0.87–0.92 and ≥94% of medium flags are retained. Figures: `manuscript/figures/fig{1,2,3}_*.png` (`src/make_figures.py`); survivor candidates: `generations/survivor_candidates_v1.csv`. Finding review: `reviews/goal_v4_finding_review_v1.md`.
- **Correction (curated panels, `generations/panels_curated_v1.json`):** the +0.90/+0.64 splice/ribo panel medians above used small hand-picked panels and overstate complex-wide weakening. Curated BAGEL sets (Broad, raw Δ median): SPLICEOSOME (n=35) +0.035 (A -0.02, F +0.03), RIBOSOMAL (n=38) +0.146 (A +0.19, F -0.01), essential baseline +0.031; proteasome/RNA-pol/DNA-rep at baseline. Weakening is subunit-concentrated (12/38 ribosomal, 7/35 spliceosome genes are medium-attributable loss hits); ribosomal is the only clear whole-set shift. Sanger depth-scaled (curated): spliceosome 1.34 vs 1.11 (no residual weakening; percentile 0.018 vs 0.027 = stronger in organoids), ribosomal 1.25 vs 1.57 (residue persists; replaces 1.53/1.45 and 1.31/1.63 above). Genome-wide loss claims (209 hits, 84% medium, slopes) unchanged. Manuscript + Fig.2 corrected.
- **Hardening (2026-10-30):** Sanger own-call audit (table 5 BAGEL binary, `generations/sanger_tables_audit_v1.json`): exclusive/headline genes are NOT threshold-fragile within organoids (median depletion frequency 0.80/0.69; none <0.25) — their calls are solid; attribution, not call quality, is the issue. Table 7 is a within-organoid subgroup analysis, not organoid-vs-2D. Expression triangulation (`generations/expression_triangulation_v1.json`, condition-mapped Omics TPM): mevalonate expression median Δ +0.36 mirrors dependency Δ -0.36 (SQLE +0.75/-0.84; LDLR expr +0.61; mev expression score FBS -0.01, org-adherent +0.18, org-dome +0.44) — sterol-starvation signature confirmed on an orthogonal data type. Heme/FA-synthesis expression moves opposite (-0.47/-0.36), so expression corroborates the sterol axis specifically, not all medium gains. Genome-wide corr(D,E)~0.
- **HPLM reverse test (Rossiter et al. 2021, PMC8172426 Table S1; `generations/hplm_reverse_test_v1.json`):** K562 genome-wide RPMI+dS vs HPLM+dS (both dialyzed-serum). Genome-wide corr(HPLM-RPMI delta, Broad D_org) = 0.04 — orthogonal axes. SQLE is LESS essential in HPLM (delta +0.44, Zdiff +3.8) vs the top organoid-medium GAIN (-0.84): physiological formulation relieves, serum-free formulation creates, the same dependency. Genes essential only in RPMI (relieved in HPLM, Z>3, n=97) are enriched 4.6x for our medium-attributable set (Fisher p=3e-4; incl. SQLE, KDSR) — medium-created dependencies are bidirectional and partly shared. Mevalonate panel median delta is tiny (-0.08, z=-3.0) with within-pathway heterogeneity (HMGCR/LDLR more essential in HPLM). Ribosomal curated set shows no HPLM weakening (delta ~0) in fast-growing K562, consistent with depletion-kinetics rather than generic medium effects. Caveats: single GW line (K562), dialyzed serum both arms, focused panel too sparse (mev n=2).
- **Astra xhigh review r1 (68/100) → v2r2 revision (2026-10-30):** all 12 issues verified true and fixed (reviews/astra_review_r1_dispositions.md). Headline now: 249 gains/207 losses (dev-only 22-model calibration), medium-consistent 86%/84% (HC3 82%/75%; bootstrap slope 0.90 [0.81,0.98], 71% of hits flagged in >=50% of reps); 1 format candidate (LSM7, symmetric rule; 0 at FDR); common-support (38 domes) slope 0.89; held-out DISJOINT baseline slope 0.96. Language downgraded throughout: medium-consistent (not causal), depletion kinetics = hypothesis, title scoped to reproduced hits. Prior FINDINGS numbers above (240/209, 85%/84%, shared-baseline held-out) superseded by v2r2.
- **Astra xhigh skeptical review loop (2026-10-30): 68 → 82 → 89 → 89 → 95/100 SHIP IT** (reviews/astra_review_r1..r5.md + dispositions). Substantive changes across rounds: dev-only calibration, disjoint held-out, symmetric format rule (LSM7), HC3 + joint bootstrap uncertainty, common-support sensitivity, curated-panel correction, medium-consistent scoped language throughout. Final numbers are the v2r2 set throughout this section as amended by the correction bullets.
- **Novelty audit (Astra deep web research, 2026-10-30): PARTIALLY TRUE.** No verified Class A (genome-wide per-gene medium attribution with fractions for the 2026 catalogues). Overstatements corrected in v2r3: Neiswender already did genome-wide format comparisons (dome vs coat r=0.984, q>0.71); medium associations quantified at scale since Lagziel 2019; Sanger/Pacini correct a medium-associated PC in cell-line data; Liang 2025 serum-free genome-scale abstract; Zaidi & Sawyers (Cell Res, 21 Oct 2026) raise the culture-condition question without quantification. Title now "medium-consistency audit". Full report: reviews/astra_novelty_research3.md.
