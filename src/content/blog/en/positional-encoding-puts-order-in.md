---
title: "How positional encoding puts order back in"
description: "Part eight left attention blind to order. This measures why writing the position in as a raw number breaks it, what sinusoids guarantee instead, and why the usual claim that similarity decays with distance is not true."
date: 2026-08-05
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 9
---

Part eight ended on attention being permutation equivariant. Shuffle the inputs
and the outputs shuffle identically; not one value changes. Attention has no
"before" and no "after".

In a sentence, order is meaning. So order has to be supplied separately. This
part is about how.

## Why the naive way fails

The first idea is to write the position number in as one more dimension: append
`i` to token `i`'s vector.

It breaks immediately. An attention logit is a dot product, and a dot product
carries the `i x j` term straight through.

```
positions 0-5     content spread 3.30   position spread  11.18   max prob 0.626
positions 100-105 content spread 3.30   position spread 458.39   max prob 1.000
```

Content moves the logits by `3.30` while position moves them by `458`, and the
ratio only widens further into the sentence. Part eight showed that large logits
saturate the softmax; here the largest probability is `1.000`. **Attention stops
looking at content at all.**

That gives the requirement. Position information has to differ from place to
place without **growing** as the place gets later.

## Sinusoids

The transformer's answer is periodic functions. Dimensions are taken in pairs,
each pair carrying a sine and cosine at its own frequency.

```python
def PE(L, d):
    pos = np.arange(L)[:, None]
    i = np.arange(0, d, 2)[None, :]
    w = 1.0 / (10000 ** (i / d))          # frequency, different per dimension
    P = np.zeros((L, d))
    P[:, 0::2] = np.sin(pos * w)
    P[:, 1::2] = np.cos(pos * w)
    return P
```

Take the guarantees one at a time. Everything below uses `d=64` and 512
positions.

**First, every position has the same size.** Each frequency contributes
`sin² + cos² = 1`, so the norm is `sqrt(d/2)` no matter the position. Measured,
that is `5.6569`, varying by `8.9e-16` across all 512 positions. This is exactly
the condition the naive method broke.

**Second, the dot product of two positions depends only on their distance.**
`PE(i)·PE(j)` does not see `i` and `j` separately, only `i-j`. Measuring the
spread of values along each diagonal gives `1.8e-13`, floating-point noise. The
angle-addition identity explains it in one line.

```
PE(i)·PE(j) = Σ [sin(i·w) sin(j·w) + cos(i·w) cos(j·w)] = Σ cos((i-j)·w)
```

Comparing against `Σ cos(distance · w)` directly, the largest difference is
`7.1e-15`. **Absolute positions go in and relative position comes out.** That is
the real reason for choosing sinusoids.

## Similarity does not decay with distance

The usual next step is one claim too far: "so the dot product shrinks with
distance, and nearby tokens end up more alike". Measured, it does not.

<figure class="fig">
<svg viewBox="0 0 460 250" role="img" aria-label="The dot product between two positional encodings plotted against their distance. It falls quickly at first, then rises and falls again from distance 6 onward, reaching its minimum at distance 406 before climbing back">
<g class="axis">
<line x1="52" y1="206.0" x2="446" y2="206.0"/>
<text class="tick-lbl" x="43" y="209.5" text-anchor="end">0</text>
<line x1="52" y1="161.0" x2="446" y2="161.0"/>
<text class="tick-lbl" x="43" y="164.5" text-anchor="end">8</text>
<line x1="52" y1="116.0" x2="446" y2="116.0"/>
<text class="tick-lbl" x="43" y="119.5" text-anchor="end">16</text>
<line x1="52" y1="71.0" x2="446" y2="71.0"/>
<text class="tick-lbl" x="43" y="74.5" text-anchor="end">24</text>
<line x1="52" y1="26.0" x2="446" y2="26.0"/>
<text class="tick-lbl" x="43" y="29.5" text-anchor="end">32</text>
<line class="frame" x1="52" y1="26" x2="52" y2="206"/><line class="frame" x1="52" y1="206" x2="446" y2="206"/>
<line class="frame" x1="52.0" y1="206" x2="52.0" y2="210"/>
<text class="tick-lbl" x="52.0" y="222" text-anchor="middle">0</text>
<line class="frame" x1="150.7" y1="206" x2="150.7" y2="210"/>
<text class="tick-lbl" x="150.7" y="222" text-anchor="middle">128</text>
<line class="frame" x1="249.4" y1="206" x2="249.4" y2="210"/>
<text class="tick-lbl" x="249.4" y="222" text-anchor="middle">256</text>
<line class="frame" x1="348.1" y1="206" x2="348.1" y2="210"/>
<text class="tick-lbl" x="348.1" y="222" text-anchor="middle">384</text>
<line class="frame" x1="446.0" y1="206" x2="446.0" y2="210"/>
<text class="tick-lbl" x="446.0" y="222" text-anchor="middle">511</text>
<text class="tick-lbl" x="249.0" y="244" text-anchor="middle">distance between the two positions</text>
<text class="tick-lbl" x="52" y="16" text-anchor="start">dot product</text></g>
<path class="curve ok" fill="none" d="M52.0,26.0 L52.8,32.1 L53.5,46.8 L54.3,62.1 L55.1,71.4 L55.9,73.8 L56.6,73.5 L57.4,75.1 L58.2,79.9 L58.9,85.1 L59.7,87.6 L60.5,86.9 L61.3,86.0 L62.0,87.8 L62.8,92.4 L63.6,96.5 L64.3,97.0 L65.1,94.2 L65.9,91.8 L66.6,93.6 L67.4,99.8 L68.2,106.0 L69.0,107.1 L69.7,102.0 L70.5,95.1 L71.3,92.7 L72.0,98.3 L72.8,108.8 L73.6,117.0 L74.4,117.3 L75.1,110.0 L75.9,100.7 L76.7,96.0 L77.4,98.3 L78.2,105.0 L79.0,111.4 L79.8,115.1 L80.5,116.9 L81.3,118.6 L82.1,120.2 L82.8,119.4 L83.6,114.0 L84.4,105.4 L85.2,98.5 L85.9,98.3 L86.7,105.8 L87.5,116.5 L88.2,123.8 L89.0,124.3 L89.8,120.4 L90.6,117.8 L91.3,120.5 L92.1,126.7 L92.9,130.8 L93.6,127.6 L94.4,117.6 L95.2,106.3 L95.9,100.3 L96.7,102.3 L97.5,109.5 L98.3,116.7 L99.0,120.9 L99.8,122.7 L100.6,124.7 L101.3,127.8 L102.1,130.3 L102.9,129.9 L103.7,126.5 L104.4,123.6 L105.2,125.1 L106.0,131.5 L106.7,138.1 L107.5,138.7 L108.3,130.3 L109.1,116.4 L109.8,104.6 L110.6,101.3 L111.4,106.9 L112.1,115.9 L112.9,122.0 L113.7,122.9 L114.5,121.4 L115.2,122.2 L116.0,127.3 L116.8,134.1 L117.5,138.1 L118.3,137.1 L119.1,133.0 L119.9,129.9 L120.6,130.3 L121.4,132.9 L122.2,134.7 L122.9,134.2 L123.7,133.4 L124.5,135.3 L125.2,140.6 L126.0,145.4 L126.8,144.1 L127.6,134.0 L128.3,118.5 L129.1,105.5 L129.9,101.8 L130.6,108.2 L131.4,119.0 L132.2,126.8 L133.0,127.9 L133.7,124.8 L134.5,122.7 L135.3,124.9 L136.0,130.5 L136.8,135.5 L137.6,137.4 L138.4,137.1 L139.1,137.5 L139.9,140.3 L140.7,143.7 L141.4,144.1 L142.2,140.1 L143.0,134.2 L143.8,131.2 L144.5,133.9 L145.3,140.3 L146.1,145.2 L146.8,144.5 L147.6,139.5 L148.4,135.6 L149.2,137.9 L149.9,146.3 L150.7,154.9 L151.5,156.5 L152.2,147.9 L153.0,132.9 L153.8,118.7 L154.5,111.0 L155.3,110.5 L156.1,113.8 L156.9,117.2 L157.6,119.9 L158.4,123.7 L159.2,129.2 L159.9,134.7 L160.7,136.6 L161.5,133.5 L162.3,128.1 L163.0,125.6 L163.8,129.5 L164.6,138.3 L165.3,146.3 L166.1,148.3 L166.9,144.1 L167.7,138.7 L168.4,138.1 L169.2,143.9 L170.0,151.9 L170.7,155.7 L171.5,151.9 L172.3,143.2 L173.1,135.7 L173.8,134.3 L174.6,138.8 L175.4,144.9 L176.1,148.1 L176.9,147.6 L177.7,145.9 L178.5,145.7 L179.2,147.0 L180.0,147.6 L180.8,146.0 L181.5,143.8 L182.3,144.8 L183.1,151.2 L183.8,160.5 L184.6,166.1 L185.4,162.3 L186.2,148.7 L186.9,131.5 L187.7,118.9 L188.5,115.2 L189.2,118.4 L190.0,122.3 L190.8,122.7 L191.6,120.0 L192.3,118.6 L193.1,122.3 L193.9,130.4 L194.6,138.5 L195.4,142.2 L196.2,140.8 L197.0,137.3 L197.7,135.5 L198.5,136.1 L199.3,137.2 L200.0,136.4 L200.8,134.6 L201.6,135.1 L202.4,140.6 L203.1,149.9 L203.9,157.5 L204.7,158.1 L205.4,151.0 L206.2,141.7 L207.0,137.6 L207.7,142.5 L208.5,153.4 L209.3,162.9 L210.1,164.9 L210.8,159.2 L211.6,150.5 L212.4,144.5 L213.1,143.4 L213.9,144.8 L214.7,145.5 L215.5,144.7 L216.2,144.5 L217.0,147.3 L217.8,152.8 L218.5,157.3 L219.3,157.4 L220.1,153.1 L220.9,148.1 L221.6,147.0 L222.4,150.7 L223.2,155.5 L223.9,156.7 L224.7,152.8 L225.5,147.6 L226.3,147.3 L227.0,155.0 L227.8,167.2 L228.6,176.3 L229.3,175.7 L230.1,165.0 L230.9,149.7 L231.7,136.8 L232.4,129.9 L233.2,127.5 L234.0,126.1 L234.7,123.8 L235.5,122.1 L236.3,123.0 L237.0,126.5 L237.8,129.9 L238.6,130.1 L239.4,127.1 L240.1,124.9 L240.9,128.0 L241.7,137.0 L242.4,147.6 L243.2,153.3 L244.0,151.0 L244.8,143.4 L245.5,137.0 L246.3,136.7 L247.1,142.0 L247.8,147.4 L248.6,147.7 L249.4,142.3 L250.2,136.1 L250.9,134.7 L251.7,140.4 L252.5,150.1 L253.2,158.3 L254.0,161.5 L254.8,160.4 L255.6,158.2 L256.3,156.6 L257.1,154.9 L257.9,151.3 L258.6,146.4 L259.4,143.7 L260.2,147.4 L261.0,157.7 L261.7,169.7 L262.5,176.2 L263.3,173.0 L264.0,162.3 L264.8,151.3 L265.6,146.5 L266.3,148.9 L267.1,153.8 L267.9,155.5 L268.7,152.1 L269.4,146.7 L270.2,144.6 L271.0,148.3 L271.7,155.4 L272.5,161.0 L273.3,162.1 L274.1,160.0 L274.8,157.9 L275.6,158.2 L276.4,159.7 L277.1,159.4 L277.9,156.2 L278.7,152.4 L279.5,152.1 L280.2,156.7 L281.0,163.2 L281.8,166.0 L282.5,161.9 L283.3,153.4 L284.1,147.6 L284.9,150.5 L285.6,162.2 L286.4,176.7 L287.2,185.6 L287.9,184.7 L288.7,176.1 L289.5,165.5 L290.3,157.3 L291.0,151.6 L291.8,146.1 L292.6,138.8 L293.3,131.3 L294.1,126.9 L294.9,127.5 L295.6,131.0 L296.4,133.4 L297.2,132.0 L298.0,128.5 L298.7,126.9 L299.5,130.0 L300.3,136.0 L301.0,139.9 L301.8,138.0 L302.6,131.7 L303.4,126.9 L304.1,129.7 L304.9,140.6 L305.7,154.0 L306.4,162.4 L307.2,161.5 L308.0,153.9 L308.8,145.8 L309.5,142.4 L310.3,144.2 L311.1,147.8 L311.8,149.5 L312.6,148.9 L313.4,148.2 L314.2,149.1 L314.9,150.6 L315.7,149.9 L316.5,145.6 L317.2,140.3 L318.0,139.1 L318.8,145.3 L319.5,157.0 L320.3,167.9 L321.1,172.1 L321.9,168.6 L322.6,161.9 L323.4,158.3 L324.2,160.3 L324.9,164.6 L325.7,165.6 L326.5,160.2 L327.3,151.1 L328.0,144.7 L328.8,145.8 L329.6,154.3 L330.3,165.2 L331.1,173.3 L331.9,176.6 L332.7,176.6 L333.4,175.8 L334.2,174.2 L335.0,170.1 L335.7,162.4 L336.5,153.5 L337.3,148.3 L338.1,150.2 L338.8,157.7 L339.6,164.9 L340.4,165.7 L341.1,158.8 L341.9,149.4 L342.7,144.6 L343.5,148.3 L344.2,157.7 L345.0,166.3 L345.8,169.0 L346.5,166.1 L347.3,162.1 L348.1,161.5 L348.8,164.8 L349.6,168.6 L350.4,168.8 L351.2,165.2 L351.9,160.6 L352.7,158.7 L353.5,160.2 L354.2,162.5 L355.0,162.7 L355.8,160.8 L356.6,159.9 L357.3,163.1 L358.1,169.3 L358.9,173.8 L359.6,171.6 L360.4,162.4 L361.2,151.8 L362.0,147.7 L362.7,154.3 L363.5,168.9 L364.3,183.7 L365.0,191.6 L365.8,190.9 L366.6,185.4 L367.4,180.1 L368.1,176.9 L368.9,174.0 L369.7,168.2 L370.4,159.4 L371.2,150.5 L372.0,145.0 L372.8,143.3 L373.5,142.7 L374.3,139.9 L375.1,134.5 L375.8,129.9 L376.6,129.9 L377.4,135.2 L378.1,141.5 L378.9,143.3 L379.7,138.7 L380.5,131.2 L381.2,127.4 L382.0,131.3 L382.8,140.8 L383.5,149.2 L384.3,150.3 L385.1,143.7 L385.9,134.5 L386.6,129.5 L387.4,131.8 L388.2,139.3 L388.9,147.7 L389.7,153.9 L390.5,158.2 L391.3,162.3 L392.0,166.2 L392.8,167.4 L393.6,163.3 L394.3,154.5 L395.1,145.9 L395.9,142.8 L396.7,147.1 L397.4,155.0 L398.2,160.4 L399.0,159.2 L399.7,153.3 L400.5,148.7 L401.3,149.7 L402.1,155.7 L402.8,161.2 L403.6,160.6 L404.4,153.3 L405.1,144.2 L405.9,139.8 L406.7,143.2 L407.4,152.1 L408.2,161.3 L409.0,167.2 L409.8,169.9 L410.5,171.8 L411.3,174.1 L412.1,175.5 L412.8,173.4 L413.6,167.9 L414.4,162.4 L415.2,161.3 L415.9,166.0 L416.7,172.6 L417.5,174.7 L418.2,168.7 L419.0,156.9 L419.8,146.7 L420.6,144.8 L421.3,152.2 L422.1,163.8 L422.9,173.0 L423.6,176.4 L424.4,176.1 L425.2,176.6 L426.0,180.3 L426.7,185.2 L427.5,186.8 L428.3,182.8 L429.0,174.7 L429.8,167.0 L430.6,162.7 L431.4,161.4 L432.1,160.3 L432.9,157.8 L433.7,155.9 L434.4,157.7 L435.2,164.3 L436.0,172.2 L436.7,175.3 L437.5,169.9 L438.3,158.2 L439.1,147.5 L439.8,145.0 L440.6,152.2 L441.4,164.1 L442.1,173.1 L442.9,175.0 L443.7,171.3 L444.5,167.3 L445.2,167.0 L446.0,169.9"/>
<circle class="mark" cx="365.0" cy="191.6" r="3"/>
<text class="lbl ok" x="365.0" y="209.6" text-anchor="middle">minimum 2.56 at distance 406</text>
<text class="lbl ok" x="75.1" y="65.5" text-anchor="start">rises again from distance 6</text>
</svg>
<figcaption>The dot product between two positional encodings against their distance. It falls fast at short range, then oscillates from distance 6 onward. Of 511 steps, 244 go up rather than down; the minimum is at distance 406 and the curve climbs again after it.</figcaption>
</figure>

At short range it holds - `32.00, 30.92, 28.30, 25.59, 23.93, 23.50`. Then at
distance 6 it climbs back to `23.56`. Of the 511 steps, `244` go up rather than
down. The minimum is `2.56` at distance `406`, and by distance 511 the value has
risen again to `6.42`.

Which is what a sum of periodic functions does. It oscillates; it is not a
decaying function. What sinusoidal encoding buys is not "closer means more
alike" but **the fact of being a function of distance at all**. What that
function looks like against distance is a separate question, and as you can see,
it is not pretty.

## The real payoff: shifting is a linear map

The value of choosing periodic functions lies elsewhere. Fix any gap `k` and
there is a single fixed matrix `M_k`, **the same one for every position**, with
`PE(pos + k) = M_k · PE(pos)`. Not a different matrix per position - one.

Each frequency pair is `[sin(pos·w), cos(pos·w)]`, so shifting by `k` is a
rotation through the angle `k·w`, and a rotation matrix does not depend on `pos`.

Check it by measurement. Fitting 512 positions with 64 dimensions leaves
**eight times more equations than unknowns**, so this cannot come out right by
accident.

```
   k     sinusoidal    random embedding
   1        4.9e-14              0.504
   2        5.0e-14              0.489
   5        4.8e-14              0.548
  17        3.9e-14              0.501
  50        1.6e-13              0.549
```

The sinusoidal residual is floating-point noise; a random embedding of the same
size sits around `0.5` - a relative error of `0.898`, which is to say it fits
nothing at all.

The difference is practical. For attention to key on a relation like "three
places back", the `W` that builds `Q` and `K` has to be able to express it, and
what a `W` does is a linear transform. With sinusoids that relation **already
exists as a linear map**, so it only has to be found. Handing each position its
own arbitrary vector leaves no such map to find.

None of this makes learned positional embeddings unusable. They are widely used
and they learn a vector per position from data. The difference is that this
structure has to be **learned rather than had for free**.

## A bonus: beyond the trained length

A sinusoid is a formula, so it has a value at any position. Train on 512 and
position 4000 still has norm `5.6569`, and the dot product of 4000 with 4001 is
`30.917` - exactly the value for positions 0 and 1. A learned embedding has
nothing to hand back for a row that was never in its table.

Having a value and working well there are different things, of course. Models do
degrade past their trained length, which is why current ones reach for other
schemes such as rotary encodings. What sinusoids guarantee stops at "defined".

## It costs something

Not free. Position is **added**, and what it adds it also blurs. Adding
positional encoding to part eight's six tokens changes the first row like this.

```
              t0     t1     t2     t3     t4     t5
no position  0.510  0.030  0.015  0.389  0.039  0.016
with         0.610  0.213  0.020  0.140  0.012  0.004
```

`t0`'s topic partner is `t3`, and its share drops from `0.389` to `0.140`, while
the immediate neighbour `t1` climbs from `0.030` to `0.213`. **Position competes
with content.**

Position won here, and what settles that contest is the ratio between the
embedding's scale and the encoding's. Real models scale the embedding by
`sqrt(d)` before adding, which tunes exactly that ratio.

The goal is met all the same. Measure permutation equivariance again and it is
broken.

```python
Z  = X + PE(6, d)          # position added in the original order
Zp = X[perm] + PE(6, d)    # tokens shuffled, positions left where they are

np.allclose(att(X[perm]), att(X)[perm])    # no position:   True
np.allclose(att(Zp),      att(Z)[perm])    # with position: False
```

The point is that `PE` is **not** shuffled when building `Zp`. Shuffle the
positions along with the tokens and `att(Z[perm])` is equivariant again - carry
the seat number around with the passenger and nobody has changed seats.

## So

- To give attention order, each place must differ without later places growing
  **larger**. Writing positions in as raw integers makes their logit
  contribution `458` against content's `3.30` near position 100, burying the
  content and pinning the largest probability at `1.000`
- Sinusoids hold every position's norm at `5.6569` and make the dot product of
  two positions a function of distance alone, `Σ cos(distance·w)`. Absolute
  positions go in, relative position comes out
- That function does **not** decay monotonically with distance. 244 of 511 steps
  go up, and the minimum sits at distance 406
- The real payoff is that shifting is a fixed linear map: residual `5e-14`
  against `0.5` for a random embedding. It leaves relative position in a form a
  `W` merely has to find
- What is added also blurs. The topic partner's share falls from `0.389` to
  `0.140`

Nine parts. Next time the head gets split in several. If one attention produces
one weighted average, the next question is what several of them look at
separately - measured and drawn, as ever.
