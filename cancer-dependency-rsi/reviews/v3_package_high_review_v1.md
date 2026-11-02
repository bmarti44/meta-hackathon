The package needs further fixes before a ≥90 integrity score. I found two high-severity issues and no critical issues. The scientific result remains a candidate bound; this review grants no scientific gate.

Paths below are relative to `cancer-dependency-rsi/`, except root `PLAN.md` and `GOAL.md`.

1. **HIGH — C7 annotations still omit known findings and contain false “not located” dispositions.**  
   Evidence: `src/build_atlas_v3.py:50–56`; `atlas/v3/genes.csv:35,93,231,250`; `atlas/v3/manifest.json:24–25`. CDK6 receives an S3 transfer annotation but omits S1’s CDKN2A-copy-loss/glial-state biomarker evidence, explicitly reported in cached `data/papers/PMC13581591.xml:4`, Fig. 3 and Extended Data Fig. 6. FZD5/TCF7L2/WLS receive state-association tags while their biomarker dispositions say no gene-specific report was located. Moreover, 234 genes say “author_library_class_only_no_gene_specific_S1_report_located” despite having joined author-test results. The inherited `prior_knowledge_status` also remains generic throughout.  
   **Exact fix:** annotate S1’s CDK6 findings with their distinct significance qualifications; classify the WNT state associations consistently across prior and biomarker fields; distinguish “tested, not FDR-significant” from “not assessed/not located”; reconcile obsolete status fields and manifest descriptions. Add regression assertions for these known cases.

2. **HIGH — pgen001’s required pre-run ledger lock is not witnessed.**  
   Evidence: root `PLAN.md:72` requires the SPEC hash locked **in the ledger before any run**; `generations/pgen001/SPEC.md:9` asserts prospective freezing. The only pgen001 ledger entry is the completed screen at `ledger/experiments.jsonl:31`. `GENERATIONS.md:4` nevertheless claims the hash was locked before probing. The current SPEC hash matches, but that establishes current content, not prospective locking. A generation-specific reserved battery budget is also absent.  
   **Exact fix:** retain contemporaneous evidence establishing the original SPEC/hash and probe chronology, and append an honest reconciliation. If that evidence cannot establish prospective locking, label pgen001 exploratory/protocol-deviating and run any subsequent screen under a new version with its hash and battery reservation ledgered beforehand. Do not backdate a lock.

3. **MEDIUM — `SCREEN-POSITIVE_CONDITIONAL` does not meet the frozen screen bar.**  
   Evidence: `generations/pgen001/SPEC.md:19–25`; `screen_results_v1.json:3–6`; `token_accounting_audit.json:11`. The SPEC requires a conservative **predeclared** failure charge. The results explicitly defer that rule to a future Lock-1 draft. Criterion 2 also requires licenses and remaining-allowance verification, neither demonstrated by the supplied screen artifacts.  
   **Exact fix:** preserve v1 and issue a versioned disposition of `PENDING` or `FAILS-SCREEN`, listing the unmet conditions. A revised screen must prospectively specify a demonstrably conservative failure-charge rule and document every required route condition before declaring passage.

4. **MEDIUM — Metadata acquisition and non-exposure claims lack an auditable request trail.**  
   Evidence: `screen_results_v1.json:5–7`; `ledger/experiments.jsonl:31`; `raw_counts_zip_listing.json:1`. The listing retains filenames and sizes, but no request ranges, response headers, source receipt, request/byte/time totals, or reproducible extraction procedure. The Passports probe remains described as an unmanifested `/tmp` artifact. Consequently, the HEAD checksum, metadata counts, budget compliance and metadata-only acquisition cannot all be independently verified from this package.  
   **Exact fix:** retain or recover contemporaneous request receipts, exact ranges, response headers, acquisition code, hashes, license evidence, metadata snapshot and cumulative budget accounting. Record unsupported historical assertions as unverified where recovery is impossible.

5. **MEDIUM — The novelty repair is substantively correct, but the mandated search completion remains unwitnessed.**  
   Evidence: root `PLAN.md:174`; `reviews/novelty_audit_v4.md:17–29`; previous review `reviews/sci_package_high_review_v1.md:7`. V4 documents S1/S3 identifier searches, but no corresponding S2 check, systematic backward/forward citation checks, or completion of the requested broader full-text/preprint and closest supplement/code checks. “Retained in session record” provides no resolvable package reference.  
   **Exact fix:** retain dated queries, source identifiers, returned records and screening dispositions; complete the missing checks or explicitly mark them outstanding. Keep C1/C6 partial until that evidence is adjudicated.

6. **MEDIUM — pgen001 improperly narrows family reopening after a failed screen.**  
   Evidence: `generations/pgen001/SPEC.md:24–25`, versus root `PLAN.md:81`, `reviews/cl_rd_raw_accounting_discriminator_v2.json:5–9`, and `cancer_rsi_handoff.txt:319`. Its failure rule permits reopening only through user-supplied measured expenditure, excluding justified alternatives and implying family closure without a necessary-condition argument.  
   **Exact fix:** preserve the frozen SPEC and append a correction limiting failure to the tested specification. Keep other alternatives open under discriminator v2 and handoff §11; require a new prospective SPEC for another test.

7. **LOW — The corrected S3 account cites the wrong results section.**  
   Evidence: `reviews/novelty_audit_v4.md:13,21`. Cached `data/papers/PMC13664187.xml:1` places within-organoid ranking in §2.10.1 and §3.7, Tables S17–S19. §3.5/Fig. 6 concerns cross-cohort target-wise synthesis.  
   **Exact fix:** replace those section references with §2.10.1/§3.7 and Tables S17–S19.

8. **LOW — The advertised live checkpoint remains stale.**  
   Evidence: root `PLAN.md:3` and `GOAL.md:79` direct readers to live status, but `status.json:36,103` still records C10 as partial and proposes atlas v2; `STATUS.md:119` still says C was not consumed.  
   **Exact fix:** update `status.json` and append a current `STATUS.md` checkpoint reflecting the executed external test, current artifacts and latest adjudications, while retaining historical entries.

Independent checks that passed:

- The goal objective matches the archived v1 objective verbatim. The v3 notes preserve the joint objective and `COMPLETE_*` requirements.
- S3’s substantive misrepresentation is repaired. Residual novelty is honestly limited to the joined measured-lability/displacement relationship. P3’s drug-response exclusion and P5’s adjacent-context disposition are supported by their abstracts ([P3](https://doi.org/10.1093/bib/bbag559), [P5](https://www.sciencedirect.com/science/article/pii/S193459092500298X)).
- All 250 atlas coefficient/FDR joins match the author files. Format FDR<0.05: **CTNNA1, ITGA3, ITGAV, ITGB1, NCKAP1, PRKCA, PTK2**. Serum: **CTNNA1, PPP1R15B, PPP2R2D, PTK2, RICTOR, SPTLC1, SPTLC2, SQLE**. Declared input/code hashes match; inherited values are unchanged; 43 exclusions remain.
- Receipt totals reproduce exactly: 15 completed calls, four without usage; input **8,750,313**, cached input **7,932,416**, output **108,308**, reasoning output **48,689**. These overlapping categories must not simply be added together.
- ZIP metadata contains **1,122** count files, three directory entries and **358** filename prefixes. ZIP-expanded member sizes sum to **2,847,239,686 bytes**; these members remain gzip-compressed.
- The measured-token proposal is explicitly unadjudicated. Discriminator v2 permits feasibility reassessment without granting C9.
- The updated CLI assertion remains a real refusal smoke test: it requires nonzero exit plus a named barrier. I did not execute it because its production launcher can write resource records. The atlas test and lineage validation test passed through direct invocation.

No files were modified or dependency data downloaded. I accessed only permitted reported outcomes. For pgen001, I found no retained evidence of count-value access; the missing acquisition receipts prevent a definitive independent non-exposure certification.

V3_PACKAGE_REVIEW_SCORE: 84; C1:PARTIAL; C6:PARTIAL; C7:PARTIAL; PGEN001:PENDING_NOT_SCREEN_PASSED