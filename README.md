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

`kind` is `log` (building the tools), `guide` (explaining something, usually
with a figure) or `note` (short, one idea). A post can also join an ordered
run:

```yaml
kind: guide
series:
  id: seeing-deep-learning   # keys src/data/series.ts
  part: 2
```

A series gets its own index at `/blog/series/<id>/`, and each part gets a
header saying where it sits plus links to the parts either side. The filename
is the URL. Nothing else is needed: the list page, the RSS feed, the sitemap,
the JSON-LD and the Open Graph card all derive from the frontmatter at build
time.

Drafts stay out of the build but `astro dev` shows them. To see one with its
real Korean type - the subsetter runs over `dist/`, not the dev server - build
with `DRAFTS=1 npm run build`.

Figures are inline SVG in the Markdown, styled by `src/styles/figure.css` so
they use the page's own colours and work in both themes. Two rules: no blank
lines inside the `<figure>` block, or Markdown ends the HTML block and parses
the rest of the SVG as text; and any class carrying weight 600 must be listed
in `BOLD_CLASSES` in `tools/post-build.py`, or its Korean lands in the wrong
subset.

## One source of data

`src/data/work.ts` holds the projects. The board on the home page renders from
it, and so does `/work.json` - a real file, which is what the `raw` tab shows.
There is no second copy of the content, so the two views cannot drift. Adding a
project means editing that one array.

## Type

The page ships IBM Plex (OFL, see `public/fonts/OFL.txt`) rather than falling back to
system fonts, so it renders the same on Windows and macOS. `public/fonts/*.woff2`
are committed and total about 57 KB. Only weights 400/600 sans and 400/500 mono
are shipped - asking for anything else makes the browser synthesise it.

Korean is never shipped whole: a full face is 2.7 MB. After `astro build`,
`tools/post-build.py` reads each built page, collects the Hangul it actually
contains, and cuts a subset for that page alone - declared under the same
family name with a Hangul `unicode-range`, so the browser picks it per
character and the font stack needs no changes. A Korean post costs tens of
kilobytes; an English one costs nothing.

Each page's Hangul is split by the weight it will be asked for, read off the
tags and classes in the markup. If that split were wrong the character would
not disappear - font matching would quietly serve it from the other weight, at
the wrong thickness. `npm run check:fonts` asks a real browser what the cascade
resolved for every text node and compares it against the shipped subsets; CI
runs it on every deploy.

`python tools/make-fonts.py` refetches everything (needs `fonttools` and
`brotli`) and caches the unsubset TrueType sources under `tools/.fonts/`,
which the icon and card scripts need. `--cache-only` fetches those sources and skips regenerating the shipped
subsets, which is what CI wants - the subsets are committed on purpose.

## Marks and cards

`public/favicon.svg` is the source of truth for the mark. `favicon.ico`,
`apple-touch-icon.png` and the site's Open Graph card come from
`python tools/make-icons.py` (Pillow, plus the font cache above) - re-run it
after changing the mark, and keep the geometry in the SVG and the script in
step by hand. Per-post cards are drawn during the build instead, by
`tools/post-build.py`.

## Analytics, view counts and comments

All three live in `src/config.ts`, and all three are off. Off means nothing
renders - no markup, no stylesheet, no request - so the pages stay exactly as
fast as they are now until each one is switched on deliberately.

| what | switch | needs first |
|---|---|---|
| visitor stats | `analytics.goatcounter` | an account at goatcounter.com; paste the subdomain code |
| per-post view count | `views.show` (already true) | analytics on, plus "allow public access to counts" in GoatCounter |
| comments | `comments.enabled` | install github.com/apps/giscus on this repo |

GoatCounter sets no cookies and collects no personal data, so there is nothing
to put a consent banner on. Comments are GitHub Discussions in this repo, in
the Announcements category - the ids are already filled in. The iframe is not
requested until the reader scrolls near it, so a thread nobody opens costs
nothing.

The count stays hidden below 25 views. A number that small is worse than no
number.

## Getting found

`robots.txt`, a sitemap and JSON-LD ship with the build, and every page names
one canonical URL.

Beyond that the engines split in two. Bing, Yandex, Naver, Seznam and Yep all
take a push notification over IndexNow and share it with each other, so
`tools/indexnow.py` posts the sitemap's URLs to them - automatically after any
deploy that touched `src/content/`, or by hand:

```
python tools/indexnow.py                       # everything in the sitemap
python tools/indexnow.py https://.../blog/x/   # or just one
```

Ownership is proved by `public/<key>.txt`, which contains the key and nothing
else. Do not rename it without changing the key inside.

Google takes none of this. It has no push protocol, so the site has to be
registered by hand at Search Console with a Google account, and the sitemap
submitted there once. Until that happens Google will only find the site by
crawling a link to it from somewhere it already visits.

## Deploying

`.github/workflows/deploy.yml` builds on every push to `main` and publishes
`dist/` to GitHub Pages. Pages must be set to build from GitHub Actions rather
than from a branch.
