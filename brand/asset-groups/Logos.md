The Cofferdam mark, v5 — interlocking brackets, 1024 viewBox — and the Cofferdam lockups.

**Marks** (`v5/`)
- `cofferdam-mark-v5-white.svg` / `cofferdam-mark-v5-black.svg` — single ink. The default mark: white on dark or Cerulean, black (or `fg`) on light.
- `cofferdam-mark-v5-mono.svg` — greyscale tones for light grounds, the tinted/mono app icon and greyscale print. `-mono-on-dark.svg` is the same on black.
- `cofferdam-mark-v5-on-dark.svg` — colour tones, for black, `web-bg` and the navy splash.
- `cofferdam-mark-v5.svg` — pale colour tones, for the Cerulean icon/splash ground only. Never on white.
- `layer-1…4-*.svg` — the four pieces separately (A stem, A arm, B stem, B arm), for animation and icon tooling.
- `preview-light-dark-mono.png`, `preview-sizes.png` — icon renders in the current tones (`scripts/render-previews.py`). The designer's originals are in `original-renders/`.

**Lockups** (`lockups/`)
- `cofferdam-lockup-horizontal-*.svg` — nav, headers, footers, documents. Minimum 34px tall.
- `cofferdam-lockup-stacked-*.svg` — title cards, store art, square spaces. Minimum 84px tall.
- Variants: `on-dark` (colour mark, white type), `on-light` (greyscale mark, `fg` type), `white`, `black`. Clear space is built into each file.

`legacy/` — the retired coffer-and-seal mark. Don't use in new work. Regenerate marks and lockups with `python3 scripts/make-logos.py` after a mark token changes.
