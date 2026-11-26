#!/usr/bin/env python3
"""Generate Lockkeeper's mark and lockups (github.com/cofferdamxyz/lockkeeper).

    uv run --with fonttools --with brotli python scripts/make-lockkeeper-logo.py

Writes: assets/logos/lockkeeper/lockkeeper-mark-{white,black}.svg
        assets/logos/lockkeeper/lockkeeper-lockup-horizontal-{white,black}.svg

The mark is the lock chamber: an L (one wall and the floor) holding one bar, the water level. An L
for Lockkeeper, drawn in the Cofferdam mark's vocabulary: one heavy rounded stroke, the same lean,
single ink only. It has no toned or colour version: Lockkeeper is a tool of Cofferdam's, not a
second brand, and where the two appear together the Cofferdam mark is the one that carries tone.

Geometry, on the 1024 canvas of the Cofferdam mark: stroke 152, every outer corner rounded at 50
(soft squares, as the Cofferdam mark's ends are), the inside corner square; wall from y 196 to 828 at x 252, floor to x 828, level bar at y 536
from x 512 to 828; then leaned 10 degrees (the Cofferdam stems' lean) and scaled to 0.94 about the
centre, which keeps one-eighth of the canvas clear on every side. Curves are written as polygons,
as in the Cofferdam mark, so the files need no transform and no stroke.

The lockup follows the Cofferdam lockup's rules (make-logos.py): "Lockkeeper" in Geist 700 at
-0.03em, outlined; mark height 1.4 cap heights, centred on the cap height; gap 0.5; clear space 0.5.
"""
import importlib.util, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

spec = importlib.util.spec_from_file_location('make_logos', P('scripts', 'make-logos.py'))
ml = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ml)

W = 152          # stroke
R = W / 2
CORNER = 50   # every outer corner; the Cofferdam mark's ends are soft squares, not pills
LEAN = math.tan(math.radians(10))
SCALE = 0.94
INKS = {'white': '#FFFFFF', 'black': '#000000'}  # the single inks of the Cofferdam lockups


def corner(cx, cy, a0, step=6):
    """A quarter turn of radius CORNER about (cx, cy), clockwise on screen from angle a0 (degrees, y down)."""
    n = round(90 / step)
    return [(cx + CORNER * math.cos(math.radians(a0 + 90 * i / n)), cy + CORNER * math.sin(math.radians(a0 + 90 * i / n))) for i in range(n + 1)]


def place(points):
    """Lean, then scale about the centre; one decimal, as the Cofferdam mark is written."""
    out = []
    for x, y in points:
        x = x - LEAN * (y - 512)
        out.append('%.1f,%.1f' % (512 + (x - 512) * SCALE, 512 + (y - 512) * SCALE))
    return ' '.join(out)


def box(x0, y0, x1, y1):
    """A rectangle with every corner rounded, clockwise from the top-left corner."""
    c = CORNER
    return corner(x0 + c, y0 + c, 180) + corner(x1 - c, y0 + c, 270) + corner(x1 - c, y1 - c, 0) + corner(x0 + c, y1 - c, 90)


def chamber():
    """The L: a wall from (252,196) down to (252,828) and a floor on to (828,828), as one outline."""
    c, x0, x1, y0, y1 = CORNER, 252 - R, 828 + R, 196 - R, 828 + R
    pts = corner(x0 + c, y0 + c, 180) + corner(252 + R - c, y0 + c, 270)   # the wall's top end
    pts += [(252 + R, 828 - R)]                                              # the inside corner, square
    pts += corner(x1 - c, 828 - R + c, 270) + corner(x1 - c, y1 - c, 0)      # the floor's end
    pts += corner(x0 + c, y1 - c, 90)                                        # the outside corner
    return pts


def level():
    """The water level: a bar from (512,536) to (828,536)."""
    return box(512 - R, 536 - R, 828 + R, 536 + R)


def mark_polygons(ink):
    return ('<polygon id="chamber" points="%s" fill="%s"/><polygon id="level" points="%s" fill="%s"/>'
            % (place(chamber()), ink, place(level()), ink))


def bounds():
    xs, ys = [], []
    for pts in (chamber(), level()):
        for pair in place(pts).split(' '):
            x, y = pair.split(',')
            xs.append(float(x)); ys.append(float(y))
    return min(xs), min(ys), max(xs), max(ys)


def main():
    out = P('assets', 'logos', 'lockkeeper')
    os.makedirs(out, exist_ok=True)
    x0, y0, x1, y1 = bounds()
    ml.WORD = 'Lockkeeper'
    d, (bx0, by0, bx1, by1), C = ml.wordmark()
    for name, ink in INKS.items():
        open(os.path.join(out, 'lockkeeper-mark-%s.svg' % name), 'w').write(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024"><title>Lockkeeper</title>%s</svg>\n' % mark_polygons(ink))
        # Horizontal lockup, in font units: the mark's trimmed box is 1.4C tall and centred on the cap height.
        mh = 1.4 * C
        k = mh / (y1 - y0)
        mw = (x1 - x0) * k
        pad, gap = 0.5 * C, 0.5 * C
        width = pad + mw + gap + (bx1 - bx0) + pad
        height = pad + mh + pad
        cap_top = pad + (mh - C) / 2
        mark = '<g transform="translate(%.2f %.2f) scale(%.5f) translate(%.2f %.2f)">%s</g>' % (pad, pad, k, -x0, -y0, mark_polygons(ink))
        word = '<path transform="translate(%.2f %.2f)" fill="%s" d="%s"/>' % (pad + mw + gap - bx0, cap_top + C, ink, d)
        open(os.path.join(out, 'lockkeeper-lockup-horizontal-%s.svg' % name), 'w').write(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" width="%.0f" height="%.0f"><title>Lockkeeper</title>%s%s</svg>\n'
            % (width, height, width / 10, height / 10, mark, word))
    print('lockkeeper: mark and horizontal lockup × %s · mark box %.1f,%.1f to %.1f,%.1f · cap %d' % (', '.join(INKS), x0, y0, x1, y1, C))


if __name__ == '__main__':
    main()
