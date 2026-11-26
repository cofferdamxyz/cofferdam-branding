# Coin marks: sources

The coins the app's money is in. Each mark is one file for both themes. Fetched 2026-11-26 from nora.finance (the founder, 2026-11-26: "the logos for USDC and BRS (take from nora.finance)").

| File | Source | Notes |
|---|---|---|
| `usdc.svg` (96×96) | https://www.nora.finance/landing/usdc.svg, byte for byte (SHA-256 `fe4f9d5f…11d1f5c57d`) | Nora's rendering of Circle's USDC mark; its blue is `#0B53BF`, where Circle's own USDC file is `#2775CA`. USDC is Circle's trademark: Circle's own brand kit is the source to prefer if Circle asks |
| `brs.svg` (96×96) | The BRS coin on nora.finance's landing page (`.lp-coin`), which Nora draws as five inline SVG parts (two arcs and the letters B, R, S) on one `viewBox` and animates into place | Nora publishes no static file (no brand kit on nora.finance or docs.nora.finance). The five paths are Nora's, byte for byte, on Nora's `viewBox`; the file only puts them in one `<svg>` with the colours Nora's stylesheet gives them at rest: the disc `#003C2F` (`.lp-coin__disc`, a circle filling the `viewBox`) and the glyphs `#E3FF63`. The coin's rim, slices and shine are 3D effects, not part of the mark, and are left out. BRS is Nora's; ask Nora for an official file before a wider use |

Never recolour either; both stay as they are on a dark or a light page.
