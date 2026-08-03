---
title: "Where it starts failing"
description: "Five architectures run under one protocol with the copy distance swept from 2 to 60. The RNN breaks between 4 and 8, the LSTM between 8 and 16. The CNN has a receptive field of 17 but only solves up to distance 12, and my explanation for why was refuted as soon as I set it up."
date: 2026-01-18
lang: en
kind: guide
series:
  id: not-attention
  part: 11
---

Part ten built the copy task and then left two things unmeasured: dropping the
copy length to see where recurrence starts succeeding, and running part five's
receptive-field-`125` CNN on the task.

Both are done here. And the prediction I wrote down before measuring was wrong -
then the explanation I built for why it was wrong got refuted too.

## Only the distance changes

The task is part ten's. Draw `L` characters at random from a 20-character
alphabet, add a separator, then write the same `L` characters again. Only the
second copy is scored.

In this task **every scored position reaches back exactly `L`.** Output position
`L + j` has to produce the `j`-th character, which sits at input position `j`.
The distance is `(L + j) - j = L`, independent of `j`. So changing `L` **is**
changing the reach-back distance.

`L` was set to `4`, `8`, `16`, `32` and `60`, and each of the five architectures
was run at two seeds: 1000 steps, validation every 100, the loss at the best
point. Chance is `ln(20) = 2.9957`.

<figure class="fig">
<svg viewBox="0 0 460 344" role="img" aria-label="Above: validation loss with the copy distance from 4 to 60. The RNN climbs to chance between 4 and 8 and the CNN between 12 and 13, while the transformer stays on the floor regardless. Below: the same CNN's path count per distance as bars, coloured by whether it actually solved that distance. The reach limit is 16 but it only solves up to 12. The bars are symmetric, so distances 3 and 13, or 2 and 14, have equal path counts and only the near one is solved">
<text class="ttl2 l" x="24.0" y="18">best validation loss against copy distance</text>
<g class="axis">
<line x1="74.0" y1="172.0" x2="386.0" y2="172.0"/>
<text class="tick-lbl" x="68.0" y="175.5" text-anchor="end">0</text>
<line x1="74.0" y1="132.6" x2="386.0" y2="132.6"/>
<text class="tick-lbl" x="68.0" y="136.1" text-anchor="end">1</text>
<line x1="74.0" y1="93.2" x2="386.0" y2="93.2"/>
<text class="tick-lbl" x="68.0" y="96.7" text-anchor="end">2</text>
<line x1="74.0" y1="53.8" x2="386.0" y2="53.8"/>
<text class="tick-lbl" x="68.0" y="57.3" text-anchor="end">3</text>
</g>
<line class="ref" x1="74.0" y1="54.0" x2="386.0" y2="54.0"/>
<text class="lbl bad" x="78.0" y="49.0">chance 2.9957</text>
<path class="curve ok" d="M90.8,171.9 L162.3,171.9 L233.8,171.9 L305.3,171.9 L370.1,171.9" fill="none"/>
<circle class="dot" cx="90.8" cy="171.9" r="2.6"/>
<circle class="dot" cx="162.3" cy="171.9" r="2.6"/>
<circle class="dot" cx="233.8" cy="171.9" r="2.6"/>
<circle class="dot" cx="305.3" cy="171.9" r="2.6"/>
<circle class="dot" cx="370.1" cy="171.9" r="2.6"/>
<path class="curve ok2" d="M90.8,171.9 L162.3,166.1 L233.8,139.2 L305.3,104.7 L370.1,80.0" fill="none"/>
<circle class="dot" cx="90.8" cy="171.9" r="2.6"/>
<circle class="dot" cx="162.3" cy="166.1" r="2.6"/>
<circle class="dot" cx="233.8" cy="139.2" r="2.6"/>
<circle class="dot" cx="305.3" cy="104.7" r="2.6"/>
<circle class="dot" cx="370.1" cy="80.0" r="2.6"/>
<path class="curve ok3" d="M90.8,171.8 L162.3,166.4 L233.8,80.7 L305.3,53.9 L370.1,53.9" fill="none"/>
<circle class="dot" cx="90.8" cy="171.8" r="2.6"/>
<circle class="dot" cx="162.3" cy="166.4" r="2.6"/>
<circle class="dot" cx="233.8" cy="80.7" r="2.6"/>
<circle class="dot" cx="305.3" cy="53.9" r="2.6"/>
<circle class="dot" cx="370.1" cy="53.9" r="2.6"/>
<path class="curve bad" d="M90.8,172.0 L162.3,53.7 L233.8,53.7 L305.3,53.9 L370.1,53.9" fill="none"/>
<circle class="dot" cx="90.8" cy="172.0" r="2.6"/>
<circle class="dot" cx="162.3" cy="53.7" r="2.6"/>
<circle class="dot" cx="233.8" cy="53.7" r="2.6"/>
<circle class="dot" cx="305.3" cy="53.9" r="2.6"/>
<circle class="dot" cx="370.1" cy="53.9" r="2.6"/>
<path class="curve bad2" d="M90.8,172.0 L162.3,172.0 L233.8,53.8 L305.3,53.9 L370.1,53.9" fill="none"/>
<circle class="dot" cx="90.8" cy="172.0" r="2.6"/>
<circle class="dot" cx="162.3" cy="172.0" r="2.6"/>
<circle class="dot" cx="233.8" cy="53.8" r="2.6"/>
<circle class="dot" cx="305.3" cy="53.9" r="2.6"/>
<circle class="dot" cx="370.1" cy="53.9" r="2.6"/>
<text class="lbl" x="392.0" y="57.4">CNN</text>
<text class="lbl" x="392.0" y="70.4">RNN</text>
<text class="lbl" x="392.0" y="83.4">LSTM</text>
<text class="lbl" x="392.0" y="96.4">GRU</text>
<text class="lbl" x="392.0" y="175.4">transformer</text>
<rect class="chunk" x="366.6" y="168.5" width="7" height="7"/>
<text class="lbl" x="364.1" y="162.0" text-anchor="end">CNN, reach 125</text>
<text class="ttl2 l" x="24.0" y="202">one plain four-layer CNN: paths per distance, and what happened</text>
<g class="axis">
<line x1="74.0" y1="290.2" x2="386.0" y2="290.2"/>
<text class="tick-lbl" x="68.0" y="293.7" text-anchor="end">1</text>
<line x1="74.0" y1="265.9" x2="386.0" y2="265.9"/>
<text class="tick-lbl" x="68.0" y="269.4" text-anchor="end">10</text>
<line x1="74.0" y1="234.4" x2="386.0" y2="234.4"/>
<text class="tick-lbl" x="68.0" y="237.9" text-anchor="end">100</text>
</g>
<g class=""><rect class="unrun" x="75.4" y="290.2" width="15.6" height="9.8"/></g>
<g class=""><rect class="unrun" x="93.8" y="277.1" width="15.6" height="22.9"/></g>
<g class="alloc"><rect class="use" x="112.1" y="265.9" width="15.6" height="34.1"/></g>
<g class="alloc"><rect class="use" x="130.5" y="256.8" width="15.6" height="43.2"/></g>
<g class="alloc"><rect class="use" x="148.8" y="249.1" width="15.6" height="50.9"/></g>
<g class=""><rect class="unrun" x="167.2" y="243.6" width="15.6" height="56.4"/></g>
<g class=""><rect class="unrun" x="185.5" y="239.9" width="15.6" height="60.1"/></g>
<g class=""><rect class="unrun" x="203.9" y="237.6" width="15.6" height="62.4"/></g>
<g class="alloc"><rect class="use" x="222.2" y="236.7" width="15.6" height="63.3"/></g>
<g class=""><rect class="unrun" x="240.6" y="237.6" width="15.6" height="62.4"/></g>
<g class=""><rect class="unrun" x="258.9" y="239.9" width="15.6" height="60.1"/></g>
<g class=""><rect class="unrun" x="277.3" y="243.6" width="15.6" height="56.4"/></g>
<g class="alloc"><rect class="use" x="295.6" y="249.1" width="15.6" height="50.9"/></g>
<g class=""><rect class="miss" x="314.0" y="256.8" width="15.6" height="43.2"/></g>
<g class=""><rect class="miss" x="332.3" y="265.9" width="15.6" height="34.1"/></g>
<g class=""><rect class="miss" x="350.7" y="277.1" width="15.6" height="22.9"/></g>
<g class=""><rect class="miss" x="369.0" y="290.2" width="15.6" height="9.8"/></g>
<line class="ref" x1="386.0" y1="218.0" x2="386.0" y2="300.0"/>
<text class="lbl bad" x="383.0" y="215.0" text-anchor="end">reach limit</text>
<g class="lbl-ax">
<text x="83.2" y="314">0</text>
<text x="156.6" y="314">4</text>
<text x="230.0" y="314">8</text>
<text x="303.4" y="314">12</text>
<text x="376.8" y="314">16</text>
<text class="cap l" x="74.0" y="330">copy distance in characters</text></g>
<g class="alloc"><rect class="use" x="394.0" y="226.0" width="8" height="8"/></g>
<text class="lbl" x="406.0" y="233.5">solved</text>
<g class=""><rect class="miss" x="394.0" y="241.0" width="8" height="8"/></g>
<text class="lbl" x="406.0" y="248.5">failed</text>
<g class=""><rect class="unrun" x="394.0" y="256.0" width="8" height="8"/></g>
<text class="lbl" x="406.0" y="263.5">not run</text>
</svg>
<figcaption>Above: best validation loss with the copy distance swept from 4 to 60. Below: the same CNN trained separately at each distance, laid over the number of paths running to that distance. The reach limit is 16 but it only solves up to 12, and because the bars are symmetric, distances 3 and 13 - or 2 and 14 - carry equal path counts while only the near one is solved.</figcaption>
</figure>

```
              L=4       L=8       L=16      L=32      L=60
transformer   0.0020    0.0021    0.0021    0.0021    0.0021
GRU           0.0036    0.1500    0.8320    1.7090    2.3369
LSTM          0.0058    0.1434    2.3183    2.9984    2.9980
RNN           0.0002    3.0029    3.0027    2.9984    2.9985
CNN           0.0006    0.0007    3.0003    2.9995    2.9988
```

## Cliffs, and one slope

**The RNN breaks between 4 and 8.** At distance `4` it solves the task outright
at `0.0002`, below the transformer's `0.0020`, and at distance `8` it is at
`3.0029`. There is nothing in between.

Part one measured a recurrent state's memory at about four characters. That was a
measurement of how many steps a perturbation to the state survives; here the same
four characters come back as **the boundary between a task it can do and one it
cannot.** The same number, arrived at two different ways.

**The LSTM gets one notch further.** Distance `8` gives `0.1434` - working, but
not cleanly - and `16` collapses to `2.3183`. The seed spread there is wide,
`1.9728` to `2.6639`: mid-collapse, one seed holds on slightly longer than the
other. From `32` on both are at chance.

**Only the GRU has no cliff.** `0.0036`, `0.1500`, `0.8320`, `1.7090`, `2.3369` -
the loss climbs steadily as the distance doubles, and it is still under chance at
`60`.

Part three's measurement does not explain this. There, trained on character
prediction, the GRU's per-unit half-life was *shorter* than the LSTM's. The
explanation is in part ten: train the same GRU on the copy task and the median
update gate moves from `0.405` to `0.921`, the median half-life from `0.75`
characters to `7.75`. How long a gate holds is not a constant the architecture
fixes, it is **a value the task pushes into it.** Whether the LSTM makes the same
adjustment was not measured.

**The transformer is flat.** The five values are `0.0020`, `0.0021`, `0.0021`,
`0.0021`, `0.0021`. The spread is `0.0001`, which is the same as the spread from
changing seeds at a fixed distance. Distance `4` and distance `60` are not
distinguishable to this architecture.

## The prediction was wrong

For the CNN I wrote this down before measuring. Part five measured the receptive
field of four kernel-5 layers as `1 + 4·4 = 17` characters, so **distance 16
should work and distance 32 should not.**

A receptive field of `17` means 17 reachable positions, numbered `0` through
`16`. So the farthest distance it can reach back is exactly `16`.

The result is `0.0007` at distance `8` and `3.0003` at distance `16`. The
prediction was wrong.

To find where it does break, the same CNN was run at distances `2`, `3`, `12`,
`13`, `14` and `15` under the same protocol.

```
distance     2      3      4      8      12     13     14     15     16
paths       10     20     35     85     35     20     10      4      1
loss      0.0005 0.0005 0.0006 0.0007 0.0020 3.0009 3.0007 3.0001 3.0003
```

**It solves up to distance 12 and fails from 13.** The receptive field reaches
`16`, what it actually uses is `12`, and **four characters are left on the
table.**

There is also nothing in between. Either `0.0020` or `3.00`. The GRU sloped as
the distance grew; the CNN either does it or does not.

## One countable explanation

Part five's tool applies: count **how many paths** run from the output to each
input position. That is the second row of the table above, `625` of them spread
in a bell. Distance `8` is the peak with `85`, and both ends have `1`.

Why only one path reaches distance `16` falls out of the count. Each layer picks
a kernel tap from `0` to `4` and the four picks must sum to `16`, so there is no
option other than `4+4+4+4`. Distance 16 is reached **only if all four layers
take their leftmost tap.**

With that in hand, the break lands exactly where the count drops from `35` to
`20`. The explanation writes itself: the limit is set by the path count, not the
receptive field.

**And that explanation is wrong.**

## Equal path counts, opposite results

The bell being symmetric is itself the test. Distance `3` has the same `20` paths
as distance `13`, and distance `2` has the same `10` as distance `14`. If the
path count is the cause, each pair has to come out the same.

```
paths      near                    far
20         distance 3   0.0005     distance 13  3.0009
10         distance 2   0.0005     distance 14  3.0007
```

**Same path count, and one side solves it outright while the other never moves.**
Same architecture, same parameters, same protocol.

It holds across architectures too. Part five's dilated variant (kernel 5, five
layers, dilations `1, 2, 4, 8, 16`) has only `4` paths running to distance `4`,
and solves it at `0.0006`. The plain CNN has the same `4` paths running to
distance `15`, and scores `3.0001`.

The path count is countable and it does explain why distance `16` is peculiar,
but **it does not set where the break falls.** I read a number that lined up
plausibly as the cause.

## So why 12

Unknown.

Two things are known: `17` is an upper bound and the break comes at `12`, and the
gap between them is not explained by the path count.

`12` being `3 x 4` invites reading it as "one layer's worth goes unused", which
is the same kind of reading that was just refuted. At four layers, "one layer
short" and "75% of the bound" are the same number, so they cannot be told apart.
Separating them needs a different depth - part five's `k5 x8` has a receptive
field of `33` (bound `32`), where the first reading predicts `28` and the second
predicts `24`. Not measured.

## Here the sparse window wins

That widening the receptive field genuinely buys distance does hold up. Part
five's dilated variant has a maximum offset of `(1+2+4+8+16)·4 = 124`, so a
receptive field of `125`.

**At distance `60` it scores `0.0010`.** It solves the task.

```
                      reach   ch   params   L=60 loss
plain, four layers       17   171  639,273     2.9988
dilated 1-2-4-8-16      125   153  635,763     0.0010
```

The budget is the same. The parameter counts differ by `0.6%` and both use
kernel 5. So the plain CNN collapsing at distance `13` is not "a CNN cannot see
far" - it is **this CNN's window being narrow.**

## Part five still stands

Part five summarised dilation as "it does not widen, it thins out", and on
language modelling the dilated variant was `0.10` worse at identical parameters.
That judgement is unchanged.

Here the same thinning is **the only reason it works.** What inverted is not
whether thinning is good but what the task is.

- In language the nearby positions are almost everything, so piling paths onto
  the previous four or five characters pays. Dilation moves that computation
  away, which costs
- In copying exactly one position is needed and it is `60` characters back, so
  all that matters is reaching it. The pile is spent where nothing needs it

**Thinning is neither good nor bad.** It is where the computation is placed, and
which places are needed is set by the task. Part five measured on language;
part eleven measures on copying.

## What is left

This table is 1000 steps. Part ten was 3000, and there the GRU's `L=60` was
`1.8966` against `2.3369` here. **The two numbers must not be placed side by
side.** The GRU column here says "how far within 1000 steps", not "how far given
enough steps". The architectures with cliffs probably would not move given more
steps, but that is unmeasured.

Where the dilated variant breaks **cannot be measured in this context.** The task
occupies `2L + 1` positions and the context is `128`, so `L` cannot exceed `63`.
That covers only about half of its `124` bound.

The RNN's and LSTM's cliffs were only seen on a doubling grid. The CNN was
narrowed one character at a time to pin the break between `12` and `13`; on the
recurrent side all that is known is "between `4` and `8`" and "between `8` and
`16`".

There are two seeds. At a position mid-collapse, like the LSTM's `L=16`, the
spread is `0.69`. That is enough to locate a cliff's **position** but not to pin
the **value** on top of it.

## So

- Swept the copy distance and ran five architectures at two seeds each under one
  1000-step protocol. Chance is `ln(20) = 2.9957`
- The RNN scores `0.0002` at `4` and `3.0029` at `8`. **The cliff is between 4
  and 8**, and part one's four characters - measured there by perturbing the
  state - come back here as a task boundary
- The LSTM reaches `0.1434` at `8` and `2.3183` at `16`. One notch further
- Only the GRU has no cliff. At `60` it is still under chance at `2.3369`. Part
  ten explains it, not part three - how long a gate holds is pushed in by the task
- The transformer is `0.0020` to `0.0021` across all five distances. Distance is
  invisible to it
- **The CNN prediction was wrong.** A receptive field of `17` suggested `16`
  would work; it solves only to `12` and gives `3.0009` at `13`. Four characters
  short of the bound
- The attempt to explain that by path count was refuted. Distances `3` and `13`
  have the same `20` paths and score `0.0005` and `3.0009`. **The path count does
  not set where the break falls**
- Why `12` is unexplained. Changing the depth would separate the candidates; not
  measured
- The dilated CNN with a receptive field of `125` solves distance `60` at
  `0.0010` on the same budget - so the plain CNN's collapse is not about being a
  CNN, it is about that CNN's window
