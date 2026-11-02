V4 substantially improves the screen, but identity resolution and patient-strict exclusion remain incomplete. **I found two medium and four low issues; no high or critical issues.** The numerical `POOL_IDENTIFIED` verdict survives the demonstrated identity correction.

Everything was read-only. I independently recomputed the joins and graph components, executed v4 with outputs intercepted in memory, and reproduced both stored JSON artifacts exactly.

| Recomputed classification | Models | DepMap PatientIDs | Passports SIDPs | Linked components |
|---|---:|---:|---:|---:|
| Established, as implemented | 1,108 | 1,069 | 1,071 | 1,069 |
| Identity unresolved | 253 | 241 | 0 | 241 |
| C overlap | 0 | 0 | 0 | 0 |

The organoid split reproduces: **11 established, 97 unresolved**.

1. **Medium — Candidate matches are treated as resolved patient identities, including demonstrably spurious NAME matches.**  
   [Resolution logic](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v4.py:121) unions every route, then accepts any nonempty patient set into the established pool.

   Screened **ACH-000561 (`T.T`)** resolves through BROAD_ID, SIDM and COSMIC to **SIDP00970**, the esophageal line. Its RRID also agrees. Normalizing `T.T` to `TT` additionally matches **SIDP00838**, a thyroid line with a different SIDM, BROAD_ID and RRID. V4 nevertheless records both patients as resolved and counts both.

   Removing this unsupported thyroid assignment changes established SIDPs from **1,071 to 1,070**, with model count unchanged. Quarantining the ambiguous model instead leaves **1,107 models / 1,069 SIDPs**, still above threshold.

   The broader metadata also expose a COSMIC conflict: unscreened **ACH-001131 (`MS-1`)** has BROAD_ID/SIDM/RRID supporting skin patient **SIDP01069**, while its COSMIC value points to lung patient **SIDP00619**. These routes therefore cannot safely be interpreted as interchangeable patient identities.

   An in-memory NAME-only ambiguity probe also remained “established.” Separate candidate exclusion evidence from confirmed identity assignments; report conflicts explicitly rather than converting all candidates into identity edges. Such edges can create false exclusions through DSU propagation. **No actual C leakage or false C exclusion was demonstrated in the pinned dataset.**

2. **Medium — Patient-strict exclusion ignores unscreened models.**  
   [Graph construction](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v4.py:150) uses only screened rows. This misses C linkages carried by other models of a screened patient, contrary to SPEC’s “ANY of their models” rule.

   In a controlled in-memory probe, I assigned an existing C SIDM to unscreened **ACH-000003**, which shares DepMap patient **PT-puKIyc** with established screened **ACH-000009**. V4 returned success, retained ACH-000009 as established and reported zero C overlap.

   Construct the identity graph from all Model.csv rows, then select screened models for the final pool. This requires resolving issue 1 first so weak collision edges do not contaminate the expanded graph. With unchanged inputs, independently using all rows still produces zero C overlaps.

3. **Low — Multivalued identifiers are not tokenized.**  
   [Identifier indexes](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v4.py:116) treat semicolon-separated identifiers as single keys.

   Actual missed routes include:

   - **ACH-000833:** Passports BROAD_ID is `ACH-000833;ACH-001741;ACH-001189`; v4 reports NAME-only resolution despite the explicit BROAD match.
   - **ACH-000338:** duplicated BROAD value `ACH-000338;ACH-000338` prevents that route.
   - **ACH-000498:** COSMIC value `907284;1330932` prevents the COSMIC route.

   Other routes rescue all three, so current classification counts remain unchanged. Split identifier lists before indexing and preserve sets of patients per key.

4. **Low — Known C-connected models can be labeled unresolved.**  
   [Classification order](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v4.py:159) checks missing direct resolution before checking the model’s patient component.

   In a probe linking screened ACH-000614 to C, its unresolved screened sibling **ACH-002461**, sharing the same DepMap PatientID, remained in `identity_unresolved` instead of `c_overlap`. Both stay outside the established pool, so eligibility is conservative, but overlap reporting is incomplete. Check component-level C membership first.

5. **Low — V4 drops specified metadata diagnostics.**  
   [Report construction](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v4.py:185) omits the screen-row count, whole-table distinct PatientIDs, total screened PatientIDs and separate C-overlap counts by key required by the retained SPEC methods.

   Independently, these are **1,604 screens**, **2,315 whole-table PatientIDs**, and **1,305 screened PatientIDs**. All five implemented C-key overlap counts are zero. Restore these diagnostics so the current report is independently interpretable.

6. **Low — Compute-then-write is fixed, but the output pair remains nontransactional.**  
   [Output writes](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen010_screen_v4.py:227) now follow complete computation. A computation-failure probe opened neither output.

   However, the report is committed before the pool file is opened. Simulating `FileExistsError` on the second output left a complete first report and no newly written pool. Interruption can likewise leave partial state. Pair-level failure handling remains necessary to fully close the original transaction finding.

The remaining v1 checks passed:

- **Unresolved exclusion:** all 253 directly unresolved screened models are excluded from the established pool; the organoid residual is accurately disclosed. Identity-route qualification remains issue 1.
- **Dual patient spaces and DSU:** reported counts reproduce. DSU passed **500 randomized graph comparisons** against independent reachability; a screened C-positive propagation probe correctly excluded both connected models. Graph coverage remains issue 2.
- **Ledger correction:** original sgen010 entries at lines 68–72 are unchanged byte-for-byte against the prior review’s captured output; captured lines 61–72 also match. The appended correction supersedes “verdict not used” and discloses the adaptive v2 bridge. Original, v3 and v4 SPEC hashes reconstruct exactly. Available timestamps support the v4 amendment preceding implementation and execution.
- **Hash enforcement:** all four actual input hashes match their constants. Simulated mismatch for each input returned refusal before CSV parsing or output writes. Reassigning one singleton C patient to ACH-000001’s Passports patient preserved **148 resolved / 142 patients**, but the canonical-map guard rejected it with no output writes. This closes the v1 negative probe.
- **DepmapModelType:** present; both distributions reproduce.
- **Outcome handling:** the four designated Model.csv clinical columns are dropped. Passports still retains its clinical fields, including 41 prior-therapy outcomes and 24 regression scores, unused. The current, explicitly scoped “no dependency-outcome access” wording is accurate.

SGEN010_V4_SCORE: 84