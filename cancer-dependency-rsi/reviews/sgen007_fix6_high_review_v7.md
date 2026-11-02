**91/100. C2 remains PARTIAL.** The requested mutation probes pass, but the battery still accepts an incomplete dependency closure.

1. **HIGH — Required closure still omits manifest-declared dependencies.**  
   [sgen007_battery.py:38](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:38) traverses the four atlas manifests but never traverses `data/data_manifest.json.files`.

   Removing its seven otherwise-unrequired entries—including `condition_cell_registry.csv`, `observation_provenance_minipool.csv`, baseline evidence and the approved G1 split—still returns **`pass=true` with 88 files**. Removing those seven, three paper XMLs and five extracted metadata workbooks together still passes with **80 files**.

   Require the data-manifest dependencies and supporting evidence independently of register membership. The four targeted additions fix their specific omissions; they do not establish complete closure.

2. **LOW — Some missing keys bypass structured schema reporting through exceptions.**  
   [sgen007_provenance.py:139](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:139) indexes fields before the validator runs. Omitting `exists` or `license_evidence` raises `KeyError`; omitting `path` does likewise on the two mismatch rows. These failures are closed, so this is a diagnostic defect rather than an acceptance bypass. Validate before indexing.

Verified independently:

- Removing **LOCK2_COMMIT, the frozen estimator, supplemental CSV or build_atlas_v3** fails, individually and together.
- All **1,710 empty/whitespace mutations** across nine required fields and 95 rows return **`screen_pass=false`**. Null values also fail. Schema failures and `no_license` now block acceptance.
- All **95 unique files** match recorded sizes and SHA-256; all **30 LOCK2 expectations** match.
- Regeneration reproduces **register v11**, excluding runtime. The in-memory installation replay reproduces **battery v8 exactly**: 250 genes, 256 covariate rows, 148 models, 144 archived groups, 142 patients, and 133 minLib / 15 v1_1 assignments.

| C2 field | Adjudication | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source manifests and receipts support access. |
| Full provenance | **PARTIAL** | Manifest-listed provenance and analysis evidence can still be omitted from an accepted installation. |
| Licensing | **MET for retained sources** | Source-specific terms and policy evidence are retained; blank licensing fields now block screening. |
| Identifier crosswalks | **MET for retained mappings** | Patient joins and locked assignments reproduce; grouping limitations remain disclosed. |
| Reproducible retrieval/cache | **PARTIAL** | Current bytes reproduce, but incomplete installations still pass. |

Review remained read-only. Installation was emulated in memory; no physical temporary installation occurred and no outcome archive was decoded.

SGEN007_FIX6_SCORE: 91; C2:PARTIAL