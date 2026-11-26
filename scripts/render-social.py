#!/usr/bin/env python3
"""Render the social-network profile assets from the current tokens.

    node scripts/build.mjs && python3 scripts/render-social.py
    python3 scripts/render-social.py x-thread-end        # only the pictures named

Reads dist/tokens.css, tokens/tokens.json (fonts), social/x-header.html, social/x-thread-end.html and
the GitHub avatar sources. Needs Playwright (Chromium); with uv: `uv run --with playwright python scripts/render-social.py`.
Writes:

  assets/social/x-header.png   X profile header, 1500x500, dark only (X shows one header in both themes)
  assets/social/x-avatar.png   X profile picture, 400x400: the colour icon tile, the same art as
                               assets/github/avatar-enterprise-light (circle-safe, X crops to a circle
                               or, for verified organisations, a rounded square)
  assets/social/x-thread-end.png  the picture that closes a thread, 1600x900 at 2x (3200x1800), dark only
"""
import json, os, re, sys

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


def shoot(browser, html, size, out, scale=1):
    # Loaded from a file, not set_content: an about:blank page cannot read the file:// fonts and textures.
    tmp = P('social', '.render.html')
    open(tmp, 'w').write(html)
    pg = browser.new_page(viewport={'width': size[0], 'height': size[1]}, device_scale_factor=scale)
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
    template = lambda name: open(P('social', name + '.html')).read()
    jobs = {'x-header': (page('dark', template('x-header')), (1500, 500), 1),
            'x-avatar': (page('light', avatar_svg), (400, 400), 1),
            'x-thread-end': (page('dark', template('x-thread-end')), (1600, 900), 2)}
    names = sys.argv[1:] or list(jobs)
    unknown = [n for n in names if n not in jobs]
    if unknown:
        sys.exit('no such picture: %s (known: %s)' % (', '.join(unknown), ', '.join(jobs)))
    with sync_playwright() as pw:
        try:
            b = pw.chromium.launch()
        except Exception:
            b = pw.chromium.launch(channel='chrome')  # the installed Chrome, when Playwright's own is not downloaded
        for n in names:
            html, size, scale = jobs[n]
            shoot(b, html, size, os.path.join(out, n + '.png'), scale)
        b.close()
    print('rendered', ', '.join('assets/social/%s.png' % n for n in names))

if __name__ == '__main__':
    main()
