**ABSENT remains upheld, but v2 is OPEN: 89/100.** Two findings remain partially resolved. Review was read-only and metadata-only; execution used intercepted writes in memory.

1. **Terminal-window commitment — resolved.** The SPEC addendum explicitly commits to terminal three-node windows. Synthetic `A→B→A→A` and `A→B→A→A→A` cases follow that rule.

2. **First-qualified-ancestor pairing — resolved.** Branches with different window ancestors now pair through their shared first qualified ancestor. The fixture produces one qualified model.

3. **Dangling parents — partially resolved; medium.** Both actual records are correctly reported:
   - `MC-002109-k258` / `ACH-002109`
   - `MC-002475-YGSw` / `ACH-002475`

   Neither is strictly screened. However, [code line 66](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen018_inventory_v2.py:66) removes the dangling marker and continues qualification with the truncated chain. A synthetic dangling-prefix fixture still produces **one qualified model**, treating its first observed node as the pairing ancestor. This conflicts with the [addendum’s commitment](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen018/SPEC.md:32) that dangling parents are never treated as roots. Reject affected paths from qualification, or explicitly commit to allowing flagged observed suffixes.

4. **Semantics and coverage nonclaims — resolved.** The inventory acknowledges unverified parent semantics, possible incomplete lineage recording, and absence of the recorded resource. Independently confirmed: all eight parent-bearing rows contain `AnchorDrug`; **1,228 conditions are unqualified**.

5. **Key normalization — partially resolved; low.** Whitespace is now stripped, but [key equality still preserves capitalization](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen018_inventory_v2.py:32). Changing a return terminal from `Adherent` to `adherent` suppresses the return and changes the fixture from one qualified model to zero. Return the normalized format. No current normalization collisions were found.

6. **Deterministic pairs — resolved.** All qualifying ancestor/library pairs are retained and sorted. A three-library fixture preserves all three in deterministic order.

7. **Dated-transition wording — resolved.** The nonclaim now distinguishes screen `Days` from dated condition transitions and elapsed time between history nodes.

The regenerated inventory matches the saved v2 artifact exactly except for its timestamp. Counts remain **3,385 conditions; 2,476 models; depths `{1: 3379, 2: 6}`; no qualifying patterns; zero qualified models; ABSENT**. Depth one still includes 3,377 genuine roots plus the two dangling records. Strict-screen counts also remain unchanged: **3,042 sequences, 1,367 screens/condition nodes, including 1,031 qualified nodes**.

SGEN018_V2: OPEN
SGEN018_V2_SCORE: 89