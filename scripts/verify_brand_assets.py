#!/usr/bin/env python3
"""Validate manifest path, PWA PNG dimensions and master-logo transparency (stdlib)."""
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / 'assets' / 'branding'
PWA = BRAND / 'pwa'
expected = {
    BRAND / 'maivoc-mark.png': (1024, 1024, True),
    BRAND / 'maivoc-lockup.png': (1800, 440, True),
    BRAND / 'maivoc-lockup-reversed.png': (1800, 440, True),
    PWA / 'favicon-16x16.png': (16, 16, True),
    PWA / 'favicon-32x32.png': (32, 32, True),
    PWA / 'apple-touch-icon-180x180.png': (180, 180, False),
    PWA / 'icon-192x192.png': (192, 192, False),
    PWA / 'icon-512x512.png': (512, 512, False),
    PWA / 'maskable-icon.png': (512, 512, False),
}
for path, (width, height, alpha) in expected.items():
    with path.open('rb') as file:
        header = file.read(26)
    assert header[:8] == b'\x89PNG\r\n\x1a\n', f'PNG signature: {path}'
    assert header[12:16] == b'IHDR', f'PNG IHDR: {path}'
    w,h,depth,color_type = struct.unpack('>IIBB', header[16:26])
    assert (w,h)==(width,height), f'Bad dimensions {path}: {(w,h)}'
    if alpha:
        assert color_type in (4, 6), f'Expected alpha channel: {path}'
manifest=json.loads((PWA / 'manifest.webmanifest').read_text())
assert manifest['short_name']=='Maivoc'
assert manifest['display']=='standalone'
assert manifest['start_url']=='/'
assert manifest['scope']=='/'
for entry in manifest['icons']:
    assert entry['src'].startswith('assets/')
    assert (PWA / entry['src'].split('/')[-1]).is_file()
assert any('maskable' in x.get('purpose','') for x in manifest['icons'])
print('Maivoc PNG and manifest checks passed.')
