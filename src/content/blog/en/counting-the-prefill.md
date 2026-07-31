---
title: "Counting the prefill turned 1.56x into 1.22x"
description: "Parts nine through eleven compared schedules by counting decode steps only. Add the cost of pushing the prompt in and continuous batching's advantage halves - because slots free one at a time, it splits prefill into 144 calls instead of 8."
date: 2025-11-07
lang: en
kind: guide
series:
  id: after-training
  part: 12
---

Part nine measured padding waste, part ten slot occupancy, part eleven cache
allocation. All three counted steps the same way: the requests are already there,
the cache is already full of prompt, and what gets counted is the walk that pulls
one character at a time.

The cost of pushing the prompt into the cache was never measured. Measured now, it
changes what those three parts concluded.

## Prefill is quadratic

Decode pushes one token at a time; prefill pushes the whole prompt at once, so
attention becomes `P x P` and the square of the length shows up. At batch 32:

```
prompt   prefill (us)   decode steps' worth
     8          2,461                  1.34
    16          3,836                  2.09
    32          6,205                  3.38
    64         13,728                  7.48
```

Fitting `t = a + b·P + c·P²` gives `a = 1,677 us`, `b = 101.0 us/token`,
`c = 1.3607 us/token²`. At `P = 64` the quadratic term is `40.6%` of the total.
Double the length and it costs more than double.

Part ten's requests had prompts between 8 and 64 and generated 37.6 characters on
average. One prefill is worth three or four decode steps, so in a thirty-seven
step request prefill looks like a tenth of the work. It looked ignorable.

## Continuous batching splits the prefill

What differs is how many calls the prefill gets split into.

Static batching starts a whole group at once, so it pushes 32 prompts in
together. Eight groups, eight prefills.

Continuous batching refills a seat the moment a request finishes. Seats free one
at a time, occasionally two.

```
                           prefills   group sizes
static                            8   32 x 8
continuous, as slots free       144   32x1  11x1  4x4  3x9  2x41
```

The same 256 prompts, split across `144` calls, average group `1.78`. Prefill's
`a = 1,677 us` is fixed whatever the row count, so paying it 144 times in twos
costs far more of it than paying it eight times in thirty-twos.

Timing prefill alone, continuous costs `2.011` times static (quartiles
`1.890~2.086`, winning all 21 rounds).

## So the table changes

Part ten reported continuous batching as `1.58` times faster than static. That
number counted decode only. Running the same traces end to end with prefill
included:

```
                          median   quartiles         of 21
decode only                1.560   1.472 ~ 1.689     21 won
with prefill included      1.218   1.154 ~ 1.283     20 won
```

<figure class="fig">
<svg viewBox="0 0 460 230" role="img" aria-label="Horizontal bars of total time split into prefill and decode. Continuous with k=1 splits prefill into 144 calls and its prefill share swells to 32%; admitting 8 at a time cuts that to 27 calls and gives the shortest total">
<text class="ttl2 l" x="20.0" y="16">Time to finish 256 requests, static batching as 1</text>
<g class="split"><rect class="pre" x="20.0" y="24" width="10" height="9"/><text class="lbl" x="34.0" y="32">prefill</text><rect class="dec" x="92.0" y="24" width="10" height="9"/><text class="lbl" x="106.0" y="32">decode</text><text class="lbl r" x="384.0" y="32" text-anchor="end">prefills</text></g>
<g class="split">
<text class="lbl r" x="84.0" y="53.0" text-anchor="end">static</text>
<rect class="dec" x="130.3" y="40.0" width="253.7" height="17.0"/>
<rect class="pre" x="92.0" y="40.0" width="38.3" height="17.0"/>
<text class="v on" x="111.1" y="52.0">13%</text>
<text class="lbl" x="390.0" y="53.0">8</text>
<text class="lbl r" x="84.0" y="77.0" text-anchor="end">cont k=1</text>
<rect class="dec" x="168.7" y="64.0" width="163.0" height="17.0"/>
<rect class="pre" x="92.0" y="64.0" width="76.7" height="17.0"/>
<text class="v on" x="130.4" y="76.0">32%</text>
<text class="lbl" x="337.7" y="77.0">144</text>
<text class="lbl r" x="84.0" y="101.0" text-anchor="end">cont k=2</text>
<rect class="dec" x="152.0" y="88.0" width="159.0" height="17.0"/>
<rect class="pre" x="92.0" y="88.0" width="60.0" height="17.0"/>
<text class="v on" x="122.0" y="100.0">27%</text>
<text class="lbl" x="317.1" y="101.0">88</text>
<text class="lbl r" x="84.0" y="125.0" text-anchor="end">cont k=4</text>
<rect class="dec" x="144.8" y="112.0" width="163.5" height="17.0"/>
<rect class="pre" x="92.0" y="112.0" width="52.8" height="17.0"/>
<text class="v on" x="118.4" y="124.0">24%</text>
<text class="lbl" x="314.3" y="125.0">48</text>
<text class="lbl r" x="84.0" y="149.0" text-anchor="end">cont k=8</text>
<rect class="dec" x="137.4" y="136.0" width="169.8" height="17.0"/>
<rect class="pre" x="92.0" y="136.0" width="45.4" height="17.0"/>
<text class="v on" x="114.7" y="148.0">21%</text>
<text class="lbl" x="313.2" y="149.0">27</text>
<text class="lbl r" x="84.0" y="173.0" text-anchor="end">cont k=16</text>
<rect class="dec" x="132.4" y="160.0" width="181.5" height="17.0"/>
<rect class="pre" x="92.0" y="160.0" width="40.4" height="17.0"/>
<text class="v on" x="112.2" y="172.0">18%</text>
<text class="lbl" x="319.9" y="173.0">15</text>
<text class="lbl r" x="84.0" y="197.0" text-anchor="end">cont k=32</text>
<rect class="dec" x="132.4" y="184.0" width="203.1" height="17.0"/>
<rect class="pre" x="92.0" y="184.0" width="40.4" height="17.0"/>
<text class="v on" x="112.2" y="196.0">17%</text>
<text class="lbl" x="341.5" y="197.0">8</text>
</g>
<g class="done"><line x1="279.2" y1="59.0" x2="279.2" y2="86.0"/><line x1="279.2" y1="212.0" x2="279.2" y2="221.0"/></g>
<text class="lbl bad" x="273.2" y="221.0" text-anchor="end">without prefill, here (1.56x)</text>
</svg>
<figcaption>Bar length is the time to finish 256 requests with static batching as 1. The dark segment is prefill and the number on the right is how many prefill calls it took. Admitting requests as slots free splits prefill into 144 calls and swells its share to 32%. The vertical rule marks where that bar ends with prefill excluded - the point part ten was looking at.</figcaption>
</figure>

`1.56` becomes `1.22`. More than half the advantage leaves through the prefill.
Prefill's share of the total is `13.1%` for static and `32.0%` for continuous.

Part ten's `1.58` is not wrong. Count decode steps and that is the answer. But
there was no prefill anywhere in that table, and I did not say so.

## Admitting in groups

The fix is visible. Instead of admitting the moment a seat frees, wait until `k`
requests have collected and admit them together, cutting the number of prefill
calls. The seat sits empty while you wait.

```
   k   prefills   mean group   decode steps   prefill share   vs static
   1        144         1.78            336           32.0%       1.218
   2         88         2.91            338           27.4%       1.333
   4         48         5.33            348           24.4%       1.350
   8         27         9.48            364           21.1%       1.357
  16         15        17.07            410           18.2%       1.316
  32          8        32.00            512           16.6%       1.199
```

An inverted U, best at `k = 8` with `1.357`, and worse at both ends.

Why `k = 1` is bad is the section above. Why `k = 32` is bad is in the decode
steps column: `512`, exactly static's. Waiting for 32 to collect means waiting
until every seat is empty, which is not doing continuous batching at all. It cuts
prefill to eight calls by importing back the seat waste part ten removed.

Raising `k` also lengthens the longest prompt in an admission group, `41.1` to
`62.8`. Part nine's padding is sitting in the prefill too.

## What is left

Here prefill and decode take turns, and decode stops while a prefill runs. One
long prompt arriving makes the thirty-one requests already running wait for it.
Cutting the prompt into chunks and slipping them between decode steps is the
answer to that, and it is unmeasured.

Prompt lengths are also uniform from 8 to 64. With the quadratic term already at
`40.6%` by `P = 64`, prompts in the hundreds or thousands would have prefill
swallow the whole picture and every ratio here would move.

And `k = 8` is optimal for this workload. Longer generations make the decode side
heavier, the number of prefill calls matters less, and the best `k` comes down.

## So

- Prefill is quadratic in prompt length. At `P = 64` the quadratic term is `40.6%`
- One prefill at batch 32 is worth `1.34` to `7.48` decode steps
- Static splits prefill into `8` calls, continuous into `144`, average group `1.78`
- So continuous's prefill costs `2.011` times static's
- Part ten's `1.58` counted decode only. With prefill it is `1.218`
- Prefill's share: `13.1%` static, `32.0%` continuous
- Admitting `k` at a time recovers it to `1.357` at `k = 8`. At `k = 32` the seat
  waste comes back and it falls to `1.199`
