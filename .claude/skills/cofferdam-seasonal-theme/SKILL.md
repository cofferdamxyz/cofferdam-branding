---
name: cofferdam-seasonal-theme
description: Create, schedule, preview or retire a seasonal Cofferdam theme (Christmas, Carnaval, a launch week…) as a dated overlay that the app and website pick up automatically. Use when someone asks for a holiday, campaign or limited-time look.
---

# Seasonal themes

A season is a dated overlay in `themes/seasonal/<id>.json`. Read `brand/sections/3-seasonal-themes.md` first. Start from `themes/seasonal/christmas.json`.

## 1. Ask (once) for what's missing

- Name and id (kebab-case), the date window (month-day start and end; it may wrap the year), and which surfaces (`app`, `pages`).
- The accent: pick from the locked Base palette (`base-blue`, `base-cerulean`, `base-tan`, `base-yellow`, `base-green`, `base-lime`, `base-red`, `base-pink`). No new hexes.
- Any artwork (files go in `assets/seasonal/<id>/`) and any one-line copy.

## 2. Write the overlay

```json
{
  "id": "carnaval",
  "name": "Carnaval",
  "enabled": true,
  "window": { "start": "02-13", "end": "02-18" },
  "surfaces": ["app", "pages"],
  "color": {
    "accent": { "dark": "{base-yellow}" },
    "accent-dim": { "dark": "rgba(255, 209, 47, 0.14)" },
    "accent-border": { "dark": "rgba(255, 209, 47, 0.32)" }
  },
  "defaults": { "accent": { "dark": "yellow" } },
  "web": { "brandAccent": { "dark": "base-yellow" } }
}
```

- `color` may override any existing colour token per theme — in practice `accent` and its `-dim`/`-border` companions (0.14 / 0.32 alpha of the same hex). Leave the neutrals, type, spacing and logo alone.
- `defaults.accent` must be an accent id from `tokens/brand.json` for that scheme; `web.brandAccent` a palette token name.
- Keep light on `base-blue` unless the chosen hue holds 4.5:1 on white (none of the others do).

## 3. Preview and validate

```bash
node scripts/build.mjs --check --season=carnaval      # contrast + overlap check
node scripts/build.mjs --date=2027-02-14 --verbose    # what that date would ship
```

The build refuses overlapping enabled windows and any accent under 4.5:1 on `bg`.

## 4. Ship

Commit with a `CHANGELOG.md` line and open a PR. After merge the daily `brand-sync` run turns the season on at the start date and off after the end date, opening a PR on each consumer each time. The app's accent change reaches people with the next release or OTA update — plan the PR merge a few days ahead of the start date. To end a season early, set `"enabled": false` (or `tokens/brand.json` → `season.force: "none"`).
