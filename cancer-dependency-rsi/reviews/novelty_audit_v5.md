# Novelty audit v5 — corrections + retained search completion (supersedes v4 §§2–3; v4 §§1,4,5 unchanged)

Date: 2026-10-28. Fixes v3-package review issues #5 (MEDIUM) and #7 (LOW). Search artifacts: `reviews/novelty_v5_searches.json` (Europe PMC REST, executed this date, HTTP 200 all queries).

## Corrections to v4

- S3 within-organoid ranking is in **§2.10.1 (methods) and §3.7 "Retrospective Gene Ranking Within Individual Organoids", Tables S17–S19** (mean within-organoid Spearman 0.343 Broad-94 / 0.429 Sanger-148 vs fixed-2D-mean 0.206/0.200 and lineage-only 0.275/0.388). v4's "§3.5 synthesis/Fig. 6" citation is retracted (§3.5 is target-wise cross-cohort synthesis). Substance unchanged: S3 ranks genes within organoids from *expression predictions* (20 genes); it does not test *measured format lability* against displacement.
- v4 §3 "retained in session record" is replaced by the resolvable artifact above.

## Additional checks executed (screening dispositions)

| check | result |
|---|---|
| S2 exact DOI `EXT_ID:10.1038/s41586-026-10830-y` | 0 hits (Europe PMC DOI indexing gap); S2 title search: 1 hit = S2 itself. S2 identity confirmed; no citing/derived lability analysis via this route |
| Forward citations of S1 (PMID 42557315) | 3: HCMI compendium (companion resource; reports models/medium context, no lability→displacement test), S1 self-record, volumetric immunofluorescence (unrelated). None reports the locked relationship |
| Forward citations of S3 (PMID 42883455) | 0 (Oct 2026 paper; citation lag — weak evidence, labeled as such) |
| Broad concept search (2024–2026, organoid×CRISPR×dependency×culture×transfer/rank) | 3,634 hits; relevance-ranked top 25 screened: S1, S3, S2 + reviews and disease-model papers; no other primary dependency-transfer study located in top 25. **Recall limit explicit: hits beyond top-25 unscreened; this is a relevance screen, not exhaustive screening** |
| Preprint concept search (SRC:PPR, organoid×CRISPR×dependency×format/medium/minipool) | 15 hits, all screened by title: drug/target and platform preprints; none tests measured environmental lability vs organoid displacement |

## Still outstanding (explicit; C1/C6 remain PARTIAL until adjudicated)

- Backward-citation (reference-list) systematic check for S1–S3 and full supplement/code inspection beyond S1 minipool code route and S3 Tables S17–S19 (supplement PDFs not inspected line-by-line).
- Exhaustive screening of the 3,634-hit broad set (only relevance top-25 screened).
- Non-Europe-PMC preprint servers and non-English literature.

## Adjudication basis (unchanged claim)

Residual novelty remains exactly as v4 §2: the joined measured-lability→external-displacement test, baseline-adjusted, panel-wide, predeclared δ — not located in S1/S2/S3, their located citations, the retained PubMed/Europe PMC searches, or the preprint screen, under the stated limits. Reviewer adjudicates; lead does not self-certify.
