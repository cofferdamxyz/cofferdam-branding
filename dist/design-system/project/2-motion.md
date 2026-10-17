# Motion

Base's principle: motion is **purposeful, physical and Square-led**. It explains where things came from and where they went. In the app it runs on the UI thread (Reanimated worklets); on the site it's restrained Framer Motion.

## Tokens

| Token | Value | Use |
|---|---|---|
| `fast` | 180ms | Press feedback, exits, reduce-motion cross-fades |
| `base` | 260ms | Fades, scale-ins, most transitions |
| `slow` | 380ms | Sheets rising (and the chat's top sheet dropping), the Square-wipe |
| `slower` | 520ms | Hero reveals |
| spring `snappy` | damping 18 · stiffness 220 · mass 0.8 | Taps, toggles, grid cells |
| spring `soft` | damping 22 · stiffness 140 · mass 1 | Sheets, cards settling |
| spring `bouncy` | damping 12 · stiffness 200 · mass 0.7 | Celebrations only |

## Rules

- Springs for physical things; timing curves for choreographed sequences. Enter with ease-out cubic, exit with ease-in cubic. Two app exceptions: a sheet docked to a moving edge (the chat's top sheet, docked to the AI bar) lifts away with ease-out over `base`, because an ease-in exit would first dip with the bar; an in-place swap (send and stop, the + popover) runs `fast` with ease-out both ways.
- Press feedback: scale down 3% and fade 10% over `fast`. Controls on glass (the AI bar's buttons, its chips, popover rows) dim instead, to 50% (chips 65%), with no scale and no fill, so the material shows through.
- Grid entrances stagger 40ms per cell. Center-burst holds 120ms before collapsing.
- Signature transitions (Square-wipe, Center-burst, Grid-mosaic, Type-scramble) are for hero moments only: account ready, verified, first payment received.
- Website: hero fades up in a staggered cascade; tiles reveal on scroll; the phone mockup floats on a 6-second sine. Nothing else moves.
- Reduce Motion replaces every hero transition with a `fast` cross-fade and removes decorative loops (the logo sweep isn't rendered at all).

## Launch splash

The app opens on the v5 mark drawing itself, one piece at a time along one continuous path. Source: `motion/splash/` (Expo + Reanimated), timings in `tokens/brand.json` → `motion.splash`.

| Phase | Time | What happens |
|---|---|---|
| Quiet beat | 0–40ms | Flat `splash-bg` (matches the native splash, so frame 0 is seamless); the gradient fades in over 400ms |
| Draw | 40–900ms | A stem (wipes up) → A arm (wipes right) → B stem (wipes down) → B arm (wipes left): 200ms each, ease-out cubic, 20ms apart. Never two pieces moving at once |
| Settle | 900–1120ms | The whole mark pulses up 3.5% and back |
| Hold | +40ms, then until the app is ready | Finished mark on screen |
| Exit | 220ms | Fade out while scaling up 8%, revealing the app |

The timeline starts on the overlay's first frame — it never waits for the Reduce Motion query — because the app underneath is usually ready within a second; about 1.4 s in all. (Tightened 2026-10-11 from 2.4 s: the first screen was arriving before the mark was half drawn.)

- The mark spans 74% of the screen width, centred.
- Light: Cerulean ground, light tones. Dark: navy ground, dark tones.
- Reduce Motion: show the finished mark for 400ms, then exit.
- The native splash (`app.json`) is a plain colour only — `splash-bg` per theme, no image.
