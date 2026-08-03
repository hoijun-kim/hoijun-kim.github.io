---
title: "Widening the window for free made it worse"
description: "The convolution's receptive field taken from 17 characters to 125 at the same budget. Wider is worse throughout. Even holding parameters, channels, depth and kernel fixed and widening from 17 to 61 by dilation alone costs 0.10 - because dilation does not widen so much as thin."
date: 2025-12-13
lang: en
kind: guide
series:
  id: not-attention
  part: 5
---

Part four showed the convolutional model reaching seventeen characters to its
left. The other four see all 128. So widening the window should close the gap.

So widen it.

## The window size comes out of an equation

Stacking layers of kernel `k` with dilation `d` gives a receptive field of

```
1 + Σ d_i · (k - 1)
```

Four layers of kernel 5 gives `1 + 4·4 = 17`; dilating them `1, 2, 4, 8` gives
`1 + 4·(1+2+4+8) = 61`.

Whether the equation is right can be measured. Take the output at the last
position, change a character `d` places back, and run it again. The first `d`
where the output changes by **exactly `0.0`** is the receptive field.

```
                channels  parameters   formula   measured
k5 x4                171     639,273        17         17
k5 x8                122     639,370        33         33
k9 x4                128     633,828        33         33
k5 dilated 1-8       171     639,273        61         61
k5 dilated 1-16      153     635,763       125        125
```

All five agree to the character. This is what part four meant by "not in the
graph means no gradient, not a small one".

## Three ways to widen

Add layers, enlarge the kernel, or dilate. The first two cost parameters, so at a
fixed budget the channel count has to come down. Dilation **costs nothing.**

<figure class="fig">
<svg viewBox="0 0 460 348" role="img" aria-label="Above: which input positions the last output reaches through three layers of kernel 3 - seven characters stacked plain, fifteen when dilated 1-2-4. Below: best validation loss with the receptive field varied from 17 to 125 at the same budget">
<text class="ttl2 l" x="30" y="30">stacked plain</text>
<circle class="nd off" cx="30.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="138.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="150.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="162.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="174.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="186.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="198.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="30.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="138.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="150.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="162.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="174.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="186.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="198.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="30.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="138.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="150.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="162.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="174.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="186.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="198.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="30.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="138.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="150.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="162.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="174.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="186.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="198.0" cy="48.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="48.0" r="2.6"/>
<line class="lk" x1="162.0" y1="126.0" x2="162.0" y2="100.0"/>
<line class="lk" x1="150.0" y1="126.0" x2="162.0" y2="100.0"/>
<line class="lk" x1="138.0" y1="126.0" x2="162.0" y2="100.0"/>
<line class="lk" x1="174.0" y1="126.0" x2="174.0" y2="100.0"/>
<line class="lk" x1="162.0" y1="126.0" x2="174.0" y2="100.0"/>
<line class="lk" x1="150.0" y1="126.0" x2="174.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="126.0" x2="186.0" y2="100.0"/>
<line class="lk" x1="174.0" y1="126.0" x2="186.0" y2="100.0"/>
<line class="lk" x1="162.0" y1="126.0" x2="186.0" y2="100.0"/>
<line class="lk" x1="198.0" y1="126.0" x2="198.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="126.0" x2="198.0" y2="100.0"/>
<line class="lk" x1="174.0" y1="126.0" x2="198.0" y2="100.0"/>
<line class="lk" x1="210.0" y1="126.0" x2="210.0" y2="100.0"/>
<line class="lk" x1="198.0" y1="126.0" x2="210.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="126.0" x2="210.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="100.0" x2="186.0" y2="74.0"/>
<line class="lk" x1="174.0" y1="100.0" x2="186.0" y2="74.0"/>
<line class="lk" x1="162.0" y1="100.0" x2="186.0" y2="74.0"/>
<line class="lk" x1="198.0" y1="100.0" x2="198.0" y2="74.0"/>
<line class="lk" x1="186.0" y1="100.0" x2="198.0" y2="74.0"/>
<line class="lk" x1="174.0" y1="100.0" x2="198.0" y2="74.0"/>
<line class="lk" x1="210.0" y1="100.0" x2="210.0" y2="74.0"/>
<line class="lk" x1="198.0" y1="100.0" x2="210.0" y2="74.0"/>
<line class="lk" x1="186.0" y1="100.0" x2="210.0" y2="74.0"/>
<line class="lk" x1="210.0" y1="74.0" x2="210.0" y2="48.0"/>
<line class="lk" x1="198.0" y1="74.0" x2="210.0" y2="48.0"/>
<line class="lk" x1="186.0" y1="74.0" x2="210.0" y2="48.0"/>
<text class="lbl ok" x="210" y="38" text-anchor="end">reach 7</text>
<text class="ttl2 l" x="250" y="30">dilated 1-2-4</text>
<circle class="nd off" cx="250.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="262.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="274.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="286.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="298.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="310.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="322.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="334.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="346.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="358.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="370.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="382.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="394.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="406.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="418.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="250.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="262.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="274.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="286.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="298.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="310.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="322.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="334.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="346.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="358.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="370.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="382.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="394.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="406.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="418.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="250.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="262.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="274.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="286.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="298.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="310.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="322.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="334.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="346.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="358.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="370.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="382.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="394.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="406.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="418.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="250.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="262.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="274.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="286.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="298.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="310.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="322.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="334.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="346.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="358.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="370.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="382.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="394.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="406.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="418.0" cy="48.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="48.0" r="2.6"/>
<line class="lk" x1="286.0" y1="126.0" x2="286.0" y2="100.0"/>
<line class="lk" x1="274.0" y1="126.0" x2="286.0" y2="100.0"/>
<line class="lk" x1="262.0" y1="126.0" x2="286.0" y2="100.0"/>
<line class="lk" x1="310.0" y1="126.0" x2="310.0" y2="100.0"/>
<line class="lk" x1="298.0" y1="126.0" x2="310.0" y2="100.0"/>
<line class="lk" x1="286.0" y1="126.0" x2="310.0" y2="100.0"/>
<line class="lk" x1="334.0" y1="126.0" x2="334.0" y2="100.0"/>
<line class="lk" x1="322.0" y1="126.0" x2="334.0" y2="100.0"/>
<line class="lk" x1="310.0" y1="126.0" x2="334.0" y2="100.0"/>
<line class="lk" x1="358.0" y1="126.0" x2="358.0" y2="100.0"/>
<line class="lk" x1="346.0" y1="126.0" x2="358.0" y2="100.0"/>
<line class="lk" x1="334.0" y1="126.0" x2="358.0" y2="100.0"/>
<line class="lk" x1="382.0" y1="126.0" x2="382.0" y2="100.0"/>
<line class="lk" x1="370.0" y1="126.0" x2="382.0" y2="100.0"/>
<line class="lk" x1="358.0" y1="126.0" x2="382.0" y2="100.0"/>
<line class="lk" x1="406.0" y1="126.0" x2="406.0" y2="100.0"/>
<line class="lk" x1="394.0" y1="126.0" x2="406.0" y2="100.0"/>
<line class="lk" x1="382.0" y1="126.0" x2="406.0" y2="100.0"/>
<line class="lk" x1="430.0" y1="126.0" x2="430.0" y2="100.0"/>
<line class="lk" x1="418.0" y1="126.0" x2="430.0" y2="100.0"/>
<line class="lk" x1="406.0" y1="126.0" x2="430.0" y2="100.0"/>
<line class="lk" x1="334.0" y1="100.0" x2="334.0" y2="74.0"/>
<line class="lk" x1="310.0" y1="100.0" x2="334.0" y2="74.0"/>
<line class="lk" x1="286.0" y1="100.0" x2="334.0" y2="74.0"/>
<line class="lk" x1="382.0" y1="100.0" x2="382.0" y2="74.0"/>
<line class="lk" x1="358.0" y1="100.0" x2="382.0" y2="74.0"/>
<line class="lk" x1="334.0" y1="100.0" x2="382.0" y2="74.0"/>
<line class="lk" x1="430.0" y1="100.0" x2="430.0" y2="74.0"/>
<line class="lk" x1="406.0" y1="100.0" x2="430.0" y2="74.0"/>
<line class="lk" x1="382.0" y1="100.0" x2="430.0" y2="74.0"/>
<line class="lk" x1="430.0" y1="74.0" x2="430.0" y2="48.0"/>
<line class="lk" x1="382.0" y1="74.0" x2="430.0" y2="48.0"/>
<line class="lk" x1="334.0" y1="74.0" x2="430.0" y2="48.0"/>
<text class="lbl ok" x="430" y="38" text-anchor="end">reach 15</text>
<text class="ttl2 l" x="30.0" y="192">best validation loss against receptive field</text>
<g class="axis">
<line x1="76.0" y1="296.0" x2="430.0" y2="296.0"/>
<text class="tick-lbl" x="70.0" y="299.5" text-anchor="end">1.65</text>
<line x1="76.0" y1="276.0" x2="430.0" y2="276.0"/>
<text class="tick-lbl" x="70.0" y="279.5" text-anchor="end">1.75</text>
<line x1="76.0" y1="256.0" x2="430.0" y2="256.0"/>
<text class="tick-lbl" x="70.0" y="259.5" text-anchor="end">1.85</text>
<line x1="76.0" y1="236.0" x2="430.0" y2="236.0"/>
<text class="tick-lbl" x="70.0" y="239.5" text-anchor="end">1.95</text>
<line x1="76.0" y1="216.0" x2="430.0" y2="216.0"/>
<text class="tick-lbl" x="70.0" y="219.5" text-anchor="end">2.05</text>
</g>
<line class="ref ok" x1="76.0" y1="297.0" x2="430.0" y2="297.0"/>
<text class="lbl ok" x="430.0" y="293.0" text-anchor="end">GRU 1.6449</text>
<line class="ref" x1="76.0" y1="272.4" x2="430.0" y2="272.4"/>
<text class="lbl bad" x="430.0" y="268.4" text-anchor="end">transformer 1.7679</text>
<path class="curve ok2" d="M96.2,251.8 L203.0,239.1 L203.0,213.6 L302.0,231.7 L417.6,226.7" fill="none"/>
<circle class="dot" cx="96.2" cy="251.8" r="3"/>
<text class="lbl" x="96.2" y="243.8" text-anchor="middle">k5 x4</text>
<circle class="dot" cx="203.0" cy="239.1" r="3"/>
<text class="lbl" x="203.0" y="253.1" text-anchor="middle">k5 x8</text>
<circle class="dot" cx="203.0" cy="213.6" r="3"/>
<text class="lbl" x="203.0" y="205.6" text-anchor="middle">k9 x4</text>
<circle class="dot" cx="302.0" cy="231.7" r="3"/>
<text class="lbl" x="302.0" y="245.7" text-anchor="middle">k5 dil 1-8</text>
<circle class="dot" cx="417.6" cy="226.7" r="3"/>
<text class="lbl" x="417.6" y="218.7" text-anchor="middle">k5 dil 1-16</text>
<g class="lbl-ax">
<text x="96.2" y="321">17</text>
<text x="203.0" y="321">33</text>
<text x="302.0" y="321">61</text>
<text x="417.6" y="321">125</text>
<text class="cap l" x="76.0" y="336">receptive field in characters, log</text></g>
</svg>
<figcaption>Above: which inputs the last position reaches through three layers, drawn with kernel 3 for legibility - seven characters stacked plain, fifteen when dilated 1-2-4, with the same number of lines either way. The real model uses kernel 5. Below: the receptive field varied from 17 to 125 at the same budget. Wider is worse throughout, and none of them come near the GRU or the transformer.</figcaption>
</figure>

The top of the figure is that difference: dilating leaves the number of lines
unchanged while the positions reached spread out.

## Wider is worse

```
                   reach  channels  parameters   best val (3 seeds)        median
k5 x4                 17       171     639,273   1.8748 1.8709 1.8695    1.8709
k5 x8                 33       122     639,370   1.9437 1.9346 1.9326    1.9346
k9 x4                 33       128     633,828   2.0592 2.0652 2.0621    2.0621
k5 dilated 1-8        61       171     639,273   1.9716 1.9795 1.9556    1.9716
k5 dilated 1-16      125       153     635,763   1.9967 2.0020 1.9907    1.9967
```

The narrowest is the best: `1.8709` at `17` characters against `1.9967` at `125`.
And none of them come near the GRU's `1.6449` or the transformer's `1.7679`.

Adding layers or enlarging the kernel has an explanation. The budget is fixed, so
channels had to drop from `171` to `122` or `128` - the width of the window was
paid for out of the width of the model.

## Widening for free is also worse

That explanation does not cover dilation. `k5 dilated 1-8` has the same `171`
channels, the same `639,273` parameters, the same four layers and the same kernel
5 as `k5 x4`. The only difference is that its window is `61` rather than `17`.

And it comes out at `1.9716` against `1.8709`, worse by `0.10`, with seed ranges
of `1.9556~1.9795` against `1.8695~1.8748` that do not overlap.

**Widened for free, and worse for it.**

## Dilation does not widen, it thins

Why is countable. Count the **number of paths** from the output back to each
input position - more paths means more computation aimed at that position.

```
                  reach   total paths   positions   share going to the nearest 4
plain x4             17           625     17                             11.2%
dilated 1-8          61           625     61                              1.6%
```

**The path count is `625` either way.** Dilation adds no computation. It spreads
the same `625` over 61 positions instead of 17.

Position by position it is starker:

```
back        0    1    2    3    4    5    6
plain       1    4   10   20   35   52   68
dilated     1    1    2    2    4    3    5
```

Paths to the immediately preceding character drop from `4` to `1`, a factor of
four. Part one measured the recurrent state remembering about four characters and
part two found the gates agreeing. Those four characters are where the signal is,
and dilation moves computation away from them.

It does not widen so much as **relocate.**

## The same 33 built two ways is not the same

`k5 x8` and `k9 x4` both reach `33` and land at `1.9346` and `2.0621`, `0.13`
apart. Eight layers beats a kernel of nine by a lot.

Enlarging a kernel costs parameters in proportion to `k` and eats channels for
it; stacking layers adds one more nonlinearity per layer. **Equal receptive
fields, and how you built them still decides the loss.**

## Correcting a sentence in part seven

Part seven ends with "the CNN sees 17 characters to its left. It loses on sight,
not on budget." The first half is right and the second half is wrong.

Widening the sight to `125` characters gives `1.9967`, worse. **The CNN is not
losing because its view is narrow.** A narrow view is what this task wants, and
whatever paid for the wider one was taken from somewhere.

That passage in part seven has been corrected.

## What is left

Everything here runs to 1200 steps. All five configurations bottom out between
300 and 900, so nothing is cut off, but whether the ordering survives longer
training was not checked.

And "wider is worse" belongs to this corpus and this task. Where the front of the
sequence genuinely matters - matching brackets, long copying - it would be the
reverse. Part eight makes the same point again from the recurrent side.

Only two dilation patterns were tried, `1-2-4-8` and `1-2-4-8-16`. Something like
`1-1-2-2`, which keeps the near positions while spreading a little, is unmeasured.

## So

- The receptive field is `1 + Σ d·(k-1)`, confirmed by changing a character
  outside it and getting **exactly zero** change. All five configurations match
- Wider is worse: `1.8709` at `17` characters up to `1.9967` at `125`
- Layers and kernels cost channels, so that much is unsurprising. But **dilation
  is free** and still takes `1.8709` to `1.9716`, with non-overlapping seed ranges
- Dilation adds no paths. It spreads the same `625` over 61 positions instead of
  17, dropping the nearest four characters' share from `11.2%` to `1.6%`
- Paths to the immediately preceding character go from `4` to `1`. Part one's
  "memory of about four characters" is exactly what gets starved
- Equal receptive fields built differently differ: `33` by depth is `1.9346`, by
  kernel `2.0621`
- Part seven's "loses on sight, not on budget" is wrong, and has been corrected
