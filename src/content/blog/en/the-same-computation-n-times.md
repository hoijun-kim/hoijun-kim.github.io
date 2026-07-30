---
title: "The same computation, n times over"
description: "Every character drawn recomputes the whole preceding context. Adding a cache cuts the arithmetic 130-fold and the wall clock only 3-fold, and this measures where that gap comes from."
date: 2025-09-08
lang: en
kind: guide
series:
  id: after-training
  part: 2
---

Part one's generation loop looked like this.

```python
for _ in range(n):
    logits = model(idx[:, -CTX:])[:, -1, :]      # the whole context goes in
    idx = torch.cat([idx, sample(logits)], 1)
```

Append a character and then **feed everything in again from the start**. Drawing
the hundredth character recomputes the ninety-nine that were already computed on
the previous step.

The answer is still right. The causal mask means an earlier token's output does
not change no matter what gets appended after it. The property that broke things
when part thirteen removed the mask turns out here to be **the guarantee that
recomputation is unnecessary**.

## What is worth keeping

Inside a block, exactly two things are needed about the earlier tokens:
attention's `K` and `V`. The new token's `Q` only has to meet those two.

```python
q, k, v = qkv(norm(x)).split(D, dim=2)     # x is the single new token
k = torch.cat([cache_k, k], dim=2)         # append the K from earlier steps
v = torch.cat([cache_v, v], dim=2)
cache_k, cache_v = k, v
a = softmax(q @ k.transpose(-1, -2) / sqrt(dh))   # no mask needed
```

The mask disappearing is worth noticing too. The new token's `Q` is looking only
at `K`s that precede it, so there is nothing left to hide.

## Does it give the same answer

That comes before speed. Generate 128 characters from the same seed and compare.

```
character sequences identical   True
largest difference in the final logits   9.06e-06
```

The sequences match exactly. The `9e-06` left in the logits is down to the
**order** of computation: one path matrix-multiplies 128 positions at once, the
other stacks one position 128 times, so floating-point additions associate
differently. Neither is wrong; they are two roundings of the same value.

One thing to be plain about: **it is not bit-identical.** At a position where two
candidates sit at nearly equal probability, that `9e-06` could flip which
character is drawn. It merely did not here.

## The arithmetic drops 130-fold

Count the multiplications. Without a cache, step `t` pushes `t` tokens through.

```
no cache, step t     linear layers 12·t·d²      attention 2·t²·d
with cache, step t   linear layers 12·d²        attention 2·t·d
```

Summed over `n` steps, the uncached side comes to `d²n²` and `dn³` while the
cached side comes to `d²n` and `dn²`. Every term drops by a factor of `n`.

At `d=128`, three blocks and `n=256` the ratio is `134.5`. On arithmetic alone it
should be **130 times faster**.

## In practice it is 3

<figure class="fig">
<svg viewBox="0 0 460 268" role="img" aria-label="Time to generate n characters. Both axes are logarithmic; the uncached slope is 1.80 and the cached one 1.15">
<g class="axis">
<line x1="58" y1="171.8" x2="446" y2="171.8"/>
<text class="tick-lbl" x="49" y="175.3" text-anchor="end">1e2</text>
<line x1="58" y1="108.5" x2="446" y2="108.5"/>
<text class="tick-lbl" x="49" y="112.0" text-anchor="end">1e3</text>
<line x1="58" y1="45.1" x2="446" y2="45.1"/>
<text class="tick-lbl" x="49" y="48.6" text-anchor="end">1e4</text>
<line class="frame" x1="58" y1="26" x2="58" y2="210"/><line class="frame" x1="58" y1="210" x2="446" y2="210"/>
<line class="frame" x1="58.0" y1="210" x2="58.0" y2="214"/>
<text class="tick-lbl" x="58.0" y="226" text-anchor="middle">64</text>
<line class="frame" x1="155.0" y1="210" x2="155.0" y2="214"/>
<text class="tick-lbl" x="155.0" y="226" text-anchor="middle">128</text>
<line class="frame" x1="252.0" y1="210" x2="252.0" y2="214"/>
<text class="tick-lbl" x="252.0" y="226" text-anchor="middle">256</text>
<line class="frame" x1="349.0" y1="210" x2="349.0" y2="214"/>
<text class="tick-lbl" x="349.0" y="226" text-anchor="middle">512</text>
<line class="frame" x1="446.0" y1="210" x2="446.0" y2="214"/>
<text class="tick-lbl" x="446.0" y="226" text-anchor="middle">1024</text>
<text class="tick-lbl" x="252.0" y="262" text-anchor="middle">characters generated</text>
<text class="tick-lbl" x="58" y="16" text-anchor="start">time (ms)</text></g>
<path class="curve bad draw" pathLength="1" fill="none" d="M58.0,181.2 L155.0,153.9 L252.0,123.4 L349.0,89.0 L446.0,41.7"/>
<path class="curve ok draw" pathLength="1" fill="none" d="M58.0,195.7 L155.0,178.6 L252.0,153.0 L349.0,133.7 L446.0,108.4"/>
<circle cx="58.0" cy="181.2" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark reveal" cx="58.0" cy="195.7" r="2.4"/>
<circle cx="155.0" cy="153.9" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark reveal" cx="155.0" cy="178.6" r="2.4"/>
<circle cx="252.0" cy="123.4" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark reveal" cx="252.0" cy="153.0" r="2.4"/>
<circle cx="349.0" cy="89.0" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark reveal" cx="349.0" cy="133.7" r="2.4"/>
<circle cx="446.0" cy="41.7" r="2.4" style="fill:var(--ink-2)"/>
<circle class="mark reveal" cx="446.0" cy="108.4" r="2.4"/>
<text class="lbl bad reveal" x="177.2" y="97.3" text-anchor="start">no cache - n^1.80</text>
<text class="lbl ok reveal" x="274.2" y="185.9" text-anchor="start">with cache - n^1.15</text>
<text class="tick-lbl" x="442" y="38" text-anchor="end">both axes log</text>
</svg>
<figcaption>Time to generate n characters, both axes logarithmic. Without a cache the slope is 1.80; with one it is 1.15. What the cache changes is the slope rather than the constant, which is why the gap widens with length.</figcaption>
</figure>

Measured on the same model with only the length changing, taking the minimum of
at least three runs.

```
     n   no cache   with cache   measured   arithmetic
    64      71 ms        42 ms       1.70         32.9
   128     192 ms        78 ms       2.45         66.1
   256     582 ms       198 ms       2.94        134.5
   512    2031 ms       400 ms       5.08        277.5
  1024   11304 ms      1001 ms      11.29        579.9
```

At `n=256` the arithmetic promises `134.5` and the measurement gives `2.94`. Only
`2.2%` of the promise was collected.

The reason is that this model is too small. A single `d=128` matrix multiply is
nothing to a CPU, and the time goes into each line of Python and into getting a
kernel ready to launch. Three blocks times eight operations times `n` steps
launches the same number of kernels either way. **What was reduced was the
multiplication, and multiplication was not what was being paid for.**

## The cache wins anyway

Look not at the last column but at the **measured column growing**: `1.70` to
`11.29`, widening 6.6-fold while the length grew 16-fold.

Slopes make it plain. Fitting both axes in log space,

```
no cache     time ∝ n^1.80
with cache   time ∝ n^1.15
```

What the cache changes is **the exponent, not the constant**. A constant factor
gets eaten by overhead; an exponent does not. Hence it looks like nothing at
short lengths and inevitably wins at long ones.

The `1.80` needs a caveat. The uncached side mixes an `n²` term with an `n³`
term, so it is not a clean power law, and the fit misses by up to `23.4%`. The
cached side misses by `10.4%`. Read them as evidence that **the slopes clearly
differ** rather than as exact exponents.

## Grow the model and the promise gets closer

If overhead is the problem, make the multiplications big. Fixing `n=256` and
growing only the width:

```
      d   no cache   with cache   measured   arithmetic   collected
    128     583 ms       195 ms       2.99        134.5        2.2%
    256    1203 ms       265 ms       4.54        131.7        3.4%
    512    3163 ms       415 ms       7.63        130.2        5.9%
   1024   10918 ms      1048 ms      10.42        129.4        8.1%
```

The arithmetic ratio barely moves from `130` while the measurement climbs from
`2.99` to `10.42`, and the collected share goes from `2.2%` to `8.1%`. The bigger
the multiplications, the more of the saved multiplication comes back as time.

Real models run `d` around 4096 across dozens of blocks. At that size overhead is
a negligible share and the cache's benefit attaches to the arithmetic. What this
experiment shows is that **a speedup measured on a small model does not transfer
to a large one**.

## The price is memory

A cache is not free. Every block has to hold a `K` and a `V` for every token.

```
cache size = 2 × blocks × tokens × d × bytes
```

For this model in float32,

```
n =  128    0.38 MB
n =  512    1.50 MB
n = 1024    3.00 MB
weights     2.43 MB   (637,156 × 4 bytes)
```

At `n=1024` the **cache is 1.23 times the size of the weights**. Running a 637k
parameter model requires storing more than the model itself.

At real scale it is worse. `d=4096`, 32 blocks, `n=8192` in float16 comes to
`4.0 GB`. This is why current models let several heads share one `K` and `V`
instead of giving each its own (GQA, MQA) - part ten's price for splitting heads,
recomputed here.

## So

- Re-feeding the context every step is correct, thanks to the causal mask, and
  wasteful. Only two things per block are needed: `K` and `V`
- The result is the same. Sequences match exactly and the logits differ by
  `9.06e-06`, a rounding from addition order. It is not bit-identical
- The arithmetic falls `134.5`-fold at `n=256` while the clock falls `2.94`-fold,
  collecting `2.2%`. On a small model the cost is overhead, not multiplication
- What the cache changes is nonetheless the exponent: `n^1.80` against `n^1.15`.
  At length it must win
- Growing the width from `128` to `1024` lifts the collected share from `2.2%` to
  `8.1%`
- The price is memory: at `n=1024`, `3.00 MB` of cache against `2.43 MB` of
  weights, and `4.0 GB` at real scale

Next time that memory gets attacked directly: what survives and what disappears
when the weights go from float32 to int8.
