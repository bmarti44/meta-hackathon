**SCORE: 89/100**

**VERDICT: Not quite ship-ready as distributed.** The computational technical note now passes. One residual claim about transfer to patients and a few stale release numbers need small editorial fixes. No further experiments or methodological expansion are required for the scoped descriptive claims.

**Per-item dispositions**

| Item | Disposition and evidence |
|---|---|
| **1. Bootstrap NaN fix** | **Fixed.** [weighted_offset()](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2_boot.py:27) uses a missingness-aware numerator and gene-specific denominator. Per-model library means also use pandas skipna semantics. Actual calibration contains **72 missing differences across 66 genes**; all-one weighted offsets exactly match `library_offset`. Additional fixtures with partially missing screens, missing pairs, zero weights, and no valid pairs also agree. |
| **Identity and honest test** | **Fixed.** [Identity validation](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/medium_attribution_v2_boot.py:113) now invokes the weighted routine. Independent inspection of its full output finds **zero primary/FDR flag mismatches across 17,525 genes**. The [new unit test](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_medium_attribution.py:85) passes currently and fails when the old inline sum is substituted in memory. |
| **2. Wet-lab materials** | **Partially fixed.** The 84–86% framing, single format candidate/none-at-FDR distinction, observational caveat, and curated ribosomal **+0.17** description are corrected. Transfer language and some numbers remain defective below. The internal finding review has the superseded banner; source and release copies match. |
| **3. Shorthand purge** | **Fixed on active v2 surfaces.** No targeted shorthand remains in the current manuscript, relevant READMEs, figure generator, renderer, or actual PDF. Historical draft/review text retains occurrences; these do not appear in the current rendered manuscript. |
| **4. Regressions and packaging** | **Pass.** Both main CSVs, bootstrap artifacts, three figures, and survivor table regenerate exactly. PDF text and embedded images match an in-memory rerender. Validator passes **33/33** and detects archived-content mutations. All **47/47** final manifest hashes and **16/16** supplementary tables match. |
| **5. Scoped scientific claims** | **Supported.** The medium-consistency catalogue, uncertainty-qualified aggregate result, and relative ribosomal weakening are defensible technical-note findings. Patient transfer remains untested. |

**NEW/residual issues by severity**

**Critical/high: none. No new computational defect found.**

1. **Medium — The transfer claim remains stronger than the proposed experiment permits.**  
   The [email](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/release_v1/wetlab_cover_email.txt:18) still says dependencies “will not transfer in vivo” and calls that testable in two weeks. The [proposal](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/wetlab_proposal_v1.md:6) now labels this a prediction, but still presents the experiment as testing patient transfer. The [manuscript introduction](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:11) similarly says add-back tests that hypothesis “directly.” Proposal line 12 also equates persistent sensitivity with “real biology.”

   **Smallest fix:** State: “LDL rescue would support LDL limitation as a contributor in these cultured models; transfer to tumors remains untested.” Describe persistent sensitivity as warranting follow-up. Apply consistently to manuscript, proposal, and email; regenerate their release copies/PDF.

2. **Low — Ancillary release numbers remain stale.**  
   The [email](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/release_v1/wetlab_cover_email.txt:32) advertises **17,524 genes**, versus **17,525**, and a **3 MB** bundle, versus **11,477,786 bytes**. The [submission checklist](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/release_v1/SUBMISSION_CHECKLIST.md:11) still says **271 abstract words** and **29/29 checks**, versus **289** and **33/33**.

   **Smallest fix:** Update these literals or omit the bundle size, then rebuild the archive and refresh validation.

**CHECKS RUN**

All analysis outputs were intercepted in memory; repository artifacts were not modified.

- **Full main recomputation:** Both released CSVs reproduced byte-for-byte; zero primary or FDR classification discrepancies.

  | Scale | Gains | Medium gains | Losses | Medium losses |
  |---|---:|---:|---:|---:|
  | Normalized | 249 | 214 — **85.9438%** | 207 | 173 — **83.5749%** |
  | Raw | 533 | 441 — **82.7392%** | 336 | 250 — **74.4048%** |

- **Bootstrap:** Reran all **150** draws; summary JSON and frequency CSV reproduce exactly. Weighted offsets agree exactly with explicit pandas resampling.

  | Statistic | Recomputed |
  |---|---:|
  | MAU2 medium frequency | **72/150 = 0.48** |
  | MAU2 identity D | **−0.271467566** |
  | A-on-D slope median | **0.898143546** |
  | Slope percentile interval | **[0.816412900, 0.988184925]** |
  | Medium-fraction median | **0.638157895** |
  | Medium-fraction interval | **[0.486239035, 0.759375000]** |
  | Frequency ≥0.5 / ≥0.9 | **329/456 / 85/456** |

- **Validator mutation checks:** One archived medium flag changed → **32/33**; all 387 changed → **31/33**. Saved validation equals fresh validation; all **48** archive files match the release directory.
- **Presentation:** Seven-page PDF contains every current body paragraph and all three current captions. Three PNGs and the survivor CSV regenerate byte-for-byte.
- **Tests:** **6/6** focused tests pass; the old-sum mutation fails the new regression test.