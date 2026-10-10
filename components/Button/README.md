The pill button every Cofferdam action uses: primary (solid `fg` on `bg`), secondary (outline) and ghost (text).

## When to use
- **primary** — the one main action on a screen ("Create account", "Send"). White-on-black in dark, near-black in light. Never accent-filled.
- **secondary** — the alternative next to it ("Import", "Maybe later"), a `border` outline.
- **ghost** — tertiary links in footers, in `fg-muted`.
- `lg` (56px) for full-width screen actions; `md` (44px) inline. Both `radius-pill`, `label` type.

## The consumer provides
`label` (required), `onPress`, and optionally `variant`, `size`, `loading` (spinner, busy), `disabled` (`opacity-disabled`), `leadingIcon` / `trailingIcon` (Lucide, 2px stroke), `fullWidth` (default true).

## Do / don't
- Press feedback is scale 0.97 + fade 10% over `fast`.
- One primary per screen. Copy is a verb phrase in sentence case.
- Don't recolour a button with the accent — the accent means proof, not action.

Hand-written web rendition of `cofferdam-app/src/components/ui/Button.tsx`.
