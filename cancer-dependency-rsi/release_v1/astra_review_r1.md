**SCORE: 68/100**

**VERDICT:** Substantial, reproducible descriptive results, but not ready to ship with the current causal headline. The main arithmetic and OLS implementation check out. The principal problems are attribution beyond what the design identifies, incomplete uncertainty propagation, contaminated validation, and several verified reporting errors.

## ISSUES

**Critical: none verified.** High, medium, and low issues follow. “Verified” denotes file inspection or recomputation; methodological concerns are identified explicitly.

1. **High — The contrasts do not identify a causal medium/format decomposition.**  
   **Evidence:** [medium_attribution_v2.py:120](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:120), [manuscript:19](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:19). Verified: the nine adherent organoid-medium models cover **six**, not nine, lineages. Thirty of 68 domes belong to lineages without adherent organoid-medium controls; **33/68 lack an adherent comparator with the same lineage–formulation combination**. F adjusts for lineage, but not formulation. D, A, and F also weight lineages differently: among normalized hits, median `|D−A−F|` is **0.0334**, maximum **0.1794**.

   Consequently, reproduction in adherent models establishes an association shared by those populations, potentially including medium, derivation, subtype, selection, and screening differences. It does not isolate medium from tumor biology. “A dependency … will not hold in vivo” at manuscript line 11 is especially unsupported.

   **Smallest fix:** Describe flags as **medium-consistent**, qualify “fixed medium” as formulation-family comparisons, report common-support sensitivity, and remove categorical causal/in-vivo conclusions. This limitation cannot be solved by lineage dummies alone.

2. **High — Reported uncertainty treats an estimated library correction as known; pooled OLS variance also materially affects classification.**  
   **Evidence:** [medium_attribution_v2.py:79](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:79), [contrast2:32](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:32). The 27-model offset is inserted before OLS, with no propagation of its uncertainty into SEs, p-values, or flags. Its coefficient in raw D is **−0.982**. The offset’s standalone estimated SE contribution is a median **1.54× the reported conditional D SE** among raw hits. This comparison is diagnostic, not a complete corrected SE: overlapping calibration/control models require covariance handling.

   Separately, verified HC3 sensitivity changes normalized medium classifications from **379 to 347**, with gain/loss fractions **78.3%/76.1%**, versus **85.0%/83.7%**. Several relevant patients also contribute multiple models.

   **Smallest fix:** Propagate calibration uncertainty and shared-model covariance, preferably through a patient/model bootstrap that re-estimates the offset and contrasts. Report a robust-SE sensitivity. The current exact fractions are more assumption-dependent than presented.

3. **High — “Depletion-kinetics artifact” is asserted more strongly than the evidence supports.**  
   **Evidence:** [manuscript:37](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:37), [panels_curated.py:39](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/panels_curated.py:39). The Sanger depth ratio **0.63085** reproduces, but compares differently processed matrices. It cannot establish biological/global depletion compression. Their nonessential medians also differ: approximately **−0.00195 versus +0.12073**. Broad’s near-identical essential depths are partly imposed by upstream Chronos scaling; further essential normalization cannot recover missing global dynamics.

   Only **one of 1,241 screens** has CPD. Fewer doublings and slow protein turnover therefore remain hypotheses. The ribosomal relative shift survives shared-gene percentile checks, which supports the pattern, not the proposed mechanism.

   **Smallest fix:** Present relative ribosomal weakening as the finding and depletion kinetics as a testable explanation. Remove claims that a doubling artifact has been established or corrected.

4. **Medium — The “Humagne-only” sensitivity is not Humagne-only.**  
   **Evidence:** [medium_attribution_v2.py:120](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:120). Screens are averaged by model before filtering on the model’s first library label. **Four of the five selected FBS controls average Humagne with corrected Avana measurements.** Two other eligible Humagne controls are omitted.

   Verified screen-level filtering produces **seven FBS models**, correlation with main D **0.7813**, and only **six significant hits** under the same normalized hit rule.

   **Smallest fix:** Filter screens to Humagne before model aggregation; regenerate this sensitivity and its descriptions.

5. **Medium — “Sequestered” and “held-out confirmation” overstate independence.**  
   **Evidence:** [medium_attribution_v2.py:79](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:79), [heldout.py:40](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2_heldout.py:40). **Five of 27 calibration models are reserved-patient models.** Missing-value filtering/imputation also precedes exclusion. Held-out contrasts use 285 FBS controls, including all 207 development controls, so their errors share a baseline with development estimates.

   This is consequential for interpretation, although my sensitivities were reassuring: development-only calibration gives **388/456 medium flags, 85.1%**. Using the 78 reserved FBS controls and development-only offset gives held-out D correlation **0.9727**, slope **0.9454**, and 100% sign agreement against the original medium-hit estimates.

   **Smallest fix:** Exclude reserved patients before calibration/preprocessing; use disjoint controls for confirmation, or explicitly describe shared-baseline confirmation.

6. **Medium — Zero format candidates is a low-power, asymmetric-rule result, not evidence that format contributes nothing.**  
   **Evidence:** [flag_hits:64](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:64). Medium support uses nominal A `p<0.05`; format support requires genome-wide F `q<0.05`. Verified: the minimum normalized F q-value is **0.999920**. Thus the “F does not dominate” safeguard never excludes anything. Nevertheless, **39/449 hits have same-direction F/D≥0.5**, and nine also satisfy A/D<0.25. LSM7 passes the corresponding nominal-p format rule.

   The literature framing should also acknowledge that Neiswender already identified seven format-associated genes and experimentally validated ITGB1’s format dependence. The useful novelty here is the catalogue-wide reanalysis, not discovering ITGB1 or first separating medium from format. [Neiswender et al.](https://www.nature.com/articles/s41586-026-10843-7)

   **Smallest fix:** Say “no format effects detected at the specified FDR,” report symmetric-threshold sensitivity, and acknowledge the existing format-positive experiments.

7. **Medium — The title generalizes a conditional fraction to the published catalogues.**  
   **Evidence:** [manuscript:1](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:1), `medium_attribution_v2.json/published_hits`. Verified Broad published gains comprise **137 medium, 21 unresolved, 127 not reproduced**. Thus **137/158=86.7%** applies to reproduced hits, whereas **137/285=48.1%** applies to the full examined published list. Only **5/18** Sanger headline genes receive medium flags.

   This does not establish that the remaining genes are non-medium effects; their attribution is unestablished. It does mean the title’s catalogue-wide “Most” exceeds the denominator actually supported.

   **Smallest fix:** Scope the headline to the newly identified or reproduced lineage-adjusted differences and show unconditional as well as conditional fractions.

8. **Medium — HPLM arithmetic is correct, but the interpretation and labels are not.**  
   **Evidence:** [hplm_reverse_test.py:59](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/hplm_reverse_test.py:59), [manuscript:29](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:29). `Z>3` selects relative differences, not genes “essential only in RPMI.” For example, RPL27 scores **−1.61 versus −1.20**. The enrichment table combines **five organoid dependency gains with four losses**. Restricting to medium-attributable gains gives **OR=4.550, p=0.00635**, rather than the combined **OR=4.608, p=0.000298**. “4.6-fold enrichment” is specifically an odds ratio; the observed prevalence enrichment is **4.19-fold**.

   Both experimental arms contain dialyzed serum, so this is not an LDL/serum-removal reversal experiment. SQLE’s opposite response is real, but the shared causal mechanism is unproven. [Rossiter et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8172426/)

   **Smallest fix:** Use “relatively more essential in RPMI,” report direction-separated enrichment and explicitly label the odds ratio; retain SQLE as a specificity observation.

9. **Medium — The Sanger frequency audit double-weights dual-library models and does not test threshold fragility.**  
   **Evidence:** [sanger_tables_audit.py:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sanger_tables_audit.py:23). Table 5 contains **178 model–library profiles across 162 models**; 16 models contribute twice. Averaging directly by gene weights those models twice.

   Collapsing model–gene records first changes exclusive/headline median frequencies from **0.80337/0.68820** to **0.80247/0.69753**. The broad prevalence finding survives. However, binary prevalence cannot show robustness to changing the BAGEL threshold.

   **Smallest fix:** Aggregate within model first and replace “not threshold-fragile” with a statement about depletion-call prevalence, unless continuous-score threshold sensitivity is actually evaluated.

10. **Medium — Several manuscript claims contradict the released gene-level tables.**  
    **Evidence:** [manuscript:39](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:39), manuscript lines 7 and 35, [FINDINGS:187](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/FINDINGS.md:187).

    - **10/38 ribosomal and 5/35 spliceosome genes** are medium-attributable **losses**, not 12/38 and 7/35. The larger numbers include gains: RPL18/RPS9 and TXNL4A/U2AF2.
    - DDX3X and ITGB1 are not the only published-catalogue hits with low adherent reproduction. **COASY, LSM7, and UTP4** are also unresolved Broad published gains with A/D<0.3.
    - Calling all eight reproduced Sanger headline genes “medium-consistent” obscures that only five pass the medium rule; the other three remain unresolved.
    - SCAP fails the nominal A significance requirement (**p=0.0790**); its ratio CI lower bound is actually positive (**0.01764**). The FINDINGS explanation should identify the failing criterion.

    **Smallest fix:** Correct these statements directly from the table, including direction when counting panel flags.

11. **Low — Four-decimal export changes a threshold decision on rereading.**  
    **Evidence:** [medium_attribution_v2.py:144](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:144), raw CSV entry `ATG14`. Its exported D is **−0.2500**, while its stored flag is `not_a_hit`. Reapplying the documented rule to the exported raw CSV yields **873 hits instead of 872**. Normalized classifications round-trip correctly.

    **Smallest fix:** Export enough numerical precision to preserve threshold decisions.

12. **Low — The release is internally consistent but its reproduction instructions are incomplete.**  
    **Evidence:** [release README:22](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/release_v1/README.md:22). The run order omits expression, HPLM, and the Sanger-table audit; their additional inputs are not fully listed. `sanger_essdepth_v1.json`, required by figure generation, has no generating script in the reviewed source tree. The bundle contains `code/`, while instructions invoke `src/`; file-relative ROOT resolution requires an explicit installation/layout instruction.

    **Smallest fix:** Document the actual placement, complete input/run list, and provide the small essential-depth calculation. No packaging overhaul is needed.

## CHECKS RUN

- **Full main-analysis recomputation:** Loaded ScreenGeneEffect and metadata, reconstructed calibration, reference sets, model means, contrasts, and flags. Both scales reproduce all saved classifications. Retained **17,524 genes**, **981 essentials**, **5,042 nonessentials**.

  | Scale | Gains | Medium gains | Losses | Medium losses |
  |---|---:|---:|---:|---:|
  | Normalized | 240 | 204 — 85.00% | 209 | 175 — 83.73% |
  | Raw | 520 | 421 — 80.96% | 352 | 263 — 74.72% |

- **Estimator checks:** Compared 25 gene/contrast fits against independent statsmodels OLS. Maximum coefficient/SE/p differences were approximately **3.5×10⁻¹⁵ / 3.6×10⁻¹⁶ / 1.2×10⁻¹⁴**. Actual designs were full rank; D/A/F/S/Humagne residual dof were **265/206/67/87/63**. BH agreed with statsmodels within **2.2×10⁻¹⁶**. V2 correctly uses t rather than normal tails.

- **Ratio covariance:** The omitted delta-method term is `−2A·Cov(A,D)/D³`. For same-sign medium candidates and the shared FBS baseline, its omission increases variance. The claimed conservative direction is correct **conditionally on the fitted preprocessing/calibration**, not an assurance about total uncertainty.

- **Library invariance:** All **1,019 Avana screens are FBS**; none are organoid/TSM. Thus applying the offset here does **not require demonstrating an Avana offset invariant across media**. Estimation uncertainty and transfer across FBS models are the relevant concerns.

- **Normalized slopes, gains/losses:** A-on-D **0.88242/0.89698**; F-on-D **0.13540/0.13861**; S-on-D **0.53546/−0.04203**.

- **Held-out/LOO:** Saved medium-hit confirmation reproduces **r=0.98125**, D slope **0.97159**, A slope **0.87788**, sign agreement **100%**. Recomputing LOO with both A and F refitted preserves minimum medium-flag retention **94.195%**. The LOO script’s promised library-offset LOO is not implemented; its actual adherent robustness result is sound.

- **Catalogue joins:** Broad strict gains reproduce **16 medium/1 unresolved**; published losses **130 medium/23 unresolved/99 not reproduced**, including one direction reversal among reproduced hits. Sanger exclusives: **93/97 covered**, 20 differential hits, 14 gains/6 losses. Headline: **16/18 covered**, five medium/three unresolved/eight not reproduced. Survivor CSV contains exactly the **70 unresolved normalized hits**.

- **Sanger matrices and coverage:** Reconstructed **16,562×162 organoid** and **17,647×930 2D** matrices. Essential depths **−0.955756/−1.515032**; ratio **0.630849**. Curated spliceosome scaled medians **1.33684/1.11226**; ribosomal **1.25457/1.56642**. Restricting both matrices and panels to shared genes preserves the conclusions. Shared-universe ribosomal percentiles are **0.02109/0.01007**; mevalonate **0.09931/0.38210**. ITGB1’s original percentile difference is **−0.23257**.

- **Expression:** Independently rebuilt keyed model/class/format units, confirming **69 dome, 10 organoid-adherent, 205 FBS-adherent** units. Multiple profiles aggregate correctly on the embedded-condition route. Expression medians: mevalonate **+0.358403**, heme **−0.473688**, fatty-acid synthesis **−0.357190**; SQLE **+0.754071**, LDLR **+0.607724**. Genome-wide correlation **−0.000999**.

- **HPLM:** Verified spreadsheet headers and three-column focused-screen blocks. **18,270 genes**, **15,940 joined**; correlation **0.0413275**; SQLE delta **+0.441896**, Z **3.808033**. Combined enrichment table is exactly `[[9,88],[344,15499]]`.

- **Data/release checks:** No duplicate retained Broad gene symbols, no QC-retained screen metadata conflicts, and no models mixing broad medium classes or formats during dependency aggregation. All three supplied tests passed. Release/source copies, supplementary contents, and recorded archive hashes agree; PDF has seven pages. The validator passes **29/29** with its final write suppressed. Those checks establish bundle consistency, not the causal claims above.