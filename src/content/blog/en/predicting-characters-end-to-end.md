---
title: "Predicting characters with 637,156 parameters"
description: "Twelve parts of pieces, wired together and actually run. Why the loss starts at ln(vocabulary), what happens when the causal mask comes off, and what one head turned out to have learned."
date: 2026-08-25
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 13
---

The pieces are all in hand. Now they get wired together and run. The goal is not
performance but **measurement**.

The corpus is the thirteen English posts on this blog. Strip the figure SVGs and
that is `75,353` characters over a vocabulary of `100`. Split 90/10, `67,817`
characters to train on and `7,536` to validate against. The model is Pre-LN as
part twelve concluded, three blocks, `d=128`, four heads, 128 characters of
context, `637,156` parameters.

## First, put a scale on the loss

Before looking at a number it has to be clear what the number means. The loss is
cross entropy, and **a model that knows nothing guesses uniformly**. With a
vocabulary of `100` that puts the loss at `ln(100) = 4.6052`.

The check is exact. Zero the final layer's weight and bias and every logit is
equal, so the prediction is perfectly uniform.

```
head zeroed:  loss 4.605171     ln(100) = 4.605170
```

A difference of `5.4e-07`. At real initialisation it reads `4.7140`, slightly
higher, which is the amount a random head's logit spread pushes the prediction
off uniform.

That fixes the ceiling; the floor needs one too. **Bigrams**: count what
character follows what, using nothing but the previous character. Counted on the
training split and measured on validation, that is `2.6501`. A transformer that
cannot beat this line has no reason to exist.

```
uniform guess   4.6052   perplexity 100
bigram          2.6501   perplexity  14.2
```

Perplexity is `exp(loss)`, and reads as **how many ways the model is torn**.
Uniform is a hundred ways, bigrams 14.2.

## Run it

<figure class="fig">
<svg viewBox="0 0 460 268" role="img" aria-label="Training and validation loss of the character language model. Validation bottoms at 1.751 by step 3000 and turns while training keeps falling">
<g class="axis">
<line x1="54" y1="194.7" x2="446" y2="194.7"/>
<text class="tick-lbl" x="45" y="198.2" text-anchor="end">1</text>
<line x1="54" y1="151.4" x2="446" y2="151.4"/>
<text class="tick-lbl" x="45" y="154.9" text-anchor="end">2</text>
<line x1="54" y1="108.2" x2="446" y2="108.2"/>
<text class="tick-lbl" x="45" y="111.7" text-anchor="end">3</text>
<line x1="54" y1="64.9" x2="446" y2="64.9"/>
<text class="tick-lbl" x="45" y="68.4" text-anchor="end">4</text>
<line class="frame" x1="54" y1="26" x2="54" y2="212"/><line class="frame" x1="54" y1="212" x2="446" y2="212"/>
<line class="frame" x1="54.0" y1="212" x2="54.0" y2="216"/>
<text class="tick-lbl" x="54.0" y="228" text-anchor="middle">0</text>
<line class="frame" x1="132.3" y1="212" x2="132.3" y2="216"/>
<text class="tick-lbl" x="132.3" y="228" text-anchor="middle">1000</text>
<line class="frame" x1="210.8" y1="212" x2="210.8" y2="216"/>
<text class="tick-lbl" x="210.8" y="228" text-anchor="middle">2000</text>
<line class="frame" x1="289.2" y1="212" x2="289.2" y2="216"/>
<text class="tick-lbl" x="289.2" y="228" text-anchor="middle">3000</text>
<line class="frame" x1="367.6" y1="212" x2="367.6" y2="216"/>
<text class="tick-lbl" x="367.6" y="228" text-anchor="middle">4000</text>
<line class="frame" x1="446.0" y1="212" x2="446.0" y2="216"/>
<text class="tick-lbl" x="446.0" y="228" text-anchor="middle">5000</text>
<text class="tick-lbl" x="250.0" y="262" text-anchor="middle">step</text>
<text class="tick-lbl" x="54" y="16" text-anchor="start">loss</text>
<line class="floor" x1="54" y1="38.8" x2="446" y2="38.8"/>
<text class="tick-lbl" x="442" y="32.8" text-anchor="end">uniform ln(100)=4.61</text>
<line class="floor" x1="54" y1="123.3" x2="446" y2="123.3"/>
<text class="tick-lbl" x="442" y="117.3" text-anchor="end">bigram 2.65</text></g>
<path class="curve bad2" fill="none" d="M54.0,40.8 L69.6,123.9 L85.3,128.9 L101.0,133.0 L116.7,139.5 L132.3,147.0 L148.0,153.5 L163.7,159.5 L179.4,163.6 L195.1,168.1 L210.8,171.5 L226.4,174.5 L242.1,177.2 L257.8,179.8 L273.5,182.0 L289.2,184.2 L304.9,185.9 L320.5,188.1 L336.2,190.1 L351.9,191.7 L367.6,193.6 L383.3,195.3 L399.0,197.1 L414.6,198.7 L430.3,200.5 L446.0,201.9"/>
<path class="curve ok" fill="none" d="M54.0,40.8 L69.6,123.4 L85.3,127.7 L101.0,130.8 L116.7,135.9 L132.3,142.8 L148.0,148.4 L163.7,152.8 L179.4,155.3 L195.1,157.8 L210.8,159.1 L226.4,160.3 L242.1,161.2 L257.8,161.7 L273.5,161.7 L289.2,162.2 L304.9,161.4 L320.5,161.4 L336.2,160.9 L351.9,159.3 L367.6,158.8 L383.3,157.5 L399.0,155.6 L414.6,153.6 L430.3,152.5 L446.0,150.3"/>
<circle class="mark" cx="289.2" cy="162.2" r="3.2"/>
<text class="lbl ok" x="289.2" y="151.2" text-anchor="middle">lowest 1.751 (step 3000)</text>
<text class="lbl bad" x="391.1" y="186.5" text-anchor="middle">train</text>
<text class="lbl ok" x="406.8" y="140.3" text-anchor="middle">validation</text>
</svg>
<figcaption>Training and validation loss for the character model. The two horizontal lines are uniform prediction (4.61) and counting bigrams (2.65). Two hundred steps catch the bigram, validation bottoms at 1.751 by step 3000 and then turns, and training loss keeps falling to the end.</figcaption>
</figure>

```
step      train       val
   1     4.5573    4.5573
 200     2.6367    2.6474      <- catches the bigram
1000     2.1031    2.2001
3000     1.2432    1.7510      <- validation minimum
5000     0.8344    2.0272
```

Two hundred steps catch the bigram. That is what learning to count the previous
character costs.

The minimum is `1.7510` at step `3000`, a perplexity of `5.8`. Down from the
bigram's `14.2`, so looking further back genuinely pays.

And part seven repeats itself exactly. Past `3000` steps **the training loss
keeps falling while validation rises**: `0.8344` against `2.0272` at the end.
Watch the training curve and it is improving; in reality it is getting worse.
With only sixty thousand characters of corpus, 637k parameters are plenty to
memorise it.

## What it learned

Samples from the same model at several points, first lines only.

```
step 0      ]TUoF%힣`Y)oYgEk1 fb3cqieQZqsV6{O²h`|F#a {_m:O.5Σ-VE·.

step 200    `1   (힣,  o 1Ee1  b3      as   Oghe        0.
            0he.0.     9     -19alongis.    ug    s

step 1000   `` ovan`, ong vo abe tientas to
            fre is steme- rivaresimere. Sonsing isactinalongis.

step 5000   `16, a=0, 36, 112003  0.3009849
            ```
            The smallest `1.000h`. **`shape(2*x) = 0
            `dL/{w_h` andeds share number `sqrt(d) = sum(0)`
```

Spaces appear by step 200, English-shaped words by 1000, and by 5000 it is
producing **markdown** - backticks, code fences, `**` emphasis, `sqrt(d)`,
things resembling `dL/dw`.

Honestly, that is not English learned but **the surface of this corpus** learned.
The corpus is technical markdown, so the shell of it comes first. A number like
`0.272` is a value actually used in part twelve, and is closer to memorised than
predicted.

## Take off the causal mask

Attention looks everywhere by default. In next-character prediction, **the next
character is already in the input**: the answer at position `t` is the input at
position `t+1`. Hence the triangular mask that forbids looking ahead.

Run it without.

```
step     train      val
 300    2.5317   2.5530
 600    0.3393   0.3348
 900    0.0473   0.0506
1200    0.0306   0.0331
```

A loss of `0.03`. Far under the bigram's `2.65`, and far under the `1.75` of the
model that trained properly. Validation falls right alongside it, so there is no
overfitting signal either. Even part seven's "judge by validation" fails here.

Of course it does. Nothing was learned; **the answer was read off the side**.
Confirming it takes one line - measure the same model with the mask switched on.

```
train loss measured with the mask on:   5.9703
```

Worse than the `4.6052` of a model that never trained. That is what makes this
failure frightening: the loss curve descends beautifully, validation follows it
down, and the real performance is **below guessing**.

## Take one head out and look

Part ten said heads have **room** to look at different things but are not forced
to. Measure it in this trained model - the average weight each head gives at
each relative distance.

```
block head    d=0     d=1     d=2     d=3     d=4
  0    0    0.017   0.020   0.016   0.016   0.015
  0    1    0.016   0.017   0.018   0.017   0.016
  0    2    0.005   0.879   0.005   0.004   0.005
  0    3    0.019   0.030   0.017   0.017   0.017
```

**Block 0, head 2 gives `0.879` to the immediately preceding character.** To
itself `0.005`, and about `0.005` everywhere else. A nearly pure
previous-character head, arrived at by training.

The other three heads in that block sit between `0.015` and `0.030` at every
distance. Spread evenly across a full context that would be about `0.010`, so
they are effectively **looking nowhere**. Part ten's "the structure only makes
room" splits like that inside a single block.

In blocks 1 and 2, eleven of the twelve heads peak at distance 1, but broadly,
between `0.20` and `0.34`. Only block 0's head 2 is sharp.

## So

- The loss has two scales. The ceiling is `ln(vocabulary)`, here `4.6052`,
  reproduced to within `5.4e-07` by zeroing the head. The floor is the bigram's
  `2.6501`
- Two hundred steps catch the bigram; step 3000 bottoms out at `1.7510`. In
  perplexity, `14.2` down to `5.8`
- After that it is part seven again. Training falls to `0.8344` while validation
  climbs to `2.0272`
- Without the causal mask the loss reaches `0.03`, and the same model measured
  with the mask on gives `5.9703` - worse than before training. **A pretty curve
  is not evidence of learning**
- Heads can specialise without being forced to. Block 0 head 2 puts `0.879` on
  the previous character while the other three in its block idle near uniform

Thirteen parts, one lap. From where a tensor sits, through steps, derivatives,
layers, batches, normalisation, generalisation, attention, position, heads,
feed-forward and stacking, to running all of it at once. Measured and drawn each
time, and re-measured the several times the first measurement turned out wrong.
