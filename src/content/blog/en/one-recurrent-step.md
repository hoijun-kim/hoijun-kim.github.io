---
title: "What one recurrent step computes"
description: "Opening up what it means to read text with a single hidden state. 73% of the 637k parameters sit in the one matrix that carries state to state, unit 546 of 683 switches on at every space, and changing one character leaves half its trace gone four characters later."
date: 2025-11-19
lang: en
kind: guide
series:
  id: not-attention
  part: 1
---

The first series began at tensors and worked through learning rates, backprop,
vanishing gradients, minibatches, normalisation and generalisation, and then went
straight to attention in part eight. The space in between is empty. There were
ways of handling order before attention, and without opening them up there is no
saying what attention actually changed.

Start with the simplest one: the recurrent network.

## What one step computes

Read the text left to right one character at a time, carrying everything read so
far in **a single vector**. That vector is the hidden state. Reading one
character is entirely this:

```python
h = torch.zeros(683)                 # knowing nothing yet
for t in range(128):
    x = tok[idx[t]]                  # this character's embedding, (128,)
    h = torch.tanh(W_ih @ x + b_ih + W_hh @ h + b_hh)
```

Transform the new character once, transform the state you were carrying once, add
them, squash with `tanh`. That is a step. Reading 128 characters runs that line
128 times.

One thing there is strange: neither `W_ih` nor `W_hh` carries a `t`. **The same
matrix is used all 128 times.** A twenty-layer network has different weights at
every layer; recurrence goes through the same ones 128 times over. That is why
the vanishing gradient part four measured against depth happens against length
here, and part eight comes back to it.

## 73% of the parameters are in one matrix

At width 683, the 637k splits like this:

```
tok.weight        (100, 128)     12,800   character -> embedding
rec.weight_ih_l0  (683, 128)     87,424   embedding -> state
rec.weight_hh_l0  (683, 683)    466,489   state -> state
four biases        (683) x 4      2,732
head.weight       (100, 683)     68,300   state -> next character
head.bias         (100)             100
                                637,845
```

`W_hh` alone is `466,489`, or `73.1%` of everything. A recurrent network spends
almost all of its parameters **moving state to state**. Taking the input in costs
`87,424`, less than a fifth of that.

Double the width and `W_hh` quadruples. That is why widening a recurrent model is
expensive.

## Pulling out one unit

The hidden state is a bundle of 683 numbers. Take one of them, follow it across
characters, and sometimes something readable comes out.

Training an RNN for 800 steps under the same protocol part seven uses, and
correlating each unit's activation with a few properties:

```
                      unit   correlation
is a space             546        +0.675
inside backticks       292        +0.226
characters since \n     594        -0.174
is uppercase           459        +0.169
```

`546` stands out. Running it over a real sentence and plotting only that unit:

<figure class="fig">
<svg viewBox="0 0 460 300" role="img" aria-label="Above: one hidden unit's value across characters. It rises near 1 on every space and drops on letters. Below: after one character is changed, the difference in hidden state halves within four characters and is near zero by thirty">
<text class="ttl2 l" x="18.0" y="16">what one hidden unit, number 546, does character by character</text>
<g class="axis">
<line x1="34.0" y1="108.0" x2="446.0" y2="108.0"/>
<text class="tick-lbl" x="30.0" y="111.5" text-anchor="end">-1</text>
<line x1="34.0" y1="69.0" x2="446.0" y2="69.0"/>
<text class="tick-lbl" x="30.0" y="72.5" text-anchor="end">+0</text>
<line x1="34.0" y1="30.0" x2="446.0" y2="30.0"/>
<text class="tick-lbl" x="30.0" y="33.5" text-anchor="end">+1</text>
</g>
<g class="guide">
<line x1="92.1" y1="26.0" x2="92.1" y2="124.0"/>
<line x1="112.9" y1="26.0" x2="112.9" y2="124.0"/>
<line x1="154.5" y1="26.0" x2="154.5" y2="124.0"/>
<line x1="196.2" y1="26.0" x2="196.2" y2="124.0"/>
<line x1="258.6" y1="26.0" x2="258.6" y2="124.0"/>
<line x1="300.3" y1="26.0" x2="300.3" y2="124.0"/>
<line x1="373.1" y1="26.0" x2="373.1" y2="124.0"/>
</g>
<path class="curve ok" d="M40.0,65.7 L50.4,49.8 L60.8,67.6 L71.2,92.7 L81.6,63.8 L92.1,33.4 L102.5,51.0 L112.9,32.5 L123.3,49.8 L133.7,77.4 L144.1,59.3 L154.5,32.2 L164.9,77.0 L175.3,72.6 L185.7,81.6 L196.2,30.7 L206.6,76.3 L217.0,57.4 L227.4,80.4 L237.8,65.9 L248.2,98.4 L258.6,32.4 L269.0,81.4 L279.4,92.7 L289.8,84.4 L300.3,32.4 L310.7,52.9 L321.1,81.7 L331.5,83.9 L341.9,73.0 L352.3,97.6 L362.7,93.0 L373.1,33.7 L383.5,49.9 L393.9,66.6 L404.4,61.5 L414.8,53.7 L425.2,84.4 L435.6,75.7 L446.0,74.3" fill="none"/>
<circle class="dot" cx="40.0" cy="65.7" r="1.7"/>
<circle class="dot" cx="50.4" cy="49.8" r="1.7"/>
<circle class="dot" cx="60.8" cy="67.6" r="1.7"/>
<circle class="dot" cx="71.2" cy="92.7" r="1.7"/>
<circle class="dot" cx="81.6" cy="63.8" r="1.7"/>
<circle class="dot" cx="92.1" cy="33.4" r="1.7"/>
<circle class="dot" cx="102.5" cy="51.0" r="1.7"/>
<circle class="dot" cx="112.9" cy="32.5" r="1.7"/>
<circle class="dot" cx="123.3" cy="49.8" r="1.7"/>
<circle class="dot" cx="133.7" cy="77.4" r="1.7"/>
<circle class="dot" cx="144.1" cy="59.3" r="1.7"/>
<circle class="dot" cx="154.5" cy="32.2" r="1.7"/>
<circle class="dot" cx="164.9" cy="77.0" r="1.7"/>
<circle class="dot" cx="175.3" cy="72.6" r="1.7"/>
<circle class="dot" cx="185.7" cy="81.6" r="1.7"/>
<circle class="dot" cx="196.2" cy="30.7" r="1.7"/>
<circle class="dot" cx="206.6" cy="76.3" r="1.7"/>
<circle class="dot" cx="217.0" cy="57.4" r="1.7"/>
<circle class="dot" cx="227.4" cy="80.4" r="1.7"/>
<circle class="dot" cx="237.8" cy="65.9" r="1.7"/>
<circle class="dot" cx="248.2" cy="98.4" r="1.7"/>
<circle class="dot" cx="258.6" cy="32.4" r="1.7"/>
<circle class="dot" cx="269.0" cy="81.4" r="1.7"/>
<circle class="dot" cx="279.4" cy="92.7" r="1.7"/>
<circle class="dot" cx="289.8" cy="84.4" r="1.7"/>
<circle class="dot" cx="300.3" cy="32.4" r="1.7"/>
<circle class="dot" cx="310.7" cy="52.9" r="1.7"/>
<circle class="dot" cx="321.1" cy="81.7" r="1.7"/>
<circle class="dot" cx="331.5" cy="83.9" r="1.7"/>
<circle class="dot" cx="341.9" cy="73.0" r="1.7"/>
<circle class="dot" cx="352.3" cy="97.6" r="1.7"/>
<circle class="dot" cx="362.7" cy="93.0" r="1.7"/>
<circle class="dot" cx="373.1" cy="33.7" r="1.7"/>
<circle class="dot" cx="383.5" cy="49.9" r="1.7"/>
<circle class="dot" cx="393.9" cy="66.6" r="1.7"/>
<circle class="dot" cx="404.4" cy="61.5" r="1.7"/>
<circle class="dot" cx="414.8" cy="53.7" r="1.7"/>
<circle class="dot" cx="425.2" cy="84.4" r="1.7"/>
<circle class="dot" cx="435.6" cy="75.7" r="1.7"/>
<circle class="dot" cx="446.0" cy="74.3" r="1.7"/>
<g class="chars">
<text x="40.0" y="122.0" text-anchor="middle">W</text>
<text x="50.4" y="122.0" text-anchor="middle">i</text>
<text x="60.8" y="122.0" text-anchor="middle">d</text>
<text x="71.2" y="122.0" text-anchor="middle">t</text>
<text x="81.6" y="122.0" text-anchor="middle">h</text>
<text x="92.1" y="122.0" text-anchor="middle">&#183;</text>
<text x="102.5" y="122.0" text-anchor="middle">2</text>
<text x="112.9" y="122.0" text-anchor="middle">&#183;</text>
<text x="123.3" y="122.0" text-anchor="middle">h</text>
<text x="133.7" y="122.0" text-anchor="middle">a</text>
<text x="144.1" y="122.0" text-anchor="middle">s</text>
<text x="154.5" y="122.0" text-anchor="middle">&#183;</text>
<text x="164.9" y="122.0" text-anchor="middle">t</text>
<text x="175.3" y="122.0" text-anchor="middle">w</text>
<text x="185.7" y="122.0" text-anchor="middle">o</text>
<text x="196.2" y="122.0" text-anchor="middle">&#183;</text>
<text x="206.6" y="122.0" text-anchor="middle">k</text>
<text x="217.0" y="122.0" text-anchor="middle">i</text>
<text x="227.4" y="122.0" text-anchor="middle">n</text>
<text x="237.8" y="122.0" text-anchor="middle">k</text>
<text x="248.2" y="122.0" text-anchor="middle">s</text>
<text x="258.6" y="122.0" text-anchor="middle">&#183;</text>
<text x="269.0" y="122.0" text-anchor="middle">a</text>
<text x="279.4" y="122.0" text-anchor="middle">n</text>
<text x="289.8" y="122.0" text-anchor="middle">d</text>
<text x="300.3" y="122.0" text-anchor="middle">&#183;</text>
<text x="310.7" y="122.0" text-anchor="middle">c</text>
<text x="321.1" y="122.0" text-anchor="middle">a</text>
<text x="331.5" y="122.0" text-anchor="middle">n</text>
<text x="341.9" y="122.0" text-anchor="middle">n</text>
<text x="352.3" y="122.0" text-anchor="middle">o</text>
<text x="362.7" y="122.0" text-anchor="middle">t</text>
<text x="373.1" y="122.0" text-anchor="middle">&#183;</text>
<text x="383.5" y="122.0" text-anchor="middle">i</text>
<text x="393.9" y="122.0" text-anchor="middle">m</text>
<text x="404.4" y="122.0" text-anchor="middle">i</text>
<text x="414.8" y="122.0" text-anchor="middle">t</text>
<text x="425.2" y="122.0" text-anchor="middle">a</text>
<text x="435.6" y="122.0" text-anchor="middle">t</text>
<text x="446.0" y="122.0" text-anchor="middle">e</text>
</g>
<text class="ttl2 l" x="22.0" y="166">state difference left after changing one character at position 32</text>
<g class="axis">
<line x1="62.0" y1="268.0" x2="446.0" y2="268.0"/>
<text class="tick-lbl" x="56.0" y="271.5" text-anchor="end">0.00</text>
<line x1="62.0" y1="245.5" x2="446.0" y2="245.5"/>
<text class="tick-lbl" x="56.0" y="249.0" text-anchor="end">0.25</text>
<line x1="62.0" y1="223.0" x2="446.0" y2="223.0"/>
<text class="tick-lbl" x="56.0" y="226.5" text-anchor="end">0.50</text>
<line x1="62.0" y1="200.5" x2="446.0" y2="200.5"/>
<text class="tick-lbl" x="56.0" y="204.0" text-anchor="end">0.75</text>
<line x1="62.0" y1="178.0" x2="446.0" y2="178.0"/>
<text class="tick-lbl" x="56.0" y="181.5" text-anchor="end">1.00</text>
</g>
<path class="curve bad" d="M62.0,192.2 L66.0,199.6 L70.1,214.3 L74.1,227.6 L78.2,238.1 L82.2,245.3 L86.3,250.4 L90.3,254.2 L94.3,257.0 L98.4,259.2 L102.4,260.7 L106.5,262.0 L110.5,263.1 L114.5,263.9 L118.6,264.5 L122.6,265.0 L126.7,265.4 L130.7,265.8 L134.8,266.1 L138.8,266.3 L142.8,266.5 L146.9,266.7 L150.9,266.8 L155.0,267.0 L159.0,267.1 L163.1,267.2 L167.1,267.3 L171.1,267.3 L175.2,267.4 L179.2,267.5 L183.3,267.5 L187.3,267.6 L191.3,267.6 L195.4,267.6 L199.4,267.7 L203.5,267.7 L207.5,267.7 L211.6,267.8 L215.6,267.8 L219.6,267.8 L223.7,267.8 L227.7,267.8 L231.8,267.9 L235.8,267.9 L239.9,267.9 L243.9,267.9 L247.9,267.9 L252.0,267.9 L256.0,267.9 L260.1,267.9 L264.1,267.9 L268.1,267.9 L272.2,267.9 L276.2,267.9 L280.3,268.0 L284.3,268.0 L288.4,268.0 L292.4,268.0 L296.4,268.0 L300.5,268.0 L304.5,268.0 L308.6,268.0 L312.6,268.0 L316.7,268.0 L320.7,268.0 L324.7,268.0 L328.8,268.0 L332.8,268.0 L336.9,268.0 L340.9,268.0 L344.9,268.0 L349.0,268.0 L353.0,268.0 L357.1,268.0 L361.1,268.0 L365.2,268.0 L369.2,268.0 L373.2,268.0 L377.3,268.0 L381.3,268.0 L385.4,268.0 L389.4,268.0 L393.5,268.0 L397.5,268.0 L401.5,268.0 L405.6,268.0 L409.6,268.0 L413.7,268.0 L417.7,268.0 L421.7,268.0 L425.8,268.0 L429.8,268.0 L433.9,268.0 L437.9,268.0 L442.0,268.0 L446.0,268.0" fill="none"/>
<path class="curve ok3" d="M62.0,175.0 L66.0,193.9 L70.1,210.9 L74.1,223.5 L78.2,233.4 L82.2,240.6 L86.3,245.8 L90.3,250.2 L94.3,253.5 L98.4,256.0 L102.4,258.0 L106.5,259.5 L110.5,260.7 L114.5,261.7 L118.6,262.6 L122.6,263.4 L126.7,263.9 L130.7,264.4 L134.8,264.9 L138.8,265.3 L142.8,265.6 L146.9,265.9 L150.9,266.1 L155.0,266.3 L159.0,266.5 L163.1,266.7 L167.1,266.8 L171.1,266.9 L175.2,267.0 L179.2,267.1 L183.3,267.2 L187.3,267.3 L191.3,267.4 L195.4,267.4 L199.4,267.5 L203.5,267.5 L207.5,267.6 L211.6,267.6 L215.6,267.7 L219.6,267.7 L223.7,267.7 L227.7,267.8 L231.8,267.8 L235.8,267.8 L239.9,267.8 L243.9,267.8 L247.9,267.9 L252.0,267.9 L256.0,267.9 L260.1,267.9 L264.1,267.9 L268.1,267.9 L272.2,267.9 L276.2,267.9 L280.3,267.9 L284.3,267.9 L288.4,267.9 L292.4,267.9 L296.4,268.0 L300.5,268.0 L304.5,268.0 L308.6,268.0 L312.6,268.0 L316.7,268.0 L320.7,268.0 L324.7,268.0 L328.8,268.0 L332.8,268.0 L336.9,268.0 L340.9,268.0 L344.9,268.0 L349.0,268.0 L353.0,268.0 L357.1,268.0 L361.1,268.0 L365.2,268.0 L369.2,268.0 L373.2,268.0 L377.3,268.0 L381.3,268.0 L385.4,268.0 L389.4,268.0 L393.5,268.0 L397.5,268.0 L401.5,268.0 L405.6,268.0 L409.6,268.0 L413.7,268.0 L417.7,268.0 L421.7,268.0 L425.8,268.0 L429.8,268.0 L433.9,268.0 L437.9,268.0 L442.0,268.0 L446.0,268.0" fill="none"/>
<path class="curve ok2" d="M62.0,175.2 L66.0,194.2 L70.1,212.2 L74.1,226.3 L78.2,237.1 L82.2,244.7 L86.3,249.9 L90.3,253.8 L94.3,256.8 L98.4,259.0 L102.4,260.6 L106.5,261.7 L110.5,262.6 L114.5,263.4 L118.6,264.0 L122.6,264.5 L126.7,264.9 L130.7,265.3 L134.8,265.6 L138.8,265.9 L142.8,266.2 L146.9,266.4 L150.9,266.6 L155.0,266.8 L159.0,266.9 L163.1,267.0 L167.1,267.1 L171.1,267.2 L175.2,267.3 L179.2,267.4 L183.3,267.5 L187.3,267.5 L191.3,267.6 L195.4,267.6 L199.4,267.7 L203.5,267.7 L207.5,267.7 L211.6,267.8 L215.6,267.8 L219.6,267.8 L223.7,267.8 L227.7,267.9 L231.8,267.9 L235.8,267.9 L239.9,267.9 L243.9,267.9 L247.9,267.9 L252.0,267.9 L256.0,267.9 L260.1,267.9 L264.1,267.9 L268.1,268.0 L272.2,268.0 L276.2,268.0 L280.3,268.0 L284.3,268.0 L288.4,268.0 L292.4,268.0 L296.4,268.0 L300.5,268.0 L304.5,268.0 L308.6,268.0 L312.6,268.0 L316.7,268.0 L320.7,268.0 L324.7,268.0 L328.8,268.0 L332.8,268.0 L336.9,268.0 L340.9,268.0 L344.9,268.0 L349.0,268.0 L353.0,268.0 L357.1,268.0 L361.1,268.0 L365.2,268.0 L369.2,268.0 L373.2,268.0 L377.3,268.0 L381.3,268.0 L385.4,268.0 L389.4,268.0 L393.5,268.0 L397.5,268.0 L401.5,268.0 L405.6,268.0 L409.6,268.0 L413.7,268.0 L417.7,268.0 L421.7,268.0 L425.8,268.0 L429.8,268.0 L433.9,268.0 L437.9,268.0 L442.0,268.0 L446.0,268.0" fill="none"/>
<g class="lgd">
<line class="curve ok2" x1="326.0" y1="182.0" x2="348.0" y2="182.0" fill="none"/>
<text class="lbl" x="354.0" y="185.5">GRU</text>
<line class="curve ok3" x1="326.0" y1="194.0" x2="348.0" y2="194.0" fill="none"/>
<text class="lbl" x="354.0" y="197.5">LSTM</text>
<line class="curve bad" x1="326.0" y1="206.0" x2="348.0" y2="206.0" fill="none"/>
<text class="lbl" x="354.0" y="209.5">RNN</text>
</g>
<g class="lbl-ax">
<text x="62.0" y="283">0</text>
<text x="94.3" y="283">8</text>
<text x="126.7" y="283">16</text>
<text x="191.3" y="283">32</text>
<text x="320.7" y="283">64</text>
<text x="446.0" y="283">95</text>
<text class="cap l" x="62.0" y="298">characters after the change</text></g>
</svg>
<figcaption>Above: unit 546 of the 683 hidden units, reading one character at a time. The vertical rules mark spaces, and the value climbs to near 1 at every one of them. Below: two texts differing in exactly one character at position 32, and the difference left in the hidden state. All three halve within four characters and fall under 0.01 by thirty-two.</figcaption>
</figure>

It climbs to about `0.9` at every space and falls back on letters. One number out
of 683 is being used to mean **"I have just read a space".**

Why that is useful is immediate. For predicting the next character it matters a
great deal whether this is the start of a word, because the distribution over
word-initial characters is not the distribution over word-internal ones.

The other three sit around `0.2`, which is not readable in any real sense. One
unit holding one concept is the exception; usually it is spread across many. This
one happened to turn up.

## Changing one character

How true is "carrying it along"? Make two copies of the same text differing in
**exactly one** character at position `32`, and measure how different the hidden
state stays afterwards.

```
    after     RNN    LSTM     GRU
        1   0.760   0.824   0.820
        4   0.332   0.385   0.343
        8   0.122   0.161   0.124
       32   0.004   0.007   0.005
       95   0.000   0.000   0.000
```

Immediately after the change, `76~82%` of the state differs. But **half of it is
gone within four characters, and less than 1% survives thirty-two.**

The gated LSTM and GRU are almost identical. Which says the rate of forgetting is
set by training rather than by architecture - and pulling the gates open to look
is part two.

The thing to keep is this. **A recurrent state remembers about four characters.**
And yet, as part seven shows, these models predict the next character rather
well, because most characters are decided by the few just before them.

## What is left

`tanh` was used without justifying it. `relu` lets the state diverge easily, which
is why recurrent cells use a squashing function - unmeasured here.

The unit correlations are linear, so anything two units represent jointly is
invisible to them. Far more will be missed by a one-unit probe than caught.

And these numbers come from a model trained 800 steps. Training longer raises the
validation loss, as part seven shows, and what the units represent at that point
was not looked at.

## So

- One recurrent step is the single line `h = tanh(W_ih·x + W_hh·h + b)`: the new
  character once, the carried state once, added and squashed
- It runs 128 times through **the same matrix**, unlike a deep network with
  different weights per layer
- Of `637,845` parameters, `466,489` - `73.1%` - are `W_hh`, carrying state to
  state. Taking the input in is only `87,424`
- Unit `546` of 683 correlates `+0.675` with spaces, switching to about `0.9` at
  every space in real text
- Changing one character alters `76%` of the state, but **half is gone in four
  characters and under 1% survives thirty-two**
- The gated LSTM and GRU forget at almost exactly the same rate
