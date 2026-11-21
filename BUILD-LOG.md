# Build log — VELMORA poster (round 1)

- Bounty: the-poster-for-a-place-that-i-2-20261121-0539, "The Poster
  for a Place That Isn't There". Deadline 2026-11-21 15:39 WIB.
- Kit downloaded from https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539/kit
  (kit.tar.gz sha256 verified against kit.json on unpack).
- Concept: VELMORA, a floating island above a sea of clouds at dusk
  — lighthouse, whitewashed houses, waterfalls off the island edge,
  big golden moon. Chosen for one clear landmark, a legible name set
  into the picture, and a warm dusk palette that promises what a stay
  feels like.
- Build: build_poster.py draws the poster procedurally with Pillow
  (fixed seed 20261121, 2x supersampling, DejaVu/Noto fonts on the
  machine, no network, no external assets).
- Visual review (v1 -> v2 fixes): moon moved out of the name band so
  VELMORA is fully legible; moon glow blurred (was visible rings);
  lighthouse beam narrowed and dimmed (was a grey slab washing out
  the tagline); waterfalls shortened, tapered and faded (were stiff
  white sticks below the island); footer text darkened for contrast
  on the pale clouds; lamp glow tightened (was reading as a second
  moon).
- Final image: entry.png, 1024x1024 PNG, 282,451 bytes (< 1 MiB).
- Determinism: main.py copies entry.png byte for byte; two runs
  both sha256 a872f3d00516013e279669f9fb90c682534f1dd8698586171b57c41f507e23c4.
- main.py: stdlib only, no network, no clock, no randomness.
- NOT submitted: repo GitHub Public Bradestudio/the-poster-for-a-place-that-i-2-20261121-0539
  still to be created by Andi; transcripts bundle + submit by parent.
- Local commit: c22e65c (see git log).
