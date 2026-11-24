#!/usr/bin/env python3
"""Render the diagrams of Lockkeeper's README (github.com/cofferdamxyz/lockkeeper) from the brand tokens.

    node scripts/build.mjs && uv run --with playwright python social/diagrams/lockkeeper/render.py

The builder is the XMTP article's (social/articles/xmtp-on-cloudflare/render.py and stack.py): the same
canvases, tiles, cards, lines and footer, imported from there (its icons too; this set adds two). Writes four 4:3 PNGs at 2400x1800 beside
this file; the README shows them at column width, so 2400 is twice what a wide screen draws. Copy them
into lockkeeper/docs/diagrams/ byte for byte.

rules: the article's (dark only, greyscale, the only colour in the logos, Geist and Geist Mono, the
       single-ink lockup bottom left). One thing is marked in every diagram that has it, by a heavy
       white line or a lighter card, with the same legend: Lockkeeper's only write to GitHub, the
       advice comment. Everything else it does there is a read. One name per thing: Session,
       Lockkeeper, GitHub. The text follows lockkeeper/DESIGN.md; when a number changes there
       (the poll's five minutes, the cosine of 0.6), it changes here.
"""
import importlib.util, os, sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'articles', 'xmtp-on-cloudflare')
sys.path.insert(0, ARTICLE)
import stack  # noqa: E402

spec = importlib.util.spec_from_file_location('article_render', os.path.join(ARTICLE, 'render.py'))
ar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ar)

stack.ICON_DIRS.append(os.path.join(HERE, 'icons'))
LEGEND = "Lockkeeper's only write to GitHub"
W, H = ar.W, ar.H
text, box, tile, line = ar.text, ar.box, ar.tile, ar.line


# 1. At a glance -----------------------------------------------------------------------------------
def d_architecture():
    r1, r2 = 206, 436            # tile tops; mid = +30, box bottom = +104
    groups = [stack.group(172, 156, 524, 410, 'Cloudflare', 'cloudflare')]
    nodes = [stack.node(80, r1, 'terminal', 'Sessions', 'people and agents'),
             stack.node(262, r1, 'cloudflare', 'Access', 'who may ask'),
             stack.node(444, r1, 'workers', 'Lockkeeper', 'API, MCP, cron'),
             stack.node(786, r1, 'github', 'GitHub', 'your repositories'),
             stack.node(262, r2, 'cloudflare', 'D1', 'the ledger'),
             stack.node(444, r2, 'cloudflare', 'Vectorize', 'branch and claim vectors'),
             stack.node(626, r2, 'cloudflare', 'Workers AI', 'bge-m3 and Clef')]
    e, el = stack.edge, stack.el
    edges = [e('M116 236 H226'), el(171, 226, 'HTTP or MCP'),
             e('M298 236 H408'),
             e('M480 224 H750'), el(615, 214, 'polls every 5 min'),
             e('M480 250 H750', 'e'), el(615, 271, 'one advice comment', 'a'),
             e('M80 200 V128 H786 V200'), el(433, 118, 'git push goes straight to GitHub, never through Lockkeeper'),
             e('M444 310 V430'), e('M424 310 V372 H262 V430'), e('M464 310 V372 H626 V430')]
    return stack.canvas('Lockkeeper at a glance',
                        'It reads GitHub for every session and writes one thing back: advice on a pull request.',
                        groups, edges, nodes, legend=LEGEND, plain='every other call')


# 2. One session -----------------------------------------------------------------------------------
def d_session():
    b = []
    lanes = [(170, 'Session', 'terminal'), (560, 'Lockkeeper', 'workers'), (950, 'GitHub', 'github')]
    for x, t, ic in lanes:
        b.append('<rect x="%d" y="160" width="232" height="60" rx="16" fill="var(--card)" stroke="var(--border)" stroke-width="1.5"/>' % (x - 116))
        b.append(tile(x - 106, 169, ic, 42))
        b.append(text(x + 24, 198, t, 22, 600, 'var(--fg)', anchor='middle'))
        b.append('<line x1="%d" y1="220" x2="%d" y2="716" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="3 7" stroke-linecap="round"/>' % (x, x))
    steps = [(170, 560, 'brief: what is in flight near my paths?', False),
             (170, 560, 'claim: I am about to work here', False),
             (170, 560, 'check, before a commit or a push', False),
             (560, 950, 'one live compare: what moved since your base', False),
             (170, 950, 'git push and a pull request, straight to GitHub', False),
             (560, 950, 'the poll sees the branch and releases its claim', False),
             (560, 950, 'advice: one comment on the pull request', True)]
    for i, (x1, x2, s, acc) in enumerate(steps):
        y = 298 + i * 66
        b.append(line([(x1 + 4, y), (x2 - 5, y)], accent=acc))
        lx = x1 + 18
        b.append('<circle cx="%d" cy="%d" r="15" fill="var(--bg)" stroke="var(--border-control)" stroke-width="1.5"/>' % (lx + 15, y - 28))
        b.append(text(lx + 15, y - 21.5, str(i + 1), 17, 600, 'var(--fg)', anchor='middle'))
        b.append(text(lx + 40, y - 21, s, 21, 500, 'var(--fg)', halo=True))
    notes = [(170, ['decides everything, and works', 'the same if Lockkeeper is down']),
             (560, ['holds no credential that', 'could change your code']),
             (950, ['main always wins;', 'branches rebase onto it'])]
    for x, ls in notes:
        for j, s in enumerate(ls):
            b.append(text(x, 752 + j * 27, s, 19.5, 500, anchor='middle'))
    return ar.frame('One session, from start to landing', 'Every arrow into Lockkeeper is a question. It answers with facts; the session decides.',
                    ''.join(b), legend=LEGEND)


# 3. What is in flight -----------------------------------------------------------------------------
def d_inflight():
    b = []
    lanes = [
        ('The poll', 'every five minutes, with no webhook', [
            ('List', ['the repositories the', 'GitHub App can see']),
            ('Compare', ['each branch, when it', 'or main has moved']),
            ('Record', ['files, merge base,', 'ahead, behind and CI']),
            ('Embed', ['one vector per branch', 'in flight, with bge-m3'])]),
        ('A claim', 'for the hour before a branch exists', [
            ('Take', ['paths, a goal and', 'a time to live']),
            ('Show', ['in every brief that', 'touches those paths']),
            ('Release', ['once its branch is on', 'GitHub, or on expiry'])]),
        ('A question', 'what is in flight near these paths?', [
            ('Match paths', ['a shared file, folder', 'or glob']),
            ('Match meaning', ['when you state a goal:', 'cosine 0.6 or more']),
            ('List what is near', ['branches, PRs and', 'claims, with overlap']),
            ('Count the rest', ['everything else,', 'as one number'])]),
    ]
    for i, (t, sub, chips) in enumerate(lanes):
        y = 156 + i * 214
        b.append(text(48, y + 28, t, 27, 700, 'var(--fg)', spacing='-0.4px'))
        b.append(text(1152, y + 28, sub, 20, 500, anchor='end'))
        for k, (ct, cl) in enumerate(chips):
            x = 48 + k * 282
            b.append(box(x, y + 46, 258, 122, ct, cl, pad=18, tsize=22, lsize=19))
            if k < len(chips) - 1:
                b.append(line([(x + 258, y + 107), (x + 280, y + 107)]))
    return ar.frame('How it knows what is in flight', 'A poll of GitHub, claims for work not pushed yet, and two ways for work to be near yours.',
                    ''.join(b), legend=False)


# 4. The advice ------------------------------------------------------------------------------------
def d_advice():
    b = []
    b.append(box(48, 156, 344, 190, 'Candidates', ['Open pull requests from the', "repository's own branches,", 'drafts included, oldest', 'first, twenty at most.'], tsize=23, lsize=19))
    b.append(box(428, 156, 344, 190, 'Three questions for Clef', ['Which lands next?', 'May it land without a person?', 'How much risk to the others?'], ['next · unattended · risk'], tsize=23, lsize=19))
    b.append(box(808, 156, 344, 190, 'Rules that can only say no', ['CI not green on its head', 'touches a sensitive path', 'shares a file with another', 'its base went stale'], tsize=23, lsize=19))
    b.append(line([(394, 251), (424, 251)]))
    b.append(line([(774, 251), (804, 251)]))
    b.append(box(48, 398, 536, 122, 'The landing order', ["Clef's pick, then its probabilities; after", 'that green CI, least overlap, oldest.'], tsize=23, lsize=19))
    b.append(box(616, 398, 536, 122, 'One comment per pull request', ['Created once, then edited in place when the', 'head, CI or the other pull requests change.'], accent=True, tsize=23, lsize=19))
    b.append(line([(520, 348), (520, 372), (316, 372), (316, 394)]))
    b.append(line([(980, 348), (980, 394)]))
    b.append(line([(586, 459), (612, 459)]))
    b.append(text(48, 572, 'WHAT THE PULL REQUEST GETS', 15, 500, spacing='0.2em'))
    b.append('<rect x="48" y="592" width="1104" height="196" rx="16" fill="var(--card)" stroke="var(--border)" stroke-width="1.5"/>')
    sans, mono = "font-family='var(--font-sans)'", "font-family='var(--font-mono)'"
    b.append('<text x="72" y="634" %s font-size="23" font-weight="600" fill="var(--fg)">Lockkeeper advice'
             '<tspan dx="12" %s font-size="18" font-weight="500" fill="var(--fg-muted)">4b5909a</tspan></text>' % (sans, mono))
    rows = [('Landing order:', '2 of 5 open pull requests in this repository (after #41).'),
            ('Unattended-eligible:', "no. Shares files with #41 (src/routes/export.ts). Clef's unattended 0.62 is under 0.80."),
            ('Risk to the other changes in flight:', 'minor risk (1.00 of 3). Clef: unattended 0.62, next 0.31.')]
    for j, (k, v) in enumerate(rows):
        b.append('<text x="72" y="%d" %s font-size="19.5" font-weight="600" fill="var(--fg)">%s'
                 '<tspan dx="8" font-weight="500" fill="var(--fg-muted)">%s</tspan></text>' % (674 + j * 31, sans, ar.E(k), ar.E(v)))
    b.append(text(72, 770, 'Advice only: Lockkeeper lands nothing and applies no label.', 16.5, 500))
    return ar.frame('From open pull requests to advice', 'After every poll, for each repository: an order to land in, and a verdict a person reads.',
                    ''.join(b), legend=LEGEND)


def main():
    s = 2400 / W
    jobs = [('01-at-a-glance', ar.page(d_architecture(), stack.CSS), (stack.W, stack.H), 2400 / stack.W),
            ('02-one-session', ar.page(d_session()), (W, H), s),
            ('03-in-flight', ar.page(d_inflight()), (W, H), s),
            ('04-advice', ar.page(d_advice()), (W, H), s)]
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
