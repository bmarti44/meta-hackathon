**C2: PARTIAL.** The retained data support substantial provenance claims, but sgen007 does not establish complete provenance or a reproducible cache installation. Four high-severity issues prevent acceptance.

1. **HIGH — MOESM3 “not retained” explanation is false.** [src/sgen007_provenance.py:101](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:101). The archive exists at `data/raw/sanger_figshare/S2_Supplementary_Tables.zip`: **127,226,341 bytes**, SHA-256 `7e83b7551c9c272de0bc0455ea9a0e7803a8043d15d9cfedf5a1c3e609a2a6e2`, matching both source manifest and Lock2. The resolver mistakes the annotated manifest filename for a filesystem path, then excuses its absence. Extracted tables cannot replace Table 6, which supplied the external analysis.
   **Fix:** Resolve the canonical archive path, register and install its opaque bytes, and supersede the incorrect explanation and battery note.

2. **HIGH — The declared closure omits required dependencies.** [src/sgen007_provenance.py:90](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:90). Lock2 is added as one file; its `files` map is never traversed. Only **9/30 Lock2-pinned files** appear in the register. Missing items include cohort/covariate/presence files, protocol, evaluator, kernels, environment locks and the archive. Frozen estimator bytes and cited licence/receipt/identity evidence are also absent.
   **Fix:** Expand manifests recursively, preserving stage-specific versions and evidence dependencies; require exact closure coverage.

3. **HIGH — Explained mismatches are unconditional exemptions.** [src/sgen007_provenance.py:105](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:105). Any hash change to the exposure log or estimator is accepted by pathname. A read-only, in-memory negative check substituted all-zero observed hashes for both files: **`screen_pass=true`, return code 0**. The screen also ignores missing manifest hashes and licence completeness.
   **Fix:** Verify the frozen exposure prefix and each required estimator version explicitly; make required provenance/licence fields acceptance conditions.

4. **HIGH — Battery success does not establish the specified installation checks.** [src/sgen007_battery.py:35](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_battery.py:35). Acceptance requires only 250 panel genes and at least 55 copied files. The 256 Sanger rows are reported without an assertion. Crosswalks, attrition, cohort membership, library rules and 148/144/142 reconciliation are never tested. Missing rows are skipped, and hashes establish agreement with the generated register rather than complete source closure.
   **Fix:** Require the exact dependency set, verify source expectations, and run metadata-only identity and attrition checks entirely against installed files.

5. **MEDIUM — Source and licence fields lose available evidence.** [src/sgen007_provenance.py:89](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:89). Import reads `download_url`, while these manifests use `source_url`; release, retrieval and licence fields are discarded. Classification labels the quarantined external RData as project-derived. “PMC open-access” also obscures differing terms: S1 is **CC BY-NC-ND 4.0**, while S2/S3 are **CC BY 4.0**. The CRISPR supplemental CSV is marked acquisition-unknown despite its retained pgen003 receipt.
   **Fix:** Import explicit source fields and evidence paths/hashes; classify by source identity rather than path substrings and install the cited evidence.

6. **MEDIUM — Reconciliation contains incorrect statements and broken references.** [src/sgen007_provenance.py:113](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen007_provenance.py:113). It says “2 screens excluded”; the documented exclusions are **two sequencing replicates**, with both affected screens retained. `status.json.verification.baseline_anchoring` is absent, the baseline JSON contains no replicate identities, and `ledger/exposure.jsonl` does not exist.
   **Fix:** Reference `data/provenance_v3_addendum.md:2`, retain both replicate IDs and the unresolved Chronos-input limitation, and correct the exposure-log/evidence links.

The independent checks support several exceptions and underlying records:

- All **63 retained register files** match their recorded SHA-256 and byte size; all **30 Lock2 files** match their locked hashes. The sgen007 SPEC hash matches its ledger lock. V1–v3 remain preserved as failed reports.
- The exposure log’s first **1,809 bytes** match the pinned hash. Its append-only explanation is legitimate for the current bytes.
- Both frozen estimator versions hash correctly. The retained sgen005 v5 report documents stage-specific materialization; sgen007 nevertheless fails to install those versions.
- All **19 retained Figshare files** match manifest SHA-256/size and official API MD5. The 32-character MD5 comparison branch is reasonable, but **no v4 row exercises it**; `figshare_md5` is not imported.
- Metadata independently reconcile **148 models / 144 archived groups / 142 Passports patients**, with no missing patient join.

Against C2’s actual wording:

| C2 field | Verdict | Field-level reason |
|---|---|---|
| Legitimately accessible public data | MET for inspected sources | Retained official manifests and receipts support the public routes; historical deviations remain disclosed. |
| Complete provenance | PARTIAL | Required dependencies, transformations and evidence links are omitted or misstated. |
| Licensing | PARTIAL | Figshare CC BY evidence and Sanger usage-policy bytes are retained, but source-specific terms and evidence are incompletely represented and installed. |
| Identifier crosswalks | PARTIAL | External-cohort reconciliation reproduces; its supporting closure is incomplete, and Broad donor identities remain explicitly unresolved. |
| Reproducible retrieval or documented cache installation | PARTIAL | Cache bytes exist, but the installer omits essential inputs and does not perform the specified metadata checks. |

Review remained read-only; no outcome archive was decoded. The filesystem-writing battery was assessed statically rather than rerun.

SGEN007_SCORE: 65; C2:PARTIAL