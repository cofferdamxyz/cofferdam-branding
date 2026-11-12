Cofferdam on social networks: profile assets rendered from the current tokens by `scripts/render-social.py`.

- `x-header.png` — the X profile header, 1500×500. The brand statement in Geist 700, set right on the Obsidian stone with `cofferdam.xyz` beneath in Geist Mono. The statement sits in the band phones keep (X trims about 70px top and bottom) and clear of the lower left, where X lays the profile picture. No mark and no name: the picture carries the mark and X prints the name under the header. Dark only, since X shows one header in both its themes. Template: `social/x-header.html`.
- `x-avatar.png` — the X profile picture, 400×400: the colour icon tile, the same art as the GitHub enterprise avatar, with the mark inside the circle-safe area, so it holds whether X crops it to a circle or, for a verified organisation, a rounded square.

Re-render both after a texture, type or icon-tile change: `node scripts/build.mjs && python3 scripts/render-social.py` (Playwright).
