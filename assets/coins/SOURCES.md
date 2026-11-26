# Coin marks: sources

The coins the app's money is in. Each mark is one file for both themes, fetched 2026-11-26 (the founder: "the logos for USDC and BRS (take from nora.finance)", then "Use Circle's official USDC logo instead").

| File | Source | Notes |
|---|---|---|
| `usdc.svg` (96×96) | Circle's brand kit (https://www.circle.com/pressroom#brandkit, "Download USDC logos" → `usdc.zip`, SHA-256 `538ce962…4fcd4bc9681f0fd44e1dfa82`), `Token Logo/USDC Token.svg`, byte for byte (SHA-256 `fe4f9d5f…11d1f5c57d`; nora.finance serves the same file). Fetched 2026-11-26 (the founder: "Use Circle's official USDC logo instead") | Circle's Brand Use Policy (https://6778953.fs1.hubspotusercontent-na1.net/hubfs/6778953/CircleBrandUsePolicy.pdf): never modified or recoloured and nothing superimposed on it; the brand kit's clear zone (the opening width in the symbol) kept free and the Token Logo at least 32px tall on screen; no implied affiliation or endorsement; a trademark line where feasible; and the policy says "Circle does not permit any use of its Brand Assets for commercial purposes" (questions: trademarks@circle.com) |
| `brs.svg` (96×96) | The BRS coin on nora.finance's landing page (`.lp-coin`), which Nora draws as five inline SVG parts (two arcs and the letters B, R, S) on one `viewBox` and animates into place | Nora publishes no static file (no brand kit on nora.finance or docs.nora.finance). The five paths are Nora's, byte for byte, on Nora's `viewBox`; the file only puts them in one `<svg>` with the colours Nora's stylesheet gives them at rest: the disc `#003C2F` (`.lp-coin__disc`, a circle filling the `viewBox`) and the glyphs `#E3FF63`. The coin's rim, slices and shine are 3D effects, not part of the mark, and are left out. BRS is Nora's; ask Nora for an official file before a wider use |

Never recolour either, and never overlap them: both stay as they are, side by side, on a dark or a light page.
