# VELMORA — The Island Above the Clouds

Travel poster for a place that does not exist, for the make.fun
bounty `the-poster-for-a-place-that-i-2-20261121-0539`.

## The place

VELMORA is a floating island that hangs in the dusk sky above a sea
of clouds. Whitewashed houses and a red-banded lighthouse stand on
its green plateau; waterfalls pour off its edge and vanish into the
clouds below. The only way to arrive is by sky ferry.

## Files

- `main.py` — entrypoint: copies `entry.png` to `/output/entry.png`
  byte for byte (deterministic, stdlib only, no network).
- `entry.png` — the poster, 1024×1024 PNG.
- `build_poster.py` — the procedural Pillow script that drew the
  poster (fixed seed, 2× supersampling, no external assets).
- `LICENSE` — MIT.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Two runs produce byte-identical output (verified by sha256).
