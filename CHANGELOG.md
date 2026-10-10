# Changelog

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
