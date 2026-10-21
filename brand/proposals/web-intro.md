# Proposal: a website intro that replays the launch splash

Status: **proposed, not adopted** (2026-10-21). Open decision OD-13 in the workspace (`docs/open-decisions.md`). Until the founder rules, the website rule in `brand/sections/2-motion.md` stands: the hero fades up, tiles reveal, the phone floats, nothing else moves.

## Why

The app opens on its signature moment: the v5 mark draws itself, piece by piece, on the `splash-bg` ground. The website opens on a headline, so the two surfaces share a palette and a typeface but no moment. A short intro that replays the launch splash and then opens into the hero would make the first second of cofferdam.xyz feel like the first second of the app.

The pattern comes from a design study of revolut.com (2026-10-21, research only, no code or assets used): a roughly 1.5 s intro where a logo animates on a solid ground and the page is then revealed through a rounded-rectangle "iris" that opens from the centre to full bleed, with every step instant under Reduce Motion. Ours would use our own mark, timings and shape.

## The sequence

Every value is an existing token; nothing new is invented.

| Phase | Time | What happens |
|---|---|---|
| Ground | 0–40ms | Full-screen `splash-bg` (navy in dark, Cerulean in light); the `splash-gradient-*` sweep fades in over 400ms |
| Draw | 40–900ms | The launch splash's draw, unchanged: A stem → A arm → B stem → B arm, 200ms each, 20ms apart, ease-out cubic (`motion.splash`) |
| Open | 900–1280ms | The page is revealed through the mark's own silhouette, the slanted rounded square the brackets close into, growing from the mark's size to past the viewport edges over `slow` (380ms) with `--cd-ease-in-out`. The splash ground stays behind and is uncovered as the shape grows |
| Done | 1280ms | The intro layer is removed; the hero's own staggered fade-up starts as the shape passes it |

About 1.3 s in all, shorter than the app's 1.4 s, because the website has nothing to wait for. The app's settle pulse and hold are dropped: they exist in the app to cover loading.

## Rules it must keep

- **First visit per session only**, on the home page only, and never when the URL carries an anchor (a deep link such as `#hire` goes straight to its section).
- **Never blocks.** The page is fully rendered underneath from the first frame; the intro layer ignores pointer events and is `aria-hidden`, focus is never trapped, and a click, key press or scroll skips to the end.
- **Reduce Motion: no intro at all.** The page appears as it does today.
- **CSS only.** Keyframes generated from `motion.splash` and the motion tokens, `clip-path` for the reveal, no JavaScript animation loop; a few lines of script only to skip it on repeat visits.
- **Performance.** The hero headline stays server-rendered and painted under the layer, so the largest paint is not delayed by script; the intro adds no network request (the mark is inline SVG).
- **Brand.** The splash ground is a brand moment with no proof elements, so it may use Cerulean in light (brand README, "Light mode: brand art and proof stay apart"). The toned mark appears on its own ground only, as in the app.

## What the founder decides

1. Whether the website gets an intro at all (it changes the website motion rule).
2. The reveal shape: the mark's slanted rounded square (proposed, ties the moment to the Square) or a plain rounded rectangle.
3. Frequency: first visit per session (proposed) or first visit ever.

If adopted, this becomes a token block (`motion.webIntro` in `tokens/brand.json`), a website rule in `2-motion.md`, a component next to `components/Splash`, and a CHANGELOG line; cofferdam-pages then wires it through `cofferdam-brand-sync`.
