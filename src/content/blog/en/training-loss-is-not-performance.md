---
title: "How to drive the training error to zero, and what it costs"
description: "Fit eighteen points with a seventeen-degree polynomial and the training error is 3e-17. Perfectly fitted. On fresh points from the same distribution the error is 3.9e10. This walks the degrees to see what happened in between."
date: 2025-07-31
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 7
---

The first six parts were all about **how to bring the loss down**: the size of a
step, the path a derivative takes, stacking layers, splitting data. This one
turns the other way and asks what happens once the loss is all the way down.

## Eighteen points, rising degree

Take eighteen points from a curve and add noise. The noise has standard
deviation `0.25`, so **the expected mean squared error on new data cannot go
below `0.0625`**. Below that is the noise itself, which is not there to be
fitted.

```python
f = lambda x: np.sin(1.6*x) + 0.35*x
x_tr = np.sort(rng.uniform(-3, 3, 18))
y_tr = f(x_tr) + 0.25 * rng.standard_normal(18)
```

The training error is not bounded by that floor. Training points are already
seen, so their noise can be memorised, and in the table below the training error
crosses `0.0625` from degree five on. That is the subject of this part.

Raise the degree from 1 to 17 and measure the error on the eighteen training
points and on 500 fresh ones. The fitting works like this: `x^17` is `1.3e8` at
`x=3`, so the columns would differ in scale by eight orders of magnitude. Each
power is centred and standardised against the training data before fitting, and
the intercept is left out of the penalty.

```python
def design(x, deg, mu=None, sd=None):
    A = np.vander(x, deg+1, increasing=True)[:, 1:]   # no constant column
    if mu is None: mu, sd = A.mean(0), A.std(0) + 1e-12
    return np.hstack([np.ones((len(x), 1)), (A - mu) / sd]), mu, sd

def fit(deg, lam=0.0):
    A, mu, sd = design(x_tr, deg)
    if lam == 0:
        c = np.linalg.lstsq(A, y_tr, rcond=None)[0]
    else:
        P = np.eye(A.shape[1]); P[0, 0] = 0            # intercept unpenalised
        c = np.linalg.solve(A.T @ A + lam * P, A.T @ y_tr)
    return c
```

Every "coefficient" in the tables below is a coefficient **in that standardised
basis**. Change the basis and the numbers change, which comes up again later.

```
degree    training     validation    largest coefficient
1         0.38697       0.7104              0.68
3         0.08564       0.3343              1.73
6         0.04163       0.0934              4.41
8         0.01869       3.8295             57.08
12        0.01721     587.0880              1144
17        0.00000  38959385960            2.2e+07
```

<figure class="fig">
<svg viewBox="0 0 460 272" role="img" aria-label="Training and validation error against polynomial degree. Training falls far enough to leave the axis; validation bottoms out at degree 6 and then climbs">
<g class="axis">
<line x1="52" y1="232.0" x2="434" y2="232.0"/>
<text class="tick-lbl" x="43" y="235.5" text-anchor="end">1e-6</text>
<line x1="52" y1="183.5" x2="434" y2="183.5"/>
<text class="tick-lbl" x="43" y="187.0" text-anchor="end">1e-2</text>
<line x1="52" y1="135.1" x2="434" y2="135.1"/>
<text class="tick-lbl" x="43" y="138.6" text-anchor="end">1e2</text>
<line x1="52" y1="86.6" x2="434" y2="86.6"/>
<text class="tick-lbl" x="43" y="90.1" text-anchor="end">1e6</text>
<line x1="52" y1="38.1" x2="434" y2="38.1"/>
<text class="tick-lbl" x="43" y="41.6" text-anchor="end">1e10</text>
<line class="frame" x1="52" y1="26" x2="52" y2="232"/><line class="frame" x1="52" y1="232" x2="434" y2="232"/>
<line class="frame" x1="52.0" y1="232" x2="52.0" y2="236"/><text class="tick-lbl" x="52.0" y="248" text-anchor="middle">1</text>
<line class="frame" x1="171.4" y1="232" x2="171.4" y2="236"/><text class="tick-lbl" x="171.4" y="248" text-anchor="middle">6</text>
<line class="frame" x1="266.9" y1="232" x2="266.9" y2="236"/><text class="tick-lbl" x="266.9" y="248" text-anchor="middle">10</text>
<line class="frame" x1="362.4" y1="232" x2="362.4" y2="236"/><text class="tick-lbl" x="362.4" y="248" text-anchor="middle">14</text>
<line class="frame" x1="434.0" y1="232" x2="434.0" y2="236"/><text class="tick-lbl" x="434.0" y="248" text-anchor="middle">17</text>
<text class="tick-lbl" x="243" y="266" text-anchor="middle">polynomial degree</text>
<text class="tick-lbl" x="52" y="16" text-anchor="start">mean squared error</text>
<line class="floor" x1="52" y1="173.9" x2="434" y2="173.9"/>
<text class="tick-lbl" x="58" y="158.9" text-anchor="start">noise floor 0.0625 (validation only)</text>
</g>
<path class="curve bad" fill="none" d="M 52.0,164.3 L 75.9,164.3 L 99.8,172.2 L 123.6,173.3 L 147.5,175.9 L 171.4,176.0 L 195.2,177.3 L 219.1,180.2 L 243.0,180.2 L 266.9,180.2 L 290.8,180.6 L 314.6,180.7 L 338.5,182.0 L 362.4,182.9 L 386.2,184.5 L 410.1,186.5 L 434.0,230.0"/>
<path class="offscale" d="M 434.0 230.0 L 434.0 241.0" marker-end="url(#dn)"/>
<defs><marker id="dn" viewBox="0 0 8 8" refX="4" refY="7" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 0 L4 8 z" class="head-off"/></marker></defs>
<text class="lbl bad" x="430.0" y="267.0" text-anchor="end">3e-17</text>
<path class="curve ok" fill="none" d="M 52.0,161.1 L 75.9,161.1 L 99.8,165.1 L 123.6,164.3 L 147.5,170.3 L 171.4,171.8 L 195.2,161.8 L 219.1,152.2 L 243.0,150.6 L 266.9,149.2 L 290.8,133.9 L 314.6,125.7 L 338.5,100.1 L 362.4,89.1 L 386.2,75.1 L 410.1,45.7 L 434.0,31.0"/>
<circle class="opt" cx="171.4" cy="171.8" r="4"/>
<text class="lbl ok" x="314.6" y="116.7" text-anchor="middle">validation</text>
<text class="lbl bad" x="290.8" y="196.6" text-anchor="middle">training</text>
<text class="lbl ok" x="171.4" y="189.8" text-anchor="middle">deg 6</text>
</svg>
<figcaption>As the degree rises the training error falls far enough to leave the axis (3e-17 at degree 17) while validation turns at degree 6. One gridline is 10,000x. The dashed line is the lower bound on expected error for new data, so it applies to the validation curve only.</figcaption>
</figure>

## The two curves separate

The training error goes all the way down. Of course it does: each added degree
frees the curve further, and at degree 17 eighteen parameters pass through
eighteen points, so it goes **exactly through them**. A training error of `3e-17`
is floating-point zero.

The validation error bottoms out at degree 6 with `0.0934`, respectably close to
the noise floor of `0.0625`, and then turns. After that: `3.83` at degree 8,
`587` at degree 12, `3.9e10` at degree 17. Squeezing the last `0.04` out of
training cost twelve orders of magnitude on validation.

The coefficients say what happened. Up to degree 6 the largest is `4.4`; at
degree 17 it is `2.2e+07`. Passing exactly through eighteen points requires
bending violently between them, and that bending explodes **between** the
training points. On the training points the error is zero, so the training loss
cannot see it.

One caveat on those coefficients: they are numbers attached to a basis. On the
raw monomial basis, measured with `np.polyfit`, the largest coefficient at degree
17 is `455`, and degree 6's `1.67` is larger than degree 8's `1.36`. The same
curve written in different coordinates changes both the number and the
monotonicity. As an indicator of the blow-up it works; its absolute value means
nothing.

This is what overfitting is. The model did not learn the signal, it **memorised
the coordinates of the noise**. The next sample has different noise, so what was
memorised cannot fit it.

## Lowering the degree is not the only answer

The usual conclusion is "make the model smaller". Half right. Keep degree 17 and
just price the coefficients: add `lambda * (sum of squared coefficients)` to the
loss, which is the `lam` in `fit` above. The penalty applies to the
**standardised** coefficients - ridge is not scale-invariant, and the same
`lambda` on the raw monomial basis gives a completely different result (there,
`lambda=0.01` scores `1.1e6` on validation).

```
degree 17 fixed    training    validation   largest coefficient
lambda 0            0.00000  38959385960          2.2e+07
lambda 1e-4         0.02105       3.4008            10.09
lambda 1e-2         0.03354       0.1354             3.13
lambda 0.1          0.06441       0.3578             1.77
lambda 1.0          0.11434       0.7403             1.15
```

At `lambda = 0.01` the validation error is `0.1354`, close to the `0.0934` of the
model whose degree was lowered to 6. **It is the same degree-17 model.** Its
expressiveness was not reduced; a price was put on using it.

The coefficient falling from `2.2e+07` to `3.13` is what that price did. A
degree-17 curve is available, but bending it hard costs loss, so the optimiser
picks a gentler one on its own.

Too strong a penalty goes the other way. At `lambda = 1.0` even the training
error rises to `0.114` and validation degrades to `0.74`. The signal has been
squashed along with everything else.

## What tells you when to stop

The reason the validation error was knowable above is that 500 labelled points
were held aside. In practice those 500 are the **validation set**.

From which one rule follows. The training loss cannot tell you when to stop,
because it goes all the way down. The stopping point can only be set by data
that was not trained on. And the moment that data is used to choose
hyperparameters it becomes a kind of training set, so the final number has to be
measured on yet another split.

## So

- The training error keeps falling as parameters are added. It reaches zero.
  That number is not performance
- The validation error traces a U. Here it bottoms at degree 6, reaching `0.0934`
  against a noise floor of `0.0625`
- Overfitting is less a problem of expressiveness than of **unpriced
  expressiveness**. Degree 17 with ridge at `0.01` comes back from `3.9e10` to
  `0.1354`
- A penalty is harmful in proportion to its strength. It squashes the signal too
- Only data that was not trained on can answer when to stop

Seven parts, one full circuit. It started where a tensor sits, went through steps
and derivatives and layers and batches, and ends on the difference between
predicting well and memorising well. Every one of them measured once, and drawn.
