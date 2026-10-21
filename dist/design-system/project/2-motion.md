# Motion

Base's principle: motion is **purposeful, physical and Square-led**. It explains where things came from and where they went. In the app it runs on the UI thread (Reanimated worklets); on the website it runs in CSS first, with Framer Motion only where CSS cannot reach.

## Tokens

| Token | Value | Use |
|---|---|---|
| `fast` | 180ms | Press feedback, exits, reduce-motion cross-fades |
| `base` | 260ms | Fades, scale-ins, most transitions, scene swaps |
| `slow` | 380ms | Sheets rising (and the chat's top sheet dropping), the Square-wipe, stage reveals |
| `slower` | 520ms | Hero reveals; the longest change inside website footage |
| spring `snappy` | damping 18 · stiffness 220 · mass 0.8 | Taps, toggles, grid cells |
| spring `soft` | damping 22 · stiffness 140 · mass 1 | Sheets, cards settling |
| spring `bouncy` | damping 12 · stiffness 200 · mass 0.7 | Celebrations only |
| ease `out` | ease-out cubic, `cubic-bezier(0.33, 1, 0.68, 1)` | Entrances |
| ease `in` | ease-in cubic, `cubic-bezier(0.32, 0, 0.67, 0)` | Exits |
| ease `inOut` | ease-in-out cubic, `cubic-bezier(0.65, 0, 0.35, 1)` | Choreographed moves (the Square-wipe), scene steps |

The website reads the same tokens from `brand.generated.css`, so it moves like the app:

- `--cd-duration-fast | base | slow | slower` and `--cd-ease-out | in | in-out`.
- `--cd-spring-snappy | soft | bouncy`: each spring as a CSS `linear()` curve, simulated from the app's spring values by `scripts/build.mjs`, with its settle time as `--cd-spring-<name>-duration` (snappy 693ms with a 5% overshoot, soft 666ms with none, bouncy 836ms with 15%). Use a spring curve with its own duration, `transition: transform var(--cd-spring-snappy-duration) var(--cd-spring-snappy)`, and no JavaScript animation loop is needed for a physical feel.
- `--cd-scroll-parallax-max` (48px) and `--cd-scroll-inset-radius` (`radius-xl`) for scroll, `--cd-video-aspect` for footage (`tokens/brand.json` → `web.scroll`, `web.video`).

## Rules everywhere

- Springs for physical things; timing curves for choreographed sequences. Enter with ease-out, exit with ease-in.
- Signature transitions (Square-wipe, Center-burst, Grid-mosaic, Type-scramble) are for hero moments only: account ready, verified, first payment received.
- Grid entrances stagger 40ms per cell. Center-burst holds 120ms before collapsing.
- One motion language: things arrive by fading and settling, change by cross-fading, and leave by fading. No hard cuts in footage, no wipes except the Square-wipe, no bounce outside celebrations.

## In the app

- Two exceptions to "exits ease in": a sheet docked to a moving edge (the chat's top sheet, docked to the AI bar) lifts away with ease-out over `base`, because an ease-in exit would first dip with the bar; an in-place swap (send and stop, the + popover) runs `fast` with ease-out both ways.
- Press feedback: scale down 3% and fade 10% over `fast`. Controls on glass (the AI bar's buttons, its chips, popover rows) dim instead, to 50% (chips 65%), with no scale and no fill, so the material shows through.

## On the website

What may move, and nothing else:

| Moment | How |
|---|---|
| Hero | Fades up in a staggered cascade on load; the hero object floats on a 6-second sine |
| Tiles | Reveal once on scroll (fade and rise, `slow`, ease-out) |
| Scroll | Scroll moves containers, never the playhead of a video. A scene stage may grow from an inset card (`--cd-scroll-inset-radius`, the page gutter) to full width as it enters, and one layer per scene may drift against the scroll by up to `--cd-scroll-parallax-max`. Scroll-linked motion is CSS first: `animation-timeline: view()` driving a registered `@property`, with a script fallback only where the browser lacks it. Snapping, if used, is `y proximity`, never mandatory |
| Scenes | The scene switcher (Workers · Hirers · Developers) swaps its stage with a cross-fade over `base`; captions swap in place in one grid cell, the old one out over `fast` with ease-in, the new one in over `base` with ease-out, so nothing below moves. No auto-advance |
| Footage | Plays when its scene is on screen and selected, pauses when it is not; play-once films stop on their end frame, loops loop (`5-footage.md`) |
| Press and hover | Fade to 85% or move one property; never scale a card, never animate a shadow or a gradient |
| Focus | The 2px accent outline appears instantly; it never animates |
| Intro | On the first home-page visit of a browsing session, and never on an anchor deep link, the page opens with the launch splash: the `splash-bg` ground with its gradient sweep, the mark drawing itself exactly as in the app (`motion.splash`: A stem → A arm → B stem → B arm, 200ms each, 20ms apart, from 40ms), then the page revealed through the mark's own slanted rounded square, growing from the mark's size past the viewport edges over `slow` with ease-in-out; about 1.3 s in all, no settle and no hold. The page is fully rendered underneath from the first frame, the layer takes no pointer events and is hidden from assistive technology, and a click, key or scroll skips to the end. CSS only, from `--cd-intro-*`; a few lines of script decide whether it runs (`motion.webIntro`, workspace decision 0050) |

The intro was proposed in `brand/proposals/web-intro.md` and adopted on 2026-10-21 (workspace decision 0050): the mark's square as the reveal shape, once per session.

## Reduce Motion

Every animation carries its own override, on top of any global switch.

| Moment | Under Reduce Motion |
|---|---|
| App hero transitions | A `fast` cross-fade |
| Launch splash | The finished mark for 400ms, then exit |
| Website hero cascade, tile reveals | Opacity only, no movement |
| Hero float, decorative loops | Not rendered |
| Scroll-linked growth and parallax | Off: the stage sits at its final size, layers do not drift |
| Scene swap | Instant, or a `fast` cross-fade |
| Footage | Never autoplays: the poster shows, with a play control |
| Intro | Not shown: the page appears as it does on a repeat visit |

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
- The native splash (`app.json`) is a plain colour only — `splash-bg` per theme, no image.
