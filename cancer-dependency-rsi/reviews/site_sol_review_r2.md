SCORE: 84/100

VERDICT: Substantially improved, but below “ship it.” The exports remain accurate, draft status is now honest, and downloads and explorer controls are stronger. The visual design and creation story remain compelling from source. Remaining causal headlines still exceed the evidence, several dispositions are only partial, and the scroll fix introduces a regression that bypasses the opening story.

**ROUND-1 DISPOSITION CHECK**

| Issue | Disposition and verified evidence |
|---|---|
| Denominator | **PARTIAL — remaining medium.** Hero and OG correctly scope 85% to this reanalysis’s 456 dependencies. However, [index.html:442](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:442) says 47% of Broad’s “published hits.” That is **135/285 gains present in the audit**; gains and losses together are **266/537 = 49.53%**. Smallest fix: explicitly say “published gains present in our audit.” |
| Causal wording | **PARTIAL — high.** The diagonal explanation now defines observational consistency correctly. But [index.html:355](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:355) still says “Almost nothing needs the dome”; line 318 promises what the medium “explains”; line 484 claims comparisons “separate food from shape”; table/detail labels still say “shape only.” The source contains **34 hits with F/D≥0.5**, despite no genome-wide-significant F contrasts. Smallest fix: describe detected consistency and limited format evidence, and label F “dome versus adherent.” |
| Publication status | **FIXED.** [index.html:592](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:592), BibTeX at 603, and Downloads at 614 identify an unpublished draft. Downloads explicitly disclose pending posting and author placeholders. PDF placeholders remain, as disclosed; ZIP handoff instructions also treat posting as future work. |
| Flag-zero wording | **FIXED.** [index.html:646](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:646) and the tooltip use “Below hit threshold.” The verdict correctly distinguishes significance from the effect cutoff. MAPK11 now says it differs significantly, has Δ−0.21 and **q<0.001**, and fails the effect-size threshold. |
| Offscreen gene details | **FIXED for the flagged paths.** [index.html:720](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:720) reveals offscreen details. Incoming ITGB1 links and offscreen gene-button selections request scrolling. Initial selection now causes a separate regression, N1 below. |
| Missing code/source download | **FIXED.** [index.html:615](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:615) links a valid ZIP containing analysis scripts and review material. Gene details link the primary CSV at line 713. |
| Mouse-only controls | **PARTIAL.** Native gene/header buttons work, and the inactive rail uses `visibility:hidden`. However, sorting replaces the focused button, and some `aria-sort` values are incorrect. See N2–N3. |
| Contrast | **PARTIAL — remaining low.** Corrected backgrounds provide **5.29:1, 5.64:1 and 5.99:1** against white. But [index.html:211](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:211) restores white on `#ff4b2e` when hovering the primary button: **3.33:1** for 13px text. Smallest fix: retain a dark background on hover. |
| Visual fallbacks | **PARTIAL — medium.** Forced renderer failure installs fig1 and hides stage captions. Nevertheless, [index.html:318](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:318) still promises hoverable points. Reduced motion removes autonomous displacement and chapter translations, but the formation timeline still morphs thousands of points. Smallest fixes: change fallback instructions and use a stationary formation under reduced motion. |
| Picking/highlight alignment | **PARTIAL — medium.** [index.html:935](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:935) mirrors idle drift, but still omits shader intro scaling and mouse repulsion. A settled SQLE arithmetic fixture at 1440×900 produced **26.4px** separation. Enlarging the picking radius does not align positions. Smallest fix: mirror those transformations, or disable repulsion and defer picking until intro completion. |
| Repeated redirect parameters | **FIXED in source.** [apex_redirect.js:9](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/apex_redirect.js:9) serializes every `multiValue` entry. Fixtures preserve `?x=one&x=two`, encoded values, empty values and www passthrough. Deployment was not independently verified. |
| Clipboard false success | **FIXED.** [index.html:663](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:663) checks the copy result. Failed legacy copying and rejected Clipboard API calls open the text prompt without showing “Copied.” |
| Polluted medium-gains ticker | **FIXED.** [build_site_data.py:91](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/build_site_data.py:91) filters medium-consistent gains before ranking. All 12 published entries match that ranking; HSD17B7 and AIRIM are excluded. |
| Signed reproduction sorting | **FIXED numerically.** [index.html:746](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:746) sorts signed ratios. STK38L is last in descending order and first in ascending order. Direction descriptions still have N2’s defect. |
| Rendering behind paper | **FIXED for computation.** Highlight updates calculate one point. A 100-tick paper-mode fixture issued zero renders. The early return introduces N4 below. |

**NEW ISSUES**

**CRITICAL / HIGH**

None newly verified. The remaining round-one causal-language issue is still high severity.

**MEDIUM**

- **N1 — Bare-root visits automatically bypass the opening story.** [index.html:900](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:900) calls `select("SQLE", false)` without a gene hash. The new `scroll || !inView` condition overrides that false argument. The startup fixture recorded a scroll to `detail` with offset −90 and changed the hash to `#gene=SQLE`. Visitors are sent past the principal visual introduction. **Smallest fix:** only select during initialization when an incoming gene hash exists.

**LOW**

- **N2 — Sorting descriptions contradict the actual order.** [index.html:755](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:755), also line 763. Gene ascending order starts with **A1BG**, but announces `aria-sort="descending"`. Ascending ratio order starts with **STK38L**, while the caption still says “sorted high to low.” Re-rendering preserves these errors. **Smallest fix:** derive direction text, arrows and ARIA from the comparator’s actual direction for each column.

- **N3 — Sorting replaces the focused control.** [index.html:762](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:762) replaces every header’s `innerHTML` after activation, removing the active `.thbtn`; no focus restoration exists. This interrupts consecutive keyboard sorting. **Smallest fix:** preserve the button node, or restore focus to its replacement when the removed button held focus.

- **N4 — Paper rendering stops while the stage is still visible.** [index.html:1179](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:1179) returns as soon as paper mode activates, which occurs at `top 52%` on line 1295. The visible upper stage freezes, and opacity changes never reach the renderer. The fixture also retained `body.style.cursor="pointer"` after entering paper mode. **Smallest fix:** suspend rendering once paper fully covers the viewport, and clear the body cursor when entering paper mode.

**CHECKS RUN**

- Read all site HTML/JavaScript, redirect, generator, regression tests and round-one dispositions.
- Compared **all 17,525 records**, exported contrasts, ratios, flags, probabilities, raw effects and bootstrap frequencies against source artifacts: **zero mismatches**.
- Rebuilt catalogue tags: **zero mismatches**. Rechecked counts, Broad denominators, summary statistics and downloadable CSV equality.
- Ran `.venv/bin/python -B -m pytest -q -s -p no:cacheprovider tests/test_site_data.py`: **4 passed**.
- Executed inline Node VM checks for initialization, gene selection, sorting, repeated rendering, verdict strings, clipboard failures, fetch failure and redirects.
- Exercised stage logic using the bundled Three.js math with a renderer stub: CPU/shader positions, reduced motion, renderer failure, paper suspension and resumption.
- Checked ZIP integrity/content, seven-page PDF text, asset/fragment targets, duplicate IDs, contrast and canonical URL strings.
- **Limits:** no real-browser/mobile rendering, GPU profiling, or live DNS/TLS/CloudFront verification. Pixel discrepancies above are numerical fixtures.