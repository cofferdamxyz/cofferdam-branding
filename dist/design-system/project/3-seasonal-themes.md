# Seasonal themes

A seasonal theme is a **dated overlay** on the brand, not a new brand. It lives in `themes/seasonal/<id>.json` in cofferdam-branding and can change only these things:

- colour token values (usually `accent`, `accent-dim`, `accent-border`), per theme;
- the default accent id the app falls back to, and the website's brand accent;
- optional seasonal artwork under `assets/seasonal/<id>/` and optional copy strings.

It never changes the neutral ladder, type, spacing, radii or the logo.

## How it goes live

1. The overlay has `"enabled": true` and a `window` (`"start": "12-01", "end": "12-26"`, month-day, may wrap the year).
2. The build picks the live overlay for the current date (or `--season=<id>` / `--date=` to preview) and fails if two overlap.
3. The sync workflow runs on every push **and daily**, so a season starts and ends on its own: it opens a pull request on cofferdam-app and cofferdam-pages with the regenerated files.
4. A person merges. The app ships its accent change in the next release (or over the air); the site redeploys.

## Rules for a seasonal palette

- Pick from the locked Base palette. No new hexes.
- The seasonal `accent` still means proof, and still holds 4.5:1 on `bg` in each theme it overrides (the build checks). Base Red passes on black (5.9:1) but not on white (3.6:1) — keep Base Blue for light.
- Users who picked their own accent keep it; the season changes the default and the website.
- Copy stays in the brand voice: one line, no hype, at most one emoji.

The repository ships a disabled **Christmas** example (Base Red as the dark accent) to copy from.
