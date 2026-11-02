# Source verification notes (Phase 1, started 2026-10-28)

Reachability (2026-10-28): all 8 seed URLs HTTP 200 via curl.

Title/abstract-level verification (methods NOT yet read — Phase 1 continues):
- S1 PMC13581591 = "A dependency map enhanced with next-generation 3D cancer models" — abstract confirms 147 genome-scale CRISPR screens, NextGen organoids/spheroids, 10 cancer types. Matches spec seed.
- S2 PMC13581617 = "A tumour-derived organoid biobank maps cancer gene dependencies" — abstract (via Europe PMC API; PMC direct fetch hit reCAPTCHA) confirms 256 clinically annotated tumour organoids (colorectal/oesophageal/ovarian/pancreatic/gastric). NOTE: 256 derived organoids vs spec seed "screens across 162 organoids" — screen count vs biobank size to reconcile from methods in Phase 1.
- S3 PMC13664187 = "Transferability of Transcriptome-Based Gene-Dependency Models from Two-Dimensional Cancer Models to Patient-Derived Organoids: Blinded External Validation" (via Europe PMC). Matches spec seed (closest transferability prior).
- S5 arXiv:2609.14858 Dream-RSI abstract + google-research/dream-rsi README/code inspected (trajectory system design, PLAN §0.4-0.5).

Access note: PMC direct HTML intermittently serves reCAPTCHA to curl; use Europe PMC REST API as the official alternative route. Never bypass challenges.

Pending Phase 1: full methods/supplements, environmental design extraction (250 genes x 18 screens x 7 models), data-route resolution via official manifests (DepMap 26Q3 vs study-specific), provenance table, crosswalk, novelty audit v1.
