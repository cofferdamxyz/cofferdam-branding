A translucent material for chrome that floats over content: the tab bar, the FAB menu, top-bar pills.

## When to use
Only over scrolling content or a wallpaper, never as a card background. On iOS 26+ the app renders Apple's Liquid Glass; elsewhere a blur with the `glass-scrim` layer` dark, `rgba(255,255,255,0.65)` light) keeps text legible.

## The consumer provides
`children`, and optionally `radius` (use a `radius-*` token, `radius-pill` for bars), `style`. The native version also takes `intensity`, `tint`, `glassEffectStyle`, `tintColor`, `scrim`.

## Rules
- The website does not use glass for surfaces — it uses solid `card`. Glass is an app-chrome material.
- Text on glass is `fg`; keep it to labels and icons.

Hand-written web rendition of the blur fallback path of `cofferdam-app/src/components/ui/GlassSurface.tsx`.
