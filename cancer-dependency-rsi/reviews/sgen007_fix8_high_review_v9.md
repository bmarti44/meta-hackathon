**98/100. The previous MEDIUM is resolved. C2 is MET for the retained sgen007 package.**

Both [provenance:89](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:89) and [battery:40](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:40) pin the five exact workbook paths for tables **1, 2, 4, 9 and 10**, independently of filesystem discovery. Version references correctly target **register v13** and **battery v10**.

Read-only simulations verified each workbook absent individually, then all five absent:

- Provenance retains **95 rows**, including each missing path with `exists=false`; reports it in `missing`; returns `screen_pass=false` and exit code **1**.
- Battery rejects the regenerated failed register.
- Removing missing-workbook rows from an otherwise passing register independently triggers the **REQUIRED closure assertion**, identifying exactly the omitted paths.
- Baseline provenance reproduces v13 exactly, excluding runtime; battery’s REQUIRED check accepts the complete register.

Carrying forward the previously verified fields:

| C2 field | Verdict | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source manifests and receipts. |
| Full provenance | **MET for retained package** | Required closure now enforces all five workbooks; reconstructed-history and replicate limitations remain disclosed. |
| Licensing | **MET for retained sources** | Source-specific terms, inherited workbook terms and retained policy evidence. |
| Identifier crosswalks | **MET for retained mappings** | Previously verified patient joins and locked assignments; grouping limitations disclosed. |
| Reproducible retrieval/cache | **MET for retained cache** | Previously verified installation, with workbook omissions now independently rejected. |

No unresolved findings in the requested scope. No files were written, physical installation performed or outcome archives decoded.

SGEN007_FIX8_SCORE: 98; C2:MET