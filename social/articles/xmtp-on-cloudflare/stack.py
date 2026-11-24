"""The two architecture diagrams, drawn the stack-diagram way: official logos on white tiles, group boxes,
orthogonal arrows anchored to node boxes (github.com/caru-ini/stack-diagram, MIT; its template's markup,
geometry rules and icon fetcher). The theme is Cofferdam's: every colour and font below reads a brand
token and the whole drawing is greyscale: the only colour is in the logos. One line style means one thing
in every diagram of the article: a heavy white line is bytes carried without being read.

Canvas 880x660 (4:3, so a phone gives the image more room), rendered at 3200x2400. A node is its 60px
tile plus the text under it (132 wide, ~104 tall): horizontal edges join tile sides at tile mid-height,
vertical ones leave from the box bottom, never through the label. Those white edges are twice as heavy as
the grey ones, so the difference does not rest on tone alone. Logos are never recoloured; Cofferdam's
tile is its own light greyscale icon (the mono mark on near-white), so it sits with the other white tiles
and the accent stays the only blue.

icons/ holds the logos as fetched (icons/manifest.json names each source). They are their owners'
trademarks, used to name the services in a diagram.
"""
import base64, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
W, H = 880, 660
SCALE = 3200 / W
E = html.escape
MIME = {'svg': 'image/svg+xml', 'png': 'image/png'}
LEGEND = 'carried without being read'
ICON_DIRS = [os.path.join(HERE, 'icons')]  # another diagram set appends its own folder


def icon(name):
    for d in ICON_DIRS:
        for ext in ('svg', 'png'):
            p = os.path.join(d, name + '.' + ext)
            if os.path.exists(p):
                return 'data:%s;base64,%s' % (MIME[ext], base64.b64encode(open(p, 'rb').read()).decode())
    if name == 'cofferdam':
        p = os.path.join(ROOT, 'assets', 'github', 'avatar-cofferdamdev-light.svg')  # the light greyscale icon: the mono mark on its near-white tile
        return 'data:image/svg+xml;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    raise SystemExit('missing icon ' + name)


LOCKUP = 'file://' + os.path.join(ROOT, 'assets', 'logos', 'lockups', 'cofferdam-lockup-horizontal-white.svg')

CSS = '''
:root { --color-paper: var(--bg); --color-rule: #0e0f11; --color-rule-2: var(--border); --color-muted: var(--fg-muted);
  --color-neutral: var(--border-control); --color-ink: var(--fg); --color-accent: var(--fg);
  --color-graphite: var(--surface-2); --color-veil: rgba(0,0,0,.8); }
* { margin:0; padding:0; box-sizing:border-box; }
body { background: var(--color-paper); }
.canvas { position:relative; width:%dpx; height:%dpx; background: var(--color-paper); color: var(--color-ink);
  font-family: var(--font-sans);
  background-image: linear-gradient(var(--color-rule) 1px, transparent 1px), linear-gradient(90deg, var(--color-rule) 1px, transparent 1px);
  background-size: 22px 22px; background-position: -1px -1px; }
.ttl { position:absolute; left:36px; top:26px; font-size:31px; line-height:36px; font-weight:700; letter-spacing:-0.9px; }
.sub { position:absolute; left:36px; top:68px; font-size:15.5px; line-height:21px; font-weight:500; color: var(--fg-muted); }
.lock { position:absolute; left:24px; bottom:16px; height:30px; }
.url { position:absolute; right:36px; bottom:24px; font-family: var(--font-mono); font-size:12.5px; color: var(--fg-muted); }
.legend { position:absolute; left:0; right:0; bottom:24px; display:flex; justify-content:center; gap:26px;
  font-size:13px; font-weight:500; color: var(--fg-muted); }
.legend .sw { display:inline-block; width:30px; vertical-align:middle; margin-right:8px; border-top:2.8px solid var(--color-accent); }
.legend .sw.n { border-color: var(--color-neutral); border-top-width:1.4px; }
.group { position:absolute; border-radius: var(--radius-lg); border:1.5px solid var(--color-neutral); background: rgba(255,255,255,.035); }
.group.nested { border-style:dashed; background: rgba(255,255,255,.03); }
.g-label { position:absolute; top:11px; left:13px; display:flex; align-items:center; gap:7px; font-size:14px; font-weight:600;
  color: var(--fg-muted); white-space:nowrap; }
.g-label img { width:17px; height:17px; }
.node { position:absolute; width:132px; text-align:center; }
.tile { width:60px; height:60px; margin:0 auto; border-radius: var(--radius-md); background:#fff; border:1px solid var(--color-rule-2);
  display:grid; place-items:center; }
.tile img { width:36px; height:36px; object-fit:contain; }
.tile.wide img { width:48px; }
.tile.icon { background:none; overflow:hidden; }
.tile.icon img { width:60px; height:60px; }
.node .name { font-weight:600; font-size:16.5px; line-height:21px; margin-top:7px; white-space:nowrap; }
.node .role { font-family: var(--font-mono); font-size:12px; line-height:16px; color: var(--color-muted); margin-top:1px; white-space:nowrap; }
.node .name, .node .role { display:flex; justify-content:center; }
.node .name span, .node .role span { background: var(--color-veil); padding:0 4px; border-radius:3px; }
svg.edges { position:absolute; inset:0; pointer-events:none; }
.e { stroke: var(--color-accent); stroke-width:2.8; fill:none; }
.n { stroke: var(--color-neutral); stroke-width:1.4; fill:none; }
.el { font-family: var(--font-mono); font-size:12.5px; fill: var(--fg-muted); paint-order:stroke; stroke: var(--color-paper);
  stroke-width:5px; stroke-linejoin:round; }
.el.a { fill: var(--color-accent); }
.el.big { font-family: var(--font-sans); font-size:15.5px; font-weight:600; fill: var(--fg); }
.el.sub2 { font-family: var(--font-sans); font-size:14px; font-weight:500; }
.span-t { position:absolute; left:44px; font-size:15.5px; font-weight:500; color: var(--fg-muted); white-space:nowrap; }
.span-t b { color: var(--fg); font-weight:700; font-size:17px; margin-right:9px; }
.eyebrow { position:absolute; left:36px; font-size:12px; letter-spacing:.2em; color: var(--fg-muted); }
''' % (W, H)

DEFS = ('<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" fill="context-stroke"/></marker></defs>')


def node(cx, top, ic, name, role, cls=''):
    return ('<div class="node" style="left:%dpx;top:%dpx"><div class="tile %s"><img src="%s" alt=""></div>'
            '<div class="name"><span>%s</span></div><div class="role"><span>%s</span></div></div>') % (cx - 66, top, cls, icon(ic), E(name), E(role))


def group(left, top, w, h, label, ic=None, cls=''):
    img = '<img src="%s" alt="">' % icon(ic) if ic else ''
    return '<div class="group %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><div class="g-label">%s%s</div></div>' % (cls, left, top, w, h, img, E(label))


def edge(d, cls='n', start=False, head=True):
    return '<path class="%s" d="%s"%s%s/>' % (cls, d, ' marker-end="url(#ar)"' if head else '', ' marker-start="url(#ar)"' if start else '')


def el(x, y, s, cls='', anchor='middle'):
    return '<text class="el %s" x="%s" y="%s" text-anchor="%s">%s</text>' % (cls, x, y, anchor, E(s))


def canvas(title, sub, groups, edges, nodes, extra='', legend=None, plain='ordinary call', url='cofferdam.xyz'):
    lg = ('<div class="legend"><span><span class="sw"></span>%s</span>'
          '<span><span class="sw n"></span>%s</span></div>') % (E(legend or LEGEND), E(plain))
    return ('<div class="canvas"><div class="ttl">%s</div><div class="sub">%s</div>%s'
            '<svg class="edges" width="%d" height="%d" viewBox="0 0 %d %d">%s%s</svg>%s%s%s'
            '<img class="lock" src="%s" alt=""><div class="url">%s</div></div>') % (
        E(title), E(sub), ''.join(groups), W, H, W, H, DEFS, ''.join(edges), ''.join(nodes), extra, lg, LOCKUP, E(url))


def d_architecture():
    """The map: nine nodes, two rows. Caddy is in the pipe diagram; the Durable Object is named under the backend."""
    r1, r2 = 190, 430            # tile tops; mid = +30, box bottom = +104
    c = [80, 250, 410, 570, 786]
    groups = [group(160, 130, 524, 428, 'Cloudflare', 'cloudflare'),
              group(702, 130, 168, 190, 'PlanetScale', 'planetscale_dark')]
    nodes = [node(c[0], r1, 'cofferdam', 'Phone', 'Cofferdam app', 'icon'),
             node(c[1], r1, 'cloudflare', 'Spectrum', 'inbound TCP'),
             node(c[2], r1, 'workers', 'Worker', 'connect()'),
             node(c[3], r1, 'xmtp', 'XMTP backend', 'Durable Object + Container', 'wide'),
             node(c[4], r1, 'postgres', 'Postgres', 'ciphertext only'),
             node(c[0], r2, 'bell', 'Apple / Google', 'push delivery'),
             node(c[1], r2, 'cloudflare', 'R2', 'encrypted files'),
             node(c[2], r2, 'workers', 'Push relay', 'stateless Worker'),
             node(c[3], r2, 'workers', 'Cleanup', 'cron')]
    edges = [edge('M116 220 H214', 'e'), el(164, 210, 'TLS', 'a'),
             edge('M286 220 H374', 'e'),
             edge('M446 220 H534', 'e'),
             edge('M606 220 H750'), el(696, 210, 'direct'),
             edge('M102 300 V374 H250 V424', 'e'), el(180, 365, 'encrypted upload', 'a'),
             edge('M570 304 V384 H410 V424'), el(490, 375, 'signed webhook'),
             edge('M410 540 V576 H80 V542'), el(245, 594, 'alert + sealed hint'),
             edge('M58 424 V302'), el(50, 368, 'wake', anchor='end'),
             edge('M606 460 H786 V302'), el(702, 450, 'via Hyperdrive')]
    return canvas('Private messaging on Cloudflare', 'XMTP 8 behind inbound TCP, with a container, a few small Workers and Postgres.', groups, edges, nodes)


def d_pipe():
    r = 312
    xs = [74, 214, 354, 494, 646, 786]
    groups = [group(564, 252, 306, 180, 'Container', cls='nested')]
    nodes = [node(xs[0], r, 'cofferdam', 'Phone', 'Cofferdam app', 'icon'),
             node(xs[1], r, 'cloudflare', 'Spectrum', 'inbound TCP'),
             node(xs[2], r, 'workers', 'Worker', 'connect(socket)'),
             node(xs[3], r, 'cloudflare', 'Durable Object', 'getTcpPort()'),
             node(xs[4], r, 'caddy', 'Caddy', 'TLS ends here'),
             node(xs[5], r, 'xmtp', 'XMTP backend', 'gRPC', 'wide')]
    edges = [edge('M%d 342 H%d' % (xs[i] + 36, xs[i + 1] - 36), 'e' if i < 4 else 'n') for i in range(5)]
    edges += [edge('M44 158 H858', 'e', start=True), el(852, 181, 'to the other phone', 'a', 'end'),
              edge('M44 220 H676', 'e', start=True),
              # what each hop can read: one bracket under the three hops that only move bytes
              edge('M152 494 V502 H556 V494', 'n', head=False),
              el(xs[0], 532, 'everything', 'big'), el(xs[0], 554, 'it is your phone', 'sub2'),
              el(354, 532, 'nothing: TLS bytes', 'big'), el(354, 554, 'Spectrum, the Worker and the object only move them', 'sub2'),
              el(xs[4] - 12, 532, 'gRPC frames', 'big'), el(xs[4] - 12, 554, 'around ciphertext', 'sub2'),
              el(xs[5] - 2, 532, 'topic ids, sizes, timing', 'big'), el(xs[5] - 2, 554, 'never a message', 'sub2')]
    extra = ['<div class="span-t" style="top:122px"><b>MLS</b>phone to phone. No machine on this page holds a key.</div>',
             '<div class="span-t" style="top:184px"><b>TLS</b>phone to Caddy.</div>',
             '<div class="eyebrow" style="top:462px">WHAT EACH HOP CAN READ</div>']
    return canvas('One pipe, opened once', 'Where TLS ends, and what each hop can read on the way to the backend.',
                  groups, edges, nodes, ''.join(extra))
