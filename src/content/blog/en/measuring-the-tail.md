---
title: "Measuring the tail put part twelve's k=8 47% behind"
description: "Part twelve picked k=8 on throughput. Measured on inter-token p99, k=8 sits at 8.21ms against k=1's 5.57ms - 47% worse. Prefill chunking, which part twelve named and left alone, turns out to hold two of the six points on the frontier."
date: 2025-11-13
lang: en
kind: guide
series:
  id: after-training
  part: 13
---

Part twelve ranked schedules by the total time to finish 256 requests, and
concluded that admitting `k` at a time is best at `k = 8`.

Total time is throughput. It is not what the person who sent one request
experiences. What they see is how evenly their own characters arrive, and part
twelve's table has nothing about that in it.

## Between one character and the next

Measure how long an already-running request waits for its next character. One
decode step hands a character to every live request, so **the time from one
decode to the decode before it** is that wait. A prefill landing in between
stretches it.

The first measurement made every schedule look identical - maxima all between 3.5
and 4.5 ms. The code was measuring from the **previous operation**, so a decode
right after a prefill got timed from the moment the prefill ended, and the
prefill's cost fell straight out of the number. Which was the one thing being
measured.

## Median and tail move in opposite directions

Fixed and re-measured:

```
             prefills  decodes     p50    p99   p99 quartiles   throughput
static              8      512    1.14  14.06   13.45~14.84        1.000
continuous k=1    144      336    1.76   5.57    5.41~ 6.88        1.207
continuous k=2     88      338    1.38   6.16    5.95~ 7.49        1.263
continuous k=4     48      348    1.17   6.99    6.34~ 7.91        1.318
continuous k=8     27      364    1.13   8.21    7.51~11.30        1.392
continuous k=16    15      410    1.13  10.78    9.83~12.07        1.273
continuous k=32     8      512    0.90  14.06   13.14~15.48        1.202
```

Raising `k` takes `p50` from `1.76` down to `0.90` and `p99` from `5.57` up to
`14.06`. One knob, two numbers, opposite directions.

The reason is all in part twelve. Small `k` prefills often but each one is small;
large `k` prefills rarely but each one is large. Doing it often delays every step
a little, which ruins the median; doing it rarely leaves most steps clean and
stops hard occasionally.

**Part twelve's `k = 8` has a `p99` of `8.21` against `k = 1`'s `5.57`, 47%
worse.** The quartile ranges do not even overlap - `7.51~11.30` against
`5.41~6.88`. Throughput goes the other way, `1.392` against `1.207`. Part twelve
was not wrong; on the axis it was looking at, that was the answer.

## Chunking the prefill

Part twelve named this and left it. Instead of pushing the whole prompt in at
once, push `c` tokens at a time and slip a decode step between the chunks, so the
stall is one chunk rather than the whole prefill.

Varying the chunk size at `k = 8`:

```
            prefills  decodes     p50    p99   p99 quartiles   throughput
monolithic        27      364    1.13   8.21    7.51~11.30          1.392
chunk 32          55      373    1.23   6.88    6.19~ 7.32          1.250
chunk 16         108      390    1.30   5.86    5.39~ 7.23          1.120
chunk 8          208      421    1.96   5.50    5.02~ 7.22          0.933
```

The tail falls from `8.21` to `5.50` and throughput falls from `1.392` to
`0.933`. At chunk 8 it is slower than static batching.

## Where chunking does nothing at all

At `k = 32` the same move runs backwards.

```
            prefills  decodes     p99   p99 quartiles   throughput
monolithic         8      512   14.06   13.14~15.48          1.202
chunk 32          16      512   14.41   13.71~16.83          1.217
chunk 16          32      512   17.83   17.46~19.34          1.147
chunk 8           64      512   24.81   22.39~26.75          1.044
```

The decode count is stuck at `512`. `k = 32` waits until **every** seat is empty
before refilling, so nothing is alive while its prefill runs. There is no decode
to slip between the chunks, so chunking only splits the prefill into more calls
and pays the fixed overhead again for each, and all of it piles into the one gap:
`p99` goes from `14.06` to `24.81`.

**Chunking pays only when there is something to run between the chunks.**

## The frontier

Both knobs on one plot.

<figure class="fig">
<svg viewBox="0 0 460 300" role="img" aria-label="Throughput against inter-token p99. With monolithic prefill, raising k from 1 to 32 peaks throughput at 8 while p99 keeps getting worse. Chunking the prefill lowers p99 and lowers throughput with it">
<g class="axis">
<line x1="74.0" y1="268.0" x2="440.0" y2="268.0"/>
<text class="tick-lbl" x="68.0" y="271.5" text-anchor="end">5</text>
<line x1="74.0" y1="204.7" x2="440.0" y2="204.7"/>
<text class="tick-lbl" x="68.0" y="208.2" text-anchor="end">8</text>
<line x1="74.0" y1="150.1" x2="440.0" y2="150.1"/>
<text class="tick-lbl" x="68.0" y="153.6" text-anchor="end">12</text>
<line x1="74.0" y1="81.3" x2="440.0" y2="81.3"/>
<text class="tick-lbl" x="68.0" y="84.8" text-anchor="end">20</text>
</g><g class="lbl-ax">
<text x="85.4" y="284">0.8</text>
<text x="142.6" y="284">0.9</text>
<text x="199.8" y="284">1.0</text>
<text x="257.0" y="284">1.1</text>
<text x="314.2" y="284">1.2</text>
<text x="371.4" y="284">1.3</text>
<text x="428.6" y="284">1.4</text>
<text class="cap l" x="74.0" y="299">throughput (static = 1)</text></g>
<g class="row-lbl"><text x="34.0" y="157" transform="rotate(-90 34.0 157)">inter-token p99 (ms)</text></g>
<g class="hop c"><path d="M388,262 L426,262" marker-end="url(#ah13)"/></g><text class="lbl" x="384" y="266" text-anchor="end">better</text>
<path class="branch" d="M318.2,253.5 L251.9,255.7 L164.4,246.9 L113.5,260.4" fill="none"/>
<rect class="chunk" x="249.3" y="253.1" width="5.2" height="5.2"/>
<rect class="chunk" x="161.8" y="244.3" width="5.2" height="5.2"/>
<rect class="chunk" x="110.9" y="257.8" width="5.2" height="5.2"/>
<text class="lbl" x="113.5" y="273.4" text-anchor="middle">8</text>
<path class="branch" d="M424.0,201.2 L342.8,225.0 L268.4,246.6 L161.5,255.2" fill="none"/>
<rect class="chunk" x="340.2" y="222.4" width="5.2" height="5.2"/>
<rect class="chunk" x="265.8" y="244.0" width="5.2" height="5.2"/>
<rect class="chunk" x="158.9" y="252.6" width="5.2" height="5.2"/>
<text class="lbl" x="161.5" y="268.2" text-anchor="middle">8</text>
<path class="branch" d="M315.3,128.8 L323.9,125.5 L283.9,96.8 L225.0,52.3" fill="none"/>
<rect class="chunk" x="321.3" y="122.9" width="5.2" height="5.2"/>
<rect class="chunk" x="281.3" y="94.2" width="5.2" height="5.2"/>
<rect class="chunk" x="222.4" y="49.7" width="5.2" height="5.2"/>
<text class="lbl" x="225.0" y="65.3" text-anchor="middle">8</text>
<path class="curve ok" d="M318.2,253.5 L350.2,239.9 L381.7,222.9 L424.0,201.2 L355.9,164.6 L315.3,128.8" fill="none"/>
<circle class="dot" cx="318.2" cy="253.5" r="3.4"/>
<text class="lbl ok" x="311.2" y="257.0" text-anchor="end">k=1</text>
<circle class="dot" cx="350.2" cy="239.9" r="3.4"/>
<text class="lbl ok" x="343.2" y="243.4" text-anchor="end">k=2</text>
<circle class="dot" cx="381.7" cy="222.9" r="3.4"/>
<text class="lbl ok" x="374.7" y="226.4" text-anchor="end">k=4</text>
<circle class="dot" cx="424.0" cy="201.2" r="3.4"/>
<text class="lbl ok" x="432.0" y="204.7" text-anchor="start">k=8</text>
<circle class="dot" cx="355.9" cy="164.6" r="3.4"/>
<text class="lbl ok" x="363.9" y="168.1" text-anchor="start">k=16</text>
<circle class="dot" cx="315.3" cy="128.8" r="3.4"/>
<text class="lbl ok" x="308.3" y="132.3" text-anchor="end">k=32</text>
<circle class="dot bad" cx="199.8" cy="128.8" r="3.4"/>
<text class="lbl bad" x="206.8" y="132.3">static</text>
<g class="lgd"><circle class="dot" cx="78.0" cy="28.0" r="3.4"/><text class="lbl ok" x="86.0" y="32.0">monolithic prefill, varying k</text><rect class="chunk" x="437.4" y="25.4" width="5.2" height="5.2"/><text class="lbl" x="430.0" y="32.0" text-anchor="end">prefill chunking</text></g>
<defs><marker id="ah13" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,1 L7,4 L0,7 z" class="ahd"/></marker></defs>
</svg>
<figcaption>Throughput across, inter-token p99 up. Down and to the right is better. With monolithic prefill, varying only k peaks throughput at k=8, and lowering k from there gives back a little throughput for a shorter tail. Chunking the prefill (squares) drops the tail further and drops throughput with it. Only the k=32 branch goes the wrong way: every seat is empty during its prefill, so there is no decode to slip between the chunks.</figcaption>
</figure>

Six points are not dominated.

```
k=8              throughput 1.392   p99  8.21
k=4              throughput 1.318   p99  6.99
k=2              throughput 1.263   p99  6.16
k=1              throughput 1.207   p99  5.57
k=1 chunk 32     throughput 1.091   p99  5.48
k=1 chunk 8      throughput 0.849   p99  5.29
```

Four monolithic, two chunked. From `p99` `8.21` down to `5.57` - most of the
usable range - `k` alone covers it, with no room for chunking in between.
Chunking appears on the frontier only below `5.57`, and getting from there to
`5.29`, a further `0.28ms`, costs 30% of throughput, `1.207` down to `0.849`.

On this workload chunking is mostly not worth buying, and the reason is that the
prompts are short. The longest here is 64 characters, and one monolithic prefill
is worth only a handful of decode steps - `1.34` to `7.48` of them, from part
twelve. There is not much to gain by splitting a lump that was never large.

## What is left

At prompts of thousands the story changes. One monolithic prefill becomes worth
hundreds of decode steps and sets `p99` by itself. Lowering `k` cannot touch it
because the prefill is large regardless, and chunking becomes the only handle
there is. This model's context is 128 characters, so that regime cannot be built
here.

Maxima are left out of the tables. Decode counts range from `336` to `512` across
configurations, so the sample counts differ, and a maximum grows with the number
of samples. Quantiles are far less sensitive to it.

And here all 256 requests arrive at once. Real arrivals are spread out, which
leaves idle seats and stretches where a prefill is close to free. That case is
unmeasured.

## So

- One `k` knob pushes `p50` and `p99` opposite ways: `p50` improves `1.76` to
  `0.90`, `p99` degrades `5.57` to `14.06`
- Part twelve's `k = 8` is 47% worse than `k = 1` on `p99`, with no quartile
  overlap
- Chunking takes `k = 8`'s tail from `8.21` to `5.50` and its throughput from
  `1.392` to `0.933`
- At `k = 32` chunking **raises** the tail, `14.06` to `24.81`. With nothing to
  run between chunks, only the overhead grows
- Four of the six frontier points are monolithic. Chunking shows up only below
  `p99` `5.57`, where `0.28ms` costs 30% of throughput
- Short prompts leave no lump worth splitting
