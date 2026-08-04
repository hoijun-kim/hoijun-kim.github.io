---
title: "Stacking layers added nothing"
description: "Part eleven's open question - why 12 - measured across six configurations. Kernel 5 breaks at exactly 12 whether it has 4, 6 or 8 layers and whether its receptive-field bound is 16, 24 or 32. Both candidate explanations were wrong, and the only thing that extends the usable distance is a wider kernel."
date: 2026-01-24
lang: en
kind: guide
series:
  id: not-attention
  part: 12
---

Part eleven ended without an answer. A four-layer kernel-5 CNN has a receptive
field of `17`, so it reaches back to distance `16`, and it solves only to `12`.
Why four characters go unused was left open.

Two candidates were written down: **one layer's worth is missing from the bound**
(`bound - (k-1)`) and **it is a fixed fraction of the bound** (`0.75 x bound`).
At four layers and kernel 5 both give `12`, so telling them apart means changing
the depth.

Changing it settled the question. **Both are wrong, and what actually separates
the results is not the axis I was looking at.**

## Three bounds, each built two ways

At the same `637k` budget, kernel and depth are varied to put the bound at `16`,
`24` and `32`. Each bound gets one configuration that reached it **by stacking
layers** and one that reached it **by widening the kernel**.

```
config    kernel  layers   ch    params    bound   one-layer   75%
k5 x4        5       4    171   639,273     16        12       12
k3 x8        3       8    156   636,744     16        14       12
k5 x6        5       6    140   635,760     24        20       18
k3 x12       3      12    128   636,900     24        22       18
k5 x8        5       8    122   639,370     32        28       24
k9 x4        9       4    128   633,828     32        24       24
```

The task is the copy task from parts ten and eleven: `L` random characters, a
separator, the same `L` again. Every scored position reaches back exactly `L`, so
`L` is the distance. 1000 steps, two seeds, chance `ln(20) = 2.9957`.

Each distance needs its own training run, so the break was located by binary
search.

## The verdict rule was tightened

The first rule was that the **median** of the two seeds under `2.0` counts as
solved. Then `k5 x8` at distance `13` came out `0.0111` and `3.0004`. The median
is `1.51`, which passes, while what actually happened is that **one of the two
seeds solved it.**

The rule was tightened to **both seeds under `2.0`**. That invalidates the path
the binary search took, so every configuration was refilled one character at a
time from its farthest confirmed pass up to its nearest confirmed failure.

Two of the six had such a split: `k5 x8` at `13` and `k9 x4` at `22`. The
collapse is sharp, but there is **a one-character band where the seeds disagree.**

## Results

<figure class="fig">
<svg viewBox="0 0 460 424" role="img" aria-label="Above: the receptive-field bound of six configurations as horizontal bars, filled up to the distance actually solved. None reaches its bound, and the configurations that raised the bound by stacking layers keep the same filled length. Below: the same values against kernel width, where the three kernel-5 configurations land on one point even though their depths are 4, 6 and 8">
<text class="ttl2 l" x="22.0" y="18">receptive-field bound against the distance solved</text>
<text class="lbl" x="76.0" y="48.5" text-anchor="end">k3 x8</text>
<g class="alloc"><rect class="pad" x="84.0" y="40.0" width="142.0" height="11"/></g>
<g class="alloc"><rect class="use" x="84.0" y="40.0" width="62.1" height="11"/></g>
<text class="lbl ok" x="151.1" y="48.5">7</text>
<text class="lbl" x="252.0" y="48.5" text-anchor="end">16</text>
<text class="lbl" x="76.0" y="69.5" text-anchor="end">k3 x12</text>
<g class="alloc"><rect class="pad" x="84.0" y="61.0" width="213.0" height="11"/></g>
<g class="alloc"><rect class="use" x="84.0" y="61.0" width="71.0" height="11"/></g>
<text class="lbl ok" x="160.0" y="69.5">8</text>
<text class="lbl" x="323.0" y="69.5" text-anchor="end">24</text>
<text class="lbl" x="76.0" y="90.5" text-anchor="end">k5 x4</text>
<g class="alloc"><rect class="pad" x="84.0" y="82.0" width="142.0" height="11"/></g>
<g class="alloc"><rect class="use" x="84.0" y="82.0" width="106.5" height="11"/></g>
<text class="lbl ok" x="195.5" y="90.5">12</text>
<text class="lbl" x="252.0" y="90.5" text-anchor="end">16</text>
<text class="lbl" x="76.0" y="111.5" text-anchor="end">k5 x6</text>
<g class="alloc"><rect class="pad" x="84.0" y="103.0" width="213.0" height="11"/></g>
<g class="alloc"><rect class="use" x="84.0" y="103.0" width="106.5" height="11"/></g>
<text class="lbl ok" x="195.5" y="111.5">12</text>
<text class="lbl" x="323.0" y="111.5" text-anchor="end">24</text>
<text class="lbl" x="76.0" y="132.5" text-anchor="end">k5 x8</text>
<g class="alloc"><rect class="pad" x="84.0" y="124.0" width="284.0" height="11"/></g>
<g class="alloc"><rect class="use" x="84.0" y="124.0" width="106.5" height="11"/></g>
<text class="lbl ok" x="195.5" y="132.5">12</text>
<text class="lbl" x="394.0" y="132.5" text-anchor="end">32</text>
<text class="lbl" x="76.0" y="153.5" text-anchor="end">k9 x4</text>
<g class="alloc"><rect class="pad" x="84.0" y="145.0" width="284.0" height="11"/></g>
<g class="alloc"><rect class="use" x="84.0" y="145.0" width="186.4" height="11"/></g>
<text class="lbl ok" x="275.4" y="153.5">21</text>
<text class="lbl" x="394.0" y="153.5" text-anchor="end">32</text>
<g class="lbl-ax">
<text x="84.0" y="179">0</text>
<text x="155.0" y="179">8</text>
<text x="226.0" y="179">16</text>
<text x="297.0" y="179">24</text>
<text x="368.0" y="179">32</text>
<text class="cap l" x="84.0" y="194">copy distance in characters</text></g>
<g class="alloc"><rect class="use" x="88.0" y="204.0" width="9" height="9"/></g>
<text class="lbl" x="101.0" y="212.5">solved</text>
<g class="alloc"><rect class="pad" x="196.0" y="204.0" width="9" height="9"/></g>
<text class="lbl" x="209.0" y="212.5">bound</text>
<text class="ttl2 l" x="22.0" y="248">the same, against kernel width</text>
<g class="axis">
<line x1="84.0" y1="372.0" x2="300.0" y2="372.0"/>
<text class="tick-lbl" x="78.0" y="375.5" text-anchor="end">0</text>
<line x1="84.0" y1="337.3" x2="300.0" y2="337.3"/>
<text class="tick-lbl" x="78.0" y="340.8" text-anchor="end">8</text>
<line x1="84.0" y1="302.7" x2="300.0" y2="302.7"/>
<text class="tick-lbl" x="78.0" y="306.2" text-anchor="end">16</text>
<line x1="84.0" y1="268.0" x2="300.0" y2="268.0"/>
<text class="tick-lbl" x="78.0" y="271.5" text-anchor="end">24</text>
</g>
<circle class="dot" cx="111.0" cy="341.7" r="3.4"/>
<text class="lbl ok" x="118.0" y="345.2">7</text>
<circle class="dot" cx="111.0" cy="337.3" r="3.4"/>
<text class="lbl ok" x="118.0" y="333.2">8</text>
<circle class="dot" cx="165.0" cy="320.0" r="3.4"/>
<text class="lbl ok" x="172.0" y="323.5">12</text>
<circle class="dot" cx="273.0" cy="281.0" r="3.4"/>
<text class="lbl ok" x="280.0" y="284.5">21</text>
<g class="lbl-ax">
<text x="111.0" y="386">3</text>
<text class="cap" x="111.0" y="399">8·12</text>
<text x="165.0" y="386">5</text>
<text class="cap" x="165.0" y="399">4·6·8</text>
<text x="273.0" y="386">9</text>
<text class="cap" x="273.0" y="399">4</text>
<text class="cap l" x="84.0" y="415">kernel width, with the depths under it</text></g>
</svg>
<figcaption>Above: the receptive-field bound of six configurations as horizontal bars, filled up to the distance actually solved. None reaches its bound, and the ones that raised the bound by stacking layers keep the same filled length. Below: the same values against kernel width. The three kernel-5 configurations land on one point even though their depths are 4, 6 and 8.</figcaption>
</figure>

```
config    kernel  layers  bound   solved   fraction
k3 x8        3       8      16       7       0.44
k3 x12       3      12      24       8       0.33
k5 x4        5       4      16      12       0.75
k5 x6        5       6      24      12       0.50
k5 x8        5       8      32      12       0.38
k9 x4        9       4      32      21       0.66
```

## Layers buy nothing

Take the three kernel-5 configurations. Stacking `4`, `6` and `8` layers doubles
the bound from `16` to `32`.

**The distance solved is `12`, `12`, `12`.** It does not move by one character.

Kernel 3 is the same story. Going from `8` layers to `12` raises the bound from
`16` to `24` and moves the solved distance from `7` to `8`. Four extra layers
bought eight characters of bound and one character of use.

"Stack more layers if the receptive field is too small" is standard advice. On
this task it **raises the bound and leaves the usable distance where it was.**

## Kernels buy something

Sorted by kernel instead, the same numbers look different.

```
kernel   distance solved      layers
  3        7,  8              8, 12
  5       12, 12, 12          4, 6, 8
  9       21                  4
```

Kernel `3` to `5` moves it from `7.5` to `12`; kernel `5` to `9` moves it from
`12` to `21`. Both intervals come out at `2.25` characters per unit of kernel.

Depth ranges from `4` to `12` and the bound from `16` to `32`, and the points
still line up on the kernel axis.

But there are only three kernel values. `2.25` is a slope fitted to three points,
not a law. **The ordering and the independence from depth are measured; the
formula is not.**

## Nor is it channels

The budget is fixed, so stacking layers costs channels, which makes channel count
a genuine suspect. The numbers rule it out.

`k3 x8` has `156` channels and solves `7`; `k5 x6` has `140` channels and solves
`12`. **More channels, shorter reach.**

## The path count dies again here

Part eleven tried to explain the break by path count and was refuted. Here it
fails harder.

`k3 x8` has `6561` paths spread in a bell over distance. The peak is distance `8`
with `1107` of them; distance `7` has `1016`.

**Distance `7` is solved and distance `8` is not.** It breaks exactly at the
distance holding the most paths. If the path count set the ability, the peak
would be the easiest place there is.

## Not a step-count artifact

When a deeper configuration does worse, the first suspicion is that 1000 steps
were not enough to learn it. So the exact distance each one failed at was rerun
at 3000 steps.

```
config   distance   1000 steps        3000 steps
k5 x4       13        3.0009      2.9989  2.9977
k3 x8        8        3.0003      2.9985  2.9988
```

Both stay at chance with three times the steps. The break belongs to the architecture, not to the training budget.

## So what is it

Unknown.

What is ruled out has grown. Not the receptive-field bound (doubling it moves
nothing), not depth (eight layers is neither better nor worse than four), not the
path count (it breaks at the peak), not channels (more of them is shorter), not
the step count.

That leaves kernel width. Why kernel width should set the value is unexplained.

## What it means when you size one

The receptive-field formula gives you **the positions that are reachable.** Sizing
a stack by that number - "to capture a dependency at distance `d`, make the
receptive field at least `d`" - falls short on this task in six cases out of six.
The best is `0.75` of the bound and the worst is `0.33`.

And the shortfall **cannot be covered by adding layers.** Only a wider kernel
covers it, and at a fixed budget a wider kernel costs channels, so it is not free
either.

## What is left

This is one task. Copying needs exactly one position and that position is known
in advance. Whether the same numbers hold on a task like character prediction,
which uses many positions a little, was not measured. What part five measured on
language was loss, not usable distance.

There are three kernel values: `3`, `5`, `9`. Adding kernel `7` or `11` and
seeing whether `2.25` survives is what decides whether this can be stated as a
formula. Not done.

There are two seeds. Two of the six configurations had a distance where the seeds
disagreed, so the table says "both seeds succeed up to here", not "nothing past
here can ever work".

Dilation was left alone. Part five's dilated stack has a bound of `125` and solves
distance `60` (part eleven), which is `0.48` of its bound and so sits in the same
range as this table. Where it breaks cannot be measured, because the context is
`128` characters.

## So

- Six configurations at the same `637k` budget put the receptive-field bound at
  `16`, `24` and `32` by varying kernel and depth; the break was located by binary
  search over the copy distance
- **Kernel 5 solves `12` at `4`, `6` and `8` layers, with bounds of `16`, `24` and
  `32`.** The bound doubled and the usable distance did not move by one character
- Kernel 3 went from `7` to `8` when the depth went from `8` layers to `12`
- Both candidates from part eleven are wrong. "One layer short" predicted `14`,
  `20`, `22`, `28` against measurements of `7`, `12`, `8`, `12`; "75% of the
  bound" fares no better
- Sorted by kernel it is `3` → `7.5`, `5` → `12`, `9` → `21`, or `2.25`
  characters per unit of kernel. That is a slope fitted to three points, so it is
  not offered as a law
- Not channels - `k3 x8` has `156` and solves `7`, `k5 x6` has `140` and solves
  `12`
- Not the path count either - `k3 x8` breaks at distance `8`, which holds the most
  paths of any distance at `1107`, while distance `7` with `1016` is solved
- The verdict rule was tightened from the median of the seeds to **both seeds**,
  after `k5 x8` at distance `13` came out `0.0111` and `3.0004`
- Why kernel width sets it is unexplained
