**86/100. One unresolved high-severity issue: the manuscript presents the archived bound more strongly than the unresolved patient grouping permits.** This review informs the sol-xhigh terminal determination; it does not replace it.

No project files were modified, downloads made, or external dependency outcomes decoded.

Independent verification established:

- The sgen002 SPEC hash matches its [ledger lock](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/experiments.jsonl:44), preceding the recorded reproduction result.
- All 30 Lock2 file hashes match.
- In-memory reconstruction reproduced **all 12 atlas CSVs across v1–v4**, using the archived v1 estimator; v2–v4 manifests also match byte-for-byte.
- V4’s declared inputs now include `atlas/v3/manifest.json`. All 207 external-coordinate entries carry the corrected **144 covariate-ID groups / 142 patients** wording.
- The primary point reproduces as **−0.14583205005879532**. Figure 1 regenerates byte-identically, with 207 points and five interval rows.
- Eligibility reproduces as **251 lines / 250 patients / 810 files**, zero full-C overlap, KP3 excluded. Displayed C10 numbers match retained results.
- **14 relevant tests passed.** I did not rerun the full suite requiring writable fixtures.

The interval, policy-comparison, and fresh-environment pending/absent labels in the reproduction report are honest.

1. **HIGH — Headline scientific claims exceed validated inference.**  
   [manuscript_draft_v1.md:7](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/manuscript_draft_v1.md:7) presents a “donor-cluster” interval and substantive BOUND conclusion; line 3 describes scientific completion as pending novelty alone. However, line 28 and the limitations statement acknowledge that patient weighting can change the **point, interval, and decision**, with unknown size and direction. The [C10 table](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reviews/c10_robustness_table_v1.md:7) likewise presents the archived bound without that qualification.

   **Exact fix:** replace the completion status and abstract conclusion with: “The archived 144-covariate-ID-group analysis yielded ρ=−0.146, interval [−0.175,−0.114], and BOUND under the locked grouping. Patient-weighted estimates, uncertainty, and decision remain unverified after reconciliation to 142 patients.” Qualify robustness as applying to archived analyses; mark C6/C10 PARTIAL. Replace the categorical title with “Measured format lability and organoid rank displacement in a selected panel.” Preserve frozen execution.

2. **MEDIUM — The reproduction runner implements less than the locked SPEC.**  
   [SPEC.md:4](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen002/SPEC.md:4) promises v1→v2→v3→v4 rebuilding and additional estimate/count checks. [sgen002_reproduce.py:30](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen002_reproduce.py:30) instead copies retained v3 outputs and runs only the v4 builder. Its aggregate excludes OLS, C10-table, and eligibility checks.

   **Exact fix:** add upstream rebuilding with the archived v1 estimator fallback, explicit C10/eligibility checks, and individual component statuses included in the aggregate. Until implemented, append a ledgered scope deviation describing this runner as **v3→v4 reproduction**. My independent upstream success does not repair the delivered command.

3. **MEDIUM — The stated numerical tolerance is not satisfied by the OLS anchor.**  
   [SPEC.md:2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen002/SPEC.md:2) freezes `atol=1e-10, rtol=1e-8`; the [legacy OLS test](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_baseline_ols.py:9) uses absolute tolerance `1e-6`. Independently, **417/3,000** coefficient comparisons exceed the SPEC tolerance: 161 plastic, 133 serum-free, 123 interaction. The reported maximum discrepancy, **1.73158e−8**, remains correct.

   **Exact fix:** report failure against the original global tolerance. Document the existing published-CSV rounding tolerance as an explicit, ledgered component-specific exception for subsequent reports. Do not retroactively call the original tolerance satisfied. This does not negate the established C5 baseline adequacy.

4. **MEDIUM — Novelty wording exceeds member-level evidence; acquisition controls remain unverified.**  
   [novelty_audit_v7.md:6](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reviews/novelty_audit_v7.md:6) categorically assigns Python-file purposes and says the package contains no measured-lability analysis, while acknowledging that contents were not inspected.

   The [receipts](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen002/s3_zenodo_listing.json:2) are internally consistent: two 206 responses, matching ranges/lengths, 460 unique members, 23 Python files, and no stated keyword matches. Minimum central-directory size calculated from names is exactly **80,167 bytes**, consistent with the requested directory range. However, the package retains neither the acquisition implementation nor response bodies to independently verify fail-closed enforcement and directory parsing.

   **Exact fix:** say “No member names indicate measured-environmental-lability analysis; content-level inspection remains pending.” Describe receipts as internally consistent. Retain the bounded fetcher, response bodies, and EOCD/directory offsets, or mark implementation-level fail-closed verification outstanding. There is no verified new payload-overfetch finding here.

5. **MEDIUM — The rejected identity caveat still survives in its producer and dossier.**  
   “May slightly understate” remains in the [dossier:12](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen001/adjudication_dossier_v1.md:12), [identity JSON:66](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen001/identity_reconciliation_v1.json:66), and [generator:61](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen001_identity.py:61).

   **Exact fix:** append an explicit supersession covering both historical artifacts; update the generator to state “effects on patient-weighted point, interval, and decision are unknown in size and direction; archived uncertainty is not validated patient-cluster uncertainty.” Preserve historical bytes.

6. **LOW — The visible figure qualification is clipped.**  
   [figure1_primary.svg:15](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/manuscript/figures/figure1_primary.svg:15) places the entire 231-character caption on one line. Helvetica 10-point measurement gives approximately **1,012 pixels**, starting at x=70 in a 980-pixel SVG: about **102 pixels overflow**, truncating the interval qualification.

   **Exact fix:** wrap the caption into two `<tspan>` lines and increase canvas height; change its [generator:52](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/make_figure1.py:52), regenerate, and record the new figure hash.

7. **MEDIUM — Reproduction overwrites retained evidence.**  
   [sgen002_reproduce.py:62](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen002_reproduce.py:62) regenerates the retained figure in place before checking equality; line 70 overwrites `reproduction_report_v1.json`. A failed rerun can replace the artifact being checked and erase the earlier report.

   **Exact fix:** generate the figure in the isolated workspace, compare against retained bytes, and require a fresh report destination with no-overwrite creation. Preserve prior reports and record each new report’s hash.

8. **LOW — Resume documentation still describes pre-sgen002 work.**  
   [status.json:104](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/status.json:104) still requests the 87-fix re-review followed by sgen002. [README.md:5](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/README.md:5) says no final external evaluation has run and describes continuing quarantine.

   **Exact fix:** update current phase, generation references, gate evidence, and next action to the completed archived external execution, sgen002 results, and outstanding review fixes. Preserve dated historical entries.

The previous live pgen002 PASS-label residue is repaired, including its index correction and accepted ENDPOINT:NO. Han’s complete abstract is now retained. Atlas donor wording is repaired; the remaining identity propagation defect is item 5.

| Gate | Snapshot | One-line evidence |
|---|---|---|
| C1 | **PARTIAL** | Novelty v7 remains filename-level; closest contents, supplement inspection, and broader screening remain incomplete. |
| C2 | **PARTIAL** | Principal public sources have manifests/licenses; complete processing provenance and reproducible acquisition evidence remain limited. |
| C3 | **PARTIAL** | Narrow measured relationship is identifiable, but archived weighting/clustering used 144 groups for 142 patients. |
| C4 | **PARTIAL** | Scientific Lock2 hashes verify; the joint policy contract, task, panels, and comparison freeze remain absent. |
| C5 | **MET** | Author OLS coefficients reproduce within 1.73158e−8, resolving direction and baseline interpretation. |
| C6 | **PARTIAL** | Archived BOUND candidate exists; novelty and patient-level inferential support remain unresolved. |
| C7 | **MET** | V4 inventories 250 genes, 43 exclusions, 3,000 paired observations, separate evidence fields, and explicit uncertainty gaps. |
| C8 | **UNMET** | Zero genuine policy-improvement cycles; no final reserved-panel comparison. |
| C9 | **UNMET** | No qualifying improvement result; material host costs remain unknown/unmatched and ENDPOINT:NO stands. |
| C10 | **PARTIAL** | Archived multiplicity/sensitivity numbers verify; appropriate patient-level uncertainty and decision robustness remain unverified. |
| C11 | **PARTIAL** | Atlas/point/figure components reproduce; interval, policy comparison, and complete clean reproduction remain absent. |
| C12 | **PARTIAL** | Manuscript, manifests, histories, and reports exist; acquisition evidence, resource completeness, and current commands need repair. |
| C13 | **UNMET** | Scientific evaluation executed, but the required end-to-end research-policy cycle has not. |

SGEN002_REVIEW_SCORE: 86