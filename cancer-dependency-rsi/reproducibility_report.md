# Reproducibility report (sgen002, componentwise)
- Atlas v4 isolated rebuild: PASS byte-identical (generations/sgen002/reproduction_report_v1.json).
- Primary point estimate: PASS exact (diff 2.8e-17) from retained per-gene coordinates.
- Figure 1: PASS byte-identical regeneration (SVG sha in report).
- OLS baseline anchor: PASS via test suite (max |diff| 1.73e-8 vs author coefficients).
- Eligibility recompute (251/250/810): regenerated in pgen003, independently reproduced by sol-high.
- Tests: full suite green at package time (see status.json).
- PENDING: donor/patient interval (no retained arrays; outcome re-access not performed);
  policy comparison (absent); fresh clean-room environment install (not run).
- Locked hashes: LOCK2_COMMIT 30/30 files verified by sol-high (incl. src/budget.py 3459abdd...).
Reproduce (project root cancer-dependency-rsi): `RUN=$(mktemp -d) && .venv/bin/python src/sgen005_upstream.py --report $RUN/up.json && .venv/bin/python src/sgen002_reproduce.py --report $RUN/sgen002.json && .venv/bin/python src/sgen008_checks.py --report $RUN/chk.json && .venv/bin/python -m pytest -q`
Figure reproduction report of record: generations/sgen002/reproduction_report_v3.json (figure hash in generations/sgen009/traceability_v17.json inventory).
Resume: cd cancer-dependency-rsi && .venv/bin/python src/cli.py resume

Reproduction report of record: generations/sgen002/reproduction_report_v3.json (sha256 620353bd787b3380c04cfbc1bd078bee66610e823aac506f22bd3a7019ab75c6); figure hash in generations/sgen009/traceability_v10.json inventory.
