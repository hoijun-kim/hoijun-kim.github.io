---
title: "Normalisation erases the initialisation"
description: "In part four three initialisations produced 1e-16, 0.97 and 0.15 after twenty layers. Add one line of normalisation per layer and all three land on the same number to four decimals. Here is what that costs."
date: 2026-07-31
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 6
---

Part four concluded that the initialisation is a precondition. Too small and the
signal is `1e-16` after twenty layers; too large and the gradients differ by
`1e9` across the depth. Only Xavier avoided both.

Normalisation removes the precondition entirely. Add one line per layer and any
initialisation arrives at the same place. Start with how same.

## One line

Right after multiplying by the weights and before the activation, subtract the
mean and divide by the standard deviation.

```python
z = h @ W
z = (z - z.mean(0)) / (z.std(0) + 1e-5)   # batch normalisation
h = np.tanh(z)
```

`mean(0)` is the mean **along the batch**: the values one neuron produced across
the 512 samples in the batch, and their mean and standard deviation. Layer
normalisation, later, differs only here.

Put that single line into part four's twenty-layer stack and run the same three
initialisations.

```
initialisation   no normalisation (L20)    batch norm (L20)
0.01                      1.135e-16             0.6310
1.0                       9.742e-01             0.6310
Xavier                    1.543e-01             0.6310
```

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Activation size per layer. Without normalisation the three initialisations split into 0.97, 0.15 and one that leaves the bottom of the frame; with batch normalisation the three overlap on a single line at 0.63">
<g class="axis">
<line x1="52" y1="38.9" x2="446" y2="38.9"/>
<text class="tick-lbl" x="43" y="42.4" text-anchor="end">1e0</text>
<line x1="52" y1="71.1" x2="446" y2="71.1"/>
<text class="tick-lbl" x="43" y="74.6" text-anchor="end">1e-1</text>
<line x1="52" y1="103.2" x2="446" y2="103.2"/>
<text class="tick-lbl" x="43" y="106.8" text-anchor="end">1e-2</text>
<line x1="52" y1="135.4" x2="446" y2="135.4"/>
<text class="tick-lbl" x="43" y="138.9" text-anchor="end">1e-3</text>
<line x1="52" y1="167.6" x2="446" y2="167.6"/>
<text class="tick-lbl" x="43" y="171.1" text-anchor="end">1e-4</text>
<line x1="52" y1="199.8" x2="446" y2="199.8"/>
<text class="tick-lbl" x="43" y="203.3" text-anchor="end">1e-5</text>
<line x1="52" y1="232.0" x2="446" y2="232.0"/>
<text class="tick-lbl" x="43" y="235.5" text-anchor="end">1e-6</text>
<line class="frame" x1="52" y1="26" x2="52" y2="232"/><line class="frame" x1="52" y1="232" x2="446" y2="232"/>
<line class="frame" x1="52.0" y1="232" x2="52.0" y2="236"/><text class="tick-lbl" x="52.0" y="248" text-anchor="middle">1</text>
<line class="frame" x1="134.9" y1="232" x2="134.9" y2="236"/><text class="tick-lbl" x="134.9" y="248" text-anchor="middle">5</text>
<line class="frame" x1="238.6" y1="232" x2="238.6" y2="236"/><text class="tick-lbl" x="238.6" y="248" text-anchor="middle">10</text>
<line class="frame" x1="342.3" y1="232" x2="342.3" y2="236"/><text class="tick-lbl" x="342.3" y="248" text-anchor="middle">15</text>
<line class="frame" x1="446.0" y1="232" x2="446.0" y2="236"/><text class="tick-lbl" x="446.0" y="248" text-anchor="middle">20</text>
<text class="tick-lbl" x="249" y="266" text-anchor="middle">layer</text>
<text class="tick-lbl" x="52" y="16" text-anchor="start">activation size</text>
</g>
<clipPath id="fr6"><rect x="52" y="18" width="394" height="214"/></clipPath>
<g clip-path="url(#fr6)">
<path class="curve bad2" fill="none" d="M 52.0,64.8 L 72.7,90.5 L 93.5,116.2 L 114.2,141.9 L 134.9,167.4 L 155.7,193.0 L 176.4,218.6 L 197.2,240.0 L 217.9,240.0 L 238.6,240.0 L 259.4,240.0 L 280.1,240.0 L 300.8,240.0 L 321.6,240.0 L 342.3,240.0 L 363.1,240.0 L 383.8,240.0 L 404.5,240.0 L 425.3,240.0 L 446.0,240.0"/>
<path class="curve bad2" fill="none" d="M 52.0,39.2 L 72.7,39.2 L 93.5,39.2 L 114.2,39.2 L 134.9,39.2 L 155.7,39.2 L 176.4,39.2 L 197.2,39.2 L 217.9,39.2 L 238.6,39.2 L 259.4,39.2 L 280.1,39.2 L 300.8,39.2 L 321.6,39.2 L 342.3,39.2 L 363.1,39.2 L 383.8,39.2 L 404.5,39.2 L 425.3,39.2 L 446.0,39.2"/>
<path class="curve bad2" fill="none" d="M 52.0,45.4 L 72.7,49.0 L 93.5,51.4 L 114.2,53.4 L 134.9,54.8 L 155.7,56.0 L 176.4,57.0 L 197.2,57.9 L 217.9,58.8 L 238.6,59.4 L 259.4,60.1 L 280.1,61.0 L 300.8,61.4 L 321.6,61.9 L 342.3,62.4 L 363.1,62.8 L 383.8,63.5 L 404.5,63.9 L 425.3,64.6 L 446.0,65.0"/>
<path class="curve ok" fill="none" d="M 52.0,45.4 L 72.7,45.4 L 93.5,45.3 L 114.2,45.3 L 134.9,45.3 L 155.7,45.3 L 176.4,45.3 L 197.2,45.3 L 217.9,45.3 L 238.6,45.3 L 259.4,45.3 L 280.1,45.3 L 300.8,45.3 L 321.6,45.3 L 342.3,45.3 L 363.1,45.3 L 383.8,45.3 L 404.5,45.3 L 425.3,45.3 L 446.0,45.3"/>
<path class="curve ok" fill="none" d="M 52.0,45.4 L 72.7,45.4 L 93.5,45.3 L 114.2,45.3 L 134.9,45.3 L 155.7,45.3 L 176.4,45.3 L 197.2,45.3 L 217.9,45.3 L 238.6,45.3 L 259.4,45.3 L 280.1,45.3 L 300.8,45.3 L 321.6,45.3 L 342.3,45.3 L 363.1,45.3 L 383.8,45.3 L 404.5,45.3 L 425.3,45.3 L 446.0,45.3"/>
<path class="curve ok" fill="none" d="M 52.0,45.4 L 72.7,45.4 L 93.5,45.3 L 114.2,45.3 L 134.9,45.3 L 155.7,45.3 L 176.4,45.3 L 197.2,45.3 L 217.9,45.3 L 238.6,45.3 L 259.4,45.3 L 280.1,45.3 L 300.8,45.3 L 321.6,45.3 L 342.3,45.3 L 363.1,45.3 L 383.8,45.3 L 404.5,45.3 L 425.3,45.3 L 446.0,45.3"/>
</g>
<text class="lbl bad" x="321.6" y="31.2" text-anchor="middle">none, 1.0 &rarr; 0.974</text>
<text class="lbl bad" x="342.3" y="78.4" text-anchor="middle">none, Xavier &rarr; 0.154</text>
<text class="lbl bad" x="217.9" y="236.4" text-anchor="middle">none, 0.01 &rarr; 1e-16 by layer 20</text>
<text class="lbl ok" x="134.9" y="36.3" text-anchor="middle">batch norm - three on one line, 0.631</text>
</svg>
<figcaption>Activation size per layer. Without normalisation the initialisation splits the result three ways: 0.974, 0.154, and one that leaves the bottom of the frame. The three normalised lines overlap into one - all three are 0.6310 at layer 20.</figcaption>
</figure>

Three identical values to four decimals. Not a coincidence - it follows from the
definition.

First, what exactly is set to one. What gets normalised is **`z`, before the
activation**. The layer's output `tanh(z)` is not 1 but `0.6310`, which is the
number in the table. Every layer returns `z` to the same distribution, so the
same value comes out each time.

The reason all three agree is simpler still. Batch normalisation erases a
positive scalar factor completely: `BN(cz) = BN(z)`, and feeding it `z` and
`100z` differs by `6e-15`, pure floating-point noise. The initialisations 0.01,
1.0 and Xavier are the same random numbers times different constants, so the
moment normalisation is added **the three are the same network**. What part four
called the base of the multiplication is reset at every layer - and this
argument does not carry to initialisations that are not scalar multiples of each
other, such as orthogonal initialisation.

That is normalisation's real value. Before any speedup, **the initialisation
stops being a hyperparameter**. Building twenty layers no longer involves
fussing over scale.

## Price 1: it depends on the batch

Not free. The mean and standard deviation are **estimated from the batch**.
Measure the layer-20 activation while varying only the batch size:

```
batch      batch norm     layer norm
4            0.6756         0.6261
8            0.6507         0.6339
32           0.6346         0.6272
256          0.6317         0.6287
512          0.6310         0.6282
```

Batch normalisation drifts upward as the batch shrinks. Layer normalisation is
flat, independent of the batch.

It is easy to explain this as "a small batch underestimates the standard
deviation, so dividing by it inflates the result". **That is wrong.**
Normalisation divides a batch by that batch's own standard deviation, so the
output has standard deviation exactly 1 at any batch size. Measured: `0.999983`
at batch 4 and `0.999990` at batch 512, no difference. However far off the
estimate is, dividing by it returns 1.

The real cause is **shape**. Standardise `n` samples against themselves and no
value can exceed `sqrt(n-1)`. At batch 4 that bound is `1.732`; at batch 512 it
is `22.6`. The tails are clipped and the kurtosis changes from `3.003` at batch
512 to `1.835` at batch 4. `tanh` is a function that squashes large values - and
at a small batch **there are no large values to squash**. So less is squashed and
the standard deviation comes out higher.

Two pieces of evidence. Swap the activation for a linear one and the batch
dependence disappears completely: `1.0000` at both batch 4 and 512. And feeding
exactly `N(0,1)` through normalisation plus `tanh` for **a single layer** already
shows the whole gap, `0.6768` against `0.6281`. It is not something twenty layers
built up.

The estimator itself is still worth a look. The sample standard deviation is off
in two ways.

```
batch   bias (how low on average)   spread (how much it moves per draw)
2              -0.4363                        0.4253
4              -0.2020                        0.3366
8              -0.0979                        0.2449
32             -0.0237                        0.1244
256            -0.0030                        0.0440
```

The spread matches `1/sqrt(2*batch)`: predicted `0.1250` at batch 32, measured
`0.1244`. The bias follows `-3/(4*batch)`. Both are leading-order approximations
for a large batch, so the first row, batch 2, is off by 14 to 17 percent; from
batch 8 they are within a few percent.

The bias splits into two pieces. NumPy's `.std()` divides by `n` rather than
`n-1`, which is `-1/(2n)`, and measuring the **square root** rather than the
variance adds `-1/(4n)` through Jensen's inequality. Switching to `ddof=1` still
leaves 3.5 percent at batch 8. Frameworks' BatchNorm uses the biased variance
too, so this is not a NumPy quirk.

What that estimation error does during training is not to change the scale but to
**shake the value from batch to batch**. The regularising effect in the next
section comes from there.

## Price 2: training and inference diverge

Using batch statistics means the same sample produces a different output
**depending on which samples share its batch**. During training that wobble acts
as a kind of regulariser and can help.

Inference is the problem. A single sample has no batch. So batch normalisation
accumulates running means and variances during training and uses those at
inference. The training path and the inference path compute different things,
and the gap shows when the batch is small or the two distributions differ.

That is where layer normalisation comes from. It normalises along the **feature
direction within one sample** instead of along the batch.

```python
z = (z - z.mean(1, keepdims=True)) / (z.std(1, keepdims=True) + 1e-5)
```

One axis changed and the properties change with it. It never looks at other
samples, so it is independent of batch size, training and inference compute the
same thing, and it works on data whose samples have different lengths. That is
why transformers use it.

## What remains

Normalisation does not replace initialisation. The three initialisations above
arrived at the same place, but that is the **scale** being equal; the directions
the weights carry are still whatever the initialisation drew. And the
normalisation layer has scale and shift parameters of its own, which have to be
initialised too.

## So

- Normalisation resets the base of the multiplication at every layer. Three
  initialisations landing on `0.6310` after twenty layers is the evidence
- What it buys, before any speedup, is **the disappearance of sensitivity to the
  initialisation**
- Batch norm's output has variance 1 at any batch size. The rise at a small batch
  is not estimator bias but self-standardisation clipping the tails at
  `sqrt(batch-1)` - swap in a linear activation and the difference vanishes
- The estimation error shows up as wobble between batches, not as scale. Bias
  `-3/(4*batch)`, spread `1/sqrt(2*batch)`, both large-batch approximations
- Layer norm never looks at the batch, so it avoids that. It normalises along a
  different axis, which makes it a different thing, not a strictly better one

The next part is about the difference between training well and **predicting
well**. It drives the training loss to zero and measures what happens on data
the model has not seen.
