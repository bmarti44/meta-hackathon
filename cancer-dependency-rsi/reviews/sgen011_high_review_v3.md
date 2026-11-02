**`NEITHER_PASSES` is confirmed.** All five original residuals are fixed. Regression probes found **0 critical, 0 high, 1 medium, and 1 low issue**.

1. **Medium — Events pricing loses per-turn rate boundaries.** [The fallback sums tokens before calling `price_entry`](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/host_cost_estimate.py:104), which can incorrectly trigger long-context rates. Two turns containing 200,000 input/1,000 output tokens each should cost **$0.82** under the script’s per-entry schedule; the executable returns **$1.63**. Sum `price_entry(u)` across turns while separately aggregating token counts. Current v6 is unaffected because it has no events-priced rows.

2. **Low — Events provenance text still describes the old algorithm.** The source label remains `events_last_usage`, and the [generated caveat](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/host_cost_estimate_v6.json:78) says only the last usage record is used. Update both to describe per-turn summation.

Verification of the five requested fixes:

| Residual | Result |
|---|---|
| B prerequisites | **Closed.** B requires precision AND crosswalk AND renewed component-level C-exclusion. All three statuses are reported false; decision-rule text is updated. Forcing precision true still leaves B rejected. |
| Two-turn reconstruction | **Closed for both requested probes.** 1,000 input/100 output followed by 2,000/200 costs **$0.009**; reversed order also costs **$0.009**. Rate-boundary regression described above remains. |
| Duplicate extraction | **Closed.** Each `turn.completed` is extracted once. The single-turn probe costs the expected **$0.003**. |
| Derived-input hashes | **Closed.** Both derived hashes appear in report inputs and match their files. Independently substituting either hash causes rejection. |
| Separate subtotals | **Closed.** Events-only fixture: receipt **$0**, events **$0.03**. Mixed fixture: receipt **$0.06**, events **$0.03**, total **$0.09**. |

The screen executable reproduces `screen_v3.json` **byte-for-byte**, including `A_pass=false`, `B_pass=false`, and `NEITHER_PASSES`.

V6 independently reconciles:

| Quantity | Exact USD |
|---|---:|
| Receipt subtotal — 60 calls | 28.8943586 |
| Events subtotal — 0 calls | 0 |
| Imputed subtotal — 5 calls | 5.1131000 |
| **Total — 65 unique reservations** | **34.0074586** |

The displayed **$34.01** is correct. Exact phase totals are **$18.8958666** and **$15.1115920**. V6 adds the v2 review receipt (**$0.5660308**) to v5; existing rows are unchanged. The current v3 review reservation postdates the snapshot.

Using the frozen reservation set, regeneration reproduces v6 JSON exactly and every CSV row. All probes captured outputs in memory; no files were written.

SGEN011_V3_SCORE: 96