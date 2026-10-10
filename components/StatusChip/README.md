A pill that shows an in-flight process and its outcome: Reserving address → Deploying → Ready (or Failed).

## When to use
Wallet deployment and other short, multi-step background work the person is waiting on. In-flight states are neutral (`fg-muted` on a `border` outline) with a pulsing dot; **Ready** takes the accent (`accent` text, `accent-dim` fill, `accent-border`); **Failed** takes `danger`.

## The consumer provides
`status`: `'reserving' | 'deploying' | 'ready' | 'failed'`, and optionally a `label` to replace the default wording.

## Do / don't
- The dot pulses between 35% and 100% opacity on a 1.4s loop while in flight; it stops on Ready/Failed and under Reduce Motion.
- `caption` type with tabular figures. Keep labels to two or three words.
- Don't use the chip as a button.

Hand-written web rendition of `cofferdam-app/src/components/ui/StatusChip.tsx`.
