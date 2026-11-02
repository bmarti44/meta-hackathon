# Validating SAM 3.1 for organoid measurement

How we checked that Meta's SAM 3.1 can measure organoids before building the site's "Measure your organoids" tool.

**Data:** the held-out test split of OrganoIDNetData (Kulkarni et al., *Scientific Data* 11, 820, 2024; [Zenodo 10643410](https://zenodo.org/records/10643410), CC BY 4.0). It has 10 brightfield images of pancreatic cancer organoids (two time-lapses, human and mouse) with hand-drawn instance masks, plus the authors' Cellpose and StarDist predictions trained on the same dataset.

**Scripts:**

| File | What it does |
|---|---|
| `rzip.py` | Lists or pulls single files from the 4.6 GB Zenodo zip with HTTP range requests |
| `sam.mjs` | Sends one image and a text prompt to `sam-3.1` (Meta Model API, `store: false`) and writes a label map (key from `MUSE_KEY`, never printed) |
| `tiles.py` | Splits an image into enlarged overlapping tiles, and merges per-tile results back, dropping objects cut by inner tile edges |
| `evalseg.py` | Matches predicted to hand-drawn organoids at IoU ≥ 0.5: precision, recall, F1, mean IoU, size correlation |

```sh
npm install --ignore-scripts
python3 rzip.py https://zenodo.org/records/10643410/files/OrganoIDNetData.zip list > listing.txt
# pull Dataset/Test/{Images,Masks} and Source_Codes/Cellpose/AlgorithmPredictions, convert TIFF to PNG, then:
MUSE_KEY=... node sam.mjs data/png/Test_Human_1_004h.png bubble out/h004_bubble
python3 evalseg.py Test_Human_1_004h Cellpose StarDist out/h004_bubble
```

## Results

- **Prompt:** "organoid", "sphere", "spheroid" and "blob" return nothing. "bubble" and "cell" work best.
- **Sparse human images (5 time points, whole image):** SAM F1 0.61 to 0.78 (mean about 0.69); Cellpose F1 0.76 to 0.85. Mean IoU of matched outlines: SAM 0.80 to 0.81, Cellpose 0.75.
- **Dense mouse image (1,884 organoids), 16 enlarged tiles:** SAM F1 0.55 to 0.57, precision 0.79 to 0.86; Cellpose F1 0.59, precision 0.88. Even Cellpose finds only 45%.
- **Size accuracy:** area correlation with hand-drawn outlines 0.92 to 0.97 (Cellpose 0.96).
- **Size bias:** recall rises with size (human: 12% under 100 px², 72% at 200 to 400 px², 100% at 400 to 800 px²). Missing the smallest organoids inflates medians and shrinks differences, so the site compares only organoids at least 20 px across (about 314 px²) in both conditions.
- **Comparisons with that floor:** mouse vs human size ratio 0.72 to 0.75 from run to run (hand-drawn, same floor: 0.81; with no floor: 0.54). The same human well at 4 h and 20 h: 1.02 (hand-drawn: about 1.05).
- **Statistics check:** in 400 simulated comparisons with no true difference, p < 0.05 occurred 5.8% of the time and the bootstrap 95% range covered 1 in 95.3%.

The test images are human and mouse organoids, not a cholesterol experiment; they show that measurement and comparison work, not what the add-back test will find.
