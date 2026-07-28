#!/usr/bin/env python3
"""Prove no character on the built site falls out of the shipped type.

tools/post-build.py splits each page's Hangul by the weight it will be asked
for, from the tag and class names in the markup. If that split is wrong the
character is not lost - font matching quietly serves it from the family's
other weight - so it renders at the wrong thickness, which is easy to ship
without noticing.

A real browser reports what the cascade resolved for every text node; the
comparison against the shipped subsets happens here, on the cmaps. Asking
FontFaceSet.check() instead would be circular: it matches exactly the way
rendering does, and approves the substitution this is meant to catch.

Run after a build, from the repo root:  python tools/check-fonts.py
Set CHROME to override the browser path. Exits non-zero on the first gap.
"""

from __future__ import annotations

import functools
import html
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

HARNESS = """<!doctype html><meta charset=utf-8>
<style>iframe{width:1100px;height:800px;border:0}</style>
<iframe id="f" src="__PAGE__"></iframe><pre id="out">PENDING</pre>
<script>
document.getElementById("f").addEventListener("load", function () {
  const w = this.contentWindow, d = this.contentDocument;
  try {
    // Measuring before the stylesheet applies reports every weight as the UA
    // default, which looks exactly like a mis-split. Refuse to report instead.
    const styled = /Plex/.test(w.getComputedStyle(d.body).fontFamily);
    const sheets = [...d.styleSheets].filter((s) => { try { return s.cssRules.length } catch (e) { return false } });
    const asked = d.querySelectorAll('link[rel="stylesheet"],style').length;
    if (!styled || sheets.length < asked) {
      document.getElementById("out").textContent =
        "UNSTYLED body=" + w.getComputedStyle(d.body).fontFamily +
        " applied=" + sheets.length + "/" + asked;
      return;
    }
    // What the cascade actually resolved, per text node. Reported raw: the
    // comparison against the shipped subsets happens in Python, because
    // FontFaceSet.check() matches the same way rendering does and would
    // happily approve a character served by the wrong weight.
    const walker = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT);
    const wanted = {};                      // "family|weight" -> chars
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const text = n.nodeValue.replace(/\s+/g, "");
      const el = n.parentElement;
      if (!text || !el || el.closest("script,style")) continue;
      const cs = w.getComputedStyle(el);
      const family = cs.fontFamily.split(",")[0].replace(/["']/g, "");
      if (!/^Plex/.test(family)) continue;
      const key = family + "|" + cs.fontWeight;
      wanted[key] = (wanted[key] || "") + text;
    }
    for (const k in wanted) wanted[k] = [...new Set(wanted[k])].join("");
    document.getElementById("out").textContent =
      JSON.stringify({ measured: d.location.pathname, fonts: wanted });
  } catch (e) {
    document.getElementById("out").textContent = "HARNESS ERROR " + e.message;
  }
});
</script>
"""


HANGUL = re.compile("[ᄀ-ᇿ㄰-㆏ꥠ-꥿가-힣ힰ-퟿]")


@functools.lru_cache(maxsize=None)
def cmap_of(path: Path) -> frozenset[int]:
    from fontTools.ttLib import TTFont

    return frozenset(TTFont(str(path)).getBestCmap())


def compare(page: Path, resolved: dict[str, str]) -> list[str]:
    """Every Hangul character must be in the subset for the weight it resolved
    to. Matching within a family would quietly serve it from the other weight,
    which renders the wrong thickness rather than nothing - so this compares
    the sets directly instead of asking the browser."""
    stem = "-".join(page.relative_to(DIST).parts[:-1]) or "index"
    gaps = []

    for key, text in resolved.items():
        family, weight = key.split("|")
        hangul = {c for c in text if HANGUL.match(c)}
        if not hangul:
            continue
        # the mono family only ever ships the regular Korean face
        want = "400" if family == "Plex Mono" else ("600" if int(weight) >= 550 else "400")
        subset = DIST / "fonts" / "ko" / f"{stem}-{want}.woff2"
        if not subset.exists():
            gaps.append(f"{family} {weight} needs {subset.name}, which was not written")
            continue
        missing = sorted(c for c in hangul if ord(c) not in cmap_of(subset))
        if missing:
            gaps.append(f"{family} {weight} missing {''.join(missing)} from {subset.name}")
    return gaps


def run(browser: str, profile: str, port: int, name: str) -> str:
    out = subprocess.run(
        [
            browser, "--headless=new", "--disable-gpu", "--no-first-run",
            f"--user-data-dir={profile}", "--virtual-time-budget=20000",
            "--dump-dom", f"http://127.0.0.1:{port}/{name}",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    body = re.search(r'<pre id="out">(.*?)</pre>', out, re.S)
    return html.unescape(body.group(1).strip()) if body else ""


def chrome() -> str:
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("no Chrome found - set CHROME to its path")


def serve() -> http.server.ThreadingHTTPServer:
    """Bound to an OS-chosen port: a fixed one lets a previous run's socket
    linger and answer for the build that is no longer on disk."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    handler.log_message = lambda *a, **k: None  # type: ignore[method-assign]
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main() -> None:
    # the whole point of the report is naming Korean characters
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

    if not DIST.is_dir():
        sys.exit("no dist/ - build first")

    # The latin subsets are static and identical on every page; only Hangul is
    # cut per page and per weight, so only Hangul pages have a claim to test.
    pages = [
        p
        for p in sorted(DIST.rglob("*.html"))
        if not p.name.startswith("__check") and HANGUL.search(p.read_text(encoding="utf-8"))
    ]
    if not pages:
        print("no page contains Hangul - nothing to check")
        return
    browser = chrome()
    server = serve()
    port = server.server_address[1]
    profile = tempfile.mkdtemp(prefix="fontcheck-")
    failed = False

    try:
        for n, page in enumerate(pages):
            url = "/" + page.relative_to(DIST).as_posix().replace("index.html", "")
            # A fresh name per page: one shared harness URL gets revalidated to
            # a 304 and the browser re-measures the page it saw last, which
            # looks exactly like a font gap on whichever page follows.
            name = f"__check-{n}.html"
            (DIST / name).write_text(HARNESS.replace("__PAGE__", url), encoding="utf-8")
            raw = run(browser, profile, port, name)
            if raw.startswith("UNSTYLED"):
                # the page was measured before its stylesheet applied; that is a
                # harness problem, not a font problem, so try again
                attempts = 2
                while attempts and raw.startswith("UNSTYLED"):
                    attempts -= 1
                    raw = run(browser, profile, port, name)
            if not raw or raw.startswith(("HARNESS ERROR", "UNSTYLED")) or raw == "PENDING":
                failed = True
                print(f"FAIL {url:<34} {raw or 'NO RESULT'}")
                continue

            payload = json.loads(raw)
            # Proof that the browser measured the page we asked about: a cached
            # harness would silently re-measure the previous one.
            if payload.get("measured") != url:
                failed = True
                print(f"FAIL {url:<34} measured {payload.get('measured')} instead")
                continue

            gaps = compare(page, payload["fonts"])
            failed = failed or bool(gaps)
            print(
                f"{'FAIL' if gaps else 'ok  '} {url:<34} "
                + ("; ".join(gaps) if gaps else "every character served by the face it asks for")
            )
    finally:
        for leftover in DIST.glob("__check-*.html"):
            leftover.unlink(missing_ok=True)
        server.shutdown()
        shutil.rmtree(profile, ignore_errors=True)

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
