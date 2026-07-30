---
title: "What disappears when the weights are quartered"
description: "Part two's cache outgrew the weights, so this attacks the weights. Going from float32 to int8 costs 0.0017 of loss - and the generated text diverges at the twenty-second character."
date: 2025-09-14
lang: en
kind: guide
series:
  id: after-training
  part: 3
---

Part two ended with the cache larger than the weights. This part goes the other
way and shrinks the weights.

The method is simple. A float32 is four bytes, but knowing the range of the
values lets one integer carry each of them.

```python
qmax = 2 ** (bits - 1) - 1
scale = w.abs().max() / qmax
q = (w / scale).round().clamp(-qmax - 1, qmax)     # the integers
w_hat = q * scale                                  # unpacked again
```

Keep one float `scale` and hold the rest as int8, and four bytes become one. The
question is how much the `round` hurts.

## int8 is nearly free

Using part thirteen's model unchanged, its float32 validation loss is `2.0272`.

```
                       one scale per matrix   one scale per channel
8 bits                            2.0290                    2.0280
float32 is 2.0272
```

`+0.0017`. It barely shows in the third decimal. All 637k weights were flattened
onto 256 levels and the model hardly noticed.

The memory goes like this.

```
631,808 two-dimensional weights    2.41 MB (fp32)  ->  0.60 MB (int8)
all 637,156                        2.43 MB         ->  0.62 MB     74.4% less
```

## Squeeze further and where does it break

<figure class="fig">
<svg viewBox="0 0 460 268" role="img" aria-label="Validation loss as the weights are squeezed into fewer bits. Eight and six bits sit on the float32 line; below four it collapses">
<g class="axis">
<line x1="56" y1="206.2" x2="446" y2="206.2"/>
<text class="tick-lbl" x="47" y="209.7" text-anchor="end">2</text>
<line x1="56" y1="167.9" x2="446" y2="167.9"/>
<text class="tick-lbl" x="47" y="171.4" text-anchor="end">3</text>
<line x1="56" y1="129.5" x2="446" y2="129.5"/>
<text class="tick-lbl" x="47" y="133.0" text-anchor="end">4</text>
<line x1="56" y1="91.2" x2="446" y2="91.2"/>
<text class="tick-lbl" x="47" y="94.7" text-anchor="end">5</text>
<line x1="56" y1="52.8" x2="446" y2="52.8"/>
<text class="tick-lbl" x="47" y="56.3" text-anchor="end">6</text>
<line class="frame" x1="56" y1="26" x2="56" y2="212"/><line class="frame" x1="56" y1="212" x2="446" y2="212"/>
<line class="frame" x1="56.0" y1="212" x2="56.0" y2="216"/>
<text class="tick-lbl" x="56.0" y="228" text-anchor="middle">8</text>
<line class="frame" x1="153.5" y1="212" x2="153.5" y2="216"/>
<text class="tick-lbl" x="153.5" y="228" text-anchor="middle">6</text>
<line class="frame" x1="251.0" y1="212" x2="251.0" y2="216"/>
<text class="tick-lbl" x="251.0" y="228" text-anchor="middle">4</text>
<line class="frame" x1="348.5" y1="212" x2="348.5" y2="216"/>
<text class="tick-lbl" x="348.5" y="228" text-anchor="middle">3</text>
<line class="frame" x1="446.0" y1="212" x2="446.0" y2="216"/>
<text class="tick-lbl" x="446.0" y="228" text-anchor="middle">2</text>
<text class="tick-lbl" x="251.0" y="262" text-anchor="middle">bits per weight</text>
<text class="tick-lbl" x="56" y="16" text-anchor="start">validation loss</text>
<line class="floor" x1="56" y1="205.2" x2="446" y2="205.2"/>
<text class="tick-lbl" x="62" y="219.2" text-anchor="start">float32 2.0272</text></g>
<path class="curve bad" fill="none" d="M56.0,205.1 L153.5,204.0 L251.0,181.8 L348.5,114.4 L446.0,60.9"/>
<path class="curve ok" fill="none" d="M56.0,205.2 L153.5,204.8 L251.0,192.6 L348.5,151.1 L446.0,40.9"/>
<circle cx="56.0" cy="205.1" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="56.0" cy="205.2" r="2.6"/>
<circle cx="153.5" cy="204.0" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="153.5" cy="204.8" r="2.6"/>
<circle cx="251.0" cy="181.8" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="251.0" cy="192.6" r="2.6"/>
<circle cx="348.5" cy="114.4" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="348.5" cy="151.1" r="2.6"/>
<circle cx="446.0" cy="60.9" r="2.6" style="fill:var(--ink-2)"/>
<circle class="mark" cx="446.0" cy="40.9" r="2.6"/>
<text class="lbl bad" x="187.6" y="110.4" text-anchor="start">one scale per matrix</text>
<text class="lbl ok" x="402.1" y="185.2" text-anchor="end">one scale per output channel</text>
</svg>
<figcaption>Validation loss as the weights are squeezed into fewer bits. Eight and six sit almost on the float32 line, four starts to separate and three collapses. At two bits the per-channel scale is the worse of the two, at a point where neither is usable.</figcaption>
</figure>

```
bits   one scale per matrix   one scale per channel
   8                 2.0290                  2.0280
   6                 2.0599                  2.0387
   4                 2.6380                  2.3571
   3                 4.3960                  3.4381
   2                 5.7894                  6.3112
```

Through `6` bits it is still a second-decimal conversation. At `4` it separates to
`2.36` and at `3` it collapses to `3.44`. Part one's bigram scored `2.6501`, so
**a four-bit model is barely better than counting the previous character**.

## At two bits it inverts

The last row is odd. At `2` bits the per-channel scale gives `6.3112`, which is
**worse** than the per-matrix `5.7894` - after being better on every row above.

Measuring what happened, for `blocks.0.f1` alone:

```
one scale per matrix    95.2% of elements collapse to zero    mean abs error 0.0519
one scale per channel   78.1% collapse to zero                mean abs error 0.0419
```

**Per-channel reconstructed the weights better.** Fewer dead elements, smaller
error. And the loss is worse.

So at two bits, "how well were the weights reconstructed" and "how well does the
model work" have already come apart. Neither is usable, and the ordering between
them means nothing. The right move is to write down what was measured and decline
to draw a conclusion from it.

## What is sensitive

Instead of squeezing everything, take one matrix down to 4 bits and leave the
rest at float32, and it becomes clear who hurts.

```
tok.weight              loss +0.0976
pos.weight              loss +0.0618
blocks.2.f1.weight      loss +0.0184
blocks.0.f2.weight      loss +0.0174
blocks.2.qkv.weight     loss +0.0132
...
blocks.2.f2.weight      loss -0.0020   (least sensitive; it dips slightly)
```

**The two embeddings dominate.** The character embedding alone hurts more than
five times as much as any matrix inside a block. This is why real quantisation
keeps embeddings and the output layer at higher precision.

Worth noting that the least sensitive is `-0.0020`, a **negative** number.
Quantisation did not accidentally help; a change that size is inside the wobble
of the loss measurement itself.

Adding up the individual damages gives `+0.2830` while quantising everything
gives `+0.3299`. The damage does not merely add; the pieces amplify each other.

## The loss holds still and the text does not

int8 moved the loss by `+0.0017`. Does the same text come out? Generating from the
same seed:

```
float32  '`16, a=0, 36, 112003  0.3009849\n```\n\nThe smallest `1.000h`. **`shape(2'
int8     '`16, a=0, 36, 112003  20350  0.63103  20.013910   0.016693939  16\n9 = '
```

**It diverges at the twenty-second character.** Identical up to there and a
completely different text after.

Which follows. As part one showed, candidates sit close together, and where the
probability gap is tiny a `0.0017` wobble picks a different character. Change one
character and the whole context after it changes.

Part two's note about the cache's `9.06e-06` - that it is not bit-identical - here
becomes a visible consequence. **Equal average performance and identical output
are different claims.**

## Per-channel barely mattered in this model

The usual argument in quantisation is about **outliers**: if one channel's range
is unusually wide, a single scale per matrix flattens everything else. Hence
splitting by channel.

Measured in this model, that premise is weak.

```
ratio of max to median channel range    worst matrix 2.49    median 1.51
```

About `1.5`. At that spread a single scale costs little, and indeed the two
schemes differ by `0.0010` at 8 bits.

The activations say the same.

```
block 0 FFN input      channel max/median 1.50    max 5.24
block 2 FFN input      channel max/median 1.54    max 6.24
residual stream (last)  channel max/median 1.64    max 6.67
```

What makes activation quantisation hard in large models is a handful of channels
spiking to tens or hundreds of times the rest; here it is `1.6`. So **this
experiment does not reproduce that problem.** The fair reading is that part
thirteen's model is small and was trained for 5000 steps on sixty thousand
characters, which means this part's finding that "per-channel adds little" is
**specific to this model**.

## So

- int8 is nearly free: validation loss `2.0272` -> `2.0290`, memory `2.43 MB` ->
  `0.62 MB`, `74.4%` less
- It holds through `6` bits. At `4` it reads `2.3571`, barely past the bigram's
  `2.6501`; at `3` it collapses
- At `2` bits the scheme that reconstructed the weights better has the worse loss.
  The two measures have already parted and the ordering means nothing
- Embeddings are the most sensitive. At 4 bits `tok` costs `+0.0976`, over five
  times any matrix inside a block
- A `+0.0017` loss still diverges the text at the twenty-second character. Equal
  averages are not identical outputs
- This model has no outliers. A channel-range ratio of `1.5` leaves little for
  per-channel to win, so this conclusion does not transfer to a large model

Three parts around the far side of training: the rule for choosing, how not to
compute twice, and the price of throwing away precision. Measured and drawn each
time, and each time what the theory promised and what actually arrived were
different.
