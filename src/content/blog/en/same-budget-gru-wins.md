---
title: "At the same budget the GRU wins - for 700 steps"
description: "RNN, LSTM, GRU and a 1D causal CNN trained on the same corpus with the same parameter budget and optimiser as the transformer from the previous series. The GRU's best validation loss, 1.6449, beats the transformer's 1.7679. But it only leads between steps 500 and 1200, and by step 4000 it has collapsed to 3.4170."
date: 2025-12-25
lang: en
kind: guide
series:
  id: not-attention
  part: 7
---

The six parts before this opened up one recurrent step, the LSTM's gates, the
GRU, the convolution kernel, the receptive field and pooling. What each of them
computes has been seen; which of them is better has not.

So put them together. One condition: **everything has to be measured against the
same thing.** Match the parameter budget to the transformer from part thirteen of
the first series, and keep the corpus and the optimiser identical.

## Matching the budget

Part thirteen's model has `637,156` parameters. Same corpus, same 128-character
context, same batch of 32, same AdamW at `3e-4`, and each architecture's width
tuned to hit that number.

```
              width    parameters   vs transformer
RNN             683       637,845          100.1%
LSTM            325       637,550          100.1%
GRU             381       635,835           99.8%
CNN     171 channels      639,273          100.3%
transformer                637,156          100.0%
```

All within 0.3%. The embedding and the output layer are identical across all
five; only the middle changes. The CNN is four causal convolutions with kernel 5,
so its receptive field is `4 x 4 + 1 = 17` characters - that comes back later.

The same budget does not mean the same use of it. The RNN pours 466k of it into a
single `683 x 683` recurrent matrix while the transformer spreads it over three
blocks. That is part of the architecture too.

## Comparing at a fixed step count is wrong

The first attempt ran all five for 4000 steps and compared the last value:

```
RNN 3.4327   LSTM 3.2872   GRU 3.3432   CNN 3.6865   transformer 1.8300
```

A rout for the transformer. Except that at step 800 of those same runs, the LSTM
is at `1.6817` and the GRU at `1.6550`. **The corpus is only 75,353 characters,
so all five memorise it, and they reach the bottom at different times.**
Comparing at a fixed step count means measuring someone else past their minimum.

So the protocol changed: validate every 100 steps up to 1500 and every 250 after
that, and take **each architecture's lowest validation loss** as its score. Three
seeds each.

## All five on one plot

<figure class="fig">
<svg viewBox="0 0 460 292" role="img" aria-label="Validation loss for five architectures. All of them bottom out and turn back up, at different times and different depths">
<g class="axis">
<line x1="62.0" y1="222.4" x2="442.0" y2="222.4"/>
<text class="tick-lbl" x="56.0" y="225.9" text-anchor="end">2.0</text>
<line x1="62.0" y1="186.8" x2="442.0" y2="186.8"/>
<text class="tick-lbl" x="56.0" y="190.2" text-anchor="end">2.5</text>
<line x1="62.0" y1="151.1" x2="442.0" y2="151.1"/>
<text class="tick-lbl" x="56.0" y="154.6" text-anchor="end">3.0</text>
<line x1="62.0" y1="115.5" x2="442.0" y2="115.5"/>
<text class="tick-lbl" x="56.0" y="119.0" text-anchor="end">3.5</text>
<line x1="62.0" y1="79.9" x2="442.0" y2="79.9"/>
<text class="tick-lbl" x="56.0" y="83.4" text-anchor="end">4.0</text>
<line x1="62.0" y1="44.2" x2="442.0" y2="44.2"/>
<text class="tick-lbl" x="56.0" y="47.8" text-anchor="end">4.5</text>
</g>
<line class="ref" x1="62.0" y1="176.1" x2="442.0" y2="176.1"/>
<text class="lbl" x="442.0" y="172.1" text-anchor="end">bigram 2.65</text>
<line class="ref" x1="62.0" y1="36.8" x2="442.0" y2="36.8"/>
<text class="lbl" x="442.0" y="32.8" text-anchor="end">uniform 4.61</text>
<path class="curve ok" d="M71.5,163.0 L81.0,175.8 L90.5,179.8 L100.0,182.3 L109.5,184.4 L119.0,187.0 L128.5,190.3 L138.0,194.6 L147.5,200.0 L157.0,206.2 L166.5,211.9 L176.0,215.6 L185.5,219.0 L195.0,223.2 L204.5,225.5 L228.2,230.9 L252.0,234.8 L275.8,236.4 L299.5,237.6 L323.2,238.5 L347.0,238.4 L370.8,237.8 L394.5,237.0 L418.2,234.7 L442.0,233.2" fill="none"/>
<circle class="dot" cx="323.2" cy="238.5" r="3"/>
<path class="curve ok2" d="M71.5,200.3 L81.0,219.6 L90.5,230.7 L100.0,238.0 L109.5,242.8 L119.0,245.2 L128.5,246.5 L138.0,247.4 L147.5,245.9 L157.0,244.6 L166.5,242.6 L176.0,239.6 L185.5,235.8 L195.0,231.0 L204.5,226.5 L228.2,210.6 L252.0,191.1 L275.8,174.4 L299.5,159.8 L323.2,148.3 L347.0,140.2 L370.8,134.6 L394.5,129.1 L418.2,124.2 L442.0,120.0" fill="none"/>
<circle class="dot" cx="138.0" cy="247.4" r="3"/>
<path class="curve ok3" d="M71.5,198.4 L81.0,217.8 L90.5,228.6 L100.0,236.3 L109.5,240.1 L119.0,242.9 L128.5,245.0 L138.0,245.0 L147.5,243.9 L157.0,243.9 L166.5,240.7 L176.0,239.1 L185.5,236.0 L195.0,231.8 L204.5,226.4 L228.2,212.9 L252.0,197.9 L275.8,185.0 L299.5,171.9 L323.2,161.2 L347.0,151.3 L370.8,144.7 L394.5,138.4 L418.2,133.3 L442.0,130.5" fill="none"/>
<circle class="dot" cx="138.0" cy="245.0" r="3"/>
<path class="curve bad" d="M71.5,202.3 L81.0,212.5 L90.5,220.8 L100.0,225.8 L109.5,228.7 L119.0,231.4 L128.5,233.5 L138.0,232.9 L147.5,233.1 L157.0,230.2 L166.5,228.5 L176.0,224.9 L185.5,221.4 L195.0,216.3 L204.5,210.3 L228.2,193.7 L252.0,175.9 L275.8,159.5 L299.5,145.7 L323.2,136.5 L347.0,128.6 L370.8,122.2 L394.5,118.4 L418.2,114.2 L442.0,111.4" fill="none"/>
<circle class="dot" cx="128.5" cy="233.5" r="3"/>
<path class="curve bad2" d="M71.5,209.6 L81.0,227.0 L90.5,231.1 L100.0,230.6 L109.5,228.2 L119.0,224.5 L128.5,219.6 L138.0,215.0 L147.5,211.4 L157.0,205.1 L166.5,200.3 L176.0,194.3 L185.5,188.3 L195.0,184.0 L204.5,177.8 L228.2,166.8 L252.0,155.9 L275.8,145.6 L299.5,137.0 L323.2,131.0 L347.0,121.8 L370.8,117.7 L394.5,113.1 L418.2,106.4 L442.0,100.3" fill="none"/>
<circle class="dot" cx="90.5" cy="231.1" r="3"/>
<g class="lgd">
<rect class="bg" x="66.0" y="39.0" width="220" height="69"/>
<line class="curve ok" x1="76.0" y1="50.0" x2="98.0" y2="50.0" fill="none"/>
<text class="lbl" x="104.0" y="53.5">transformer</text>
<text class="lbl" x="228.0" y="53.5" text-anchor="end">1.7679</text>
<text class="lbl" x="278.0" y="53.5" text-anchor="end">@2750</text>
<line class="curve ok2" x1="76.0" y1="63.0" x2="98.0" y2="63.0" fill="none"/>
<text class="lbl" x="104.0" y="66.5">GRU</text>
<text class="lbl" x="228.0" y="66.5" text-anchor="end">1.6449</text>
<text class="lbl" x="278.0" y="66.5" text-anchor="end">@800</text>
<line class="curve ok3" x1="76.0" y1="76.0" x2="98.0" y2="76.0" fill="none"/>
<text class="lbl" x="104.0" y="79.5">LSTM</text>
<text class="lbl" x="228.0" y="79.5" text-anchor="end">1.6776</text>
<text class="lbl" x="278.0" y="79.5" text-anchor="end">@800</text>
<line class="curve bad" x1="76.0" y1="89.0" x2="98.0" y2="89.0" fill="none"/>
<text class="lbl" x="104.0" y="92.5">RNN</text>
<text class="lbl" x="228.0" y="92.5" text-anchor="end">1.8355</text>
<text class="lbl" x="278.0" y="92.5" text-anchor="end">@800</text>
<line class="curve bad2" x1="76.0" y1="102.0" x2="98.0" y2="102.0" fill="none"/>
<text class="lbl" x="104.0" y="105.5">CNN</text>
<text class="lbl" x="228.0" y="105.5" text-anchor="end">1.8709</text>
<text class="lbl" x="278.0" y="105.5" text-anchor="end">@300</text>
</g>
<g class="lbl-ax">
<text x="62.0" y="274">0</text>
<text x="157.0" y="274">1000</text>
<text x="252.0" y="274">2000</text>
<text x="347.0" y="274">3000</text>
<text x="442.0" y="274">4000</text>
<text class="cap l" x="62.0" y="289">training step</text></g>
<g class="row-lbl"><text x="28.0" y="144" transform="rotate(-90 28.0 144)">validation loss</text></g>
</svg>
<figcaption>Validation loss for five architectures, parameters matched at 637k with the same corpus and the same optimiser. Curves are the median seed of three; the dot marks each minimum. All five bottom out and turn back, but they reach the bottom anywhere from 300 to 2750 steps apart - a factor of nine. Only the transformer stays nearly flat after turning.</figcaption>
</figure>

```
              parameters   best val   3 seeds              at step   perplexity
GRU              635,835     1.6449   1.6276~1.6503            800        5.180
LSTM             637,550     1.6776   1.6737~1.6785            800        5.353
transformer      637,156     1.7679   1.7662~1.7694           2750        5.859
RNN              637,845     1.8355   1.8354~1.8362            800        6.268
CNN              639,273     1.8709   1.8695~1.8748            300        6.494
```

The seed spread is tiny. The RNN's three land between `1.8354` and `1.8362`, the
transformer's between `1.7662` and `1.7694`. Seeds do not reorder this.

## The GRU wins

`1.6449` against `1.7679`. In perplexity, `5.180` against `5.859` - **11.6%
better.** The LSTM leads too at `1.6776`. At 637k parameters learning 75 thousand
characters, attention is not the best answer available.

Which is not surprising. Attention earns its keep where the context is long and
the data is plentiful; here the context is 128 characters and the data is a
chapter of a novel. At that size, carrying one hidden state is the more efficient
arrangement.

The RNN losing at `1.8355` is the other side of the same story. Without gates
there is no deciding what to keep and what to drop. The margin from the RNN to
the LSTM and GRU (`0.16` to `0.19`) is wider than the margin to the transformer.
**Gating makes a bigger difference here than attention does.**

## For 700 steps

But that table collects everybody's best moment. The curves say something else.

```
              best    at 4000     ratio
GRU         1.6449     3.4170      2.08
LSTM        1.6776     3.3660      2.01
RNN         1.8355     3.5293      1.92
CNN         1.8709     3.7161      1.99
transformer 1.7679     1.8424      1.04
```

**Only the transformer holds together.** Past its minimum and out to step 4000 it
is at `1.04` times its best, while the others double.

Counting the steps where the GRU is under the transformer's best of `1.7679`
gives **step 500 to step 1200**. All three seeds give exactly that interval. The
LSTM gives `500~1100`. Outside it, the transformer wins.

The other way round, the transformer stays under 1.1 times its own best
(`1.945`) from `step 1500 to step 4000` and is still inside at 4000. The GRU on
the same test gets `300~1500`.

So read it like this. **The GRU's peak is higher, but it sits in a 700-step
window, and the transformer's seat stays open.** If you know exactly when to
stop, use the GRU. If you do not, use the transformer.

## The convolution sees 17 characters

Four layers of kernel 5 reach `17` characters to the left. The other four see all
128.

That was first written up as the reason it comes last. Part five widens the
window to `125` and gets `1.9967` - **worse** - and even widening by dilation
alone, without adding a single parameter, takes `1.8709` to `1.9716`. It is not
losing because its view is narrow.

It is also first to the bottom, at `300` steps. It has the least to learn, so it
finishes learning first and starts memorising first.

How to widen a receptive field, and whether widening it closes the gap, gets
measured later in this series.

## Why this differs from part thirteen

Part thirteen reported the same transformer's best validation as `1.7510`. Here
the three seeds are `1.7662`, `1.7679` and `1.7694`. Part thirteen's number is
outside that range.

The cause turned up. Part thirteen's training script samples text partway
through, and that function begins with `torch.manual_seed(0)`. That reseeds the
global generator, so from there the batch order **repeats from the beginning.**

```
no reseed midway   136044 248239 714933  93760 848963 848379
reseed on the 3rd  136044 248239 714933 136044 248239 714933
```

Part thirteen's model took that reseed at steps 200 and 1000, so it saw a
different data order than this run did. There is no reason the two numbers would
agree. What part thirteen published is what that run actually produced, and that
checkpoint still gives that loss, so the earlier series stand. This part just
uses numbers from one protocol run across all five.

## What is left

What this gives is a ranking **for this corpus at this size**. 75 thousand
characters is small. Scaling the data would be expected to reorder it, but
expectation is not measurement.

Depth was not touched either. Every recurrent model here is one layer and the
transformer is three. The budget was matched on width alone, so what happens when
recurrence gets a second layer is unknown.

And training time was not measured. One GRU run took more than twice as long as
the transformer, which means the per-step cost differs, which means whether
comparing at equal step counts is fair at all is itself a question. Measured
later.

## So

- Matched to `637,156` parameters, all five architectures land within 0.3%
- All five overfit. Comparing at a fixed step count measures someone else past
  their minimum
- By lowest validation: `GRU 1.6449` < `LSTM 1.6776` < `transformer 1.7679` <
  `RNN 1.8355` < `CNN 1.8709`
- The GRU is `11.6%` better than the transformer in perplexity. The ungated RNN
  loses - gating makes a bigger difference here than attention
- But the GRU only leads from step `500` to `1200`, and by 4000 it is `2.08`
  times its best. The transformer is at `1.04`
- The CNN sees `17` characters to its left. But part five widens that window and
  it gets worse - a narrow view is not why it loses
