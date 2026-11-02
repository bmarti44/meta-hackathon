SCORE: 89/100

VERDICT: Minor fixes before shipping. The three reported instances were corrected, and no regression from those edits was found. The broader sweep still finds misleading formulation-match wording and normal-text contrast failures, keeping this below the 90-point ship threshold.

**PER-ITEM DISPOSITION CHECK**

| Item | Disposition and evidence |
|---|---|
| Causal-isolation phrases | **Reported instances fixed; class remains partial.** [Figure caption](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:439) now says “dome-versus-adherent contrast within the organoid-medium family.” The [timeline](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:487) uses “same medium family (the shape contrast).” Another instance remains below. |
| Two hover contrasts | **Both fixed; class remains partial.** [Paper-link hover](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:154) is `#b02e12` on paper: **5.50:1**. [Popular-gene hover](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:168) is white on `#b02e12`: **6.47:1**. |
| CPU smoothstep order | **Fixed.** [CPU](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:960) now computes `mouseOn * smoothstep(falloff)`, matching the [shader’s order](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:1074). Across **1,120 arithmetic comparisons**, maximum residual was **0.00000435 world units**, attributable to the differing π constants. First-pointer-tick projected separation fell to **0.000015px**. No further actionable arithmetic mismatch was found. |

**NEW ISSUES — remaining instances found by the sweep**

**CRITICAL / HIGH:** None.

**MEDIUM**

- **Methods still implies identical formulations.** [Line 539](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:539) asks what remains when “comparing blobs to flat on the same food,” while [limitations](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:561) explicitly say “mixed (not identical) formulations.” This still suggests cleaner isolation than the comparison establishes. **Smallest fix:** say “comparing domes with adherent models within the organoid-medium family.” Apply that qualification to the repeated “same-medium” shorthand in the narrative, table, detail and citation labels.

**LOW**

- **Other normal-text combinations remain below 4.5:1.** These are existing leftovers, not regressions introduced by the six edited lines.

| Verified instance | Contrast | Smallest fix |
|---|---:|---|
| Default [paper links](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:153), section/timeline labels and summary hover: `#c93318` on `#f3ecdd` | **4.4968:1** | Use existing `#b02e12` for `--phenol-dk`; do not round this into a pass. |
| [Rail hover labels](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:78), axis notes and stage captions using `--faint` | **3.42:1** on base background; **3.63:1** even against black | Use `--bone-dim`. |
| [Search placeholder](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:165) | **2.95:1** | Use `--ink-mut`. |
| [Header gene count](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:67) remains amber in paper mode | **1.73:1** on paper | Override `.live-chip b` to `--ink-mut` in paper mode. |
| [Dim ticker text](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:138), including opacity compositing | **2.54:1** | Remove the text opacity reduction. |
| [Selected text](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:33): white on orange | **3.33:1** | Use the darker red selection background. |
| [Figure 1](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/assets/fig1.png): black FASN annotation crosses red markers | **3.86:1** | Give annotations a white background in [the figure generator](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/make_figures.py:39). |

**CHECKS RUN**

- Recovered all **1,360 round-3 source lines** from its recorded output; comparison found exactly the six intended changed lines.
- Ran `pytest -q -s -p no:cacheprovider tests/test_site_data.py`: **5 passed**.
- Rebuilt both JSON exports entirely in memory: **byte-for-byte matches**. Confirmed **17,525 genes; 456 hits; 387 medium-consistent; 68 unresolved; one format candidate**.
- Re-executed explorer, deep-link, sorting/ARIA/focus, clipboard-failure, fetch-failure and redirect fixtures: passed.
- Re-executed stage arithmetic, formation, reduced-motion, WebGL-fallback and paper suspension/resumption fixtures: passed.
- Checked asset equality, ZIP integrity, local targets, duplicate IDs, downloadable prose/PDF, figures and CSS contrast.

Limits: no real-browser/mobile rendering, GPU execution or live deployment verification. CPU/shader results above are numerical fixtures.