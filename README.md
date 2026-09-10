# Stanley Ngugi's website

Static HTML, CSS, and JavaScript. Serve this directory locally with
`python3 -m http.server 8765`, then visit `http://localhost:8765`.

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
