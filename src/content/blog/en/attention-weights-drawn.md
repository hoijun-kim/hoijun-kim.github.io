---
title: "Taking the attention weights out and looking at them"
description: "Attention is a weighted average whose weights the data decides. This computes the matrix for six tokens and draws it, then measures what happens when the one line dividing by sqrt(d) is removed."
date: 2025-08-01
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 8
---

The first seven parts were about stacking layers and measuring steps. This one
looks at a layer with a different shape. Attention is, in the end, a **weighted
average**; what is unusual is that the weights are not learned constants but
**computed from the input every time**.

Those weights never appear on screen. Take them out and draw them.

## Six tokens

Build embeddings where three topics are shared by two tokens each: `t0` with
`t3`, `t1` with `t4`, `t2` with `t5`.

```python
import numpy as np

X = 2.6 * np.array([
    [1.0, 0.2, 0.0, 0.0],   # t0
    [0.0, 1.0, 0.3, 0.0],   # t1
    [0.0, 0.0, 1.0, 0.2],   # t2
    [0.9, 0.3, 0.0, 0.0],   # t3  - same topic as t0
    [0.1, 0.9, 0.2, 0.0],   # t4  - same topic as t1
    [0.0, 0.1, 0.9, 0.3],   # t5  - same topic as t2
])
d = X.shape[1]

def softmax(a):
    a = a - a.max(-1, keepdims=True)
    e = np.exp(a)
    return e / e.sum(-1, keepdims=True)

A = softmax(X @ X.T / np.sqrt(d))     # the attention weights
out = A @ X                           # the weighted average they produce
```

The projection matrices that make `Q`, `K` and `V` are deliberately left out.
Including all three mixes up what comes from the structure and what comes from
training. Here `Q = K = V = X`, so only the **structure** is on show.

<figure class="fig">
<svg viewBox="0 0 431 421" role="img" aria-label="6x6 attention matrix; each row sums to one and the two darkest cells are always the token itself and the one sharing its topic">
<g class="hm">
<rect x="72" y="60" width="55" height="55" rx="4" style="opacity:0.981"/>
<text class="v on" x="99.5" y="91.5">0.510</text>
<rect x="130" y="60" width="55" height="55" rx="4" style="opacity:0.114"/>
<text class="v off" x="157.5" y="91.5">0.030</text>
<rect x="188" y="60" width="55" height="55" rx="4" style="opacity:0.087"/>
<text class="v off" x="215.5" y="91.5">0.015</text>
<rect x="246" y="60" width="55" height="55" rx="4" style="opacity:0.763"/>
<text class="v on" x="273.5" y="91.5">0.389</text>
<rect x="304" y="60" width="55" height="55" rx="4" style="opacity:0.131"/>
<text class="v off" x="331.5" y="91.5">0.039</text>
<rect x="362" y="60" width="55" height="55" rx="4" style="opacity:0.089"/>
<text class="v off" x="389.5" y="91.5">0.016</text>
<rect x="72" y="118" width="55" height="55" rx="4" style="opacity:0.106"/>
<text class="v off" x="99.5" y="149.5">0.026</text>
<rect x="130" y="118" width="55" height="55" rx="4" style="opacity:1.000"/>
<text class="v on" x="157.5" y="149.5">0.521</text>
<rect x="188" y="118" width="55" height="55" rx="4" style="opacity:0.125"/>
<text class="v off" x="215.5" y="149.5">0.036</text>
<rect x="246" y="118" width="55" height="55" rx="4" style="opacity:0.125"/>
<text class="v off" x="273.5" y="149.5">0.036</text>
<rect x="304" y="118" width="55" height="55" rx="4" style="opacity:0.666"/>
<text class="v on" x="331.5" y="149.5">0.336</text>
<rect x="362" y="118" width="55" height="55" rx="4" style="opacity:0.142"/>
<text class="v off" x="389.5" y="149.5">0.046</text>
<rect x="72" y="176" width="55" height="55" rx="4" style="opacity:0.087"/>
<text class="v off" x="99.5" y="207.5">0.015</text>
<rect x="130" y="176" width="55" height="55" rx="4" style="opacity:0.135"/>
<text class="v off" x="157.5" y="207.5">0.042</text>
<rect x="188" y="176" width="55" height="55" rx="4" style="opacity:0.979"/>
<text class="v on" x="215.5" y="207.5">0.509</text>
<rect x="246" y="176" width="55" height="55" rx="4" style="opacity:0.087"/>
<text class="v off" x="273.5" y="207.5">0.015</text>
<rect x="304" y="176" width="55" height="55" rx="4" style="opacity:0.114"/>
<text class="v off" x="331.5" y="207.5">0.030</text>
<rect x="362" y="176" width="55" height="55" rx="4" style="opacity:0.762"/>
<text class="v on" x="389.5" y="207.5">0.389</text>
<rect x="72" y="234" width="55" height="55" rx="4" style="opacity:0.904"/>
<text class="v on" x="99.5" y="265.5">0.468</text>
<rect x="130" y="234" width="55" height="55" rx="4" style="opacity:0.151"/>
<text class="v off" x="157.5" y="265.5">0.050</text>
<rect x="188" y="234" width="55" height="55" rx="4" style="opacity:0.093"/>
<text class="v off" x="215.5" y="265.5">0.018</text>
<rect x="246" y="234" width="55" height="55" rx="4" style="opacity:0.749"/>
<text class="v on" x="273.5" y="265.5">0.382</text>
<rect x="304" y="234" width="55" height="55" rx="4" style="opacity:0.171"/>
<text class="v off" x="331.5" y="265.5">0.062</text>
<rect x="362" y="234" width="55" height="55" rx="4" style="opacity:0.096"/>
<text class="v off" x="389.5" y="265.5">0.020</text>
<rect x="72" y="292" width="55" height="55" rx="4" style="opacity:0.146"/>
<text class="v off" x="99.5" y="323.5">0.047</text>
<rect x="130" y="292" width="55" height="55" rx="4" style="opacity:0.912"/>
<text class="v on" x="157.5" y="323.5">0.472</text>
<rect x="188" y="292" width="55" height="55" rx="4" style="opacity:0.125"/>
<text class="v off" x="215.5" y="323.5">0.036</text>
<rect x="246" y="292" width="55" height="55" rx="4" style="opacity:0.172"/>
<text class="v off" x="273.5" y="323.5">0.062</text>
<rect x="304" y="292" width="55" height="55" rx="4" style="opacity:0.667"/>
<text class="v on" x="331.5" y="323.5">0.337</text>
<rect x="362" y="292" width="55" height="55" rx="4" style="opacity:0.143"/>
<text class="v off" x="389.5" y="323.5">0.046</text>
<rect x="72" y="350" width="55" height="55" rx="4" style="opacity:0.095"/>
<text class="v off" x="99.5" y="381.5">0.019</text>
<rect x="130" y="350" width="55" height="55" rx="4" style="opacity:0.174"/>
<text class="v off" x="157.5" y="381.5">0.063</text>
<rect x="188" y="350" width="55" height="55" rx="4" style="opacity:0.895"/>
<text class="v on" x="215.5" y="381.5">0.462</text>
<rect x="246" y="350" width="55" height="55" rx="4" style="opacity:0.096"/>
<text class="v off" x="273.5" y="381.5">0.020</text>
<rect x="304" y="350" width="55" height="55" rx="4" style="opacity:0.141"/>
<text class="v off" x="331.5" y="381.5">0.045</text>
<rect x="362" y="350" width="55" height="55" rx="4" style="opacity:0.765"/>
<text class="v on" x="389.5" y="381.5">0.391</text>
</g><g class="lbl-ax">
<text x="99.5" y="46">t0</text>
<text x="157.5" y="46">t1</text>
<text x="215.5" y="46">t2</text>
<text x="273.5" y="46">t3</text>
<text x="331.5" y="46">t4</text>
<text x="389.5" y="46">t5</text>
<text class="r" x="58" y="91.5">t0</text>
<text class="r" x="58" y="149.5">t1</text>
<text class="r" x="58" y="207.5">t2</text>
<text class="r" x="58" y="265.5">t3</text>
<text class="r" x="58" y="323.5">t4</text>
<text class="r" x="58" y="381.5">t5</text>
<text class="cap" x="244.5" y="22">looked at &rarr;</text>
<text class="cap l" x="6" y="22">from &darr;</text>
</g>
</svg>
<figcaption>The attention weight matrix. One row is one token's gaze and sums to one. The two darkest cells in every row are always the token itself and the one sharing its topic, together taking 0.81 to 0.90 of the row; unrelated tokens sit at 0.015 and are effectively ignored.</figcaption>
</figure>

## A row is one token's gaze

Row `t0` gives `0.510` to itself, `0.389` to `t3` which shares its topic, and
between `0.015` and `0.039` to the rest. The ratio of partner to unrelated is
`0.389 / 0.015`, about 26 times. All six rows have the same shape: **in every
row the top two cells are the token itself and its topic partner**, and those
two take between `0.81` and `0.90` of the row. The remaining four together come
to under `0.2`, the largest of them `0.063`.

The **order** of those top two differs by row, though. `t3`, `t4` and `t5` give
more to their partner than to themselves - `t3` gives itself `0.382` and `t0`
`0.468`. A dot product sees magnitude as well as direction, and with norms of
`2.651` for `t0` against `2.467` for `t3`, `t3` finds `t0` a closer match than
itself. Attention holds no rule saying "I look at me". It has one rule,
similarity, and size counts as part of similarity.

Each row sums to one, because what attention does is not **selection** but
**allocation**. It decides how much to look where, and mixes the values in that
proportion. Multiplying by this matrix, `A @ X`, is the layer's output.

Nothing here was learned. Similar embeddings give a large dot product, and a
large dot product gets a large share from the softmax. A real transformer uses
`XW_q` and `XW_k` instead of `X`, but what those `W`s do is **choose which
similarity to look at**, not change this structure.

## The line that divides by sqrt(d)

There is a `/ np.sqrt(d)` after `X @ X.T`. Here is what happens without it, as
the dimension grows - eight random vectors, an 8x8 attention.

```python
for d in (4, 16, 64, 256, 1024):
    rng = np.random.default_rng(0)
    for _ in range(200):                       # averaged over 200 trials
        q = rng.standard_normal((8, d))
        k = rng.standard_normal((8, d))
        L = q @ k.T
        raw, scaled = softmax(L), softmax(L / np.sqrt(d))
```

```
    d   logit sd   max prob (raw)   max prob (scaled)   entropy (raw)   entropy (scaled)
    4       1.93            0.526               0.342           1.290              1.750
   16       3.88            0.755               0.359           0.662              1.732
   64       7.94            0.872               0.357           0.323              1.728
  256      15.81            0.937               0.361           0.157              1.719
 1024      31.89            0.968               0.363           0.078              1.716
```

Spreading evenly over eight would give an entropy of `2.079`.

The logits' standard deviation grows with the dimension. A dot product of two
vectors with unit-variance components is a sum of `d` terms, so its standard
deviation is `sqrt(d)`; the measured `1.93, 3.88, 7.94, 15.81, 31.89` sit right
on top of `2, 4, 8, 16, 32`.

Softmax sharpens as its inputs spread. So at `d=1024` the largest probability
climbs to `0.968` and the entropy falls to `0.078` against `2.079` for looking
evenly. **It looks at one place and throws away the rest.** That is not a
weighted average any more, it is a selection.

Dividing by `sqrt(d)` brings the logits' standard deviation back to about one
regardless of dimension. In the table, while the dimension grows 256-fold, the
largest probability moves from `0.342` to `0.363` and the entropy from `1.750`
to `1.716` - which is to say, not at all.

## The real problem is the gradient

Why is sharpening bad? Part three answers it. The softmax Jacobian has
`p_i(1-p_i)` on the diagonal and `-p_i p_j` off it. Once the probability piles
up in one place and `p` sits near 0 or 1, both terms die. What follows measures
its trace, `sum p(1-p)`; a small trace means the whole Jacobian is small.

```
    d   sum p(1-p) (raw)   sum p(1-p) (scaled)
    4             0.6052                0.7747
   16             0.3397                0.7691
   64             0.1809                0.7705
  256             0.0908                0.7668
 1024             0.0465                0.7651
```

Without the division this keeps shrinking with dimension, down to `0.0465` at
`d=1024`. With it, the value does not budge from about `0.77`. **A factor of
16.5.** It is the same accident as part four - saturate the forward value and
the derivative at that point disappears. `sqrt(d)` is not performance tuning but
**the condition under which training starts**.

## Attention does not know about order

One last thing. The matrix above was built from the **contents** of the tokens.
Position entered nowhere.

```python
perm = [3, 1, 5, 0, 4, 2]
A2 = softmax(X[perm] @ X[perm].T / np.sqrt(d))
np.allclose(A2 @ X[perm], (A @ X)[perm])   # True
```

Shuffle the inputs and the outputs shuffle identically. The values do not
change, **only their places do**. Attention has no "before" and no "after".

In a sentence, order is meaning. So a transformer adds position separately.
Why positional encoding is needed is entirely explained by this one experiment:
without it the model has no way at all to see word order.

## So

- Attention is a weighted average and the weights are computed from the input.
  Each row sums to one
- That matrix can be taken out and looked at. Here every row's top two cells are
  the token and its topic partner: `0.389` against `0.015` for an unrelated one,
  a factor of 26
- `sqrt(d)` undoes the `sqrt(d)` growth of the logits with dimension. Without it,
  `d=1024` saturates at max probability `0.968` and entropy `0.078`
- Saturation is paid for in gradient: `0.0465` against `0.7651` at `d=1024`, a
  factor of 16.5
- Attention knows nothing about order. Positional encoding is not decoration, it
  supplies information that is otherwise absent

Eight parts. From where a tensor sits, through steps, derivatives, layers,
batches, normalisation and generalisation, to a layer that computes its own
weights. Measured and drawn, every time.

The next part fills the hole just left open. If attention does not know about
order, how does order get in? Positional encoding, measured.
