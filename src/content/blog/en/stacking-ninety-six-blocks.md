---
title: "What breaks when you stack 96 blocks"
description: "Between residual connections and where the norm goes, which one carries depth? Stacking from 6 blocks to 96 and measuring the gradient at every layer puts a number on it, and the two do not weigh the same."
date: 2025-08-20
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 12
---

The pieces are all in hand: attention, position, several heads, feed-forward.
Now they get tied into a block and stacked. Tying them takes two lines, and
those two lines are the difference between twenty layers and ninety-six.

```python
x = LN(x + Attn(x));   x = LN(x + FFN(x))     # Post-LN, the original paper
x = x + Attn(LN(x));   x = x + FFN(LN(x))     # Pre-LN, the current default
```

The only difference is whether the norm sits **outside** or **inside** the
residual. Do what part four did: stack them and measure the gradient at each
layer. `d=128`, four heads, 4x expansion, PyTorch's default initialisation, in
float64.

## At twenty layers, nothing happens

```
             layer 1 grad   layer 20 grad   ratio (seed 0)   ratio (median of 6)
Post-LN          1.78e-01        3.45e-01            0.516                 0.595
Pre-LN           1.89e-01        1.15e-01            1.646                 1.618
no residual      2.99e-01        9.86e-01            0.303                 0.360
```

All three sit inside a factor of three, removing the residual connections
included, and changing the seed even reorders them - nothing next to the `1e9`
spread part four got out of a bad initialisation.

Part six says why. **Normalisation already resets the scale at every layer.**
With an `LN` in place the forward pass does not die even without residuals. So
a twenty-layer stack cannot tell these three apart.

The depth has to go up.

## Up to ninety-six

The number below is the first layer's gradient divided by the last layer's. At
`1` the two ends match; below it the early layers starve, above it the late
ones do. Median of six seeds.

```
   L   Post-LN   Pre-LN   no residual
   6     0.671     1.20         0.773
  24     0.534     1.69         0.432
  48     0.372     2.23         0.245
  96     0.306     2.89         0.031
```

<figure class="fig">
<svg viewBox="0 0 460 262" role="img" aria-label="Gradient magnitude per block across 96 blocks. Without residual connections the early blocks sink to 0.026, while Pre-LN and Post-LN stay flat within a factor of three">
<g class="axis">
<line x1="54" y1="34.7" x2="446" y2="34.7"/>
<text class="tick-lbl" x="45" y="38.2" text-anchor="end">1e0</text>
<line x1="54" y1="121.3" x2="446" y2="121.3"/>
<text class="tick-lbl" x="45" y="124.8" text-anchor="end">1e-1</text>
<line x1="54" y1="208.0" x2="446" y2="208.0"/>
<text class="tick-lbl" x="45" y="211.5" text-anchor="end">1e-2</text>
<line class="frame" x1="54" y1="26" x2="54" y2="208"/><line class="frame" x1="54" y1="208" x2="446" y2="208"/>
<line class="frame" x1="54.0" y1="208" x2="54.0" y2="212"/>
<text class="tick-lbl" x="54.0" y="224" text-anchor="middle">1</text>
<line class="frame" x1="153.0" y1="208" x2="153.0" y2="212"/>
<text class="tick-lbl" x="153.0" y="224" text-anchor="middle">25</text>
<line class="frame" x1="252.1" y1="208" x2="252.1" y2="212"/>
<text class="tick-lbl" x="252.1" y="224" text-anchor="middle">49</text>
<line class="frame" x1="351.1" y1="208" x2="351.1" y2="212"/>
<text class="tick-lbl" x="351.1" y="224" text-anchor="middle">73</text>
<line class="frame" x1="446.0" y1="208" x2="446.0" y2="212"/>
<text class="tick-lbl" x="446.0" y="224" text-anchor="middle">96</text>
<text class="tick-lbl" x="250.0" y="256" text-anchor="middle">block</text>
<text class="tick-lbl" x="54" y="16" text-anchor="start">gradient size</text></g>
<path class="curve bad" fill="none" d="M54.0,172.6 L58.1,162.1 L62.3,155.9 L66.4,148.9 L70.5,147.0 L74.6,150.9 L78.8,153.9 L82.9,150.3 L87.0,156.1 L91.1,155.3 L95.3,153.8 L99.4,150.0 L103.5,148.3 L107.6,139.8 L111.8,141.8 L115.9,142.3 L120.0,140.3 L124.1,141.9 L128.3,140.8 L132.4,131.0 L136.5,122.7 L140.7,118.7 L144.8,112.6 L148.9,106.6 L153.0,109.5 L157.2,114.8 L161.3,111.3 L165.4,114.1 L169.5,117.9 L173.7,118.3 L177.8,118.6 L181.9,117.7 L186.0,109.7 L190.2,100.8 L194.3,97.7 L198.4,99.0 L202.5,110.6 L206.7,115.2 L210.8,116.8 L214.9,115.4 L219.1,114.9 L223.2,118.9 L227.3,109.5 L231.4,100.5 L235.6,105.6 L239.7,107.7 L243.8,107.0 L247.9,108.0 L252.1,119.9 L256.2,118.2 L260.3,118.0 L264.4,111.2 L268.6,111.3 L272.7,116.1 L276.8,123.0 L280.9,128.8 L285.1,118.0 L289.2,109.0 L293.3,112.3 L297.5,105.1 L301.6,100.4 L305.7,95.8 L309.8,96.4 L314.0,106.2 L318.1,108.4 L322.2,105.3 L326.3,100.8 L330.5,90.0 L334.6,87.1 L338.7,92.7 L342.8,89.7 L347.0,85.0 L351.1,93.8 L355.2,94.4 L359.3,89.9 L363.5,91.4 L367.6,84.7 L371.7,82.1 L375.9,81.5 L380.0,75.6 L384.1,70.3 L388.2,65.1 L392.4,62.5 L396.5,59.7 L400.6,56.7 L404.7,58.8 L408.9,65.6 L413.0,62.6 L417.1,60.0 L421.2,53.8 L425.4,47.7 L429.5,50.4 L433.6,49.8 L437.7,56.7 L441.9,53.7 L446.0,40.9"/>
<path class="curve bad2" fill="none" d="M54.0,113.8 L58.1,115.1 L62.3,114.2 L66.4,113.5 L70.5,112.5 L74.6,110.7 L78.8,110.9 L82.9,110.3 L87.0,108.3 L91.1,107.2 L95.3,104.9 L99.4,107.4 L103.5,106.1 L107.6,105.6 L111.8,102.2 L115.9,104.7 L120.0,104.6 L124.1,103.7 L128.3,103.5 L132.4,108.4 L136.5,107.5 L140.7,100.8 L144.8,102.0 L148.9,99.8 L153.0,100.2 L157.2,104.4 L161.3,104.4 L165.4,105.2 L169.5,104.8 L173.7,108.6 L177.8,105.9 L181.9,106.8 L186.0,107.8 L190.2,103.7 L194.3,105.9 L198.4,103.9 L202.5,103.7 L206.7,102.9 L210.8,100.7 L214.9,100.8 L219.1,98.1 L223.2,98.8 L227.3,101.1 L231.4,100.5 L235.6,99.8 L239.7,102.6 L243.8,101.6 L247.9,102.2 L252.1,102.0 L256.2,98.6 L260.3,96.4 L264.4,94.9 L268.6,97.5 L272.7,97.3 L276.8,95.4 L280.9,98.4 L285.1,100.2 L289.2,100.3 L293.3,98.2 L297.5,98.3 L301.6,96.1 L305.7,94.7 L309.8,95.0 L314.0,96.5 L318.1,94.2 L322.2,95.1 L326.3,93.8 L330.5,92.9 L334.6,92.5 L338.7,91.0 L342.8,90.7 L347.0,91.2 L351.1,89.4 L355.2,88.0 L359.3,87.9 L363.5,87.6 L367.6,86.3 L371.7,85.8 L375.9,87.9 L380.0,91.1 L384.1,92.9 L388.2,87.2 L392.4,91.2 L396.5,86.4 L400.6,89.2 L404.7,88.3 L408.9,88.2 L413.0,90.7 L417.1,93.9 L421.2,95.5 L425.4,91.5 L429.5,93.8 L433.6,95.3 L437.7,91.6 L441.9,93.1 L446.0,69.3"/>
<path class="curve ok" fill="none" d="M54.0,99.3 L58.1,101.5 L62.3,101.9 L66.4,103.2 L70.5,103.1 L74.6,103.4 L78.8,104.5 L82.9,105.1 L87.0,106.1 L91.1,106.1 L95.3,105.1 L99.4,107.5 L103.5,109.2 L107.6,110.0 L111.8,110.2 L115.9,111.2 L120.0,112.3 L124.1,112.4 L128.3,112.3 L132.4,114.7 L136.5,116.5 L140.7,115.0 L144.8,116.4 L148.9,116.3 L153.0,118.1 L157.2,120.4 L161.3,119.6 L165.4,121.0 L169.5,121.3 L173.7,123.1 L177.8,123.1 L181.9,123.5 L186.0,125.6 L190.2,125.1 L194.3,126.9 L198.4,127.6 L202.5,127.8 L206.7,128.4 L210.8,128.0 L214.9,128.5 L219.1,128.8 L223.2,129.1 L227.3,129.2 L231.4,129.2 L235.6,128.6 L239.7,130.7 L243.8,128.5 L247.9,132.4 L252.1,131.5 L256.2,131.5 L260.3,131.5 L264.4,132.7 L268.6,132.5 L272.7,131.8 L276.8,131.8 L280.9,133.7 L285.1,134.1 L289.2,133.6 L293.3,134.6 L297.5,134.7 L301.6,136.4 L305.7,135.4 L309.8,134.7 L314.0,137.9 L318.1,135.1 L322.2,135.9 L326.3,135.7 L330.5,137.9 L334.6,136.2 L338.7,135.9 L342.8,140.2 L347.0,137.5 L351.1,138.2 L355.2,137.5 L359.3,138.1 L363.5,137.3 L367.6,136.8 L371.7,136.9 L375.9,137.2 L380.0,138.6 L384.1,139.0 L388.2,139.1 L392.4,138.1 L396.5,139.3 L400.6,138.5 L404.7,138.5 L408.9,139.5 L413.0,138.7 L417.1,139.5 L421.2,139.1 L425.4,140.9 L429.5,140.9 L433.6,142.6 L437.7,139.9 L441.9,141.8 L446.0,142.8"/>
<text class="lbl bad" x="87.0" y="173.1" text-anchor="start">no residual</text>
<text class="lbl bad" x="219.1" y="88.1" text-anchor="middle">Post-LN</text>
<text class="lbl ok" x="384.1" y="156.0" text-anchor="middle">Pre-LN</text>
</svg>
<figcaption>Gradient magnitude per block in a 96-block stack. Drop the residual connections and the early blocks sink to 0.026, a thirty-third of the last block. With residuals, putting the norm before or after leaves the profile flat within a factor of three.</figcaption>
</figure>

The three rows tell different stories.

**Only the no-residual stack breaks.** From `0.773` to `0.031`: at ninety-six
layers the first block receives a thirty-second of what the last one does. And it
accelerates - it holds at `0.245` through forty-eight layers and falls away
sharply after. An `LN` keeps the forward pass alive but does not keep the
backward pass balanced across layers.

**Post-LN and Pre-LN tilt in opposite directions.** Post-LN's `0.306` starves
the early layers by 3.3x; Pre-LN's `2.89` starves the late ones by 2.9x. Both grow
with depth, and both are still inside a factor of three at ninety-six layers.

So **what carries depth is the residual connection, and where the norm goes is
the dial that tilts the gradient one way or the other on top of it.** They are
an order of magnitude apart.

Post-LN starving its early layers is the reason learning-rate warmup is known to
be necessary for it. Note though that what is measured here is only **the
gradient profile at initialisation**. How it changes as training proceeds is a
question this experiment does not answer.

## The residual stream grows

Pre-LN comes with one more property. Every block only ever **adds** to the
stream, so the stream keeps growing.

```
   L   layer 1 sd   last sd   factor   sqrt(L)
   6         1.04      1.21     1.17      2.45
  24         1.03      1.91     1.85      4.90
  96         1.04      3.59     3.46      9.80
```

The growth is usually quoted as `sqrt(L)`: add `L` independent things and the
variance multiplies by `L`, so the standard deviation multiplies by `sqrt(L)`.
Measured, it is `3.46`, not `9.80` - an exponent of `0.272`, about half of
`0.5`.

The premise does not hold. `sqrt(L)` is the calculation for terms **comparable
in size** to the stream, and at default initialisation a sublayer's output is
far smaller than the stream. Checking it is easy: scale up the initialisation of
`Wo` and `W2`.

```
  output scale 1     factor  3.46   exponent 0.272
  output scale 3     factor  9.21   exponent 0.487
  output scale 10    factor 14.19   exponent 0.581
```

At three times the scale the exponent is `0.487`, right on `0.5`. **`sqrt(L)` is
not wrong but conditional**, and at real initialisation the condition fails.

The stream does grow all the same, which is why a Pre-LN network puts one more
`LN` at the very end. The experiment above includes it. Without it the output
leaves at whatever size the stream reached.

## So

- Twenty layers distinguish nothing. Normalisation resets the scale every layer,
  so even a residual-free stack looks healthy
- Ninety-six layers separate them. Without residuals the first layer's gradient
  is `1/32` of the last's, and it turns sharp past forty-eight
- Post-LN and Pre-LN tilt opposite ways, `0.306` against `2.89`. Opposite in
  direction but both inside a factor of three - a different order of magnitude
  from the residual's thirty-two
- The Pre-LN stream grows, but not by `sqrt(L)`. Measured exponent `0.272`;
  scale the sublayer outputs by three and it becomes `0.487`, matching the
  calculation
- What is measured is the gradient profile at initialisation. Training is a
  separate question

Next time all of it runs at once. Having looked at the pieces and
the wiring, the smallest thing that actually predicts characters gets built end
to end.
