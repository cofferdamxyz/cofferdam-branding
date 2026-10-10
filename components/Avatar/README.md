A circular profile picture with a monochrome initials fallback, an accent ✓ badge for verified people and an optional chain badge.

## When to use
People everywhere: the top bar, the drawer, message threads, contracts. `sm` 28 · `md` 40 · `lg` 64 · `xl` 96.

## The consumer provides
`name` (for initials) or `source` (image URL), and optionally `verified` (Self.xyz-bound → accent ✓ bottom-right), `chainId` (Base chain badge bottom-left, `lg` and `xl` only — at 40px and below it can't hold its tile, so it's dropped), `size`, `initials`.

## Do / don't
- Initials are `fg-muted` on `surface-2`, weight 600 at 40% of the diameter.
- The ✓ badge is the accent's main job: show it only for a real verification, never as decoration.
- Badges sit on a `bg`-coloured ring so they cut cleanly out of any surface; the chain badge fills with `chain-tile`.
- The chain badge's Square is white on dark and black on light, so the ✓ stays the only blue on the avatar.

Hand-written web rendition of `cofferdam-app/src/components/ui/Avatar.tsx` (the native version also supports a privacy blur).
