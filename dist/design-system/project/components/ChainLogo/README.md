The Base network mark: the official Base Square on a rounded tile, with a testnet variant for Sepolia.

## When to use
Currency and chain selectors, avatar chain badges, transaction rows. This is the reference implementation of the Square in product UI.

## The consumer provides
`chainId` (8453 → Base Mainnet; anything else → Base Sepolia) and `size` (default 24).

## Rules
- The Square is `chain-mark`: **white on dark, black on light**. Base's guidelines allow blue, black or white; product UI uses black on light because blue is reserved for proof (`accent`). Never change its corner radius or gradient it, and never put Base Blue on dark.
- Mainnet: solid tile. Sepolia: muted tile, hairline edge and a `warning` testnet dot, so the two read apart at a glance (the word "Sepolia" in the label carries it for screen readers).

Hand-written web rendition of `cofferdam-app/src/components/ui/ChainLogo.tsx` using the same Square path.
