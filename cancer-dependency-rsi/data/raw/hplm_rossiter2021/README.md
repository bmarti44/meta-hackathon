# HPLM (Rossiter et al., Cell Metab 2021) screen data — downloaded 2026-10-30, analyzed in src/hplm_reverse_test.py

PMC file downloads are reCAPTCHA-walled from scripts. In a browser:
1. Open https://pmc.ncbi.nlm.nih.gov/articles/PMC8172426/
2. Supplementary Materials section: download NIHMS1674248-supplement-2.xlsx .. -7.xlsx
   (Table S1 = genome-wide screen datasets, RPMI+dS vs HPLM+dS; supplement-4.xlsx ~ Table S3 secondary screens).
3. Save them into this directory (data/raw/hplm_rossiter2021/).
GEO GSE164693 contains only RNA-seq counts (already inventoried, not needed).
Planned test: mevalonate/sterol gene scores should NOT gain essentiality in HPLM vs RPMI (plasma-like lipids/nutrients), opposite sign to organoid medium vs FBS.
