---
title: "Pulling the gates out, the forget gate had barely moved"
description: "Reading what an LSTM opens and closes straight out of the trained weights. The forget gate averages 0.495, essentially the sigmoid(0) = 0.5 it started at, and not one of the 325 units holds anything longer than three characters. Yet the state remembers longer than that."
date: 2025-11-25
lang: en
kind: guide
series:
  id: not-attention
  part: 2
---

Part one changed one character and watched the difference in hidden state halve
within four. The gated LSTM and GRU decayed at nearly the same rate as the
ungated RNN. Seeing why a gated cell behaves like an ungated one means pulling the
gates out and looking.

## One LSTM step

An RNN replaces its state wholesale. An LSTM splits the state in two: the **cell
state** `c` is only edited a little at a time, and the **hidden state** `h` takes
out of it whatever is needed. Gates decide how much of each.

```python
z = W_ih @ x + b_ih + W_hh @ h + b_hh     # four chunks at once
i = sigmoid(z[0:H])      # input gate - how much of the new goes in
f = sigmoid(z[H:2H])     # forget gate - how much of the old stays
g = tanh(z[2H:3H])       # candidate - the content to put in
o = sigmoid(z[3H:4H])    # output gate - how much of the cell shows

c = f * c + i * g
h = o * tanh(c)
```

`i`, `f` and `o` come through `sigmoid`, so they live between 0 and 1: shut at 0,
open at 1.

The line that matters is `c = f * c + i * g`. A gradient going backward is
multiplied by `f` at each step, so how far back the cell remembers is set by `f` -
in theory at least.

`nn.LSTM` returns only `h` and keeps the gates to itself, so the lines above were
run by hand from the trained weights. They match PyTorch's `h` to at most
`6.85e-07`. Everything below is read out that way.

## What the gates actually are

Taking the same 800-step LSTM part one used, feeding 32 validation lines of 128
characters and collecting all 325 units' gates gives `1,331,200` values.

```
              mean     5%     25%     50%     75%     95%
input i      0.661  0.294   0.515   0.684   0.828   0.946
forget f     0.495  0.081   0.258   0.491   0.730   0.922
output o     0.587  0.178   0.392   0.597   0.798   0.947
```

**The forget gate averages `0.495`.** PyTorch starts biases at zero, so an
untrained forget gate is `sigmoid(0) = 0.5`. After 800 steps of training it has
barely left.

## No unit is holding a long memory

An average of 0.5 would still be interesting if some units sat at 0.95, holding
on for a long time, while others sat at 0.1 and dropped everything - a division
of labour across timescales, which is the usual telling. Unit by unit:

<figure class="fig">
<svg viewBox="0 0 460 316" role="img" aria-label="Above: the mean forget gate of all 325 LSTM units, sorted. They all fall between 0.31 and 0.79, barely leaving the 0.5 they started at. Below: how the cell-state difference dies after one character changes - the measured curve outlives what the forget gate alone would leave">
<text class="ttl2 l" x="34.0" y="16">mean forget gate of all 325 units, sorted</text>
<g class="axis">
<line x1="66.0" y1="115.2" x2="372.0" y2="115.2"/>
<text class="tick-lbl" x="60.0" y="118.7" text-anchor="end">0.3</text>
<line x1="66.0" y1="101.5" x2="372.0" y2="101.5"/>
<text class="tick-lbl" x="60.0" y="105.0" text-anchor="end">0.4</text>
<line x1="66.0" y1="87.8" x2="372.0" y2="87.8"/>
<text class="tick-lbl" x="60.0" y="91.3" text-anchor="end">0.5</text>
<line x1="66.0" y1="74.2" x2="372.0" y2="74.2"/>
<text class="tick-lbl" x="60.0" y="77.7" text-anchor="end">0.6</text>
<line x1="66.0" y1="60.5" x2="372.0" y2="60.5"/>
<text class="tick-lbl" x="60.0" y="64.0" text-anchor="end">0.7</text>
<line x1="66.0" y1="46.8" x2="372.0" y2="46.8"/>
<text class="tick-lbl" x="60.0" y="50.3" text-anchor="end">0.8</text>
</g>
<line class="ref" x1="66.0" y1="87.8" x2="372.0" y2="87.8"/>
<text class="lbl bad" x="74.0" y="81.8">init 0.5</text>
<path class="curve ok" d="M66.0,114.3 L66.9,113.2 L67.9,111.7 L68.8,111.3 L69.8,111.3 L70.7,109.9 L71.7,109.6 L72.6,109.4 L73.6,108.7 L74.5,108.3 L75.4,108.0 L76.4,106.9 L77.3,106.8 L78.3,106.5 L79.2,106.1 L80.2,105.2 L81.1,104.6 L82.1,104.3 L83.0,104.2 L83.9,104.0 L84.9,103.8 L85.8,103.8 L86.8,103.6 L87.7,103.5 L88.7,103.5 L89.6,103.1 L90.6,103.0 L91.5,103.0 L92.4,102.9 L93.4,102.8 L94.3,102.4 L95.3,102.3 L96.2,102.2 L97.2,101.9 L98.1,101.9 L99.1,101.9 L100.0,101.8 L100.9,101.7 L101.9,101.7 L102.8,101.4 L103.8,101.3 L104.7,101.3 L105.7,101.0 L106.6,100.9 L107.6,100.8 L108.5,100.6 L109.4,100.6 L110.4,100.2 L111.3,99.9 L112.3,99.4 L113.2,99.3 L114.2,99.2 L115.1,99.2 L116.1,99.2 L117.0,99.1 L117.9,99.0 L118.9,99.0 L119.8,98.9 L120.8,98.8 L121.7,98.7 L122.7,98.6 L123.6,98.6 L124.6,98.5 L125.5,98.4 L126.4,98.4 L127.4,97.9 L128.3,97.9 L129.3,97.8 L130.2,97.6 L131.2,97.6 L132.1,97.5 L133.1,97.3 L134.0,96.9 L134.9,96.9 L135.9,96.6 L136.8,96.6 L137.8,96.5 L138.7,96.3 L139.7,96.2 L140.6,96.2 L141.6,96.2 L142.5,96.1 L143.4,96.0 L144.4,95.9 L145.3,95.5 L146.3,95.5 L147.2,95.5 L148.2,95.3 L149.1,95.3 L150.1,95.1 L151.0,94.9 L151.9,94.7 L152.9,94.4 L153.8,94.4 L154.8,94.3 L155.7,94.2 L156.7,94.2 L157.6,94.1 L158.6,94.1 L159.5,94.1 L160.4,94.0 L161.4,94.0 L162.3,94.0 L163.3,93.9 L164.2,93.9 L165.2,93.8 L166.1,93.4 L167.1,93.2 L168.0,93.1 L168.9,93.1 L169.9,93.0 L170.8,92.9 L171.8,92.9 L172.7,92.8 L173.7,92.8 L174.6,92.8 L175.6,92.7 L176.5,92.3 L177.4,92.1 L178.4,92.1 L179.3,92.0 L180.3,92.0 L181.2,92.0 L182.2,91.7 L183.1,91.6 L184.1,91.6 L185.0,91.6 L185.9,91.5 L186.9,91.5 L187.8,91.5 L188.8,91.4 L189.7,91.4 L190.7,91.3 L191.6,91.3 L192.6,91.2 L193.5,91.2 L194.4,91.1 L195.4,91.0 L196.3,91.0 L197.3,90.9 L198.2,90.8 L199.2,90.7 L200.1,90.7 L201.1,90.6 L202.0,90.4 L202.9,90.4 L203.9,90.2 L204.8,90.2 L205.8,90.2 L206.7,90.1 L207.7,90.1 L208.6,90.0 L209.6,90.0 L210.5,89.9 L211.4,89.8 L212.4,89.6 L213.3,89.3 L214.3,89.3 L215.2,89.1 L216.2,89.1 L217.1,89.0 L218.1,88.9 L219.0,88.7 L219.9,88.6 L220.9,88.6 L221.8,88.6 L222.8,88.6 L223.7,88.3 L224.7,88.3 L225.6,88.2 L226.6,88.0 L227.5,88.0 L228.4,87.8 L229.4,87.8 L230.3,87.7 L231.3,87.7 L232.2,87.6 L233.2,87.6 L234.1,87.5 L235.1,87.5 L236.0,87.4 L236.9,87.4 L237.9,87.3 L238.8,87.2 L239.8,87.2 L240.7,87.1 L241.7,87.0 L242.6,86.8 L243.6,86.7 L244.5,86.7 L245.4,86.6 L246.4,86.6 L247.3,86.5 L248.3,86.3 L249.2,86.1 L250.2,86.1 L251.1,86.0 L252.1,85.9 L253.0,85.9 L253.9,85.7 L254.9,85.7 L255.8,85.7 L256.8,85.4 L257.7,85.3 L258.7,85.2 L259.6,85.2 L260.6,85.2 L261.5,85.2 L262.4,85.0 L263.4,84.8 L264.3,84.7 L265.3,84.6 L266.2,84.6 L267.2,84.6 L268.1,84.2 L269.1,84.0 L270.0,84.0 L270.9,83.7 L271.9,83.7 L272.8,83.4 L273.8,83.4 L274.7,83.3 L275.7,83.2 L276.6,83.2 L277.6,83.1 L278.5,83.1 L279.4,83.1 L280.4,83.1 L281.3,83.1 L282.3,82.9 L283.2,82.8 L284.2,82.5 L285.1,82.3 L286.1,82.1 L287.0,82.0 L287.9,82.0 L288.9,81.9 L289.8,81.9 L290.8,81.7 L291.7,81.6 L292.7,81.0 L293.6,81.0 L294.6,80.9 L295.5,80.9 L296.4,80.8 L297.4,80.4 L298.3,80.2 L299.3,80.1 L300.2,79.8 L301.2,79.6 L302.1,79.6 L303.1,79.5 L304.0,79.3 L304.9,79.2 L305.9,79.2 L306.8,78.9 L307.8,78.8 L308.7,78.8 L309.7,78.7 L310.6,78.1 L311.6,78.1 L312.5,78.1 L313.4,78.0 L314.4,77.9 L315.3,77.9 L316.3,77.5 L317.2,77.5 L318.2,77.5 L319.1,77.4 L320.1,77.3 L321.0,77.2 L321.9,77.1 L322.9,77.0 L323.8,76.8 L324.8,76.8 L325.7,76.7 L326.7,76.6 L327.6,76.6 L328.6,76.1 L329.5,75.7 L330.4,75.7 L331.4,75.7 L332.3,75.4 L333.3,75.4 L334.2,75.3 L335.2,75.1 L336.1,75.0 L337.1,75.0 L338.0,74.6 L338.9,74.6 L339.9,74.3 L340.8,74.1 L341.8,73.7 L342.7,73.6 L343.7,73.5 L344.6,73.4 L345.6,73.3 L346.5,73.2 L347.4,73.1 L348.4,72.9 L349.3,72.9 L350.3,72.7 L351.2,72.6 L352.2,72.2 L353.1,72.1 L354.1,71.8 L355.0,71.6 L355.9,71.4 L356.9,71.2 L357.8,71.2 L358.8,71.0 L359.7,70.7 L360.7,70.6 L361.6,70.6 L362.6,70.4 L363.5,70.2 L364.4,69.4 L365.4,69.3 L366.3,68.7 L367.3,68.6 L368.2,67.9 L369.2,66.4 L370.1,65.0 L371.1,64.7 L372.0,47.8" fill="none"/>
<text class="cap" x="377.0" y="32">half-life</text>
<text class="tick-lbl" x="377.0" y="111.8">0.7</text>
<text class="tick-lbl" x="377.0" y="74.9">1.4</text>
<text class="tick-lbl" x="377.0" y="51.7">2.9</text>
<text class="ttl2 l" x="34.0" y="174">cell-state difference left after changing one character</text>
<g class="axis">
<line x1="66.0" y1="188.2" x2="440.0" y2="188.2"/>
<text class="tick-lbl" x="60.0" y="191.7" text-anchor="end">1</text>
<line x1="66.0" y1="216.0" x2="440.0" y2="216.0"/>
<text class="tick-lbl" x="60.0" y="219.5" text-anchor="end">0.1</text>
<line x1="66.0" y1="243.7" x2="440.0" y2="243.7"/>
<text class="tick-lbl" x="60.0" y="247.2" text-anchor="end">0.01</text>
<line x1="66.0" y1="271.5" x2="440.0" y2="271.5"/>
<text class="tick-lbl" x="60.0" y="275.0" text-anchor="end">0.001</text>
</g>
<path class="curve ok" d="M66.0,188.4 L77.7,192.3 L89.4,195.3 L101.1,198.3 L112.8,201.3 L124.4,204.0 L136.1,206.6 L147.8,209.2 L159.5,211.6 L171.2,213.8 L182.9,216.0 L194.6,218.0 L206.2,219.8 L217.9,221.5 L229.6,223.3 L241.3,225.0 L253.0,226.6 L264.7,228.2 L276.4,229.9 L288.1,231.5 L299.8,233.0 L311.4,234.4 L323.1,235.8 L334.8,237.1 L346.5,238.4 L358.2,239.7 L369.9,240.9 L381.6,242.0 L393.2,243.3 L404.9,244.5 L416.6,245.8 L428.3,247.0 L440.0,248.2" fill="none"/>
<text class="lbl ok" x="436.0" y="240.2" text-anchor="end">measured</text>
<path class="curve bad" d="M66.0,188.4 L77.7,194.9 L89.4,201.0 L101.1,207.2 L112.8,213.4 L124.4,218.9 L136.1,224.4 L147.8,229.4 L159.5,234.3 L171.2,238.9 L182.9,242.6 L194.6,246.0 L206.2,249.0 L217.9,251.6 L229.6,253.9 L241.3,256.2 L253.0,258.0 L264.7,260.2 L276.4,261.9 L288.1,263.3 L299.8,264.6 L311.4,265.7 L323.1,266.8 L334.8,267.6 L346.5,268.6 L358.2,269.7 L369.9,270.8 L381.6,271.8 L393.2,272.6 L404.9,273.5 L416.6,274.4 L428.3,275.0 L440.0,276.7" fill="none"/>
<text class="lbl bad" x="436.0" y="289.7" text-anchor="end">forget gate alone</text>
<g class="lbl-ax">
<text x="66.0" y="301">0</text>
<text x="112.8" y="301">4</text>
<text x="159.5" y="301">8</text>
<text x="253.0" y="301">16</text>
<text x="346.5" y="301">24</text>
<text x="440.0" y="301">32</text>
<text class="cap l" x="66.0" y="316">characters after the change</text></g>
</svg>
<figcaption>Above: the mean forget gate of all 325 units, smallest first. Every one falls between 0.307 and 0.793, and 172 of them - more than half - sit below the 0.5 they started at. The right-hand scale is the half-life in characters that value implies; even the most retentive unit holds for three. Below: the cell-state difference after one character changes. The measured curve outlives what the forget gate alone would leave - by a factor of 11 at thirty-two characters.</figcaption>
</figure>

```
mean forget gate across the 325 units
  min 0.307    5% 0.377    median 0.494    95% 0.622    max 0.793
the half-life in characters that implies
  min 0.59     median 0.98                 max 2.99
```

**All 325 fall between `0.31` and `0.79`.** As half-lives, the most retentive unit
holds for `3` characters, and `172` of them - more than half - sit below the `0.5`
they started at. Not one holds for ten.

There is no division of labour across timescales. They all forget quickly
together.

## The forget gate is not the whole rate

Except that part one measured the state difference halving in four characters,
four times the `0.98` the median unit's forget gate implies.

Looking at `c = f * c + i * g` again shows why. A perturbation does not only
shrink by `f`. A different `h` makes the next step's `i` and `g` different too,
and that difference goes **back into** the cell. There is a return path alongside
the forgetting one.

Separating them: take the cell difference just after the perturbation and roll it
forward multiplying only by `f`, against actually running both texts to the end.

```
    after   measured   forget gate alone
        1      0.711               0.574
        4      0.337               0.124
        8      0.144               0.022
       16      0.041               0.003
       32     0.0069            6.48e-04
```

Half-life `4` characters measured, `3` with the forget gate alone. By
thirty-two characters the measured difference is **11 times** what the gate would
have left.

**The forget gate sets only part of the rate.** The rest is what re-enters
through the input side every step, and it drags the memory out longer than the
gate says.

## The gates respond to the character

Gate values are not fixed numbers; they are computed from `x` and `h` at every
step, so they should move with the text. Splitting the `4,096` positions by
character and averaging the forget gate:

```
space       0.4623   (865 positions)
newline     0.4597   (105 positions)
everything else 0.5057   (3,126 positions)
```

About `0.05` more closed at spaces and newlines - discarding slightly more where
a word ends. Not a large difference, but the direction is unmistakable: clear out
at the boundary.

## What is left

These numbers come from a model trained 800 steps, which part seven shows is the
bottom of its validation loss. Where the gates go if it keeps training was not
looked at.

The GRU was not opened either. It has two gates and no separate cell state, and
part one found it forgetting at almost the LSTM's rate. That is the next part.

And "no unit holds a long memory" is attached to this corpus and this task. Part
eight opens the forget bias and the reach goes to the whole context while the loss
gets worse. On a task that needed long memory, training would have taken the gates
somewhere else.

## So

- One LSTM step is `c = f·c + i·g` and `h = o·tanh(c)`, with `i`, `f` and `o` all
  doors between 0 and 1
- `nn.LSTM` does not hand over the gates, so the step was run by hand from the
  weights - matching PyTorch to `6.85e-07`
- The forget gate averages `0.495`, essentially the `sigmoid(0) = 0.5` it started
  at
- All 325 units' mean forget gates fall inside `0.307`~`0.793`. As half-lives
  that tops out at `3` characters with none past ten. No division of timescales
- Yet the state itself has a half-life of `4`, and at thirty-two characters holds
  `11` times what the forget gate alone would leave - the difference re-enters
  through the input side
- The gates move with the text: `0.4623` at spaces, `0.4597` at newlines,
  `0.5057` elsewhere. Slightly more discarded at boundaries
