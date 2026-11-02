> SUPERSEDED by provenance_v2.md (2026-10-28, G1 remediation). Retained for audit trail; do not cite v1 numbers.

# Provenance & identifiability audit v1 (2026-10-28, Phase 1 — in progress)

## Verified from primary full texts (Europe PMC fullTextXML, local copies in `data/papers/`)

### S1 Broad NextGen (PMC13581591, doi:10.1038/s41586-026-10843-7)
- 147 genome-scale CRISPR screens; NextGen organoids/spheroids; 10 cancer types; Chronos processing (incl. Chronos **pre-trained on traditional+NextGen CNS models** before organoid application — preprocessing-provenance flag for transfer analyses).
- **Environmental minipool:** enAsCas12a library, **250 test genes** from 9+ functional classes (Integrin, ECM Adhesion, Actin Regulation/Nucleation, Adherens/Tight/Gap Junction, Lipid Metabolism, Wnt, PI3K-MTOR, Cell Cycle, Other per `minipool_library_composition.csv`); genes selected partly from 3D-vs-2D dependency differences → **selected, not representative**.
- **18 screens, 7 biological models** (ACH-000048, ACH-000108, ACH-000178, ACH-001418, ACH-002958, ACH-003040, ACH-003052): format = 2D plastic vs 3D Matrigel dome; medium = RPMI/FBS (serum) vs OPAC (serum-free). Screen counts: dome 11, plastic 7, OPAC 9, RPMI-FBS 9. QC: total reads ≥ 5×10⁶, NNMD ≤ −1.5 (observed NNMD −9.19…−1.81, ROC-AUC 0.786…0.951). Analysis: Chronos + OLS with format, serum, interaction terms (`minipool_regression_coefficients.csv`).
- **Published findings = CONTROLS (not discoveries):** integrin/actin-regulation classes vary by growth format; lipid-metabolism class varies by medium; differential integrin vs cholesterol-homeostasis effects.
- Data: DepMap portal file set "NextGen Model Manuscript 2026"; figshare 10.6084/m9.figshare.29472362 (CC BY 4.0). Code: github.com/broadinstitute/DepMap-NextGen-Public. Raw WGS/RNA in dbGaP phs003444 (controlled — **not used**; processed public data only).

### S2 Sanger organoid biobank (PMC13581617, doi:10.1038/s41586-026-10830-y)
- 256 clinically annotated tumour organoids derived (colorectal, oesophageal, ovarian, pancreatic, gastric); genome-wide CRISPR-Cas9 screens across **162 organoids**; CRISPRcleanR-normalized LFCs + BAGEL2 essentiality — **different measurement system from Broad Chronos; values not interchangeable/subtractable**.
- Data: figshare 10.6084/m9.figshare.28339340 (CC BY 4.0; processed matrix `07_EssMatrix_qnorm_corrected_logFCs.RData` 126 MB, BAGEL `07_EssMatrix_bDepletionsB2.Rdata`); Cell Model Passports; Sanger DepMap DataMiner. Code: github.com/Garnett-Lab/SangerOrganoidBiobank.

### S3 Closest transfer prior (PMC13664187, doi:10.3390/biology15191782)
- Expression-only Elastic Net, **20 preselected genes**, trained on 852 conventional models; blinded external validation: Broad-94 macro Spearman 0.1518, Sanger-148 0.1015 (17/20 positive); Sanger eligibility: 162 organoids / 157 donors before outcome access, donor-overlap exclusions applied. Rank-based (Chronos vs Sanger LFC scales acknowledged non-equivalent).
- **Explicitly left open:** "Differences in cellular state, growth geometry, medium composition, lineage composition, and functional-screening platforms may contribute individually or jointly. Their contributions were not experimentally disentangled or quantified here." → generic transfer is done; **disentangling measured environmental sensitivity as the explanation is the open gap** this project targets.

## Measured identifiability (our audit, `src/audit_minipool.py` → `data/identifiability_audit.json`)
- Matched **medium contrasts: 5** (same model+format); matched **format contrasts: 7** (same model+medium). Matches spec exactly. Zero missing values in 18×1000 Chronos matrix; ScreenIDs ↔ metadata exact match.
- Median |Δ| (test genes): medium 0.18, format 0.16 Chronos units. **Heterogeneity dominates:** 91% (medium) / 98% (format) of test genes take both signs across pairs → average effects are near-uninterpretable; estimands must be conditional (model/genotype/state-dependent) with all individual paired changes reported.
- **Direction integrity (C5 precursor):** our paired mean deltas vs authors' OLS coefficients — format test250 Pearson 0.91 / Spearman 0.82; medium 0.96 / 0.95. Cohort, direction, measurement interpretation confirmed.

## Open Phase-1 items
- Donor/model crosswalk Broad↔HCMI↔Sanger (incl. the 7 minipool models' lineages/genotypes from `model_metadata.csv`); count independent donors for transfer cohort after overlap exclusion.
- DepMap 26Q3 integrated vs study-specific (figshare) release decision + leakage audit (Chronos pre-training noted above).
- Sanger processed-matrix route (RData vs Passports/Project Score CSVs) + score-direction/QC audit mirror of the Broad audit.
- Novelty audit v1 (dated search, claim ledger) and the named G1 question.

## Route-resolution log (2026-10-28)
- Broad figshare 29472362 (CC BY 4.0): 9 minipool/metadata files downloaded + SHA-256 manifest (`data/source_manifest_broad_figshare.json`). Minipool models: ACH-000048 (ovarian endometrioid), ACH-000108 (pancreas adenosquamous), ACH-000178 (pancreatic adeno), ACH-001418 (serous ovarian), ACH-002958 (stomach adeno, organoid), ACH-003040 (pancreatic adeno, organoid), ACH-003052 (organoid, OPAC dome/plastic pair; **lineage absent from figshare model/screen metadata — crosswalk gap**, resolve via DepMap Model.csv when a non-verification-gated route is available; blocks lineage-conditioned claims for this model only).
- Sanger figshare 28339340 (CC BY 4.0): BAGEL binary depletions parsed (17,647 genes x 930 ACH columns — DepMap-wide incl. cell lines); covariates use HCM-SANG IDs (256 organoids). **HCM-SANG <-> ACH crosswalk still needed** (candidates: figshare jaccard/VAF HCMI files; Cell Model Passports — SPA, no direct file route found unattended; DepMap portal serves a verification page to curl — not bypassed per spec).
- DepMap 26Q3 (forum 2026-10-05): integrates 150 NextGen models. Per spec preference, development uses study-specific figshare releases; integrated 26Q3 treated as transductive-risk until leakage audit.

## Genome-wide Layer-A route constraint (2026-10-28)
Author code (DepMap-NextGen-Public: src/minipool.py etc.) expects the DepMap-portal file set "NextGen Model Manuscript 2026" downloaded interactively into data/. Unattended curl to depmap.org receives a verification page (not bypassed). Options at Lock 1: (a) user-assisted portal download, (b) proceed with figshare minipool + published result tables (organoids_vs_2d tests) with provenance caveats, (c) sol-xhigh unstick consultation for another official route. Environmental estimand (minipool) is unaffected; genome-wide transfer analyses depend on this decision.
