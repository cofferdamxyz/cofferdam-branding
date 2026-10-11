#!/usr/bin/env python3
"""Re-render the icon and splash previews in the current tokens.

    node scripts/build.mjs && python3 scripts/render-previews.py

Reads dist/brand.resolved.json, dist/tokens.css, components/bundle.js (+ lib/react*). Needs Playwright (Chromium),
Pillow and ffmpeg. Writes:
  assets/logos/v5/preview-light-dark-mono.png   light / dark / mono icon tiles
  assets/logos/v5/preview-sizes.png             the light tile at 512 / 120 / 60 / 40 px
  motion/splash/preview-keyframes.png           8 frames of the launch splash, light row over dark row
  motion/splash/cofferdam-splash-preview.mp4    light, 390×844 @ 30 fps   (+ -dark.mp4)
  motion/splash/cofferdam-splash-preview.gif    light, 195×422 @ 15 fps
The designer's originals are kept in */original-renders/.
"""
import json, os, re, shutil, subprocess, tempfile

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
PIECES = ['a-stem', 'a-arm', 'b-stem', 'b-arm']
STAGE = '#e8e8ec'


def geometry():
    svg = open(P('assets', 'logos', 'v5', 'cofferdam-mark-v5-on-dark.svg')).read()
    return {p: re.search(r'<polygon id="%s" points="([^"]+)"' % p, svg).group(1) for p in PIECES}


def tile_html(geo, size, ground_from, ground_to, fills, edge):
    polys = ''.join('<polygon points="%s" fill="%s"/>' % (geo[p], fills[p]) for p in PIECES)
    rim = ''.join('<polygon points="%s"/>' % geo[p] for p in PIECES)
    return (
        '<div class="tile" style="width:{s}px;height:{s}px;border-radius:{r}px;'
        'background:linear-gradient(135deg,{a},{b});box-shadow:inset 0 0 0 1px {e},inset 0 {hl}px 0 rgba(255,255,255,.16),0 {d}px {blur}px rgba(10,15,31,.16)">'
        '<svg viewBox="0 0 1024 1024" width="{s}" height="{s}"><g transform="translate(31 31) scale(.94)" style="filter:drop-shadow(0 18px 22px rgba(0,0,0,.22))">{p}</g>'
        '<g transform="translate(31 31) scale(.94)" fill="none" stroke="rgba(255,255,255,.38)" stroke-width="4">{rim}</g></svg></div>'
    ).format(s=size, r=size * 0.225, a=ground_from, b=ground_to, e=edge, hl=max(1, size // 256), d=max(1, size // 40), blur=max(2, size // 14), p=polys, rim=rim)


def page(body, extra_css=''):
    return ('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:%s}'
            '.row{display:flex;align-items:center}.tile{flex:none;overflow:hidden}%s</style></head><body>%s</body></html>') % (STAGE, extra_css, body)


def main():
    r = json.load(open(P('dist', 'brand.resolved.json')))
    c = r['colors']
    geo = geometry()
    fills = lambda prefix, th: {p: c[th][prefix + p] for p in PIECES}
    tiles = {
        'light': (c['light']['splash-gradient-from'], c['light']['splash-gradient-to'], fills('mark-', 'light'), 'rgba(255,255,255,.18)'),
        'dark': (c['dark']['splash-gradient-from'], c['dark']['splash-gradient-to'], fills('mark-', 'dark'), c['dark']['chain-tile-edge']),
        'mono': (c['light']['tile-mono-from'], c['light']['tile-mono-to'], fills('mark-mono-', 'light'), c['light']['chain-tile-edge']),
    }
    # Timeline from tokens/brand.json → motion.splash (same as splashMath.ts and the web replay).
    T = json.load(open(P('tokens', 'brand.json')))['motion']['splash']
    draw_end = T['start'] + 4 * T['dur'] + 3 * T['gap']          # last piece finished = settle starts
    hold_end = draw_end + T['bumpDur'] + T['hold']
    exit_start = hold_end + 500                                   # the web replay waits 500 ms for "app ready"
    total = exit_start + T['exitDur']
    piece_end = lambda i: T['start'] + i * (T['dur'] + T['gap']) + T['dur']
    piece_mid = lambda i: T['start'] + i * (T['dur'] + T['gap']) + T['dur'] // 2
    tmp = tempfile.mkdtemp()
    with sync_playwright() as pw:
        b = pw.chromium.launch()

        def shot(html, w, h, out, scale=1):
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
            pg.set_content(html)
            pg.screenshot(path=out)
            pg.close()

        # Icon tiles: light / dark / mono (same frame as the designer's 1616×552 sheet).
        body = '<div class="row" style="gap:20px;padding:20px">%s</div>' % ''.join(tile_html(geo, 512, *tiles[k]) for k in ('light', 'dark', 'mono'))
        shot(page(body), 1616, 552, P('assets', 'logos', 'v5', 'preview-light-dark-mono.png'))
        # Sizes: 512 / 120 / 60 / 40 (852×512).
        body = '<div class="row" style="gap:20px;height:512px;padding:0 0 0 10px">%s</div>' % ''.join(tile_html(geo, s, *tiles['light']) for s in (500, 120, 60, 40))
        shot(page(body), 852, 512, P('assets', 'logos', 'v5', 'preview-sizes.png'))

        # Splash: drive the web Splash (same timeline as splashMath.ts) on a virtual clock.
        lib = lambda f: open(P('components', 'lib', f)).read()
        tokens_css = open(P('dist', 'tokens.css')).read()
        clock = ('window.__cbs=[];window.requestAnimationFrame=function(cb){__cbs.push(cb);return __cbs.length};'
                 'window.cancelAnimationFrame=function(){};window.__step=function(t){var q=__cbs;__cbs=[];q.forEach(function(f){f(t)})};')
        app = ("const e=React.createElement,bar=(h,o)=>e('div',{style:{height:h,borderRadius:20,background:'var(--card)',"
               "boxShadow:'inset 0 0 0 1px var(--card-border)',opacity:o}});"
               "ReactDOM.createRoot(document.getElementById('r')).render(e(window.Cofferdam.Splash,{width:390,height:844,loop:false},"
               "e('div',{style:{height:56}}),bar(48,1),bar(120,1),bar(120,.7),bar(120,.45)));")
        frames = {}
        for th in ('light', 'dark'):
            html = ('<!doctype html><html data-theme="%s"><head><meta charset="utf-8"><style>%s\n%s\nhtml,body{margin:0;background:var(--bg)}'
                    '.cd-splash{border-radius:0!important;box-shadow:none!important}</style></head><body><div id="r"></div>'
                    '<script>%s</script><script>%s</script><script>%s</script><script>%s</script><script>%s</script></body></html>') % (
                th, tokens_css, open(P('components', 'bundle.css')).read(), clock, lib('react.production.min.js'),
                lib('react-dom.production.min.js'), open(P('components', 'bundle.js')).read(), app)
            pg = b.new_page(viewport={'width': 390, 'height': 844})
            pg.set_content(html)
            pg.wait_for_function('window.__cbs && window.__cbs.length > 0')
            pg.evaluate('window.__step(0)')
            d = os.path.join(tmp, th)
            os.makedirs(d)
            fps = 30
            n = int(total * fps / 1000) + 1
            for i in range(n):
                pg.evaluate('t => { window.__step(t); return new Promise(r => setTimeout(r, 0)); }', i * 1000 / fps)
                pg.screenshot(path=os.path.join(d, 'f%04d.png' % i))
            pg.close()
            frames[th] = (d, n)
        b.close()

    def mp4(th, out):
        d, _ = frames[th]
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(d, 'f%04d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', out], check=True)

    mp4('light', P('motion', 'splash', 'cofferdam-splash-preview.mp4'))
    mp4('dark', P('motion', 'splash', 'cofferdam-splash-preview-dark.mp4'))
    d, _ = frames['light']
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(d, 'f%04d.png'),
                    '-vf', 'fps=15,scale=195:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer',
                    P('motion', 'splash', 'cofferdam-splash-preview.gif')], check=True)

    # Keyframes: 8 moments (empty, each piece, bump, exit), light row over dark row.
    # 8 moments: native frame, A stem drawing, A stem done, A arm done, B stem done, settle peak, hold, mid-exit.
    ms = [0, piece_mid(0), piece_end(0), piece_end(1), piece_end(2), draw_end + T['bumpDur'] // 2, hold_end, exit_start + T['exitDur'] // 2]
    W, H, gap = 195, 422, 10
    sheet = Image.new('RGB', (gap + len(ms) * (W + gap), gap + 2 * (H + gap)), STAGE)
    for row, th in enumerate(('light', 'dark')):
        d, n = frames[th]
        for col, t in enumerate(ms):
            f = Image.open(os.path.join(d, 'f%04d.png' % min(n - 1, -(-t * 30 // 1000)))).convert('RGB').resize((W, H), Image.LANCZOS)
            sheet.paste(f, (gap + col * (W + gap), gap + row * (H + gap)))
    sheet.save(P('motion', 'splash', 'preview-keyframes.png'), optimize=True)
    shutil.rmtree(tmp)
    print('rendered icon previews, splash keyframes, mp4 (light, dark) and gif')


if __name__ == '__main__':
    main()
