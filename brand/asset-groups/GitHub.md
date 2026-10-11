Cofferdam on GitHub: account avatars and the organisation profile header, rendered from the current tokens by `scripts/render-github.py`.

- `avatar-enterprise-light.png` / `-dark.png` — the colour icon tile, for the GitHub Enterprise account and the `cofferdamxyz` organisation.
- `avatar-cofferdamdev-light.png` / `-dark.png` — the greyscale tile, for the CofferdamDev account, so the tooling account never passes for the brand.
- `banner-light.png` / `banner-dark.png` — the profile header (the design-system cover at 2x, rounded, transparent corners). The README swaps them with `<picture>` and `prefers-color-scheme`.

GitHub shows one avatar per account in every theme, so pick one of each pair. Recommended: the **light** enterprise icon (Cerulean stands out on both GitHub themes; the navy tile nearly matches GitHub's dark background) and the **dark** CofferdamDev icon (charcoal reads on GitHub light and still separates from GitHub dark). Avatars are full-bleed 1024 px squares with the mark inside the circle-safe area — upload as is; GitHub rounds organisation avatars and circles user avatars. SVG sources sit beside the PNGs in `assets/github/`.

The profile README lives in `github/profile/README.md`; `node scripts/sync.mjs --only=github --write` copies it and its assets into a local clone of `cofferdamxyz/.github` (default `../github-profile`).
