"""Narration: one Eleven v4 pass per section (natural flow, light audio tags), then split at sentence ends
using the character timestamps and re-assembled with designed pauses.

Outputs (here): clips/secN.mp3 + clips/secN.json, narration.wav, timeline.json
Usage: python make_narration.py [section numbers to regenerate]
The API key is read from ELEVENLABS_API_KEY and never written anywhere.
"""
import base64, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOICE = "Xb7hH8MSUJpSbSDYk0k2"  # Alice: clear, engaging educator
MODEL = "eleven_v4"
SETTINGS = {"stability": 0.5, "similarity_boost": 0.8, "speed": 0.92}
LEAD, SR = 0.6, 48000

lines = json.loads((HERE / "lines.json").read_text())
for ln in lines:
    ln.setdefault("say", ln["show"])
clips = HERE / "clips"; clips.mkdir(exist_ok=True)
redo = {int(x) for x in sys.argv[1:]}
sections = sorted({ln["sec"] for ln in lines})


def tts(sec):
    text = " ".join(ln["say"] for ln in lines if ln["sec"] == sec)
    body = {"text": text, "model_id": MODEL, "voice_settings": SETTINGS}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_192",
        data=json.dumps(body).encode(), headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    assert "".join(d["alignment"]["characters"]) == text, "alignment does not match input text"
    (clips / f"sec{sec}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (clips / f"sec{sec}.json").write_text(json.dumps(d["alignment"]))
    print("tts section", sec, f"{d['alignment']['character_end_times_seconds'][-1]:.1f}s", flush=True)


for sec in sections:
    if sec in redo or not (clips / f"sec{sec}.mp3").exists():
        tts(sec)

# split every section into its lines. Cut points come from the audio itself: the quietest 10 ms frame
# between two sentences, then each piece is trimmed to where the voice actually starts and stops.
import array
def rms_frames(path):
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a = array.array("h"); a.frombytes(raw); hop = 160
    return [((sum(x * x for x in a[i:i + hop]) / hop) ** 0.5) / 32768 for i in range(0, len(a) - hop, hop)]
segs = []
for sec in sections:
    al = json.loads((clips / f"sec{sec}.json").read_text())
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    env = rms_frames(clips / f"sec{sec}.mp3"); peak = max(env); thr = peak * 0.035
    fr = lambda tt: max(0, min(len(env) - 1, int(tt * 100)))
    off = 0; spans = []
    for ln in [l for l in lines if l["sec"] == sec]:
        s_ = ln["say"]; mask = [True] * len(s_)
        for m in re.finditer(r"\[[^\]]*\]", s_):
            for k in range(m.start(), m.end()): mask[k] = False
        idx = [off + k for k, ch in enumerate(s_) if mask[k] and not ch.isspace()]
        spans.append([ln, st[idx[0]], en[idx[-1]], [(s_[k - off], st[k], en[k]) for k in idx]])
        off += len(s_) + 1
    # boundaries: quietest frame between the end of one line and the start of the next
    cuts = [0.0]
    for (_, _, e0, _), (_, s1, _, _) in zip(spans, spans[1:]):
        lo, hi = fr(e0 - 0.06), fr(s1 + 0.06)
        if hi <= lo: hi = lo + 1
        cuts.append(min(range(lo, hi + 1), key=lambda f: env[f]) / 100)
    cuts.append(len(env) / 100)
    for k, (ln, a0, b0, chars) in enumerate(spans):
        c0, c1 = cuts[k], cuts[k + 1]
        f = fr(c0)
        while f < fr(c1) and env[f] < thr: f += 1
        a = max(c0, f / 100 - 0.03)
        f = fr(c1) - 1
        while f > fr(c0) and env[f] < thr: f -= 1
        b = min(c1, f / 100 + 0.07)
        segs.append({"ln": ln, "src": f"sec{sec}", "a": a, "b": b, "chars": chars})

t = LEAD; timeline, filters, inputs, srcidx = [], [], [], {}
for sec in sections:
    srcidx[f"sec{sec}"] = len(srcidx); inputs += ["-i", str(clips / f"sec{sec}.mp3")]
for k, g in enumerate(segs):
    dur = g["b"] - g["a"]; ln = g["ln"]
    timeline.append({"i": k, "id": ln.get("id"), "sec": ln["sec"], "show": ln["show"], "mark": ln.get("mark"), "start": round(t, 3), "end": round(t + dur, 3),
                     "chars": [{"c": c, "t0": round(t + a - g["a"], 3), "t1": round(t + b - g["a"], 3)} for c, a, b in g["chars"]]})
    ms = int(t * 1000)
    filters.append(f"[{srcidx[g['src']]}:a]atrim={g['a']:.3f}:{g['b']:.3f},asetpts=PTS-STARTPTS,aresample={SR},"
                   f"afade=t=in:d=0.012,afade=t=out:st={max(0, dur - 0.05):.3f}:d=0.05,adelay={ms}|{ms}[a{k}]")
    t += dur + ln["gap"]
total = t
splits = {}
for k, g in enumerate(segs):
    splits.setdefault(srcidx[g["src"]], []).append(k)
# each source is used by several segments: split it first
pre = [f"[{i}:a]asplit={len(ks)}" + "".join(f"[s{i}_{j}]" for j in range(len(ks))) for i, ks in splits.items()]
use = {}
for i, ks in splits.items():
    for j, k in enumerate(ks): use[k] = f"[s{i}_{j}]"
filters = [f.replace(f"[{srcidx[segs[k]['src']]}:a]", use[k], 1) for k, f in enumerate(filters)]
mix = "".join(f"[a{k}]" for k in range(len(segs)))
graph = ";".join(pre + filters + [f"{mix}amix=inputs={len(segs)}:normalize=0,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[out]"])
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", graph,
                "-map", "[out]", "-ac", "1", "-ar", str(SR), str(HERE / "narration.wav")], check=True)
(HERE / "timeline.json").write_text(json.dumps({"total": round(total, 3), "lines": timeline}))
secs = {}
for ln in timeline:
    secs.setdefault(ln["sec"], [ln["start"], ln["end"]]); secs[ln["sec"]][1] = ln["end"]
print(f"total {total:.1f}s")
for k, v in secs.items(): print(f"  section {k}: {v[0]:6.1f} to {v[1]:6.1f}")
