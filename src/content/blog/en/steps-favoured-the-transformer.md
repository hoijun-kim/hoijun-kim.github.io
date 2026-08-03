---
title: "Comparing by steps favoured the transformer"
description: "Paying off part seven's debt. Recurrence goes in order, so it should be the slow one - and the LSTM comes in at 0.82 times the transformer. The cost of being sequential is there, hidden by a fused kernel, and what makes the transformer expensive is the number of steps rather than the price of one."
date: 2026-01-06
lang: en
kind: guide
series:
  id: not-attention
  part: 9
---

Part seven compared five architectures at **the same step count**, and closed by
noting that if a step costs different amounts, whether that comparison is fair is
itself a question.

Paying it off.

## What one step costs

Time one training step at batch 32 - forward, backward, clipping - with the
context from 16 to 128, running all five once per round in a round robin.

<figure class="fig">
<svg viewBox="0 0 460 322" role="img" aria-label="Above: training time per step from context 16 to 128. All five sit between 74 and 120 milliseconds. Below: the time each takes to reach its own validation minimum, where the transformer alone needs 272 seconds, over twelve times the CNN's">
<text class="ttl2 l" x="18.0" y="16">time for one training step</text>
<g class="axis">
<line x1="76.0" y1="123.7" x2="300.0" y2="123.7"/>
<text class="tick-lbl" x="70.0" y="127.2" text-anchor="end">20</text>
<line x1="76.0" y1="98.6" x2="300.0" y2="98.6"/>
<text class="tick-lbl" x="70.0" y="102.1" text-anchor="end">50</text>
<line x1="76.0" y1="73.6" x2="300.0" y2="73.6"/>
<text class="tick-lbl" x="70.0" y="77.1" text-anchor="end">80</text>
<line x1="76.0" y1="48.5" x2="300.0" y2="48.5"/>
<text class="tick-lbl" x="70.0" y="52.0" text-anchor="end">110</text>
</g>
<path class="curve bad2" d="M76.0,125.6 L150.7,119.3 L225.3,110.1 L300.0,78.8" fill="none"/>
<path class="curve ok3" d="M76.0,127.9 L150.7,119.6 L225.3,100.2 L300.0,72.6" fill="none"/>
<path class="curve bad" d="M76.0,127.8 L150.7,119.3 L225.3,107.2 L300.0,66.5" fill="none"/>
<path class="curve ok2" d="M76.0,125.1 L150.7,113.7 L225.3,93.6 L300.0,40.3" fill="none"/>
<path class="curve ok" d="M76.0,126.5 L150.7,117.0 L225.3,101.1 L300.0,57.6" fill="none"/>
<text class="lbl" x="308.0" y="43.8">GRU 120</text>
<text class="lbl" x="308.0" y="61.1">transformer 99</text>
<text class="lbl" x="308.0" y="73.1">RNN 88</text>
<text class="lbl" x="308.0" y="85.1">LSTM 81</text>
<text class="lbl" x="308.0" y="97.1">CNN 74</text>
<g class="lbl-ax">
<text x="76.0" y="147">16</text>
<text x="150.7" y="147">32</text>
<text x="225.3" y="147">64</text>
<text x="300.0" y="147">128</text>
<text class="cap l" x="76.0" y="162">context length, log</text>
<text class="cap l" x="46.0" y="30">ms</text></g>
<text class="ttl2 l" x="10.0" y="184">time to reach its own minimum</text>
<text class="cap l" x="132.0" y="202">seconds · steps · best val</text>
<g class="split">
<text class="lbl r" x="124.0" y="221.0" text-anchor="end">CNN</text>
<rect class="dec" x="132.0" y="210.0" width="12.5" height="14"/>
<text class="lbl" x="150.5" y="221.0">22 &#183; 300 &#183; 1.8709</text>
<text class="lbl r" x="124.0" y="245.0" text-anchor="end">LSTM</text>
<rect class="dec" x="132.0" y="234.0" width="36.7" height="14"/>
<text class="lbl" x="174.7" y="245.0">65 &#183; 800 &#183; 1.6776</text>
<text class="lbl r" x="124.0" y="269.0" text-anchor="end">RNN</text>
<rect class="dec" x="132.0" y="258.0" width="39.9" height="14"/>
<text class="lbl" x="177.9" y="269.0">71 &#183; 800 &#183; 1.8355</text>
<text class="lbl r" x="124.0" y="293.0" text-anchor="end">GRU</text>
<rect class="dec" x="132.0" y="282.0" width="54.1" height="14"/>
<text class="lbl" x="192.1" y="293.0">96 &#183; 800 &#183; 1.6449</text>
<text class="lbl r" x="124.0" y="317.0" text-anchor="end">transformer</text>
<rect class="dec" x="132.0" y="306.0" width="153.8" height="14"/>
<text class="lbl" x="291.8" y="317.0">273 &#183; 2750 &#183; 1.7679</text>
</g></svg>
<figcaption>Above: time for one training step at batch 32, context 16 to 128, median of 25 round-robin rounds. All five sit between 74 and 120 milliseconds and the recurrent ones are not especially slow. Below: how long each takes to reach its own validation minimum. Only the transformer is far out at 273 seconds - not because a step is expensive but because it needs many more of them.</figcaption>
</figure>

```
context         16     32     64    128   128/16
CNN           17.6   25.2   36.3   73.8      4.2
LSTM          14.9   24.9   48.1   81.2      5.4
RNN           15.0   25.2   39.7   88.4      5.9
transformer   16.6   27.9   47.1   99.1      6.0
GRU           18.2   31.9   55.9  119.8      6.6
```

## Recurrence is not the slow one

At context 128, with the transformer as 1: CNN `0.74`, LSTM `0.82`, RNN `0.89`,
GRU `1.21`.

**Two of the recurrent models are faster than the transformer.** Which is
backwards. Recurrence has to walk the context 128 steps in order while the
transformer computes the positions together, so recurrence should be losing.

The growth from context 16 to 128 is also bunched, `4.2` to `6.6`. Attention is
`T²` and recurrence is `T`, and the transformer's `6.0` against the RNN's `5.9`
does not tell them apart.

## The cost of being sequential is hidden by a fused kernel

Because `nn.LSTM` runs its sequential loop in C rather than Python. Part two wrote
the same computation as a Python loop to get at the gates, so dividing the two
inside the same round shows the price.

```
context   Python loop (ms)   nn.LSTM (ms)   ratio
     16                4.9            3.4    1.61
     32               13.8            5.6    2.44
     64               24.5           11.5    2.15
    128               48.3           22.1    2.12
```

Growing the context eight times takes the Python loop up `9.8` times and the
fused kernel `6.4`. **The Python loop scales with the number of steps and the
fused kernel does not.** The sequential cost is real; the kernel absorbs about
half of it.

And at this size what remains after that absorption is too small to distinguish
from attention's `T²`. The same story as the second series, where half of a step
was fixed overhead.

## What is expensive is the step count

If a step costs about the same, what decides the time is how many are needed.
Multiplying part seven's step-to-minimum by the per-step time:

```
                steps   per step (ms)   total (s)   best val
CNN               300            73.8        22.1     1.8709
LSTM              800            81.2        65.0     1.6776
RNN               800            88.4        70.7     1.8355
GRU               800           119.8        95.8     1.6449
transformer      2750            99.1       272.5     1.7679
```

**The transformer needs `272.5 seconds` to reach its own bottom, `12.3` times the
CNN's and `2.84` times the GRU's.** Not because a step is expensive. Because it
needs `2750` of them.

## So was comparing by steps fair

It was, and if anything it favoured the transformer.

Part seven gave all five the same 4000 steps and looked at each one's minimum.
Converted to time, the transformer alone spends three or four times what the
others do. Budgeted in seconds it would have been cut off before reaching its
bottom.

The GRU reaches `1.6449` in `95.8` seconds; the transformer spends `272.5` to
reach `1.7679`. Part seven's ordering survives the switch to time, and the gap
widens.

## Correcting a sentence in part seven

Part seven said "one GRU run took more than twice as long as the transformer".
That number came from timing five configurations one after another, which is not
trustworthy. Measured round-robin, it is `1.21` times per step.

Part ten of the second series had already established that absolute times must
not be measured consecutively, and writing part seven did not apply that lesson
to its own data. It has been corrected.

## What is left

This is a CPU story. On a GPU attention parallelises far better while
recurrence's sequential loop stays sequential, so the ordering would likely
invert - there is no GPU here.

Context only went to 128. `T²` hurts more the longer it gets and recurrence's `T`
does not, so somewhere near 1024 the table would look different. The position
embedding is 128 characters, so it cannot be extended here.

And the step counts are taken from part seven as they were. Tuning the learning
rate per architecture would change how many steps each needs and therefore this
table too. Giving all five the same `3e-4` may have been the thing that hurt the
transformer.

## So

- Per-step time at context 128 is CNN `0.74`, LSTM `0.82`, RNN `0.89`, GRU `1.21`
  against the transformer at 1. **Recurrence is not the slow one**
- Growth over an eightfold context is bunched at `4.2`~`6.6`. Attention's `T²`
  cannot be told from recurrence's `T`
- The sequential cost is real: the same LSTM computation as a Python loop is
  `2.12` times slower and grows `9.8` times over that context against the fused
  kernel's `6.4`
- What makes the transformer expensive is the step count, not the step: `2750`
  against `800`
- To its own bottom: CNN `22s`, GRU `96s`, transformer `273s`. The transformer
  spends `2.84` times the GRU's to land on a worse loss
- Part seven's step-count comparison was fair, and leaned the transformer's way
- Part seven's "more than twice as long" came from consecutive timing and was
  wrong. Corrected
