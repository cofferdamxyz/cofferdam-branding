---
name: cofferdam-brand-sync
description: Bring brand changes from cofferdam-branding into cofferdam-app or cofferdam-pages — review a brand-sync PR, copy the generated files, and wire tokens into theme.ts, customization.ts or globals.css. Use in either consumer repo when a brand-sync PR arrives or the brand was updated.
---

# Syncing the brand into the app and the website

The consumers never hold brand values of their own: they import generated files. A brand change arrives as a `brand-sync/auto` PR (or run `node scripts/sync.mjs --write` from cofferdam-branding locally).

## Generated files (never edit by hand)

| Consumer | File | From |
|---|---|---|
| cofferdam-app | `src/lib/brand.generated.ts` | `dist/app/brand.generated.ts` |
| cofferdam-app | `src/lib/brand.resolved.json` | `dist/brand.resolved.json` |
| cofferdam-app | `assets/wallpapers/*.png`, `assets/fonts/Geist*.woff2` | `assets/`, `fonts/` |
| cofferdam-pages | `src/app/brand.generated.css` | `dist/pages/brand.generated.css` |
| cofferdam-app | `src/components/brand/splash/{CofferdamSplash.tsx,splashMath.ts,cofferdamMark.ts}`, `assets/brand/cofferdam-mark-v5*.svg`, `assets/brand/cofferdam-lockup-*.svg` | `motion/splash/`, `assets/logos/v5/`, `assets/logos/lockups/` |
| cofferdam-pages | `public/textures/*.webp`, `public/brand/cofferdam-mark-v5*.svg`, `public/brand/cofferdam-lockup-*.svg` | `assets/` |

## One-time wiring — cofferdam-app

> Done on 2026-10-11 (cofferdam-app, tokens v6 / brand v3). Kept as the reference for a fresh consumer; a later brand-sync PR only needs the review steps below.

1. `src/lib/theme.ts`: replace the literal `darkColors`, `lightColors`, `spacing`, `radii`, `type`, `motion`, `shadow` with re-exports from `./brand.generated` (keep the Proxy, `setColorscheme`, `makeStyles`, `truncateAddress`). Key names already match.
2. `src/lib/customization.ts`: build `ACCENTS` from the generated `ACCENTS`, and `BACKGROUNDS` from the generated `BACKGROUNDS`, mapping `image` file names to `require('../../assets/wallpapers/<name>')` (Metro needs static requires — keep a small `{ 'obsidian.png': require(...) }` map). Take `DEFAULT_CUSTOMIZATION` and the 0.14/0.32 alphas from the generated file.
3. Fonts: native platforms cannot load the woff2 files. `yarn add @expo-google-fonts/geist @expo-google-fonts/geist-mono` and register their static 400–700 TTFs in the `expo-font` plugin in `app.json` — `ios.fonts` as a list (iOS reads the family from the files), `android.fonts` as XML families named `Geist` and `Geist Mono` with weights — then `npx expo prebuild --platform ios` (no `--clean`). Embedded fonts exist at launch, so nothing gates on them. The generated `type` already sets `fontFamily`. Check the plugin options against the Expo SDK docs for the installed version first.
4. `src/constants/theme.ts` (Expo template leftovers): migrate its users to `@/lib/theme`, then delete it.
5. Splash: mount `CofferdamSplash` from `src/components/brand/splash/` in the root layout as in `cofferdam-branding/motion/splash/App.example.tsx` (keep `SplashScreen.preventAutoHideAsync()`, hide the native splash in `onMounted`, pass `ready` once fonts and the session are loaded). Set the `expo-splash-screen` plugin to `backgroundColor` = light `splash-bg` (#3C8AFF) and `dark.backgroundColor` = dark `splash-bg` (#121A33), no image. Replace `CofferdamMark.tsx` (the old coffer mark) with the v5 SVG — single ink (`fg`) by default; the toned mark only on the icon tile or navy.
6. App icon: rebuild `assets/expo.icon` (iOS 26+/27 Icon Composer) from the four `layer-*.svg` files on the `splash-bg` gradient, and regenerate `icon.png` / Android adaptive layers — the current icon is Expo's placeholder.

## One-time wiring — cofferdam-pages

1. In `src/app/globals.css`, after the three `@import`s: `@import "./brand.generated.css";`
2. Delete the hand-written `--base-*`, `--self-teal`, `--brand*`, `--texture*` lines from `:root` and `.dark` (the generated file declares them).
3. Point the shadcn variables at brand tokens, in both `:root` and `.dark`: `--background: var(--cd-web-bg); --foreground: var(--cd-fg); --card: var(--cd-card); --popover: var(--cd-card); --primary: var(--cd-fg); --primary-foreground: var(--cd-bg); --secondary: var(--cd-surface-2); --muted: var(--cd-card); --muted-foreground: var(--cd-fg-muted); --destructive: var(--cd-danger); --surface-strong: var(--cd-surface-2); --radius: var(--cd-radius-web);` — keep the alpha `--border`/`--input`/`--ring` values. This moves light mode from #fafafa to the canonical #ffffff and the dark brand accent from Lime to Cerulean (both decided in the brand).
4. Set `viewport.themeColor` in `layout.tsx` to the dark `web-bg` (#0a0a0a) — it already is.
5. Replace `src/components/landing/CofferdamMark.tsx` (the old coffer mark) with the v5 geometry — use `cofferdam-lockup-horizontal-*.svg` (or its paths) in the nav and footer instead of mark + live text, `currentColor` single ink for the bare mark, the dark-tone version only for the SdkShowcase hero in dark — and update the SdkShowcase mask SVG to the v5 polygons. Regenerate the favicon from `cofferdam-mark-v5-white.svg` on `splash-bg`.

## Reviewing a brand-sync PR

1. Read the PR body: source commit and active season.
2. `git diff` the generated files. Values changed → nothing else to do. A key was **added** → wire it where the brand README says it's used. A key was **removed** → find its uses (`rg`) and migrate before merging.
3. Run the consumer's own checks (`expo lint` / `next build`) and look at the screens that show the accent (verified badge, Ready chip, the site's TrustEngine "Proven" tick, the Showcase swatches).
4. Merge. The app ships on its next release; the site on its next deploy.

Never "fix" a brand value in the consumer. If it's wrong, fix it in cofferdam-branding with `cofferdam-brand-update`.
