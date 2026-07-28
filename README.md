# hoijun-kim.github.io

My personal site and blog - https://hoijun-kim.github.io

Astro, no UI framework. The pages ship as static HTML with a few dozen lines of
JavaScript; nothing on the site needs script to be readable.

```
npm install
npm run dev      # local, with hot reload
npm run build    # astro build, then tools/post-build.py over dist/
```

## Writing a post

Drop a Markdown file in `src/content/blog/`:

```yaml
---
title: "What broke and what it cost"
description: "One or two sentences - this is the search result and the card."
date: 2026-08-01
lang: ko          # en | ko, defaults to en
draft: false      # true keeps it out of the build entirely
---
```

The filename is the URL. A post needs nothing else: the list page, the RSS
feed, the sitemap, the JSON-LD and the Open Graph card are all derived from
that frontmatter at build time.

## One source of data

`src/data/work.ts` holds the projects. The board on the home page renders from
it, and so does `/work.json` - a real file, which is what the `raw` tab shows.
There is no second copy of the content, so the two views cannot drift. Adding a
project means editing that one array.

## Type

The page ships IBM Plex (OFL, see `fonts/OFL.txt`) rather than falling back to
system fonts, so it renders the same on Windows and macOS. `public/fonts/*.woff2`
are committed and total about 57 KB. Only weights 400/600 sans and 400/500 mono
are shipped - asking for anything else makes the browser synthesise it.

Korean is never shipped whole: a full face is 2.7 MB. After `astro build`,
`tools/post-build.py` reads each built page, collects the Hangul it actually
contains, and cuts a subset for that page alone - declared under the same
family name with a Hangul `unicode-range`, so the browser picks it per
character and the font stack needs no changes. A Korean post costs tens of
kilobytes; an English one costs nothing.

`python tools/make-fonts.py` refetches everything (needs `fonttools` and
`brotli`) and caches the unsubset TrueType sources under `tools/.fonts/`,
which the icon and card scripts need. `--korean-only` fetches just the Korean
sources, which is all CI wants - the latin subsets are committed on purpose.

## Marks and cards

`favicon.svg` is the source of truth for the mark. `favicon.ico`,
`apple-touch-icon.png` and the site's Open Graph card come from
`python tools/make-icons.py` (Pillow, plus the font cache above) - re-run it
after changing the mark, and keep the geometry in the SVG and the script in
step by hand. Per-post cards are drawn during the build instead, by
`tools/post-build.py`.

## Deploying

`.github/workflows/deploy.yml` builds on every push to `main` and publishes
`dist/` to GitHub Pages. Pages must be set to build from GitHub Actions rather
than from a branch.
