# Accents and wallpapers

In the app, people personalise Cofferdam with **one accent** and **two backgrounds** (Home and Lock). The options are fixed brand data in `tokens/brand.json`; the app and the site read them from the generated files, never from hand-copied hexes.

## Accents

Every option is a locked Base palette colour. The picked accent replaces `accent` everywhere: verification ticks, badges, active state. Its companions are derived: `accent-dim` at 0.14 alpha, `accent-border` at 0.32.

| Scheme | Options (default first) |
|---|---|
| Dark | **Cerulean**, Yellow, Green, Lime Green, Red, Pink, Tan, Self Teal |
| Light | **Base Blue**, Cerulean, Yellow, Green, Red, Pink, Tan, Self Teal (#00a37a) |

- Base Blue is absent from dark on purpose. Lime Green is dark-only.
- On light, only Base Blue is safe as accent **text** (8.6:1). Cerulean (3.4:1), Red (3.6:1) and Self Teal (3.2:1) work for marks and icons; Yellow, Green, Pink and Tan fall below 3:1 on white.
- The website follows the app's defaults: Cerulean on dark, Base Blue on light, on proof signals only. Its palette swatch row is the one place every accent shows at once.

## Backgrounds

| Scheme | Options (default first) |
|---|---|
| Dark | **Pure Black**, Obsidian, Carbon, Graphite |
| Light | **Paper White**, Marble, Sand, Ice |

- Wallpapers are 1440×1440 PNGs, centre-cropped (cover) so foldables and tablets keep the middle. The flat colour behind each (`base`) shows while the image decodes.
- The website reuses Obsidian (dark) and Marble (light) as 1080px WebP texture layers.
- Text over a wallpaper stays on a `card` or glass surface. Never set body copy straight on texture.
