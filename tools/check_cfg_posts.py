#!/usr/bin/env python3
"""Check generated article integrity and local links without a web service."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.images, self.headings, self.canonicals = [], [], [], [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag == 'img': self.images.append(a)
        if tag == 'h1': self.headings.append(tag)
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a['href'])

manifest = json.loads((ROOT/'content/manifest.json').read_text())
for name, record in manifest.items():
    assert hashlib.sha256((ROOT/'content'/name).read_bytes()).hexdigest() == record['sha256'], name
    path = ROOT/record['output']
    page = Page(path.read_text())
    assert len(page.headings) == 1 and len(page.canonicals) == 1, path
    assert len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {path}'
    assert '[TOC]' not in path.read_text(), path
    for img in page.images:
        assert img.get('alt'), f'Missing image description: {path}'
    for ref in page.links + [x['src'] for x in page.images]:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        target = ROOT/unquote(url.path.lstrip('/')) if url.path.startswith('/') else path.parent/unquote(url.path)
        if not url.path: target = path
        if target.is_dir(): target = target/'index.html'
        assert target.is_file(), f'{path.name}: missing {ref}'
        if url.fragment and target.suffix == '.html':
            assert unquote(url.fragment) in Page(target.read_text()).ids, f'{path.name}: missing anchor {ref}'
for name in ('rss.xml', 'sitemap.xml'):
    ET.parse(ROOT/name)
print('Two articles: source hashes, headings, canonical URLs, local links, anchors, image descriptions, and XML pass.')
