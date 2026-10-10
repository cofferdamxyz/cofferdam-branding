---
name: cofferdam-design
description: Design anything for Cofferdam — app screens, website sections, slides, social posts, emails, mockups — following the Cofferdam brand. Use whenever a design, layout, palette, typography, copy tone or asset choice for Cofferdam is being made.
---

# Designing for Cofferdam

Cofferdam's brand lives in the `cofferdam-branding` repository. Never copy values from memory or from the app/site source — read them here.

## 1. Load the brand (every time)

1. Read `brand/README.md` — principles, colour, type, shape, logo, imagery, icons, voice, accessibility.
2. Read the section that matches the job in `brand/sections/` (accents & wallpapers, motion, seasonal themes).
3. Take values from `dist/brand.resolved.json` (every token resolved per theme, the active season already applied). If `dist/` is stale or missing, run `node scripts/build.mjs` first.
4. Assets come from `assets/` and `fonts/` only. Never redraw, recolour or approximate a logo.

## 2. The rules that decide most designs

- **Dark-first, zero-chroma.** Black `bg` (website: `web-bg`), white `fg`, greys for structure. Design dark first; light mirrors it.
- **One accent, and it means proof.** `accent` (Cerulean on dark, Base Blue on light, or the active season's) goes on verified ticks, Ready/live states, focus, the site's proof signal. Never on eyebrows, headings, links, CTA fills or decoration.
- **Primary CTA = white-on-black** (dark) / near-black (light). Never accent-filled.
- **Never Base Blue on dark.** The Base Square is white on dark, blue on light.
- **Geist / Geist Mono** only. Hierarchy through size and weight from the type roles (`display`, `title`, `h1`, `h2`, `body`, `body-muted`, `label`, `caption`, `eyebrow`). Tabular figures for money.
- **Rounded, Square-family shapes.** Radii from `radius-*`; pills for buttons and chips. Hairline borders over shadows.
- **Textures, not illustrations.** Obsidian/Carbon/Graphite (dark), Marble/Sand/Ice (light). No mascots, emoji decoration or blue-purple glows; the only gradient is the icon/splash ground (`splash-gradient-*`).
- **Voice:** brief, human, active. The brand statement is *Work that proves itself.* Zero crypto jargon on every surface (no crypto, wallet, token, blockchain, gas, address, deploy) — "Built on Base." as a partner credit is the only exception. Never "bank", "deposit", "APY", "guaranteed". Every number cites a source doc.

## 3. Logo

The mark is v5, the interlocking brackets (`assets/logos/v5/`): `cofferdam-mark-v5.svg` on the Cerulean icon/splash ground, `cofferdam-mark-v5-on-dark.svg` on dark grounds, `cofferdam-mark-v5-white.svg` as a single ink. Never the light-tone mark on white; there is no mono SVG yet. Keep the canvas padding as clear space. The coffer-and-seal mark in `assets/logos/legacy/` is retired. For anything that animates the mark, follow the splash grammar in `brand/sections/2-motion.md`: one piece at a time, A stem → A arm → B stem → B arm. "Built on Base." uses the Base lockup from `assets/partners/base/`.

## 4. Check before you hand over

- Text contrast ≥ 4.5:1 on its ground in every theme you show (3:1 for 24px+, icons, focus rings). `fg-muted-2`, light `warning` and light `success` are known weak — don't use them for body copy.
- The accent appears only where something is proven or live.
- Status uses a word or icon, not colour alone.
- Copy passes the voice rules; numbers have a source.

If the design needs a value the brand doesn't have (a new colour, a new radius), don't invent it in the design — propose it through the `cofferdam-brand-update` skill.
