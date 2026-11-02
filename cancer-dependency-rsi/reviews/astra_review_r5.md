**SCORE: 95/100**

**VERDICT: Ship it for the scoped technical-note claims.** Both round-4 issues are fixed, including the rendered PDF and distributed archive. No further experiments are needed for the stated descriptive claims.

**Per-item disposition checks**

| Round-4 item | Disposition and evidence |
|---|---|
| **Medium — Patient-transfer overclaim** | **Fixed.** The [manuscript introduction](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v2.md:11), [proposal](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/wetlab_proposal_v1.md:6), and [email](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/release_v1/wetlab_cover_email.txt:18) explicitly leave tumor transfer untested. Proposal line 12 now describes persistent sensitivity as warranting follow-up. PDF page 1 contains the corrected introduction. Source/release copies and archived versions agree. |
| **Low — Stale release numbers** | **Fixed.** Proposal and email state **17,525 genes**, matching both main tables. The email’s bundle-size literal is removed. The [checklist](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/release_v1/SUBMISSION_CHECKLIST.md:11) states **289 abstract words** and **33/33 checks**; both independently verified. Submission-field title/abstract match the manuscript. No targeted stale literals remain on active surfaces or in PDF text; historical reviews retain their historical values. |

**NEW issues by severity**

**Critical/high/medium/low: none found.** No additional issue at low-or-above severity, no regression identified, and no further fix required.

**CHECKS RUN**

All generated outputs were captured in memory; repository artifacts were not modified.

- **Release integrity:** Fresh validator **33/33**, identical to saved validation. **49/49 hashes**, **50/50 archive files**, **43/43 source/release pairs**, and **16/16 supplementary tables** match; inventories complete, no duplicate archive entries. Changing one archived classification correctly reduces validation to **32/33**.
- **Main recomputation:** Both CSVs reproduce byte-for-byte; summary JSON matches except timestamp. Across **17,525 genes per scale**, zero primary/FDR classification discrepancies. Normalized gains: **214/249 = 85.9438%** medium-consistent; losses: **173/207 = 83.5749%**. **LSM7 alone** qualifies under nominal format criteria; none under FDR.
- **Bootstrap:** All **150 draws** reproduce summary and frequencies exactly. Full-gene identity check has zero flag discrepancies. Slope **0.89814**, interval **[0.81641, 0.98818]**; MAU2 frequency **0.48**.
- **Manuscript spot checks:** Catalogue joins, named genes, curated-panel counts, expression summaries, and Sanger depth agree. Held-out slope **0.96338**, correlation **0.97413**, sign agreement **100%**. Independently recomputed HPLM enrichment: **OR 4.38424**, **p=0.00735548**.
- **Presentation:** Seven-page PDF matches an in-memory rerender’s text and embedded images; all **27 body blocks** and three captions present. Three figures and survivor table regenerate byte-for-byte.
- **Focused tests:** **6/6 pass.**