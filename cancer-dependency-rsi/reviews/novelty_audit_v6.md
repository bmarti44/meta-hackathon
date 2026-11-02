# Novelty audit v6 — coverage correction delta (supersedes v5 search-coverage statements; claim unchanged)

Per sol-high issue 5 (87/100), verified: cached XML bibliographies contain S1 76 / S2 103 / S3 41
references; Europe PMC API returned 72/96/38 — a subset (omits e.g. S3 ref 41, its Zenodo package
10.5281/zenodo.22472622, verified live: reproducibility zip 37.9 MB + sha256 file; contents not
inspected — closest-code check remains OUTSTANDING). v5/dossier "complete reference lists" wording
is corrected to "Europe PMC-returned subsets, title-screened".

New dispositions (generations/sgen001/novelty_fix_searches.json):
- PMID 32238925 (Han et al., Nature 2020, CRISPR screens in cancer spheroids): genome-wide 2D-vs-3D
  screens in lung spheroids establish 3D-specific vulnerabilities — adjacent prior for
  format-dependent dependency existence. EXCLUDED as same-claim prior: no paired-format lability
  predictor, no external organoid displacement endpoint, no baseline-adjusted panel association.
- S2 forward citations (Europe PMC, PMID 42557320): 5 records = S2 self, S1, HCMI compendium,
  a 2D/3D review, immunofluorescence methods. None reports the locked relationship (title-level).
- S1/S3 forward + concept/preprint screens as in v5.

Still outstanding (C1/C6 remain PARTIAL): S3 Zenodo code contents, S1 supplement PDF line
inspection, exhaustive broad-set screening beyond relevance top-25, non-Europe-PMC sources,
full-text (not title) screening of all backward references.
