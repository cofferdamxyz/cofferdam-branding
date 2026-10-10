---
name: cofferdam-brand-update
description: Change the Cofferdam brand itself — a colour, type style, spacing or radius step, accent option, wallpaper, logo, font or guideline — in the cofferdam-branding repo, validate it, and ship it to the app, the website and the design-system artifact. Use when someone asks to update, add or remove anything in the brand.
---

# Updating the Cofferdam brand

The repository is the single source of truth. cofferdam-app, cofferdam-pages and the Claude Design System artifact are outputs — never edit brand values there.

## 1. Find the right file

| Change | Edit |
|---|---|
| Colour, type style, spacing, radius, shadow, opacity | `tokens/tokens.json` |
| Accent options, wallpapers, motion, defaults, website accent/texture | `tokens/brand.json` |
| A dated seasonal look | `themes/seasonal/<id>.json` — use `cofferdam-seasonal-theme` |
| Guidelines, voice, rules | `brand/README.md`, `brand/sections/*.md` |
| Logo / wallpaper / texture / partner mark | `assets/…` (copy the real file; never redraw) |
| Fonts | `fonts/` + `type.fonts` in `tokens/tokens.json` |

## 2. Rules for tokens

- `tokens/tokens.json` is in the Design System format: every family is a LIST of `{name, value, usage}`; colours per theme as `{ "dark": …, "light": … }` (dark first — light inherits dark when missing); aliases as `"{other-token}"`.
- Names: `[A-Za-z0-9][A-Za-z0-9_.-]*`, unique across families. Every token has a usage note naming where it's used and, for text colours, the grounds it reads on.
- Base palette values are locked (brand.base.org). Don't change them; add a new option only from that palette.
- Colours: hex or `rgb()/rgba()`. No `var()`, `color-mix()` or named colours.
- Renaming a token breaks consumers: add the new one, migrate, then remove the old one in a later change.

## 3. Validate

```bash
node scripts/build.mjs --check      # names, aliases, files, contrast
node scripts/build.mjs --verbose    # full contrast + accent tables
node scripts/build.mjs              # write dist/
node scripts/sync.mjs               # dry run: which consumer files would change
```

The build fails on any new text/ground pair under 4.5:1. If a real brand decision must miss it, add the pair to `KNOWN` in `scripts/build.mjs` AND say so in the token's usage note.

## 4. Record and ship

1. Add a line to `CHANGELOG.md` (date, what, why). Bump `version` in `tokens/tokens.json` for token changes, `tokens/brand.json` for brand data.
2. Update `brand/README.md` if a rule changed.
3. Commit and open a PR on cofferdam-branding. On merge, `.github/workflows/brand-sync.yml` regenerates and opens `brand-sync/auto` PRs on cofferdam-app and cofferdam-pages.
4. Republish the design-system artifact from `dist/design-system/project/` (see `AGENTS.md` → "Design System artifact").
5. If the change needs UI wiring (a brand-new token, not just a new value), follow `cofferdam-brand-sync` in each consumer.
