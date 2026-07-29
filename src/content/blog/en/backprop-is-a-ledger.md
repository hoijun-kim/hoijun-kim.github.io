---
title: "Backpropagation is a ledger"
description: "Follow the derivatives through a three-node graph by hand, then check them against numerical differences. Backpropagation is not a new way to differentiate - it is a way of not throwing away what you already computed."
date: 2026-07-29
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 3
---

In the previous part the gradient was written by hand. Two parameters and a
one-line formula made that possible. Stack layers and it stops being possible,
which is what backpropagation is for.

Most of the difficulty people report with it comes from its being introduced as
a new kind of differentiation. It is not. The only rule is the chain rule from
school, and backpropagation is the trick of **writing the intermediate values
into a ledger instead of discarding them**.

## One neuron

Start with the smallest real thing: one input, one weight, one bias, a sigmoid,
and squared error.

```python
import numpy as np

w, b, x, t = 0.5, -0.2, 2.0, 1.0

z = w * x + b                 # 0.8
a = 1 / (1 + np.exp(-z))      # 0.689974
L = (a - t) ** 2              # 0.096116
```

```
z=0.800000  a=0.689974  L=0.096116
```

Now for `dL/dw`. Read the chain rule like this: wobble `w` and `z` wobbles,
wobble `z` and `a` wobbles, wobble `a` and `L` wobbles. Multiply the ratios of
the wobbles.

<figure class="fig">
<svg viewBox="0 0 460 232" role="img" aria-label="A computation graph from w, x and b through z and a to L. The top arrow carries values forward, the bottom arrow carries derivatives back">
<defs><marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="head"/></marker><marker id="ahb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 z" class="head-b"/></marker></defs>
<g class="lane-mark">
<path d="M10 34 L432 34" marker-end="url(#ah)"/>
<text x="10" y="26">forward - values this way</text>
<path class="b" d="M438 196 L16 196" marker-end="url(#ahb)"/>
<text class="b" x="438" y="188" text-anchor="end">backward - derivatives this way</text>
</g>
<g class="edge">
<path d="M92 62 C 122 62, 128 100, 152 100" marker-end="url(#ah)"/>
<path d="M92 100 C 122 100, 128 100, 152 100" marker-end="url(#ah)"/>
<path d="M92 138 C 122 138, 128 100, 152 100" marker-end="url(#ah)"/>
<path d="M214 100 L256 100" marker-end="url(#ah)"/>
<path d="M318 100 L360 100" marker-end="url(#ah)"/>
</g>
<g class="grad-link">
<path d="M10 62 L4 62 L4 172 L14 172"/>
<text x="18" y="176">dL/dw = -0.2653</text>
</g>
<g class="node">
<rect x="10" y="47.0" width="82" height="30" rx="6"/>
<rect x="10" y="85.0" width="82" height="30" rx="6"/>
<rect x="10" y="123.0" width="82" height="30" rx="6"/>
<rect x="158" y="85.0" width="56" height="30" rx="8" class="op"/>
<rect x="262" y="85.0" width="56" height="30" rx="8" class="op"/>
<rect x="366" y="85.0" width="72" height="30" rx="8" class="out"/>
</g>
<g class="txt">
<text x="51.0" y="66">w 0.5</text>
<text x="51.0" y="104">x 2.0</text>
<text x="51.0" y="142">b -0.2</text>
<text x="186.0" y="104">z</text>
<text x="290.0" y="104">a</text>
<text x="402.0" y="104">L</text>
</g>
<g class="fwd">
<text x="186.0" y="76.0">0.800</text>
<text x="290.0" y="76.0">0.690</text>
<text x="402.0" y="76.0">0.0961</text>
</g>
<g class="bwd">
<text x="186.0" y="133.0">-0.1326</text>
<text x="290.0" y="133.0">-0.6201</text>
<text x="402.0" y="133.0">1</text>
</g>
</svg>
<figcaption>The same graph, walked twice. Forward it carries values, backward it carries derivatives. The bottom row is how much each node moves the loss.</figcaption>
</figure>

Three pieces, computed separately.

```python
dL_da = 2 * (a - t)     # -0.620051
da_dz = a * (1 - a)     #  0.213910
dz_dw = x               #  2.0
```

`a * (1 - a)` is the sigmoid's derivative, and here is the first economy: `a` is
**already in the ledger from the forward pass**, so the sigmoid is never
evaluated again. The stored value is used as it stands.

Multiply and it is done.

```python
dL_dz = dL_da * da_dz            # -0.132635
print(dL_dz * dz_dw)             # dL/dw
print(dL_dz * 1.0)               # dL/db
```

```
dL/dw=-0.265270  dL/db=-0.132635
```

## Do not trust it, check it

Hand-derived formulas are easy to get wrong, so compare against numerical
differences. Wobble the parameter a little and measure how much the loss moves.

```python
def L_of(w_, b_):
    return (1 / (1 + np.exp(-(w_ * x + b_))) - t) ** 2

h = 1e-6
num_w = (L_of(w + h, b) - L_of(w - h, b)) / (2 * h)
num_b = (L_of(w, b + h) - L_of(w, b - h)) / (2 * h)
```

```
        analytic                 numerical                agreement
dL/dw   -0.26526985862215685     -0.2652698586486091      10 decimals
dL/db   -0.13263492931107843     -0.1326349292687934       9 decimals
```

`dL/dw` parts company at the eleventh decimal, `dL/db` at the tenth. Two
quantities measured the same way, at the same `h`, landing on different accuracy
is already the hint: the precision of a numerical derivative is not a fixed
number. It depends on what is being measured and on `h`.

This comparison is called **gradient checking**, and it is the first safety net
to attach when implementing a layer yourself. It needs two forward passes per
parameter, so it is useless for training. For checking it carries the `h`
problem below, so it is better used against a stated threshold - relative error
under 1e-8, say - than a digit count.

The two-sided difference is not an accident either. Its truncation error goes
like `h^2`, so cutting `h` by ten cuts the error by a hundred. That is the left
column below.

```
h=1e-2  error 8.9e-06        h=1e-6  error 2.6e-11
h=1e-3  error 8.9e-08        h=1e-8  error 2.3e-09
h=1e-4  error 8.9e-10        h=1e-10 error 3.1e-08
h=1e-5  error 6.3e-12        h=1e-12 error 2.9e-06
```

Past `1e-5` the direction reverses. `L(w+h)` and `L(w-h)` are nearly equal, so
subtracting them destroys significant digits, and dividing by a tiny `2h`
amplifies what is left. At `1e-12` the estimate is worse than at `1e-2`. The
useful `h` is not the smallest one but somewhere in the middle - around `1e-5`
in double precision.

## Where paths meet, derivatives add

What happens when a node is used twice? Practically all of the confusion in
backpropagation lives here.

```python
a, b = 3.0, 4.0
c = a * b        # 12
d = a + c        # 15  -> a was used twice
```

`a` reaches `d` by two routes, directly and through `c`. The rule is simple:
**add the contribution of every path.**

```
dd/da = 1 (direct) + 1 x b (through c) = 1 + 4 = 5
numerical: 5.000000
```

That is why a framework accumulates gradients with `+=` rather than `=` **within
one backward pass**.

`zero_grad()` is one step removed from this. That is accumulation **between**
passes, not within one, and frameworks do it deliberately because it is useful:
splitting a batch, backpropagating several times and updating once relies on it.
The price is that a step which does not clear the buffer inherits the previous
step's gradient.

## Why backwards

Multiplying the derivatives front to back gives the same answer. It is a real
method, called forward mode. Nobody uses it in deep learning, because of the
shape of the problem.

There are N parameters and one loss. Going forwards means one sweep per
parameter, N sweeps. Going backwards starts from the single loss and produces
every parameter's gradient in **one**. At a hundred million parameters that is a
hundred million to one.

Backpropagation is not special in itself. What is special is that counting
backwards is overwhelmingly cheaper when the entrance is wide and the exit is a
single number.

## So

- The mathematics is one chain rule. The rest is not discarding the forward pass
- Where a node branches, the paths add. That is what `+=` inside one backward
  pass is for; `zero_grad()` is the separate business of clearing between passes
- Check hand-derived gradients numerically, near `h=1e-5`, against a relative
  error threshold
- The reason to go backwards is not calculus. It is arithmetic on counts

That is tensors, steps and gradients. The next part stacks layers and watches
what twenty of these multiplications do to a gradient.
