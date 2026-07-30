---
title: "Cut the cache and keep the beginning"
description: "Part two ended with the cache larger than the weights. Dropping the oldest entries is the obvious fix, and what gets kept decides the outcome. Keeping the first eight positions runs at 19% of the cache for almost the full-cache loss."
date: 2025-10-02
lang: en
kind: guide
series:
  id: after-training
  part: 6
---

Part two ended with the cache bigger than the weights: `3.00 MB` against `2.43 MB`
at `n=1024`, and `4.0 GB` at real scale. The longer the context, the further that
number climbs.

The simplest answer is to **throw entries away**: keep the most recent `W` and
delete the rest. The question is how much breaks.

## A window alone

On part thirteen's model, restrict position `t` to seeing only `[t-W+1, t]` and
measure validation loss.

```
window W    validation loss
       4             2.7566
       8             2.4575
      16             2.2905
      32             2.1989
      64             2.0770
    full             2.0272
```

`W=16` gives `2.2905`. Better than part one's bigram at `2.6501`, but well adrift
of the full cache's `2.0272`.

## Keeping a few from the beginning

Now add one thing: on top of the window, **always keep the first few positions.**

```
on top of W=16    validation loss
keep none                 2.2905
first 1                   2.2068
first 2                   2.1631
first 4                   2.1111
first 8                   2.0905
first 16                  2.1446
```

The first eight give `2.0905`. The full cache is `2.0272`, so the gap is `0.063`,
and the entries stored are `24` against `128` - `19%`.

```
full          128 entries    0.38 MB
W16 + first 8  24 entries    0.07 MB
```

Note that keeping the first sixteen is *worse*, at `2.1446`. Keeping more does not
keep helping.

## Is it the beginning, or just four more keys

That question has to be asked. Whether keeping four positions helped because of
**where they are or because there are four of them** needs separating.

```
on top of W=16          validation loss
keep nothing                    2.2905
first 4 (0-3)                   2.1111
middle 4 (30-33)                2.2049
middle 4 (60-63)                2.2759
just widen the window to 20     2.2655
```

**It is the beginning.** The same count taken from the middle gives `2.2759`,
almost nothing, and widening the window by four gives `2.2655`, the same. Sweeping
the position looks like this.

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Validation loss against where the four always-kept positions sit, on top of a window of 16. Earlier is better, and late enough is worse than keeping nothing">
<g class="axis">
<line x1="58" y1="200.9" x2="446" y2="200.9"/>
<text class="tick-lbl" x="49" y="204.4" text-anchor="end">2.0</text>
<line x1="58" y1="149.4" x2="446" y2="149.4"/>
<text class="tick-lbl" x="49" y="152.9" text-anchor="end">2.1</text>
<line x1="58" y1="98.0" x2="446" y2="98.0"/>
<text class="tick-lbl" x="49" y="101.5" text-anchor="end">2.2</text>
<line x1="58" y1="46.6" x2="446" y2="46.6"/>
<text class="tick-lbl" x="49" y="50.1" text-anchor="end">2.3</text>
<line class="frame" x1="58" y1="26" x2="58" y2="206"/><line class="frame" x1="58" y1="206" x2="446" y2="206"/>
<line class="frame" x1="58.0" y1="206" x2="58.0" y2="210"/>
<text class="tick-lbl" x="58.0" y="222" text-anchor="middle">0</text>
<line class="frame" x1="194.5" y1="206" x2="194.5" y2="210"/>
<text class="tick-lbl" x="194.5" y="222" text-anchor="middle">4</text>
<line class="frame" x1="298.3" y1="206" x2="298.3" y2="210"/>
<text class="tick-lbl" x="298.3" y="222" text-anchor="middle">16</text>
<line class="frame" x1="354.6" y1="206" x2="354.6" y2="210"/>
<text class="tick-lbl" x="354.6" y="222" text-anchor="middle">32</text>
<line class="frame" x1="446.0" y1="206" x2="446.0" y2="210"/>
<text class="tick-lbl" x="446.0" y="222" text-anchor="middle">96</text>
<text class="tick-lbl" x="252.0" y="266" text-anchor="middle">start of the kept block</text>
<text class="tick-lbl" x="58" y="16" text-anchor="start">validation loss</text>
<line class="floor" x1="58" y1="51.5" x2="446" y2="51.5"/>
<text class="tick-lbl" x="64" y="45.5" text-anchor="start">keep nothing 2.2905</text>
<line class="floor" x1="58" y1="186.9" x2="446" y2="186.9"/>
<text class="tick-lbl" x="64" y="180.9" text-anchor="start">full cache 2.0272</text></g>
<path class="curve ok" fill="none" d="M58.0,143.7 L116.8,139.0 L151.2,137.5 L194.5,136.2 L244.4,132.0 L298.3,124.1 L354.6,92.9 L406.7,59.0 L446.0,48.1"/>
<circle class="mark" cx="58.0" cy="143.7" r="2.6"/>
<circle class="mark" cx="116.8" cy="139.0" r="2.6"/>
<circle class="mark" cx="151.2" cy="137.5" r="2.6"/>
<circle class="mark" cx="194.5" cy="136.2" r="2.6"/>
<circle class="mark" cx="244.4" cy="132.0" r="2.6"/>
<circle class="mark" cx="298.3" cy="124.1" r="2.6"/>
<circle class="mark" cx="354.6" cy="92.9" r="2.6"/>
<circle class="mark" cx="406.7" cy="59.0" r="2.6"/>
<circle class="mark" cx="446.0" cy="48.1" r="2.6"/>
<text class="lbl ok" x="223.0" y="154.2" text-anchor="middle">the four kept</text>
</svg>
<figcaption>Validation loss when four positions are always kept on top of a window of 16, against where those four sit. The very beginning is best, it degrades steadily further in, and from 96 it is worse than keeping nothing. The two horizontal lines are keeping nothing and the full cache.</figcaption>
</figure>

```
start of kept block    validation loss
                  0             2.1111
                  1             2.1203
                  4             2.1258
                 16             2.1493
                 32             2.2100
                 60             2.2759
                 96             2.2971
```

Earlier is better, and far enough in it is **worse than keeping nothing at all**
(`2.2971` against `2.2905`).

## Attention mass does not explain it

The usual explanation here is the "attention sink": the earliest positions soak up
a large share of attention, so they must not be discarded. Measured, **this model
has no such thing.**

In normal operation, the mass later positions give to position 0:

```
block 0   0.0035     uniform from those positions would be 0.0108   ratio 0.3
block 1   0.0000                                                     0.0
block 2   0.0000                                                     0.0
```

It receives **less** than uniform. Position 0 is not a place this model looks.

Under the window it is the same story.

```
mass given to those four from later positions
first (0-3)       0.0155
middle (60-63)    0.0336
```

**The middle four take more than twice the mass and help far less.** So "keep the
positions that receive the most" does not fit what was measured.

Then why does the beginning help? **Unknown.** The measurement separates position
from count, and rules out mass, but what those positions carry is not something
this experiment answers. A plausible story could be attached; an unmeasured one
will not be written down.

The absence of a sink here does not contradict the reports from large models
either. This is a vocabulary of 100 across three blocks, trained 5000 steps on
sixty thousand characters. A phenomenon reported at scale not showing up here is
unremarkable, and this part's conclusion stops at **the beginning pays, in this
model**.

## So

- Windowing the cache costs loss: `2.2905` at `W=16` against the full `2.0272`
- Adding the first eight positions gives `2.0905` - `24` entries against `128`,
  `19%`, for a gap of `0.063`
- Keeping more does not keep helping. The first sixteen go back up to `2.1446`
- It is position, not count. The same four from the middle give `2.2759`, and
  widening the window by four gives `2.2655`
- Attention mass does not explain it. There is no sink in this model, and the
  first four receive half the mass the middle four do
- Why it works was not measured. Only that it is position, and that it is not mass

Six parts: the rule for choosing, how not to compute twice, the price of throwing
away precision, the price of writing ahead, the price of handling many at once,
and the price of choosing what to discard.

Next time measures a time nobody has measured yet in this series. Everything so
far has been the cost of producing characters; before that comes reading the
prompt.
