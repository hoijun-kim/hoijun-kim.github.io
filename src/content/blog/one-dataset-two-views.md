---
title: "One dataset, two views"
description: "This site claims that fiddly technical work should be visible and clickable. Making the claim in prose would have been the easy way out, so the work section renders itself twice from a single source instead."
date: 2026-07-28
lang: en
---

The line at the top of this site is a claim: work that usually needs a query
language should be something you can see and click. A page that only *says*
that is a page that does the opposite of what it argues, so the work section
renders twice from the same data.

## The board and the raw view

There is one array of projects. The board renders from it, and so does
`/work.json` - a real file you can fetch:

```bash
curl -s https://hoijun-kim.github.io/work.json | jq '.work[].name'
```

The `raw` tab shows the contents of that file, syntax-highlighted at build
time. Nothing is duplicated: if I add a project, both views change, because
there is only one place to change it.

## Why not just hardcode the JSON

Because then it would be a screenshot of data rather than data, and it would
rot the first time I edited one and not the other. The whole argument of the
page is that a second, hand-maintained copy of the truth is the problem.

## What it costs

About forty lines of build-time code: one module holding the projects, one
serialiser that walks a value and emits a coloured line per line of output,
and a tab that toggles two panels. The board is plain HTML, so with JavaScript
off the content is all still there - only the switch and the JSON hide
themselves.

That is the whole trick. It is a small one, but it is the difference between
arguing for something and demonstrating it.
