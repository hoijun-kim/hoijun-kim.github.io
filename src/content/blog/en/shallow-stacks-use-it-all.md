---
title: "Shallow stacks use the whole bound"
description: "Part twelve found that raising the receptive-field bound does not raise the distance a CNN can use. Cut the depth to two or three layers and the whole bound gets used, with nothing left over. And matching the depth at four exposes an error: part twelve's line put depth-mixed points on a kernel axis, and kernel 3 sits 1.5 characters below it."
date: 2026-01-30
lang: en
kind: guide
series:
  id: not-attention
  part: 13
---

Part twelve left two things. Whether the `2.25` slope on the kernel axis is a
formula - there were only three kernel values, so it was not offered as a law -
and where the ceiling starts biting.

Both are measurable. Adding kernels `7` and `11` settles the first; cutting the
depth to two or three layers settles the second.

Four predictions were written down before measuring.

```
config      bound   prediction   reasoning
k5 x2           8            8   the bound is under the ceiling of 12, so all of it
k5 x3          12           12   same, with the bound equal to the ceiling
k7 x4          24           16   2.25 x 7 = 15.75
k11 x4         40           25   2.25 x 11 = 24.75
```

## The shallow end and the wide end

All at the same `637k` budget.

```
config    kernel  layers   ch    params    bound
k3 x2         3       2   303   635,565       4
k3 x3         3       3   250   635,400       6
k3 x4         3       4   218   636,162       8
k5 x2         5       2   238   635,746       8
k5 x3         5       3   196   636,180      12
k7 x4         7       4   145   636,835      24
k11 x4       11       4   116   633,152      40
```

The task and the protocol are part twelve's. The copy distance is swept for the
break, and a distance counts as solved only when **both seeds** land under `2.0`.
For the small bounds, walking up one character at a time is cheaper than binary
search, so that is what was done.

## Results

<figure class="fig">
<svg viewBox="0 0 460 432" role="img" aria-label="Above: the receptive-field bound and the distance actually solved for thirteen configurations. The diagonal is where the whole bound gets used. Stacks of two or three layers sit on it; deeper ones flatten at a height that depends on the kernel, 12 for kernel 5 and 6 to 8 for kernel 3. Below: only the five configurations at a matched depth of four, against kernel width. The line drawn in part twelve lands within half a character for kernels 5, 7, 9 and 11 and sits 1.5 above kernel 3">
<text class="ttl2 l" x="22.0" y="18">receptive-field bound against the distance solved</text>
<g class="axis">
<line x1="74.0" y1="196.0" x2="400.0" y2="196.0"/>
<text class="tick-lbl" x="68.0" y="199.5" text-anchor="end">0</text>
<line x1="74.0" y1="149.8" x2="400.0" y2="149.8"/>
<text class="tick-lbl" x="68.0" y="153.3" text-anchor="end">8</text>
<line x1="74.0" y1="103.6" x2="400.0" y2="103.6"/>
<text class="tick-lbl" x="68.0" y="107.1" text-anchor="end">16</text>
<line x1="74.0" y1="57.3" x2="400.0" y2="57.3"/>
<text class="tick-lbl" x="68.0" y="60.8" text-anchor="end">24</text>
</g>
<line class="ref" x1="74.0" y1="196.0" x2="283.6" y2="40.0"/>
<text class="lbl bad" x="287.6" y="43.0">using the whole bound</text>
<path class="curve bad" d="M105.0,172.9 L120.6,161.3 L136.1,161.3 L198.2,155.6 L260.3,149.8" fill="none"/>
<circle class="dot" cx="105.0" cy="172.9" r="2.8"/>
<circle class="dot" cx="120.6" cy="161.3" r="2.8"/>
<circle class="dot" cx="136.1" cy="161.3" r="2.8"/>
<circle class="dot" cx="198.2" cy="155.6" r="2.8"/>
<circle class="dot" cx="260.3" cy="149.8" r="2.8"/>
<text class="lbl" x="267.3" y="153.3">kernel 3</text>
<path class="curve ok" d="M136.1,149.8 L167.1,132.4 L198.2,126.7 L260.3,126.7 L322.4,126.7" fill="none"/>
<circle class="dot" cx="136.1" cy="149.8" r="2.8"/>
<circle class="dot" cx="167.1" cy="132.4" r="2.8"/>
<circle class="dot" cx="198.2" cy="126.7" r="2.8"/>
<circle class="dot" cx="260.3" cy="126.7" r="2.8"/>
<circle class="dot" cx="322.4" cy="126.7" r="2.8"/>
<text class="lbl" x="329.4" y="130.2">kernel 5</text>
<circle class="dot" cx="260.3" cy="97.8" r="2.8"/>
<text class="lbl" x="267.3" y="101.3">kernel 7</text>
<circle class="dot" cx="322.4" cy="74.7" r="2.8"/>
<text class="lbl" x="329.4" y="78.2">kernel 9</text>
<circle class="dot" cx="384.5" cy="51.6" r="2.8"/>
<text class="lbl" x="391.5" y="55.1">kernel 11</text>
<g class="lbl-ax">
<text x="74.0" y="210">0</text>
<text x="136.1" y="210">8</text>
<text x="198.2" y="210">16</text>
<text x="260.3" y="210">24</text>
<text x="322.4" y="210">32</text>
<text x="384.5" y="210">40</text>
<text class="cap l" x="74.0" y="225">receptive-field bound in characters</text></g>
<text class="ttl2 l" x="22.0" y="258">at a matched depth of four layers</text>
<g class="axis">
<line x1="74.0" y1="386.0" x2="300.0" y2="386.0"/>
<text class="tick-lbl" x="68.0" y="389.5" text-anchor="end">0</text>
<line x1="74.0" y1="354.0" x2="300.0" y2="354.0"/>
<text class="tick-lbl" x="68.0" y="357.5" text-anchor="end">8</text>
<line x1="74.0" y1="322.0" x2="300.0" y2="322.0"/>
<text class="tick-lbl" x="68.0" y="325.5" text-anchor="end">16</text>
<line x1="74.0" y1="290.0" x2="300.0" y2="290.0"/>
<text class="tick-lbl" x="68.0" y="293.5" text-anchor="end">24</text>
</g>
<line class="ref" x1="87.6" y1="359.6" x2="291.0" y2="278.6" stroke-dasharray="3 2"/>
<text class="lbl" x="286.4" y="379.6" text-anchor="end">part twelve's line</text>
<circle class="dot" cx="96.6" cy="362.0" r="3.4"/>
<text class="lbl ok" x="103.6" y="365.5">6</text>
<circle class="dot" cx="141.8" cy="338.0" r="3.4"/>
<text class="lbl ok" x="148.8" y="341.5">12</text>
<circle class="dot" cx="187.0" cy="318.0" r="3.4"/>
<text class="lbl ok" x="194.0" y="321.5">17</text>
<circle class="dot" cx="232.2" cy="302.0" r="3.4"/>
<text class="lbl ok" x="239.2" y="305.5">21</text>
<circle class="dot" cx="277.4" cy="286.0" r="3.4"/>
<text class="lbl ok" x="284.4" y="289.5">25</text>
<g class="lbl-ax">
<text x="96.6" y="400">3</text>
<text x="141.8" y="400">5</text>
<text x="187.0" y="400">7</text>
<text x="232.2" y="400">9</text>
<text x="277.4" y="400">11</text>
<text class="cap l" x="74.0" y="415">kernel width</text></g>
</svg>
<figcaption>Above: the receptive-field bound and the distance actually solved, for thirteen configurations. The dashed diagonal is where the whole bound gets used; the two- and three-layer stacks sit on it, and deeper ones flatten at a height set by the kernel. Below: only the five configurations at a matched depth of four, against kernel width. Part twelve's line lands within half a character for kernels 5, 7, 9 and 11 and sits 1.5 above kernel 3.</figcaption>
</figure>

With part twelve's configurations that makes thirteen.

```
config    kernel  layers  bound   solved   fraction
k3 x2         3       2      4        4      1.00
k3 x3         3       3      6        6      1.00
k3 x4         3       4      8        6      0.75
k3 x8         3       8     16        7      0.44
k3 x12        3      12     24        8      0.33
k5 x2         5       2      8        8      1.00
k5 x3         5       3     12       11      0.92
k5 x4         5       4     16       12      0.75
k5 x6         5       6     24       12      0.50
k5 x8         5       8     32       12      0.38
k7 x4         7       4     24       17      0.71
k9 x4         9       4     32       21      0.66
k11 x4       11       4     40       25      0.62
```

## Shallow means the bound is everything

`k3 x2` solves `4` on a bound of `4`, `k3 x3` solves `6` on `6`, and `k5 x2`
solves `8` on `8`. **Nothing is left over.**

Part twelve ended on "raising the bound does not raise the usable distance", and
that was measured from a bound of `16` upward. Below it, the bound is the answer.

Only `k5 x3` leaves one character, solving `11` on a bound of `12`. That is the
place where the bound and the ceiling coincide, so this single configuration
cannot say which one it hit.

## The elbow

Lined up per kernel, there is one shape.

```
kernel 5   layers  2    3    4    6    8
           bound   8   12   16   24   32
           solved  8   11   12   12   12

kernel 3   layers  2    3    4    8   12
           bound   4    6    8   16   24
           solved  4    6    6    7    8
```

It climbs along the bound and then flattens. Kernel 5 flattens at `12` and is
already there at four layers - **four layers and eight layers give the same
thing.** Kernel 3 flattens around `6`, but not completely: from four layers to
twelve it still gains two characters, `6`, `7`, `8`.

## Kernels 7 and 11

`k7 x4` solves `17` and `k11 x4` solves `25`. Part twelve's line `2.25k + 0.75`
gives `16.5` and `25.5`, so both land within one character of an integer
measurement.

`k11` was an extrapolation. Part twelve had kernels `3`, `5` and `9`, and `11` is
outside that range. **It held outside the range too.**

The predictions written above said `16` and `25`, which come from `2.25k` with
the intercept of `0.75` dropped. The line gives `16.5` and the measurement is
`17`. The line was right and my arithmetic was not.

## Correcting part twelve's line

Matching the depth at `4` and looking again, one point does not fit.

```
kernel (all four layers)   solved   part twelve's line
        3                       6                 7.50
        5                      12                12.00
        7                      17                16.50
        9                      21                21.00
       11                      25                25.50
```

Kernel `3` is off by `1.5` characters. The other four are within half.

The reason is that part twelve used `7` and `8` as kernel 3's values, and those
come from **eight-layer and twelve-layer** stacks. Kernel 5 reached `12` at four,
six and eight layers, so it does not depend on depth; kernel 3 does, and putting
its deep values on a kernel axis lifts them.

At a matched depth, kernel 3 is `6`. Part twelve's lower panel **placed
depth-mixed points on a kernel axis.** The `2.25` slope survives for kernel `5`
and above, but putting kernel `3` on that line was wrong.

## How the predictions did

```
config      predicted   solved   result
k3 x2               4        4    right
k3 x3               6        6    right
k5 x2               8        8    right
k5 x3              12       11    one short
k11 x4             25       25    right
k7 x4              16       17    one off (dropped intercept)
k3 x4             7~8        6    two off
```

The three "the whole bound gets used" predictions were all right. The three that
missed are all **near the ceiling** - where exactly the ceiling falls still cannot
be called to within one character.

## When you size one

One more line joins what parts eleven and twelve gave.

- If the distance you need is **small**, size the stack by the formula. Bounds of
  `4`, `6` and `8` deliver their bound
- If the distance is past that kernel's ceiling, **more layers will not get you
  there.** Kernel 5 gives `12` at four layers and `12` at eight
- Getting past it means a wider kernel: `5` → `12`, `7` → `17`, `9` → `21`,
  `11` → `25`. At a fixed budget that cuts the channels from `171` to `116`

## What is left

`k5 x3` solving `11` on a bound of `12` was not resolved. There is no other way to
build a bound of `12` with kernel 5 (three layers is the only one), so this single
configuration cannot separate the bound from the ceiling.

Kernel 3's ceiling was not reached. At `4`, `8` and `12` layers it gives `6`, `7`
and `8`, still climbing. Going to `20` or `30` layers would show where it stops,
but at a fixed budget the channels keep shrinking, so at that point channels
become a candidate cause.

There are still two seeds. Three of the thirteen had a distance where the seeds
disagreed: `k5 x8` at `13`, `k9 x4` at `22`, and `k11 x4` at `26` (`0.0041` and
`3.0002`).

This is one task. The caveats from parts eleven and twelve carry over unchanged.

## So

- Configurations cut to `2` and `3` layers, plus kernels `7` and `11`, all at the
  same `637k` budget, extend part twelve's table to thirteen
- **Shallow means the whole bound is used.** `k3 x2` is `4/4`, `k3 x3` is `6/6`,
  `k5 x2` is `8/8`. Part twelve's "the bound buys nothing" was measured from a
  bound of `16` upward
- Kernel 5 climbs `8`, `11`, `12` along the bound and then flattens at `12`.
  **Four layers is already all of it, and eight gives the same**
- Kernel 3 goes `4`, `6`, `6`, `7`, `8` - it flattens more slowly, gaining two
  characters between four layers and twelve
- `k7 x4` solves `17` and `k11 x4` solves `25`; part twelve's line gives `16.5`
  and `25.5`, both within one character, and `11` was outside its fitted range
- **Kernel 3's point on part twelve's line is corrected.** Part twelve put the
  eight- and twelve-layer values `7` and `8` on the kernel axis; at a matched
  depth of four it is `6`, which is `1.5` below the line
- Of seven predictions, four were right, two were off by one and one by two. All
  the misses are near the ceiling
