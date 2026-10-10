#!/usr/bin/env python3
"""Generate the v5 single-colour marks and the Cofferdam lockups from tokens + the official geometry.

    python3 scripts/make-logos.py

Reads:  tokens/tokens.json (mark-*, mark-mono-*, fg), assets/logos/v5/cofferdam-mark-v5-on-dark.svg (geometry),
        fonts/Geist-Variable-latin.woff2 (wordmark outlines, instanced at wght 700).
Writes: assets/logos/v5/cofferdam-mark-v5-black.svg, cofferdam-mark-v5-mono.svg, cofferdam-mark-v5-mono-on-dark.svg
        assets/logos/lockups/cofferdam-lockup-{horizontal,stacked}-{on-dark,on-light,white,black}.svg, wordmark.json

Needs fontTools (and brotli for woff2). The wordmark is outlined, so the SVGs need no font.
Lockup geometry (all relative to the wordmark cap height C, Geist 700, tracking -0.03em):
  horizontal  mark height 1.4C, centred on the cap height; gap 0.5C; clear space 0.5C on every side
  stacked     mark height 3.2C, centred over the wordmark; gap 0.6C; clear space 0.5C on every side
"""
import json, os, re, sys

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
PIECES = ['a-stem', 'a-arm', 'b-stem', 'b-arm']
# Trimmed bounds of the 1024 mark geometry (the canvas padding is the mark's own clear space).
MX0, MY0, MX1, MY1 = 126.3, 176.0, 897.7, 848.0
TRACK = -0.03
WORD = 'Cofferdam'


def tokens():
    t = json.load(open(P('tokens', 'tokens.json')))
    return {x['name']: x['value'] for x in t['color']['tokens']}


def geometry():
    svg = open(P('assets', 'logos', 'v5', 'cofferdam-mark-v5-on-dark.svg')).read()
    out = {}
    for pid in PIECES:
        m = re.search(r'<polygon id="%s" points="([^"]+)"' % pid, svg)
        if not m:
            sys.exit('geometry: %s not found' % pid)
        out[pid] = m.group(1)
    return out


def kern_lookup(font):
    gpos = font['GPOS'].table if 'GPOS' in font else None

    def kern(a, b):
        if not gpos:
            return 0
        for fr in gpos.FeatureList.FeatureRecord:
            if fr.FeatureTag != 'kern':
                continue
            for li in fr.Feature.LookupListIndex:
                lk = gpos.LookupList.Lookup[li]
                for st in lk.SubTable:
                    if lk.LookupType == 9:
                        st = st.ExtSubTable
                    if getattr(st, 'LookupType', 2) != 2 or not hasattr(st, 'Coverage'):
                        continue
                    cov = st.Coverage.glyphs
                    if a not in cov:
                        continue
                    if st.Format == 1:
                        for pv in st.PairSet[cov.index(a)].PairValueRecord:
                            if pv.SecondGlyph == b and pv.Value1 is not None:
                                return getattr(pv.Value1, 'XAdvance', 0) or 0
                    else:
                        c1 = st.ClassDef1.classDefs.get(a, 0)
                        c2 = st.ClassDef2.classDefs.get(b, 0)
                        v = st.Class1Record[c1].Class2Record[c2].Value1
                        if v is not None and getattr(v, 'XAdvance', 0):
                            return v.XAdvance
        return 0

    return kern


def wordmark():
    """Return (path d in font units, y-down, baseline at 0), ink bounds, cap height."""
    font = instancer.instantiateVariableFont(TTFont(P('fonts', 'Geist-Variable-latin.woff2')), {'wght': 700})
    upm = font['head'].unitsPerEm
    cap = font['OS/2'].sCapHeight
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font['hmtx']
    kern = kern_lookup(font)
    names = [cmap[ord(c)] for c in WORD]
    x, parts = 0.0, []
    bp = BoundsPen(gs)
    for i, n in enumerate(names):
        pen = SVGPathPen(gs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
        gs[n].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        gs[n].draw(TransformPen(bp, (1, 0, 0, -1, x, 0)))
        parts.append(pen.getCommands())
        if i + 1 < len(names):
            x += hmtx[n][0] + kern(n, names[i + 1]) + TRACK * upm
    return ' '.join(parts), bp.bounds, cap


def seal(fills, p):
    # Single ink: a same-colour hairline closes the anti-aliasing seams between the pieces.
    return ' stroke="%s" stroke-width="6" stroke-linejoin="round"' % fills[p] if len(set(fills.values())) == 1 else ''


def mark_group(geo, fills, tx, ty, scale):
    polys = ''.join('<polygon points="%s" fill="%s"%s/>' % (geo[p], fills[p], seal(fills, p)) for p in PIECES)
    return '<g transform="translate(%.2f %.2f) scale(%.5f) translate(%.1f %.1f)">%s</g>' % (tx, ty, scale, -MX0, -MY0, polys)


def svg(w, h, body, title='Cofferdam'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f" role="img">'
            '<title>%s</title>%s</svg>\n') % (w, h, w, h, title, body)


def main():
    tk = tokens()
    geo = geometry()
    tone = lambda prefix, theme: {p: tk['%s%s' % (prefix, p)][theme] for p in PIECES}
    one = lambda c: {p: c for p in PIECES}

    v5 = P('assets', 'logos', 'v5')
    full = lambda fills: svg(1024, 1024, ''.join('<polygon id="%s" points="%s" fill="%s"%s/>' % (p, geo[p], fills[p], seal(fills, p)) for p in PIECES))
    open(os.path.join(v5, 'cofferdam-mark-v5-black.svg'), 'w').write(full(one('#000000')))
    open(os.path.join(v5, 'cofferdam-mark-v5-mono.svg'), 'w').write(full(tone('mark-mono-', 'light')))
    open(os.path.join(v5, 'cofferdam-mark-v5-mono-on-dark.svg'), 'w').write(full(tone('mark-mono-', 'dark')))

    d, (bx0, by0, bx1, by1), C = wordmark()
    ww = bx1 - bx0
    mw_per_h = (MX1 - MX0) / (MY1 - MY0)
    pad = 0.5 * C
    variants = {
        'on-dark': (tone('mark-', 'dark'), '#ffffff'),
        'on-light': (tone('mark-mono-', 'light'), tk['fg']['light']),
        'white': (one('#ffffff'), '#ffffff'),
        'black': (one('#000000'), '#000000'),
    }
    out = P('assets', 'logos', 'lockups')
    os.makedirs(out, exist_ok=True)
    # The wordmark outline for components/bundle.js (CofferdamLockup) — font units, y-down, baseline at 0.
    json.dump({'d': d, 'x0': round(bx0, 1), 'x1': round(bx1, 1), 'cap': C}, open(os.path.join(out, 'wordmark.json'), 'w'))
    for name, (fills, ink) in variants.items():
        # horizontal
        mh = 1.4 * C
        s = mh / (MY1 - MY0)
        mw = mh * mw_per_h
        gap = 0.5 * C
        H = mh + 2 * pad
        W = pad + mw + gap + ww + pad
        cap_top = pad + (mh - C) / 2  # cap height centred on the mark
        text = '<path transform="translate(%.2f %.2f)" fill="%s" d="%s"/>' % (pad + mw + gap - bx0, cap_top + C, ink, d)
        open(os.path.join(out, 'cofferdam-lockup-horizontal-%s.svg' % name), 'w').write(
            svg(W, H, mark_group(geo, fills, pad, pad, s) + text))
        # stacked
        mh = 3.2 * C
        s = mh / (MY1 - MY0)
        mw = mh * mw_per_h
        gap = 0.6 * C
        W = max(mw, ww) + 2 * pad
        H = pad + mh + gap + C + pad  # no descenders in "Cofferdam"
        text = '<path transform="translate(%.2f %.2f)" fill="%s" d="%s"/>' % ((W - ww) / 2 - bx0, pad + mh + gap + C, ink, d)
        open(os.path.join(out, 'cofferdam-lockup-stacked-%s.svg' % name), 'w').write(
            svg(W, H, mark_group(geo, fills, (W - mw) / 2, pad, s) + text))
    print('marks: black, mono, mono-on-dark · lockups: horizontal/stacked × %s · cap %d, word %.0f' % (', '.join(variants), C, ww))


if __name__ == '__main__':
    main()
