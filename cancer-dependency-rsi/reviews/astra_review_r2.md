**SCORE: 82/100**

**VERDICT:** Substantial improvement. The regenerated main results and disjoint held-out confirmation reproduce. Not ready to ship: the bootstrap implements a different estimator and fails to preserve calibration–analysis covariance. Several reporting and release-validation defects also remain. No headline reversal was verified.

**Round-one disposition checks**

| # | Status | Evidence |
|---|---|---|
| 1. Causal attribution | **Partially fixed** | Title, main discussion, formulation-family qualification, and common-support sensitivity are corrected. Figure labels still say “same/fixed medium” and “medium-attributable”; HPLM prose retains an unsupported causal conclusion. |
| 2. Uncertainty | **Partially fixed** | HC3 is correct, including real-data comparisons with statsmodels. Bootstrap numbers reproduce, but its preprocessing and resampling are incorrect for the claimed joint uncertainty analysis; see H1. |
| 3. Depletion kinetics | **Fixed** | [Manuscript:37–45](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:37) distinguishes relative weakening from an untested mechanism and acknowledges processing and Chronos-rescaling limitations. |
| 4. Humagne sensitivity | **Fixed** | [Screen filtering precedes aggregation](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:151). Seven FBS controls; recomputed normalized correlation **0.774959**, slope **0.827863**. |
| 5. Hold-out contamination | **Fixed computationally** | Development exclusion precedes filtering/calibration/imputation in all four scripts. Held-out preprocessing uses development estimates; controls are **78 reserved versus 207 development FBS models**, with zero model or patient overlap. |
| 6. Format rule | **Partially fixed** | [Implementation](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2.py:66) includes nominal F significance and `ratio_F_lo>0`; normalized LSM7 alone qualifies, versus zero under `flag_fdr`. Neiswender’s seven format genes and named integrins are accurately acknowledged. Documentation/figures remain inconsistent. |
| 7. Title denominator | **Fixed** | “Most reproduced” is appropriately conditional. Broad gains: **135/285=47.37% overall; 135/156=86.54% among reproduced hits**. |
| 8. HPLM | **Partially fixed** | Direction-separated enrichment, relative-essentiality labels, odds/prevalence distinction, and dialyzed-serum caveat are correct. “A physiological formulation relieves several that organoid formulation creates” still exceeds the cross-system evidence. |
| 9. Sanger weighting | **Fixed** | [Within-model collapse](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sanger_tables_audit.py:23) reproduces medians **0.802469/0.697531** across 162 models. Threshold-robustness claim removed. |
| 10. Specific reporting errors | **Fixed for the listed corrections** | Ribosomal **13 losses/2 gains of 38**; spliceosome **5/2 of 35**. Sanger headline classification is five medium/three unresolved. SCAP fails A significance: **p=0.0572325**, despite positive ratio lower bound **0.082402**. Other stale numbers remain below. |
| 11. Export precision | **Fixed** | Both exported scales reproduce every stored hit decision and primary flag. Normalized **456**, raw **869** hits; zero discrepancies. |
| 12. Reproduction instructions | **Partially fixed** | Layout, additional inputs, run order, and essential-depth generator are supplied and work. Release documentation and validation still need correction; see M2–M3. |

**New or residual issues**

**Critical: none.**

**High — H1. The “joint bootstrap” neither bootstraps the main estimator nor preserves shared-model covariance.**

Evidence: [bootstrap preprocessing:28](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2_boot.py:28), [reference sets:46](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2_boot.py:46), [independent draws:61](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2_boot.py:61).

- Bootstrap reference sets are selected **before library correction**, giving **1,003 essentials/5,729 nonessentials**, versus the main estimator’s **978/5,027**. They are therefore not the advertised frozen point-estimate sets.
- Bootstrap calibration follows imputation; main calibration precedes it. Offsets differ by more than \(10^{-5}\) for **66 genes**, with maximum difference **0.027988** at TTF2.
- Running the bootstrap estimator with each model included once changes **26 hit memberships and 34 classifications**, including **20 classifications among the original 456 hits**. This directly demonstrates an estimator mismatch.
- Calibration and analysis models receive independent multiplicities, although **six calibration models also enter D/A/F analysis**. Their covariance is lost.

**Smallest fix:** Share preprocessing with the main analysis, freeze the actual corrected-data reference sets if retaining that simplification, and apply common resampling multiplicities to overlapping calibration/analysis units. Regenerate intervals/frequencies and qualify the manuscript’s “total uncertainty” claim.

**Medium — M1. LOO retention does not apply the new classification rule.**

[LOO:49–62](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2_loo.py:49) refits A only and omits the F safeguard from `still_medium`.

Recomputing both A and F changes retention for two omissions from **95.0904% to 94.8320%**. The actual minimum remains **93.5401%**, contradicting “≥94%” in [manuscript:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:23).

**Smallest fix:** Refit F after each omission, call `flag_hits`, and report the actual minimum.

**Medium — M2. VALIDATION.json does not validate the released numerical contents and contains stale hashes.**

[Validator:42–63](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/validate_release.py:42) genuinely computes some checks from local CSVs—it does **not merely echo constants**. However, archive checks mostly establish presence/integrity; numerical checks read `generations/`, not archived tables.

Verified:

- **28 of 39 recorded hashes** disagree with the current archive; six archive files are absent from the hash inventory.
- Replacing archived medium flags with `unresolved` in memory still produces **31/31 passing checks**.
- Export validation checks only normalized hit **counts**, not both scales or gene identities.
- Bootstrap validation only checks file presence.
- The old Sanger headline target **0.688** passes because its tolerance also accepts the new **0.697531**.

**Smallest fix:** Validate the actual archived contents against recomputed expectations, check both scales by gene, update numeric assertions, and generate a manifest for the final bundle excluding its own self-hash.

**Medium — M3. Documentation and figures did not fully follow the rule and interpretation changes.**

- [Release README:49](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/release_v1/README.md:49) still states **449 hits/zero format candidates**.
- [Column/rule README:22–35](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/RELEASE_README.md:22) still specifies five Humagne controls, 27 calibrators, and the old F-q primary rule.
- [Figure code:24–28](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/make_figures.py:24) labels **every non-medium hit “unresolved,” including LSM7**, and retains same/fixed-medium causal shorthand.
- [Manuscript:19](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:19) calls the format rule “mirror-image” without specifying its additional `ratio_A<0.25` requirement; [line 29](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:29) retains the HPLM causal overstatement noted above.

**Smallest fix:** Synchronize documentation with the implemented rules, give format candidates their own figure class, use formulation-family/medium-consistent labels, and describe HPLM as cross-system concordance.

**Low — L1. Several manuscript numbers remain stale.**

At [line 23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:23), same-direction F/D≥0.5 occurs in **34**, not 39 hits. At [line 51](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:51), reference sets are **978/5,027**, not 981/5,042. At [line 35](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:35), headline prevalence is **69.753%**, conventionally rounded to 70%.

**Smallest fix:** Refresh these statements from artifacts and add exact checks.

**Checks run**

All execution was read-only; output writes were intercepted in memory.

- **Full main recomputation:** 17,525 retained genes; 22 development calibrators. Every saved primary and FDR-variant classification reproduced.

  | Scale | Gains | Medium gains | Losses | Medium losses |
  |---|---:|---:|---:|---:|
  | Normalized | 249 | 214 — 85.9438% | 207 | 173 — 83.5749% |
  | Raw | 533 | 441 — 82.7392% | 336 | 250 — 74.4048% |

- **Held-out:** Full reconstruction and separate calculation from saved tables agree. Among 387 normalized medium hits: **r=0.974132**, D slope **0.963379**, A slope **0.896255**, sign agreement **100%**. Raw: r **0.965393**, D slope **0.973826**, sign agreement **99.4211%**.
- **HC3:** Seventy real gene/contrast comparisons with statsmodels; maximum coefficient/HC3-SE differences **8.99×10⁻¹⁵ / 2.44×10⁻¹⁵**. Normalized HC3 fractions reproduce **203/249=81.5261%** and **156/207=75.3623%**.
- **Format/tests:** Five tests pass. The LSM7-like test fails under the old FDR rule; HC3 testing requires the new output. Enlarging F uncertainty makes the ratio-CI gate reject LSM7. Actual LSM7: **F p=0.039402**, F/D **0.801904**, lower bound **0.155305**.
- **Bootstrap:** All 150 shipped replicates reproduce. Slope median **0.898719**, percentile interval **[0.814182, 0.984502]**. Fixed-456-hit flag-fraction median **0.644737**, interval **[0.507950, 0.743037]**. Frequencies ≥0.5: **326/456**; ≥0.9: **92/456**. Offset is re-estimated each replicate; frequency arithmetic is correct; no resampled-design index misalignment found. These findings do not resolve H1.
- **Common support:** Six lineages; **38 domes, nine adherent organoid models, 125 FBS controls**. Hits are reselected after refitting: **451** normalized hits; slope **0.891476**, median A/D **0.891469**, **90.2439%** with A/D≥0.5.
- **Sanger/HPLM:** Sanger audit, essential-depth generator, and curated-panel outputs reproduce exactly. RPMI-side gains enrichment table **[[5,92],[194,15650]]** gives OR **4.384245**, prevalence ratio **4.209799**, p **0.00735548**.
- **Figures/release:** All three PNGs and the **68-row unresolved survivor CSV** regenerate byte-for-byte. Source/release copies, supplementary ZIP tables, and release directory/archive contents agree. The remaining figure defects are semantic, not stale plotting data.