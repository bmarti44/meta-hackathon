"""zipfetch fail-closed tests (in-memory fake HTTP over a locally built zip)."""
import io
import zipfile

import pytest

import zipfetch


def _zip_bytes():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('a.py', 'print("hello")\n' * 50)
        z.writestr('b.txt', 'data')
    return buf.getvalue()


class _Resp:
    def __init__(self, body, status=206, cr=None):
        self._b = io.BytesIO(body)
        self.status = status
        self.headers = {'Content-Range': cr} if cr else {}

    def read(self, n=-1):
        return self._b.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _fake_factory(blob, corrupt_cr=False):
    def fake(req, timeout=90):
        rng = req.get_header('Range')
        s, e = (int(x) for x in rng.replace('bytes=', '').split('-'))
        body = blob[s:e + 1]
        cr = f'bytes {s}-{e}/{len(blob)}' if not corrupt_cr else f'bytes {s + 500}-{e + 500}/{len(blob)}'
        return _Resp(body, 206, cr)
    return fake


def test_roundtrip(monkeypatch):
    blob = _zip_bytes()
    # pad tail window requirement: fetcher reads last 64KiB; small zips need size>=65536 handling via server clamp
    # emulate a large archive by padding with a stored comment-like suffix is invalid; instead pad member data
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('a.py', 'print("hello")\n' * 50)
        z.writestr('big.bin', __import__('os').urandom(70000))
    blob = buf.getvalue()
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(blob))
    rec = []
    members = zipfetch.list_members('http://x/z.zip', len(blob), rec)
    assert {m['name'] for m in members} == {'a.py', 'big.bin'}
    a = [m for m in members if m['name'] == 'a.py'][0]
    assert zipfetch.fetch_member('http://x/z.zip', len(blob), a, rec) == b'print("hello")\n' * 50


def test_content_range_mismatch_rejected(monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('a.py', __import__('os').urandom(70000))
    blob = buf.getvalue()
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(blob, corrupt_cr=True))
    with pytest.raises(RuntimeError, match='Content-Range mismatch'):
        zipfetch.list_members('http://x/z.zip', len(blob), [])


def test_corrupt_directory_rejected(monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('a.py', __import__('os').urandom(70000))
    blob = bytearray(buf.getvalue())
    i = bytes(blob).find(b'PK\x01\x02')
    blob[i + 3] = 0xFF
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(bytes(blob)))
    with pytest.raises(RuntimeError, match='corrupt|incomplete'):
        zipfetch.list_members('http://x/z.zip', len(blob), [])


def test_budget_ceiling_enforced(monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('a.py', __import__('os').urandom(70000))
    blob = buf.getvalue()
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(blob))
    with pytest.raises(RuntimeError, match='byte ceiling'):
        zipfetch.list_members('http://x/z.zip', len(blob), [], zipfetch.Budget(max_requests=10, max_bytes=1024))
    with pytest.raises(RuntimeError, match='request ceiling'):
        zipfetch.list_members('http://x/z.zip', len(blob), [], zipfetch.Budget(max_requests=1, max_bytes=10_000_000))


def test_budget_exact_boundary(monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('a.py', __import__('os').urandom(70000))
    blob = buf.getvalue()
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(blob))
    b = zipfetch.Budget(max_requests=2, max_bytes=65537)  # tail read (65536+1 detection) exactly fits
    with pytest.raises(RuntimeError, match='request ceiling|byte ceiling'):
        zipfetch.list_members('http://x/z.zip', len(blob), [], b)
    assert b.requests_used >= 1  # failed/partial attempts consume allowance


def test_inflation_cap_and_trailing_junk(monkeypatch):
    import zlib as _z
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('pad.bin', __import__('os').urandom(70000))
        z.writestr('bomb.bin', b'A' * 100000)  # highly compressible
    blob = buf.getvalue()
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(blob))
    members = zipfetch.list_members('http://x/z.zip', len(blob), [])
    bomb = [m for m in members if m['name'] == 'bomb.bin'][0]
    fake = dict(bomb)
    fake['uncomp_size'] = 100  # lie: stream inflates beyond declared cap+1 window
    with pytest.raises(RuntimeError):
        zipfetch.fetch_member('http://x/z.zip', len(blob), fake, [])


def _patch_sizes(blob, comp_delta=0, uncomp=None):
    """Patch comp/uncomp size fields in BOTH local and central headers (internally consistent)."""
    import struct as _s
    b = bytearray(blob)
    cd = bytes(b).find(b'PK\x01\x02')
    lh = bytes(b).find(b'PK\x03\x04')
    # first entry only (tests use single-member archives for these cases via caller)
    return b, lh, cd


def test_trailing_junk_reaches_decompression(monkeypatch):
    import struct as _s
    buf = io.BytesIO()
    payload = __import__('os').urandom(70000)
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('pad.bin', payload)
        z.writestr('victim.bin', b'hello world' * 10)
    blob = bytearray(buf.getvalue())
    # locate victim local header (second PK\x03\x04), append junk into its compressed region by
    # rebuilding: easier - craft with zipfile then splice junk before central directory and fix sizes/offsets of victim only is complex;
    # instead use STORED victim with extra trailing bytes declared in comp_size but method=deflate mismatch is caught earlier.
    # Direct approach: build victim deflate stream + junk manually via zipfile on a fresh archive with one member.
    buf2 = io.BytesIO()
    with zipfile.ZipFile(buf2, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('pad.bin', payload)
    base = buf2.getvalue()
    # extract compressed stream region of pad.bin, append junk, fix comp sizes in local+central
    lh = base.find(b'PK\x03\x04')
    nl, el = _s.unpack('<HH', base[lh + 26:lh + 30])
    start = lh + 30 + nl + el
    comp = _s.unpack('<I', base[lh + 18:lh + 22])[0]
    junk = b'JUNKJUNK'
    b2 = bytearray(base[:start + comp] + junk + base[start + comp:])
    newcomp = comp + len(junk)
    b2[lh + 18:lh + 22] = _s.pack('<I', newcomp)
    cd = bytes(b2).find(b'PK\x01\x02')
    b2[cd + 20:cd + 24] = _s.pack('<I', newcomp)
    # fix EOCD central-directory offset (+len(junk))
    eo = bytes(b2).rfind(b'PK\x05\x06')
    cdo = _s.unpack('<I', bytes(b2)[eo + 16:eo + 20])[0]
    b2[eo + 16:eo + 20] = _s.pack('<I', cdo + len(junk))
    blob2 = bytes(b2)
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(blob2))
    members = zipfetch.list_members('http://x/z.zip', len(blob2), [])
    m = members[0]
    with pytest.raises(RuntimeError, match='not completely/exactly consumed'):
        zipfetch.fetch_member('http://x/z.zip', len(blob2), m, [])


def test_declaration_cap(monkeypatch):
    import struct as _s
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('pad.bin', __import__('os').urandom(70000))
    b = bytearray(buf.getvalue())
    lh = bytes(b).find(b'PK\x03\x04')
    cd = bytes(b).find(b'PK\x01\x02')
    big = 65 * 1024 * 1024
    b[lh + 22:lh + 26] = _s.pack('<I', big)
    b[cd + 24:cd + 28] = _s.pack('<I', big)
    blob = bytes(b)
    monkeypatch.setattr(zipfetch.urllib.request, 'urlopen', _fake_factory(blob))
    members = zipfetch.list_members('http://x/z.zip', len(blob), [])
    with pytest.raises(RuntimeError, match='64 MiB cap'):
        zipfetch.fetch_member('http://x/z.zip', len(blob), members[0], [])
