---
title: "Pooling throws away three bits of position"
description: "What pooling buys and what it spends, measured separately. At window 8 a one-character shift moves the representation 0.22 instead of 1.16 - and the price is 3.00 bits saying which position inside the window won. For next-character prediction that trade loses."
date: 2025-12-19
lang: en
kind: guide
series:
  id: not-attention
  part: 6
---

Pooling is a part borrowed from images. A cat three pixels to the left is still a
cat, so it is used to build representations that do not wobble under small shifts.

For predicting the next character, position is the entire question. So what
pooling does here has to be measured on its own.

## What pooling computes

Take the largest value inside a window of `w` (max pooling) or their average
(mean pooling). It has no weights, so it costs no parameters.

With stride `w` the sequence shortens by a factor of `w`; with stride `1` the
length is unchanged. Either way, padding only on the left keeps it causal.

## What it buys: less movement under a shift

Take the first convolutional layer's output from part four, shift the text by one
character, recompute, and compare the downsampled representations.

<figure class="fig">
<svg viewBox="0 0 460 356" role="img" aria-label="Above: how much the downsampled representation changes when the text shifts by one character. Plain subsampling changes completely at 1.16; max pooling falls to 0.22 as the window grows. Below: what that costs, with pooling itself nine times the cost of the wider reach it brings">
<text class="ttl2 l" x="18.0" y="18">how much the representation moves under a one-character shift</text>
<g class="axis">
<line x1="76.0" y1="132.0" x2="240.0" y2="132.0"/>
<text class="tick-lbl" x="70.0" y="135.5" text-anchor="end">0</text>
<line x1="76.0" y1="96.6" x2="240.0" y2="96.6"/>
<text class="tick-lbl" x="70.0" y="100.1" text-anchor="end">0.5</text>
<line x1="76.0" y1="61.2" x2="240.0" y2="61.2"/>
<text class="tick-lbl" x="70.0" y="64.7" text-anchor="end">1</text>
</g>
<path class="curve bad" d="M76.0,49.3 L158.0,49.5 L240.0,49.9" fill="none"/>
<circle class="dot bad" cx="76.0" cy="49.3" r="2.8"/>
<circle class="dot bad" cx="158.0" cy="49.5" r="2.8"/>
<circle class="dot bad" cx="240.0" cy="49.9" r="2.8"/>
<text class="lbl bad" x="78.0" y="40.3" text-anchor="start">subsample, no pooling</text>
<path class="curve ok" d="M76.0,80.3 L158.0,103.5 L240.0,116.4" fill="none"/>
<circle class="dot" cx="76.0" cy="80.3" r="2.8"/>
<circle class="dot" cx="158.0" cy="103.5" r="2.8"/>
<circle class="dot" cx="240.0" cy="116.4" r="2.8"/>
<text class="lbl ok" x="240.0" y="131.4" text-anchor="end">max pool</text>
<g class="lbl-ax">
<text x="76.0" y="147">2</text>
<text x="158.0" y="147">4</text>
<text x="240.0" y="147">8</text>
<text class="cap l" x="76.0" y="162">pooling window</text></g>
<text class="cap l" x="296.0" y="86">position bits discarded</text>
<text class="lbl bad" x="296.0" y="102">w=2 : 0.95 bit</text>
<text class="lbl bad" x="296.0" y="116">w=4 : 1.99 bit</text>
<text class="lbl bad" x="296.0" y="130">w=8 : 3.00 bit</text>
<text class="ttl2 l" x="10.0" y="184">best validation loss</text>
<g class="split">
<text class="lbl r" x="142.0" y="211.0" text-anchor="end">no pooling</text>
<rect class="dec" x="150.0" y="200.0" width="35.9" height="14"/>
<text class="lbl" x="191.9" y="211.0">1.8709</text>
<text class="lbl r" x="142.0" y="233.0" text-anchor="end">max pool 2</text>
<rect class="dec" x="150.0" y="222.0" width="107.6" height="14"/>
<text class="lbl" x="263.6" y="233.0">1.9726</text>
<text class="lbl r" x="142.0" y="255.0" text-anchor="end">control, same reach 29</text>
<rect class="dec" x="150.0" y="244.0" width="55.5" height="14"/>
<text class="lbl" x="211.5" y="255.0">1.8987</text>
<text class="lbl r" x="142.0" y="277.0" text-anchor="end">max pool 4</text>
<rect class="dec" x="150.0" y="266.0" width="226.3" height="14"/>
<text class="lbl" x="382.3" y="277.0">2.1409</text>
<text class="lbl r" x="142.0" y="299.0" text-anchor="end">mean pool 4</text>
<rect class="dec" x="150.0" y="288.0" width="229.8" height="14"/>
<text class="lbl" x="385.8" y="299.0">2.1458</text>
</g>
<g class="done"><line x1="185.9" y1="196.0" x2="185.9" y2="312.0"/><line x1="205.5" y1="240.0" x2="205.5" y2="312.0"/></g>
<text class="lbl" x="150.0" y="324.0">from the wider reach +0.0278</text>
<text class="lbl ok" x="150.0" y="339.0">from pooling +0.2422</text>
</svg>
<figcaption>Above: how much the downsampled representation changes when the text shifts by one character. Plain subsampling becomes effectively a different thing at 1.16, while max pooling falls to 0.22 as the window grows - that is the invariance being bought. To the right, the position information being spent on it. Below: validation loss at the same 171 channels and 639,273 parameters. Between the dotted rules is what the wider reach cost; to the right of them is what pooling itself cost.</figcaption>
</figure>

```
window            2       4       8
max pool      0.730   0.403   0.220
mean pool     0.720   0.410   0.231
plain sample  1.168   1.166   1.160
```

Taking one value every `w` without pooling gives `1.16` under a single-character
shift. A relative norm above one means it is effectively uncorrelated with what it
was.

Max pooling brings that to `0.730`, `0.403`, `0.220`. **The wider the window, the
less it wobbles.** That is what pooling buys, and why images use it.

## What it spends: log2(w) bits of position

The price is which place inside the window it was. A max-pooled output is one
value, so **which position won does not survive.**

How much is being discarded is countable. The distribution of the winning offset:

```
window   winning offset                       entropy / max
     2   0.632  0.368                          0.95 / 1.00
     4   0.301  0.231  0.236  0.232            1.99 / 2.00
     8   every offset 0.120 ~ 0.129            3.00 / 3.00
```

All but perfectly uniform. At window 8 the entropy is `3.00` bits, equal to the
maximum to two decimal places. **The three bits being thrown away are three bits
recoverable from nowhere else.** Had there been any regularity in which offset
wins, the entropy would have come in under three.

## On this task

Whether the trade pays is a training question. Insert stride-1 pooling after each
layer of part four's convolution - stride 1, so the length is unchanged and no
parameters are added - and hold everything else fixed.

```
                        reach  channels  parameters   best val (3 seeds)      median
no pooling                 17       171     639,273   1.8748 1.8709 1.8695  1.8709
max pool 2                 21       171     639,273   2.0047 1.9726 1.9628  1.9726
max pool 4                 29       171     639,273   2.1446 2.1409 2.1060  2.1409
mean pool 4                29       171     639,273   2.1518 2.1458 2.1342  2.1458
control, same reach 29     29       171     639,273   1.8987 1.9033 1.8922  1.8987
```

Identical channels and identical parameters across all five. Max pooling at 4
takes `1.8709` to `2.1409`, worse by `0.27`.

## Not because the reach widened

Stride-1 pooling still widens the receptive field: a window of `w` across four
layers adds `4(w-1)`, so max pool 4 reaches `29` rather than `17`. Part five found
wider to be worse, so some of that `0.27` is the widening.

Hence the control: reach pinned to `29` by dilation alone with no pooling, again
at the same channels and parameters.

```
no pooling (reach 17)          1.8709
control (reach 29, no pool)    1.8987     from the wider reach  +0.0278
max pool 4 (reach 29)          2.1409     from pooling itself   +0.2422
```

**Pooling itself costs `8.7` times what the widening did.** The confound is small.

## Max and mean are indistinguishable

`2.1409` against `2.1458`, with seed ranges of `2.1060~2.1446` and
`2.1342~2.1518` that overlap. It is not which one you pick but **that you pick at
all** that costs.

Which follows. Both collapse `w` values into one, and whether the rule is a
maximum or an average, the position goes the same way.

## What is left

Pooling went in after every layer here. Only at the last, or every other layer,
would cost less - unmeasured.

Stride-`w` downsampling was not trained either. Shortening the sequence means
building something to lengthen it again for a per-position prediction, and that
makes it a different comparison.

And this conclusion belongs to a task **where position is the answer.**
Classifying a whole passage - is this code or prose - would likely be helped by
throwing position away. That task was not built.

## So

- Pooling collapses a window into one value. No weights, no parameters
- What it buys is invariance: a one-character shift moves the representation
  `1.16` without it and `0.22` with max pooling at window 8
- What it spends is position: the winning offset's entropy at window 8 is `3.00`
  bits, equal to the maximum - three bits recoverable from nowhere else
- On this task it loses, `1.8709` to `2.1409`, worse by `0.27`
- Only `+0.0278` of that is the wider reach; `+0.2422` is pooling itself. `8.7`
  times
- Max and mean are indistinguishable. The collapsing is the cost, not the rule
