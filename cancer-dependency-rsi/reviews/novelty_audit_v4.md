# Novelty audit v4 — exact-claim adjudication (C1 / C6), supersedes v3 comparison matrix

Date: 2026-10-28 (post sci-package review 82/100). v1–v3 preserved; v3 §3 matrix rows on S3 are **corrected** here (sci-package HIGH-1, independently verified against cached full text).

## 1. Exact locked claim (unchanged, no renaming)

Across the fixed 207-gene confirmatory panel, partial Spearman ρ = −0.146 (donor 95% interval −0.175 to −0.114; BOUND under predeclared δ = 0.20), relating observed format-bundle score lability (equal-weight mean over 6 Broad models of within-model mean |Chronos_Dome − Chronos_Plastic|) to donor-averaged normalized displacement of each gene's within-panel dependency rank from the fixed Broad 2D consensus ordering (AdherentMean), in 148 independently filtered Sanger organoid models / 144 donors, adjusted for ranked |AdherentMean|. Conditional on fixed genes, the 6 measured Broad models, and processed measurements. Association only. Sign robust; magnitude bound primary-definition only (C10 table).

## 2. Corrected closest-prior account (verified from cached PMC full texts)

- **S1 Broad NextGen (Nature 2026, doi:10.1038/s41586-026-10843-7, PMC13581591).** Reports paired minipool format/medium OLS effects (7 format genes q<0.05 incl. ITGB1/ITGAV/ITGA3, NCKAP1/PTK2; 8 medium genes incl. lipid SPTLC1/SPTLC2/SQLE), class-level variance, genome-wide organoid-vs-2D differential dependency (source of AdherentMean), and state-associated WNT dependencies (MESD/WLS/TCF7L2/FZD5/LGR4 vs PDAC-classical/MUC). It does **not** join per-gene measured format lability to any external organoid ranking endpoint.
- **S2 Sanger biobank (Nature 2026, doi:10.1038/s41586-026-10830-y, PMC13581617).** Reports the organoid dependency/biomarker landscape (the external cohort) and notes culture conditions may alter dependencies, untested. No lability→displacement test.
- **S3 October transfer study (Biology 2026, doi:10.3390/biology15191782, PMC13664187) — CORRECTED.** Primary endpoint ranks *organoids per gene* (20 preselected genes, expression Elastic Net; Broad-94 + Sanger-148). **Additionally**, a retrospective secondary analysis *does* rank genes within individual organoids from the same frozen expression predictions, vs lineage-only and fixed-2D-mean comparators (abstract; Introduction; §3.5 synthesis/Fig. 6; "modest improvement over lineage-only … top-three overlap improved only in Sanger"). v3's claim that S3 "not done (explicitly not ranking genes)" is retracted — that quotation scopes S3's *primary* hypothesis only. What S3 does not do: use *measured environmental sensitivity* as the predictor, a 207-gene panel-conditional displacement estimand, donor-averaged displacement from a fixed 2D ordering, baseline-strength partial association, or a predeclared-δ donor-cluster bound. v2 had this distinction right; v4 restores it.

**Residual novelty (the only novelty asserted):** joining *measured paired-format lability* to *external within-organoid gene-rank displacement*, conditional on baseline dependency strength, panel-wide, with a predeclared material-magnitude bound. Endpoint components exist in priors; the substantive joined relationship and its negative/bounded result were not located in any searched source. This is a bounded "not located" statement, not proof of global novelty.

## 3. Searches executed for v4 (dated 2026-10-28; queries/results retained in session record)

| check | method | result / disposition |
|---|---|---|
| S3 full-text re-read | cached PMC13664187.xml (§3.5, abstract, intro) | within-organoid ranking confirmed → matrix corrected above |
| Flagged P3 record PMID 42879314 ("Decoding cellular vulnerabilities…", Brief Bioinform 2026, doi:10.1093/bib/bbag559) | NCBI efetch abstract | VCAT drug-response (IC50) prediction from CMap/LINCS + CRISPR vulnerability features; organoid use = drug-response generalization cohort. No environmental lability, no dependency-rank displacement. **Excluded: different estimand (drug response, not dependency transfer).** |
| Flagged P5 record PMID 40902593 (gastric neuron–tumor organoid, Cell Stem Cell 2025, doi:10.1016/j.stem.2025.08.006) | NCBI efetch abstract + publisher page | Co-culture reveals metabolic vulnerabilities (LSS/ACACA) absent in monolayers — adjacent evidence that environment can reveal dependencies. No paired format lability, no panel displacement test. **Excluded as same-claim prior; retained as adjacent context.** |
| Exact-identifier / citing search, S1 DOI | web search on 10.1038/s41586-026-10843-7 + minipool | News/coverage + S1 itself + supplement; no follow-up joining minipool lability to an external endpoint located |
| Exact-identifier / citing search, S3 | web search on title/DOI 10.3390/biology15191782 | No citing analysis of measured lability located (search recall limited; S3 is Oct 2026, citation lag expected) |
| Concept search | "measured culture format lability organoid dependency rank displacement CRISPR minipool" | S1, S2, S3 only among relevant hits |
| Prior searches | v1 Europe PMC (3 q), v3 PubMed (6 q, `novelty_refresh_v3b_pubmed.json`); v3 Europe PMC failed 503 (not executed, no inference) | Preserved; P3's other 10 records screened by title/abstract topic (antiviral, reviews, NF1 breast, zebrafish/fish lines, hiPSC, SCLC, mouse models, gene-editing review) — none tests dependency transfer by measured environmental sensitivity |

Limits (permanent): title/abstract + web-index recall; supplement-only and preprint analyses can be missed; citation indexes lag Oct-2026 papers. Absence of a hit is not proof of novelty (spec §7).

## 4. Why the result resolves the predeclared uncertainty (unchanged from v3 §4, endorsed 82-review)

G1-approved alternatives: (a) environment-labile genes are those whose 2D rank fails to transfer (positive association); (b) paired-model lability does not carry to population-level organoid displacement. The single locked test (categories SIGNAL/BOUND/NEGATIVE/INCONCLUSIVE and δ=0.20 fixed pre-access) excludes |ρ|≥0.20 for the primary definition with an entirely negative interval: (a) gets no support in this panel.

## 5. Consequence (scope-limited, unchanged)

Within this 207-gene panel, greater measured format lability supplies no support for greater organoid rank displacement beyond reference strength; the observed relationship points oppositely. Target interpretation requires direct transfer/context evidence rather than treating paired-format score lability as a sufficient transfer warning. Not inferred: target-ranking utility (S3's expression-based ranking result stands on its own estimand), invariance/equivalence, latent sensitivity, causation, clinical validity, or generalization beyond panel/cohorts/conditions.

## 6. Adjudication requested

C1/C6 qualification rests on §§2–5: corrected prior matrix, screened exclusions with reasons, residual-novelty scoping, and the C10 robustness limits. Reviewer (sol-high) to confirm or refute gate-by-gate; lead does not self-certify.
