---
title: "Stack twenty layers and the gradient disappears"
description: "Initialise at 0.01 and the activations are 1e-16 after twenty layers; initialise at 1.0 and the first layer's gradient is 1e8. Measure each layer and it becomes clear why initialisation is not a hyperparameter but a precondition."
date: 2026-07-30
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 4
---

The previous part said the chain rule is multiplication. Three layers, three
multiplications; twenty layers, twenty. Multiply a number slightly below one by
itself twenty times and it sticks to zero; slightly above one and it explodes.
That obvious arithmetic held deep learning back for years, and the initial
values are what set the base of the multiplication.

## Build twenty layers and measure

Draw each layer's weights from a normal distribution, varying only the standard
deviation. The activation is `tanh`, the width 256, the depth 20.

```python
import numpy as np
rng = np.random.default_rng(0)
N, D, L = 512, 256, 20

def run(scale):
    x = rng.standard_normal((N, D))         # input standard deviation 1
    h, Ws, hs = x, [], [x]
    for _ in range(L):
        W = rng.standard_normal((D, D)) * scale
        h = np.tanh(h @ W)
        Ws.append(W); hs.append(h)

    g = rng.standard_normal(h.shape) / np.sqrt(N)   # a gradient from the loss
    grads = []
    for i in range(L - 1, -1, -1):
        g = g * (1 - hs[i+1] ** 2)                  # tanh derivative
        grads.append((hs[i].T @ g).std())           # this layer's weight gradient
        g = g @ Ws[i].T
    return [a.std() for a in hs[1:]], grads[::-1]
```

Three initialisations: very small (0.01), very large (1.0), and `1/sqrt(n)`. The
last is Xavier initialisation.

```
                  act L1     act L20      grad L1      grad L20     L20/L1
small 0.01        1.56e-01   1.14e-16     7.27e-16     7.01e-16     0.96
large 1.0         9.75e-01   9.74e-01     1.74e+08     1.80e-01     1.0e-09
Xavier 1/sqrt(n)  6.27e-01   1.62e-01     1.92e-01     1.58e-01     0.82
```

<figure class="fig">
<svg viewBox="0 0 460 264" role="img" aria-label="Gradient magnitude across twenty layers. Small initialisation is flat at 1e-16, large falls steeply from 1e8 at the first layer, and Xavier stays near 0.2">
<g class="axis">
<line x1="52" y1="230.0" x2="444" y2="230.0"/>
<text class="tick-lbl" x="43" y="233.5" text-anchor="end">1e-18</text>
<line x1="52" y1="183.3" x2="444" y2="183.3"/>
<text class="tick-lbl" x="43" y="186.8" text-anchor="end">1e-12</text>
<line x1="52" y1="136.7" x2="444" y2="136.7"/>
<text class="tick-lbl" x="43" y="140.2" text-anchor="end">1e-6</text>
<line x1="52" y1="90.0" x2="444" y2="90.0"/>
<text class="tick-lbl" x="43" y="93.5" text-anchor="end">1e0</text>
<line x1="52" y1="43.3" x2="444" y2="43.3"/>
<text class="tick-lbl" x="43" y="46.8" text-anchor="end">1e6</text>
<line class="frame" x1="52" y1="20" x2="52" y2="230"/>
<line class="frame" x1="52" y1="230" x2="444" y2="230"/>
<line class="frame" x1="52.0" y1="230" x2="52.0" y2="234"/>
<text class="tick-lbl" x="52.0" y="246" text-anchor="middle">1</text>
<line class="frame" x1="237.7" y1="230" x2="237.7" y2="234"/>
<text class="tick-lbl" x="237.7" y="246" text-anchor="middle">10</text>
<line class="frame" x1="444.0" y1="230" x2="444.0" y2="234"/>
<text class="tick-lbl" x="444.0" y="246" text-anchor="middle">20</text>
<text class="tick-lbl" x="248" y="260" text-anchor="middle">layer</text>
<text class="tick-lbl" x="52" y="13" text-anchor="start">gradient size</text>
</g>
<path class="curve bad" fill="none" d="M 52.0,207.7 L 72.6,207.7 L 93.3,207.7 L 113.9,207.7 L 134.5,207.7 L 155.2,207.7 L 175.8,207.8 L 196.4,207.7 L 217.1,207.8 L 237.7,207.8 L 258.3,207.8 L 278.9,207.7 L 299.6,207.8 L 320.2,207.9 L 340.8,207.7 L 361.5,207.8 L 382.1,207.8 L 402.7,207.8 L 423.4,207.8 L 444.0,207.9"/>
<path class="curve bad2" fill="none" d="M 52.0,25.9 L 72.6,29.6 L 93.3,33.4 L 113.9,36.7 L 134.5,40.3 L 155.2,44.2 L 175.8,47.8 L 196.4,51.3 L 217.1,55.1 L 237.7,59.0 L 258.3,62.5 L 278.9,66.2 L 299.6,69.9 L 320.2,73.6 L 340.8,77.3 L 361.5,81.1 L 382.1,84.8 L 402.7,88.4 L 423.4,92.1 L 444.0,95.8"/>
<path class="curve ok" fill="none" d="M 52.0,95.6 L 72.6,95.9 L 93.3,96.0 L 113.9,96.0 L 134.5,96.0 L 155.2,96.0 L 175.8,96.2 L 196.4,96.2 L 217.1,96.2 L 237.7,96.2 L 258.3,96.2 L 278.9,96.2 L 299.6,96.3 L 320.2,96.3 L 340.8,96.3 L 361.5,96.3 L 382.1,96.4 L 402.7,96.2 L 423.4,96.2 L 444.0,96.2"/>
<text class="lbl bad" x="93.3" y="24.4" text-anchor="start">large 1.0</text>
<text class="lbl ok" x="278.9" y="86.2" text-anchor="middle">Xavier 1/sqrt(n)</text>
<text class="lbl bad" x="278.9" y="222.7" text-anchor="middle">small 0.01</text>
</svg>
<figcaption>Weight-gradient magnitude per layer. One gridline is a million. Small keeps every layer flat at 1e-16, large opens a 1e9 gap between layer 1 and layer 20, and Xavier stays nearly level.</figcaption>
</figure>

## Too small: everything shrinks together

`0.01` shrinks the activations at every layer. What is 0.156 at layer 1 is
`1.14e-16` at layer 20. Sixteen digits gone.

The gradients are flat at around `7e-16` across all layers. No explosion, no
vanishing gradient in the usual sense - **all of them are equally close to
zero**. No learning rate makes weights move at that magnitude.

It is tempting to blame `tanh`. Measured, it is the opposite. The activations
are packed near zero, so the derivative `1 - h^2` is 0.9755 at layer 1 and
`1.0000` to four decimals from layer 3 on. **The derivative is as large as it
can be.**

The culprit is the weight scale. `0.01 x sqrt(256) = 0.16` is the per-layer
factor, and the forward signal shrinks by a measured 0.160 per layer. The
backward signal shrinks by the same 0.16 travelling the other way. Because both
directions decay at the same rate, every layer's weight gradient is
`|input| x |backward signal|`, which lands on `0.16^20` regardless of the layer.
That symmetry is the flat line in the figure.

## Too large: every layer a different world

`1.0` is the opposite. The activation is stuck at 0.975 from layer 1 to layer 20:
`tanh` has saturated. The inputs are large, the outputs pinned near +-1, and in
that region `tanh`'s derivative `1 - h^2` is close to zero.

Yet the gradients do not die. The first layer sits at `1.74e+08`. Multiplying
back through `W` grows the signal faster than the derivative shrinks it. The
problem is not the size itself but the **spread between layers**: layer 1 and
layer 20 differ by `1e9`. There is no single learning rate that serves both.
Tune for layer 20 and layer 1 diverges; tune for layer 1 and layer 20 stops.
This is part two's "one steepest direction sets the ceiling", opened up along
the depth of the network.

## Xavier: set the base of the multiplication to one

`1/sqrt(n)` comes out of one line of variance arithmetic. The variance of a sum
of `n` terms is `n` times the variance of one, so setting the weight variance to
`1/n` preserves the variance across a layer. It puts the base of the
multiplication near one.

To be precise, that calculation balances the **forward** pass only, and what it
yields is `1/n_in` - LeCun initialisation. Balancing the backward pass as well
would want `1/n_out`, and both cannot hold at once; Xavier takes the compromise
`2/(n_in + n_out)`. Here every layer is 256 wide, so the two coincide exactly,
but carrying this derivation to a layer with different widths gives a different
constant from any framework's `xavier_normal_`.

The measurement follows. The gradient is `0.192` at layer 1 and `0.158` at layer
20, a factor of 0.82 across twenty layers.

The comparison needs two axes to be fair. On **uniformity** alone the small
initialisation is actually flatter, at 0.96 - but the flat value is `7e-16`, so
nothing happens. On **magnitude** alone the large one is generous, but its
layers differ by `1e9`. Only Xavier satisfies both: magnitude `0.19`, layer ratio
`0.82`.

Honestly, it is not perfect either. The activations fall from 0.627 to 0.162
over twenty layers, about fourfold, because `tanh` has unit gain only near the
origin and less further out. He initialisation with `2/n` exists for the ReLU
family for the same reason: half the outputs are zeroed, so the variance is
compensated twofold.

## So

- Stacking layers means multiplying the same number that many times. Off one,
  and the drift is exponential
- Too small and forward and backward shrink together at the same rate; too large
  and the spread between layers opens up. Neither is fixable with a learning
  rate
- `1/sqrt(n)` is not magic, it is a variance-preservation formula. Change the
  activation and the constant changes
- Initialisation is less a hyperparameter to tune than the condition under which
  training can start at all

Batch normalisation is visible in the same picture: it rescales at every layer,
so the base is pinned at one and the initial scale stops mattering - with it,
all three initialisations reach 0.63 at layer 20.

Residual connections work differently. A block is `h + f(h)`, so the Jacobian is
`I + J` and an **identity path that skips the multiplication** always survives
on the way back. It does not pin the product at one; it opens a route around it.
On its own it makes the forward scale grow - measured, the activation standard
deviation climbs from 1.2 to 3.8 over twenty blocks. That is why real residual
networks pair it with normalisation or scale the branch by `1/sqrt(L)`.

The next part shakes the data instead of the network. It measures why taking a
step from a fraction of the data - noisier, and wrong more often - arrives
sooner than one step from all of it.
