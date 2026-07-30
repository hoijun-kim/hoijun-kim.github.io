---
title: "Why a noisier minibatch arrives sooner"
description: "Instead of one exact step over all the data, take many inexact ones over parts of it. Measured over a single pass through the data, which one gets further down."
date: 2025-07-30
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 5
---


Part two's gradient descent looked at all the data for every gradient. With four
data points that was fine. With a million, every step reads a million.

A minibatch compromises on the spot: look at part of it, approximate the
gradient, and step immediately. Being an approximation, the direction is wrong.
And yet it arrives sooner. Here is why, measured.

## The setup

Fitting a line to 2048 points. Putting the mean of `x` away from zero produces
the long, narrow contours of part two.

```python
import numpy as np
rng = np.random.default_rng(0)

n = 2048
x = rng.normal(2.0, 1.0, n)
y = 1.9 * x + 0.05 + 0.3 * rng.standard_normal(n)
X = np.stack([x, np.ones(n)], 1)          # two parameters, w and b

loss = lambda p: np.mean((X @ p - y) ** 2)
grad = lambda p, i: 2 * X[i].T @ (X[i] @ p - y[i]) / len(i)
```

The loss is quadratic, so its Hessian is constant. Taking its eigenvalues the
way part two did gives the shape of the problem and the learning-rate ceiling in
one move.

```
Hessian eigenvalues   0.3507 and 11.4379      condition number 32.6
learning-rate ceiling 2 / 11.4379 = 0.1749
minimum loss          0.0885                  (noise 0.3^2 = 0.09)
```

The noise was added at `0.3`, so no fit can push the loss much under `0.09`. The
actual minimum is `0.0885`. Keep that line in mind.

## How wrong is the approximation

Measure how far a batch gradient sits from the full gradient: the relative error
at the starting point, averaged over 20000 draws.

```
batch 8      relative error 0.2302
batch 32     relative error 0.1140
batch 256    relative error 0.0380
batch 2048   relative error 0.0000     (the whole set, so zero by definition)
```

Growing the batch shrinks the error as its square root. The exact law is
`sqrt((1/B)(n-B)/(n-1))`, and the familiar `1/sqrt(B)` is its approximation for
a batch much smaller than the whole. Here batch 256 is an eighth of everything,
so the difference shows.

```
ratio 8/32     measured 2.020   predicted 2.012
ratio 32/256   measured 2.997   predicted 3.000     1/sqrt(B) alone says 2.828
```

The second line is the point. The exact law calls `3.000` and the measurement is
`2.997`, while the `1/sqrt(B)` approximation calls `2.828`. Batch 2048's error
of zero is the same formula's endpoint - draw everything and `1/n - 1/n = 0`.

Up to here, a minibatch is simply a bad approximation.

## Over one pass through the data

What matters is **the unit of comparison**. Counted in steps, full batch wins,
because every step is exact. But steps do not cost the same. A full-batch step
reads 2048 points; a batch-32 step reads 32.

Compare them in the unit that costs the same: an **epoch**, one pass over the
data.

Full batch was given a learning rate of its own. Sweeping from `0.005` up to the
ceiling and keeping whichever gives the lowest loss at twelve epochs picks
`0.14462`, which is 83% of the ceiling. Handing it the `0.02` used for the small
batches would not be a fair comparison.

<figure class="fig">
<svg viewBox="0 0 460 276" role="img" aria-label="Loss per epoch. Batch 8 reaches the floor within a single epoch while full batch, even at its best learning rate, has not arrived by twelve">
<g class="axis">
<line x1="56" y1="206.3" x2="446" y2="206.3"/>
<text class="tick-lbl" x="47" y="209.8" text-anchor="end">1e-1</text>
<line x1="56" y1="130.5" x2="446" y2="130.5"/>
<text class="tick-lbl" x="47" y="134.0" text-anchor="end">1e0</text>
<line x1="56" y1="54.8" x2="446" y2="54.8"/>
<text class="tick-lbl" x="47" y="58.3" text-anchor="end">1e1</text>
<line class="frame" x1="56" y1="26" x2="56" y2="218"/><line class="frame" x1="56" y1="218" x2="446" y2="218"/>
<line class="frame" x1="56.0" y1="218" x2="56.0" y2="222"/>
<text class="tick-lbl" x="56.0" y="234" text-anchor="middle">1</text>
<line class="frame" x1="126.9" y1="218" x2="126.9" y2="222"/>
<text class="tick-lbl" x="126.9" y="234" text-anchor="middle">3</text>
<line class="frame" x1="233.3" y1="218" x2="233.3" y2="222"/>
<text class="tick-lbl" x="233.3" y="234" text-anchor="middle">6</text>
<line class="frame" x1="339.6" y1="218" x2="339.6" y2="222"/>
<text class="tick-lbl" x="339.6" y="234" text-anchor="middle">9</text>
<line class="frame" x1="446.0" y1="218" x2="446.0" y2="222"/>
<text class="tick-lbl" x="446.0" y="234" text-anchor="middle">12</text>
<text class="tick-lbl" x="251.0" y="270" text-anchor="middle">epoch</text>
<text class="tick-lbl" x="56" y="16" text-anchor="start">loss</text>
<line class="floor" x1="56" y1="210.3" x2="446" y2="210.3"/>
<text class="tick-lbl" x="62" y="224.3" text-anchor="start">minimum 0.0885</text></g>
<path class="curve bad" fill="none" d="M56.0,52.0 L91.5,68.7 L126.9,85.2 L162.4,101.3 L197.8,116.8 L233.3,131.5 L268.7,144.8 L304.2,156.5 L339.6,166.2 L375.1,173.7 L410.5,179.2 L446.0,183.0"/>
<path class="curve bad2" fill="none" d="M56.0,62.6 L91.5,89.7 L126.9,115.7 L162.4,139.8 L197.8,160.5 L233.3,176.3 L268.7,186.8 L304.2,193.1 L339.6,196.7 L375.1,198.9 L410.5,200.3 L446.0,201.4"/>
<path class="curve ok2" fill="none" d="M56.0,156.5 L91.5,189.3 L126.9,191.8 L162.4,193.3 L197.8,194.7 L233.3,196.1 L268.7,197.3 L304.2,198.5 L339.6,199.6 L375.1,200.6 L410.5,201.5 L446.0,202.3"/>
<path class="curve ok" fill="none" d="M56.0,197.9 L91.5,204.7 L126.9,207.9 L162.4,209.3 L197.8,209.5 L233.3,209.9 L268.7,210.1 L304.2,210.1 L339.6,210.3 L375.1,210.2 L410.5,210.2 L446.0,210.2"/>
<path class="curve ok3" fill="none" d="M56.0,209.2 L91.5,210.3 L126.9,210.3 L162.4,210.2 L197.8,209.8 L233.3,209.6 L268.7,209.8 L304.2,210.2 L339.6,210.3 L375.1,209.7 L410.5,210.3 L446.0,210.3"/>
<path class="curve bad" fill="none" d="M254.54545454545453,40 L276.5454545454545,40"/>
<text class="lbl bad" x="282.5454545454545" y="44" text-anchor="start">full batch lr 0.02</text>
<path class="curve bad2" fill="none" d="M254.54545454545453,55 L276.5454545454545,55"/>
<text class="lbl bad" x="282.5454545454545" y="59" text-anchor="start">full batch lr 0.14462</text>
<path class="curve ok2" fill="none" d="M254.54545454545453,70 L276.5454545454545,70"/>
<text class="lbl ok" x="282.5454545454545" y="74" text-anchor="start">batch 256</text>
<path class="curve ok" fill="none" d="M254.54545454545453,85 L276.5454545454545,85"/>
<text class="lbl ok" x="282.5454545454545" y="89" text-anchor="start">batch 32</text>
<path class="curve ok3" fill="none" d="M254.54545454545453,100 L276.5454545454545,100"/>
<text class="lbl ok" x="282.5454545454545" y="104" text-anchor="start">batch 8</text>
</svg>
<figcaption>An epoch is one pass over the data, so all five cases pay the same price for it. Batch 8 reaches the floor within one epoch and batch 32 takes three. Full batch, even handed its best learning rate, has not arrived by twelve.</figcaption>
</figure>

```
setting                 1 epoch   3 epochs   12 epochs   steps per epoch
full batch lr 0.02      10.8950     3.9688      0.2026                 1
full batch lr 0.14462    7.8806     1.5682      0.1159                 1
batch 256  lr 0.02       0.4545     0.1555      0.1128                 8
batch 32   lr 0.02       0.1288     0.0951      0.0887                64
batch 8    lr 0.02       0.0914     0.0886      0.0886               256
minimum                                         0.0885
```

**Batch 8 is at `0.0914` after a single epoch.** The minimum is `0.0885`, so it
has essentially arrived - within one pass over the data.

Full batch, even at its best learning rate, sits at `7.8806` after that same
epoch and at `0.1159` after all twelve. Twelve passes over the data do not take
it where batch 8 got in one.

Two hundred and fifty-six inaccurate steps beat one accurate step. The noise was
what bought the extra steps.

## Why the noise is not fatal

How the approximation is wrong matters. Draw the batch at random and the
gradient's **expectation equals the full gradient**. It is wrong, but not wrong
in a consistent direction. The direction wobbles from step to step while
pointing downhill on average.

And the errors cancel as steps accumulate. Being independent wobble rather than a
shared bias, sixty-four steps accumulate error not sixty-four-fold but roughly
`sqrt(64) = 8`-fold, while the progress accumulates in full.

## The price

Not free. That accounting holds **only on the way down**. Far from the minimum
the true gradient is large and signal beats noise; near it the signal shrinks
towards zero and the noise stays.

Run it long and that shows up as a number.

```
             12 epochs   300 epochs   gap to minimum at 300
batch 32        0.0887       0.0891                  0.0007
batch 8         0.0886       0.0904                  0.0019
```

**More training made it worse.** Batch 32 goes from `0.0887` to `0.0891`, batch
8 from `0.0886` to `0.0904`. Once it has arrived near the minimum only the
noise-driven wobble is left, and further steps just land somewhere on that
wobble.

And the smaller the batch, the higher that floor: at 300 epochs batch 8 is at
`0.0904` against batch 32's `0.0891`. Arriving sooner is paid for by orbiting
further out. This is why learning-rate schedules decay towards the end.

Two more costs remain.

- **A bigger batch means fewer steps.** Matching the result with a large batch
  means raising the learning rate, and part two's ceiling forbids it. The full
  batch rows above are that wall
- **Hardware moves the goalposts.** The comparison above prices an epoch by how
  many points get read, but on a GPU batch 256 does not take eight times as long
  as batch 32. While the device is idle, growing the batch barely lengthens a
  step, so the **cost per sample** falls. In practice that pushes batches above
  the theoretical optimum - until the device saturates and time starts scaling
  with the batch again

## So

- A minibatch gradient wobbles without bias. The direction is wrong, the average
  is right
- Its error follows `sqrt((1/B)(n-B)/(n-1))`. Measured `2.997` against a
  predicted `3.000`, where the `1/sqrt(B)` approximation would miss at `2.828`
- Compare in epochs rather than steps and many inaccurate steps beat one accurate
  one. Batch 8 hits `0.0914` in one epoch; full batch is still at `0.1159` after
  twelve
- The noise charges for it. Run to 300 epochs and batch 8 gets **worse**, to
  `0.0904`, and the smaller the batch the higher that floor sits
- Batch size is a dial trading accuracy against step count, not a number that
  should be as large as possible

Next time goes back to part four. All that care over initialisation turns out to
be removable by adding one line per layer - measuring how normalisation erases
the initialisation.
