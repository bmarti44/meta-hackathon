# Submission checklist — do these two things to finish GOAL v4 deliverables 4–5

## A. Post the preprint (bioRxiv, ~15 min)
1. Fill authors/affiliations/corresponding author: edit `manuscript/manuscript_draft_v2.md`
   (or directly in the PDF source), then regenerate the PDF:
   `.venv/bin/python src/render_pdf.py` (from `cancer-dependency-rsi/`).
   Until then `manuscript_v2.pdf` carries bracketed placeholders.
2. Go to https://www.biorxiv.org/submit-a-manuscript (your account).
   - Manuscript file: `release_v1/manuscript_v2.pdf` (7 pages, figures embedded).
   - Title/abstract/subject: copy from `release_v1/biorxiv_fields.txt`
     (abstract ~289 words; suggested subject: Cancer Biology; license CC-BY).
   - Supplementary material: upload `release_v1/supplementary_tables.zip`
     (attribution tables raw/normalized, held-out contrasts, survivor
     candidates, run-summary JSONs).
   - Code: link or upload `release_v1/code/` (or push repo and cite URL).
3. After posting: send me the DOI — remaining work is only to stamp it into
   the release README/STATUS and close the goal.

Validation: `src/validate_release.py` → 33/33 checks (zip integrity, cited
paths, headline numbers re-derived from artifacts, no stale panel numbers,
abstract length). Record: `release_v1/VALIDATION.json` incl. per-file
SHA-256 (computed over the zip read at validation time; file contents are
what matters).

## B. Send the wet-lab proposal (~5 min)
- Email draft: `release_v1/wetlab_cover_email.txt` (fill [Name]/[Your name]).
- Attach: `wetlab_proposal_v1.md`, `manuscript_v2.pdf`, and either
  `tables/medium_attribution_v2_norm.csv` or the whole `release_v1.zip`.
- Best recipients: a lab actively growing OPAC/organoid-medium models from
  the NextGen/HCMI collections, or any collaborator following up
  Herranz-Ors-nominated targets (sterol axis especially).

## C. If a collaborator bites
Their LDL add-back / drug-shift result either falsifies (pre-agreed: IC50
within 2x in >=3/4 models) or confirms the medium prediction; analysis
support is already promised in the email. Any resulting screen data can be
scored against the released tables directly.
