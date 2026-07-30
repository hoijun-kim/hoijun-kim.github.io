---
title: "Waste cut 4.5-fold, time not cut at all"
description: "Part five measured 50% padding waste and left the remedy unmeasured. Sorting by length takes the waste from 46% to 10%. The time does not follow, and why comes out of only half a step depending on length."
date: 2025-10-20
lang: en
kind: guide
series:
  id: after-training
  part: 9
---

Part five left something open. Requests of different lengths in a batch must be
padded to the longest, and with lengths spread out the waste converges on `50%` -
that much was measured. The remedies were named and not measured. This part is
that.

## Grouping by length

The simplest remedy is to **put similar lengths together**. Draw 256 requests with
context lengths uniform from 1 to 128, and count the waste when grouped in arrival
order against grouped after sorting by length.

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Padding waste against batch size. Grouped in arrival order it sits near 47% regardless; sorted by length it falls as the batch shrinks">
<g class="axis">
<line x1="58" y1="206.0" x2="446" y2="206.0"/>
<text class="tick-lbl" x="49" y="209.5" text-anchor="end">0%</text>
<line x1="58" y1="172.5" x2="446" y2="172.5"/>
<text class="tick-lbl" x="49" y="176.0" text-anchor="end">10%</text>
<line x1="58" y1="139.1" x2="446" y2="139.1"/>
<text class="tick-lbl" x="49" y="142.6" text-anchor="end">20%</text>
<line x1="58" y1="105.6" x2="446" y2="105.6"/>
<text class="tick-lbl" x="49" y="109.1" text-anchor="end">30%</text>
<line x1="58" y1="72.2" x2="446" y2="72.2"/>
<text class="tick-lbl" x="49" y="75.7" text-anchor="end">40%</text>
<line x1="58" y1="38.7" x2="446" y2="38.7"/>
<text class="tick-lbl" x="49" y="42.2" text-anchor="end">50%</text>
<line class="frame" x1="58" y1="32" x2="58" y2="206"/><line class="frame" x1="58" y1="206" x2="446" y2="206"/>
<line class="frame" x1="58.0" y1="206" x2="58.0" y2="210"/>
<text class="tick-lbl" x="58.0" y="222" text-anchor="middle">8</text>
<line class="frame" x1="155.0" y1="206" x2="155.0" y2="210"/>
<text class="tick-lbl" x="155.0" y="222" text-anchor="middle">16</text>
<line class="frame" x1="252.0" y1="206" x2="252.0" y2="210"/>
<text class="tick-lbl" x="252.0" y="222" text-anchor="middle">32</text>
<line class="frame" x1="349.0" y1="206" x2="349.0" y2="210"/>
<text class="tick-lbl" x="349.0" y="222" text-anchor="middle">64</text>
<line class="frame" x1="446.0" y1="206" x2="446.0" y2="210"/>
<text class="tick-lbl" x="446.0" y="222" text-anchor="middle">128</text>
<text class="tick-lbl" x="252.0" y="266" text-anchor="middle">batch size</text>
<text class="tick-lbl" x="58" y="16" text-anchor="start">padding waste</text></g>
<path class="curve bad" fill="none" d="M58.0,64.3 L155.0,56.3 L252.0,50.7 L349.0,48.2 L446.0,47.2"/>
<path class="curve ok" fill="none" d="M58.0,197.1 L155.0,188.0 L252.0,171.9 L349.0,143.3 L446.0,101.0"/>
<circle cx="58.0" cy="64.3" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="58.0" cy="197.1" r="2.6"/>
<circle cx="155.0" cy="56.3" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="155.0" cy="188.0" r="2.6"/>
<circle cx="252.0" cy="50.7" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="252.0" cy="171.9" r="2.6"/>
<circle cx="349.0" cy="48.2" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="349.0" cy="143.3" r="2.6"/>
<circle cx="446.0" cy="47.2" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="446.0" cy="101.0" r="2.6"/>
<text class="lbl bad" x="211.7" y="38.7" text-anchor="middle">grouped in arrival order</text>
<text class="lbl ok" x="211.7" y="129.0" text-anchor="middle">sorted by length first</text>
</svg>
<figcaption>Padding waste against batch size. Grouped in arrival order it sits near 47% almost regardless of batch, while sorting by length first takes it to 2.7% at batch 8. The larger the batch, the wider the spread of lengths inside a sorted group, so the gain shrinks.</figcaption>
</figure>

```
batch    waste (arrival order)   waste (sorted by length)
    8                    42.4%                       2.7%
   16                    44.7%                       5.4%
   32                    46.4%                      10.2%
   64                    47.2%                      18.7%
  128                    47.5%                      31.4%
```

Arrival order sits near `47%` almost regardless of batch, because the maximum of
32 random draws is already close to the ceiling.

Sorting takes it to `2.7%` at batch 8. But **the gain shrinks as the batch grows**:
put 128 in a group and even sorted it holds lengths from 1 to 128 together,
leaving `31.4%`. Sorting works when the groups are small.

At batch 32 the waste goes from `46.4%` to `10.2%` - **cut 4.5-fold.**

## And the time does not follow

Cutting waste 4.5-fold ought to cut the time similarly. It does not, because
**padding only touches part of a step.**

Fixing the batch at 32 and varying only the cache length:

```
cache length   time (us)
           1         723
          16         901
          32         873
          64        1171
         128        1398
```

Going from `1` to `128` adds `675 us`, so `48.3%` of a step depends on length and
the other `51.7%` does not. The linear layers push one token through regardless of
how long the cache is, and part five's fixed overhead `a` is unchanged. **Only
attention scales with length.**

Which makes the expected gain calculable:

```
batch    mean padded length    predicted
    8            117 ->  69         1.24
   16            122 ->  71         1.25
   32            126 ->  75         1.24
   64            127 ->  83         1.20
  128            128 ->  98         1.13
```

Cutting waste `4.5`-fold buys `1.24` in time, because what was cut was `40%` of
the half of a step that depends on length at all.

## The measurement cannot confirm it

Something has to be said plainly here. Confirming that prediction by measurement
**does not resolve on this machine.**

Running arrival order and sorted alternately, taking a ratio per pair, median of
seven pairs:

```
batch    predicted    measured median    range
    8         1.24               1.08    0.73-1.30
   16         1.25               0.96    0.85-1.32
   32         1.24               1.36    0.87-1.68
   64         1.20               1.57    0.83-2.01
  128         1.13               0.98    0.91-1.14
```

Most of those ranges straddle `1.0`. A predicted `1.2` sits inside this laptop's
load wobble, so it is **neither confirmed nor refuted.** The first single run gave
`1.22`, agreeing with the prediction nicely; measuring the same configuration
again gave `0.91`. A number that agreed once is not a result.

The waste column has none of this problem. Given the list of lengths it is exactly
reproducible, so the first two columns can be trusted.

## What sorting cannot fix

Sorting has a price: to sort requests you have to **hold them and wait**. An early
request waits for others of similar length, and the latency grows by that much.
Part five's throughput-against-latency trade returns here.

And sorting is a one-shot arrangement. In real serving, requests finish at
different times, so a short one's seat sits empty until the long ones are done.
Slotting a new request into that seat immediately is continuous batching, and this
experiment did not measure it.

## So

- Sorting by length before grouping cuts padding waste from `46.4%` to `10.2%` at
  batch 32, a factor of `4.5`
- It works best on small groups: `2.7%` at batch 8, still `31.4%` at batch 128
- The time does not follow. Only `48.3%` of a step depends on length, so the
  predicted gain is around `1.2`
- Even that `1.2` does not resolve on this machine; the ranges straddle `1.0`
- Sorting means holding requests and waiting, which costs latency
- The waste figures are deterministic and the timings are not. This part's
  conclusion rests on the former

Nine parts. This one set out to fill the hole part five left, and filling it
turned out to show the hole was smaller than it looked.
