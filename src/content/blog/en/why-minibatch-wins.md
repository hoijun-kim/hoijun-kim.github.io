---
title: "Why a noisier minibatch arrives sooner"
description: "Instead of one exact step from the whole dataset, take sixty-four inexact ones from thirty-two samples each. Measured over one pass through the data, which gets further down?"
date: 2026-07-30
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 5
---

Part two computed the gradient from the whole dataset. There were four points,
so that was fine. With a million, every step reads a million.

A minibatch compromises on the spot: look at 32, estimate the gradient, step.
The estimate is wrong, so the direction is wrong. And it arrives sooner. Here is
the measurement of why.

## How wrong is the estimate

Start with the size of the noise: how far a batch gradient falls from the full
one, averaged over 200 draws.

```python
g_full = grad(w, np.arange(n))
err = np.linalg.norm(grad(w, idx) - g_full) / np.linalg.norm(g_full)
```

```
batch 8     relative error 1.539
batch 32    relative error 0.806
batch 256   relative error 0.271
batch 2048  relative error 0     (the whole set, so zero by definition)
```

Batch 8 may as well be pointing the wrong way: a relative error of 1.5 means the
error is larger than the gradient. Growing the batch shrinks the error like its
square root.

The exact law is `sqrt(1/batch - 1/n)`. The familiar `1/sqrt(batch)` is its
approximation for a batch much smaller than the whole set `n`. Here batch 256 is
an eighth of the data, so the difference shows: the predicted ratios are `2.01`
and `3.00` against measured `1.539/0.806 = 1.91` and `0.806/0.271 = 2.97`. Under
`1/sqrt(batch)` alone the second would have to be `2.83`, and it is not. The
zero at batch 2048 is the same formula's endpoint - draw everything and
`1/n - 1/n = 0`.

## Over one pass through the data

What matters is **the unit of comparison**. Per step, the full batch wins, since
each of its steps is exact. But a step does not cost the same on both sides: the
full batch reads 2048 samples per step, batch 32 reads 32.

Compare over the unit that costs the same on both sides, one pass over the data
- an **epoch**. Steps per epoch: 1 for the full batch, 8 for batch 256, 64 for
batch 32.

The full batch was also given a learning rate of its own. Following part two, the
Hessian's largest eigenvalue gives a ceiling of `0.844`, and 90% of that is
`0.76`. Handing it the `0.02` used for the small batches would not be a fair
comparison.

<figure class="fig">
<svg viewBox="0 0 460 258" role="img" aria-label="Loss per epoch. Batch 32 reaches the minimum by the third epoch; the full batch takes twelve even with its learning rate at the ceiling">
<g class="axis">
<line x1="50" y1="209.9" x2="446" y2="209.9"/>
<text class="tick-lbl" x="41" y="213.4" text-anchor="end">1e-1</text>
<line x1="50" y1="139.1" x2="446" y2="139.1"/>
<text class="tick-lbl" x="41" y="142.6" text-anchor="end">1e0</text>
<line x1="50" y1="68.4" x2="446" y2="68.4"/>
<text class="tick-lbl" x="41" y="71.9" text-anchor="end">1e1</text>
<line class="frame" x1="50" y1="26" x2="50" y2="224"/><line class="frame" x1="50" y1="224" x2="446" y2="224"/>
<line class="frame" x1="50.0" y1="224" x2="50.0" y2="228"/><text class="tick-lbl" x="50.0" y="240" text-anchor="middle">0</text>
<line class="frame" x1="149.0" y1="224" x2="149.0" y2="228"/><text class="tick-lbl" x="149.0" y="240" text-anchor="middle">3</text>
<line class="frame" x1="248.0" y1="224" x2="248.0" y2="228"/><text class="tick-lbl" x="248.0" y="240" text-anchor="middle">6</text>
<line class="frame" x1="347.0" y1="224" x2="347.0" y2="228"/><text class="tick-lbl" x="347.0" y="240" text-anchor="middle">9</text>
<line class="frame" x1="446.0" y1="224" x2="446.0" y2="228"/><text class="tick-lbl" x="446.0" y="240" text-anchor="middle">12</text>
<text class="tick-lbl" x="248" y="254" text-anchor="middle">epoch</text>
<text class="tick-lbl" x="50" y="16" text-anchor="start">loss</text>
<line class="floor" x1="50" y1="213.6" x2="446" y2="213.6"/>
<text class="tick-lbl" x="58.2" y="207.6" text-anchor="start">minimum 0.0885</text>
</g>
<path class="curve bad2" fill="none" d="M 50.0,45.4 L 83.0,47.8 L 116.0,50.3 L 149.0,52.7 L 182.0,55.2 L 215.0,57.6 L 248.0,60.1 L 281.0,62.5 L 314.0,64.9 L 347.0,67.4 L 380.0,69.8 L 413.0,72.2 L 446.0,74.7"/>
<path class="curve bad" fill="none" d="M 50.0,45.4 L 83.0,85.9 L 116.0,117.1 L 149.0,141.0 L 182.0,159.9 L 215.0,175.0 L 248.0,186.9 L 281.0,195.9 L 314.0,202.3 L 347.0,206.5 L 380.0,209.3 L 413.0,211.0 L 446.0,212.0"/>
<path class="curve ok2" fill="none" d="M 50.0,45.4 L 83.0,65.0 L 116.0,84.4 L 149.0,103.5 L 182.0,122.1 L 215.0,140.1 L 248.0,157.0 L 281.0,172.1 L 314.0,185.0 L 347.0,195.1 L 380.0,202.3 L 413.0,206.9 L 446.0,209.8"/>
<path class="curve ok" fill="none" d="M 50.0,45.4 L 83.0,185.5 L 116.0,213.2 L 149.0,213.5 L 182.0,213.5 L 215.0,213.5 L 248.0,213.5 L 281.0,213.5 L 314.0,213.5 L 347.0,213.5 L 380.0,213.5 L 413.0,213.5 L 446.0,213.5"/>
<text class="lbl bad" x="413.0" y="63.2" text-anchor="end">full batch, lr 0.02</text>
<text class="lbl bad" x="248.0" y="203.9" text-anchor="middle">full batch, lr 0.76</text>
<text class="lbl ok" x="201.8" y="233.5" text-anchor="middle">batch 32</text>
</svg>
<figcaption>An epoch is one pass over the data, so it costs the same in all four cases. Batch 32 meets the minimum line at the third epoch; the full batch has not arrived by the twelfth, even at its ceiling learning rate.</figcaption>
</figure>

```
                       1 epoch    3 epochs   12 epochs   steps/epoch
full batch, lr 0.02    19.5502    16.6655     8.1644          1
full batch, lr 0.76     5.6670     0.9408     0.0931          1
batch 256,  lr 0.02    11.1921     3.1969     0.1002          8
batch 32,   lr 0.02     0.2211     0.0889     0.0887         64
minimum                                       0.0885
```

Batch 32 **reaches the minimum in three epochs**. The full batch, even with its
learning rate at the ceiling, takes twelve to get to 0.0931. In the time it
takes to read the data three times, one is finished and the other is still ten
times above.

Sixty-four inexact steps beat one exact step. The noise was what bought the
step count.

## Why the noise is not fatal

How the estimate is wrong matters. Draw the batch at random and the **expected
value of its gradient equals the full gradient**. It is wrong, but not
systematically wrong in one direction. The direction shakes step to step while
still pointing downhill on average.

The errors also cancel as steps accumulate. They are independent wobbles rather
than a shared bias, so the accumulated error over sixty-four steps grows not
sixty-fourfold but about `sqrt(64) = 8`. The forward progress accumulates in
full.

That accounting holds **while descending**. Far from the minimum the true
gradient is large and the signal beats the noise; approaching it, the signal
shrinks towards zero while the noise does not. From there, more steps buy
nothing. Running the experiment above to 300 epochs, the distance to the minimum
never improves on the `0.021` it had at epoch 3. Which is exactly the next
section.

## The price

Not free.

- **It does not stop at the minimum.** In the table batch 32 sits at `0.0887`
  against a minimum of `0.0885`, and more steps only rattle around there. The
  smaller the batch the higher that floor: batch 8 is still at `0.0917` after 12
  epochs. This is why learning-rate schedules decay towards the end
- **A larger batch buys fewer steps.** Matching the result with a bigger batch
  means raising the learning rate, and part two's ceiling stops that
- **Hardware moves the goalposts.** The comparison above priced a step by the
  samples it reads, but on a GPU batch 256 does not take eight times as long as
  batch 32. While the device is idle, growing the batch barely lengthens the
  step, so the **per-sample cost** falls. That is why practice runs larger
  batches than the theory suggests - until the device saturates and time starts
  scaling with the batch again

## So

- A minibatch gradient wobbles without bias. Wrong direction, right average
- Compare by epoch rather than by step and many inexact steps beat one exact
  one: three epochs against twelve, on this data
- The noise leaves a floor near the minimum, which is where learning-rate
  schedules come from
- Batch size is a dial trading accuracy against step count, not a number that
  should be as large as possible

Five parts in. Where a tensor sits, how big a step is, how the derivative flows,
what stacking layers does to that product, and what splitting the data costs.
Every one measured and drawn once.
