# Changelog

## 2026-10-21 — website motion tokens (brand v6)

- `tokens/brand.json` → `motion.easing`: the brand's three timing curves (ease-out, ease-in and ease-in-out cubic, the same curves as the app's Reanimated easings). The website CSS now carries them as `--cd-ease-out | in | in-out`.
- The springs (`snappy`, `soft`, `bouncy`) reach the website as CSS `linear()` curves, `--cd-spring-<name>` with `--cd-spring-<name>-duration`, simulated by `scripts/build.mjs` from the app's spring values. The site can move like the app without a JavaScript animation loop. Idea from a design study of bleap.finance and revolut.com (research only).
- `brand/sections/2-motion.md`: the easing rows, "On the website", and per-animation Reduce Motion overrides on the site.
- Proposed, not adopted: `brand/proposals/web-intro.md`, a first-visit website intro that replays the launch splash and opens into the hero (workspace OD-13).
- `components/Splash/README.md` stated the pre-2026-10-11 timings; it now gives the current ones.
- No value changed for the app: its generated file differs only in the build header.

## 2026-10-21 — the website gets the type roles and fluid headlines (brand v5)

- The website CSS (`dist/pages/brand.generated.css`) now carries every type role as `--cd-text-<role>-size / -line / -weight / -tracking`, the same values the app reads from `type`. The site had no type tokens and improvised its sizes per component (a Hallmark audit of cofferdam-pages found the same `clamp()` copied four times and sizes from 8 to 15px).
- New `web.headlines` in `tokens/brand.json`: the two fluid headlines the brand book allows on the website only, written as `--cd-headline-display-*` (40px at a 375px viewport to 88px at 1280px, line height 1, −0.03em) and `--cd-headline-title-*` (28px to 52px, 1.05, −0.02em). Both keep their role's weight (700), which is what makes the app read as finished; the lighter display weights of the reference sites studied (Bleap 400, Revolut 500) were rejected for that reason.
- No value changed for the app: its generated files differ only in the build header.

## 2026-10-18 — token notes follow the guidelines; the Design System artifact republished

- Usage notes only (no value changes): `accent` also marks the current selection; `radius-sm` is for small badges and a chat bubble's tail corner, chips being pills; `radius-xl` covers popovers. They had lagged the 2026-10-17 README.
- The Design System artifact carries the 2026-10-17 guidelines (`README.md`, `2-motion.md`, `GlassSurface`, `tokens.json`; via `af4e96f`); `dist/design-system/project/design-system.json` mirrors its index. These three notes reach it on the next publish.

## 2026-10-17 — guidelines follow the assistant-first Home (no value changes)

- The app's Home rebuild (workspace decisions 0024 and 0033 to 0036) left the guidelines describing chrome that is gone and missing rules the new chrome set. No token value changed, so consumers need no sync.
- `GlassSurface`: the material now covers the AI bar, its chips and its + popover (the tab bar and the FAB are gone). Glass never fades as a whole, because Liquid Glass under a low-opacity ancestor is dropped and shows fully transparent. A surface that comes and goes uses the native `materialized` prop. Pressed controls on glass dim and never fill. The `glass-scrim` values in the doc are repaired.
- README: the accent also marks the current selection; maps draw in the ground (the range is one translucent `bg` disc, 40% fill and 85% edge, never the accent). Corners: chips are pills and `radius-sm` is for small badges. Shadows: `shadow-card` and `shadow-card-lg` name their app users, and `shadow-fab` has none since the FAB left Home. NativeMenu is not carried over.
- Motion: two app exceptions to "exits ease in" (the chat's top sheet lifts away with ease-out over `base`; in-place swaps run `fast` ease-out both ways), and controls on glass dim instead of the 3% / 10% press.
- `tokens.json` usage notes for `radius-pill`, `shadow-card`, `shadow-card-lg` and `shadow-fab` follow the same changes (values unchanged).
- `cofferdam-design` skill: the same accent, map and glass rules.

## 2026-10-11 — faster launch splash (brand v4)

- Splash fix from the first device run: the pieces animate as `Path` `d` strings (`wipePath` in `splashMath.ts`), not `Polygon` `points` — react-native-svg converts points to a path only on React render, so the animated polygons never appeared and the launch showed a bare ground. The exit-timer ref is assigned in an effect (React Compiler rule).
- `motion.splash` tightened from about 2.4 s to about 1.4 s: start 40 ms (was 120), 200 ms per piece (340), 20 ms gaps (40), 220 ms settle (350), 40 ms hold (120), 220 ms exit (300), gradient fade 400 ms (700). The first screen was arriving before the mark was half drawn.
- `CofferdamSplash` starts its timeline on the first frame instead of after the asynchronous Reduce Motion query (which still jumps to the finished mark when it reports reduced motion). `splashMath.ts` carries `gradientFadeIn`; the motion section and the splash README follow. Splash preview videos/keyframes not re-rendered (no Playwright on this machine).

## 2026-10-11 — cofferdam-app wired

- The app consumes the brand: `brand.generated.ts`, wallpapers, v5 marks, lockups and the splash module synced in; `theme.ts` / `customization.ts` re-export the tokens, accents, wallpapers and defaults; `CofferdamMark` is the v5 geometry; `CofferdamSplash` is the launch splash over a plain `splash-bg` native splash; the Base Square in chain tiles is `chain-mark`; app icon, Android adaptive layers and favicon rendered from the mark geometry on the `splash-gradient-*` ground.
- Fonts: native platforms cannot load woff2, so the app embeds the Google Fonts static TTFs from `@expo-google-fonts/geist` / `geist-mono` (400–700) through the `expo-font` plugin under the families `Geist` and `Geist Mono` (`fonts/README.md`, brand book "Not synced", `cofferdam-brand-sync` step 3).

## 2026-10-11 — GitHub presence

- Avatars (`assets/github/`): enterprise / `cofferdamxyz` org on the colour icon tile, CofferdamDev on the greyscale tile, each in light and dark, 1024 px PNG + SVG, circle-safe.
- Organisation profile (`github/profile/README.md` + assets): the cover as a light/dark header via `<picture>`, the product story in brand voice, the open-source repositories with plain one-liners, and the "Built on Base." credit.
- `scripts/render-github.py` renders avatars and banners from the tokens (`npm run renders` now includes it); `scripts/sync.mjs --only=github` copies the profile into a local clone of `cofferdamxyz/.github`.

## 2026-10-10 — v6, blue means proof, mono tile, no hand-copied values

- New `chain-mark` token: the Base Square in chain badges and ChainLogo is white on dark and **black on light** (was Base Blue), so blue only ever means proof. The light testnet dot is now `warning` (was Base Blue).
- `CofferdamMark tile="mono"`: the greyscale icon tile from new `tile-mono-from` / `tile-mono-to` tokens (`tile` / `tile="brand"` keeps the colour tile; both get a `chain-tile-edge` hairline). The cover and `render-previews.py` use the same tokens.
- `CofferdamLockup tone="tones"` falls back to the greyscale mark in light instead of vanishing.
- Avatar: the chain badge shows at `lg` and `xl` only, on a filled `chain-tile` disc with an edge.
- New `radius-device` (28px) for phone frames; the Splash replay uses it. No hard-coded colours or radii remain in `bundle.css`.
- Build: `components/bundle.js` now carries the splash timing (`motion.splash`) and the wordmark (`wordmark.json`) in `@generated` blocks that the build refreshes and `--check` enforces; the Cover's mark comes from `{{mark-polygons}}`, filled from the official geometry.

## 2026-10-10 — v5, identity kit, cover, light-mode rule

- Lockups: horizontal and stacked, in `on-dark`, `on-light`, `white` and `black` (`assets/logos/lockups/`). Wordmark is Geist 700 at -0.03em, outlined. Geometry in cap heights: horizontal mark 1.4C / gap 0.5C, stacked 3.2C / 0.6C, clear space 0.5C; minimum 34px / 84px tall.
- New marks: `cofferdam-mark-v5-black.svg`, `cofferdam-mark-v5-mono.svg` and `-mono-on-dark.svg`, from new `mark-mono-*` tokens (greyscale, same tone order, tight range).
- `CofferdamMark` now defaults to single ink (`tone="ink"`); new `tone="mono"` and a `tile` prop that draws the app-icon tile. New `CofferdamLockup` component.
- Dark icon/splash ground lifted so the tile separates from black: `splash-bg` #0A0F1F → #121A33, gradient #141C34 → #1B2645 and #060A18 → #0B1124. Splash source and native splash colour updated.
- Brand book: single ink is the default mark; lockup rules; new "Light mode: brand art and proof stay apart" rule.
- Cover (v5.1): the stone texture is now the full background at the website texture opacity, faded under the name; the light cover uses the greyscale icon tile; the verified tick is removed from both covers (a brand moment carries no proof elements).
- Cover rebuilt around the idea: the app-icon tile on one stone texture (Obsidian / Marble) with one verified tick; the white square and grey band are gone.
- Icon previews, splash videos (light and dark) and keyframes re-rendered in the current tones (`scripts/render-previews.py`); designer originals kept in `original-renders/`.
- Build: new checks for mark-face contrast (mono on bg/surface-2, dark tones on the navy tile) and for stale generated logo files.

## 2026-10-10 — v4, light ladder, control borders, blue roles

- Light neutral ladder: `surface` #F7F7F8, `surface-2` #F0F0F3, `card-border` #DCDCE0, `border` #E2E2E6, `divider` #ECECEF (were all white / near-invisible).
- New `border-control` (dark #6C7079, light #8A8A8A): ≥3:1 outline for secondary buttons and inputs; the build now enforces it.
- Light `danger` darkened #D92B1A → #CC2818 so it holds 4.5:1 on the new `surface-2` (caught by the build).
- Blue roles: `accent` stays Base Blue (light) / Cerulean (dark) for proof; new `identity` token (Cerulean, both themes) for icon, splash, glow and brand art.
- Hard-coded component colours moved to tokens: `danger-dim`, `danger-border`, `glass-scrim`, `chain-tile`, `chain-tile-testnet`, `chain-tile-edge`; all exported to the app module.
- Light accent picker trimmed to Base Blue, Cerulean, Red, Self Teal (Yellow, Green, Pink, Tan removed: <3:1 on white).
- Cover: dropped the faint accent sliver.

## 2026-10-10 — v3, brand statement and mark tones

- Brand statement is now *Work that proves itself.* everywhere; "sealed crypto" is gone.
- Zero crypto jargon on every surface (was website only). Copy samples, StatusChip labels ("Getting ready", "Setting up") and token notes rewritten.
- Mark tones tightened (option A): no pure-white face; light #EAF3FF / #CFE2FF / #BDD7FF / #A3C8FF, dark #DCE9FF / #B5CFF7 / #7DB2FF / #5A97F2. Applied to the `mark-*` tokens, the v5 SVGs, the four layers and the splash source.
- Design-system cover: one v5 mark on the icon ground with the new statement.

## 2026-10-10 — v2, the v5 mark and the launch splash

- Logo: v5 interlocking brackets is now the mark (`assets/logos/v5/`, designer files verbatim, plus a generated on-dark variant). The coffer-and-seal mark moves to `assets/logos/legacy/`.
- New colour tokens: `splash-bg`, `splash-gradient-from`, `splash-gradient-to`, `mark-a-stem`, `mark-a-arm`, `mark-b-stem`, `mark-b-arm` (dark + light).
- Launch splash: `motion/splash/` (Expo source and previews); timings in `tokens/brand.json` → `motion.splash`; `splash` export in the app module; the build fails if the splash source and the tokens disagree.
- Sync now ships the splash component and v5 logos to the app and v5 logos to the site.
- Pending: a mono (greyscale) v5 SVG; the app icon rebuilt from the v5 layers.

## 2026-10-10 — v1, unified brand

- Created from `cofferdam-app` (`src/lib/theme.ts`, `src/lib/customization.ts`, `src/lib/motion.ts`, `docs/DESIGN.md`, `assets/wallpapers`, `assets/base`), `cofferdam-pages` (`src/app/globals.css`, `README.md` §3, `public/textures`, `CofferdamMark.tsx`) and `cofferdam-os/assets/branding/cofferdam-mark.svg`.
- Neutrals: app ladder canonical (pure black / white); website keeps `web-bg` #0a0a0a dark.
- Dark default accent Cerulean on both surfaces (website was Lime).
- Typeface Geist + Geist Mono everywhere (app was system font; Self's Advercase/DINOT/IBM Plex Mono retired).
- Seasonal overlay mechanism + disabled Christmas example.
- Pending: full-charset Geist files (current files are the Latin subsets the website ships).
