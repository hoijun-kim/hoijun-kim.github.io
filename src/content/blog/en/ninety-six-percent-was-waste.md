---
title: "96% of a batch of one was waste"
description: "Part two found that what was being paid for was overhead, not multiplication. This puts a number on that share and then converts it into throughput by batching. The price is latency."
date: 2025-09-26
lang: en
kind: guide
series:
  id: after-training
  part: 5
---

In part two the cache cut the arithmetic `134.5`-fold and the clock only
`2.94`-fold. The diagnosis was that on a small model the cost is overhead rather
than multiplication. This part nails that share down and then takes it back.

## Split the cost of one step by batch

Time one character out of a filled cache, changing only the batch size. The
requests in a batch are unrelated and get handled in the same step.

```
    B   step (us)   throughput (chars/s)   latency per request (us)
    1         434                   2302                       434
    8         655                  12214                       655
   32         929                  34431                       929
  128        2565                  49899                      2565
  256        4811                  53207                      4811
```

The batch grew 256-fold and the step only lengthened `11.1`-fold. All of that
difference becomes throughput: `2302` to `53207` characters a second, `23.1`
times.

## a and b

Time is nearly linear in the batch, so it splits into two terms.

```
t = a + b · B
```

`a` is what gets paid regardless of batch size - interpreting each line of
Python, getting kernels ready, allocating tensors. `b` is the multiplication one
extra request actually adds. Fitting by least squares:

```
a = 456.4 us     b = 16.88 us     fit error at most 9.7%
```

Those two numbers are the whole of this part.

**At batch 1, 96.4% of the step is overhead.**

```
batch   arithmetic   overhead
    1         3.6%      96.4%
    8        22.8%      77.2%
   27        50.0%      50.0%
   64        70.3%      29.7%
  256        90.4%       9.6%
```

Part two's line about reducing the multiplication when multiplication was not
what was being paid for is `3.6%` against `96.4%`. What the cache saved was under
four percent of a step, so `134.5` collapsing to `2.94` follows.

`a/b = 27` reads out of the same two numbers: **at batch 27 the arithmetic equals
the overhead.** Below it the machine is idling; above it, it is computing.

Saturation throughput is `1/b`, or `1e6 / 16.88 = 59250` characters a second. No
batch size gets past that line, and batch 256 is already at `53207`, `90%` of it.

## Throughput and latency do not move together

<figure class="fig">
<svg viewBox="0 0 460 276" role="img" aria-label="Throughput and per-request latency against batch size. Throughput saturates while latency keeps climbing">
<g class="axis">
<line x1="58" y1="214.0" x2="404" y2="214.0"/>
<text class="tick-lbl" x="49" y="217.5" text-anchor="end">0k</text>
<line x1="58" y1="151.3" x2="404" y2="151.3"/>
<text class="tick-lbl" x="49" y="154.8" text-anchor="end">20k</text>
<line x1="58" y1="88.7" x2="404" y2="88.7"/>
<text class="tick-lbl" x="49" y="92.2" text-anchor="end">40k</text>
<line x1="58" y1="26.0" x2="404" y2="26.0"/>
<text class="tick-lbl" x="49" y="29.5" text-anchor="end">60k</text>
<text class="tick-lbl" x="413" y="185.4" text-anchor="start">500</text>
<text class="tick-lbl" x="413" y="141.9" text-anchor="start">1000</text>
<text class="tick-lbl" x="413" y="98.4" text-anchor="start">2000</text>
<text class="tick-lbl" x="413" y="54.9" text-anchor="start">4000</text>
<line class="frame" x1="58" y1="26" x2="58" y2="214"/><line class="frame" x1="58" y1="214" x2="404" y2="214"/>
<line class="frame" x1="404" y1="26" x2="404" y2="214"/>
<line class="frame" x1="58.0" y1="214" x2="58.0" y2="218"/>
<text class="tick-lbl" x="58.0" y="230" text-anchor="middle">1</text>
<line class="frame" x1="144.5" y1="214" x2="144.5" y2="218"/>
<text class="tick-lbl" x="144.5" y="230" text-anchor="middle">4</text>
<line class="frame" x1="231.0" y1="214" x2="231.0" y2="218"/>
<text class="tick-lbl" x="231.0" y="230" text-anchor="middle">16</text>
<line class="frame" x1="317.5" y1="214" x2="317.5" y2="218"/>
<text class="tick-lbl" x="317.5" y="230" text-anchor="middle">64</text>
<line class="frame" x1="404.0" y1="214" x2="404.0" y2="218"/>
<text class="tick-lbl" x="404.0" y="230" text-anchor="middle">256</text>
<text class="tick-lbl" x="231.0" y="270" text-anchor="middle">batch size</text>
<text class="tick-lbl" x="58" y="16" text-anchor="start">throughput (chars/s)</text>
<text class="tick-lbl" x="404" y="16" text-anchor="end">latency (us)</text>
<line class="floor" x1="263.6" y1="26" x2="263.6" y2="214"/>
<text class="tick-lbl" x="269.6" y="39" text-anchor="start">a/b = 27</text>
<line class="floor" x1="58" y1="28.3" x2="404" y2="28.3"/>
<text class="tick-lbl" x="64" y="43.3" text-anchor="start">saturation 1/b = 59250</text></g>
<path class="curve ok" fill="none" d="M58.0,206.8 L101.2,202.1 L144.5,192.2 L187.8,175.7 L231.0,142.9 L274.2,106.1 L317.5,82.9 L360.8,57.7 L404.0,47.3"/>
<path class="curve bad" fill="none" d="M58.0,190.8 L101.2,178.6 L144.5,173.2 L187.8,165.0 L231.0,160.4 L274.2,143.0 L317.5,111.8 L360.8,79.3 L404.0,39.9"/>
<circle class="mark" cx="58.0" cy="206.8" r="2.4"/>
<circle cx="58.0" cy="190.8" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="101.2" cy="202.1" r="2.4"/>
<circle cx="101.2" cy="178.6" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="144.5" cy="192.2" r="2.4"/>
<circle cx="144.5" cy="173.2" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="187.8" cy="175.7" r="2.4"/>
<circle cx="187.8" cy="165.0" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="231.0" cy="142.9" r="2.4"/>
<circle cx="231.0" cy="160.4" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="274.2" cy="106.1" r="2.4"/>
<circle cx="274.2" cy="143.0" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="317.5" cy="82.9" r="2.4"/>
<circle cx="317.5" cy="111.8" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="360.8" cy="57.7" r="2.4"/>
<circle cx="360.8" cy="79.3" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark" cx="404.0" cy="47.3" r="2.4"/>
<circle cx="404.0" cy="39.9" r="2.4" style="fill:var(--ink-2)"/>
<text class="lbl ok" x="244.9" y="94.1" text-anchor="middle">throughput</text>
<text class="lbl bad" x="144.5" y="162.2" text-anchor="middle">latency per request</text>
</svg>
<figcaption>Throughput (left axis) and per-request latency (right axis, log) against batch size. Throughput saturates near 50k characters a second while latency climbs all the way. The vertical line is a/b = 27, where the arithmetic equals the fixed overhead.</figcaption>
</figure>

Throughput on the left axis, per-request latency on the right. The throughput
curve lies down and the latency curve climbs all the way.

This is the actual dial in inference serving. Raising the batch **raises
characters per second and lengthens what one person waits for**: `434 us` at
batch 1 against `4811 us` at 256, `11.1` times. Throughput of `23.1` was bought
with latency of `11.1`.

Which side is right depends on what is being sold. For a screen someone is
talking to, latency is everything; for a job left running overnight, throughput
is. Same model, same weights, and the batch size alone changes its character.

## With mixed lengths, half of it is padding

So far every request in a batch has been the same length. Real ones are not.
Attention needs the batch as one tensor, so it **pads to the longest** and the
shorter requests' share is discarded.

Drawing context lengths uniformly from 1 to 128:

```
batch   mean length   max length   waste
    1          64.0         63.5    0.0%
    4          64.1        103.0   37.5%
   16          64.5        121.4   46.6%
   64          64.4        126.5   49.0%
  256          64.5        127.8   49.5%
```

Growing the batch leaves the mean where it is and **pushes the maximum against
the ceiling**, so the waste converges on `50%` - which is what a uniform
distribution's mean being half its ceiling implies.

Batch 256 raised throughput `23.1`-fold in the previous section, but with lengths
spread like this, half of that went into computing padding. The effective
throughput is cut accordingly.

Removing that waste is what real serving systems do: group requests of similar
length, slot a new request into a finished seat immediately (continuous
batching), or concatenate without padding and track the boundaries separately.
This experiment measures the need for that and does not measure the remedies.

## A note on the measuring

`a` and `b` were timed on this laptop's CPU with four threads and a randomly
filled cache. What transfers is not the two numbers but **the way of measuring
them**. On another machine, another model size, or a GPU, `a` and `b` are
completely different and so is `a/b`.

Whether `b` is really constant in the batch needs a caveat too. The fit misses by
up to `9.7%`, which is not small, and at large batches cache locality worsens and
bends `b` upward. Summarising as two linear terms is an approximation, and
`a/b = 27` should be read as **an order of magnitude**, not a precise boundary.

## So

- The cost of one step splits as `t = a + b·B`, here `a = 456.4 us` and
  `b = 16.88 us`
- At batch 1, `96.4%` of the step is overhead. That number is part two's diagnosis
- At `a/b = 27` the arithmetic catches up with the overhead. Below it the machine
  idles
- Batch 256 gives `23.1` times the throughput for `11.1` times the latency.
  Saturation is `1/b`, `59250` characters a second
- With spread lengths, growing the batch converges the padding waste on `50%`
- The two numbers belong to this machine. What transfers is the way of measuring

Five parts: the rule for choosing, how not to compute twice, the price of
throwing away precision, the price of writing ahead, and the price of handling
many at once.

Next time takes up the other problem part two left behind. The cache outgrew the
weights, so what breaks when the oldest entries get thrown away.
