The Cofferdam mark, v5: two interlocking slanted brackets with folded-corner tones, drawn from the official 1024 geometry.

## When to use
Favicons, avatars, tab bars, app chrome and anywhere the name is already on screen. When the name isn't, use `CofferdamLockup`. For the app icon use `tile`; for the launch animation use `Splash`.

## The consumer provides
`size` (default 32), `tone` and `tile`:
- `ink` (default) — all four pieces in one colour (`currentColor`, or `color`): `fg` on any surface, white on Cerulean. This is the everyday mark.
- `mono` — the greyscale tones (`mark-mono-*`): dark greys on light grounds, light greys on `bg` in dark. Use where the folded-corner depth should show but colour isn't earned.
- `tones` — the colour tones (`mark-*`). The dark palette works on `bg`/navy; the light palette is the pale set for the Cerulean ground, so in light **only use it inside the tile**.
- `tile` — draws the app-icon ground (`splash-gradient-from` → `splash-gradient-to`, 22.5% corner) with the toned mark (ink ≈ 70% of the tile). Forces `tones`.

## Rules
- Clear space: the 1024 canvas padding (about 1/8 of the size).
- Minimum: 16px (ink or tile); `mono` and `tones` from 24px, where the tone steps still read.
- In light mode the colour mark lives only inside its tile; never next to proof blue on white (see brand README, *Light mode*).
- Don't rotate, outline, glow, reorder tones or pull the brackets apart.

Hand-written from `cofferdam-branding/motion/splash/cofferdamMark.ts`; replaces the retired coffer-and-seal mark.
