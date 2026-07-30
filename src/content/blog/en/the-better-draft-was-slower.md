---
title: "The better the draft, the slower it got"
description: "Speculative decoding has a cheap model write several characters ahead and an expensive one check them in a single pass. This measures whether the output distribution really survives, and why a draft with 0.9 acceptance loses to one with 0.29."
date: 2025-09-20
lang: en
kind: guide
series:
  id: after-training
  part: 4
---

In part two, every character required one pass through the target model. Adding a
cache does nothing about that: **the number of passes still equals the number of
characters.**

Speculative decoding attacks the count. A cheap model writes `k` characters
ahead, and the expensive model checks all `k+1` positions in **one** pass.
Whatever matched is kept and everything from the first mismatch is thrown away.

It comes with a claim that sounds too good: **the output distribution is exactly
what the target alone would have produced.** Given that part three's int8 moved
the loss by `0.0017` and still diverged the text at the twenty-second character,
that deserves checking first.

## Why the distribution survives

Say the draft proposed `x` with draft probability `q(x)` against target
probability `p(x)`. The whole rule is this.

```python
if rand() < min(1, p[x] / q[x]):
    accept(x)
else:
    resid = (p - q).clamp_min(0)
    emit(sample(resid / resid.sum()))     # and discard the rest
    break
```

Where `q` proposed `x` more often than `p` wanted it, only that fraction is kept;
where it is rejected, the replacement is drawn from `max(0, p-q)`, the part `p`
wanted and `q` under-supplied. The two cases together come to exactly `p`.

Measured rather than argued. Fixing a context and drawing the first character
20000 times, against the target distribution:

```
bigram draft            total variation 0.0158
4-bit draft             total variation 0.0095
sampling the target     total variation 0.0134     <- baseline at the same count
```

Right at the baseline. Twenty thousand draws carry that much sampling error
anyway, and what speculative decoding adds sits inside it. **However bad the
draft model is, the output belongs to the target.**

## Three drafts

Three drafts, all of them already in this series.

- **bigram**: part one's baseline, a table lookup on the previous character
- **8-bit**: part three's weights flattened to int8
- **4-bit**: part three's, one step from collapse

## Acceptance follows draft quality

```
  draft      k   acceptance   chars per target pass   target passes
bigram       1        0.290                    1.29             155
bigram       8        0.059                    1.47             136
8-bit        1        0.896                    1.89             106
8-bit        8        0.610                    5.88              34
4-bit        1        0.653                    1.65             121
4-bit        8        0.351                    3.77              53
```

As expected. The 8-bit draft is nearly the target itself and gets `0.896`
accepted; the bigram gets `0.290`. Raising `k` lowers acceptance - the context
drifts further out with each drafted character - while raising the characters
harvested per pass.

At `k=8` the 8-bit draft takes the target from **200 passes down to 34**, `5.88`
characters each. If part two's cache changed the exponent, this divides the
constant by six.

## And in practice the 8-bit draft is the slowest

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Measured speedup against draft length k. Only the bigram, the worst draft, clears 1, while the quantised drafts with far higher acceptance come out slower">
<g class="axis">
<line x1="56" y1="199.5" x2="446" y2="199.5"/>
<text class="tick-lbl" x="47" y="203.0" text-anchor="end">0.4</text>
<line x1="56" y1="170.6" x2="446" y2="170.6"/>
<text class="tick-lbl" x="47" y="174.1" text-anchor="end">0.6</text>
<line x1="56" y1="141.7" x2="446" y2="141.7"/>
<text class="tick-lbl" x="47" y="145.2" text-anchor="end">0.8</text>
<line x1="56" y1="112.8" x2="446" y2="112.8"/>
<text class="tick-lbl" x="47" y="116.3" text-anchor="end">1.0</text>
<line x1="56" y1="83.8" x2="446" y2="83.8"/>
<text class="tick-lbl" x="47" y="87.3" text-anchor="end">1.2</text>
<line x1="56" y1="54.9" x2="446" y2="54.9"/>
<text class="tick-lbl" x="47" y="58.4" text-anchor="end">1.4</text>
<line class="frame" x1="56" y1="26" x2="56" y2="214"/><line class="frame" x1="56" y1="214" x2="446" y2="214"/>
<line class="frame" x1="56.0" y1="214" x2="56.0" y2="218"/>
<text class="tick-lbl" x="56.0" y="230" text-anchor="middle">1</text>
<line class="frame" x1="186.0" y1="214" x2="186.0" y2="218"/>
<text class="tick-lbl" x="186.0" y="230" text-anchor="middle">2</text>
<line class="frame" x1="316.0" y1="214" x2="316.0" y2="218"/>
<text class="tick-lbl" x="316.0" y="230" text-anchor="middle">4</text>
<line class="frame" x1="446.0" y1="214" x2="446.0" y2="218"/>
<text class="tick-lbl" x="446.0" y="230" text-anchor="middle">8</text>
<text class="tick-lbl" x="251.0" y="266" text-anchor="middle">draft length k</text>
<text class="tick-lbl" x="56" y="16" text-anchor="start">measured speedup</text>
<line class="floor" x1="56" y1="112.8" x2="446" y2="112.8"/>
<text class="tick-lbl" x="442" y="106.8" text-anchor="end">1.0 = break even</text></g>
<polygon class="spread ok" points="56.0,138.2 186.0,115.3 316.0,85.9 446.0,100.9 446.0,60.2 316.0,44.5 186.0,60.1 56.0,71.2"/>
<polygon class="spread bad" points="56.0,132.3 186.0,180.2 316.0,143.7 446.0,185.4 446.0,162.4 316.0,125.8 186.0,125.4 56.0,106.5"/>
<polygon class="spread bad2" points="56.0,152.3 186.0,167.9 316.0,193.2 446.0,202.5 446.0,190.0 316.0,184.0 186.0,158.8 56.0,121.5"/>
<path class="curve ok" fill="none" d="M56.0,100.9 L186.0,98.5 L316.0,68.8 L446.0,75.1"/>
<circle cx="56.0" cy="100.9" r="2.5" style="fill:var(--accent)"/>
<circle cx="186.0" cy="98.5" r="2.5" style="fill:var(--accent)"/>
<circle cx="316.0" cy="68.8" r="2.5" style="fill:var(--accent)"/>
<circle cx="446.0" cy="75.1" r="2.5" style="fill:var(--accent)"/>
<path class="curve bad" fill="none" d="M56.0,127.7 L186.0,131.5 L316.0,141.7 L446.0,176.3"/>
<circle cx="56.0" cy="127.7" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="186.0" cy="131.5" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="316.0" cy="141.7" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="446.0" cy="176.3" r="2.5" style="fill:var(--ink-2)"/>
<path class="curve bad2" fill="none" d="M56.0,148.6 L186.0,160.2 L316.0,190.5 L446.0,198.3"/>
<circle cx="56.0" cy="148.6" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="186.0" cy="160.2" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="316.0" cy="190.5" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="446.0" cy="198.3" r="2.5" style="fill:var(--ink-2)"/>
<text class="lbl ok" x="316.0" y="57.4" text-anchor="middle">bigram draft</text>
<text class="lbl bad" x="316.0" y="157.7" text-anchor="middle">8-bit draft</text>
<text class="lbl bad" x="186.0" y="176.5" text-anchor="middle">4-bit draft</text>
</svg>
<figcaption>Measured speedup against draft length k. The line is the median of five interleaved pairs and the band is the min to max. Only the bigram, with the lowest acceptance, clears 1, while the 8-bit draft at 0.9 acceptance falls to 0.56. What sets the sign is the draft's cost, not its acceptance.</figcaption>
</figure>

```
  draft      k   chars per pass   measured   range
bigram       4             1.39       1.30   1.19-1.47
bigram       8             1.47       1.26   1.08-1.36
8-bit        4             4.35       0.80   0.79-0.91
8-bit        8             5.88       0.56   0.50-0.66
4-bit        8             3.77       0.41   0.38-0.47
```

**The one that cut target passes 5.9-fold came out 0.56 times as fast.** The
bigram, which cut them by barely 1.47, runs `1.26` times faster.

The reason is what the draft costs. Timing one drafted character against one
target pass:

```
one target pass              1235 us
one bigram character            5 us    c = 0.004
one 8-bit character          1307 us    c = 1.059
one 4-bit character          1276 us    c = 1.034
```

`c = 1.059`. **The 8-bit draft is more expensive than the target.** So at `k=8`,
saving one target pass costs eight draft passes, and those eight cost what eight
target passes would.

Re-reading part three makes this obvious. What int8 saved there was **memory**:
`2.43 MB` became `0.62 MB`, and nothing at all was claimed about time. The
multiplications still run in float32 with the weights merely rounded. Reading
quantisation as a speed win produces exactly this mistake.

## A formula that holds

For the first time in this series, a simple expression matched the measurement.

```
speedup = (chars per target pass) / (1 + k · c)
```

What one target pass yields on top, what was paid in draft calls to get it
underneath.

```
  draft      k   predicted   measured median
bigram       2        1.36              1.10
bigram       4        1.37              1.30
8-bit        2        0.87              0.87
8-bit        4        0.83              0.80
8-bit        8        0.62              0.56
4-bit        2        0.67              0.67
4-bit        4        0.49              0.46
4-bit        8        0.41              0.41
```

For the quantised drafts it holds to the second decimal. For the bigram it runs a
little generous, because `c` was timed from a single call and leaves out the
Python loop around it - and with a cost that small, that share looks large.

Set this against part two, where the arithmetic promised `134.5` and the
measurement gave `2.94`. The difference is **what went into the count**: there,
only multiplications; here, everything that was paid.

## A note on the timings

The timings in this part were untrustworthy at first. The same baseline read
`749 ms` on one run and `448 ms` on the next, because the laptop's load moves.

So the baseline and the speculative run were measured **alternately**, a ratio
taken per pair, and the median of five pairs reported. Drift hits both sides of a
ratio and cancels. The range column is the min and max of those five, and some,
like the bigram at `k=1`, are as wide as `0.82-1.29`. The band in the figure is
that width.

Acceptance rates and pass counts are deterministic given the seed and have none
of this problem, which is why this part's conclusion leans on those rather than
on the clock.

## So

- Speculative decoding does not change the output distribution: total variation
  `0.0158` and `0.0095` against a same-sample-count baseline of `0.0134`
- A better draft raises acceptance. 8-bit reaches `0.896`, the bigram `0.290`
- Target passes drop a lot. At `k=8` the 8-bit draft takes 200 down to 34, `5.88`
  characters per pass
- And that one is the slowest, at `0.56`. The draft costs more than the target,
  with `c` at `1.059`
- The only draft that actually wins is the worst one: the bigram at `1.26`, with
  `c = 0.004`
- What sets the sign is not acceptance but the draft's cost:
  `(chars per pass) / (1 + k·c)`

Four parts: the rule for choosing, how not to compute twice, the price of
throwing away precision, and the price of writing ahead.

Next time returns to the gap part two could not explain. If overhead is what is
being paid for, how large is that share exactly - and is there a way to take it
back.
