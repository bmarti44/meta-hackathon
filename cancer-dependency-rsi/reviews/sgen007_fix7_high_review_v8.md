**94/100. C2 remains PARTIAL.** The data-manifest closure and schema-diagnostic fixes verify. One workbook-completeness gap remains.

**MEDIUM — Workbooks absent before regeneration disappear from the required closure.** Both [battery:40](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:40) and [provenance:89](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:89) enumerate currently existing `*.xlsx` files.

In read-only absence simulations:

- Each missing workbook produces a regenerated register with **94 rows**, `screen_pass=true`, and battery **`pass=true`**.
- All five missing workbooks produce **90 rows**, with both checks still passing and `exact_installation=true`.

Pin the five expected workbook paths independently of filesystem discovery, then require their presence in both scripts.

The other fixes pass independent verification:

- Removing any of the **95 register rows** rejects installation. The previous seven omissions, three papers and five workbooks also reject individually and in groups.
- Simulated cache absence of the condition registry, observation provenance, baseline/audit/precision evidence, approved split or paper XMLs produces structured screening failures.
- All **3,420 omission/empty/whitespace/null mutations** across nine required fields and 95 completed rows produce structured schema failures without exceptions.
- All **95 files** match recorded sizes and SHA-256; all **30 LOCK2 hashes** match.
- Regeneration reproduces **register v12**, excluding runtime. Memory-only installation reproduces **battery v9 exactly**: 250 genes, 256 covariate rows, 148 models, 144 archived groups, 142 patients, and 133 minLib / 15 v1_1 assignments.

| C2 field | Adjudication | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source manifests and receipts support access. |
| Full provenance | **PARTIAL** | Required workbook evidence can disappear undetected during regeneration. |
| Licensing | **MET for retained sources** | Source-specific terms and policy evidence remain retained; blank license fields fail. |
| Identifier crosswalks | **MET for retained mappings** | Patient joins and locked assignments reproduce; disclosed donor limitations remain. |
| Reproducible retrieval/cache | **PARTIAL** | Current installation reproduces, but an incomplete workbook cache still passes. |

Review remained read-only. Outputs and installations were intercepted in memory; no outcome archive was decoded.

SGEN007_FIX7_SCORE: 94; C2:PARTIAL