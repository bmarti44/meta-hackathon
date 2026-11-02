# HANDOFF — organoid medium-attribution project (final state, 2026-10-30)

Everything below is on disk in this repo. Start here.

## One-paragraph summary
Genome-wide audit of the two 2026 Nature organoid CRISPR dependency
catalogues (Neiswender/Broad, Herranz-Ors/Sanger) in DepMap 26Q3:
of 456 differential dependencies, 84–86% are medium-consistent (reproduced
in adherent organoid-medium culture; HC3-robust 75–82%; bootstrap slope
0.90 [0.82–0.99]; disjoint held-out patients slope 0.96), 1 format
candidate (LSM7; 0 at 5% FDR). Published Broad gains: 47% medium-consistent
overall, 87% of those replicating under lineage adjustment. Sanger
headline-18: 5/8 replicating genes medium-consistent (sterol/SREBP axis).
Ribosomal relative weakening persists in both assays; depletion kinetics
is a testable, unproven explanation (CPD recorded for 1/1,241 screens).

## Verification status
- Independent skeptical review (Codex gpt-6-astra, xhigh): 5 rounds
  68 → 82 → 89 → 89 → 95/100 "ship it". Trail: cancer-dependency-rsi/reviews/
  astra_review_r1..r5.md + *_dispositions.md. Every verified issue fixed.
- Deep-web novelty audit (uncapped Astra live search, 230+ searches):
  PARTIALLY TRUE — narrow catalogue-audit claim unreported as of 2026-10-30;
  framing corrected to credit precedents (Lagziel 2019, Pacini 2021,
  Liang 2025, Zaidi & Sawyers 2026). Report: reviews/astra_novelty_research3.md
  (run 1 timed out pre-synthesis; run 2 was stopped by user in favor of the
  uncapped run 3; events/receipts retained alongside).
- Release validator: 33/33 checks over archived contents
  (release_v1/VALIDATION.json, SHA-256 manifest).
- Tests: 105 passed, 1 skipped (1 pre-existing timing flake in
  tests/test_tree_cpu.py passes in isolation).

## Key files (cancer-dependency-rsi/)
- Manuscript: manuscript/manuscript_draft_v2.md (v2r3) + PDF in release_v1/manuscript_v2.pdf (7 pp, author placeholders)
- Findings log: FINDINGS.md (GOAL v4 section + corrections); STATUS.md (chronology)
- Tables: generations/medium_attribution_v2_{norm,raw}.csv (+ heldout, boot freq, survivor candidates)
- Code: src/medium_attribution*.py, sanger_*.py, panels_curated.py,
  expression_triangulation.py, hplm_reverse_test.py, make_figures.py,
  render_pdf.py, validate_release.py
- Bundle: release_v1/ and release_v1.zip (manuscript, figures, tables,
  code, reviews, biorxiv_fields.txt, supplementary_tables.zip,
  wetlab_cover_email.txt, SUBMISSION_CHECKLIST.md, VALIDATION.json)
- External data acquired this session: data/raw/hplm_rossiter2021/
  (PMC8172426 supplements; user-downloaded)

## Remaining actions (user only)
1. Fill authors/affiliations in manuscript, regenerate PDF:
   `.venv/bin/python src/render_pdf.py` (from cancer-dependency-rsi/).
2. Post to bioRxiv using release_v1/biorxiv_fields.txt + manuscript_v2.pdf
   + supplementary_tables.zip. Steps: release_v1/SUBMISSION_CHECKLIST.md.
3. Send release_v1/wetlab_cover_email.txt + wetlab_proposal_v1.md to a
   wet-lab collaborator (LDL add-back test, pre-agreed falsification).
4. Send the DOI back to stamp into release README/STATUS and close the goal.

## Honest limits (do not overclaim)
Observational consistency, not causal proof; adherent comparators 6/9
lineages, mixed formulations; per-gene flags uncertain (bootstrap
frequencies released); true per-doubling correction impossible in 26Q3.
Novelty = first systematic per-gene audit of these two catalogues,
nothing broader.
