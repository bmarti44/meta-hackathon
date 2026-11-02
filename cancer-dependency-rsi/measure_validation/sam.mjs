// node sam.mjs IMAGE.png "prompt" OUTPREFIX   (key from MUSE_KEY env; never printed)
import { readFileSync, writeFileSync } from 'node:fs';
import { parseImageStream, recordsOfKind, decodeMaskToRaster } from '@meta-sam/parser';
const [img, prompt, out] = process.argv.slice(2);
const b64 = readFileSync(img).toString('base64');
const t0 = Date.now();
const res = await fetch('https://api.meta.ai/v1/responses', {
  method: 'POST',
  headers: { authorization: `Bearer ${process.env.MUSE_KEY}`, 'content-type': 'application/json' },
  body: JSON.stringify({ model: 'sam-3.1', store: false, metadata: { include_confidence: 'true' },
    input: [{ type: 'message', role: 'user', content: [{ type: 'input_text', text: prompt }, { type: 'input_image', image_url: `data:image/png;base64,${b64}` }] }] }),
});
const body = await res.json();
if (!res.ok) { console.error('HTTP', res.status, JSON.stringify(body).slice(0, 400)); process.exit(1); }
const text = (body.output || []).flatMap(o => o.content || []).filter(c => c.type === 'output_text').map(c => c.text).join('');
writeFileSync(out + '.txt', text);
writeFileSync(out + '.body.json', JSON.stringify(body, null, 1).slice(0, 4000));
if (!text) { writeFileSync(out + '.json', JSON.stringify({ prompt, n: 0, ms: Date.now() - t0, objs: [] })); console.log(`${img.split('/').pop()} "${prompt}": 0 objects`); process.exit(0); }
async function* ev() {
  if (text) { yield { type: 'response.output_text.delta', item_id: 'm', output_index: 0, content_index: 0, delta: text };
    yield { type: 'response.output_text.done', item_id: 'm', output_index: 0, content_index: 0, text }; }
  yield { type: 'response.completed' };
}
const parsed = parseImageStream(ev()); for await (const _ of parsed) {}
const result = await parsed.finalResult;
const W = +(text.match(/;w=(\d+)/)?.[1] || 0), H = +(text.match(/;h=(\d+)/)?.[1] || 0);
const lab = new Uint16Array(W * H); const objs = [];
const masks = [...recordsOfKind(result.records, 'mask')].sort((a, b) => (a.confidence ?? 0) - (b.confidence ?? 0));
masks.forEach((m, k) => {
  const r = decodeMaskToRaster(m.mask), { left, top } = m.bounds, mw = m.mask.width, mh = m.mask.height;
  let area = 0;
  for (let y = 0; y < mh; y++) for (let x = 0; x < mw; x++) if (r[y * mw + x]) { const X = left + x, Y = top + y; if (X < W && Y < H) { lab[Y * W + X] = k + 1; area++; } }
  objs.push({ label: k + 1, id: m.objectId, conf: m.confidence, bounds: m.bounds, area });
});
writeFileSync(out + '.lab', Buffer.from(lab.buffer));
writeFileSync(out + '.json', JSON.stringify({ prompt, W, H, n: objs.length, ms: Date.now() - t0, diagnostics: result.diagnostics.length, objs }));
console.log(`${img.split('/').pop()} "${prompt}": ${objs.length} objects, ${Date.now() - t0} ms`);
