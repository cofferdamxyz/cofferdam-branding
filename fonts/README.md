# Fonts

| File | Family | Axes | Use |
|---|---|---|---|
| `Geist-Variable-latin.woff2` | Geist | wght 100–900 | Everything (`sans`) |
| `GeistMono-Variable-latin.woff2` | Geist Mono | wght 100–900 | Addresses, hashes, code (`mono`) |

These are the Latin-subset variable files the website already ships (from `next/font/google`), copied byte for byte. They cover Latin, not Latin Extended or Cyrillic. Before the app ships Geist, replace them with the full files from the official release (github.com/vercel/geist-font, OFL 1.1) under the same names, or add `-latin-ext` siblings and list them in `tokens/tokens.json` → `type.fonts`.

In React Native, `expo-font` registers each file under its family name (`Geist`, `Geist Mono`); the generated `type` styles already reference those names. Variable weights render on iOS; check Android, and fall back to static instances if a weight doesn't resolve.

Licence: SIL Open Font License 1.1, © Vercel.
