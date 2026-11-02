"""Instance matching at IoU>=0.5. evalseg.py IMAGE_STEM PRED... (pred = out/<prefix> for SAM, or cellpose/stardist)"""
import sys, json, numpy as np
from PIL import Image
def load_gt(stem): return np.array(Image.open(f'data/test/{stem}_mask.tif')).astype(np.int64)
def load_pred(stem, p):
    if p in ('Cellpose', 'StarDist'): return np.array(Image.open(f'data/cellpose/{stem}_{p}Mask.tif')).astype(np.int64)
    j = json.load(open(p + '.json'))
    if not j['n']: return None
    return np.frombuffer(open(p + '.lab', 'rb').read(), dtype=np.uint16).reshape(j['H'], j['W']).astype(np.int64)
def score(gt, pr):
    ng = len(np.unique(gt)) - 1
    if pr is None: return dict(gt=ng, pred=0, tp=0, prec=0, rec=0, f1=0, miou=0, area_r=float('nan'))
    np_ = len(np.unique(pr)) - 1
    m = (gt > 0) | (pr > 0); g, p = gt[m], pr[m]
    pairs = np.stack([g, p], 1); u, c = np.unique(pairs, axis=0, return_counts=True)
    ga = np.bincount(gt.ravel()); pa = np.bincount(pr.ravel())
    cand = []
    for (a, b), n in zip(u, c):
        if a and b: iou = n / (ga[a] + pa[b] - n); cand.append((iou, a, b))
    cand.sort(reverse=True); ug, up, mt = set(), set(), []
    for iou, a, b in cand:
        if iou < 0.5: break
        if a in ug or b in up: continue
        ug.add(a); up.add(b); mt.append((iou, ga[a], pa[b]))
    tp = len(mt); prec = tp / max(np_, 1); rec = tp / max(ng, 1)
    ar = np.corrcoef([x[1] for x in mt], [x[2] for x in mt])[0, 1] if tp > 2 else float('nan')
    return dict(gt=ng, pred=np_, tp=tp, prec=round(prec, 2), rec=round(rec, 2), f1=round(2 * prec * rec / max(prec + rec, 1e-9), 2), miou=round(float(np.mean([x[0] for x in mt])) if mt else 0, 2), area_r=round(float(ar), 3))
stem = sys.argv[1]; gt = load_gt(stem)
for p in sys.argv[2:]:
    print(f'{p.split("/")[-1]:28s}', score(gt, load_pred(stem, p)))
