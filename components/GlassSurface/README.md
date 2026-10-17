A translucent material for chrome that floats over content: the AI bar, its chips and its + popover.

## When to use
Only for chrome over scrolling content, a map or a wallpaper (the bar, its chips, a small popover anchored to the bar), never as a content card's background. On iOS 26+ the app renders Apple's Liquid Glass; elsewhere a blur with the `glass-scrim` layer (`rgba(20,21,24,0.55)` dark, `rgba(255,255,255,0.65)` light) keeps text legible.

## The consumer provides
`children`, and optionally `radius` (use a `radius-*` token: `radius-pill` for the bar and its chips, `radius-xl` for a popover), `style`. The native version also takes `intensity`, `tint`, `glassEffectStyle`, `tintColor`, `scrim` and `materialized`, which shows and hides Liquid Glass with UIKit's own animation for a surface that comes and goes.

## Rules
- The website does not use glass for surfaces — it uses solid `card`. Glass is an app-chrome material.
- Text on glass is `fg`; keep it to labels and icons.
- Never fade the glass or anything above it. Liquid Glass under a low-opacity ancestor is dropped for good, and the surface shows fully transparent. A glass surface that appears and goes away uses `materialized` and fades only its content.
- Pressed controls on glass dim their glyph or row and never fill, so the material shows through.

Hand-written web rendition of the blur fallback path of `cofferdam-app/src/components/ui/GlassSurface.tsx`.
