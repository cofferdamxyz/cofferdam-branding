The app's launch splash: the v5 mark draws itself one piece at a time, settles, then fades into the app.

## When to use
This card replays the native splash for review and for marketing captures. In the app, use `CofferdamSplash` from `cofferdam-branding/motion/splash/` (Expo + Reanimated) — this web version shares its timeline, wipe directions and colours.

## The consumer provides
`width` (default 220; height follows a phone ratio), optional `markScale` (0.74), `loop` (default true), and `children` — what the app shows underneath once the splash fades.

## Sequence
A stem wipes up → A arm wipes right → B stem wipes down → B arm wipes left (340ms each, 40ms apart, ease-out cubic) → 3.5% settle pulse → hold → 300ms fade with an 8% scale-up. Ground: `splash-bg` with the `splash-gradient-*` sweep fading in over 700ms; pieces in the `mark-*` tones. Reduce Motion shows the finished mark only.

Hand-written web rendition of `motion/splash/CofferdamSplash.tsx`.
