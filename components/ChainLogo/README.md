The Base network mark: the official Base Square on a rounded tile, with a testnet variant for Sepolia.

## When to use
Currency and chain selectors, avatar chain badges, transaction rows. This is the reference implementation of "the Square on dark".

## The consumer provides
`chainId` (8453 → Base Mainnet; anything else → Base Sepolia) and `size` (default 24).

## Rules
- The Square is **white on dark, `base-blue` on light**. Never change its corner radius, never gradient it, never put Base Blue on dark.
- Mainnet: solid tile. Sepolia: muted tile, hairline edge and a testnet dot (`warning` amber on dark, `base-blue` on light) so the two read apart at a glance.

Hand-written web rendition of `cofferdam-app/src/components/ui/ChainLogo.tsx` using the same Square path.
