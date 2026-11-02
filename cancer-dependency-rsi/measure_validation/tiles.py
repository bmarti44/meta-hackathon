"""tiles.py split STEM NX NY OVERLAP SCALE  -> data/tiles/STEM_r{i}_c{j}.png + manifest
   tiles.py merge STEM PROMPTTAG [PROMPTTAG...] -> out/STEM_merged_<tags>.lab/.json (instances deduped by IoU)"""
import sys, json, os, numpy as np
from PIL import Image
cmd, stem = sys.argv[1], sys.argv[2]
man = f'data/tiles/{stem}.json'
if cmd == 'split':
    nx, ny, ov, sc = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
    im = Image.open(f'data/png/{stem}.png'); W, H = im.size; os.makedirs('data/tiles', exist_ok=True)
    tw, th = W // nx, H // ny; tiles = []
    for i in range(ny):
        for j in range(nx):
            x0, y0 = max(0, j * tw - ov), max(0, i * th - ov); x1, y1 = min(W, (j + 1) * tw + ov), min(H, (i + 1) * th + ov)
            f = f'data/tiles/{stem}_r{i}_c{j}.png'; im.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * sc), int((y1 - y0) * sc)), Image.LANCZOS).save(f)
            tiles.append(dict(f=f, x0=x0, y0=y0, x1=x1, y1=y1))
    json.dump(dict(W=W, H=H, sc=sc, tiles=tiles), open(man, 'w')); print(len(tiles), 'tiles')
else:
    M = json.load(open(man)); W, H, sc = M['W'], M['H'], M['sc']; tags = sys.argv[3:]
    inst = []   # (area, conf, mask coords)
    for tag in tags:
        for t in M['tiles']:
            pre = 'out/' + os.path.basename(t['f'])[:-4] + '_' + tag; j = json.load(open(pre + '.json'))
            if not j['n']: continue
            lab = np.frombuffer(open(pre + '.lab', 'rb').read(), dtype=np.uint16).reshape(j['H'], j['W'])
            lab = np.array(Image.fromarray(lab).resize((t['x1'] - t['x0'], t['y1'] - t['y0']), Image.NEAREST))
            conf = {o['label']: (o['conf'] or 0) for o in j['objs']}
            for k in np.unique(lab):
                if not k: continue
                ys, xs = np.nonzero(lab == k)
                # drop objects cut by an inner tile edge (they are found whole in the neighbouring tile)
                edge = (xs.min() == 0 and t['x0'] > 0) or (ys.min() == 0 and t['y0'] > 0) or (xs.max() == lab.shape[1] - 1 and t['x1'] < W) or (ys.max() == lab.shape[0] - 1 and t['y1'] < H)
                if edge: continue
                inst.append((conf[k], ys + t['y0'], xs + t['x0']))
    inst.sort(key=lambda r: -r[0]); out = np.zeros((H, W), np.uint16); n = 0; objs = []
    for c, ys, xs in inst:
        cur = out[ys, xs]; occ = (cur > 0).mean()
        if occ > 0.3: continue   # already covered by a more confident instance
        n += 1; free = cur == 0; out[ys[free], xs[free]] = n; objs.append(dict(label=n, conf=c, area=int(free.sum())))
    tag = '_'.join(tags); pre = f'out/{stem}_merged_{tag}'
    open(pre + '.lab', 'wb').write(out.tobytes()); json.dump(dict(W=W, H=H, n=n, objs=objs), open(pre + '.json', 'w')); print(pre, n, 'instances')
