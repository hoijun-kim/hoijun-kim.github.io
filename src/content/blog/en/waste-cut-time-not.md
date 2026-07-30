---
title: "Padding waste was never about the batch"
description: "Part five measured padding waste converging on 50% once request lengths spread out. That number rested on taking requests in the order they arrive. Allow reordering and what sets the waste is not the batch size but how many are pooled."
date: 2025-10-20
lang: en
kind: guide
series:
  id: after-training
  part: 9
---

Part five reported that padding waste converges on `50%` once request lengths
spread out, because the maximum inside a batch pins to the ceiling as the batch
grows. The remedies got named and left unmeasured.

That number carried an unstated premise: **requests are taken in the order they
arrive.** Allow them to be reordered and the question changes.

## Not the batch, the pool

Fix the batch at `32` and vary only **how many requests are collected before
grouping**. Lengths are uniform from 1 to 128; the pool is sorted by length and
then cut into groups of 32 from the front.

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Padding waste against how many requests are pooled. In arrival order it does not move from 47%; sorted, it approaches zero as the pool grows">
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
<text class="tick-lbl" x="58.0" y="222" text-anchor="middle">32</text>
<line class="frame" x1="168.9" y1="206" x2="168.9" y2="210"/>
<text class="tick-lbl" x="168.9" y="222" text-anchor="middle">128</text>
<line class="frame" x1="279.7" y1="206" x2="279.7" y2="210"/>
<text class="tick-lbl" x="279.7" y="222" text-anchor="middle">512</text>
<line class="frame" x1="446.0" y1="206" x2="446.0" y2="210"/>
<text class="tick-lbl" x="446.0" y="222" text-anchor="middle">4096</text>
<text class="tick-lbl" x="252.0" y="266" text-anchor="middle">requests pooled (batch fixed at 32)</text>
<text class="tick-lbl" x="58" y="16" text-anchor="start">padding waste</text></g>
<path class="curve bad" fill="none" d="M58.0,47.5 L113.4,45.3 L168.9,49.5 L224.3,50.0 L279.7,47.6 L335.1,46.6 L446.0,45.6"/>
<path class="curve ok" fill="none" d="M58.0,47.5 L113.4,98.4 L168.9,143.5 L224.3,171.2 L279.7,187.5 L335.1,196.3 L446.0,203.5"/>
<circle cx="58.0" cy="47.5" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="58.0" cy="47.5" r="2.6"/>
<circle cx="113.4" cy="45.3" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="113.4" cy="98.4" r="2.6"/>
<circle cx="168.9" cy="49.5" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="168.9" cy="143.5" r="2.6"/>
<circle cx="224.3" cy="50.0" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="224.3" cy="171.2" r="2.6"/>
<circle cx="279.7" cy="47.6" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="279.7" cy="187.5" r="2.6"/>
<circle cx="335.1" cy="46.6" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="335.1" cy="196.3" r="2.6"/>
<circle cx="446.0" cy="45.6" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="446.0" cy="203.5" r="2.6"/>
<text class="lbl bad" x="260.0" y="38.0" text-anchor="middle">arrival order</text>
<text class="lbl ok" x="304.7" y="205.5" text-anchor="middle">sorted by length</text>
</svg>
<figcaption>Padding waste with the batch fixed at 32 and only the number of pooled requests changing. In arrival order it does not move from 47% however many arrive; sorted by length it goes from 47.4% at 32 requests to 0.7% at 4096. The batch is the same throughout.</figcaption>
</figure>

```
pooled   groups   waste (sorted)   waste (arrival)
    32        1            47.4%            47.4%
    64        2            32.2%            48.0%
   128        4            18.7%            46.8%
   256        8            10.4%            46.6%
   512       16             5.5%            47.3%
  1024       32             2.9%            47.6%
  4096      128             0.7%            47.9%
```

The batch is `32` throughout. All that changes is how many were waiting in front
of it, and the waste goes from `47.4%` to `0.7%`.

With one group, sorting achieves nothing: sort 32 requests into one group of 32
and only the order changes, not the maximum. At two groups the long ones start
separating from the short ones, and at 128 groups the spread of lengths inside a
group narrows to about one.

Arrival order does not move from `47%` however many requests turn up. The maximum
of 32 random draws is near the ceiling regardless of how many you drew from.

**Part five's `50%` was not a property of batching but the consequence of
declining to reorder.**

## The price is paid in waiting

Not free. Pooling 4096 requests means waiting for 4096 requests. The first to
arrive stands in the queue until others of similar length show up, and that time
becomes latency.

It is part five's throughput-against-latency trade with a different dial. There,
batch size bought latency; here, **waiting buys waste** - with the batch held at
`32` the whole time.

## Removing all the waste halves nothing

One more thing has to be measured. If the waste falls from `47%` to `0.7%`, does
the time follow? No.

Holding the batch at 32 and varying only the cache length:

```
cache length   time (us)
           1         723
          16         901
          32         873
          64        1171
         128        1398
```

Going from `1` to `128` adds `675 us`. So `48.3%` of a step depends on length and
`51.7%` does not: the linear layers push one token through no matter how long the
cache is, and part five's fixed overhead `a` is unchanged. **Padding attaches to
attention and nowhere else.**

So for 256 requests at batch 32, taking the waste from `46.4%` to `10.2%`
predicts a time gain of `1.24`. What was removed was `40%` of the half of a step
that depends on length at all.

Confirming that `1.24` by measurement does not resolve on this laptop.
Alternating arrival order and sorted, seven paired ratios, the median at batch 32
is `1.36` with a range of `0.87-1.68`, and at most batch sizes the range straddles
`1.0`. The first single run gave `1.22`, agreeing with the prediction nicely;
re-measuring the same configuration gave `0.91`. A number that agreed once is not
a result. The waste figures reproduce exactly given the list of lengths, which is
where these tables rest.

## What is left

Sorting is a one-shot arrangement. Requests finish at different times, so a short
one's seat stays empty until the long ones are done. Filling it immediately is
continuous batching, and this experiment did not go there.

The lengths used here are uniform from 1 to 128. Real request lengths bunch at the
short end with a long tail, where arrival-order waste would be higher and sorting
would gain more - unmeasured.

## So

- `50%` was not a property of batching. It followed from declining to reorder
- Holding the batch at `32` and growing the pool from `32` to `4096` takes the
  waste from `47.4%` to `0.7%`
- With one group sorting does nothing. It needs somewhere to separate things into
- Arrival order sits at `47%` however many arrive; the maximum of 32 draws is
  always near the ceiling
- The price is waiting. Part five bought latency with batch size; this buys waste
  with pooling
- Removing the waste does not halve the time. Only `48.3%` of a step depends on
  length
