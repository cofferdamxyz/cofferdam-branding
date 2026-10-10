# cofferdam-branding

The single source of truth for the Cofferdam brand: tokens, guidelines, assets, fonts, and the agent skills that design with them and keep **cofferdam-app**, **cofferdam-pages** and the Claude Design System artifact in sync.

```
tokens/tokens.json        colours (dark + light), type, spacing, radii, shadows, opacity — Design System format
tokens/brand.json         accent options, wallpapers, motion, defaults, website accent/texture
themes/seasonal/*.json    dated overlays (Christmas example included, disabled)
brand/                    the brand book (README.md + sections/)
assets/                   logos, wallpapers, website textures, partner marks (Base, Self)
fonts/                    Geist + Geist Mono
components/               web reference renditions of the app's UI kit (for the design-system artifact)
scripts/build.mjs         validate + generate dist/
scripts/sync.mjs          copy dist/ into the consumer repos
dist/                     generated — committed so consumers can diff it
.claude/skills/           cofferdam-design · cofferdam-brand-update · cofferdam-seasonal-theme · cofferdam-brand-sync
.github/workflows/        brand-sync: on push + daily → PRs on app and pages
```

## How a change flows

```
edit tokens / brand / assets  ──►  node scripts/build.mjs  ──►  dist/
                                         │  (validates names, aliases, files, WCAG contrast,
                                         │   picks the live seasonal overlay by date)
                                         ▼
          push to main ──► brand-sync workflow ──► PR on cofferdam-app   (src/lib/brand.generated.ts, wallpapers, fonts)
          daily cron   ──►                    └─► PR on cofferdam-pages (src/app/brand.generated.css, textures, marks)
                                              └─► republish the Design System artifact from dist/design-system/project
```

A seasonal theme is just an overlay file with a date window: the daily run switches it on and off and opens the PRs, so agents (and people) see it arrive as a reviewable diff.

## Commands

```bash
node scripts/build.mjs                      # build for today
node scripts/build.mjs --check --verbose    # validate only, print contrast tables
node scripts/build.mjs --date=2026-12-10    # preview what a date ships
node scripts/build.mjs --season=christmas   # force a season (or --season=none)
node scripts/sync.mjs                       # dry run against ../cofferdam-app and ../cofferdam-pages
node scripts/sync.mjs --write               # copy generated files into them
```

Node 20+, no dependencies.

## Decisions recorded here (2026-10-10)

- Neutral ladder: the app's — pure black / paper white. The website keeps `web-bg` #0a0a0a in dark as a documented exception (sticky-nav separation).
- Dark default accent: **Cerulean** on app and website (the site moves off Lime). Light: **Base Blue**.
- Typeface: **Geist + Geist Mono** everywhere (the app moves off the system font and drops the stale Self faces).
- Logo: the v5 interlocking-brackets mark is primary once its file is added to `assets/logos/`; the coffer-and-seal mark is the interim.

## Design System artifact

https://claude.ai/code/artifact/adcfadc5-b427-4d8d-aa1a-4d2d8fc10fc5 — generated from `dist/design-system/project/`. See `AGENTS.md`.

## Licences

Geist and Geist Mono: SIL Open Font License 1.1 (Vercel). Base marks: Base brand guidelines (`assets/partners/base/`). Self marks belong to Self.xyz. Wallpapers and the Cofferdam mark: © Cofferdam Inc.
