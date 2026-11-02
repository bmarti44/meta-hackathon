**89/100. C2 remains PARTIAL.** Three targeted fixes verify, but the claimed schema validation is absent and required closure remains incomplete.

1. **HIGH — The four additions do not complete required closure.**  
   [sgen007_battery.py:25](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:25)  
   Removing either Figshare manifest, atlas v3’s manifest, or the exposure log now fails as intended. However, removing **LOCK2_COMMIT.json, the frozen estimator artifact, the supplemental CSV, and src/build_atlas_v3.py together still passes with 91 files**. These retain governing expectations, historical verification, or declared dependencies. Independently require the controlling documents and recursively traverse their dependencies.

2. **MEDIUM — Required-field presence and nonempty validation remains unenforced.**  
   [sgen007_provenance.py:142](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:142), [acceptance expression:152](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:152)  
   In-memory omission, empty-string, and whitespace tests for each of `acquisition_class`, `transformations`, `identity_role`, `exposure_status`, and `limitations` still return `screen_pass=true`. Empty license evidence flags **60 rows but still passes**; whitespace licenses also pass. A missing license key raises `KeyError`. Add an explicit required-field validator and make schema/license failures block acceptance.

Other verification succeeded:

- All **95 unique registered files** match recorded sizes and SHA-256; all **30 LOCK2 files** are covered. Regeneration reproduces register v10, excluding runtime.
- Both receipt expectations are asserted present. Missing, empty, or null SHA-256 values are rejected; substituted digests fail screening.
- The in-memory battery replay reproduces v7: **250 genes, 256 covariate rows, 148 models, 144 archived groups, 142 patients, 133 minLib / 15 v1_1**.
- The note renders the captured `moesm3_installed=True`. The corrected artifact is [battery v7](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen007/cache_install_battery_v7.json:18); v6 preserves the old wording. The prompt’s version reference is cosmetic because v7 matches current execution.

| C2 field | Adjudication | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source evidence supports access. |
| Full provenance | **PARTIAL** | Required semantics and dependency closure remain insufficiently enforced. |
| Licensing | **PARTIAL** | Terms are retained, but empty licensing evidence can pass. |
| Identifier crosswalks | **MET for retained mappings** | Installed mappings and locked assignments reproduce; the 144-group/142-patient limitation remains disclosed. |
| Reproducible retrieval/cache | **PARTIAL** | Current bytes reproduce, but incomplete installations remain acceptable. |

No files were written or outcome archives decoded. Installation was emulated in memory; no physical temporary installation was performed.

SGEN007_FIX5_SCORE: 89; C2:PARTIAL