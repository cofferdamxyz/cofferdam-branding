# Source and updates

This design system is generated from the **cofferdam-branding** repository (`cofferdamxyz/cofferdam-branding`). The repository is the single source of truth; cofferdam-app, cofferdam-pages and this artifact are outputs.

| Change | Where |
|---|---|
| A colour, size, radius, shadow | `tokens/tokens.json` |
| Accent options, wallpapers, motion, defaults | `tokens/brand.json` |
| A seasonal look | `themes/seasonal/<id>.json` |
| Guidelines and voice | `brand/README.md`, `brand/sections/` |
| Logos, wallpapers, textures, partner marks | `assets/` |
| Fonts | `fonts/` |

`node scripts/build.mjs` validates every value (names, aliases, files, contrast) and writes:

- `dist/app/brand.generated.ts` → cofferdam-app `src/lib/brand.generated.ts`
- `dist/pages/brand.generated.css` → cofferdam-pages `src/app/brand.generated.css`
- `dist/brand.resolved.json` → anything else (decks, emails, agents)
- `dist/design-system/project/` → this artifact

Edits made in this page are welcome for exploring, but carry them back to the repository or the next sync overwrites them.
