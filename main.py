#!/usr/bin/env python3
"""Entrypoint for the make.fun the-poster-for-a-place-that-i-2-20261121-0539 entry.

Writes one travel poster to /output/entry.png: VELMORA, the island
above the clouds -- a floating island at dusk with a lighthouse,
whitewashed houses and waterfalls pouring off its edge into a sea
of clouds, under a big golden moon. Stdlib only, no network, no
clock, no randomness: the program copies the entry image shipped in
this repository byte for byte, so every run writes the exact same
bytes.

The poster (1024x1024 PNG, ~283 KB):
- Name set large into the picture: VELMORA, with the tagline
  "THE ISLAND ABOVE THE CLOUDS" and the footer
  "REACHED ONLY BY SKY FERRY" -- the one way to arrive there.
- One landmark: the floating island itself, with its lighthouse
  sweeping a beam across the dusk sky.
- Palette: indigo night sky grading to amber dusk at the horizon,
  a pale gold moon, warm glowing windows, a sea of clouds below.
- The image was drawn procedurally by build_poster.py (Pillow,
  fixed seed, 2x supersampling); entry.png is its output.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    shutil.copyfile(ASSET, out)
    data = out.read_bytes()
    if len(data) > 1_048_576:
        print(f"entry.png too large: {len(data)} bytes", file=sys.stderr)
        return 1
    print(f"wrote {out} ({len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
