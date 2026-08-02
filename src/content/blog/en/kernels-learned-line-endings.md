---
title: "What the first-layer kernels learned was line endings"
description: "A convolution carries nothing along. One kernel reads five characters at a position and slides. Searching the trained first layer for the five characters each channel responds to most turns up detectors for newlines, decimals, backticks and commas."
date: 2025-12-07
lang: en
kind: guide
series:
  id: not-attention
  part: 4
---

Parts one to three all carried a state around. A convolution carries nothing. It
looks at a few characters near each position, answers, and that is the whole of
it.

## What one kernel computes

A kernel is **a window of a few weights**. At position `t` it multiplies the
characters inside the window by those weights and adds them up, then moves along
one and does it again.

<figure class="fig">
<svg viewBox="0 0 460 300" role="img" aria-label="Above: a kernel of five looking at five characters and sliding one position at a time, the same kernel at every position. Below: channel 12's value rising sharply at every newline">
<text class="ttl2 l" x="40.0" y="18">one kernel slides across positions</text>
<g class="chars2">
<text x="96.0" y="42.0" text-anchor="middle">t</text>
<text x="122.0" y="42.0" text-anchor="middle">h</text>
<text x="148.0" y="42.0" text-anchor="middle">e</text>
<text x="174.0" y="42.0" text-anchor="middle">&#183;</text>
<text x="200.0" y="42.0" text-anchor="middle">c</text>
<text x="226.0" y="42.0" text-anchor="middle">a</text>
<text x="252.0" y="42.0" text-anchor="middle">t</text>
<text x="278.0" y="42.0" text-anchor="middle">&#183;</text>
<text x="304.0" y="42.0" text-anchor="middle">s</text>
<text x="330.0" y="42.0" text-anchor="middle">a</text>
<text x="356.0" y="42.0" text-anchor="middle">t</text>
</g>
<rect class="win" x="85.0" y="60.0" width="126.0" height="14" rx="3"/>
<path class="hop c" d="M200.0,74.0 L200.0,117.0" fill="none"/>
<circle class="dot" cx="200.0" cy="122.0" r="3"/>
<rect class="win" x="137.0" y="78.0" width="126.0" height="14" rx="3"/>
<path class="hop c" d="M252.0,92.0 L252.0,117.0" fill="none"/>
<circle class="dot" cx="252.0" cy="122.0" r="3"/>
<rect class="win" x="189.0" y="96.0" width="126.0" height="14" rx="3"/>
<path class="hop c" d="M304.0,110.0 L304.0,117.0" fill="none"/>
<circle class="dot" cx="304.0" cy="122.0" r="3"/>
<text class="lbl" x="452" y="71.0" text-anchor="end">same kernel every time</text>
<text class="lbl" x="77.0" y="125.5" text-anchor="end">output</text>
<text class="ttl2 l" x="40.0" y="172">what channel 12 learned to do on real text</text>
<g class="axis">
<line x1="40.0" y1="258.0" x2="446.0" y2="258.0"/>
<text class="tick-lbl" x="34.0" y="261.5" text-anchor="end">-1</text>
<line x1="40.0" y1="228.0" x2="446.0" y2="228.0"/>
<text class="tick-lbl" x="34.0" y="231.5" text-anchor="end">+0</text>
<line x1="40.0" y1="198.0" x2="446.0" y2="198.0"/>
<text class="tick-lbl" x="34.0" y="201.5" text-anchor="end">+1</text>
</g><g class="guide">
<line x1="175.3" y1="182.0" x2="175.3" y2="280.0"/>
<line x1="258.6" y1="182.0" x2="258.6" y2="280.0"/>
<line x1="269.0" y1="182.0" x2="269.0" y2="280.0"/>
</g>
<path class="curve ok" d="M40.0,234.8 L50.4,216.6 L60.8,234.5 L71.2,208.9 L81.6,229.3 L92.1,228.6 L102.5,226.4 L112.9,212.6 L123.3,236.5 L133.7,201.0 L144.1,232.7 L154.5,229.9 L164.9,215.9 L175.3,191.1 L185.7,259.7 L196.2,233.3 L206.6,244.1 L217.0,209.8 L227.4,240.6 L237.8,222.3 L248.2,230.4 L258.6,193.3 L269.0,218.7 L279.4,243.3 L289.8,232.4 L300.3,233.1 L310.7,224.3 L321.1,208.8 L331.5,234.2 L341.9,228.0 L352.3,213.0 L362.7,237.6 L373.1,209.4 L383.5,229.4 L393.9,236.3 L404.4,220.2 L414.8,242.5 L425.2,220.9 L435.6,212.6 L446.0,238.7" fill="none"/>
<g class="chars">
<text x="40.0" y="278.0" text-anchor="middle">n</text>
<text x="50.4" y="278.0" text-anchor="middle">k</text>
<text x="60.8" y="278.0" text-anchor="middle">s</text>
<text x="71.2" y="278.0" text-anchor="middle">&#183;</text>
<text x="81.6" y="278.0" text-anchor="middle">a</text>
<text x="92.1" y="278.0" text-anchor="middle">n</text>
<text x="102.5" y="278.0" text-anchor="middle">d</text>
<text x="112.9" y="278.0" text-anchor="middle">&#183;</text>
<text x="123.3" y="278.0" text-anchor="middle">`</text>
<text x="133.7" y="278.0" text-anchor="middle">m</text>
<text x="144.1" y="278.0" text-anchor="middle">+</text>
<text x="154.5" y="278.0" text-anchor="middle">1</text>
<text x="164.9" y="278.0" text-anchor="middle">`</text>
<text x="175.3" y="278.0" text-anchor="middle">&#182;</text>
<text x="185.7" y="278.0" text-anchor="middle">p</text>
<text x="196.2" y="278.0" text-anchor="middle">i</text>
<text x="206.6" y="278.0" text-anchor="middle">e</text>
<text x="217.0" y="278.0" text-anchor="middle">c</text>
<text x="227.4" y="278.0" text-anchor="middle">e</text>
<text x="237.8" y="278.0" text-anchor="middle">s</text>
<text x="248.2" y="278.0" text-anchor="middle">.</text>
<text x="258.6" y="278.0" text-anchor="middle">&#182;</text>
<text x="269.0" y="278.0" text-anchor="middle">&#182;</text>
<text x="279.4" y="278.0" text-anchor="middle">H</text>
<text x="289.8" y="278.0" text-anchor="middle">e</text>
<text x="300.3" y="278.0" text-anchor="middle">r</text>
<text x="310.7" y="278.0" text-anchor="middle">e</text>
<text x="321.1" y="278.0" text-anchor="middle">&#183;</text>
<text x="331.5" y="278.0" text-anchor="middle">i</text>
<text x="341.9" y="278.0" text-anchor="middle">s</text>
<text x="352.3" y="278.0" text-anchor="middle">&#183;</text>
<text x="362.7" y="278.0" text-anchor="middle">`</text>
<text x="373.1" y="278.0" text-anchor="middle">s</text>
<text x="383.5" y="278.0" text-anchor="middle">i</text>
<text x="393.9" y="278.0" text-anchor="middle">n</text>
<text x="404.4" y="278.0" text-anchor="middle">(</text>
<text x="414.8" y="278.0" text-anchor="middle">3</text>
<text x="425.2" y="278.0" text-anchor="middle">x</text>
<text x="435.6" y="278.0" text-anchor="middle">)</text>
<text x="446.0" y="278.0" text-anchor="middle">`</text>
</g>
<text class="lbl" x="40.0" y="293">newline &#182;</text>
</svg>
<figcaption>Above: a kernel of five reads five characters and slides one position at a time. The same kernel at all three, and the window only reaches left, so nothing ahead is visible. Below: what the trained first-layer channel 12 does on real text. The vertical rules are newlines, where it jumps to about 1.2 against an average of 0.02 everywhere else.</figcaption>
</figure>

```python
xp = F.pad(x, (k-1, 0))            # pad only on the left, by k-1
for t in range(L):
    win = xp[:, :, t:t+k]          # (batch, channels, k)
    out[:, :, t] = (win * W).sum() + b
```

Running those lines with the trained weights matches `nn.Conv1d` to at most
`1.79e-06`. The numbers below come from there.

The three windows at the top of the figure are **the same kernel**. That is the
same idea as recurrence reusing one matrix at every step, pointed differently.
Recurrence shares along the time axis and has to go in order; convolution shares
along the position axis and can compute **every position at once**.

## Length grows, the parameter count does not

The first convolution's weights are `(171, 171, 5)`, or `146,205` numbers. Whether
the context is 128 characters or 1024, that does not change, because a kernel only
ever looks near one position.

Doing the same job with a dense layer connecting every position to every position
would take `128 x 171 = 21,888` inputs wired to as many outputs: `479,084,544`
weights. **3,277 times** as many.

Over the whole model:

```
tok.weight        (100, 128)      12,800
inp.weight     (171, 128, 1)      21,888
convs.0~3   (171, 171, 5) x 4    585,504    91.6%
head.weight       (100, 171)      17,100
biases and norms                   1,981
                                 639,273
```

The four kernels are `91.6%` of it - the same shape as part one's RNN spending
73% on carrying state to state.

## Causality is left-only padding

For next-character prediction, position `t` must not see past `t`, or it is
reading the answer.

A convolution usually pads both sides so the window reaches left and right. Here
it is padded **only on the left, by `k-1`**, so position `t`'s window runs from
`t-4` to `t` and nothing ahead gets in. That is the single `F.pad(x, (k-1, 0))`
in the code above.

What part thirteen of the first series did with an attention mask, a convolution
does with where it puts the padding.

## What the kernels respond to

Scanning `7,000` characters of validation text for the five characters each
first-layer channel responds to most turns up readable ones.

```
channel  12   'd^2`\n'  'arts\n'  'why.\n'  '887`\n'
channel 134   '# So\n'  ' the\n'  'd^2`\n'  'or a\n'
channel  20   'ver.\n'  'sum.\n'  'ces.\n'  'full\n'
channel 169   'um.\n\n'  '0`.\n\n'  'ad.\n\n'  '0885\n'
channel  59   ' 0.10'  ' 0.80'  '/0.80'  '`0.80'
channel 105   '`m+1`'  ' = 0`'  ' = 8`'  '0.02`'
channel  63   'bias,'  'ches,'  'ides,'  'odels'
channel  51   ' add '  'y `Σ '  ' 90% '  'eads '
```

Three of them catch **line endings**. `169` catches two newlines together - a
**blank line**. `59` catches **decimal numbers**, `105` **backticks**, `63`
**commas and plural s**, `51` **things ending in a space**.

The lower half of the figure is channel `12` run over real text. It jumps to
`1.23` and `1.16` at the newlines against an average of `0.02` everywhere else.

That is what a first layer does. It picks out whatever is visible in a
five-character window - has the line ended, is this a number, is this code - and
the layers above work from those.

## What is left

This is the **first** layer. Going up, the window widens - nine characters at
layer two, seventeen at layer four - and what the upper channels catch was not
examined. Part five is about that widening.

This model also bottomed out at 300 steps, the fastest of the five in part
seven's table, and what the channels turn into with longer training is unknown.

Only kernel size 5 was used. What changes at 3 or 7 is unmeasured.

## So

- A convolution carries no state. It multiplies a five-character window and adds
- Run by hand it matches `nn.Conv1d` to `1.79e-06`
- All three windows are the same kernel. Recurrence shares weights along time, a
  convolution shares them along position
- The first kernel is `(171, 171, 5)`, `146,205` numbers, independent of context
  length. A dense layer doing the same would need `479,084,544` - `3,277` times
  more
- `91.6%` of the model's parameters are the four kernels
- Causality comes from padding only the left by `k-1`. What attention does with a
  mask, a convolution does with where the padding goes
- First-layer channels catch newlines, blank lines, decimals, backticks and
  commas. Channel `12` reaches `1.23` at a newline against `0.02` elsewhere
