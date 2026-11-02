**C2 remains PARTIAL.** The fixes improve the retained evidence, but three high-severity acceptance defects remain.

Verified read-only:

- **MOESM3:** canonical archive registered; **127,226,341 bytes**, SHA-256 `7e83b7551c9c272de0bc0455ea9a0e7803a8043d15d9cfedf5a1c3e609a2a6e2`. The in-memory battery copied and hashed its opaque bytes.
- **Register:** all **83 files** match recorded sizes and SHA-256. All **30 Lock2 files** are present and match their locked hashes; complete recursive closure remains incomplete.
- **Exemptions:** the **1,809-byte exposure prefix** matches `09f7b9e3a66ad7876ddc16e7ca86590e59815bec3f4b2b528b3b2979c55b939e`. Frozen estimator contents match their content-addressed hash. Corrupting either correctly fails; substituting the current estimator hash still passes.
- **Battery counts:** reproduced **250 panel genes, 148 models, 144 archived groups**, and 256 covariate rows using an in-memory installation. Independent metadata joins also reproduce **142 patients**, zero missing patient joins, and **133 minLib / 15 v1_1** selections.
- **Source corrections:** manifest `source_url`, license and release fields are imported. Retained XML confirms **S1 CC BY-NC-ND 4.0**, **S2/S3 CC BY 4.0**. Quarantined RData now retains its Figshare source/license and opaque flag.
- **Reconciliations:** both excluded replicate IDs match sequence metadata: `0178_Adh_Alt_SF_Dome_RepA` and `0178_Adh_Nat_Serum_Dome_RepB`. Both screens remain retained; the Chronos-input limitation and corrected exposure path are stated.

Remaining issues:

1. **HIGH — Current estimator substitutions still pass.** [src/sgen007_provenance.py:41](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:41), [src/sgen007_provenance.py:86](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:86).  
   Deduplication keeps the provisional-v1 estimator expectation and discards the later-stage/Lock2 expectation. The current hash is recorded without comparison; a valid frozen v1 artifact exempts the pathname. Substituting an all-zero current estimator hash produced **`screen_pass=true`, return 0**. Moreover, `all(checks.values())` treats the nested estimator dictionary as truthy without validating its members.  
   **Fix:** preserve stage-specific expectations, compare current bytes against the v2/Lock2 hash, validate frozen contents separately, and require explicit Boolean checks.

2. **HIGH — Closure still omits required frozen bytes and evidence.** [src/sgen007_provenance.py:55](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:55), [src/sgen007_provenance.py:73](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:73).  
   Lock2’s 30-file map is covered, but the register omits the frozen estimator artifact, `data/data_manifest.json`, `LOCK2_COMMIT.json`, provisional/v2/v4 atlas manifests, retained Sanger usage-policy bytes, the supplemental receipt, and sgen001 identity reconciliation. Thus installation cannot carry the evidence or both estimator versions that justify acceptance.  
   **Fix:** recursively register and install versioned inputs, controlling manifests, and cited evidence dependencies; verify coverage against an independently derived required set.

3. **HIGH — “Exact installation” remains self-referential.** [src/sgen007_battery.py:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:23), [src/sgen007_battery.py:36](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:36).  
   Removing the MOESM3 row, or marking it nonexistent, still gives **82 files, `exact_installation=true`, pass**. Duplicating a row reports **84 installed files** despite only **83 unique paths**, also passing. The added counts are real improvements, but crosswalk correctness, attrition, library selection and the 142-patient reconciliation remain untested by the battery.  
   **Fix:** reject missing/duplicate rows, compare unique installed paths against independent closure expectations, and assert metadata joins and selection rules from installed files.

4. **MEDIUM — Missing provenance/license evidence is still accepted.** [src/sgen007_provenance.py:49](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:49), [src/sgen007_provenance.py:99](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:99).  
   The fallback labels any input “project-derived,” including extracted third-party tables. Available Passports and supplemental receipt hashes/URLs are not imported; their register expectations remain null. Removing imported external license metadata or a required expected hash still passes. License completeness is absent from the acceptance expression. Acquisition class, transformations, identity role and exposure status required by SPEC are also absent from rows.  
   **Fix:** import retained evidence, inherit applicable source terms for extracted tables, represent unknowns explicitly, and enforce required provenance fields.

5. **LOW — Battery source still emits the superseded archive explanation.** [src/sgen007_battery.py:45](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:45).  
   It says MOESM3 is absent, while retained battery v2 correctly says it is included.  
   **Fix:** generate the note from verified installation contents and preserve a reproducible versioned report.

| C2 field | Verdict | Basis |
|---|---|---|
| Legitimately accessible public data | **MET for inspected sources** | Retained official-source evidence supports public access. |
| Full provenance | **PARTIAL** | Missing evidence closure, stage expectations and required row fields. |
| Licensing | **PARTIAL** | Paper terms corrected; policy evidence and acceptance enforcement incomplete. |
| Identifier crosswalks | **PARTIAL** | External metadata reconciliation reproduces; installation checks and supporting evidence remain incomplete, with disclosed identity limitations. |
| Reproducible retrieval/cache | **PARTIAL** | Opaque copying and counts reproduce, but closure and exact-set acceptance remain insufficient. |

No files were written. Installation and negative checks used in-memory substitutions; outcome archives were never decoded.

SGEN007_FIX_SCORE: 78; C2:PARTIAL