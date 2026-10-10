# Motion

Base's principle: motion is **purposeful, physical and Square-led**. It explains where things came from and where they went. In the app it runs on the UI thread (Reanimated worklets); on the site it's restrained Framer Motion.

## Tokens

| Token | Value | Use |
|---|---|---|
| `fast` | 180ms | Press feedback, exits, reduce-motion cross-fades |
| `base` | 260ms | Fades, scale-ins, most transitions |
| `slow` | 380ms | Sheets rising, the Square-wipe |
| `slower` | 520ms | Hero reveals |
| spring `snappy` | damping 18 · stiffness 220 · mass 0.8 | Taps, toggles, grid cells |
| spring `soft` | damping 22 · stiffness 140 · mass 1 | Sheets, cards settling |
| spring `bouncy` | damping 12 · stiffness 200 · mass 0.7 | Celebrations only |

## Rules

- Springs for physical things; timing curves for choreographed sequences. Enter with ease-out cubic, exit with ease-in cubic.
- Press feedback: scale down 3% and fade 10% over `fast`.
- Grid entrances stagger 40ms per cell. Center-burst holds 120ms before collapsing.
- Signature transitions (Square-wipe, Center-burst, Grid-mosaic, Type-scramble) are for hero moments only: wallet ready, verified, first balance.
- Website: hero fades up in a staggered cascade; tiles reveal on scroll; the phone mockup floats on a 6-second sine. Nothing else moves.
- Reduce Motion replaces every hero transition with a `fast` cross-fade and removes decorative loops (the logo sweep isn't rendered at all).

## Launch splash

The app opens on the v5 mark drawing itself, one piece at a time along one continuous path. Source: `motion/splash/` (Expo + Reanimated), timings in `tokens/brand.json` → `motion.splash`.

| Phase | Time | What happens |
|---|---|---|
| Quiet beat | 0–120ms | Flat `splash-bg` (matches the native splash, so frame 0 is seamless); the gradient fades in over 700ms |
| Draw | 120–1600ms | A stem (wipes up) → A arm (wipes right) → B stem (wipes down) → B arm (wipes left): 340ms each, ease-out cubic, 40ms apart. Never two pieces moving at once |
| Settle | 1600–1950ms | The whole mark pulses up 3.5% and back |
| Hold | +120ms, then until the app is ready | Finished mark on screen |
| Exit | 300ms | Fade out while scaling up 8%, revealing the app |

- The mark spans 74% of the screen width, centred.
- Light: Cerulean ground, light tones. Dark: navy ground, dark tones.
- Reduce Motion: show the finished mark for 400ms, then exit.
- The native splash (`app.json`) is a plain colour only — `splash-bg` per theme, no image.
