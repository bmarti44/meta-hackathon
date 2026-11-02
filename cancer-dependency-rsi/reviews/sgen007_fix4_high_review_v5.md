**89/100, up from 88. C2 remains PARTIAL.** Several fixes are verified, but required closure and schema enforcement remain incomplete.

Read-only verification confirmed:

- All **95 registered files** match their sizes and SHA-256; all **30 LOCK2 files** are covered.
- Regenerating v9 reproduces the register, excluding runtime. An in-memory battery replay reproduces v6: **250 genes, 256 covariate rows, 148 models, 144 archived groups, 142 patients, 133 minLib / 15 v1_1**.
- The ten explicitly added governing-evidence paths are required; removing each fails. Rows marked nonexistent also fail.
- Duplicate-add merging now enforces the policy HTML expectation. Substituting its expected digest fails.
- Empty and whitespace-only sole patient matches fail.
- All five extracted tables record `reconstructed_extraction_from_retained_zip` and inherited MOESM3 terms; Table 2 has `identity_crosswalk`.

Remaining findings:

1. **HIGH — Independent required closure still omits governing evidence.**  
   [sgen007_battery.py:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:23)  
   Removing **both Figshare source manifests, atlas v3’s manifest, and the exposure log** still returns **pass with 91 files**. The battery reads source manifests from the project before installation, allowing an installation without its source/license evidence to pass. Derive required closure recursively, including controlling manifests and evidence dependencies.

2. **MEDIUM — Required provenance fields are not enforced by screen acceptance.**  
   [sgen007_provenance.py:150](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:150)  
   Independently omitting `acquisition_class`, `transformations`, `identity_role`, `exposure_status`, or `limitations` during row construction still passes. Blanking license evidence produces **60 flagged rows yet still passes**. The battery also accepts removal of all semantic provenance fields. Validate required fields, types, allowed values, and licensing dispositions before acceptance.

3. **MEDIUM — Missing receipt expectations remain acceptable.**  
   [sgen007_provenance.py:97](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:97)  
   Removing `sha256` from either the Passports manifest or supplemental receipt still passes screen generation. Reject missing required expectations; measuring current bytes does not establish agreement with retained acquisition evidence.

4. **LOW — MOESM3 note remains hard-coded.**  
   [sgen007_battery.py:91](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:91)  
   `moesm3_installed` is computed inside the installation context, but the note still uses `if False else 'verified in copy loop'`. Render the captured boolean directly.

| C2 field | Adjudication | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source and terms evidence supports access. |
| Full provenance | **PARTIAL** | Extracted-table semantics improved; governing closure and schema enforcement remain incomplete. |
| Licensing | **PARTIAL** | Inherited terms and policy digest verified; missing license evidence can still pass. |
| Identifier crosswalks | **MET for retained mappings** | Counts and locked assignments reproduce; blank sole patient matches fail. The 144-group/142-patient limitation remains disclosed. |
| Reproducible retrieval/cache | **PARTIAL** | Registered bytes reproduce; incomplete evidence installations and missing receipt expectations remain acceptable. |

No files were written or outcome archives decoded. Installation behavior was emulated in memory; no physical temporary installation was performed.

SGEN007_FIX4_SCORE: 89; C2:PARTIAL