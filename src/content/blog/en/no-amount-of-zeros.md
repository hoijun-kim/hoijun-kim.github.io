---
title: "No amount of zeros makes it faster"
description: "Part three flattened the weights into int8. This sets them to zero instead. Which ones get zeroed decides everything, quantisation wins at every compression ratio, and zeroing 99% of them changes the clock not at all."
date: 2025-10-14
lang: en
kind: guide
series:
  id: after-training
  part: 8
---

Part three flattened the weights into int8: the values got coarser and the count
stayed. There is an opposite move - **keep the precision and cut the count**, by
setting some of them to zero.

## Which ones get zeroed

Cut the same fraction and the outcome depends entirely on which. Compare cutting
the smallest by magnitude against cutting at random.

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Validation loss against sparsity. Cutting by magnitude holds to 30%; cutting at random is already worse than the bigram at 5%">
<g class="axis">
<line x1="58" y1="200.7" x2="446" y2="200.7"/>
<text class="tick-lbl" x="49" y="204.2" text-anchor="end">2</text>
<line x1="58" y1="148.0" x2="446" y2="148.0"/>
<text class="tick-lbl" x="49" y="151.5" text-anchor="end">3</text>
<line x1="58" y1="95.3" x2="446" y2="95.3"/>
<text class="tick-lbl" x="49" y="98.8" text-anchor="end">4</text>
<line x1="58" y1="42.5" x2="446" y2="42.5"/>
<text class="tick-lbl" x="49" y="46.0" text-anchor="end">5</text>
<line class="frame" x1="58" y1="32" x2="58" y2="206"/><line class="frame" x1="58" y1="206" x2="446" y2="206"/>
<line class="frame" x1="58.0" y1="206" x2="58.0" y2="210"/>
<text class="tick-lbl" x="58.0" y="222" text-anchor="middle">0%</text>
<line class="frame" x1="187.3" y1="206" x2="187.3" y2="210"/>
<text class="tick-lbl" x="187.3" y="222" text-anchor="middle">30%</text>
<line class="frame" x1="273.6" y1="206" x2="273.6" y2="210"/>
<text class="tick-lbl" x="273.6" y="222" text-anchor="middle">50%</text>
<line class="frame" x1="359.8" y1="206" x2="359.8" y2="210"/>
<text class="tick-lbl" x="359.8" y="222" text-anchor="middle">70%</text>
<line class="frame" x1="446.0" y1="206" x2="446.0" y2="210"/>
<text class="tick-lbl" x="446.0" y="222" text-anchor="middle">90%</text>
<text class="tick-lbl" x="252.0" y="266" text-anchor="middle">fraction set to zero</text>
<text class="tick-lbl" x="58" y="16" text-anchor="start">validation loss</text>
<line class="floor" x1="58" y1="63.4" x2="446" y2="63.4"/>
<text class="tick-lbl" x="64" y="57.4" text-anchor="start">untrained 4.6052</text>
<line class="floor" x1="58" y1="166.4" x2="446" y2="166.4"/>
<text class="tick-lbl" x="442" y="160.4" text-anchor="end">bigram 2.6501</text></g>
<path class="curve ok" fill="none" d="M58.0,199.3 L101.1,198.8 L187.3,189.7 L273.6,142.7 L359.8,90.5 L402.9,66.3 L446.0,39.8"/>
<path class="curve bad" fill="none" d="M58.0,199.3 L62.3,185.6 L66.6,175.3 L79.6,140.5 L101.1,106.5 L144.2,79.7 L187.3,69.0 L273.6,71.3 L359.8,65.1 L402.9,65.0 L446.0,62.1"/>
<circle class="mark" cx="58.0" cy="199.3" r="2.5"/>
<circle class="mark" cx="101.1" cy="198.8" r="2.5"/>
<circle class="mark" cx="187.3" cy="189.7" r="2.5"/>
<circle class="mark" cx="273.6" cy="142.7" r="2.5"/>
<circle class="mark" cx="359.8" cy="90.5" r="2.5"/>
<circle class="mark" cx="402.9" cy="66.3" r="2.5"/>
<circle class="mark" cx="446.0" cy="39.8" r="2.5"/>
<circle cx="58.0" cy="199.3" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="62.3" cy="185.6" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="66.6" cy="175.3" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="79.6" cy="140.5" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="101.1" cy="106.5" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="144.2" cy="79.7" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="187.3" cy="69.0" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="273.6" cy="71.3" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="359.8" cy="65.1" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="402.9" cy="65.0" r="2.5" style="fill:var(--ink-2)"/>
<circle cx="446.0" cy="62.1" r="2.5" style="fill:var(--ink-2)"/>
<text class="lbl ok" x="316.7" y="178.6" text-anchor="middle">cut by magnitude</text>
<text class="lbl bad" x="187.3" y="119.0" text-anchor="middle">cut at random</text>
</svg>
<figcaption>Validation loss against sparsity. Cutting by magnitude holds within a tenth through 30%; cutting at random is already worse than the bigram at 5%. The two horizontal lines are part one's bigram and the untrained ln(100).</figcaption>
</figure>

```
fraction zeroed   magnitude (global)   magnitude (per layer)   random
            10%               2.0358                  2.0397   3.7873
            30%               2.2097                  2.3893   4.4976
            50%               3.1009                  3.3498   4.4543
            70%               4.0908                  4.4716   4.5714
            90%               5.0523                  5.0089   4.6292
```

The baseline is `2.0272`. By magnitude it holds to `2.2097` at `30%`; at random it
is already `3.7873` at `10%`.

Looking at the random side more finely shows how fast it goes.

```
 1%   2.2862
 2%   2.4815
 5%   3.1419
10%   3.7873
20%   4.2955
```

At `5%` it is `3.1419`, already worse than part one's bigram at `2.6501`, and by
`20%` it is `4.2955`, up against the untrained `4.6052`. **Delete one weight in
twenty at random and the model is worse than counting the previous character.**

Magnitude is different because what it cuts is already near zero. Cutting at
random removes large values with the same probability, and one of those shakes
the whole next layer.

The table also shows that **cutting globally beats cutting per layer**: `2.2097`
against `2.3893` at `30%`. Layers have different distributions of magnitude, and
forcing the same fraction on each means cutting large values out of the layers
that only have large ones.

## To match part three's loss

Compared directly against quantisation: what sparsity does it take to reach each
bit width's loss?

```
8 bits (2.0280)   sparsity  1.8%
6 bits (2.0387)   sparsity 10.3%
4 bits (2.3571)   sparsity 35.5%
```

`int8` is a `4x` compression, and reaching its loss by pruning allows cutting
`1.8%`. Deleting `1.8%` saves nothing.

## At equal space, quantisation wins

Here is pruning's trap. Zeroing half the weights does not halve the storage,
because **where the non-zeros are has to be stored too.**

```
bytes per element
float32 dense        4.00
int8 dense           1.00      (part three)
float32 50% sparse   COO 4.00 / bitmask 2.12
float32 75% sparse   COO 2.00 / bitmask 1.12
float32 90% sparse   COO 0.80 / bitmask 0.52
```

With the common value-and-index layout (COO), cutting `50%` **saves nothing at
all.** A one-bit-per-element mask does better and still costs `2.12` bytes at
`50%`.

Comparing loss at equal compression settles it.

```
int8            4.00x compression   loss 2.0280
75% sparse      3.56x               loss 4.3935     (bitmask)
50% sparse      1.88x               loss 3.1009
```

`int8` compresses more and loses `2.0280`, while pruning at a similar ratio loses
`4.3935` - worse than before training. **In this model quantisation beats pruning
at every compression ratio.**

## And it is not faster either

The other reason to prune is speed: if half the multiplications are by zero,
surely half can be skipped. Measured:

```
dense original   889 us
50% sparse       881 us   1.01x
90% sparse       885 us   1.00x
99% sparse       882 us   1.01x
```

**Zeroing 99% changes nothing.** A matrix multiply is still a dense matrix
multiply, and multiplying by zero is still multiplying. Skipping would require
checking where the zeros are, and that check costs more than the multiplication.

It is part three's story again, where int8 saved memory and not time, and part
four's, where `c = 1.059` made the 8-bit draft dearer than the target.
**Compression that touches the weights is a memory story, not a time one.**

Getting time out of it needs the zeros in a regular pattern - two out of every
four, say - so a dedicated instruction can skip them, which is what structured
sparsity means. This experiment cut without any such constraint and collects none
of that benefit.

## So

- Which ones get zeroed is everything. By magnitude, `2.2097` at `30%`; at random,
  `3.7873` at `10%`
- Deleting `5%` at random gives `3.1419`, worse than the bigram's `2.6501`
- Global beats per layer: `2.2097` against `2.3893` at `30%`
- Reaching part three's int8 loss by pruning allows cutting `1.8%`
- The zeros' positions must be stored too, so cutting `50%` saves nothing under
  COO. At equal compression, quantisation wins
- It is not faster. Zeroing `99%` gives `1.01x`. Compression is a memory story,
  not a time one

Eight parts: the rule for choosing, how not to compute twice, the price of
throwing away precision, the price of writing ahead, the price of handling many at
once, the price of choosing what to discard, the price of reading against writing,
and the price of cutting the count.

Next time takes up the place part five explicitly left open. It measured padding
waste and only named the remedies; this measures one.
