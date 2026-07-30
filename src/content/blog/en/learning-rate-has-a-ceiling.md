---
title: "There is a line the learning rate cannot cross"
description: "Plot what gradient descent does to a two-parameter loss and the divergence boundary stops being a matter of taste. It falls out of a calculation, and the experiment agrees to three decimal places."
date: 2025-07-29
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 2
---

The learning rate is usually taught like this: too small is slow, too large
diverges. True, and useless, because it never says how large is large.

With two parameters the boundary can be computed **exactly**. Compute it once
and the same reason explains why the learning rate cannot be raised on a model
with a hundred million parameters.

## Building a loss surface

Four points, one straight line. The parameters are the slope `w` and the
intercept `b`.

```python
import numpy as np

x = np.array([1., 2., 3., 4.])
y = np.array([2., 4., 5., 8.])

def loss(w, b):
    return np.mean((w * x + b - y) ** 2)

def grad(w, b):
    e = w * x + b - y
    return 2 * np.mean(e * x), 2 * np.mean(e)
```

The answer is known in advance: least squares gives `w = 1.9`, `b = 0`, with
loss `0.175`. The data carries noise, so the loss does not reach zero.

Two parameters make the loss a surface. This one is exactly quadratic, so the
contours are ellipses - not round ones, but stretched more than sevenfold in one
direction. That elongation decides everything in the next two sections.

## One step

Gradient descent is one line. Step against the gradient, by the learning rate.

```python
w = b = 0.0
lr = 0.05
for step in range(5):
    gw, gb = grad(w, b)
    w, b = w - lr * gw, b - lr * gb
    print(f"step {step+1}: w={w:.4f} b={b:.4f} loss={loss(w, b):.4f}")
```

```
step 1: w=1.4250 b=0.4750 loss=0.9647
step 2: w=1.6625 b=0.5463 loss=0.2478
step 3: w=1.7041 b=0.5510 loss=0.2267
step 4: w=1.7133 b=0.5449 loss=0.2247
step 5: w=1.7171 b=0.5371 loss=0.2232
```

The first step dwarfs the rest: the loss falls from 27.25 to 0.96. After that it
looks stopped - five steps move it from 0.2478 to 0.2232, about one percent.

It has not stopped. Two hundred steps from the start reach `w=1.8904`,
`b=0.0284`, loss `0.1751`, which is essentially the minimum. **Across the valley
it is fast, along the valley it is slow.** The contours being long ellipses
rather than circles shows up directly in the walk.

## The boundary is a calculation

Raise the learning rate.

```
lr=0.11   loss after 200 steps 0.175
lr=0.119  loss after 200 steps 0.343
lr=0.121  loss after 200 steps 100803
lr=0.13   loss after 200 steps 7.3e+28
```

<figure class="fig">
<svg viewBox="0 0 460 260" role="img" aria-label="Loss curves for four learning rates. 0.05 and 0.119 fall while 0.121 and 0.13 climb">
<g class="axis">
<line x1="50" y1="205.4" x2="446" y2="205.4"/>
<text class="tick-lbl" x="41" y="208.9" text-anchor="end">1e0</text>
<line x1="50" y1="164.2" x2="446" y2="164.2"/>
<text class="tick-lbl" x="41" y="167.7" text-anchor="end">1e2</text>
<line x1="50" y1="123.0" x2="446" y2="123.0"/>
<text class="tick-lbl" x="41" y="126.5" text-anchor="end">1e4</text>
<line x1="50" y1="81.8" x2="446" y2="81.8"/>
<text class="tick-lbl" x="41" y="85.3" text-anchor="end">1e6</text>
<line x1="50" y1="40.6" x2="446" y2="40.6"/>
<text class="tick-lbl" x="41" y="44.1" text-anchor="end">1e8</text>
<line class="frame" x1="50" y1="20" x2="50" y2="226"/>
<line class="frame" x1="50" y1="226" x2="446" y2="226"/>
<line class="frame" x1="50.0" y1="226" x2="50.0" y2="230"/>
<text class="tick-lbl" x="50.0" y="242" text-anchor="middle">0</text>
<line class="frame" x1="182.0" y1="226" x2="182.0" y2="230"/>
<text class="tick-lbl" x="182.0" y="242" text-anchor="middle">20</text>
<line class="frame" x1="314.0" y1="226" x2="314.0" y2="230"/>
<text class="tick-lbl" x="314.0" y="242" text-anchor="middle">40</text>
<line class="frame" x1="446.0" y1="226" x2="446.0" y2="230"/>
<text class="tick-lbl" x="446.0" y="242" text-anchor="middle">60</text>
<text class="tick-lbl" x="248" y="256" text-anchor="middle">step</text>
<text class="tick-lbl" x="41" y="13" text-anchor="end">loss</text>
</g>
<path class="curve ok draw" pathLength="1" fill="none" d="M 50.0,175.8 L 56.6,205.7 L 63.2,217.9 L 69.8,218.7 L 76.4,218.8 L 83.0,218.8 L 89.6,218.9 L 96.2,218.9 L 102.8,219.0 L 109.4,219.0 L 116.0,219.1 L 122.6,219.1 L 129.2,219.2 L 135.8,219.2 L 142.4,219.3 L 149.0,219.3 L 155.6,219.4 L 162.2,219.4 L 168.8,219.5 L 175.4,219.5 L 182.0,219.5 L 188.6,219.6 L 195.2,219.6 L 201.8,219.7 L 208.4,219.7 L 215.0,219.7 L 221.6,219.8 L 228.2,219.8 L 234.8,219.8 L 241.4,219.9 L 248.0,219.9 L 254.6,219.9 L 261.2,220.0 L 267.8,220.0 L 274.4,220.0 L 281.0,220.0 L 287.6,220.1 L 294.2,220.1 L 300.8,220.1 L 307.4,220.2 L 314.0,220.2 L 320.6,220.2 L 327.2,220.2 L 333.8,220.2 L 340.4,220.3 L 347.0,220.3 L 353.6,220.3 L 360.2,220.3 L 366.8,220.3 L 373.4,220.4 L 380.0,220.4 L 386.6,220.4 L 393.2,220.4 L 399.8,220.4 L 406.4,220.4 L 413.0,220.5 L 419.6,220.5 L 426.2,220.5 L 432.8,220.5 L 439.4,220.5 L 446.0,220.5"/>
<path class="curve ok2 draw" pathLength="1" fill="none" d="M 50.0,175.8 L 56.6,176.1 L 63.2,176.3 L 69.8,176.5 L 76.4,176.7 L 83.0,177.0 L 89.6,177.2 L 96.2,177.4 L 102.8,177.6 L 109.4,177.9 L 116.0,178.1 L 122.6,178.3 L 129.2,178.5 L 135.8,178.8 L 142.4,179.0 L 149.0,179.2 L 155.6,179.5 L 162.2,179.7 L 168.8,179.9 L 175.4,180.1 L 182.0,180.4 L 188.6,180.6 L 195.2,180.8 L 201.8,181.0 L 208.4,181.3 L 215.0,181.5 L 221.6,181.7 L 228.2,181.9 L 234.8,182.2 L 241.4,182.4 L 248.0,182.6 L 254.6,182.8 L 261.2,183.1 L 267.8,183.3 L 274.4,183.5 L 281.0,183.7 L 287.6,183.9 L 294.2,184.2 L 300.8,184.4 L 307.4,184.6 L 314.0,184.8 L 320.6,185.1 L 327.2,185.3 L 333.8,185.5 L 340.4,185.7 L 347.0,186.0 L 353.6,186.2 L 360.2,186.4 L 366.8,186.6 L 373.4,186.8 L 380.0,187.1 L 386.6,187.3 L 393.2,187.5 L 399.8,187.7 L 406.4,188.0 L 413.0,188.2 L 419.6,188.4 L 426.2,188.6 L 432.8,188.8 L 439.4,189.1 L 446.0,189.3"/>
<path class="curve bad draw" pathLength="1" fill="none" d="M 50.0,175.8 L 56.6,175.5 L 63.2,175.1 L 69.8,174.7 L 76.4,174.4 L 83.0,174.0 L 89.6,173.6 L 96.2,173.3 L 102.8,172.9 L 109.4,172.6 L 116.0,172.2 L 122.6,171.8 L 129.2,171.5 L 135.8,171.1 L 142.4,170.7 L 149.0,170.4 L 155.6,170.0 L 162.2,169.6 L 168.8,169.3 L 175.4,168.9 L 182.0,168.5 L 188.6,168.2 L 195.2,167.8 L 201.8,167.4 L 208.4,167.1 L 215.0,166.7 L 221.6,166.3 L 228.2,166.0 L 234.8,165.6 L 241.4,165.2 L 248.0,164.9 L 254.6,164.5 L 261.2,164.1 L 267.8,163.8 L 274.4,163.4 L 281.0,163.0 L 287.6,162.6 L 294.2,162.3 L 300.8,161.9 L 307.4,161.5 L 314.0,161.2 L 320.6,160.8 L 327.2,160.4 L 333.8,160.1 L 340.4,159.7 L 347.0,159.3 L 353.6,159.0 L 360.2,158.6 L 366.8,158.2 L 373.4,157.9 L 380.0,157.5 L 386.6,157.1 L 393.2,156.8 L 399.8,156.4 L 406.4,156.0 L 413.0,155.7 L 419.6,155.3 L 426.2,154.9 L 432.8,154.6 L 439.4,154.2 L 446.0,153.8"/>
<path class="curve bad2 draw" pathLength="1" fill="none" d="M 50.0,175.8 L 56.6,173.0 L 63.2,170.2 L 69.8,167.4 L 76.4,164.6 L 83.0,161.8 L 89.6,158.9 L 96.2,156.1 L 102.8,153.3 L 109.4,150.5 L 116.0,147.6 L 122.6,144.8 L 129.2,142.0 L 135.8,139.2 L 142.4,136.3 L 149.0,133.5 L 155.6,130.7 L 162.2,127.9 L 168.8,125.0 L 175.4,122.2 L 182.0,119.4 L 188.6,116.6 L 195.2,113.7 L 201.8,110.9 L 208.4,108.1 L 215.0,105.3 L 221.6,102.4 L 228.2,99.6 L 234.8,96.8 L 241.4,94.0 L 248.0,91.1 L 254.6,88.3 L 261.2,85.5 L 267.8,82.7 L 274.4,79.8 L 281.0,77.0 L 287.6,74.2 L 294.2,71.4 L 300.8,68.5 L 307.4,65.7 L 314.0,62.9 L 320.6,60.1 L 327.2,57.2 L 333.8,54.4 L 340.4,51.6 L 347.0,48.7 L 353.6,45.9 L 360.2,43.1 L 366.8,40.3 L 373.4,37.4 L 380.0,34.6 L 386.6,31.8 L 393.2,29.0 L 399.8,26.1 L 406.4,23.3 L 413.0,20.5 L 419.6,17.7 L 426.2,14.8 L 432.8,12.0 L 439.4,9.2 L 446.0,6.4"/>
<text class="lbl bad reveal" x="340.4" y="43.6" text-anchor="middle">lr 0.13</text>
<text class="lbl bad reveal" x="419.6" y="170.3" text-anchor="end">lr 0.121</text>
<text class="lbl ok reveal" x="300.8" y="175.4" text-anchor="middle">lr 0.119</text>
<text class="lbl ok reveal" x="221.6" y="209.8" text-anchor="middle">lr 0.05</text>
</svg>
<figcaption>Sixty steps from the same start. The vertical axis is loss and one gridline is 100x. Between 0.119 and 0.121 the curve stops going down and starts going up.</figcaption>
</figure>

Something snaps between 0.119 and 0.121. That something is the **curvature** of
the loss.

For a quadratic loss the curvature is one matrix.

```python
H = 2 * np.array([[np.mean(x*x), np.mean(x)],
                  [np.mean(x),   1.0        ]])
print(H)                        # [[15.  5.] [ 5.  2.]]
print(np.linalg.eigvalsh(H))    # [ 0.2994 16.7006]
print(2 / 16.7006)              # 0.11976
```

Two eigenvalues. The larger, `16.70`, is the curvature of the steepest
direction; the smaller, `0.30`, the gentle one along the valley. On this surface
gradient descent converges under exactly one condition.

```
lr < 2 / largest eigenvalue = 2 / 16.7006 = 0.1198
```

That is why 0.119 survived and 0.121 exploded. Not a feel for it - a line, and
it holds to three decimal places.

Why `2/lambda` is clear if you isolate one direction. If the loss along it is
`lambda/2 * d^2`, the gradient is `lambda*d`, and one step leaves the distance
at `d(1 - lr*lambda)`. Shrinking needs `|1 - lr*lambda| < 1`, that is
`lr < 2/lambda`. Above that, every step lands further out on the other side.
Trace `lr=0.13` and that is exactly the shape: `(0, 0)` jumps to `(3.7, 1.24)`,
returns to `(-0.62, -0.26)`, then goes out to `(4.46, 1.44)`. The straight climb
of that curve in the figure is this ricochet.

## Why this is the same story at scale

With a hundred million parameters the Hessian cannot be written down - it would
need the square of that many entries. But a Hessian-vector product costs two
backward passes, and power iteration on top of it recovers the largest
eigenvalue. You cannot see all of it; you can see the one that sets stability.
The structure is unchanged.

- Stability is set by **one direction, the steepest**. However gentle the rest,
  if that one diverges everything goes with it
- Slowness comes from the other end, the **gentlest** direction. The learning
  rate has to respect the steepest, so the gentlest crawls at that rate
- The ratio of the eigenvalues, `16.7 / 0.30 = 56`, is this problem's condition
  number. The larger it is, the longer the ellipse and the more laborious
  gradient descent becomes

This is also where normalising the input becomes precise. It is often explained
as "shrink the inputs and you can raise the learning rate", which is half right.
Measured on this data:

```
x as is             eigenvalues [0.299, 16.70]   condition 55.8   lr ceiling 0.120
x times 0.1         eigenvalues [0.024,  2.13]   condition 90.4   lr ceiling 0.940
x minus its mean    eigenvalues [2.00,   2.50]   condition  1.2   lr ceiling 0.800
centred and scaled  eigenvalues [2.00,   2.00]   condition  1.0   lr ceiling 1.000
```

Shrinking alone lifts the ceiling eightfold and makes **the conditioning worse**
(55.8 to 90.4). The surface got longer, so whatever the higher ceiling buys is
handed straight back.

What actually works is **subtracting the mean**. Centring `x` sends `mean(x)` to
zero, which kills the off-diagonal term of the Hessian. The entanglement between
`w` and `b` comes apart and the condition number falls from 55.8 to 1.2.
Standardise as well and it is 1.0, a perfect circle. The value of normalising is
in squaring up the axes, not in the scale.

Momentum and Adam attack the same problem differently: they change the step
rather than the landscape. Momentum accumulates steps along directions that keep
their sign, so it travels further along the gentle axis; Adam divides each axis
by its recent gradient magnitude, evening out the imbalance between axes. Adam
does not remove the conditioning, though - it corrects per axis, so a landscape
tilted off the coordinate axes keeps its elongation.

## So

- A loss surface can be drawn, and with two parameters it really can be
- The learning-rate ceiling is `2 / lambda_max`, and the experiment agrees to
  three decimal places
- A good share of training that will not converge is not the algorithm but the
  **elongation of the surface**

The next part is the gradient itself. Above, `grad` was written by hand; with
layers stacked that stops being possible. It follows backpropagation through a
three-node graph by hand, then checks the result against numerical differences.
