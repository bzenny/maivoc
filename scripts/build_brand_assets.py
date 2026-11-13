#!/usr/bin/env python3
"""Rebuild transparent Maivoc master PNGs and opaque PWA icon set.

Requires Pillow==11.3.0 and CairoSVG==2.8.2. Network is not used.
See docs/MEDIA_GUIDE.md. Run from any working directory.
"""
from __future__ import annotations

import io
from pathlib import Path
import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / 'assets' / 'branding'
PWA = BRAND / 'pwa'
PWA.mkdir(parents=True, exist_ok=True)

def render_svg(svg: Path, width: int, height: int) -> Image.Image:
    output = cairosvg.svg2png(url=str(svg), output_width=width, output_height=height)
    return Image.open(io.BytesIO(output)).convert('RGBA')

def save(image: Image.Image, path: Path) -> None:
    image.save(path, format='PNG', optimize=True)
    print(f'{path.relative_to(ROOT)} {image.width}x{image.height}')

def tile(size: int, content_width: float = 0.85) -> Image.Image:
    background = Image.new('RGBA', (size, size), (11, 15, 23, 255))
    emblem = render_svg(BRAND / 'maivoc-mark.svg', size, size)
    target = round(size * content_width)
    emblem = emblem.resize((target, target), Image.Resampling.LANCZOS)
    offset = (size - target) // 2
    background.alpha_composite(emblem, (offset, offset))
    return background

save(render_svg(BRAND / 'maivoc-mark.svg', 1024, 1024), BRAND / 'maivoc-mark.png')
save(render_svg(BRAND / 'maivoc-lockup.svg', 1800, 440), BRAND / 'maivoc-lockup.png')
for size in (16, 32):
    save(render_svg(BRAND / 'maivoc-mark.svg', size, size), PWA / f'favicon-{size}x{size}.png')
save(tile(180), PWA / 'apple-touch-icon-180x180.png')
save(tile(192), PWA / 'icon-192x192.png')
save(tile(512), PWA / 'icon-512x512.png')
save(tile(512, 0.63), PWA / 'maskable-icon.png')
