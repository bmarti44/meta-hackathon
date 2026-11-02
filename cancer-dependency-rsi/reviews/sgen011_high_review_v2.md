**`NEITHER_PASSES` remains supported. The eight findings are not all fully closed.** Remaining issues: **0 critical, 0 high, 3 medium, 2 low**.

All verification was read-only; executable outputs were captured in memory.

1. **Medium — B’s executable gate omits the amended prerequisites.** The SPEC now requires the applicable authoritative crosswalk and renewed component-level C-exclusion checks, but [`b_pass` still equals `precB["pass"]`](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen011_screen_v2.py:155). The generated `decision_rule` also says B needs only precision. Make these prerequisites explicit executable gates and report their status. This does not change today’s rejection: B fails precision.

2. **Medium — Monotonic usage does not establish cumulative semantics.** The [events reconstruction rule](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/host_cost_estimate.py:100) treats increasing token counts as cumulative checkpoints. Two independent completed turns containing respectively 1,000 input/100 output and 2,000 input/200 output tokens should cost **$0.009**; the executable returns **$0.006**. The verified single-turn history cannot establish semantics for multiple turns. Use documented counter semantics or apply the disclosed missing-usage imputation.

3. **Medium — The new summation branch double-counts completed turns.** Each top-level `turn.completed` usage is [appended twice](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/host_cost_estimate.py:89). Previously, selecting the last record concealed this duplication; the new nonmonotone branch sums both copies. Reversing the two turns above produces **$0.018**, versus the correct **$0.009**. Extract each usage event once before reconstruction.

4. **Low — The screen report still omits derived-input hashes.** Both derived artifacts are pinned and enforced correctly, but the [report’s `inputs` mapping](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen011_screen_v2.py:161) records only the raw CSV hashes. Include `established_pool_v4.json` and `screen_v7.json` so the saved result carries its identity-artifact provenance.

5. **Low — The receipt subtotal includes events-priced costs.** [`receipt_priced_subtotal_usd`](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/host_cost_estimate.py:167) includes both receipt and events rows despite their separate counts. An events-only $0.03 fixture reports zero receipt-priced calls but a $0.03 receipt subtotal. Separate the subtotals or rename the combined field. The frozen v5 value is correct because it contains no events-priced rows.

Verification of the eight requested closures:

| Prior finding | Re-review result |
|---|---|
| **1. Scientific scope** | **Closed.** [Amendment v2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen011/SPEC.md:50) explicitly limits the screen to necessary conditions, identifies precision as optimistic, and treats 0.146 as a screen convention requiring future scientific justification. |
| **2. A includes organoids** | **Closed.** Independently recomputed **1,095 cell-line models / 1,057 linked components**, MDR **0.08608101374934927**, displayed as **0.0861**. |
| **3. B prerequisites** | **Documentary closure only.** The amended SPEC is explicit; the executable and generated decision-rule description retain the precision-only rule described above. |
| **4. Premature witnesses** | **Closed.** [Panels, task-specific replay, and task/arm cost attribution](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/pgen005/WITNESSES.md:5) are unchecked and pending. Rollouts remain blocked. |
| **5. Derived inputs/components** | **Runtime closure verified; reporting residual above.** Both hashes match; simulated mismatches are rejected. Independently rerunning sgen010 reproduces both saved artifacts exactly. Its graph over all 2,554 models confirms the subset component counts. |
| **6. Events reconstruction/attribution** | **Partially closed.** All **59 usage-bearing event files** contain one completed turn whose complete usage dictionary matches its receipt. Reservation attribution works for current naming. Multiple-turn reconstruction fails the two probes above. |
| **7. Full-precision aggregation** | **Closed.** Receipt costs and imputation maxima retain precision through aggregation; exact totals reconcile below. |
| **8. Counts/subtotals** | **Frozen snapshot correct; fallback-label residual above.** There are **59 receipt-priced, 0 events-priced, 5 imputed, 64 accounted calls**, with 64 unique reservation IDs. Every receipt and imputation recomputes correctly. |

The exact v5 reconciliation is:

| Quantity | USD |
|---|---:|
| Receipt-priced subtotal | 28.3283278 |
| Imputed subtotal | 5.1131000 |
| **Total** | **33.4414278** |
| phase2_lock1 | 18.8958666 |
| phase6_7 | 14.5455612 |

The displayed **$33.44** is correct. Separately rounded phase amounts sum to $33.45; their unrounded values reconcile exactly.

The screen executable reproduces `screen_v2.json` exactly. B remains **11 components**, MDR **0.7575796853**, requiring **366** under the stated approximation. The current review reservation postdates the frozen accounting snapshot and is not a missing v5 entry. Neither events-reconstruction defect affects v5’s current total.

SGEN011_V2_SCORE: 91