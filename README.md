# Stanley Ngugi's website

Static HTML, CSS, and JavaScript. Serve this directory locally with
`python3 -m http.server 8765`, then visit `http://localhost:8765`.

## Current research articles

`content/mathcheck-engine.md`, `content/mathcheck-rl.md`, and
`content/formally-verified-c.md` are unchanged copies of their canonical GitHub
articles. `content/research-posts-manifest.json` records source URLs and hashes.
To update them, sync the source copies, then run
`python3 tools/build_mathcheck_posts.py` (Pandoc 3 is required). The renderer
creates a distinct page and BibTeX file for each article, repairs repo-relative
evidence links, and links companion posts together. Update homepage, RSS, and
sitemap entries for any title or date changes. The GitHub articles remain
available until the website pages are live; only then replace the repository
articles with pointers if desired.

Visible post headers and homepage cards have no publication dates. Metadata and
RSS use September 12, 2026 for the MathCheck articles and September 13, 2026
for Formally Verified C, matching their public GitHub publication/release dates;
the website does not backdate unrelated work.

## Editing the two CFG articles

Their canonical Markdown and figure generator live in the sibling
`ai-proof-grammars` repository, under `articles/` and `analysis/figures.py`.
This website keeps a synchronized copy in `content/` and generated HTML in
`posts/`. Edit the canonical Markdown, then rebuild:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements-build.txt
python tools/build_cfg_posts.py --source ../ai-proof-grammars
python tools/check_cfg_posts.py
```

To render the committed website sources without a companion checkout:

```bash
python tools/build_cfg_posts.py
python tools/check_cfg_posts.py
```

The build updates article HTML, homepage entries, RSS descriptions, sitemap dates,
and citation metadata. `content/manifest.json` records source hashes. SVG assets
are copied from the companion project, where their numerical inputs and generation
instructions are documented. Python 3.12 is required for the build script.

Original August 22 posts remain in `archive/revisions/`, with a visible revision
notice and `noindex` metadata. The existing public article URLs and original
publication dates are preserved. Review changes on a branch before merging into
the deployment branch.

## Publication dates

The homepage uses topics and reading time instead of dates, keeping attention on
the work rather than publishing cadence. RSS, citation metadata, sitemap records,
and article history retain the real publication and revision dates. Revisions use
an accurate `dateModified`; original publication dates are never backdated or
redistributed for presentation.


## Search visibility

The live site's canonical address is `https://stanleyngugi.netlify.app/`.
Article and CV canonical URLs use Netlify's extensionless Pretty URLs. The
homepage, article metadata, sitemap, citation URLs, and feed links agree on
those addresses. Existing RSS GUIDs remain stable for subscribers.

The homepage identifies Stanley Ngugi through Person, ProfilePage, and WebSite
structured data. Articles link their author back to the same identity. Update
the verified `sameAs` links if another public author profile is added.

Retired `/research`, `/posts`, and `/about` overview routes redirect permanently
to the current homepage or its corresponding section. Legacy essays redirect
to `/archive/`. Archive pages use an `X-Robots-Tag: noindex` header. They remain
crawlable so search engines can read that instruction; a robots.txt crawl block
would prevent them from seeing it.

After deployment, open Google Search Console for this site's URL-prefix
property, submit `sitemap.xml`, and inspect the homepage, `/cv`, and the six
current articles. Request indexing for the current homepage and three new
project articles first. Check the live redirects for `/research` and `/posts`,
and confirm an archived page returns the noindex header. Keep the existing
Google verification file. Source changes cannot submit indexing requests on
their own, and search engines choose when to refresh snippets.
