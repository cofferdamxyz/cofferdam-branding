# Fonts

| File | Family | Axes | Use |
|---|---|---|---|
| `Geist-Variable-latin.woff2` | Geist | wght 100–900 | Everything (`sans`) |
| `GeistMono-Variable-latin.woff2` | Geist Mono | wght 100–900 | Addresses, hashes, code (`mono`) |

These are the Latin-subset variable files the website already ships (from `next/font/google`), copied byte for byte. They cover Latin, not Latin Extended or Cyrillic. Before the app ships Geist, replace them with the full files from the official release (github.com/vercel/geist-font, OFL 1.1) under the same names, or add `-latin-ext` siblings and list them in `tokens/tokens.json` → `type.fonts`.

React Native cannot load woff2 (CoreText and Android need TTF/OTF), so cofferdam-app does not use these files natively: it embeds the Google Fonts static TTFs from `@expo-google-fonts/geist` and `@expo-google-fonts/geist-mono` (weights 400–700, OFL) through the `expo-font` config plugin — `ios.fonts` as a list, `android.fonts` as XML families — under the family names `Geist` and `Geist Mono` that the generated `type` styles reference. The sync still copies these woff2 files to `cofferdam-app/assets/fonts/` for a future web target.

Licence: SIL Open Font License 1.1, © Vercel.
