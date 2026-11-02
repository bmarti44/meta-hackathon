# Measured format lability and organoid rank displacement in a selected panel

**Draft for independent expert review — not submitted. Status: archived locked analysis reported with unresolved patient-weighting qualification (C6/C10 PARTIAL); novelty screening completed 2026-10-29 (sgen014, residual claim not located in completed set); policy-improvement claims: none (C8/C9/C13 unmet, see Limitations). Final campaign determination (2026-10-29, sol-xhigh slot 3/3): INCONCLUSIVE, GOAL_COMPLETE: NO (determination score 98) — reviews/terminal_determination_xhigh_v3.md.**

## Abstract

Whether a cancer gene dependency measured in conventional culture persists in patient-derived organoids is usually assessed gene-by-gene or by expression-based prediction. We asked a narrower, predeclared question: across a fixed 207-gene panel, does *measured* sensitivity to growth format — paired dome-vs-plastic dependency lability in six Broad models (NextGen minipool, Chronos) — track how far each gene's dependency rank is displaced from a fixed 2D consensus ordering inside independently filtered Sanger organoids (148 models, 144 covariate donor records reconciled to 142 patients post-lock (see Limitations)), beyond baseline dependency strength? In a single locked external test (hypotheses, panel, estimator, and material magnitude δ = 0.20 frozen before outcome access), the archived 144-covariate-ID-group analysis yielded ρ = −0.146, interval [−0.175, −0.114], and BOUND under the locked grouping. Patient-weighted estimates, uncertainty, and decision remain unverified after reconciliation to 142 patients (sgen001); a worst-case weighting-envelope screen failed to establish even point-estimate sign/magnitude robustness (ENVELOPE_TOO_WIDE, sgen004) and cannot certify an interval or decision. Sign robustness statements below apply to the archived analyses. We report a complete 250-gene evidence atlas separating environment, transfer, biomarker, and prior evidence per gene.

## Introduction (condensed)

Broad NextGen (S1) measured paired format/medium effects for 250 selected genes and genome-wide organoid-vs-2D differences; Sanger (S2) mapped organoid dependencies/biomarkers; an October 2026 study (S3) showed attenuated *expression-based* rank transfer for 20 genes, including retrospective within-organoid gene ranking (§3.7). None joined *measured environmental lability* to an external displacement endpoint. That join — with selection-tail exclusion and baseline-strength adjustment — is the residual uncertainty tested here (novelty audits v4-v8 plus sgen014 completion: S1 supplement visually inspected (no figure panels exist in MOESM1) and the complete broad query set screened beyond the relevance top-25 (stage-2 abstract triage: full abstracts for nearest/strong-signal records, lead+signal sentences for all - qualified deviation recorded in sgen014) with no plausible overlap located; C1 adjudicated MET with bounded 'not located' qualification; residuals: non-Europe-PMC sources, main-article extended-data pixels).

## Methods (summary; full protocol in PROTOCOL.md / lock_s/scientific_protocol_v1.json)

- **Predictor (Layer A, exploratory/adaptively reused):** per-gene mean |Chronos_Dome − Chronos_Plastic| within model, equal-weight over 6 models with matched format pairs (medium held fixed per pair). Authors' OLS design reproduced exactly first (max |diff| 1.73e-8).
- **External endpoint (single locked use of cohort C):** donor-averaged normalized |rank displacement| of each gene from the fixed Broad 2D consensus (AdherentMean) within the 207-gene panel, 148 Sanger organoid models / 142 patients (144 locked covariate donor records; see Limitations) after donor-overlap and library filtering. Chronos and Sanger fitness scores were never subtracted; cross-study comparison is rank-based within panel.
- **Estimator:** partial Spearman via ranked-residual regression on ranked |AdherentMean|; donor-cluster percentile interval (5,000 draws); single primary + 4 Holm-controlled secondaries; δ = 0.20 predeclared as smallest material panel-wide rank association. Synthetic calibration of the donor kernel: 95/100 null, 97/100 nonzero coverage (code diagnostic only).
- **Locks:** Lock-S commit `lock2-scientific-only-v1-ce2b56c295fe` (reviews 78→88→89→94) preceded the single external run; result review 93/100 verified execution (30 locked hashes).

## Results

Archived 144-group primary: **BOUND**, ρ = −0.146 [−0.175, −0.114] (reproduced from retained per-gene coordinates to 3e-17). Secondaries (Holm): null-calibrated −0.209, TMOD-alias −0.145, alternate-library −0.151, unadjusted −0.217 — all negative; magnitude < 0.20 holds only for primary/S2/S3 definitions. Leave-one-Broad-model-out: all negative (−0.166…−0.082). Model-cluster and pathway-block ranges cross −0.20. Full table: `reviews/c10_robustness_table_v1.md` (C10 PARTIAL: archived sensitivity results verified; patient-weighted uncertainty and decision robustness unverified).

**Atlas (v4):** all 250 panel genes; 207 with external displacement coordinates (descriptive per gene — the panel association validates no individual gene); 43 exclusions with reasons; per-gene S1 author format/serum test results (7 and 8 FDR<0.05 genes respectively, all others explicitly tested-not-significant), S1 state/genotype findings (WLS/TCF7L2/FZD5; CDK6), separate medium/format axes with 3,000 paired observations.

## Limitations (binding)

Selected 250-gene panel (outcome-informed Tier-A tails excluded confirmatorily); external-cohort patient identity reconciled post-lock (sgen001): 148 models = **142 patients** (Passports same-patient records merge two model pairs the locked covariate file counted as separate donors), so the archived estimate and BOUND decision used 144 covariate-ID groups, splitting two actual patients across groups; effects on the patient-weighted estimate, interval, and decision are unquantified (size and direction unknown), the archived interval is not validated patient-cluster uncertainty, the locked execution is preserved, and no replacement confirmatory estimate/interval has been computed; 6 Broad models with unresolved donor identity (conditional inference only; no population claim over Broad models); processed-score measurement systems differ (rank-based cross-study estimand only); normalization uncertainty (Chronos; Sanger spline/ComBat within cohort) disclosed, not propagated; retrospective external validation (public data; exposure logged — 0 organoid outcomes seen pre-lock); no invariance/equivalence, causal, clinical, or genome-wide claim. **Policy-improvement (RSI) evidence: none claimed.** The research-policy loop has not yet run a cycle: generations pgen001–003 established measured-token accounting (adjudicated insufficient for C9 as written by sol-xhigh) and an identity-resolved raw-count universe (251 lines/250 patients) whose battery is gated on named accounting/schema witnesses; C8/C9/C13 remain unmet and the joint goal is not complete.

## Reproducibility

**Data and code availability.** Broad data: figshare 29472362 (CC BY 4.0 dataset terms as recorded in the retained source manifest; S1 article text CC BY-NC-ND 4.0 governs article reuse, not dataset reuse). Sanger data: figshare 28339340 + Nature MOESM3 (CC BY 4.0). Passports metadata: Sanger Data Usage Policy (internal research/educational use; no resale/commercial services), fetched and hashed in-project. Project code: LOCK2-pinned hashes in `lock_s/LOCK2_COMMIT.json` establish byte identity only; no separate code license has been recorded — treat reuse terms as unrecorded pending author designation. Full per-source register: `generations/sgen007/provenance_register_v13.json`.

Frozen artifacts + hashes (`lock_s/LOCK2_COMMIT.json`, atlas manifests); component reproductions: OLS matches published rounded coefficients within the documented 1e-6 component tolerance (417/3,000 comparisons fail the original sgen002 global tolerance), atlas CSVs byte-identical, primary point estimate exact from retained coordinates; donor interval reproduction from donor-level artifacts pending (labeled). Commands: `src/cli.py {status,resume,audit-data,reproduce-baselines}`; tests 99 passed/1 skipped (2026-10-29). Resource ledgers retained. A 2026-10-29 budget-allocation amendment briefly overwrote a LOCK2-pinned config file; the original was recovered byte-exact, all 30 LOCK2 hashes re-verify, and amended caps now apply only prospectively via a shadow budget root (incident + remediation ledgered and independently reviewed 98/100; Lock-S path untouched). Host model cost (2026-10-29 user amendment): estimated-cost basis — $42.44 list-price equivalent across 85 accounted calls at campaign close (estimator v8 final snapshot; v7 independently micro-reviewed 100/100); actual additional metered spend $0 (subscription auth). Estimates are not metered billing.

## References (primary seeds, verified)

S1 Broad NextGen, Nature 2026, doi:10.1038/s41586-026-10843-7 (PMC13581591; figshare 29472362). S2 Sanger organoid biobank, Nature 2026, doi:10.1038/s41586-026-10830-y (PMC13581617; figshare 28339340). S3 Transferability of transcriptome-based models, Biology 2026, doi:10.3390/biology15191782 (PMC13664187). Dream-RSI, arXiv:2609.14858 (method inspiration; adaptation departures in PLAN §0.4).

## Campaign update (2026-10-29; post-results, outcome-blind)

After the archived analysis, the campaign established a fresh DepMap-based pool disjoint from the spent cohort (sgen010) and ran two pre-registered metadata feasibility screens for a follow-on design. A two-arm culture-medium contrast fails the frozen feasibility criteria on current metadata (coverage, lineage positivity, and a structural precision ceiling: best achievable two-arm MDR 0.171 exceeds the 0.146 screen threshold; media-lineage Cramér V 0.568), and a one-sample transport design lacks component-level paired-format measurements beyond a single model (sgen011–sgen013, all outcome-blind; no DepMap outcome file has been opened). No follow-on outcome analysis has been run, and none of these screens alters the archived result above. The research-policy loop still has not run a cycle: its task contract is locked (pgen005) but no qualifying scientific task has been instantiated, so no policy-improvement evidence exists. Full generation-by-generation record: GENERATIONS.md.

## Direct-phase addendum (2026-10-29; development data, user-authorized)

Post-determination analyses on DepMap 26Q3 (Downloads release; 981-patient
reserve sequestered before value access; organoid subset opened once for a
frozen confirmation) reframed the organoid-displacement phenomenon:

1. With the frozen Lock-S estimand, Broad organoids replicate the Sanger
   direction at reduced magnitude (dev partial rho=-0.053 [-0.098,-0.007],
   n=82 models/80 patients; held-out -0.076 [-0.150,-0.008], n=28/26) vs
   Sanger -0.146. Below the 0.20 materiality bound; the lability claim is
   terminated as material.
2. The dominant, reproducible structure is a **medium-formulation law**:
   mevalonate/sterol synthesis dependency is switched on by lipid-poor
   defined media (per-screen centered pathway score: FBS -0.10; B27 stem
   media -0.21; OPAC/Ad+++ -0.50; breast organoid media -0.52), is
   format-independent (paired minipool 2x2: format -0.011 at fixed medium,
   serum-free -0.266 at fixed format; effect present in adherent screens),
   homogeneous across 8 lineages, predicts per-screen scores at
   patient-held-out R2=0.58 from formulation alone, replicates in
   sequestered held-out patients (-0.396 [-0.431,-0.356]) and across
   measurement systems (mevalonate essentiality percentile: Broad 2D-FBS
   0.44, Broad organoids 0.22, Sanger organoids 0.25). LDLR shows the
   inverse switch (dependency -0.107 -> -0.012; expression +1.0 logTPM).
   The NextGen paper reported the cholesterol-homeostasis organoid
   association; the medium-not-format decomposition, formulation
   gradient, and LDLR switch are, to our knowledge, unreported.
3. The same gradient extends, weaker, to sphingolipid (SPTLC1/2) and
   phosphatidylcholine synthesis (PCYT1A -0.55 in OPAC vs +0.30 in
   B27 media), heme (-0.32) and OXPHOS (-0.19/-0.13); iron handling
   (+0.20) and glutathione (+0.16) dependencies weaken.
4. Spliceosome/ribosome dependencies weaken specifically in dome
   formulations (uncentered spliceosome Chronos -1.96 FBS -> -1.20);
   not mediated by screen depth, duration, proliferation or target
   expression, lineage, or protein half-life. Mechanism open.
5. Wnt-secretion machinery (FZD5, LGR4, WLS, PORCN) gains dependency
   only in OPAC:Ad+++ , consistent with absent exogenous Wnt.

Full record: FINDINGS.md; per-analysis artifacts in generations/recomb*.json
and generations/formulation_atlas_v2.csv. An earlier "medium lability"
statistic was corrected (missing-formulation artifact) in the ledger.
