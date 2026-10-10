Cofferdam is a work-matching app and website built on Base: workers find jobs, hirers post them, the money is set aside before the job starts, and every finished job is signed off by someone who was there. The brand inherits Base's system — palette, the Square, motion grammar, voice — and adds one rule of its own: **colour is earned**. Everything is black, white and grey until something is proven.

**Brand statement:** *Cofferdam — sealed crypto, built on Base.* On the website, for a non-crypto reader: *Work that proves itself.*

## Principles

- **Dark-first, monochrome canvas.** Pure black `bg` ground, white `fg`, greyscale structure (`surface`, `card`, `border`, `divider`). Every surface and CTA stays zero-chroma.
- **One accent at a time, and it means something.** `accent` marks proof: verified ticks, the live/active state, the Ready chip, focus. Never eyebrows, links, headings or decoration. The moment the accent lands on decoration it stops reading as *proven*.
- **The Square is the seed.** Base's Square is the atomic shape. Marks, avatars, tiles, cards and wallpapers rhyme with it through the `radius-*` scale.
- **Calm, physical motion.** Purposeful, with mass, on the UI thread. Never decorative jitter.
- **Plain, punchy voice.** Brief, human, active. "Your face is your key." not "Biometric authentication enrolment."

## Colour

- Set app screens on `bg` (pure black / paper white). Set the website on `web-bg` (#0a0a0a in dark so the sticky nav separates; white in light). Raise with `surface` → `surface-2`; put tiles and cards on `card` with a `card-border` hairline.
- Body text in `fg`; secondary in `fg-muted` (≥7:1 in both themes). Keep `fg-muted-2` for tertiary hints or 24px+ text — it is 4.2:1 on dark `bg` and 3.5:1 on light. `fg-dim` is disabled only.
- Primary actions are **white-on-black** in dark (`fg` fill, `bg` label) and near-black in light. The accent never fills a primary button.
- `accent` defaults to **Cerulean** (`base-cerulean`, 6.3:1 on black) in dark and **Base Blue** (`base-blue`, 8.6:1 on white) in light. Pair accent text with `accent-dim` fill and `accent-border` hairline (the Ready chip, the verified pill).
- **Never put Base Blue on a dark background** (2.4:1, and the Base guidelines forbid it). The Base Square is white on dark, blue only on light.
- The Base palette tokens (`base-blue`, `base-cerulean`, `base-tan`, `base-yellow`, `base-green`, `base-lime`, `base-red`, `base-pink`) are locked hex values from brand.base.org. Never interpolate, tint or invent shades. Components read `accent`, never a swatch directly.
- `danger`, `warning`, `success`, `info` are status only, independent of the user's accent, and always come with a word or icon. Base Green is an accent option, not `success`.
- `self-teal` is Self.xyz's colour. Use it only inside the Self mark/card and as the last accent option.

## Typography

- Set everything in **Geist** (`sans`); addresses, hashes and code in **Geist Mono** (`mono`). On the website enable Geist's `ss01`, `cv01`, `cv11` stylistic sets on `body`.
- Use the scale as roles: `display` for the balance hero, `title` for onboarding and page headlines, `h1`/`h2` for section and card heads, `body` for copy, `body-muted` for secondary copy, `label` for buttons and chips, `caption` for metadata, `eyebrow` (uppercase, 0.2em tracking) for website section labels.
- Build hierarchy with size and weight, never colour. Money always uses tabular figures; truncate addresses as `0xfb13…9de`.
- Website headlines may scale fluidly (`clamp()`) above `title`; keep the negative tracking of `display`.

## Shape and spacing

- Spacing runs on a 4px grid: `space-xxs` 2 → `space-huge` 64. Screen gutter and card padding `space-base`; gaps between cards `space-xl`; between sections `space-xxl`. Website sections pad `space-section` (96) on mobile and `space-section-lg` (128) from md up.
- Corners: chips `radius-sm`, tiles and inputs `radius-lg`, cards `radius-xl`, sheets `radius-xxl`, buttons and status chips `radius-pill`. The website's shadcn scale derives from `radius-web` (10px). Product UI never uses a hard rectangle.
- Prefer hairline borders to shadows, especially in dark. `shadow-card` and `shadow-card-lg` are for light mode and popovers; `shadow-fab` is the FAB only.
- Surfaces are **solid**, not glass, on the website (`surface`, `surface-strong` utilities). In the app, chrome over content may use the native glass material (Liquid Glass on iOS 26+, blur fallback elsewhere).

## Logo

- Primary mark: the **interlocking brackets** (v5) — two point-symmetric slanted brackets with folded-corner tones. *File pending: add it under `assets/Logos/` when final.*
- Interim mark in production: the rounded-square **coffer** (outer ring) with an offset solid **seal** (`cofferdam-mark.svg`, Cerulean; `cofferdam-mark-white.svg` on dark; `cofferdam-mark-black.svg` on light). Give it clear space of at least half its width; never stretch, rotate, outline or recolour it outside these inks.
- The app icon currently in `cofferdam-app` is Expo's placeholder brandmark, not ours. Don't ship it.
- **Built on Base:** use the approved Base lockup or Basemark (white on dark, black or blue on light) with the copy "Built on Base." Never type the Base wordmark in our font.

## Imagery and texture

- Wallpapers are stone and fibre textures, square and centre-cropped so they survive any aspect ratio: **Obsidian, Carbon, Graphite** on dark; **Marble, Sand, Ice** on light; plus flat Pure Black / Paper White (the defaults).
- On the website, paint the texture as an `aria-hidden` layer behind content at `opacity-texture-dark` (0.5, Obsidian) or `opacity-texture-light` (0.4, Marble), faded with a mask. Never below 0.3 — the source art is low-contrast and disappears.
- No illustrations, mascots, gradients or emoji decoration. Product footage and real app captures carry the story; crop personal data out.

## Iconography

- **Lucide** line icons: single weight, 2px rounded stroke, 24px grid, monochrome (`fg` / `fg-muted`). Same DNA as the mark.
- An icon turns `accent` only for a verified, active or selected state. Container glyphs (documents, cards) stay square-cornered.
- Every icon-only control has a label; tap targets are at least 44px.

## Voice

- Write like a knowledgeable friend, not a bank: brief, active, direct, optimistic but real. Two short sentences beat one long one.
- Say "use", not "utilize"; "Sending your payment.", not "Your transaction is being processed."
- On the website, zero crypto jargon: no "blockchain", "web3", "wallet", "on-chain", "gas", "stablecoin". Say "the money is locked before you accept".
- Never call Cofferdam a bank, never imply a return, never say "deposit", "savings account", "APY" or "guaranteed". Never imply custody of keys. Never overstate verification ("optional, but it unlocks more").
- Every number traces to a source document. No invented metrics, user counts or dates.
- One emoji at most, rarely. Times as `7am ET`; versions as `v2.6.4`.

## Accessibility

- Text holds 4.5:1 on the ground its token names, in both themes (3:1 for 24px+ text, icons, borders that carry meaning, focus rings). The known source exceptions are flagged in the token notes: `fg-muted-2`, light `warning`, light `success`.
- On light schemes, only Base Blue passes as accent text. Yellow, Green, Lime, Pink and Tan are below 3:1 on white — marks only there.
- Status never relies on colour alone. Honour Reduce Motion: hero transitions fall back to a `fast` cross-fade.

## Not synced

- Components are **hand-written web renditions** of the React Native kit in cofferdam-app (`src/components/ui/`): Button, StatusChip, Avatar, ChainLogo, BottomChip, GlassSurface, plus the site's CofferdamMark. Not carried over: Icon (use Lucide directly), Numpad, TxSpinner, AppBackground, SelfLogo, and the site's shadcn Button.
- Fonts are the Latin-subset Geist files the website ships; full-charset files are pending.
- The v5 interlocking-brackets logo is pending; the Base Brand Guidelines PDF stays in cofferdam-app.
