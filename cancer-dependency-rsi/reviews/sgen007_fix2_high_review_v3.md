**C2 remains PARTIAL. Score: 84/100, up from 78.** The estimator fix works, but closure and provenance acceptance remain incomplete.

Verified read-only, with execution and negative checks confined to memory:

- All **93 unique files** match registered sizes and SHA-256; all **30 Lock2 files** are covered.
- Current estimator bytes match the latest expectation; historical bytes match the frozen artifact. Corrupting either fails. Corrupting the exposure prefix also fails.
- The frozen estimator, controlling manifests, policy HTML, supplemental receipt and identity JSON are registered. The **Passports manifest hash is imported and verified**.
- Battery v3 reproduces **250 genes, 256 covariate rows, 148 models, 144 archived groups and 142 patients**. Independent joins find **zero unmatched models**, and independently applying the library rule reproduces **133 minLib / 15 v1_1**, including 13 dual-library models.
- Duplicate rows and removal of the MOESM3 row are rejected. The generated note reproduces.

Remaining issues:

1. **HIGH — Required installation coverage remains incomplete.**  
   [src/sgen007_battery.py:22](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:22), [line 30](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:30).  
   `REQUIRED` independently names only six paths. Setting MOESM3’s `exists=false` still returns **pass, exact_installation=true, 92 files**. Removing eight evidence rows—including policy, receipt, identity reconciliation and atlas manifests—still passes with **85 files**. The note incorrectly reports MOESM3 present because it checks register membership.  
   **Fix:** derive complete required coverage independently, require every required row to exist, validate installed manifests and expectations, and generate the note from installed paths.

2. **MEDIUM — Available receipt hashes are not enforced.**  
   [src/sgen007_provenance.py:87](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:87), [line 94](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:94).  
   Policy HTML and the supplemental CSV match their retained receipts, but both register expectations remain null and source URLs blank. Substituting either computed digest still passes. Removing the Passports expected hash also passes.  
   **Fix:** import retained receipt URLs/hashes and reject missing required expectations; distinguish a newly measured digest from verification against retained evidence.

3. **MEDIUM — Patient and library checks validate totals rather than complete correctness.**  
   [src/sgen007_battery.py:51](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:51), [line 52](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:52).  
   Unmatched or ambiguous models are silently omitted from the patient set. With an in-memory cohort substitution and updated register hash, one unmatched longitudinal model still passes at 142 patients; swapping two library choices also passes because 133/15 totals remain unchanged.  
   **Fix:** require one nonempty, unambiguous patient mapping for every cohort model; recompute each library choice from installed crosswalk availability and compare assignments model by model.

4. **MEDIUM — Evidence closure omits controlling corrections and receipts.**  
   [src/sgen007_provenance.py:82](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:82).  
   The register includes historical identity reconciliation but omits its governing `identity_erratum_v1.json`. Consequently, installation retains the withdrawn “may slightly understate” claim without its correction. The policy acquisition receipt in `probe_results_v2.json` is also omitted.  
   **Fix:** register governing amendments and cited acquisition evidence recursively, retaining explicit supersession links.

5. **MEDIUM — Provenance fields exist but remain generic and unenforced.**  
   [src/sgen007_provenance.py:54](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:54), [line 59](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:59), [line 138](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:138).  
   Extracted third-party spreadsheets receive “project-derived” license evidence; acquisition class follows URL presence, including an extraction-description string. All 93 rows lack `limitations`. Removing external source/license metadata still passes through the fallback.  
   **Fix:** inherit source terms, link actual receipts and transformations, record row-specific identity/exposure roles and limitations, and enforce required provenance fields explicitly.

| C2 field | Verdict | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source evidence supports access. |
| Full provenance | **PARTIAL** | Generic fields, unenforced expectations and missing governing evidence. |
| Licensing | **PARTIAL** | Retained paper terms verified; extracted-source inheritance and completeness checks remain deficient. |
| Identifier crosswalks | **PARTIAL** | Current joins independently reproduce; battery lacks complete mapping and selection assertions. |
| Reproducible retrieval/cache | **PARTIAL** | Baseline bytes reproduce; incomplete installations can still pass. |

No files were written or outcome archives decoded.

SGEN007_FIX2_SCORE: 84; C2:PARTIAL