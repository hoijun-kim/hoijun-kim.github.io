---
title: "Shipping Korean type only to the posts that need it"
description: "A Korean webfont costs dozens of times what a latin one does. Cut each post a subset containing only the characters it actually uses and an English post pays nothing while a Korean one pays tens of kilobytes."
date: 2026-07-28
lang: en
kind: log
---

This site ships IBM Plex Sans for latin text rather than falling back to
whatever the operating system has. Four faces, 57 KB together. That is cheap for
the same page rendering the same way everywhere.

Korean is a different matter. Carry all 11,172 precomposed syllables and one
face is over 4 MB. Nobody should download that to read one post.

## Cut it per post

The method is simple. After the build, read each post's HTML, collect the Hangul
codepoints that actually appear in it, and cut a subset for that post alone.

```python
chars = set(re.findall(r"[가-힣ㄱ-ㅎㅏ-ㅣ]", html))
subset(font, unicodes=chars, output=f"fonts/ko/{slug}.woff2")
```

A post like this one uses a few hundred characters. The subset comes out at
roughly one percent of the original, and a post written in English carries no
Korean face at all.

## The price

Editing a post means rebuilding its font. That is the build's job, so it costs no
attention - but editing the HTML by hand without a build is no longer possible.

And a subset is valid only for its own post. Read several in a row and each one
fetches a new font. Once there are dozens of posts it would be better to fetch a
shared subset of the 2,350 common syllables first and fill in the rest per post.
With two posts that optimisation is premature.

## Choosing the face

**IBM Plex Sans KR**. Same family as the latin, so the voice does not split, and
OFL, so self-hosting is fine. Better than adding one more typeface to the mix.
