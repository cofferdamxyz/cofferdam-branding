The Cofferdam mark, v5: two interlocking slanted brackets with folded-corner tones, drawn from the official 1024 geometry.

## When to use
Nav, footer, about screens, and anywhere the brand signs off. For the app icon and splash use the files in `assets/Logos` and the Splash component.

## The consumer provides
`size` (default 32) and `tone`:
- `tones` (default) — each piece filled from `mark-a-stem`, `mark-a-arm`, `mark-b-stem`, `mark-b-arm`. In the dark theme these are the dark palette (works on `bg`); in the light theme they are the pale palette for the Cerulean `splash-bg` ground, so **place it on `splash-bg` in light**, never on white.
- `ink` — all four pieces in one colour (`currentColor`, or `color`): `fg` on any surface, white on Cerulean.

## Rules
- Clear space: the 1024 canvas padding (about 1/8 of the size).
- Don't rotate, outline, glow, reorder tones or pull the brackets apart.
- Under Reduce Motion skip the website's sweep/glow effects.

Hand-written from `cofferdam-branding/motion/splash/cofferdamMark.ts`; replaces the retired coffer-and-seal mark.
