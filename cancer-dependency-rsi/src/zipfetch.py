"""Fail-closed ZIP member extraction by exact ranges (hardened per sgen003 review, 84/100).

Validates: 206 status + exact Content-Range bounds/total before consuming the body;
bounded reads (expected length + 1, reject excess/truncation); EOCD structure
(comment length, single-disk, non-ZIP64 sentinel check, declared entry count);
complete central-directory consumption; local-header filename/method/flags vs
directory metadata; member bounds; CRC32. Receipts returned per request.
Only files selected BEFORE any policy use may be fetched through this module.
"""
from __future__ import annotations

import hashlib
import re
import struct
import time
import urllib.request
import zlib

UA = {'User-Agent': 'cd-rsi-zipfetch/3.0'}


class Budget:
    """Caller-supplied allowances reserved BEFORE dispatch (review issue 2).
    Failed attempts consume request allowance; bytes reserved = requested length."""

    def __init__(self, max_requests, max_bytes):
        self.max_requests, self.max_bytes = max_requests, max_bytes
        self.requests_used = 0
        self.bytes_reserved = 0

    def reserve(self, nbytes):
        if self.requests_used + 1 > self.max_requests:
            raise RuntimeError(f'request ceiling exceeded ({self.max_requests})')
        if self.bytes_reserved + nbytes > self.max_bytes:
            raise RuntimeError(f'byte ceiling exceeded ({self.max_bytes})')
        self.requests_used += 1
        self.bytes_reserved += nbytes
_CR = re.compile(r'bytes (\d+)-(\d+)/(\d+)')


def _get(url, start, end, total_expected, receipts, budget=None):
    """Fetch exactly bytes [start, end] inclusive; fail closed on any mismatch."""
    if start < 0 or end < start:
        raise RuntimeError(f'invalid range {start}-{end}')
    want = end - start + 1
    if budget is not None:
        budget.reserve(want + 1)  # reserve the excess-detection byte before dispatch
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={**UA, 'Range': f'bytes={start}-{end}'})
    with urllib.request.urlopen(req, timeout=90) as r:
        status = r.status
        cr = r.headers.get('Content-Range') or ''
        m = _CR.fullmatch(cr.strip())
        if status != 206 or m is None:
            raise RuntimeError(f'range not honored: status={status} content-range={cr!r}')
        got_s, got_e, got_total = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if (got_s, got_e) != (start, end) or (total_expected is not None and got_total != total_expected):
            raise RuntimeError(f'Content-Range mismatch: got {got_s}-{got_e}/{got_total}, want {start}-{end}/{total_expected}')
        body = r.read(want + 1)
    if len(body) != want:
        raise RuntimeError(f'body length {len(body)} != requested {want} (truncated or excess)')
    receipts.append({'url': url, 'range': f'bytes={start}-{end}', 'status': status,
                     'content_range': cr, 'bytes': len(body),
                     'sha256': hashlib.sha256(body).hexdigest(), 'wall_s': round(time.monotonic() - t0, 3)})
    return body


def list_members(url, size, receipts, budget=None):
    """Return validated central-directory entries. Raises on any structural defect."""
    tail = _get(url, max(0, size - 65536), size - 1, size, receipts, budget)
    i = tail.rfind(b'PK\x05\x06')
    if i < 0 or i + 22 > len(tail):
        raise RuntimeError('EOCD not found in 64KiB tail window (fail-closed stop)')
    (disk, cd_disk, n_disk, n_total, cs, co, clen) = struct.unpack('<HHHHIIH', tail[i + 4:i + 22])
    if i + 22 + clen != len(tail):
        raise RuntimeError('EOCD comment length inconsistent with tail')
    if disk != 0 or cd_disk != 0 or n_disk != n_total:
        raise RuntimeError('multi-disk archive rejected')
    if n_total == 0xFFFF or cs == 0xFFFFFFFF or co == 0xFFFFFFFF:
        raise RuntimeError('ZIP64 sentinel present; not supported by this fetcher')
    if co + cs > size - 22 - clen:
        raise RuntimeError('central directory bounds exceed archive')
    cd = _get(url, co, co + cs - 1, size, receipts, budget)
    out, p = [], 0
    while p < len(cd):
        if p + 46 > len(cd) or cd[p:p + 4] != b'PK\x01\x02':
            raise RuntimeError(f'central directory corrupt at offset {p}')
        flags, method = struct.unpack('<HH', cd[p + 8:p + 12])
        crc, comp, uncomp = struct.unpack('<III', cd[p + 16:p + 28])
        nl, el, cl = struct.unpack('<HHH', cd[p + 28:p + 34])
        disk_start = struct.unpack('<H', cd[p + 34:p + 36])[0]
        lho = struct.unpack('<I', cd[p + 42:p + 46])[0]
        if disk_start != 0:
            raise RuntimeError('entry starting disk nonzero rejected')
        if flags & 0x0001:
            raise RuntimeError('encrypted entry rejected')
        if comp == 0xFFFFFFFF or uncomp == 0xFFFFFFFF or lho == 0xFFFFFFFF:
            raise RuntimeError('ZIP64 entry sentinel rejected')
        if p + 46 + nl + el + cl > len(cd):
            raise RuntimeError('central directory entry overruns directory')
        if lho >= co:
            raise RuntimeError('local header offset beyond central directory')
        out.append({'name': cd[p + 46:p + 46 + nl].decode('utf-8', 'replace'),
                    'comp_size': comp, 'uncomp_size': uncomp, 'crc': crc,
                    'method': method, 'flags': flags, 'lho': lho, 'cd_off': co, 'name_bytes': cd[p + 46:p + 46 + nl]})
        p += 46 + nl + el + cl
    if p != len(cd) or len(out) != n_total:
        raise RuntimeError(f'incomplete directory parse: consumed {p}/{len(cd)}, entries {len(out)}/{n_total}')
    return out


def fetch_member(url, size, member, receipts, budget=None):
    """Fetch and decompress one member by exact ranges; verify local header + CRC32."""
    lh = _get(url, member['lho'], member['lho'] + 29, size, receipts, budget)
    if lh[:4] != b'PK\x03\x04':
        raise RuntimeError('bad local header signature')
    lflags, lmethod = struct.unpack('<HH', lh[6:10])
    lcrc, lcomp, luncomp = struct.unpack('<III', lh[14:26])
    if not (lflags & 0x0008) and (lcrc, lcomp, luncomp) != (member['crc'], member['comp_size'], member['uncomp_size']):
        raise RuntimeError('local CRC/sizes != directory metadata (data-descriptor flag unset)')
    nl, el = struct.unpack('<HH', lh[26:30])
    name_b = _get(url, member['lho'] + 30, member['lho'] + 30 + nl - 1, size, receipts, budget) if nl else b''
    if name_b != member.get('name_bytes', member['name'].encode()):
        raise RuntimeError('local filename bytes != directory filename bytes')
    if lmethod != member['method'] or lflags != member['flags']:
        raise RuntimeError('local method/flags != directory metadata')
    start = member['lho'] + 30 + nl + el
    if start + member['comp_size'] > size:
        raise RuntimeError('member data overruns archive')
    if 'cd_off' in member and start + member['comp_size'] > member['cd_off']:
        raise RuntimeError('member region overlaps central directory')
    raw = _get(url, start, start + member['comp_size'] - 1, size, receipts, budget)
    if member['uncomp_size'] > 64 * 1024 * 1024:
        raise RuntimeError('declared uncompressed size exceeds 64 MiB cap; rejected before inflation')
    if member['method'] == 8:
        dobj = zlib.decompressobj(-15)
        data = dobj.decompress(raw, member['uncomp_size'] + 1)
        if not dobj.eof or dobj.unused_data:
            raise RuntimeError('compressed stream not completely/exactly consumed')
    elif member['method'] == 0:
        data = raw
    else:
        raise RuntimeError(f"unsupported compression method {member['method']}")
    if len(data) != member['uncomp_size'] or (zlib.crc32(data) & 0xFFFFFFFF) != member['crc']:
        raise RuntimeError(f"CRC/size mismatch for {member['name']}")
    return data
