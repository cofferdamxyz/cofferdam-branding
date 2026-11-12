#!/usr/bin/env python3
"""Render the social-network profile assets from the current tokens.

    node scripts/build.mjs && python3 scripts/render-social.py

Reads dist/tokens.css, tokens/tokens.json (fonts), social/x-header.html and the GitHub avatar
sources. Needs Playwright (Chromium); with uv: `uv run --with playwright python scripts/render-social.py`.
Writes:

  assets/social/x-header.png   X profile header, 1500x500, dark only (X shows one header in both themes)
  assets/social/x-avatar.png   X profile picture, 400x400: the colour icon tile, the same art as
                               assets/github/avatar-enterprise-light (circle-safe, X crops to a circle
                               or, for verified organisations, a rounded square)
"""
import json, os, re

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)


def page(theme, body):
    """A full document around a template: tokens, the brand fonts, the theme."""
    css = open(P('dist', 'tokens.css')).read()
    fonts = ''.join("@font-face{font-family:'%s';src:url(file://%s);font-weight:100 900}" % (f['family'], P(f['file']))
                    for f in json.load(open(P('tokens', 'tokens.json')))['type']['fonts'])
    body = re.sub(r'\{\{asset:([^}]+)\}\}', lambda m: 'file://' + P(m.group(1)), body)
    return ('<!doctype html><html data-theme="%s"><head><meta charset="utf-8"><style>%s\n%s</style></head>'
            '<body style="margin:0">%s</body></html>') % (theme, fonts, css, body)


def shoot(browser, html, size, out):
    # Loaded from a file, not set_content: an about:blank page cannot read the file:// fonts and textures.
    tmp = P('social', '.render.html')
    open(tmp, 'w').write(html)
    pg = browser.new_page(viewport={'width': size[0], 'height': size[1]})
    pg.goto('file://' + tmp)
    pg.wait_for_timeout(600)
    pg.screenshot(path=out)
    pg.close()
    os.remove(tmp)


def main():
    out = P('assets', 'social')
    os.makedirs(out, exist_ok=True)
    avatar_svg = open(P('assets', 'github', 'avatar-enterprise-light.svg')).read()
    # Resize the outer <svg> only; the tile's own <rect> carries the same attributes in viewBox units.
    avatar_svg = re.sub(r'(<svg[^>]*?)width="1024" height="1024"', r'\1width="400" height="400"', avatar_svg, count=1)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        shoot(b, page('dark', open(P('social', 'x-header.html')).read()), (1500, 500), os.path.join(out, 'x-header.png'))
        shoot(b, page('light', avatar_svg), (400, 400), os.path.join(out, 'x-avatar.png'))
        b.close()
    print('rendered assets/social/x-header.png and x-avatar.png')


if __name__ == '__main__':
    main()
