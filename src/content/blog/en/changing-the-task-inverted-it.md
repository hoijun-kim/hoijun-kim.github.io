---
title: "Changing the task inverted the order"
description: "Parts two, five and eight each attached the same caveat - this conclusion belongs to a task where the front of the sequence hardly matters. So here is one where it must. The transformer solves it outright at 0.0002 while RNN, LSTM and CNN never move off chance."
date: 2026-01-12
lang: en
kind: guide
series:
  id: not-attention
  part: 10
---

This series has said the same thing several times. A recurrent state remembers
about four characters (part one); opening the gates makes the loss worse (part
eight); widening the convolution's window makes it worse (part five); reach does
not predict performance.

And every time it attached the same caveat - **this is a task where the front of
the sequence hardly matters.** Parts two, five and eight each wrote "on a task
that genuinely needed it, this would be the reverse" and moved on. Three
deferrals is enough.

## A task where the front is required

Draw 60 characters at random from an alphabet of 20, put in a separator, then
repeat the same 60. Only the second copy is scored.

<figure class="fig">
<svg viewBox="0 0 460 316" role="img" aria-label="Above: 60 random characters, a separator, then the same 60. Getting the first copied character right means reaching 60 back. Below: loss at each copied position. On a task where the front genuinely matters, the ordering from the earlier parts inverts">
<text class="ttl2 l" x="44.0" y="18">the copy task</text>
<g class="split">
<rect class="dec" x="44.0" y="54.0" width="196.4" height="16"/>
<rect class="pre" x="240.4" y="54.0" width="3.3" height="16"/>
<rect class="dec" x="243.6" y="54.0" width="196.4" height="16"/>
</g>
<text class="lbl" x="142.2" y="99.0" text-anchor="middle">60 random characters</text>
<text class="lbl" x="341.8" y="99.0" text-anchor="middle">the same 60 again</text>
<g class="hop c"><path d="M242.0,50.0 C191.3,24.0 93.1,24.0 45.6,50.0" fill="none" marker-end="url(#a10)"/></g>
<text class="lbl ok" x="188.0" y="22.0" text-anchor="middle">60 characters back</text>
<text class="ttl2 l" x="44.0" y="134">loss at each copied position</text>
<g class="axis">
<line x1="66.0" y1="276.0" x2="440.0" y2="276.0"/>
<text class="tick-lbl" x="60.0" y="279.5" text-anchor="end">0</text>
<line x1="66.0" y1="237.2" x2="440.0" y2="237.2"/>
<text class="tick-lbl" x="60.0" y="240.7" text-anchor="end">1</text>
<line x1="66.0" y1="198.4" x2="440.0" y2="198.4"/>
<text class="tick-lbl" x="60.0" y="201.9" text-anchor="end">2</text>
<line x1="66.0" y1="159.6" x2="440.0" y2="159.6"/>
<text class="tick-lbl" x="60.0" y="163.1" text-anchor="end">3</text>
</g>
<line class="ref" x1="66.0" y1="159.8" x2="440.0" y2="159.8"/>
<text class="lbl bad" x="70.0" y="154.8">chance 2.9957</text>
<path class="curve ok" d="M66.0,276.0 L72.3,276.0 L78.7,276.0 L85.0,276.0 L91.4,276.0 L97.7,276.0 L104.0,276.0 L110.4,276.0 L116.7,276.0 L123.1,276.0 L129.4,276.0 L135.7,276.0 L142.1,276.0 L148.4,276.0 L154.7,276.0 L161.1,276.0 L167.4,276.0 L173.8,276.0 L180.1,276.0 L186.4,276.0 L192.8,276.0 L199.1,276.0 L205.5,276.0 L211.8,276.0 L218.1,276.0 L224.5,276.0 L230.8,276.0 L237.2,276.0 L243.5,276.0 L249.8,276.0 L256.2,276.0 L262.5,276.0 L268.8,276.0 L275.2,276.0 L281.5,276.0 L287.9,276.0 L294.2,276.0 L300.5,276.0 L306.9,276.0 L313.2,276.0 L319.6,276.0 L325.9,276.0 L332.2,276.0 L338.6,276.0 L344.9,276.0 L351.3,276.0 L357.6,276.0 L363.9,276.0 L370.3,276.0 L376.6,276.0 L382.9,276.0 L389.3,276.0 L395.6,276.0 L402.0,276.0 L408.3,276.0 L414.6,276.0 L421.0,276.0 L427.3,276.0 L433.7,276.0 L440.0,276.0" fill="none"/>
<path class="curve ok2" d="M66.0,228.0 L72.3,221.6 L78.7,220.9 L85.0,219.8 L91.4,214.9 L97.7,215.4 L104.0,212.1 L110.4,214.6 L116.7,210.2 L123.1,207.4 L129.4,207.2 L135.7,209.0 L142.1,208.8 L148.4,206.4 L154.7,210.2 L161.1,205.8 L167.4,205.9 L173.8,205.7 L180.1,205.5 L186.4,203.9 L192.8,204.2 L199.1,202.3 L205.5,200.8 L211.8,202.2 L218.1,201.0 L224.5,201.5 L230.8,199.7 L237.2,201.0 L243.5,200.7 L249.8,198.8 L256.2,197.6 L262.5,201.4 L268.8,196.0 L275.2,194.7 L281.5,197.3 L287.9,196.1 L294.2,198.2 L300.5,197.4 L306.9,194.5 L313.2,195.7 L319.6,194.9 L325.9,193.8 L332.2,193.3 L338.6,195.8 L344.9,190.7 L351.3,192.9 L357.6,194.4 L363.9,197.1 L370.3,194.6 L376.6,193.0 L382.9,197.9 L389.3,194.6 L395.6,196.5 L402.0,199.0 L408.3,197.1 L414.6,199.2 L421.0,200.5 L427.3,201.4 L433.7,203.6 L440.0,207.8" fill="none"/>
<path class="curve ok3" d="M66.0,159.7 L72.3,159.8 L78.7,159.8 L85.0,159.7 L91.4,159.9 L97.7,159.8 L104.0,159.8 L110.4,159.8 L116.7,159.9 L123.1,159.8 L129.4,159.7 L135.7,159.7 L142.1,159.7 L148.4,159.7 L154.7,159.7 L161.1,159.8 L167.4,159.8 L173.8,159.8 L180.1,159.8 L186.4,159.8 L192.8,159.7 L199.1,159.8 L205.5,159.9 L211.8,159.7 L218.1,159.8 L224.5,159.7 L230.8,159.7 L237.2,159.8 L243.5,159.7 L249.8,159.7 L256.2,159.9 L262.5,159.9 L268.8,159.7 L275.2,159.7 L281.5,159.8 L287.9,159.8 L294.2,159.8 L300.5,159.7 L306.9,159.8 L313.2,159.7 L319.6,159.7 L325.9,159.8 L332.2,159.7 L338.6,159.7 L344.9,159.8 L351.3,159.8 L357.6,159.7 L363.9,159.8 L370.3,159.7 L376.6,159.7 L382.9,159.8 L389.3,159.8 L395.6,159.9 L402.0,159.7 L408.3,159.8 L414.6,159.8 L421.0,159.7 L427.3,159.8 L433.7,159.8 L440.0,159.7" fill="none"/>
<path class="curve bad" d="M66.0,159.7 L72.3,159.9 L78.7,159.7 L85.0,159.8 L91.4,159.6 L97.7,159.9 L104.0,159.7 L110.4,160.0 L116.7,159.7 L123.1,159.7 L129.4,159.7 L135.7,159.9 L142.1,160.0 L148.4,159.7 L154.7,159.7 L161.1,159.7 L167.4,159.7 L173.8,159.6 L180.1,159.8 L186.4,159.8 L192.8,159.8 L199.1,159.8 L205.5,159.6 L211.8,159.8 L218.1,159.7 L224.5,159.8 L230.8,159.7 L237.2,159.7 L243.5,159.8 L249.8,159.7 L256.2,159.5 L262.5,159.6 L268.8,159.7 L275.2,159.6 L281.5,159.7 L287.9,159.9 L294.2,159.8 L300.5,159.7 L306.9,160.0 L313.2,159.7 L319.6,159.6 L325.9,159.7 L332.2,159.8 L338.6,159.8 L344.9,159.8 L351.3,159.8 L357.6,159.9 L363.9,159.6 L370.3,159.6 L376.6,159.8 L382.9,159.8 L389.3,159.7 L395.6,159.7 L402.0,159.7 L408.3,159.7 L414.6,159.7 L421.0,159.6 L427.3,159.7 L433.7,159.5 L440.0,159.6" fill="none"/>
<path class="curve bad2" d="M66.0,159.7 L72.3,159.8 L78.7,159.7 L85.0,159.7 L91.4,159.9 L97.7,159.7 L104.0,159.7 L110.4,159.8 L116.7,159.8 L123.1,159.8 L129.4,159.7 L135.7,159.6 L142.1,159.6 L148.4,159.8 L154.7,159.7 L161.1,159.8 L167.4,159.9 L173.8,159.7 L180.1,159.8 L186.4,159.7 L192.8,159.7 L199.1,159.8 L205.5,159.8 L211.8,159.6 L218.1,159.8 L224.5,159.7 L230.8,159.8 L237.2,159.8 L243.5,159.7 L249.8,159.6 L256.2,159.8 L262.5,160.0 L268.8,159.7 L275.2,159.8 L281.5,159.8 L287.9,159.6 L294.2,159.8 L300.5,159.7 L306.9,159.8 L313.2,159.7 L319.6,159.6 L325.9,159.7 L332.2,159.6 L338.6,159.8 L344.9,159.6 L351.3,159.8 L357.6,159.7 L363.9,159.9 L370.3,159.7 L376.6,159.6 L382.9,159.7 L389.3,159.8 L395.6,159.8 L402.0,159.7 L408.3,159.7 L414.6,159.9 L421.0,159.8 L427.3,159.9 L433.7,159.7 L440.0,159.7" fill="none"/>
<text class="lbl" x="444.0" y="171.8" text-anchor="end">RNN</text>
<text class="lbl" x="444.0" y="185.8" text-anchor="end">CNN</text>
<text class="lbl" x="444.0" y="199.8" text-anchor="end">LSTM</text>
<text class="lbl" x="444.0" y="213.8" text-anchor="end">GRU</text>
<text class="lbl" x="444.0" y="269.0" text-anchor="end">transformer</text>
<g class="lbl-ax">
<text x="66.0" y="291">0</text>
<text x="129.4" y="291">10</text>
<text x="192.8" y="291">20</text>
<text x="256.2" y="291">30</text>
<text x="319.6" y="291">40</text>
<text x="382.9" y="291">50</text>
<text x="440.0" y="291">59</text>
<text class="cap l" x="66.0" y="306">which copied character</text></g>
<defs><marker id="a10" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,1 L7,4 L0,7 z" class="ahd"/></marker></defs>
</svg>
<figcaption>Above: 60 random characters, a separator, then the same 60. Getting the first copied character right means reaching 60 back, and the distance stays 60 for every one after it. Below: loss at each copied position. Only the transformer sits on the floor; RNN, LSTM and CNN never leave the chance line. The GRU alone is somewhere in between.</figcaption>
</figure>

What has to be predicted at position `60` is the character at position `0` - a
distance of exactly `60` - and position `60+j` needs position `j`, so the distance
stays `60` throughout. The string is random, so without looking back there is
nothing to do but guess, and guessing is `ln(20) = 2.9957`.

The models, the budget and the optimiser are the same as the earlier parts. Only
the data changed.

## Three of them cannot do it at all

```
             best val (3 seeds)               median
transformer  0.0002  0.0002  0.0002       0.0002
GRU          1.8907  1.9005  1.8966       1.8966
LSTM         2.9967  2.9974  2.9966       2.9967
CNN          2.9974  2.9975  2.9974       2.9974
RNN          2.9980  2.9982  2.9975       2.9980
```

RNN, LSTM and CNN do not leave `2.9957` to three decimal places. **They learned
nothing.**

For the CNN that is expected. Part five confirmed its receptive field at `17`
characters with everything outside it absent from the computation graph. Sixty
back may as well not exist. There is a configuration reaching `125`, and it was
not run here - that is noted below.

The two recurrent models can structurally see it. They still cannot do it. Part
one measured a single changed character losing half its trace within four and
under 1% by thirty-two. Reaching back `60` with that is not possible.

## The transformer solves it outright

`0.0002`, the same for all three seeds. A loss of `0.0002` means all sixty
characters right - `15,000` times better than chance.

Attention wires positions directly to each other. That is what part eight
measured: at 127 back its gradient was `1.19e-02`, `39,145` times the GRU's at
the same distance. There, that reach was useless. Here it is the whole task.

**Part eight's "reach does not predict performance" inverts here** - or more
precisely, the condition under which it inverts is now known.

## The GRU does about half of it

`1.8966`, well under chance and well over the transformer. Position by position,
the first copied character is easiest at `1.237` and it worsens toward `1.77`
further along.

The first being easiest was strange enough to hypothesise about: the first input
writes into an empty state with nothing to compete with, so perhaps it leaves a
larger imprint. Measured, on an untrained GRU, changing position `j` and seeing
how much the state at step 60 moves:

```
changed at   j=0      j=20     j=40     j=58     j=59
state moves  0.0000   0.0000   0.0001   0.5809   1.1070
```

Everything through `j = 40` is `0`. There is no first-impression effect. **The
hypothesis was wrong and the reason remains unknown.**

## Gates move when the task asks

Since the GRU manages something, the place to look is where its gates went.
Pulling the update gate out exactly as part three did:

```
                          z mean   unit median   median half-life   10+ chars
trained on the copy task   0.921         0.914          7.75 chars   131 of 381
trained on characters (3)  0.405         0.398          0.75 chars            0
```

Same architecture, same width, same optimiser, and the update gate has gone from
`0.405` to `0.921`. The median half-life goes from `0.75` characters to `7.75`, a
factor of ten, and the "holds ten or more" units that part three could not find
even one of now number `131`.

**Parts two and three were not wrong.** Part two found the forget gate barely off
its `0.5` initialisation; part three found no unit holding a long memory. Both
were right, and both because character prediction never asked. Ask, and they move.

## The earlier parts are not overturned

What inverts here is not the earlier **numbers** but the **conditions** they were
attached to.

- Part one's "about four characters" still holds. It is exactly why the RNN and
  LSTM fail here
- Part two's "the gates barely moved" still holds. Change the task and they move
- Part five's "widening makes it worse" still holds. There was no reason to widen
- Part eight's "reach does not predict performance" still holds. Here reach is
  all there is

That the three caveats were right is this part's result.

## What is left

The CNN was not run at a receptive field of `125`. Part five's configuration
exists, so it could be, and whether a window past `60` lets it copy is unmeasured.
It probably would - unmeasured is unmeasured.

Only one copy length was used, `60`. Dropping it to `4`, `8`, `16` and watching
where recurrence starts succeeding would connect directly to part one's "four
characters", and was not done.

And the transformer's `0.0002` comes from 3000 steps. Copying has a single rule
and nothing to memorise, so unlike the earlier parts no overfitting appears. It is
a different kind of easy from real text.

## So

- Built a task where the front of the sequence is required: 60 random characters
  rewritten after a separator, chance `ln(20) = 2.9957`
- RNN `2.9980`, LSTM `2.9967`, CNN `2.9974` - **none of the three move off
  chance.** Part one's four-character memory and part five's 17-character window
  are what is being paid for
- The transformer solves it at `0.0002`, `15,000` times better than chance
- Only the GRU sits between, at `1.8966`. Its first copied character is easiest at
  `1.237` and why is unexplained - the first-impression hypothesis was measured
  and rejected
- The GRU's update gate moves from `0.405` to `0.921` and its median half-life
  from `0.75` characters to `7.75`. Part three found zero units holding ten or
  more; here there are `131`
- The earlier numbers all stand. What inverted is the condition attached to them,
  and three of those parts had already written it down
