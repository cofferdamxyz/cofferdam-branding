#!/usr/bin/env python3
"""Render the diagrams of the X article "Private messaging on Cloudflare" from the brand tokens.

    node scripts/build.mjs && uv run --with playwright python social/articles/xmtp-on-cloudflare/render.py

Reads dist/tokens.css and the brand fonts, like scripts/render-social.py. Writes PNGs beside this file:
the cover (1500x600, X's 5:2 article cover, at 2x) and five 4:3 diagrams at 3200x2400. 4:3 because a
phone gives a taller image more room, and the type is sized to be read there. Diagrams 1 and 2 are in
stack.py (logos on tiles, the stack-diagram way); 3 to 5 are drawn here on a 1200x900 canvas.

rules: dark only, greyscale throughout (the only colour is in the logos), Geist and Geist Mono. A heavy
       white line or a lighter card marks one thing in every diagram, with the same legend line: bytes
       carried without being read. Ordinary calls are thin and grey. One name per thing: Phone, Push relay, XMTP backend, Apple / Google.
       Single-ink lockup, bottom left.
"""
import html, json, os

from playwright.sync_api import sync_playwright

import stack

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
P = lambda *a: os.path.join(ROOT, *a)
W, H = 1200, 900
LOCKUP = 'file://' + P('assets', 'logos', 'lockups', 'cofferdam-lockup-horizontal-white.svg')
E = html.escape

DEFS = '''<defs>
<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="var(--border-control)"/></marker>
<marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="var(--fg)"/></marker>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0 H0 V30" fill="none" stroke="#0e0f11" stroke-width="1.25"/></pattern>
</defs>'''


def text(x, y, s, size=20, weight=500, fill='var(--fg-muted)', mono=False, anchor='start', spacing=None, halo=False):
    fam = 'var(--font-mono)' if mono else 'var(--font-sans)'
    extra = ' letter-spacing="%s"' % spacing if spacing else ''
    if halo:
        extra += ' paint-order="stroke" stroke="var(--bg)" stroke-width="7" stroke-linejoin="round"'
    return '<text x="%s" y="%s" font-family=\'%s\' font-size="%s" font-weight="%s" fill="%s" text-anchor="%s"%s>%s</text>' % (
        x, y, fam, size, weight, fill, anchor, extra, E(s))


def box(x, y, w, h, title, lines=(), mono=(), accent=False, pad=20, tsize=24, lsize=20):
    """A card: title, then muted lines, then mono lines."""
    stroke = 'var(--fg-muted)' if accent else 'var(--border)'
    fill = 'var(--border)' if accent else 'var(--card)'
    out = ['<rect x="%s" y="%s" width="%s" height="%s" rx="16" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, y, w, h, fill, stroke)]
    ty = y + pad + tsize - 2
    out.append(text(x + pad, ty, title, tsize, 600, 'var(--fg)'))
    ty += 8
    for s in lines:
        ty += lsize + 8
        out.append(text(x + pad, ty, s, lsize))
    for s in mono:
        ty += lsize + 8
        out.append(text(x + pad, ty, s, lsize - 2, 500, 'var(--fg-muted)', mono=True))
    return ''.join(out)


def tile(x, y, name, size=46, cls=''):
    """A logo on a white tile, as in stack.py; cls 'icon' is Cofferdam's light app icon, which is its own tile."""
    if cls == 'icon':
        return ('<clipPath id="c%s%s"><rect x="%s" y="%s" width="%s" height="%s" rx="%s"/></clipPath>'
                '<image href="%s" x="%s" y="%s" width="%s" height="%s" clip-path="url(#c%s%s)"/>') % (
            x, y, x, y, size, size, size * 0.2, stack.icon(name), x, y, size, size, x, y)
    pad = size * (0.14 if cls == 'wide' else 0.2)
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="var(--border)"/>'
            '<image href="%s" x="%s" y="%s" width="%s" height="%s"/>') % (
        x, y, size, size, size * 0.2, '#fff',
        stack.icon(name), x + pad, y + pad, size - 2 * pad, size - 2 * pad)


def line(points, accent=False, head=True):
    d = 'M' + ' L'.join('%s,%s' % p for p in points)
    col = 'var(--fg)' if accent else 'var(--border-control)'
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"%s/>' % (
        d, col, 4 if accent else 2, ' marker-end="url(#%s)"' % ('b' if accent else 'a') if head else '')


def label(x, y, s, anchor='middle', size=18):
    return text(x, y, s, size, 500, 'var(--fg-muted)', mono=True, anchor=anchor)


def frame(title, sub, body, legend=True, url='cofferdam.xyz'):
    """legend: True for the article's line, a string for another diagram set's, False for none."""
    foot = H - 44
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H), DEFS,
           '<rect width="100%" height="100%" fill="var(--bg)"/><rect width="100%" height="100%" fill="url(#grid)"/>',
           text(48, 80, title, 42, 700, 'var(--fg)', spacing='-1.2px'),
           text(48, 118, sub, 21, 500),
           body,
           '<image href="%s" x="32" y="%d" width="170" height="41"/>' % (LOCKUP, foot - 28),
           text(W - 48, foot, url, 17, 500, mono=True, anchor='end')]
    if legend:
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--fg)" stroke-width="4" stroke-linecap="round"/>' % (W / 2 - 150, foot - 6, W / 2 - 108, foot - 6))
        out.append(text(W / 2 - 96, foot, legend if isinstance(legend, str) else stack.LEGEND, 18, 500))
    out.append('</svg>')
    return ''.join(out)


# 3. The database ----------------------------------------------------------------------------------
def d_database():
    b = []
    b.append(box(48, 156, 532, 176, 'XMTP backend', ['Keeps state on its connections: a leader', 'lock, timeouts, migrations at boot.'], ['needs a direct connection']))
    b.append(box(620, 156, 532, 176, 'Cleanup Worker', ['A cron job. Short transactions only,', 'with a role that only reads and deletes.'], ['pooling is fine here']))
    b.append(box(120, 408, 420, 112, 'Postgres', ['on PlanetScale']))
    b.append(box(680, 408, 420, 112, 'Hyperdrive', ['pooled connections, caching off']))
    b.append(tile(516, 172, 'xmtp', cls='wide') + tile(1088, 172, 'workers') + tile(476, 424, 'postgres') + tile(1036, 424, 'cloudflare'))
    b.append(line([(314, 334), (314, 404)]))
    b.append(label(332, 376, 'direct connection', anchor='start'))
    b.append(line([(886, 334), (886, 404)]))
    b.append(line([(678, 464), (544, 464)]))
    # retention: the mechanism, not our numbers
    b.append(text(48, 584, 'HOW LONG CIPHERTEXT STAYS', 15, 500, spacing='0.2em'))
    y = 646
    b.append('<rect x="48" y="%s" width="560" height="40" rx="20" fill="var(--border)" stroke="var(--border-control)" stroke-width="1.5"/>' % (y - 20))
    b.append(text(70, y + 7, 'kept for the retention you set', 20, 600, 'var(--fg)'))
    b.append('<rect x="614" y="%s" width="170" height="40" rx="20" fill="none" stroke="var(--border-control)" stroke-width="1.5" stroke-dasharray="3 6" stroke-linecap="round"/>' % (y - 20))
    b.append(text(699, y + 7, 'a grace period', 19, 500, anchor='middle'))
    b.append(line([(792, y), (838, y)]))
    b.append(text(852, y + 7, 'deleted by the Worker', 20, 600, 'var(--fg)'))
    b.append(text(48, 706, 'Retention is set per kind: messages, welcomes, key packages.', 20))
    b.append(text(48, 752, 'Never deleted:', 20, 600, 'var(--fg)'))
    b.append(text(196, 752, 'commits and identity updates. XMTP needs them to decrypt.', 20))
    b.append(text(48, 784, 'The backend only stamps an expiry on each row. The Worker is what deletes.', 20))
    return frame('Two doors to one database', 'The backend connects directly. Only the cleanup job uses Hyperdrive.', ''.join(b), legend=False)


# 4. Push ------------------------------------------------------------------------------------------
def d_push():
    b = []
    lanes = [(170, 'Phone', 'cofferdam', 'icon'), (470, 'Push relay', 'workers', ''), (770, 'XMTP backend', 'xmtp', 'wide'), (1030, 'Apple / Google', 'bell', '')]
    for x, t, ic, cls in lanes:
        b.append('<rect x="%d" y="160" width="232" height="60" rx="16" fill="var(--card)" stroke="var(--border)" stroke-width="1.5"/>' % (x - 116))
        b.append(tile(x - 106, 169, ic, 42, cls))
        b.append(text(x + 24, 198, t, 22, 600, 'var(--fg)', anchor='middle'))
        b.append('<line x1="%d" y1="220" x2="%d" y2="712" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="3 7" stroke-linecap="round"/>' % (x, x))
    steps = [(170, 470, 'seal my device token', False),
             (470, 170, 'a sealed delivery URL', True),
             (170, 770, 'register the sealed URL as my push channel', True),
             (770, 470, 'signed webhook', False),
             (470, 1030, 'an alert, and a hint they cannot read', True),
             (1030, 170, 'the phone wakes, fetches and decrypts the message itself', True)]
    for i, (x1, x2, s, acc) in enumerate(steps):
        y = 300 + i * 78
        d = 1 if x2 > x1 else -1
        b.append(line([(x1 + 4 * d, y), (x2 - 5 * d, y)], accent=acc))
        lx = min(x1, x2) + 18
        b.append('<circle cx="%d" cy="%d" r="15" fill="var(--bg)" stroke="var(--border-control)" stroke-width="1.5"/>' % (lx + 15, y - 28))
        b.append(text(lx + 15, y - 21.5, str(i + 1), 17, 600, 'var(--fg)', anchor='middle'))
        b.append(text(lx + 40, y - 21, s, 21, 500, 'var(--fg)', halo=True))
    notes = [(170, ['opens the hint,', 'writes the notification']), (470, ['stores nothing,', 'logs nothing']),
             (770, ['its database never holds', 'a device token']), (1030, ['never see which', 'conversation it was'])]
    for x, ls in notes:
        for j, s in enumerate(ls):
            b.append(text(x, 748 + j * 27, s, 19.5, 500, anchor='middle'))
    return frame('Push without a phone book', 'The backend never holds a device token. Apple and Google never see the conversation.', ''.join(b))


# 5. Three things that travel ----------------------------------------------------------------------
def d_lifecycle():
    b = []
    lanes = [
        ('A message', 'optimistic, like any good chat app', [
            ('Write locally', ['saved on the phone,', 'shown as sending'], False),
            ('Publish', ['gRPC to the backend,', 'as MLS ciphertext'], True),
            ('Stream', ["the other phone's open", 'stream delivers it'], True),
            ('Expire', ['deleted once retention', 'and a grace have passed'], False)]),
        ('A read receipt', "XMTP's standard content type", [
            ('Open the thread', ['someone wrote since', 'the last receipt'], False),
            ('Send one receipt', ['an encrypted message', 'that never pushes'], True),
            ('Mark as read', ['hidden from the thread;', 'lines show as read'], False)]),
        ('An attachment', 'a large file goes beside the chat', [
            ('Encrypt', ['on the phone, a fresh', 'key for each file'], False),
            ('Upload ciphertext', ['to R2, named by its', 'own SHA-256'], True),
            ('Send the pointer', ['URL, key and digest,', 'inside the message'], True),
            ('Expire', ['a lifecycle rule that', 'matches retention'], False)]),
    ]
    for i, (t, sub, chips) in enumerate(lanes):
        y = 156 + i * 214
        b.append(text(48, y + 28, t, 27, 700, 'var(--fg)', spacing='-0.4px'))
        b.append(text(1152, y + 28, sub, 20, 500, anchor='end'))
        for k, (ct, cl, acc) in enumerate(chips):
            x = 48 + k * 282
            b.append(box(x, y + 46, 258, 122, ct, cl, accent=acc, pad=18, tsize=22, lsize=19))
            if k < len(chips) - 1:
                b.append(line([(x + 258, y + 107), (x + 280, y + 107)]))
    return frame('Three things that travel', 'A message, a read receipt and an attachment, from one phone to the other.', ''.join(b))


# Cover --------------------------------------------------------------------------------------------
def d_cover():
    w, h = 1500, 600
    tex = 'file://' + P('assets', 'textures', 'obsidian.webp')
    return ('''<div style="position:relative;width:%dpx;height:%dpx;overflow:hidden;background:var(--bg);color:var(--fg);font-family:var(--font-sans)">
<div style="position:absolute;inset:0;background:url('%s') center/cover;opacity:var(--opacity-texture-dark);-webkit-mask-image:linear-gradient(90deg,rgba(0,0,0,.2) 0%%,rgba(0,0,0,.55) 45%%,#000 85%%)"></div>
<img src="%s" style="position:absolute;left:74px;top:56px;height:44px">
<div style="position:absolute;left:96px;top:176px">
<p style="margin:0;font-size:92px;line-height:1;font-weight:700;letter-spacing:-0.03em">Private messaging<br>on Cloudflare.</p>
<p style="margin:34px 0 0;font-size:28px;line-height:38px;font-weight:500;color:var(--fg-muted);max-width:900px">XMTP 8 on Workers, Containers and inbound TCP,<br>with Postgres on PlanetScale and a server that stays blind.</p>
</div>
<p style="position:absolute;left:96px;bottom:44px;margin:0;font-family:var(--font-mono);font-size:20px;letter-spacing:.02em;color:var(--fg-muted)">cofferdam.xyz</p>
</div>''' % (w, h, tex, LOCKUP))


def page(body, extra_css=''):
    css = open(P('dist', 'tokens.css')).read()
    fonts = ''.join("@font-face{font-family:'%s';src:url(file://%s);font-weight:100 900}" % (f['family'], P(f['file']))
                    for f in json.load(open(P('tokens', 'tokens.json')))['type']['fonts'])
    return ('<!doctype html><html data-theme="dark"><head><meta charset="utf-8"><style>%s\n%s\nsvg{display:block}\n%s</style></head>'
            '<body style="margin:0;background:#000">%s</body></html>') % (fonts, css, extra_css, body)


def main():
    s = 3200 / W
    jobs = [('00-cover', page(d_cover()), (1500, 600), 2),
            ('01-architecture', page(stack.d_architecture(), stack.CSS), (stack.W, stack.H), stack.SCALE),
            ('02-pipe', page(stack.d_pipe(), stack.CSS), (stack.W, stack.H), stack.SCALE),
            ('03-database', page(d_database()), (W, H), s), ('04-push', page(d_push()), (W, H), s),
            ('05-lifecycle', page(d_lifecycle()), (W, H), s)]
    tmp = os.path.join(HERE, '.render.html')
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='chrome')  # the installed Chrome: no browser download
        for name, doc, size, scale in jobs:
            open(tmp, 'w').write(doc)
            pg = br.new_page(viewport={'width': size[0], 'height': size[1]}, device_scale_factor=scale)
            pg.goto('file://' + tmp)
            pg.wait_for_timeout(500)
            pg.screenshot(path=os.path.join(HERE, name + '.png'))
            pg.close()
        br.close()
    os.remove(tmp)
    print('rendered', ', '.join(j[0] for j in jobs))


if __name__ == '__main__':
    main()
