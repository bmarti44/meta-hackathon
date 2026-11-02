// It's the Medium: deterministic frame renderer. window.renderAt(t) draws the frame at time t (seconds).
// Layers: #under (2D: dishes, liquids), #gl (three.js: cells, gene field, demo screens), #over (2D: type, labels, captions, grain).
import * as THREE from './three.module.min.js';

const W = 1920, H = 1080;
const C = { bg: '#0c0a08', bone: '#f3ecdd', dim: '#c4b9a2', mute: '#8f846f', red: '#ff4b2e', redDk: '#b02e12', amber: '#eda93c', blue: '#7fd4ff', green: '#5fd39b', line: 'rgba(243,236,221,0.16)' };
const RGB = { bone: [0.953, 0.925, 0.867], red: [1.0, 0.36, 0.26], amber: [0.93, 0.66, 0.24], blue: [0.5, 0.83, 1.0], dim: [0.45, 0.41, 0.35], cell: [0.96, 0.84, 0.78] };
const SERIF = '"Fraunces", Georgia, serif', SANS = '"Archivo", Helvetica, Arial, sans-serif', MONO = '"IBM Plex Mono", Menlo, monospace';

/* ---------------- utilities ---------------- */
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ramp = (t, a, b) => clamp((t - a) / (b - a));
const ease = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;          // in-out cubic
const eout = x => 1 - Math.pow(1 - x, 3);                                              // out cubic
const expo = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const lerp = (a, b, k) => a + (b - a) * k;
const win = (t, a, b, fi = 0.5, fo = 0.5) => Math.min(eout(ramp(t, a, a + fi)), 1 - ease(ramp(t, b - fo, b)));  // fade in at a, out at b
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

/* ---------------- data ---------------- */
const VAR = new URLSearchParams(location.search).get('v');   // e.g. ?v=3min renders the 3-minute cut
const [TL, GENES] = await Promise.all([fetch(`../narration/timeline${VAR ? '_' + VAR : ''}.json`).then(r => r.json()), fetch('genes.json').then(r => r.json())]);
const L = TL.lines;
const LI = new Map(L.map(l => [l.id, l]));
const NEVER = 1e6;   // lines cut from a variant resolve to a time that never arrives, so their animations stay off
const has = id => LI.has(id);
const S = id => has(id) ? LI.get(id).start : NEVER, E = id => has(id) ? LI.get(id).end : NEVER;
const SEC0 = n => L.find(l => l.sec === n)?.start ?? NEVER, SEC1 = n => [...L].reverse().find(l => l.sec === n)?.end ?? NEVER;
/* anchors that cut lines used to provide */
const NF = has('notflat') ? S('notflat') : E('flat') + 0.3;            // flat sheet lifts into an organoid
const SER = has('serum') ? S('serum') : S('clean');                    // left dish turns to serum
const SWEEP = has('small') ? E('small') + 0.05 : E('howmany') + 0.15;  // hits sweep onto the line
const WHY = has('why') ? S('why') : S('notshape') - 0.6;               // 85% card hands over to the meaning
const SAME = has('same') ? S('same') : S('notshape');                  // organoid = flat cells on the same food
const BRK = has('break') ? S('break') : SEC1(8) + 0.9;                 // end of the put-it-back test
const LOOK = has('lookup') ? S('lookup') : S('paste');                 // demo: end of the hero shot
const LOOP = has('loop') ? S('loop') : SEC1(9) + 2.0;                  // demo: end of the Muse answer
const MUSE0 = has('muse') ? S('muse') : S('ask');                      // demo: Muse typing starts
const PASTE_END = has('sam') ? S('sam') : MUSE0;                       // demo: end of the hit-list shot
const RAN_MUSE = LI.get('ran').show.includes('Muse');
const TOTAL = TL.total;
const BYG = new Map(GENES.map(g => [g.g, g]));

/* ---------------- canvases ---------------- */
const under = document.getElementById('under').getContext('2d');
const over = document.getElementById('over').getContext('2d');
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('gl'), antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.setClearColor(0x000000, 0);
renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, W / H, 0.1, 100);
camera.position.set(0, 0, 10); camera.lookAt(0, 0, 0);
const FOCAL = (H / 2) / Math.tan(THREE.MathUtils.degToRad(17.5));
const _v = new THREE.Vector3();
function toScreen(x, y, z) { _v.set(x, y, z).project(camera); return [(_v.x + 1) / 2 * W, (1 - _v.y) / 2 * H]; }

/* ---------------- point clouds (cells and genes) ---------------- */
function pointsMat(shade, depthWrite) {
  return new THREE.ShaderMaterial({
    transparent: true, depthWrite, depthTest: true,
    uniforms: { uScale: { value: FOCAL }, uShade: { value: shade } },
    vertexShader: `attribute float size; attribute vec4 rgba; varying vec4 vC; uniform float uScale;
      void main(){ vC = rgba; vec4 mv = modelViewMatrix * vec4(position, 1.0); gl_Position = projectionMatrix * mv; gl_PointSize = size * uScale / -mv.z; }`,
    fragmentShader: `varying vec4 vC; uniform float uShade;
      void main(){ vec2 p = gl_PointCoord * 2.0 - 1.0; float r = dot(p, p); if (r > 1.0 || vC.a < 0.003) discard;
        float edge = smoothstep(1.0, 0.78, r); float z = sqrt(max(0.0, 1.0 - r)); vec3 n = vec3(p.x, -p.y, z);
        float lam = 0.42 + 0.58 * max(0.0, dot(n, normalize(vec3(-0.45, 0.55, 0.7))));
        float spec = pow(max(0.0, dot(n, normalize(vec3(-0.35, 0.5, 0.8)))), 18.0) * 0.22;
        float rim = smoothstep(0.55, 1.0, r) * 0.25;
        vec3 shaded = vC.rgb * lam + spec - rim * vC.rgb;
        gl_FragColor = vec4(mix(vC.rgb, shaded, uShade), vC.a * edge); }`,
  });
}
class Cloud {
  constructor(n, shade, depthWrite) {
    this.n = n; this.pos = new Float32Array(n * 3); this.col = new Float32Array(n * 4); this.size = new Float32Array(n);
    this.g = new THREE.BufferGeometry();
    this.g.setAttribute('position', new THREE.BufferAttribute(this.pos, 3));
    this.g.setAttribute('rgba', new THREE.BufferAttribute(this.col, 4));
    this.g.setAttribute('size', new THREE.BufferAttribute(this.size, 1));
    this.obj = new THREE.Points(this.g, pointsMat(shade, depthWrite)); this.obj.frustumCulled = false; scene.add(this.obj);
  }
  set(i, x, y, z, r, g, b, a, s) { const k = i * 3, c = i * 4; this.pos[k] = x; this.pos[k + 1] = y; this.pos[k + 2] = z; this.col[c] = r; this.col[c + 1] = g; this.col[c + 2] = b; this.col[c + 3] = a; this.size[i] = s; }
  hide() { this.obj.visible = false; }
  commit() { this.obj.visible = true; for (const k of ['position', 'rgba', 'size']) this.g.attributes[k].needsUpdate = true; }
}

// cell layouts: unit sphere (fibonacci) and unit disc (sunflower)
function cellLayout(n, seed) {
  const R = rng(seed), sph = [], disc = [], jit = [];
  const ga = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < n; i++) {
    const y = 1 - (i + 0.5) / n * 2, rr = Math.sqrt(1 - y * y), th = ga * i;
    const k = 0.93 + 0.07 * R(); sph.push([Math.cos(th) * rr * k, y * k, Math.sin(th) * rr * k]);
    const rd = Math.sqrt((i + 0.5) / n), td = ga * i * 1.0007; disc.push([Math.cos(td) * rd, Math.sin(td) * rd]);
    jit.push([R(), R(), R()]);
  }
  return { sph, disc, jit };
}
const CELLS_A = 760, CELLS_B = 520;
const LA = cellLayout(CELLS_A, 11), LB = cellLayout(CELLS_B, 23);
const cloudA = new Cloud(CELLS_A, 1, true);   // the hero cells: flat sheet <-> organoid
const cloudB = new Cloud(CELLS_B, 1, true);   // flat culture in serum
const cloudC = new Cloud(CELLS_B, 1, true);   // flat culture in organoid medium

/* draw cells: m=0 flat sheet on a dish floor, m=1 organoid sphere */
function drawCells(cloud, Lx, t, o) {
  const { cx = 0, floorY = -1.1, cz = 0, discR = 2.2, sphY = 0, sphR = 1.15, m = 0, alpha = 1, grow = 1, size = 0.17, spin = 0.12, tint = RGB.cell, glow = 0 } = o;
  const n = cloud.n, th = t * spin;
  const cs = Math.cos(th), sn = Math.sin(th);
  for (let i = 0; i < n; i++) {
    const [jx, jy, jz] = Lx.jit[i];
    const mi = ease(clamp(m * 1.35 - jx * 0.35));
    const d = Lx.disc[i], s = Lx.sph[i];
    const fx = cx + d[0] * discR, fy = floorY + 0.02 + jy * 0.015, fz = cz + d[1] * discR * 0.9;
    const ux = s[0] * cs + s[2] * sn, uz = -s[0] * sn + s[2] * cs;
    const wob = 1 + 0.015 * Math.sin(t * 1.3 + jx * 20);
    const px = cx + ux * sphR * wob, py = sphY + s[1] * sphR * wob, pz = cz + uz * sphR * wob;
    // lift in an arc so the sheet visibly rises into the ball
    const arc = Math.sin(mi * Math.PI) * 0.6 * (0.5 + jz);
    const x = lerp(fx, px, mi), y = lerp(fy, py, mi) + arc, z = lerp(fz, pz, mi);
    const appear = clamp(grow * 1.3 - Math.hypot(d[0], d[1]) * 0.3 * 1.3 / 1.0);
    const shade = 0.82 + 0.18 * jz, g = glow * (0.5 + 0.5 * Math.sin(jx * 30 + t * 2));
    cloud.set(i, x, y, z, Math.min(1, tint[0] * shade + g * 0.05), tint[1] * shade, tint[2] * shade, alpha * eout(appear), size * (0.88 + 0.24 * jy) * eout(appear));
  }
  cloud.commit();
}

/* ---------------- gene field ---------------- */
const NG = GENES.length;
const field = new Cloud(NG, 0.35, false);
const GR = rng(7);
const order = GENES.map((g, i) => i).sort(() => GR() - 0.5);
const gridPos = new Array(NG);
{ const cols = 200, rows = Math.ceil(NG / cols), w = 10.8, h = 4.4;
  order.forEach((gi, k) => { const c = k % cols, r = Math.floor(k / cols);
    gridPos[gi] = [(c / (cols - 1) - 0.5) * w + (GR() - 0.5) * 0.02, (0.5 - r / (rows - 1)) * h + (GR() - 0.5) * 0.02 - 0.45, (GR() - 0.5) * 0.4]; }); }
const PLOT = { cx: 0.15, cy: -0.25, k: 2.15 };
const plotXY = (D, A) => [PLOT.cx + clamp(D, -1.25, 1.1) * PLOT.k, PLOT.cy + clamp(A, -1.25, 1.1) * PLOT.k];
const HITS = GENES.map((g, i) => [g, i]).filter(([g]) => g.f > 0);
const landT = new Map();   // when each hit lands on the plot (seconds after sweep start)
{ const R = rng(99); HITS.forEach(([g, i]) => landT.set(i, R() * 0.9 + (g.f === 1 ? 0 : 0.25))); }
const colOf = f => f === 1 ? RGB.red : f === 2 ? RGB.amber : f === 3 ? RGB.blue : RGB.bone;

/* ---------------- demo screens ---------------- */
const loader = new THREE.TextureLoader();
const texCache = new Map();
async function tex(name) {
  if (texCache.has(name)) return texCache.get(name);
  const t = await loader.loadAsync(`demo/${name}.png`);
  t.colorSpace = THREE.NoColorSpace; t.anisotropy = 8; t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter;
  texCache.set(name, t);
  if (texCache.size > 14) { const k = texCache.keys().next().value; texCache.get(k).dispose(); texCache.delete(k); }
  return t;
}
const planeMat = (shadow) => new THREE.ShaderMaterial({
  transparent: true, depthWrite: false,
  uniforms: { map: { value: null }, crop: { value: new THREE.Vector4(0, 0, 1, 1) }, op: { value: 1 }, sizePx: { value: new THREE.Vector2(1000, 600) }, rad: { value: 22 }, shadow: { value: shadow ? 1 : 0 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: `uniform sampler2D map; uniform vec4 crop; uniform float op; uniform vec2 sizePx; uniform float rad; uniform float shadow; varying vec2 vUv;
    void main(){ vec2 p = (vUv - 0.5) * sizePx; vec2 q = abs(p) - (sizePx * 0.5 - rad); float d = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - rad;
      if (shadow > 0.5) { float a = 1.0 - smoothstep(-40.0, 70.0, d); gl_FragColor = vec4(0.0, 0.0, 0.0, op * a * 0.55); return; }
      float a = 1.0 - smoothstep(-1.0, 1.0, d); vec4 c = texture2D(map, crop.xy + vUv * crop.zw);
      float border = smoothstep(-2.5, -1.0, d) * 0.35; gl_FragColor = vec4(mix(c.rgb, vec3(1.0), border), op * a); }`,
});
class Screen {
  constructor() {
    this.group = new THREE.Group(); scene.add(this.group);
    this.shadow = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), planeMat(true)); this.shadow.position.set(0.12, -0.18, -0.05);
    this.mesh = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), planeMat(false));
    this.group.add(this.shadow, this.mesh); this.group.visible = false;
  }
  async show(name, o) {
    const t = await tex(name); const img = t.image; const pad = o.pad ?? 56;
    const cw = img.width - 2 * pad, ch = img.height - 2 * pad - (o.cropBottom || 0) - (o.cropTop || 0);
    const w = o.w, h = o.h ?? w * ch / cw;
    for (const m of [this.mesh, this.shadow]) {
      m.scale.set(w, h, 1);
      const u = m.material.uniforms; u.map.value = t; u.op.value = o.op ?? 1;
      u.crop.value.set(pad / img.width, (pad + (o.cropBottom || 0)) / img.height, cw / img.width, ch / img.height);
      u.sizePx.value.set(w * FOCAL / 10, h * FOCAL / 10); u.rad.value = o.rad ?? 16;
    }
    this.shadow.material.uniforms.sizePx.value.set(w * FOCAL / 10 + 30, h * FOCAL / 10 + 30);
    const g = this.group; g.visible = true; g.position.set(o.x || 0, o.y || 0, o.z || 0); g.rotation.set(o.rx || 0, o.ry || 0, o.rz || 0);
  }
  hide() { this.group.visible = false; }
}
const screens = [new Screen(), new Screen(), new Screen()];

/* ---------------- 2D helpers ---------------- */
function font(ctx, fam, size, weight = 400, italic = false) { ctx.font = `${italic ? 'italic ' : ''}${weight} ${size}px ${fam}`; }
function text(ctx, s, x, y, o = {}) {
  ctx.save(); font(ctx, o.fam || SANS, o.size || 32, o.w || 400, o.italic); ctx.fillStyle = o.color || C.bone; ctx.globalAlpha = clamp(o.a ?? 1);
  ctx.textAlign = o.align || 'center'; ctx.textBaseline = o.base || 'alphabetic'; ctx.letterSpacing = (o.ls || 0) + 'px';
  if (o.glow) { ctx.shadowColor = o.glow; ctx.shadowBlur = o.blur || 30; }
  ctx.fillText(s, x, y); ctx.restore();
}
function label(ctx, s, x, y, o = {}) { text(ctx, s.toUpperCase(), x, y, { fam: MONO, size: o.size || 19, w: 500, ls: 3.2, color: o.color || C.dim, a: o.a, align: o.align || 'center' }); }
function chip(ctx, s, x, y, o = {}) {   // editorial tag: colour bar + spaced mono caps, no box
  const a = clamp(o.a ?? 1); if (a <= 0) return;
  ctx.save(); font(ctx, MONO, o.size || 20, 600); ctx.letterSpacing = '3.5px';
  const str = s.toUpperCase(), tw = ctx.measureText(str).width, w = tw + 22;
  const x0 = (o.align === 'left') ? x : x - w / 2;
  ctx.globalAlpha = a; ctx.fillStyle = o.color || C.bone; ctx.fillRect(x0, y - (o.size || 20) * 0.42, 4, (o.size || 20) * 0.84);
  ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(str, x0 + 18, y + 1);
  if (o.strike) { ctx.strokeStyle = o.color || C.bone; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x0 + 14, y); ctx.lineTo(x0 + 14 + (tw + 8) * clamp(o.strike), y); ctx.stroke(); }
  ctx.restore(); return w;
}
// headline revealed word by word across [t0,t1]; returns nothing. o: size, fam, w, color, x, y, maxW, hl (map of word->color), out (fade-out time)
function headline(ctx, t, s, t0, t1, o = {}) {
  const fade = o.out ? 1 - ease(ramp(t, o.out, o.out + 0.6)) : 1; if (t < t0 || fade <= 0) return;
  const size = o.size || 64; font(ctx, o.fam || SERIF, size, o.w || 600, o.italic); ctx.letterSpacing = (o.ls ?? -0.5) + 'px';
  const words = s.split(' '), maxW = o.maxW || 1500, lh = size * (o.lh || 1.18);
  const lines = []; let cur = [], cw = 0; const sp = ctx.measureText(' ').width;
  for (const w of words) { const ww = ctx.measureText(w).width; if (cw + ww > maxW && cur.length) { lines.push(cur); cur = []; cw = 0; } cur.push([w, ww]); cw += ww + sp; }
  lines.push(cur);
  const total = s.length; let ci = 0;
  const y0 = (o.y || 540) - (lines.length - 1) * lh / 2;
  lines.forEach((ln, li) => {
    const lw = ln.reduce((a, [, ww]) => a + ww, 0) + sp * (ln.length - 1);
    let x = (o.align === 'left') ? o.x : (o.x ?? W / 2) - lw / 2;
    for (const [w, ww] of ln) {
      const wt = t0 + (t1 - t0) * (ci / total) * (o.speed || 1);
      const k = eout(ramp(t, wt - 0.05, wt + 0.3));
      const col = (o.hl && o.hl[w.replace(/[.,?:]/g, '')]) || o.color || C.bone;
      ctx.save(); ctx.globalAlpha = k * fade * (o.a ?? 1); ctx.fillStyle = col; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
      font(ctx, o.fam || SERIF, size, o.w || 600, o.italics && o.italics.includes(w.replace(/[.,?]/g, ''))); ctx.letterSpacing = (o.ls ?? -0.5) + 'px';
      ctx.fillText(w, x, y0 + li * lh + (1 - k) * 14); ctx.restore();
      x += ww + sp; ci += w.length + 1;
    }
  });
}
function leader(ctx, x0, y0, x1, y1, a, color = C.dim) { if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = color; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); ctx.beginPath(); ctx.arc(x0, y0, 3, 0, 7); ctx.fillStyle = color; ctx.fill(); ctx.restore(); }

/* dish drawn in perspective from projected 3D rim circles */
function ring(cx, y, cz, r, n = 72) { const pts = []; for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; pts.push(toScreen(cx + Math.cos(a) * r, y, cz + Math.sin(a) * r * 0.9)); } return pts; }
function poly(ctx, pts) { ctx.beginPath(); pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); }
function dish(ctx, o) {
  const { cx = 0, floorY = -1.1, r = 2.5, h = 0.38, a = 1, liquid = 0, tint = [180, 200, 215], tintA = 0.08, glow = 0 } = o; if (a <= 0) return;
  const bot = ring(cx, floorY, 0, r), top = ring(cx, floorY + h, 0, r), liq = ring(cx, floorY + h * 0.72, 0, r * 0.995);
  ctx.save(); ctx.globalAlpha = a;
  // floor
  poly(ctx, bot); ctx.fillStyle = 'rgba(243,236,221,0.035)'; ctx.fill();
  // liquid volume
  if (liquid > 0) {
    ctx.save(); ctx.globalAlpha = a * liquid;
    const grad = ctx.createLinearGradient(0, Math.min(...liq.map(p => p[1])), 0, Math.max(...bot.map(p => p[1])));
    grad.addColorStop(0, `rgba(${tint},${tintA * 1.6})`); grad.addColorStop(1, `rgba(${tint},${tintA * 0.7})`);
    ctx.beginPath(); liq.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); ctx.fillStyle = grad; ctx.fill();
    // front wall of liquid
    const n = bot.length, half = [];
    for (let i = 0; i <= n / 2; i++) half.push(liq[i]); for (let i = n / 2; i >= 0; i--) half.push(bot[i]);
    poly(ctx, half); ctx.fillStyle = `rgba(${tint},${tintA})`; ctx.fill();
    poly(ctx, liq); ctx.strokeStyle = `rgba(${tint},${0.35 + glow * 0.5})`; ctx.lineWidth = 1.2 + glow * 2; ctx.stroke();
    ctx.restore();
  }
  // glass walls
  ctx.strokeStyle = `rgba(243,236,221,${0.32 + glow * 0.3})`; ctx.lineWidth = 1.6;
  poly(ctx, top); ctx.stroke(); poly(ctx, bot); ctx.globalAlpha = a * 0.6; ctx.stroke(); ctx.globalAlpha = a;
  const li = top.reduce((b, p, i) => p[0] < top[b][0] ? i : b, 0), ri = top.reduce((b, p, i) => p[0] > top[b][0] ? i : b, 0);
  ctx.beginPath(); ctx.moveTo(...top[li]); ctx.lineTo(...bot[li]); ctx.moveTo(...top[ri]); ctx.lineTo(...bot[ri]); ctx.stroke();
  // glass highlight
  ctx.globalAlpha = a * 0.5; ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 3;
  ctx.beginPath(); top.slice(Math.floor(top.length * 0.58), Math.floor(top.length * 0.7)).forEach(([x, y], i) => i ? ctx.lineTo(x, y - 2) : ctx.moveTo(x, y - 2)); ctx.stroke();
  ctx.restore();
}
/* cholesterol: four fused rings, drawn as a skeletal glyph */
function cholesterol(ctx, x, y, s, a, color = C.amber) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = color; ctx.lineWidth = Math.max(1.4, s * 0.11); ctx.lineJoin = 'round';
  const hex = (cx, cy) => { ctx.beginPath(); for (let i = 0; i < 6; i++) { const ang = Math.PI / 6 + i * Math.PI / 3; const px = cx + Math.cos(ang) * s, py = cy + Math.sin(ang) * s; i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.closePath(); ctx.stroke(); };
  const dx = Math.sqrt(3) * s;
  hex(x, y); hex(x + dx, y); hex(x + dx * 1.5, y - 1.5 * s);
  ctx.beginPath(); const px = x + dx * 2.5, py = y - 1.5 * s; for (let i = 0; i < 5; i++) { const ang = Math.PI + i * 2 * Math.PI / 5; const qx = px + Math.cos(ang) * s * 0.92, qy = py + Math.sin(ang) * s * 0.92; i ? ctx.lineTo(qx, qy) : ctx.moveTo(qx, qy); } ctx.closePath(); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(px + s * 0.85, py - s * 0.3); ctx.lineTo(px + s * 1.7, py - s * 0.9); ctx.lineTo(px + s * 2.6, py - s * 0.4); ctx.lineTo(px + s * 3.4, py - s * 1.0); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x - dx / 2, y + s / 2); ctx.lineTo(x - dx, y + s * 1.0); ctx.stroke();
  text(ctx, 'HO', x - dx * 1.25, y + s * 1.55, { fam: MONO, size: s * 0.9, color, a, w: 500 });
  ctx.restore();
}

/* captions: no box, soft shadow over a gentle bottom gradient */
const NOCAP = new Set(['n387', 'n85', 'title', 'url']);
const CAPS = [];
L.forEach(l => {
  if (NOCAP.has(l.id)) return;
  const words = l.show.split(' '); const chunks = []; let cur = '';
  for (const w of words) { if ((cur + ' ' + w).trim().length > 54 && cur) { chunks.push(cur); cur = w; } else cur = (cur + ' ' + w).trim(); }
  if (cur) chunks.push(cur);
  const total = chunks.reduce((a, c) => a + c.length, 0); let acc = 0;
  chunks.forEach((c, k) => { const t0 = l.start + (l.end - l.start) * acc / total; acc += c.length; const t1 = l.start + (l.end - l.start) * acc / total; CAPS.push({ s: c, t0, t1: k === chunks.length - 1 ? t1 + 0.35 : t1 }); });
});
function captions(ctx, t, a = 1) {
  const c = CAPS.find(c => t >= c.t0 && t < c.t1); if (!c || a <= 0) return;
  const k = Math.min(eout(ramp(t, c.t0, c.t0 + 0.14)), 1 - ramp(t, c.t1 - 0.1, c.t1));
  const g = ctx.createLinearGradient(0, H - 190, 0, H); g.addColorStop(0, 'rgba(6,5,4,0)'); g.addColorStop(1, 'rgba(6,5,4,0.62)');
  ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = g; ctx.fillRect(0, H - 190, W, 190); ctx.restore();
  ctx.save(); font(ctx, SANS, 32, 500); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.globalAlpha = k * a; ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 2;
  ctx.fillStyle = C.bone; ctx.fillText(c.s, W / 2, 1010); ctx.restore();
}
/* dark band behind headings when they sit over busy imagery */
function scrim(ctx, a, h = 300) { if (a <= 0) return; const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, `rgba(8,6,5,${0.94 * a})`); g.addColorStop(0.6, `rgba(8,6,5,${0.75 * a})`); g.addColorStop(1, 'rgba(8,6,5,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, h); }

/* film grain + vignette */
const GRAIN = [];
for (let s = 0; s < 6; s++) { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); const im = g.createImageData(256, 256); const R = rng(500 + s);
  for (let i = 0; i < im.data.length; i += 4) { const v = R() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; } g.putImageData(im, 0, 0); GRAIN.push(c); }
function finish(ctx, t) {
  const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05);
  vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.55)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.globalAlpha = 0.045; ctx.globalCompositeOperation = 'overlay';
  ctx.fillStyle = ctx.createPattern(GRAIN[Math.floor(t * 24) % 6], 'repeat'); ctx.fillRect(0, 0, W, H); ctx.restore();
}
function hair(ctx, x0, y0, x1, y1, a, color = 'rgba(243,236,221,0.28)', w = 1.2) { if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = color; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); ctx.restore(); }

/* ================= SCENES ================= */
function sceneIntro(t) {   // 1: why it matters
  const end1 = SEC1(1); if (t > end1 + 1.6) return;
  const out = 1 - ease(ramp(t, end1 + 0.1, end1 + 1.3));
  headline(over, t, 'Most cancer drugs fail before they reach a patient.', S('fail'), E('fail') - 0.6, { size: 78, y: 520, out: E('fail') + 0.5 });
  headline(over, t, 'Part of the problem is the testing.', S('testing'), E('testing') - 0.4, { size: 56, y: 200, color: C.dim, w: 500, out: S('notflat') - 0.3 });
  const dishA = win(t, S('flat') - 0.3, NF + 3.6, 1.2, 1.4) * out;
  dish(under, { cx: 0, floorY: -1.25, r: 2.6, a: dishA, liquid: 0 });
  if (dishA > 0.01) label(over, 'a plastic dish', W / 2, 905, { a: dishA * win(t, S('flat') + 1.2, NF + 0.2) });
  if (t > S('flat') - 0.3) {
    const grow = ramp(t, S('flat'), S('flat') + 2.8), m = ease(ramp(t, NF, NF + 2.9));
    drawCells(cloudA, LA, t, { floorY: -1.25, discR: 2.35, sphY: 0.05, sphR: 1.25, m, grow, size: lerp(0.15, 0.2, m), alpha: out, spin: 0.10 });
  }
  headline(over, t, 'Real tumours aren’t flat.', S('notflat'), E('notflat') - 0.2, { size: 60, y: 175, out: S('organoids') - 0.3 });
  const lab = win(t, S('organoids') + 3.6, end1 + 1.0, 0.8, 0.8);
  if (lab > 0) { const [sx, sy] = toScreen(1.25, 0.05, 0); leader(over, sx + 18, sy, sx + 150, sy - 70, lab, C.dim);
    text(over, 'organoid', sx + 165, sy - 78, { fam: SERIF, size: 46, w: 600, align: 'left', a: lab, italic: true });
    label(over, 'tiny 3D copy of a patient’s tumour', sx + 166, sy - 38, { a: lab, align: 'left', size: 17 }); }
  headline(over, t, 'Grown from a patient’s own tumour, in 3D.', S('organoids') + 0.2, S('organoids') + 3.4, { size: 54, y: 175, w: 500, out: end1 + 0.8 });
}

function sceneStudies(t) {  // 2
  const a0 = SEC0(2) - 0.6, a1 = SEC1(2) + 1.0; if (t < a0 || t > a1 + 0.5) return;
  const a = win(t, a0, a1, 0.8, 0.9);
  [['Broad Institute', 'Nature, 2026'], ['Wellcome Sanger Institute', 'Nature, 2026']].forEach(([n, j], k) => {
    const ca = a * eout(ramp(t, S('studies') + 0.1 + k * 0.35, S('studies') + 0.9 + k * 0.35)); if (ca <= 0) return;
    const x = W / 2 + (k ? 1 : -1) * 360, y = 205 + (1 - ca) * 16;
    text(over, n, x, y, { fam: SERIF, size: 44, w: 600, a: ca });
    hair(over, x - 60, y + 26, x + 60, y + 26, ca * 0.8, 'rgba(255,75,46,0.8)', 1.5);
    label(over, j, x, y + 60, { a: ca, size: 17 });
  });
  hair(over, W / 2, 160, W / 2, 280, a * ramp(t, S('studies') + 0.6, S('studies') + 1.2) * 0.5);
  const cols = 64, rows = 15, sx = 27, x0 = W / 2 - (cols - 1) * sx / 2, y0 = 430;
  const R = rng(5); const ga = a * eout(ramp(t, S('studies') + 2.0, S('studies') + 3.2));
  const sweep0 = S('studies') + 3.6, sweep1 = E('studies') + 0.3;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const k = r * cols + c, hit = R() < 0.085, rr = R();
    const tk = lerp(sweep0, sweep1, k / (cols * rows)), off = ramp(t, tk, tk + 0.25);
    let col = C.bone, al = 0.55 * (1 - off * 0.75), rad = 4.2;
    if (hit && off > 0) { col = C.red; al = 0.95; rad = 4.2 + 3 * Math.exp(-Math.max(0, t - tk) * 3); }
    const x = x0 + c * sx, y = y0 + r * sx;
    over.globalAlpha = ga * al; over.fillStyle = col; over.beginPath(); over.arc(x, y, rad, 0, 7); over.fill();
    const tgt = ramp(t, S('hundreds') + 3.4 + rr * 1.2, S('hundreds') + 4.2 + rr * 1.2);
    if (hit && tgt > 0) { over.globalAlpha = ga * tgt; over.strokeStyle = C.red; over.lineWidth = 1.5; over.beginPath(); over.arc(x, y, 9 + (1 - tgt) * 10, 0, 7); over.stroke(); }
  }
  over.globalAlpha = 1;
  label(over, 'every gene, switched off one at a time', W / 2, 850, { a: ga * win(t, S('studies') + 3.0, S('hundreds') - 0.2) });
  label(over, 'hundreds matter more in organoids', W / 2, 850, { a: a * win(t, S('hundreds') + 0.2, S('hundreds') + 3.6), color: C.red });
  label(over, '→ proposed as new drug targets', W / 2, 850, { a: a * ramp(t, S('hundreds') + 3.8, S('hundreds') + 4.4), color: C.red });
}

function dishLayout(t) { const k = ease(ramp(t, S('existed') + 0.2, S('existed') + 2.0)); return { left: lerp(-2.6, -3.35, k), right: lerp(2.6, 3.35, k), mid: k }; }
function sceneCatch(t) {   // 3 + 4
  const a0 = SEC0(3) - 0.4, a1 = SEC1(4) + 0.6;
  if (t < a0 || t > a1 + 1.2) { cloudB.hide(); cloudC.hide(); return; }
  const all = win(t, S('two') - 0.2, a1 + 1.0, 1.0, 1.0);
  headline(over, t, 'Here’s the catch.', S('catch'), E('catch'), { size: 84, y: 520, out: S('two') - 0.4 });
  const D = dishLayout(t), R = 1.38, floorY = -0.62;
  const liq = ramp(t, S('medium'), S('medium') + 1.0), serum = ramp(t, SER, SER + 1.2), clean = ramp(t, S('clean'), S('clean') + 1.2);
  const foodGlow = win(t, S('diet'), E('diet') + 1.2, 0.3, 0.6) + win(t, S('food'), S('food') + 2.2, 0.3, 0.6) * 0.6;
  const leftTint = [Math.round(lerp(190, 205, serum)), Math.round(lerp(205, 60, serum)), Math.round(lerp(220, 40, serum))];
  dish(under, { cx: D.left, floorY, r: R, a: all, liquid: liq, tint: leftTint, tintA: lerp(0.07, 0.2, serum), glow: foodGlow });
  dish(under, { cx: D.right, floorY, r: R, a: all, liquid: liq, tint: [190, 210, 225], tintA: 0.07, glow: foodGlow });
  const midA = all * eout(ramp(t, S('database'), S('database') + 1.2));
  if (midA > 0) dish(under, { cx: 0, floorY, r: R, a: midA, liquid: 1, tint: [190, 210, 225], tintA: 0.07, glow: win(t, S('samediet'), E('foodcan') + 1.5, 0.3, 0.8) });
  const shapeGlow = win(t, S('shape'), S('shape') + 3.0, 0.3, 0.8) + win(t, S('theshape'), E('theshape') + 0.6, 0.3, 0.6);
  drawCells(cloudB, LB, t, { cx: D.left, floorY, discR: R * 0.9, m: 0, grow: ramp(t, S('two'), S('two') + 1.6), size: 0.13, alpha: all });
  drawCells(cloudA, LA, t, { cx: D.right, floorY, discR: R * 0.9, sphY: floorY + 0.88, sphR: 0.76, m: 1, grow: 1, size: 0.13, alpha: all, spin: 0.12, glow: shapeGlow });
  if (midA > 0) drawCells(cloudC, LB, t, { cx: 0, floorY, discR: R * 0.9, m: 0, grow: ramp(t, S('database') + 0.3, S('database') + 1.8), size: 0.13, alpha: midA }); else cloudC.hide();
  if (serum > 0) for (let i = 0; i < 6; i++) { const ph = i * 1.7; const [x, y] = toScreen(D.left + Math.cos(ph + t * 0.25) * R * 0.6, floorY + 0.12 + 0.04 * Math.sin(t + i), Math.sin(ph + t * 0.25) * R * 0.5);
    cholesterol(under, x - 30, y - 6, 7, all * serum * 0.75, C.amber); }
  const [lx] = toScreen(D.left, floorY, 0), [rx] = toScreen(D.right, floorY, 0), [mx] = toScreen(0, floorY, 0);
  const subA = all * win(t, S('two') + 0.8, a1 + 1.0, 0.6, 1.0);
  label(over, 'classic flat culture', lx, 800, { a: subA * (1 - ramp(t, SER - 0.4, SER)) });
  label(over, 'organoid', rx, 800, { a: subA * (1 - ramp(t, S('clean') - 0.4, S('clean'))) });
  text(over, 'serum', lx, 800, { fam: SERIF, size: 40, w: 600, color: '#ff8a70', a: all * serum, italic: true });
  label(over, 'nutrient-rich · from blood', lx, 838, { a: all * serum, size: 17 });
  text(over, 'lab-made medium', rx, 800, { fam: SERIF, size: 40, w: 600, color: C.blue, a: all * clean, italic: true });
  label(over, 'almost no cholesterol', rx, 838, { a: all * clean, size: 17 });
  label(over, 'flat cells · organoid medium', mx, 800, { a: midA * ramp(t, S('database') + 1.2, S('database') + 1.8) });
  label(over, 'public data', mx, 836, { a: midA * ramp(t, S('database') + 1.6, S('database') + 2.2), size: 16, color: C.mute });
  const sh = all * win(t, S('shape'), S('existed') + 0.4, 0.4, 0.6), fd = all * win(t, S('food'), S('existed') + 0.4, 0.4, 0.6);
  chip(over, '1  shape', W / 2 - 150, 175, { a: sh, color: C.blue });
  chip(over, '2  food', W / 2 + 150, 175, { a: fd, color: '#ff8a70' });
  label(over, 'flat', lx, 330, { a: all * win(t, S('shape') + 1.4, S('food'), 0.4, 0.5), color: C.blue });
  label(over, '3D', rx, 330, { a: all * win(t, S('shape') + 1.4, S('food'), 0.4, 0.5), color: C.blue });
  const medA = all * win(t, S('medium') + 0.6, SER + 0.2, 0.5, 0.4);
  if (medA > 0) { const [px, py] = toScreen(D.right - R * 0.7, floorY + 0.28, R * 0.4); leader(over, px, py, px - 90, py - 150, medA, C.blue);
    text(over, 'the medium', px - 100, py - 160, { fam: SERIF, size: 40, w: 600, italic: true, align: 'right', a: medA, color: C.blue }); }
  headline(over, t, 'Which change caused it?', S('which') + 0.3, E('which') - 0.6, { size: 62, y: 290, out: S('existed') - 0.3 });
  headline(over, t, 'The data to tell them apart already existed.', S('existed'), E('existed') - 0.3, { size: 54, y: 175, w: 500, out: S('samediet') - 0.5 });
  const sd = midA * win(t, S('samediet'), a1 + 0.8, 0.4, 0.8);
  chip(over, 'same food', mx - 120, 300, { a: sd, color: '#ff8a70' });
  chip(over, 'no 3D', mx + 110, 300, { a: sd, color: C.blue, strike: ramp(t, S('samediet') + 1.2, S('samediet') + 1.7) });
  const arr = midA * win(t, S('foodcan'), a1 + 0.8, 0.5, 0.8);
  if (arr > 0) { const ax0 = mx + 150, ax1 = rx - 150, ay = 470; over.save(); over.globalAlpha = arr; over.strokeStyle = '#ff8a70'; over.lineWidth = 2; over.setLineDash([8, 8]);
    over.beginPath(); over.moveTo(ax0, ay); over.lineTo(lerp(ax0, ax1, eout(ramp(t, S('foodcan'), S('foodcan') + 1.2))), ay); over.stroke(); over.restore();
    label(over, 'same change?', (ax0 + ax1) / 2, ay - 22, { a: arr, color: '#ff8a70', size: 16 }); }
  headline(over, t, 'Then the shape can’t explain it. The food can.', S('foodcan') + 2.6, E('foodcan'), { size: 54, y: 175, w: 500, hl: { food: C.red, can: C.red }, out: a1 + 0.6 });
}

/* gene field: section 5 (sweep and reveal) and section 7 (the chart explained) */
const CHOL = ['SQLE', 'MSMO1', 'MVD', 'IDI1'], LEAD = ['SCAP', 'DDX3X', 'ITGB1'];
function sceneField(t) {
  const in0 = SEC1(4) + 0.5, chart0 = S('chart') - 1.2, end7 = SEC1(7) + 0.8;
  const inSec5 = t > in0 && t < WHY + 0.8, inSec7 = t > chart0 && t < end7 + 1.5;
  if (!inSec5 && !inSec7) { field.hide(); return; }
  const sweep0 = SWEEP, reveal = t >= S('n85') - 0.02 && t < WHY + 0.9;
  const fin = inSec5 ? ramp(t, in0 + 0.2, in0 + 2.4) : ramp(t, chart0, chart0 + 1.2);
  const fout = inSec7 ? 1 - ease(ramp(t, end7, end7 + 1.2)) : 1;
  const hitsOn = ramp(t, S('g456'), S('g456') + 1.2);
  const landed = inSec7 ? 1 : 0;
  const mostPulse = win(t, S('most'), E('most') + 0.6, 0.3, 0.6);
  const leftOnly = ramp(t, S('left'), S('left') + 1.0);
  for (let i = 0; i < NG; i++) {
    const g = GENES[i], hit = g.f > 0, gp = gridPos[i];
    const ap = inSec5 ? ramp(t, in0 + 0.4 + (Math.abs(gp[0]) / 5.4) * 1.8, in0 + 1.2 + (Math.abs(gp[0]) / 5.4) * 1.8) : 1;
    let x = gp[0], y = gp[1], z = gp[2], a = 0.5 * ap, s = 0.034, col = RGB.bone;
    if (hit) {
      a = lerp(0.5, 1, hitsOn) * ap; s = lerp(0.034, 0.06, hitsOn);
      const lk = landed || ease(ramp(t, sweep0 + landT.get(i), sweep0 + landT.get(i) + 1.1));
      const [px, py] = plotXY(g.D, g.A);
      x = lerp(x, px, lk); y = lerp(y, py, lk); z = lerp(z, 0, lk); s = lerp(s, 0.075, lk);
      const cc = colOf(g.f); col = [lerp(RGB.bone[0], cc[0], lk), lerp(RGB.bone[1], cc[1], lk), lerp(RGB.bone[2], cc[2], lk)];
      if (g.f === 1) { a *= lerp(1, 0.16, leftOnly); s *= 1 + mostPulse * 0.35; }
      if (CHOL.includes(g.g)) s *= 1 + win(t, S('chol') + 0.4, S('left'), 0.5, 0.8) * 0.9;
      if (g.f === 3) s *= 1 + ramp(t, S('one'), S('one') + 0.6) * 0.8;
      if (LEAD.includes(g.g)) s *= 1 + ramp(t, S('three') + 0.8, S('three') + 1.4) * 0.8;
    } else {
      a *= inSec7 ? 0 : lerp(1, 0.13, hitsOn) * (1 - ease(ramp(t, sweep0 - 0.4, sweep0 + 1.2)) * 0.85);
    }
    field.set(i, x, y, z, col[0], col[1], col[2], reveal ? 0 : a * fin * fout, s);
  }
  field.commit();
  if (reveal) return;
  const plotA = (inSec7 ? fin : ease(ramp(t, sweep0 - 0.3, sweep0 + 0.9))) * fout;
  if (plotA > 0) {
    const [ox, oy] = toScreen(PLOT.cx, PLOT.cy, 0), [ax, ay] = toScreen(PLOT.cx + 1.25 * PLOT.k, PLOT.cy, 0), [bx, by] = toScreen(PLOT.cx, PLOT.cy + 1.1 * PLOT.k, 0);
    const [l0x, l0y] = toScreen(...plotXY(-1.2, -1.2), 0), [l1x, l1y] = toScreen(...plotXY(1.05, 1.05), 0);
    const [nx] = toScreen(PLOT.cx - 1.25 * PLOT.k, 0, 0), [, ny] = toScreen(0, PLOT.cy - 1.2 * PLOT.k, 0);
    hair(over, nx, oy, ax, ay, plotA * 0.5, C.dim); hair(over, ox, ny, bx, by, plotA * 0.5, C.dim);
    const lineGlow = inSec7 ? win(t, S('line'), E('most') + 0.8, 0.4, 0.8) : 0;
    const dk = inSec7 ? 1 : eout(ramp(t, sweep0, sweep0 + 1.4));
    over.save(); over.globalAlpha = plotA * (0.8 + 0.2 * lineGlow); over.setLineDash([10, 9]); over.strokeStyle = C.red; over.lineWidth = 1.8 + lineGlow * 1.6;
    if (lineGlow > 0) { over.shadowColor = C.red; over.shadowBlur = 18 * lineGlow; }
    over.beginPath(); over.moveTo(l0x, l0y); over.lineTo(lerp(l0x, l1x, dk), lerp(l0y, l1y, dk)); over.stroke(); over.restore();
    const axA = plotA * (inSec7 ? win(t, chart0, S('chol') - 0.2, 0.6, 0.6) : 1);
    label(over, '← organoids need it more', nx + 6, oy + 34, { a: axA, align: 'left', size: 15 });
    label(over, 'organoids need it less →', ax - 6, oy + 34, { a: axA, align: 'right', size: 15 });
    over.save(); over.translate(ox - 22, ny + 10); over.rotate(-Math.PI / 2); label(over, 'flat cells on organoid food →', 0, 0, { a: axA, align: 'left', size: 15 }); over.restore();
    label(over, 'same change either way', l1x - 6, l1y - 18, { a: plotA * (inSec7 ? 1 : ramp(t, sweep0 + 1.2, sweep0 + 1.8)), color: '#ff8a70', align: 'right', size: 16 });
  }
  if (inSec5) {
    const cnt = fin;
    scrim(over, ramp(t, S('howmany'), S('howmany') + 0.5) * (1 - ramp(t, sweep0 - 0.2, sweep0 + 0.3)), 300);
    if (t < sweep0 + 0.2) {
      const n = Math.round(17525 * eout(ramp(t, S('ran') + 0.4, S('ran') + 3.0)));
      const c1 = cnt * ramp(t, S('ran'), S('ran') + 0.4) * (1 - ramp(t, S('g456') - 0.3, S('g456')));
      text(over, n.toLocaleString('en-US'), W / 2, 150, { fam: MONO, size: 52, w: 500, a: c1 });
      label(over, 'genes, every one measured', W / 2, 196, { a: c1, size: 17 });
      if (RAN_MUSE) { const ma = c1 * ramp(t, S('ran') + 0.2, S('ran') + 0.8); over.save(); over.globalAlpha = ma; over.fillStyle = 'rgba(8,6,5,0.88)'; over.fillRect(0, 228, W, 68); over.restore(); }
      if (RAN_MUSE) chip(over, 'research loop run by Muse  ·  Meta’s AI model', W / 2, 262, { a: c1 * ramp(t, S('ran') + 0.2, S('ran') + 0.8), color: C.amber, size: 19 });
      const c2 = cnt * ramp(t, S('g456'), S('g456') + 0.4) * (1 - ramp(t, S('howmany') - 0.2, S('howmany') + 0.2));
      text(over, '456', W / 2, 150, { fam: MONO, size: 52, w: 500, a: c2 });
      label(over, 'behave differently in organoids', W / 2, 196, { a: c2, size: 17 });
    }
    headline(over, t, 'How many also change with only the food?', S('howmany') + 0.2, E('howmany') - 1.0, { size: 58, y: 150, w: 500, out: sweep0 - 0.2 });
    if (t >= sweep0) {
      const n = Math.round(387 * eout(ramp(t, sweep0 + 0.1, S('n387') - 0.05)));
      text(over, String(n), 150, 190, { fam: SERIF, size: 120, w: 700, align: 'left', color: C.red, a: ramp(t, sweep0, sweep0 + 0.3) });
      label(over, 'of 456 follow the food', 156, 238, { a: ramp(t, sweep0 + 0.3, sweep0 + 0.8), align: 'left', size: 18, color: '#ff8a70' });
    }
  }
  if (inSec7) {
    const fa = fout;
    scrim(over, fa * fin, 260);
    headline(over, t, 'Each dot is one of the 456 genes.', S('chart'), E('chart') - 0.3, { size: 50, y: 130, w: 500, out: S('line') + 0.2 });
    headline(over, t, 'On the dashed line: same change either way.', S('line') + 0.2, E('line') - 1.0, { size: 50, y: 130, w: 500, hl: { dashed: C.red, line: C.red }, out: S('chol') - 0.4 });
    const ca = win(t, S('chol') + 0.4, S('left') + 0.2, 0.5, 0.6) * fa;
    const offs = { SQLE: [-150, 40], MSMO1: [-170, -10], MVD: [-150, -60], IDI1: [-120, -110] };
    for (const s of CHOL) { const g = BYG.get(s); const [px, py] = plotXY(g.D, g.A); const [sx, sy] = toScreen(px, py, 0); const off = offs[s];
      leader(over, sx, sy, sx + off[0] + 70, sy + off[1], ca, '#ff8a70'); text(over, s, sx + off[0] + 62, sy + off[1] + 7, { fam: MONO, size: 22, w: 600, align: 'right', color: '#ffb3a3', a: ca }); }
    const molA = win(t, S('chol') + 0.2, E('make') + 0.2, 0.6, 1.0) * fa;
    cholesterol(over, 1330, 330, 26, molA * (1 - 0.7 * ramp(t, S('make') + 0.5, S('make') + 2.0)), C.amber);
    label(over, 'cholesterol', 1430, 410, { a: molA, color: C.amber, size: 18 });
    label(over, 'almost none in organoid food', 1430, 442, { a: molA * ramp(t, S('make'), S('make') + 0.6), size: 15 });
    label(over, '→ cells must build their own', 1430, 470, { a: molA * ramp(t, S('make') + 2.0, S('make') + 2.6), size: 15, color: '#ff8a70' });
    headline(over, t, 'The clearest case: cholesterol.', S('chol'), E('chol'), { size: 50, y: 130, w: 500, out: S('left') - 0.4 });
    headline(over, t, 'The genes that don’t clearly follow the food.', S('left'), E('left') - 0.4, { size: 50, y: 130, w: 500, color: C.amber, out: S('three') - 0.4 });
    chip(over, '68  the data can’t tell', 1360, 560, { a: fa * ramp(t, S('g68'), S('g68') + 0.5), color: C.amber, align: 'left' });
    const lsm = BYG.get('LSM7'); { const [px, py] = plotXY(lsm.D, lsm.A); const [sx, sy] = toScreen(px, py, 0); const la = fa * win(t, S('one'), end7 + 1, 0.5, 0.5);
      leader(over, sx, sy, sx + 90, sy + 150, la, C.blue); label(over, 'LSM7 · leans to shape · not solid', sx + 98, sy + 160, { a: la, align: 'left', color: C.blue, size: 16 }); }
    const la = fa * ramp(t, S('three') + 0.8, S('three') + 1.4);
    const spots = { SCAP: [560, 470], DDX3X: [560, 530], ITGB1: [560, 590] };
    for (const s of LEAD) { const g = BYG.get(s); const [px, py] = plotXY(g.D, g.A); const [sx, sy] = toScreen(px, py, 0); const [lx, ly] = spots[s];
      leader(over, sx, sy, lx + 10, ly - 7, la, C.amber); text(over, s, lx, ly, { fam: MONO, size: 24, w: 600, align: 'right', color: C.amber, a: la });
      const pr = ramp(t, S('leads'), S('leads') + 1.4); if (pr > 0 && pr < 1) { over.save(); over.globalAlpha = (1 - pr) * fa; over.strokeStyle = C.amber; over.lineWidth = 2; over.beginPath(); over.arc(sx, sy, 10 + pr * 40, 0, 7); over.stroke(); over.restore(); } }
    label(over, 'Sanger’s top picks', 470, 420, { a: la, color: C.amber, size: 16 });
    headline(over, t, 'The more credible leads.', S('leads'), E('leads'), { size: 52, y: 130, w: 500, color: C.amber, out: end7 });
  }
}

/* the 85% card, then section 6: why it matters */
const SHORTLIST = ['SQLE', 'MSMO1', 'MVD', 'IDI1', 'FDFT1', 'MBTPS1', 'MBTPS2', 'NSDHL'];
function sceneWhy(t) {
  const r0 = S('n85'), w0 = WHY, end6 = SEC1(6) + 0.9;
  if (t < r0 - 0.02 || t > end6 + 1.2) return;
  const out6 = 1 - ease(ramp(t, end6, end6 + 1.0));
  over.save(); over.globalAlpha = (t < w0 + 0.9) ? 1 : 1 - ease(ramp(t, w0 + 0.9, w0 + 1.6)); over.fillStyle = '#060504'; over.fillRect(0, 0, W, H); over.restore();
  // 85%: punch, then shrink to an anchor at the top
  const k = t - r0, mv = ease(ramp(t, w0 + 0.3, w0 + 1.5));
  const sc = (1 + 0.07 * Math.exp(-k * 5)) * lerp(1, 0.36, mv);
  const anchorOut = 1 - ease(ramp(t, S('blood') - 0.8, S('blood') - 0.1));
  over.save(); over.translate(W / 2, lerp(560, 185, mv)); over.scale(sc, sc);
  text(over, '85%', 0, 120, { fam: SERIF, size: 400, w: 800, color: C.red, glow: 'rgba(255,75,46,0.35)', blur: 80, ls: -12, a: anchorOut * out6 });
  over.restore();
  const sub = ramp(k, 0.9, 1.6) * (1 - ramp(t, w0 + 0.2, w0 + 0.7));
  text(over, 'of the genes that changed also change with the food alone', W / 2, 800, { fam: SANS, size: 34, w: 500, color: C.dim, a: sub });
  text(over, '387 of 456', W / 2, 860, { fam: MONO, size: 22, w: 500, color: C.mute, a: sub * ramp(k, 1.2, 1.9), ls: 3 });
  if (t < w0) return;
  // the kind of genes being put forward as drug targets
  const ka = win(t, S('kind'), S('blood') - 0.3, 0.6, 0.6) * out6;
  SHORTLIST.forEach((g, i) => { const gx = W / 2 + (i - 3.5) * 185, gy = 400; const ga = ka * eout(ramp(t, S('kind') + 0.2 + i * 0.18, S('kind') + 0.7 + i * 0.18));
    text(over, g, gx, gy, { fam: MONO, size: 30, w: 600, color: '#ffb3a3', a: ga });
    over.save(); over.globalAlpha = ga * 0.8; over.strokeStyle = C.red; over.lineWidth = 1.4; over.beginPath(); over.arc(gx, gy + 34, 7, 0, 7); over.moveTo(gx - 13, gy + 34); over.lineTo(gx + 13, gy + 34); over.moveTo(gx, gy + 21); over.lineTo(gx, gy + 47); over.stroke(); over.restore(); });
  label(over, 'put forward as drug targets', W / 2, 482, { a: ka * ramp(t, S('kind') + 1.6, S('kind') + 2.2), color: '#ff8a70', size: 17 });
  // same change: organoid = flat cells on the same food
  const sa = win(t, SAME, S('blood') - 0.3, 0.8, 0.6) * out6;
  if (sa > 0) {
    dish(under, { cx: -2.3, floorY: -1.45, r: 1.25, a: sa, liquid: 1, tint: [190, 210, 225], tintA: 0.07 });
    dish(under, { cx: 2.3, floorY: -1.45, r: 1.25, a: sa, liquid: 1, tint: [190, 210, 225], tintA: 0.07 });
    drawCells(cloudA, LA, t, { cx: 2.3, sphY: -0.82, sphR: 0.66, m: 1, grow: 1, size: 0.115, alpha: sa, spin: 0.12 });
    drawCells(cloudC, LB, t, { cx: -2.3, floorY: -1.45, discR: 1.1, m: 0, grow: 1, size: 0.11, alpha: sa });
    text(over, '=', W / 2, 800, { fam: SERIF, size: 110, w: 500, color: C.red, a: sa * ramp(t, SAME + 1.6, SAME + 2.2) });
    label(over, 'organoid', toScreen(2.3, 0, 0)[0], 965, { a: sa, size: 16 });
    label(over, 'flat cells · same food', toScreen(-2.3, 0, 0)[0], 965, { a: sa, size: 16 });
    const ns = win(t, S('notshape'), S('blood') - 0.3, 0.5, 0.6) * out6;
    chip(over, '3D shape', W / 2 - 160, 560, { a: ns * 0.9, color: C.blue, strike: ramp(t, S('notshape') + 1.0, S('notshape') + 1.6) });
    chip(over, 'the food', W / 2 + 150, 560, { a: ns * ramp(t, S('notshape') + 2.6, S('notshape') + 3.2), color: '#ff8a70' });
  }
  // in a patient: a tumour fed by blood, full of cholesterol
  const ba = win(t, S('blood') - 0.2, end6, 0.9, 0.9);
  if (ba > 0) {
    const path = u => [lerp(-80, W + 80, u), 760 + Math.sin(u * Math.PI * 1.6 + 0.6) * 90];
    under.save(); under.globalAlpha = ba; under.lineCap = 'round';
    for (const [wdt, col] of [[118, 'rgba(120,18,10,0.55)'], [92, 'rgba(176,40,22,0.75)'], [40, 'rgba(255,90,60,0.18)']]) {
      under.strokeStyle = col; under.lineWidth = wdt; under.beginPath(); for (let i = 0; i <= 60; i++) { const [x, y] = path(i / 60); i ? under.lineTo(x, y) : under.moveTo(x, y); } under.stroke(); }
    under.restore();
    for (let i = 0; i < 9; i++) { const u = ((t * 0.045 + i / 9) % 1); const [x, y] = path(u); cholesterol(over, x - 30, y - 8 + Math.sin(i * 3) * 18, 7, ba * 0.9, C.amber); }
    drawCells(cloudA, LA, t, { cx: 0.2, sphY: 0.55, sphR: 0.78, m: 1, grow: 1, size: 0.13, alpha: ba, spin: 0.1 });
    label(over, 'in the body', 1460, 330, { a: ba * ramp(t, S('blood') + 0.4, S('blood') + 1.0), size: 18, color: C.dim });
    text(over, 'fed by blood, full of cholesterol', 1460, 372, { fam: SERIF, size: 36, w: 500, italic: true, color: '#ff8a70', a: ba * ramp(t, S('blood') + 1.4, S('blood') + 2.0) });
    headline(over, t, 'A weakness made by the lab diet may not exist in a patient.', S('maynot') + 0.6, E('maynot') - 0.4, { size: 50, y: 170, w: 500, maxW: 1400, hl: { patient: C.red } });
  }
}

function sceneTest(t) {   // 8: the test, and trying to break it
  const a0 = SEC0(8) - 0.8, a1 = SEC1(8) + 0.8; if (t < a0 || t > a1 + 1.0) return;
  const a = win(t, a0 + 0.2, a1 + 0.6, 0.6, 0.9);
  headline(over, t, 'A pattern in existing data, not proof.', S('proof'), E('proof') - 0.6, { size: 74, y: 520, out: S('check') + 0.2 });
  const dA = a * win(t, S('check') + 0.2, BRK + 0.2, 0.8, 0.8);
  if (dA > 0) {
    dish(under, { cx: 0, floorY: -1.25, r: 1.9, a: dA, liquid: 1, tint: [190, 210, 225], tintA: 0.08, glow: win(t, S('putback') + 2.2, S('putback') + 4.0, 0.2, 1.0) });
    drawCells(cloudA, LA, t, { cx: 0, sphY: -0.2, sphR: 0.85, m: 1, grow: 1, size: 0.14, alpha: dA, spin: 0.12 });
    const td = ramp(t, S('putback') + 0.6, S('putback') + 1.8); const [dx, dy0] = toScreen(0.0, 2.4, 0), [, dy1] = toScreen(0, -0.95, 0);
    if (td > 0 && td < 1) { const y = lerp(dy0, dy1, td * td); over.save(); over.globalAlpha = dA; over.fillStyle = C.amber; over.shadowColor = C.amber; over.shadowBlur = 20; over.beginPath(); over.ellipse(dx, y, 10, 14, 0, 0, 7); over.fill(); over.restore();
      cholesterol(over, dx + 30, y - 10, 7, dA * 0.9, C.amber); }
    const rp = ramp(t, S('putback') + 1.8, S('putback') + 3.2); if (rp > 0 && rp < 1) { const [rx, ry] = toScreen(0, -0.95, 0); over.save(); over.globalAlpha = dA * (1 - rp); over.strokeStyle = C.amber; over.lineWidth = 2; over.beginPath(); over.ellipse(rx, ry, 20 + rp * 160, (20 + rp * 160) * 0.22, 0, 0, 7); over.stroke(); over.restore(); }
    headline(over, t, 'Put the cholesterol back.', S('putback'), E('putback') - 0.2, { size: 60, y: 175, out: BRK - 0.3 });
    // two outcomes, set as type
    const o1 = dA * ramp(t, S('ifstop') + 0.2, S('ifstop') + 0.8), o2 = dA * ramp(t, S('ifstop') + 2.6, S('ifstop') + 3.2);
    text(over, 'Need goes away', 330, 520, { fam: SERIF, size: 40, w: 600, a: o1 }); hair(over, 250, 545, 410, 545, o1, 'rgba(255,75,46,0.8)', 1.5);
    text(over, 'it was the food', 330, 590, { fam: SERIF, size: 34, w: 500, italic: true, color: '#ff8a70', a: o1 });
    text(over, 'Need stays', W - 330, 520, { fam: SERIF, size: 40, w: 600, a: o2 }); hair(over, W - 410, 545, W - 250, 545, o2, 'rgba(237,169,60,0.8)', 1.5);
    text(over, 'a stronger candidate', W - 330, 590, { fam: SERIF, size: 34, w: 500, italic: true, color: C.amber, a: o2 });
    label(over, 'about two weeks · no new screen', W / 2, 905, { a: dA * ramp(t, S('twoweeks'), S('twoweeks') + 0.6), color: C.dim, size: 20 });
  } else if (t > S('break')) cloudA.hide();
  // trying to break it: three columns divided by hairlines, no boxes
  headline(over, t, 'We tried hard to prove ourselves wrong.', S('break'), E('break'), { size: 60, y: 250, out: a1 + 0.2 });
  const cols = [['Unseen', 'patient samples', 'held out from the analysis', 'unseen'], ['150', 'reruns', 'on reshuffled data', 'rerun'], ['5', 'rounds of review', 'code and claims, checked independently', 'reviews']];
  cols.forEach(([big, mid, small, id], k) => {
    const ca = a * eout(ramp(t, S(id) - 0.1, S(id) + 0.5)) * (1 - ramp(t, a1 - 0.2, a1 + 0.4)); if (ca <= 0) return;
    const x = W / 2 + (k - 1) * 500, y = 520 + (1 - ca) * 18;
    label(over, `0${k + 1}`, x, y - 110, { a: ca, color: C.amber, size: 16 });
    text(over, big, x, y, { fam: SERIF, size: 92, w: 700, a: ca, ls: -2 });
    text(over, mid, x, y + 56, { fam: SERIF, size: 34, w: 500, italic: true, color: C.dim, a: ca });
    label(over, small, x, y + 100, { a: ca, size: 14, color: C.mute });
    if (k > 0) hair(over, x - 250, y - 120, x - 250, y + 110, ca * 0.6);
  });
  const fa = a * eout(ramp(t, S('dropped'), S('dropped') + 0.6));
  if (fa > 0) { label(over, 'one early finding didn’t hold up', W / 2, 770, { a: fa, color: C.dim, size: 17 });
    text(over, 'the “spliceosome” effect', W / 2, 830, { fam: SERIF, size: 40, w: 500, italic: true, color: C.mute, a: fa });
    const st = ramp(t, S('dropped') + 1.4, S('dropped') + 2.0); hair(over, W / 2 - 200, 818, W / 2 - 200 + 400 * st, 818, fa * (st > 0 ? 1 : 0), C.red, 3);
    label(over, 'dropped', W / 2, 880, { a: fa * ramp(t, S('dropped') + 2.0, S('dropped') + 2.5), color: C.red, size: 16 }); }
}

/* 9: the product, Linear-style tilted screens */
function seqFrame(prefix, n, t, t0, t1) { const k = Math.floor(clamp((t - t0) / (t1 - t0)) * (n - 1)); return `${prefix}${String(k).padStart(2, '0')}`; }
const ASK_TYPE = Array.from({ length: 21 }, (_, i) => `ask_type_${String(i * 2).padStart(2, '0')}`);
function urlMark(ctx, a, y = 940, size = 40) { if (a <= 0) return; text(ctx, 'itsthemedium.com', W / 2, y, { fam: MONO, size, w: 500, ls: 2, a }); font(ctx, MONO, size, 500); ctx.letterSpacing = '2px'; const w = ctx.measureText('itsthemedium.com').width; hair(ctx, W / 2 - w / 2, y + 16, W / 2 + w / 2, y + 16, a, C.red, 2); }
async function sceneDemo(t) {
  screens.forEach(s => s.hide());
  const a0 = SEC0(9) - 0.5, a1 = SEC1(9) + (has('loop') ? 1.0 : 0.6); if (t < a0 || t > a1 + 0.6) return;
  const a = win(t, a0 + 0.2, a1 + 0.4, 0.9, 0.9);
  const drift = (t - a0) * 0.006;
  if (t < LOOK - 0.2) {
    const k = ease(ramp(t, a0, LOOK));
    await screens[0].show('hero', { w: 9.0, x: lerp(0.4, 0.0, k), y: lerp(0.1, 0.35, k), z: -1.6, rx: -0.10 + drift, ry: lerp(-0.32, -0.22, k), op: a * win(t, a0, LOOK - 0.2, 0.8, 0.5), pad: 0, rad: 10 });
    scrim(over, 0.0);
    const ua = a * win(t, S('site') + 0.8, LOOK - 0.3, 0.5, 0.4);
    over.save(); over.globalAlpha = ua * 0.85; over.fillStyle = 'rgba(8,6,5,0.85)'; over.fillRect(0, 860, W, 160); over.restore();
    urlMark(over, ua, 950, 52);
  } else if (t < S('paste') - 0.2) {
    const k = ease(ramp(t, S('lookup') - 0.2, S('lookup') + 1.2));
    const sidx = Math.min(4, Math.floor(ramp(t, S('lookup') + 0.2, S('lookup') + 1.4) * 5));
    await screens[0].show(`search_${sidx}`, { w: 6.4, x: -1.4, y: lerp(1.75, 1.6, k), z: -0.6, rx: -0.10, ry: 0.20, op: a * win(t, S('lookup') - 0.2, S('paste') - 0.2, 0.5, 0.4), rad: 8 });
    const dk = eout(ramp(t, S('lookup') + 1.6, S('lookup') + 2.6));
    await screens[1].show('detail', { w: 6.4, x: -1.4, y: lerp(-1.3, -0.75, dk), z: -0.6, rx: -0.10, ry: 0.20, op: a * dk * win(t, S('lookup') - 0.2, S('paste') - 0.2, 0.5, 0.4), rad: 8, cropBottom: 260 });
    headline(over, t, 'Any gene. A simple answer.', S('lookup'), S('lookup') + 1.6, { size: 46, y: 500, x: 1500, maxW: 640, w: 500, out: S('paste') - 0.6 });
    text(over, 'Does it follow the food, or not?', 1480, 575, { fam: SERIF, size: 32, w: 500, italic: true, color: C.dim, a: a * ramp(t, S('lookup') + 2.2, S('lookup') + 2.8) * (1 - ramp(t, S('paste') - 0.8, S('paste') - 0.3)) });
  } else if (t < PASTE_END - 0.3) {
    const k = ramp(t, S('paste') - 0.2, PASTE_END - 0.3);
    const name = t < S('paste') + 1.0 ? 'list_input' : t < S('paste') + 4.2 ? seqFrame('list_seq_', 45, t, S('paste') + 1.0, S('paste') + 4.2) : 'list_done';
    const tall = name !== 'list_input';
    await screens[0].show(name, tall ? { w: 5.6, x: -2.0, y: lerp(-0.6, 1.0, ease(k)), z: -0.4, rx: -0.10, ry: 0.24, op: a * win(t, S('paste') - 0.2, PASTE_END - 0.3, 0.4, 0.4), rad: 8 }
      : { w: 6.2, x: -1.8, y: 0.2, z: -0.4, rx: -0.1, ry: 0.22, op: a * win(t, S('paste') - 0.2, PASTE_END - 0.3, 0.4, 0.4), rad: 8 });
    headline(over, t, 'Paste your own gene list.', S('paste'), S('paste') + 2.0, { size: 48, y: 470, x: 1480, maxW: 560, w: 500, out: PASTE_END - 0.8 });
    text(over, 'See which look like diet effects.', 1480, 545, { fam: SERIF, size: 32, w: 500, italic: true, color: C.dim, a: a * ramp(t, S('paste') + 2.4, S('paste') + 3.0) * (1 - ramp(t, PASTE_END - 0.8, PASTE_END - 0.3)) });
  } else if (has('sam') && t < MUSE0 - 0.3) {
    /* SAM 3.1 outlines organoids in two microscope images, then the measured comparison */
    const s0 = S('sam'), s1 = MUSE0 - 0.3, seqEnd = s0 + 4.8, cardAt = s0 + 5.4;
    /* frame 00 was captured before the second image loaded, so the sequence starts at 01 */
    const idx = 1 + Math.floor(clamp((t - s0 - 0.2) / (seqEnd - s0 - 0.2)) * 14);
    const name = t < seqEnd ? `meas_seq_${String(idx).padStart(2, '0')}` : 'meas_done';
    const k = ease(ramp(t, s0 - 0.3, s1)), up = ease(ramp(t, cardAt - 0.4, cardAt + 0.8));
    const fade = a * win(t, s0 - 0.3, s1, 0.4, 0.4);
    await screens[0].show(name, { w: lerp(8.4, 7.6, up), x: lerp(0.1, -0.1, k), y: lerp(-0.1, 1.05, up), z: lerp(-0.8, -0.6, k), rx: -0.08, ry: lerp(-0.14, -0.08, k), op: fade * (1 - 0.5 * up), pad: 44, cropBottom: 54, rad: 8 });
    const ca = ease(ramp(t, cardAt, cardAt + 0.8));
    if (ca > 0) await screens[1].show('meas_out', { w: 6.6, x: 0.15, y: lerp(-2.4, -0.85, ca), z: 0.3, rx: -0.06, ry: -0.06, op: fade * ca, pad: 40, rad: 10 });
    chip(over, 'SAM 3.1  ·  Meta’s vision model', W / 2, 118, { a: fade * win(t, s0, cardAt - 0.1, 0.5, 0.4), color: C.amber, size: 22 });
    label(over, 'outlines every organoid it can find · statistics on our server · Muse explains', W / 2, 934, { a: fade * win(t, s0 + 0.6, cardAt - 0.2, 0.5, 0.4), color: C.dim, size: 18 });
  } else if (t < LOOP - 0.3) {
    const t0 = MUSE0 + 0.3, typeEnd = MUSE0 + 2.6, seqEnd = S('ask') + 4.6;
    let name;
    if (t < typeEnd) name = ASK_TYPE[Math.min(20, Math.floor(ramp(t, t0, typeEnd) * 21))];
    else if (t < seqEnd) name = seqFrame('ask_seq_', 55, t, typeEnd + 0.2, seqEnd);
    else name = 'ask_done';
    const k = ease(ramp(t, MUSE0 - 0.3, LOOP));
    if (t < typeEnd) await screens[0].show(name, { w: 7.6, x: 0.0, y: 0.9, z: -0.3, rx: -0.10, ry: -0.18, op: a * ramp(t, MUSE0 - 0.3, MUSE0 + 0.3), rad: 8 });
    else await screens[0].show(name, { w: 8.4, x: lerp(0.0, -0.2, k), y: lerp(0.5, 0.1, k), z: lerp(-0.6, 0.2, k), rx: -0.08, ry: lerp(-0.2, -0.12, k), op: a * (1 - ramp(t, LOOP - 0.6, LOOP - 0.3)), rad: 10 });
    chip(over, 'Muse  ·  Meta’s AI model', W / 2, 150, { a: a * win(t, MUSE0, Math.min(LOOP, a1) - 0.4, 0.5, 0.4), color: C.amber, size: 22 });
    label(over, 'searches all 17,525 genes with its own tools · shows every step', W / 2, 920, { a: a * win(t, S('ask') + 0.4, Math.min(LOOP, a1) - 0.4, 0.5, 0.4), color: C.dim, size: 18 });
  } else {
    const k = ease(ramp(t, S('loop') - 0.3, a1));
    await screens[0].show('credits', { w: 8.6, x: 0, y: lerp(-0.6, -0.4, k), z: lerp(-0.6, 0.0, k), rx: -0.06, ry: 0.0, op: a * ramp(t, S('loop') - 0.3, S('loop') + 0.3), rad: 8 });
    headline(over, t, 'Muse ran the research loop behind this audit.', S('loop'), E('loop'), { size: 58, y: 330, w: 500, hl: { Muse: C.amber } });
  }
}

function sceneClose(t) {   // 10
  const c0 = SEC0(10) - (has('loop') ? 0.8 : 0.3); if (t < c0) return;
  const a = ramp(t, c0 + 0.2, c0 + 1.6) * (1 - ease(ramp(t, TOTAL - 1.6, TOTAL - 0.2)));
  dish(under, { cx: 0, floorY: 0.25, r: 1.25, a: a * 0.9, liquid: 1, tint: [190, 210, 225], tintA: 0.07 });
  drawCells(cloudA, LA, t, { cx: 0, sphY: 0.95, sphR: 0.62, m: 1, grow: 1, size: 0.11, alpha: a, spin: 0.1 });
  headline(over, t, 'Organoids are still a big step forward.', S('step'), E('step'), { size: 48, y: 760, w: 500, color: C.dim, out: S('title') - 0.6 });
  headline(over, t, 'We just need to check what we’re feeding them.', S('feed'), E('feed') - 0.4, { size: 48, y: 830, w: 500, out: S('title') - 0.6 });
  const ta = a * eout(ramp(t, S('title') - 0.1, S('title') + 0.6));
  if (ta > 0) {
    over.save(); over.globalAlpha = ta; font(over, SERIF, 132, 800); over.letterSpacing = '-3px'; over.textBaseline = 'alphabetic';
    const p1 = 'It’s the ', w1 = over.measureText(p1).width; font(over, SERIF, 132, 800, true); const p2 = 'Medium', w2 = over.measureText(p2).width; font(over, SERIF, 132, 800); const w3 = over.measureText('.').width;
    let x = W / 2 - (w1 + w2 + w3) / 2, y = 790 + (1 - ta) * 16;
    over.fillStyle = C.bone; over.fillText(p1, x, y); x += w1; font(over, SERIF, 132, 800, true); over.fillStyle = C.red; over.fillText(p2, x, y); x += w2; font(over, SERIF, 132, 800); over.fillStyle = C.bone; over.fillText('.', x, y);
    over.restore();
  }
  urlMark(over, a * ramp(t, S('url') - 0.15, S('url') + 0.3), 885, 40);
  label(over, 'Built with Muse by Meta · github.com/bmarti44/meta-hackathon', W / 2, 970, { a: a * ramp(t, S('url') + 0.8, S('url') + 1.4), size: 16, color: C.mute });
}

/* ================= frame ================= */
window.renderAt = async function (t) {
  under.clearRect(0, 0, W, H); over.clearRect(0, 0, W, H);
  under.fillStyle = C.bg; under.fillRect(0, 0, W, H);
  const gl = under.createRadialGradient(W / 2, H * 0.55, 0, W / 2, H * 0.55, H * 0.75); gl.addColorStop(0, 'rgba(60,40,26,0.35)'); gl.addColorStop(1, 'rgba(0,0,0,0)'); under.fillStyle = gl; under.fillRect(0, 0, W, H);
  cloudA.hide(); cloudB.hide(); cloudC.hide();
  camera.position.set(Math.sin(t * 0.05) * 0.06, Math.cos(t * 0.04) * 0.04, 10); camera.lookAt(0, 0, 0); camera.updateMatrixWorld();
  sceneIntro(t); sceneStudies(t); sceneCatch(t); sceneField(t); sceneWhy(t); sceneTest(t); await sceneDemo(t); sceneClose(t);
  renderer.render(scene, camera);
  const capA = (t > S('n85') - 0.3 && t < WHY - 0.1) ? 0 : 1;
  captions(over, t, capA);
  finish(over, t);
  return true;
};
window.TOTAL = TOTAL;
await document.fonts.load('600 64px Fraunces'); await document.fonts.load('italic 800 64px Fraunces'); await document.fonts.load('500 30px Archivo'); await document.fonts.load('500 20px "IBM Plex Mono"');
await document.fonts.ready;
window.READY = true;
const q = new URLSearchParams(location.search); if (q.has('t')) await window.renderAt(parseFloat(q.get('t')));
