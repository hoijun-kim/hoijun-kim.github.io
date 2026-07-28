# hoijun-kim.github.io

My personal site - https://hoijun-kim.github.io

Static single page (plain HTML/CSS/JS). Edit `index.html`.

## One source of data

The work section renders twice: `board` is the static markup, and `raw` is JSON
built at runtime by reading that same markup back out of the DOM - every field
is an element carrying `data-k` (a key path), and `data-list` marks a container
whose children are the array items. There is no second copy of the content in
the file, so the two views cannot drift apart. Adding a project means adding a
`.row` with the same attributes; the JSON follows.

The board is plain HTML, so it survives with JavaScript off - only the view
switch and the JSON hide themselves.

## Type

The page ships IBM Plex (OFL, see `fonts/OFL.txt`) rather than falling back to
system fonts, so it renders the same on Windows and macOS. Re-run
`python tools/make-fonts.py` (needs `fonttools` and `brotli`) to refetch and
re-subset it; the four `fonts/*.woff2` are committed and total about 57 KB.
Only weights 400/600 sans and 400/500 mono are shipped - asking for anything
else makes the browser synthesise it.

That script also caches the unsubset TrueType copies under `tools/.fonts/`
(untracked), which the icon script needs.

## Mark

`favicon.svg` is the source of truth. `favicon.ico`, `apple-touch-icon.png` and
the Open Graph card `og.png` are generated from a copy of its geometry - re-run
`python tools/make-icons.py` (Pillow, plus the font cache above) after changing
the mark, and keep the two geometries in step by hand.
