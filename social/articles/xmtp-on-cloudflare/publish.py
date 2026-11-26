#!/usr/bin/env python3
"""Turn article.md into what X's article editor takes.

    python3 social/articles/xmtp-on-cloudflare/publish.py
    python3 social/articles/xmtp-on-cloudflare/publish.py --since 1a8fdf3

X's editor takes rich text, not Markdown, and a paste carries no code: a code block comes only from the
editor's Insert menu, one sample at a time (seen in the editor, 2026-11-23). So this writes paste.html
beside this file, a page to copy from: the title, the body as clean rich text with a marker where each
diagram and code sample goes, each sample's code for Insert > Code, every image's alt text, and the post
that announces the article.

An article on X is edited by hand, so `--since <commit>` also writes edit.html: what changed in article.md
since that commit, as a list of edits, each saying where it goes, what to delete and what to paste.

Nothing here posts anything. One source: edit article.md or launch-post.md and run this again. Standard
library only; the page reads dist/tokens.css and the brand fonts by relative path.

rules: every code line fits MAX_COLS columns, so a sample reads on a phone without wrapping.
"""
import difflib, html, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
E = lambda s: html.escape(s, quote=False)
MAX_COLS = 60
# One per fenced block, in the article's order: what the sample is and its language, for the marker.
CODE = ['The Worker · TypeScript',
        'Joining two sockets · TypeScript',
        'The Durable Object · TypeScript',
        'The reverse proxy · Caddyfile',
        'Restart on a changed secret · TypeScript',
        'The backend · TOML',
        'The cleanup Worker · TypeScript',
        'The delete · SQL',
        'The push relay · TypeScript',
        'The hint · pseudocode',
        'Read receipts · TypeScript']


# Reading article.md -------------------------------------------------------------------------------
def parse(md):
    """The article as blocks: title, h2, p, ul, ol, image, code. Paragraphs are one line each."""
    lines, out, i = re.sub(r'<!--.*?-->', '', md, flags=re.S).split('\n'), [], 0
    item = re.compile(r'(- |\d+\. )')
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            j = i + 1
            while not lines[j].startswith('```'):
                j += 1
            out.append(('code', '\n'.join(lines[i + 1:j]).expandtabs(4)))
            i = j
        elif ln.startswith('# '):
            out.append(('title', ln[2:]))
        elif ln.startswith('## '):
            out.append(('h2', ln[3:]))
        elif re.fullmatch(r'\[image: (.+)\]', ln):
            out.append(('image', ln[8:-1]))
        elif item.match(ln):
            items = []
            while i < len(lines) and item.match(lines[i]):
                items.append(item.sub('', lines[i], count=1))
                i += 1
            out.append(('ul' if ln.startswith('- ') else 'ol', items))
            continue
        elif ln.strip():
            out.append(('p', ln))
        i += 1
    return out


def alts(md):
    """The alt texts in article.md's closing comment: a file name, then its text on the next line."""
    tail = md[md.rindex('<!--'):]
    return {m[1]: m[2].strip() for m in re.finditer(r'^\s*(\S+\.png)\n\s*(\S.*)$', tail, flags=re.M)}


def inline(s, plain=False):
    """Markdown's inline marks as HTML, or stripped to text."""
    spans = []

    def stash(m):
        spans.append(m[1])
        return '\x00%d\x00' % (len(spans) - 1)

    s = re.sub(r'`([^`]+)`', stash, s)
    if plain:
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
        return re.sub('\x00(\\d+)\x00', lambda m: spans[int(m[1])], s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', E(s))
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return re.sub('\x00(\\d+)\x00', lambda m: '<code>%s</code>' % E(spans[int(m[1])]), s)


# What goes on the clipboard -----------------------------------------------------------------------
def image_marker(name):
    return '[image: %s]' % name


def code_marker(n):
    return '[code %d of %d: %s]' % (n + 1, len(CODE), CODE[n])


def text_block(kind, v):
    """A heading, paragraph or list as HTML and as text."""
    if kind == 'h2':
        return '<h2>%s</h2>' % inline(v), inline(v, True)
    if kind == 'p':
        return '<p>%s</p>' % inline(v), inline(v, True)
    bullets = ['%s %s' % ('•' if kind == 'ul' else '%d.' % (k + 1), inline(x, True)) for k, x in enumerate(v)]
    return '<%s>%s</%s>' % (kind, ''.join('<li>%s</li>' % inline(x) for x in v), kind), '\n'.join(bullets)


def clean(blocks):
    """The body as the plainest HTML an editor can take, and as text. No title: X has its own field."""
    h, t, n = [], [], 0
    for kind, v in blocks:
        if kind == 'image':
            m = image_marker(v)
        elif kind == 'code':
            m, n = code_marker(n), n + 1
        else:
            a, b = text_block(kind, v)
            h.append(a)
            t.append(b)
            continue
        h.append('<p>%s</p>' % E(m))
        t.append(m)
    return {'html': ''.join(h), 'text': '\n\n'.join(t)}


# The page to copy from ----------------------------------------------------------------------------
PASTE_CSS = '''
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 500 16px/26px var(--font-sans); }
main { max-width: 760px; margin: 0 auto; padding: 48px 20px 120px; }
h1 { font-size: 34px; line-height: 40px; font-weight: 700; letter-spacing: -0.8px; margin: 0 0 12px; text-wrap: balance; }
code { font-family: var(--font-mono); font-size: .9em; }
.lede, .note { color: var(--fg-muted); margin: 0 0 12px; }
.note { font-size: 14px; line-height: 22px; }
ol.steps { margin: 20px 0 0; padding-left: 22px; color: var(--fg-muted); }
ol.steps li { margin: 6px 0; }
section { margin-top: 44px; border-top: 1px solid var(--border); padding-top: 28px; }
.eyebrow { font: 500 13px/18px var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--fg-muted); margin: 0 0 12px; }
.row { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 12px; margin: 14px 0 0; }
button { font: 600 15px/20px var(--font-sans); padding: 11px 16px; min-height: 44px; border-radius: var(--radius-web);
         border: 1px solid var(--border-control); background: transparent; color: var(--fg); cursor: pointer; }
button:hover { background: var(--card); }
button:focus-visible { outline: 2px solid var(--fg); outline-offset: 2px; }
button.primary { background: var(--fg); color: var(--bg); border-color: var(--fg); }
button.primary:hover { background: var(--fg-muted); border-color: var(--fg-muted); }
.plain { margin: 0; padding: 16px 18px; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-md);
         white-space: pre-wrap; font: 500 16px/26px var(--font-sans); }
.body { margin-top: 22px; padding: 6px 22px 22px; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); }
.body h2 { font-size: 22px; line-height: 28px; font-weight: 700; letter-spacing: -0.2px; margin: 34px 0 10px; }
.body p, .body li { color: var(--fg-muted); }
.body p { margin: 14px 0; }
.body strong { color: var(--fg); font-weight: 600; }
.body a { color: var(--fg); text-underline-offset: 3px; }
.body code, .body pre { font-family: var(--font-mono); font-size: 14px; color: var(--fg); }
.body pre { margin: 0; overflow-x: auto; padding: 14px 16px; background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-sm); line-height: 22px; }
figure { margin: 20px 0; padding: 12px; background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-md); }
figure img { display: block; width: 100%; height: auto; border-radius: var(--radius-sm); }
figcaption { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px 12px; margin-top: 10px;
             font: 500 14px/20px var(--font-mono); color: var(--fg); overflow-wrap: anywhere; }
figcaption button { font-size: 14px; padding: 8px 12px; min-height: 40px; }
'''

PASTE_JS = '''
const D = JSON.parse(document.getElementById('data').textContent);
function done(b) { const t = b.textContent; b.textContent = 'Copied'; setTimeout(() => { b.textContent = t; }, 1400); }
function legacy(htmlText, text) {
  const el = document.createElement(htmlText ? 'div' : 'textarea');
  if (htmlText) { el.contentEditable = 'true'; el.innerHTML = htmlText; } else { el.value = text; }
  el.style.cssText = 'position:fixed;left:-9999px;top:0;white-space:pre-wrap';
  document.body.appendChild(el);
  if (htmlText) { const r = document.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  else { el.select(); }
  document.execCommand('copy'); el.remove(); getSelection().removeAllRanges();
}
async function copy(b, text, htmlText) {
  try {
    if (htmlText) {
      await navigator.clipboard.write([new ClipboardItem({
        'text/html': new Blob([htmlText], { type: 'text/html' }), 'text/plain': new Blob([text], { type: 'text/plain' }) })]);
    } else { await navigator.clipboard.writeText(text); }
  } catch (e) { legacy(htmlText, text); }
  done(b);
}
document.addEventListener('click', (e) => {
  const b = e.target.closest('button'); if (!b) return;
  if (b.dataset.copy === 'title') return copy(b, D.title);
  if (b.dataset.copy === 'post') return copy(b, D.post);
  if (b.dataset.copy === 'body') return copy(b, D.body.text, D.body.html);
  if (b.dataset.alt) return copy(b, D.alt[b.dataset.alt]);
  if (b.dataset.code) return copy(b, D.code[Number(b.dataset.code)]);
  if (b.dataset.edit) return copy(b, D.edits[Number(b.dataset.edit)].text, D.edits[Number(b.dataset.edit)].html);
});
'''


def figure(name):
    """An image where its marker will be."""
    return ('<figure><img src="%s" alt="" loading="lazy"><figcaption><span>%s</span>'
            '<button data-alt="%s">Copy alt text</button></figcaption></figure>') % (name, name, name)


def sample(n, code):
    """A code sample where its marker will be, with its text for the editor's own code block."""
    return ('<figure><pre><code>%s</code></pre><figcaption><span>%s</span>'
            '<button data-code="%d">Copy code</button></figcaption></figure>') % (E(code), E(code_marker(n)), n)


def preview(blocks):
    """The body as the page shows it: the same text, with each image and sample where its marker will be."""
    out, n = [], 0
    for kind, v in blocks:
        if kind == 'image':
            out.append(figure(v))
        elif kind == 'code':
            out.append(sample(n, v))
            n += 1
        else:
            out.append(text_block(kind, v)[0])
    return ''.join(out)


def paste_page(title, blocks, alt, post):
    codes = [v for k, v in blocks if k == 'code']
    data = {'title': title, 'post': post, 'alt': alt, 'code': codes, 'body': clean(blocks)}
    fonts = ''.join("@font-face{font-family:'%s';src:url(../../../%s);font-weight:%s}" % (f['family'], f['file'], f['weight'])
                    for f in json.load(open(os.path.join(ROOT, 'tokens', 'tokens.json')))['type']['fonts'])
    return '''<!doctype html>
<!-- Generated by publish.py from article.md and launch-post.md. Do not edit: run publish.py again. -->
<html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paste sheet: %(title)s</title>
<link rel="stylesheet" href="../../../dist/tokens.css"><style>%(fonts)s%(css)s</style></head>
<body><main>
<p class="eyebrow">Paste sheet for X's article editor</p>
<h1>%(title)s</h1>
<p class="lede">Each button puts one piece on the clipboard, ready to paste into X. Nothing on this page posts anything.</p>
<ol class="steps">
<li>On x.com, open Articles, then Write. Upload <code>00-cover.png</code> as the cover.</li>
<li>Copy the title and paste it into the title field.</li>
<li>Copy the body and paste it into the editor.</li>
<li>At each <code>[image: …]</code> line, choose Insert, Media, add that file and its alt text, then delete the line.</li>
<li>At each <code>[code …]</code> line, choose Insert, Code, paste that sample with Copy code, then delete the line.</li>
<li>Preview, publish, then post the announcement with the article's link.</li>
</ol>

<section><p class="eyebrow">1 · Title</p>
<p class="plain">%(title)s</p>
<div class="row"><button class="primary" data-copy="title">Copy title</button></div>
<figure><img src="00-cover.png" alt=""><figcaption><span>00-cover.png</span><button data-alt="00-cover.png">Copy alt text</button></figcaption></figure>
</section>

<section><p class="eyebrow">2 · Body</p>
<p class="note">A paste carries no images and no code into X's editor, so the body holds a marker for each of the %(pictures)d diagrams and %(samples)d code samples.</p>
<div class="row"><button class="primary" data-copy="body">Copy body</button></div>
<div class="body">%(preview)s</div>
</section>

<section><p class="eyebrow">3 · The post that announces it</p>
<p class="note">Replace ARTICLE_LINK with the article's URL. Attach <code>01-architecture.png</code> with its alt text.</p>
<p class="plain">%(post)s</p>
<div class="row"><button class="primary" data-copy="post">Copy post</button></div>
</section>
</main>
<script type="application/json" id="data">%(data)s</script>
<script>%(js)s</script>
</body></html>
''' % {'title': E(title), 'fonts': fonts, 'css': PASTE_CSS, 'samples': len(codes),
       'pictures': sum(1 for k, _ in blocks if k == 'image'), 'preview': preview(blocks), 'post': E(post),
       'data': json.dumps(data).replace('</', '<\\/'), 'js': PASTE_JS}


# What changed since the article went up ----------------------------------------------------------
def label(block):
    """One block in a few words, to find it in X's editor."""
    kind, v = block
    if kind == 'image':
        return 'the image %s' % v
    if kind == 'code':
        return 'the code sample that starts "%s"' % v.strip().split('\n')[0][:50]
    text = inline(v if isinstance(v, str) else v[0], True)
    what = {'h2': 'the heading', 'p': 'the paragraph that starts', 'ul': 'the list that starts', 'ol': 'the numbered list that starts'}[kind]
    return '%s "%s"' % (what, text if kind == 'h2' or len(text) <= 70 else text[:70].rstrip() + '…')


def edits(old, new):
    """The changes that turn the old body into the new one, in the article's order."""
    key = lambda b: json.dumps(b)
    out = []
    for op, a0, a1, b0, b1 in difflib.SequenceMatcher(None, [key(b) for b in old], [key(b) for b in new], autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        out.append({'after': label(old[a0 - 1]) if a0 else None, 'before': label(old[a1]) if a1 < len(old) else None,
                    'remove': [label(b) for b in old[a0:a1]], 'add': new[b0:b1]})
    return out


def edit_page(title, rev, changes):
    data = {'edits': [clean(c['add']) for c in changes]}
    fonts = ''.join("@font-face{font-family:'%s';src:url(../../../%s);font-weight:%s}" % (f['family'], f['file'], f['weight'])
                    for f in json.load(open(os.path.join(ROOT, 'tokens', 'tokens.json')))['type']['fonts'])
    parts = []
    for n, c in enumerate(changes):
        where = ('At the very start of the body, before %s.' % c['before']) if c['after'] is None else \
                ('Find %s.' % c['after']) + (' The change goes right after it.' if not c['remove'] else '')
        steps = ['<li>%s</li>' % E(where)]
        if c['remove']:
            steps.append('<li>Delete what follows it%s:<ul>%s</ul></li>' % (
                ', up to %s' % E(c['before']) if c['before'] else ', to the end of the article',
                ''.join('<li>%s</li>' % E(r) for r in c['remove'])))
        if c['add']:
            steps.append('<li>Put the cursor there, copy the new text with the button below, and paste.</li>')
        parts.append('<section><p class="eyebrow">Edit %d of %d</p><ol class="steps">%s</ol>%s</section>' % (
            n + 1, len(changes), ''.join(steps),
            ('<div class="row"><button class="primary" data-edit="%d">Copy the new text</button></div><div class="body">%s</div>'
             % (n, preview_plain(c['add']))) if c['add'] else ''))
    return '''<!doctype html>
<!-- Generated by publish.py --since %(rev)s from article.md. Do not edit: run publish.py again. -->
<html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edit sheet: %(title)s</title>
<link rel="stylesheet" href="../../../dist/tokens.css"><style>%(fonts)s%(css)s</style></head>
<body><main>
<p class="eyebrow">Edit sheet for the article on X</p>
<h1>%(title)s</h1>
<p class="lede">What changed in the article since <code>%(rev)s</code>, as %(count)d edit(s) to make by hand in X's editor, top to bottom. Nothing on this page posts anything.</p>
<p class="note">On x.com, open the article, choose Edit, make each edit below, then Preview and publish. A paste carries headings, lists, bold and links.</p>
%(parts)s
</main>
<script type="application/json" id="data">%(data)s</script>
<script>%(js)s</script>
</body></html>
''' % {'title': E(title), 'rev': E(rev), 'fonts': fonts, 'css': PASTE_CSS, 'count': len(changes), 'parts': ''.join(parts),
       'data': json.dumps(data).replace('</', '<\\/'), 'js': PASTE_JS}


def preview_plain(blocks):
    """New blocks as the edit sheet shows them: text as it will paste, with a marker for an image or a sample."""
    return ''.join(text_block(k, v)[0] if k in ('h2', 'p', 'ul', 'ol') else '<p>%s</p>' % E('[%s: add it with Insert]' % label((k, v)))
                   for k, v in blocks)


def main():
    md = open(os.path.join(HERE, 'article.md')).read()
    blocks = parse(md)
    title = next(v for k, v in blocks if k == 'title')
    codes = [v for k, v in blocks if k == 'code']
    assert len(codes) == len(CODE), 'article.md has %d code samples, CODE names %d' % (len(codes), len(CODE))
    for label, code in zip(CODE, codes):
        for ln in code.split('\n'):
            assert len(ln) <= MAX_COLS, '%s: over %d columns: %s' % (label, MAX_COLS, ln)

    alt = alts(md)
    for name in ['00-cover.png'] + [v for k, v in blocks if k == 'image']:
        assert os.path.exists(os.path.join(HERE, name)), 'no file ' + name
        assert name in alt, 'no alt text for ' + name
        assert len(alt[name]) <= 1000, '%s: alt text is %d characters, X takes 1,000' % (name, len(alt[name]))

    post = re.sub(r'<!--.*?-->', '', open(os.path.join(HERE, 'launch-post.md')).read(), flags=re.S).strip()
    counted = len(post.replace('ARTICLE_LINK', 'x' * 23))
    assert counted <= 280, 'the launch post is %d characters' % counted

    open(os.path.join(HERE, 'paste.html'), 'w').write(paste_page(title, [b for b in blocks if b[0] != 'title'], alt, post))
    print('wrote paste.html: %d code samples; the launch post counts %d of 280' % (len(codes), counted))

    if '--since' in sys.argv:
        rev = sys.argv[sys.argv.index('--since') + 1]
        rel = os.path.relpath(os.path.join(HERE, 'article.md'), ROOT)
        before = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (rev, rel)], check=True, capture_output=True, text=True).stdout
        body = lambda text: [b for b in parse(text) if b[0] != 'title']
        changes = edits(body(before), body(md))
        open(os.path.join(HERE, 'edit.html'), 'w').write(edit_page(title, rev, changes))
        print('wrote edit.html: %d edit(s) since %s' % (len(changes), rev))


if __name__ == '__main__':
    main()
