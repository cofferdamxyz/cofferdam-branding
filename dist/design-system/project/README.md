Cofferdam is a work-matching app and website: workers find jobs, hirers post them, the money is set aside before the job starts, and every finished job is signed off by someone who was there. The brand inherits Base's system — palette, the Square, motion grammar, voice — and adds one rule of its own: **colour is earned**. Everything is black, white and grey until something is proven.

**Brand statement:** *Work that proves itself.* Use it as written — same words, sentence case, with the full stop — on the site, the store listings, the cover and sign-offs.

## Principles

- **Dark-first, monochrome canvas.** Pure black `bg` ground, white `fg`, greyscale structure (`surface`, `card`, `border`, `divider`). Every surface and CTA stays zero-chroma.
- **One accent at a time, and it means something.** `accent` marks proof: verified ticks, the live/active state, the Ready chip, focus. Never eyebrows, links, headings or decoration. The moment the accent lands on decoration it stops reading as *proven*.
- **The Square is the seed.** Base's Square is the atomic shape. The v5 brackets close into a slanted rounded square; avatars, tiles, cards and wallpapers rhyme with it through the `radius-*` scale.
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

- Set everything in **Geist** (`sans`); IDs, reference numbers and code in **Geist Mono** (`mono`). On the website enable Geist's `ss01`, `cv01`, `cv11` stylistic sets on `body`.
- Use the scale as roles: `display` for the balance hero, `title` for onboarding and page headlines, `h1`/`h2` for section and card heads, `body` for copy, `body-muted` for secondary copy, `label` for buttons and chips, `caption` for metadata, `eyebrow` (uppercase, 0.2em tracking) for website section labels.
- Build hierarchy with size and weight, never colour. Money always uses tabular figures; shorten long IDs in the middle, keeping the start and end (`CD-4821…09`).
- Website headlines may scale fluidly (`clamp()`) above `title`; keep the negative tracking of `display`.

## Shape and spacing

- Spacing runs on a 4px grid: `space-xxs` 2 → `space-huge` 64. Screen gutter and card padding `space-base`; gaps between cards `space-xl`; between sections `space-xxl`. Website sections pad `space-section` (96) on mobile and `space-section-lg` (128) from md up.
- Corners: chips `radius-sm`, tiles and inputs `radius-lg`, cards `radius-xl`, sheets `radius-xxl`, buttons and status chips `radius-pill`. The website's shadcn scale derives from `radius-web` (10px). Product UI never uses a hard rectangle.
- Prefer hairline borders to shadows, especially in dark. `shadow-card` and `shadow-card-lg` are for light mode and popovers; `shadow-fab` is the FAB only.
- Surfaces are **solid**, not glass, on the website (`surface`, `surface-strong` utilities). In the app, chrome over content may use the native glass material (Liquid Glass on iOS 26+, blur fallback elsewhere).

## Logo

- The mark is **v5, the interlocking brackets**: two point-symmetric slanted brackets, A (top-left) and B (bottom-right), each a stem plus an arm with a folded-corner tone — the cofferdam's two sealed halves, linked but separate. 1024 viewBox, four pieces.
- **On the Cerulean icon/splash ground** (`splash-bg` light): `cofferdam-mark-v5.svg` — tones `mark-a-arm` #EAF3FF, `mark-a-stem` #CFE2FF, `mark-b-arm` #BDD7FF, `mark-b-stem` #A3C8FF.
- **On dark grounds** (`bg`, `web-bg`, navy `splash-bg`): `cofferdam-mark-v5-on-dark.svg` — the dark palette (`mark-a-arm` #DCE9FF, `mark-a-stem` #B5CFF7, `mark-b-arm` #7DB2FF, `mark-b-stem` #5A97F2).
- **Tone balance:** light falls from the top-left, so A is lighter than B and each arm lighter than its stem — but the range is deliberately tight. No face is pure white; the top bracket must never outshine the bottom one. Don't brighten the arm to white for "pop".
- **Single ink:** `cofferdam-mark-v5-white.svg` on dark or on Cerulean when tones aren't possible (favicons below 32px, embossing, one-colour print). On light grounds use the greyscale (mono) treatment shown in `preview-light-dark-mono.png`; there is no mono SVG yet, so don't improvise one — ask for it.
- Never use the light-tone mark on white: its pale faces vanish.
- Keep the 1024 canvas padding as clear space (about one-eighth of the size on every side). Don't rotate, skew further, outline, add a glow, reorder the tones or separate the brackets. It holds down to 16px as a tile (see `preview-sizes.png`).
- **App icon:** the mark on the `splash-bg` ground with the `splash-gradient-from` → `splash-gradient-to` sweep (top-left to bottom-right), in the iOS/macOS 27 rounded-square glass style; navy in dark mode, greyscale for the tinted/mono icon. The icon in `cofferdam-app` today is still Expo's placeholder — replace it with this.
- **Splash:** the mark draws itself piece by piece (A stem → A arm → B stem → B arm, one at a time), settles with a small pulse, holds until the app is ready, then fades in. See *Motion*.
- The previous coffer-and-seal mark is retired (`assets/logos/legacy/`). Don't use it in new work.
- **Built on Base:** use the approved Base lockup or Basemark (white on dark, black or blue on light) with the copy "Built on Base." Never type the Base wordmark in our font.

## Imagery and texture

- Wallpapers are stone and fibre textures, square and centre-cropped so they survive any aspect ratio: **Obsidian, Carbon, Graphite** on dark; **Marble, Sand, Ice** on light; plus flat Pure Black / Paper White (the defaults).
- On the website, paint the texture as an `aria-hidden` layer behind content at `opacity-texture-dark` (0.5, Obsidian) or `opacity-texture-light` (0.4, Marble), faded with a mask. Never below 0.3 — the source art is low-contrast and disappears.
- No illustrations, mascots or emoji decoration. The one gradient in the brand is the icon/splash ground (`splash-gradient-from` → `splash-gradient-to`); nothing else gets one. Product footage and real app captures carry the story; crop personal data out.

## Iconography

- **Lucide** line icons: single weight, 2px rounded stroke, 24px grid, monochrome (`fg` / `fg-muted`). Rounded terminals echo the mark's soft corners.
- An icon turns `accent` only for a verified, active or selected state. Container glyphs (documents, cards) stay square-cornered.
- Every icon-only control has a label; tap targets are at least 44px.

## Voice

- Write like a knowledgeable friend, not a bank: brief, active, direct, optimistic but real. Two short sentences beat one long one.
- Say "use", not "utilize"; "Sending your payment.", not "Your transaction is being processed."
- **Zero crypto jargon, on every surface** — app, website, store listings, notifications, support replies. No "crypto", "blockchain", "web3", "wallet", "token", "on-chain", "gas", "stablecoin", "seed phrase", "address" (for an account), "deploy". Say "your account", "payment", "the money is locked before you accept", "signed off". The only exception is the partner credit "Built on Base." and Base's own logo.
- Never call Cofferdam a bank, never imply a return, never say "deposit", "savings account", "APY" or "guaranteed". Never imply Cofferdam holds people's money. Never overstate verification ("optional, but it unlocks more").
- Every number traces to a source document. No invented metrics, user counts or dates.
- One emoji at most, rarely. Times as `7am ET`; versions as `v2.6.4`.

## Accessibility

- Text holds 4.5:1 on the ground its token names, in both themes (3:1 for 24px+ text, icons, borders that carry meaning, focus rings). The known source exceptions are flagged in the token notes: `fg-muted-2`, light `warning`, light `success`.
- On light schemes, only Base Blue passes as accent text. Yellow, Green, Lime, Pink and Tan are below 3:1 on white — marks only there.
- Status never relies on colour alone. Honour Reduce Motion: hero transitions fall back to a `fast` cross-fade.

## Not synced

- Components are **hand-written web renditions** of the React Native kit in cofferdam-app (`src/components/ui/`): Button, StatusChip, Avatar, ChainLogo, BottomChip, GlassSurface, plus CofferdamMark (v5) and a web replay of the launch Splash. Not carried over: Icon (use Lucide directly), Numpad, TxSpinner, AppBackground, SelfLogo, and the site's shadcn Button.
- Fonts are the Latin-subset Geist files the website ships; full-charset files are pending.
- The v5 mark has no mono (greyscale) SVG yet — only the preview PNG. The Base Brand Guidelines PDF stays in cofferdam-app.
