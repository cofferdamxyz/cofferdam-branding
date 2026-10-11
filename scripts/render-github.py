#!/usr/bin/env python3
"""Render the GitHub account avatars and the organisation profile assets from the current tokens.

    node scripts/build.mjs && python3 scripts/render-github.py

Reads dist/brand.resolved.json, dist/tokens.css, components/Cover/preview.html, the v5 geometry, the textures,
fonts and Base partner logos. Needs Playwright (Chromium) and Pillow. Writes:

  assets/github/avatar-enterprise-{light,dark}.{svg,png}   enterprise + cofferdamxyz org: the colour icon tile
  assets/github/avatar-cofferdamdev-{light,dark}.{svg,png} the CofferdamDev account: the greyscale tile
  github/profile/assets/banner-{light,dark}.png            org profile header (the design-system cover, 2x)
  github/profile/assets/base-lockup-{white,black}.svg      "Built on Base." credit (copied, never redrawn)

Avatars are full-bleed squares (GitHub rounds org avatars and circles user avatars), 1024 px, with the mark kept
inside the circle-safe area so the same file works for both crops.
"""
import json, os, re, shutil

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
PIECES = ['a-stem', 'a-arm', 'b-stem', 'b-arm']
# Mark canvas at 86% of the avatar: ink ≈ 65% wide, corners ≈ 0.69 of the radius — safe inside GitHub's circle crop.
MARK_SCALE = 0.86


def geometry():
    svg = open(P('assets', 'logos', 'v5', 'cofferdam-mark-v5-on-dark.svg')).read()
    return {p: re.search(r'<polygon id="%s" points="([^"]+)"' % p, svg).group(1) for p in PIECES}


def avatar_svg(geo, g0, g1, fills):
    off = 1024 * (1 - MARK_SCALE) / 2
    polys = ''.join('<polygon points="%s" fill="%s"/>' % (geo[p], fills[p]) for p in PIECES)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">'
            '<title>Cofferdam</title><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect width="1024" height="1024" fill="url(#g)"/>'
            '<g transform="translate(%.1f %.1f) scale(%.3f)">%s</g></svg>\n') % (g0, g1, off, off, MARK_SCALE, polys)


def main():
    c = json.load(open(P('dist', 'brand.resolved.json')))['colors']
    geo = geometry()
    fills = lambda prefix, th: {p: c[th][prefix + p] for p in PIECES}
    out = P('assets', 'github')
    os.makedirs(out, exist_ok=True)
    avatars = {}
    for th in ('light', 'dark'):
        avatars['avatar-enterprise-%s' % th] = avatar_svg(geo, c[th]['splash-gradient-from'], c[th]['splash-gradient-to'], fills('mark-', th))
        avatars['avatar-cofferdamdev-%s' % th] = avatar_svg(geo, c[th]['tile-mono-from'], c[th]['tile-mono-to'], fills('mark-mono-', th))

    prof = P('github', 'profile', 'assets')
    os.makedirs(prof, exist_ok=True)
    shutil.copyfile(P('assets', 'partners', 'base', 'Base_lockup_white.svg'), os.path.join(prof, 'base-lockup-white.svg'))
    shutil.copyfile(P('assets', 'partners', 'base', 'Base_lockup_black.svg'), os.path.join(prof, 'base-lockup-black.svg'))

    # The banner is the design-system cover, rendered with the same tokens and placeholders the build fills in.
    cover = open(P('components', 'Cover', 'preview.html')).read()
    polys = ''.join('<polygon class="m-%s" points="%s"/>' % (p, geo[p]) for p in PIECES)
    cover = cover.replace('{{mark-polygons}}', polys)
    cover = re.sub(r'\{\{asset:([^}]+)\}\}', lambda m: 'file://' + P(m.group(1)), cover)
    fonts = ''.join("@font-face{font-family:'%s';src:url(file://%s);font-weight:100 900}" % (f['family'], P(f['file']))
                    for f in json.load(open(P('tokens', 'tokens.json')))['type']['fonts'])
    css = open(P('dist', 'tokens.css')).read()

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, svg in avatars.items():
            open(os.path.join(out, name + '.svg'), 'w').write(svg)
            pg = b.new_page(viewport={'width': 1024, 'height': 1024})
            pg.set_content('<html><body style="margin:0">%s</body></html>' % svg)
            pg.screenshot(path=os.path.join(out, name + '.png'))
            pg.close()
        for th in ('light', 'dark'):
            # Rounded corners on a transparent page, so the banner sits cleanly on GitHub's own background.
            html = ('<!doctype html><html data-theme="%s"><head><meta charset="utf-8"><style>%s\n%s</style>%s'
                    '<style>html,body{background:transparent!important}.cover{border-radius:var(--radius-xxl)}</style></head>'
                    '<body style="margin:0">%s</body></html>') % (th, fonts, css, '', cover)
            tmp = P('github', '.banner.html')
            open(tmp, 'w').write(html)
            pg = b.new_page(viewport={'width': 960, 'height': 288}, device_scale_factor=2)
            pg.goto('file://' + tmp)
            pg.wait_for_timeout(500)
            pg.screenshot(path=os.path.join(prof, 'banner-%s.png' % th), omit_background=True)
            pg.close()
            os.remove(tmp)
        b.close()
    print('rendered 4 avatars (svg + png) and the profile banners')


if __name__ == '__main__':
    main()
