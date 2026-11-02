**C2 remains PARTIAL. Score: 88/100, up from 84.** The fixes improve coverage and per-model checks, but several acceptance gaps remain.

Verified read-only, with execution and negative checks confined to memory:

- All **95 unique files** match registered sizes and SHA-256; all **30 LOCK2 files** are covered. Regenerating v8 reproduces the retained register, excluding runtime.
- Passports and supplemental CSV expectations match their retained manifest/receipt hashes; substituting either digest fails. **Policy HTML’s expectation remains unenforced.**
- Both governing evidence rows—`identity_erratum_v1.json` and `probe_results_v2.json`—are present. All five extracted spreadsheets explicitly inherit MOESM3’s CC BY 4.0 terms.
- Battery v4 independently derives **45 required paths** from the project’s LOCK2 map and source manifests. Nonexistent rows and removal of MOESM3 are rejected.
- The in-memory battery replay reproduces the saved report: **250 genes, 256 covariate rows, 148 models, 144 archived groups, 142 patients, 133 minLib / 15 v1_1**. Independent crosswalk checks confirm current library and donor assignments. Swapping either assignment fails.

Remaining issues:

1. **HIGH — Required closure still excludes governing evidence.**  
   [src/sgen007_battery.py:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:23)  
   Removing nine evidence rows—including the policy, probe results, supplemental receipt, identity reconciliation/erratum, Passports manifest and three atlas manifests—still returns **pass with 86 files**. The independent set protects core data and code, but does not protect the complete provenance closure.  
   **Fix:** independently require controlling manifests, receipts, governing amendments and their dependencies.

2. **MEDIUM — Policy expectation is discarded; missing receipt expectations remain acceptable.**  
   [src/sgen007_provenance.py:46](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:46), [line 90](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:90)  
   Policy HTML is first added without an expectation. Its later receipt-backed `add()` returns before updating the row; single expectations are also skipped by stage verification. Consequently, v8 retains null `manifest_sha256`/`hash_verified` and a blank URL, and digest substitution still passes. In-memory removal of the Passports or supplemental expected hash also passes.  
   **Fix:** merge duplicate-path evidence, validate every required expectation, and reject absent receipt hashes.

3. **MEDIUM — Provenance fields remain generic and insufficiently validated.**  
   [src/sgen007_provenance.py:54](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:54)  
   All rows now contain `limitations`, but **90/95** use the same fallback. Extracted spreadsheets are classified `retained_receipt` despite their explicitly reconstructed extraction history; Table 2 is labelled `not_identity_bearing` despite containing model/donor crosswalk columns. Removing provenance fields from register rows does not fail the battery.  
   **Fix:** record row-specific evidence links, transformations, identity/exposure roles and limitations; enforce the required schema.

4. **MEDIUM — Exactly-one patient check accepts an empty identifier.**  
   [src/sgen007_battery.py:63](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:63)  
   `{''}` satisfies `len(_hits) == 1`. Replacing one patient identifier with blank, with the measured register hash updated, still passes at **142 patients**. Current installed mappings are nonempty.  
   **Fix:** reject empty or whitespace-only patient identifiers before counting or accepting mappings.

5. **LOW — MOESM3 note is still hard-coded.**  
   [src/sgen007_battery.py:86](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:86)  
   `if False else 'verified in copy loop'` never inspects installed contents. Current installation checks establish presence, but the requested note derivation is unfinished.  
   **Fix:** capture installed presence and hash-verification results inside the temporary-directory context and render those values.

| C2 field | Verdict | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source evidence supports access. |
| Full provenance | **PARTIAL** | Governing evidence is present but removable; row semantics remain generic. |
| Licensing | **PARTIAL** | MOESM3 inheritance corrected; required source/terms evidence is not fully enforced. |
| Identifier crosswalks | **PARTIAL** | Current mappings reproduce; empty patient identifiers remain acceptable. |
| Reproducible retrieval/cache | **PARTIAL** | Baseline bytes reproduce; incomplete evidence installations still pass. |

No files were written or outcome archives decoded.

SGEN007_FIX3_SCORE: 88; C2:PARTIAL