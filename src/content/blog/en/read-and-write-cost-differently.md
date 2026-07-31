---
title: "A character read costs a fortieth of one written"
description: "Same model, same weights, and reading a prompt costs 40 times less per character than producing one. Part five's a and b explain it, and so does why serving systems name the two phases separately."
date: 2025-10-08
lang: en
kind: guide
series:
  id: after-training
  part: 7
---


Two kinds of time have been measured so far: part two timed producing characters
one at a time, part five split that step by batch. One is still missing - **the
time to read the prompt**.

Hand a model some text to continue and there are two phases. First the given text
goes through in one pass to fill the cache, then characters come out one at a
time. Same weights, same operations, and wildly different cost per character.

## Fed at once, it is cheap

Time to push a prompt of `P` characters through in one pass:

```
    P   time (us)   per character (us)
    1         405                404.7
    4         489                122.3
   16         564                 35.3
   64         902                 14.1
  128        1354                 10.6
```

`P` grew 128-fold and the time only `3.3`-fold. Per character it falls from
`404.7` to `10.6`.

Part five's expression reads straight onto this. In `t = a + b·B`, the number of
characters fed at once takes the `B` slot. The fixed overhead `a` is split across
`P` of them, so the per-character cost converges on `b` as `P` grows. Reading a
prompt **is one step with a large batch**.

## Produced one at a time, it is expensive

The same model, cache filled, producing one character:

```
context 16    399 us
context 64    410 us
context 127   428 us
```

Barely moves with context length. Around `400 us`, which is where part five's
fixed overhead sat - it fitted `a = 456.4 us` from the batch sweep. **Every
character produced pays the whole fixed overhead again.** The two do not match
exactly because they were measured separately, and on this laptop absolute times
drift by about that much as a matter of course.

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Per-character time when a prompt of P characters goes in at once. It falls as P grows, down to a fortieth of one generated character">
<g class="axis">
<line x1="60" y1="194.4" x2="446" y2="194.4"/>
<text class="tick-lbl" x="51" y="197.9" text-anchor="end">10</text>
<line x1="60" y1="106.4" x2="446" y2="106.4"/>
<text class="tick-lbl" x="51" y="109.9" text-anchor="end">100</text>
<line class="frame" x1="60" y1="32" x2="60" y2="208"/><line class="frame" x1="60" y1="208" x2="446" y2="208"/>
<line class="frame" x1="60.0" y1="208" x2="60.0" y2="212"/>
<text class="tick-lbl" x="60.0" y="224" text-anchor="middle">1</text>
<line class="frame" x1="170.3" y1="208" x2="170.3" y2="212"/>
<text class="tick-lbl" x="170.3" y="224" text-anchor="middle">4</text>
<line class="frame" x1="280.6" y1="208" x2="280.6" y2="212"/>
<text class="tick-lbl" x="280.6" y="224" text-anchor="middle">16</text>
<line class="frame" x1="390.9" y1="208" x2="390.9" y2="212"/>
<text class="tick-lbl" x="390.9" y="224" text-anchor="middle">64</text>
<line class="frame" x1="446.0" y1="208" x2="446.0" y2="212"/>
<text class="tick-lbl" x="446.0" y="224" text-anchor="middle">128</text>
<text class="tick-lbl" x="253.0" y="266" text-anchor="middle">characters fed at once, P</text>
<text class="tick-lbl" x="60" y="16" text-anchor="start">time per character (us)</text>
<text class="tick-lbl" x="446" y="16" text-anchor="end">both axes log</text>
<line class="floor" x1="60" y1="50.8" x2="446" y2="50.8"/>
<text class="tick-lbl" x="442" y="64.8" text-anchor="end">generating 428 us</text></g>
<path class="curve ok" fill="none" d="M60.0,52.9 L170.3,98.7 L280.6,146.2 L390.9,181.2 L446.0,192.2"/>
<circle class="mark" cx="60.0" cy="52.9" r="2.6"/>
<circle class="mark" cx="170.3" cy="98.7" r="2.6"/>
<circle class="mark" cx="280.6" cy="146.2" r="2.6"/>
<circle class="mark" cx="390.9" cy="181.2" r="2.6"/>
<circle class="mark" cx="446.0" cy="192.2" r="2.6"/>
<text class="lbl ok" x="312.8" y="134.2" text-anchor="middle">reading the prompt</text>
</svg>
<figcaption>Per-character time when a prompt of P characters goes in at once, both axes logarithmic. The fixed overhead divides as P grows, down to 10.6 us at 128 characters. The horizontal line is the 428 us the same model takes to produce one character.</figcaption>
</figure>

```
per character read       10.6 us
per character produced    428 us
ratio                      40x
```

Same model, same multiplications, and a character read is `40` times cheaper than
one written. The difference is not the computation but **how many went in at
once**.

## Where a request spends its time

What that ratio means for an actual request - read `P` characters, write `G`:

```
   P     G   to first char (ms)   total (ms)   prompt's share
 128    16                 1.35         8.21            16.5%
 128    64                 1.35        28.77             4.7%
 128   128                 1.35        56.19             2.4%
  32   128                 0.66        55.49             1.2%
   8   128                 0.51        55.35             0.9%
```

However long the prompt, the first character arrives at `1.35 ms`, while writing
128 characters costs `55 ms`. **Reading a 128-character prompt costs what writing
two or three characters does.**

So a request with a long prompt and a short answer and one with a short prompt
and a long answer are different animals: the prompt takes `16.5%` of the first
and `0.9%` of the second.

This is why serving systems name and measure the two phases separately. Time to
the first character and time per character after it **use different resources and
optimise differently**. In part five's terms, reading the prompt is the regime
where `b` dominates and producing characters is where `a` does.

## Which is why batching is a decode-side story

Part five showed throughput rising with batch size. It is now clear which phase
that was about.

Reading a prompt already feeds `P` at once, so it is its own large batch. At
`P=128` it is already past part five's `a/b = 27` and the overhead share is
small; grouping further leaves little to gain.

Producing characters, by contrast, is **always batch 1**. One request emits one
character per step, structurally. So part five's `96.4%` overhead is a statement
about this phase, and grouping several requests into one step is what pays here.

## Notes

Every number here is the minimum of 60 runs, and all three tables use that same
estimator. The first attempt mixed minimum and median across tables, which made
reading a `P=32` prompt look more expensive than a `P=128` one. Measuring the same
quantity two ways destroys the comparison.

Carrying `a` and `b` over to prompt reading is not exact either. Part five's batch
members do not see each other, while characters inside a prompt do. Attention
grows as `P²`, so large `P` bends away from the line - and indeed going from
`P=64` to `128` costs `1.5` times, not a constant plus a straight line.

## So

- Feeding a prompt at once takes the per-character cost from `404.7` to
  `10.6 us`, because `P` characters split one fixed overhead
- Producing a character costs around `400 us` almost regardless of context. The
  overhead is paid in full every time
- A character read is `40` times cheaper than one written, on the same weights and
  the same multiplications
- Reading a 128-character prompt costs what writing two or three characters does:
  `1.35 ms` to the first character against `55 ms` for 128 of them
- Batching is a decode-side story. Reading is already a large batch; producing is
  structurally batch 1
- All three tables use one estimator. Mixing them makes `P=32` look dearer than
  `P=128`

Next time goes back to part three. There the weights got coarser; this time they
get removed, and the two are compared at equal compression.
