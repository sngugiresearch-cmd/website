#!/usr/bin/env python3
"""Render the two CFG articles; optionally sync canonical sources from their code repo."""
from pathlib import Path
import argparse
import hashlib
from html import escape
import json
import math
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parents[1]
POSTS = [
    {'source': '01-tactic-cfg.md', 'slug': '2026-08-22-lean-tactic-language-cfg',
     'description': 'A worked study of Lean tactic grammars: explicit syntax, permissive fallbacks, corpus extraction, mutation tests, and a reduced-grammar ablation.'},
    {'source': '02-constrained-decoding.md', 'slug': '2026-08-22-grammar-constrained-decoding-lean',
     'description': 'How grammar masking changes Lean tactic outputs: a reproducible Qwen comparison, token-level mechanics, exact denominators, latency, and exploratory Goedel runs.'},
]
CODE = 'https://github.com/stanleyngugi/lean-tactic-research/tree/revise-cfg-articles'
BASE = 'https://stanleyngugi.netlify.app'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, help='Companion repository; sync its articles and assets first')
    args = ap.parse_args()
    (ROOT/'content').mkdir(exist_ok=True)
    (ROOT/'assets/cfg').mkdir(parents=True, exist_ok=True)
    if args.source:
        for post in POSTS:
            shutil.copyfile(args.source/'articles'/post['source'], ROOT/'content'/post['source'])
        for asset in (args.source/'articles/assets').glob('*.svg'):
            shutil.copyfile(asset, ROOT/'assets/cfg'/asset.name)
    manifests = {}
    index = (ROOT/'index.html').read_text()
    rss = (ROOT/'rss.xml').read_text()
    for post in POSTS:
        source = ROOT/'content'/post['source']
        text = source.read_text()
        title, body = text.split('\n', 1)
        title = title.removeprefix('# ')
        minutes = math.ceil(len(text.split())/220)
        # Insert a keyboard-accessible collapsible contents list after the introduction.
        body = body.replace('\n## ', '\n[TOC]\n\n## ', 1)
        renderer = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc', 'codehilite'],
                                     extension_configs={'codehilite': {'guess_lang': False}})
        rendered = renderer.convert(body)
        rendered = re.sub(r'<div class="toc">(.*?)</div>',
                          r'<details class="article-contents"><summary>In this article</summary><nav aria-label="Article contents">\1</nav></details>', rendered, flags=re.S)
        rendered = rendered.replace('<table>', '<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable data table"><table>').replace('</table>', '</table></div>')
        archived = ROOT/'archive/revisions'/f"{post['slug']}-original.html"
        old = archived.read_text()
        prefix = old.split('<article class="prose">')[0]
        prefix = re.sub(r'<meta name="robots"[^>]*>\s*', "", prefix)
        suffix = old.split('</article>', 1)[1]
        prefix = re.sub(r'<title>.*?</title>', f'<title>{escape(title)} - Stanley Ngugi</title>', prefix)
        for key, value in [('description', post['description']), ('og:title', title),
                           ('og:description', post['description']), ('citation_title', title)]:
            prefix = re.sub(r'(<meta (?:name|property)="'+re.escape(key)+r'" content=")[^"]*(">)',
                            lambda m:m[1]+escape(value, quote=True)+m[2], prefix)
        canonical = f"{BASE}/posts/{post['slug']}.html"
        data = {'@context':'https://schema.org', '@type':'Article', 'headline':title,
                'description':post['description'], 'author':{'@type':'Person','name':'Stanley Ngugi'},
                'datePublished':'2026-08-22', 'dateModified':'2026-09-05', 'url':canonical,
                'mainEntityOfPage':canonical}
        meta = f'<link rel="canonical" href="{canonical}">\n<meta property="article:modified_time" content="2026-09-05T00:00:00Z">\n<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'
        prefix = prefix.replace('</head>', meta+'</head>')
        article = f'''<article class="prose cfg-article">
<header class="article-header"><h1>{escape(title)}</h1>
<div class="entry-date">August 22, 2026 · updated September 5 · {minutes} min read · <a href="{CODE}">code ↗</a></div></header>
{rendered}
<div class="cite-box"><div class="cite-label">Cite this revision</div>
<pre><code>{escape('@misc{ngugi2026' + ('cfg' if post == POSTS[0] else 'decoding') + ',\n  title = {' + title + '},\n  author = {Ngugi, Stanley},\n  year = {2026},\n  url = {' + canonical + '},\n  note = {Revised September 5, 2026}\n}')}</code></pre></div>
<p class="article-artifacts"><a href="{CODE}">Companion code and evidence</a> · <a href="/content/{post['source']}">Markdown source</a></p>
</article>'''
        (ROOT/'posts'/f"{post['slug']}.html").write_text(prefix+article+suffix)
        # Update only the corresponding homepage entry.
        pattern = r'(<a href="/posts/'+re.escape(post['slug'])+r'\.html" class="entry">)(.*?)(</a>)'
        def entry(m):
            inner = re.sub(r'(<span class="entry-title">).*?(</span>)', lambda x:x[1]+escape(title)+x[2],m[2],flags=re.S)
            inner = re.sub(r'(<div class="entry-desc">).*?(</div>)', lambda x:x[1]+'\n'+escape(post['description'])+'\n'+x[2],inner,flags=re.S)
            inner = inner.replace('>Aug 22</span>', '>Aug 22 · revised Sep 5</span>')
            return m[1]+inner+m[3]
        index, n = re.subn(pattern,entry,index,flags=re.S)
        if n != 1:raise RuntimeError(f"Expected one homepage entry for {post['slug']}")
        def item(m):
            value = m[0]
            if canonical not in value:return value
            value = re.sub(r'<title>.*?</title>', '<title>'+escape(title)+'</title>',value,flags=re.S)
            return re.sub(r'<description>.*?</description>', '<description>'+escape(post['description'])+'</description>',value,flags=re.S)
        rss = re.sub(r'<item>.*?</item>',item,rss,flags=re.S)
        manifests[post['source']] = {'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                                     'output':f"posts/{post['slug']}.html", 'title':title,'reading_minutes':minutes}
    (ROOT/'index.html').write_text(index)
    (ROOT/'rss.xml').write_text(rss)
    sitemap = (ROOT/'sitemap.xml').read_text().replace('<lastmod>2026-08-22</lastmod>','<lastmod>2026-09-05</lastmod>')
    (ROOT/'sitemap.xml').write_text(sitemap)
    (ROOT/'content/manifest.json').write_text(json.dumps(manifests,indent=2,ensure_ascii=False)+'\n')
    print('Rendered two articles; synchronized homepage, RSS, sitemap, and metadata.')


if __name__ == '__main__':
    main()
