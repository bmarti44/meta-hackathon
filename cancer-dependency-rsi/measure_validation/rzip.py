"""Read members of a remote zip with HTTP range requests. Usage: rzip.py URL list | rzip.py URL get OUTDIR NAME..."""
import io, sys, urllib.request, zipfile, os
class HF(io.RawIOBase):
    def __init__(s, url):
        s.url = url; s.pos = 0
        r = urllib.request.urlopen(urllib.request.Request(url, method="HEAD")); s.size = int(r.headers["Content-Length"])
    def seekable(s): return True
    def readable(s): return True
    def tell(s): return s.pos
    def seek(s, o, w=0):
        s.pos = o if w == 0 else s.pos + o if w == 1 else s.size + o; return s.pos
    def readinto(s, b):
        if s.pos >= s.size: return 0
        end = min(s.size, s.pos + len(b)) - 1
        d = urllib.request.urlopen(urllib.request.Request(s.url, headers={"Range": f"bytes={s.pos}-{end}"})).read()
        b[:len(d)] = d; s.pos += len(d); return len(d)
url, cmd = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(io.BufferedReader(HF(url), buffer_size=1 << 20))
if cmd == "list":
    for i in z.infolist(): print(i.file_size, i.filename)
else:
    out = sys.argv[3]
    for n in sys.argv[4:]:
        p = os.path.join(out, os.path.basename(n)); open(p, "wb").write(z.read(n)); print("got", p)
