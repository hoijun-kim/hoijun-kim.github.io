---
title: "What splitting the head into eight actually changes"
description: "The parameter count is identical, so why split at all. This measures the fact that one weighted average cannot carry two things, and what the rank ceiling on a head actually limits - along with how I misread it the first time."
date: 2025-08-10
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 10
---

By part nine one block of attention is complete: weights built from content,
with position added so it knows about order. A real transformer does one more
thing to that block. It **splits it into eight.**

What the split buys is this part. Start with the strange bit.

## Not one extra parameter

Whether `d_model = 64` runs as one head or eight, the weight matrices are the
same.

```
1 head  (dh=64)   Wq, Wk, Wv, Wo, each 64x64 = 4,096  |  16,384 for all four
8 heads (dh=8)    Wq, Wk, Wv, Wo, each 64x64 = 4,096  |  16,384 for all four
```

Splitting means cutting the same `64` dimensions into eight slices of `8`, doing
attention **separately** inside each slice, then stitching the results back
together and multiplying by `Wo`. Same parameters, same multiplications. If
anything comes for free, it comes from the structure.

## One average cannot carry two things

The crux is already in one sentence from part eight. Attention is a **weighted
average**. One row is one probability distribution, and one distribution
collapses the result to **a single point**.

So what happens when a token needs two things at once - the value of the token
sharing its topic, and the value of its immediate neighbour? Measure whether
**both** can be read back out of the layer's output. The readout is the best
linear map, and the tokens outnumber the value dimensions 1600 to 1 so that
nothing fits by accident.

```
1 head, all on the partner (a=1.00)    relative error 0.7069
1 head, split evenly       (a=0.50)    relative error 0.7075
1 head, any ratio at all               best is 0.7069
2 heads, one each                      relative error 0.0000
```

Recovering exactly half would score `sqrt(1/2) = 0.7071`. One head sits exactly
there - **one of the two is lost entirely.**

The middle row is the interesting one. Splitting the attention evenly feels like
a compromise worth making, and it scores `0.7075`, which is **worse**. Blending
ruins both: from the single point `0.5(v_partner + v_neighbour)` there is no way
to pull `v_partner` and `v_neighbour` back apart.

Sweeping the ratio from 0 to 1, the best move is to give everything to one side.
For a single head, **compromise costs**. It has to choose.

With two heads there is nothing to choose. Each takes one, and the results pass
through different row blocks of `Wo` before being added, so they never mix. The
error is `0.0000`.

## Which is why heads look at different things

Take part eight's six tokens, attach part nine's positional encoding, and hand
the first four dimensions (content) and the last four (position) to different
heads. They split like this.

<figure class="fig">
<svg viewBox="0 0 522 293" role="img" aria-label="Two heads' attention matrices on the same input. The left one finds tokens sharing a topic, the right one looks only at adjacent positions">
<g class="hm">
<rect x="36" y="62" width="33" height="33" rx="3" style="opacity:0.981"/>
<text class="v on" x="52.5" y="82.0">0.51</text>
<rect x="72" y="62" width="33" height="33" rx="3" style="opacity:0.114"/>
<text class="v off" x="88.5" y="82.0">0.03</text>
<rect x="108" y="62" width="33" height="33" rx="3" style="opacity:0.087"/>
<text class="v off" x="124.5" y="82.0">0.02</text>
<rect x="144" y="62" width="33" height="33" rx="3" style="opacity:0.763"/>
<text class="v on" x="160.5" y="82.0">0.39</text>
<rect x="180" y="62" width="33" height="33" rx="3" style="opacity:0.131"/>
<text class="v off" x="196.5" y="82.0">0.04</text>
<rect x="216" y="62" width="33" height="33" rx="3" style="opacity:0.089"/>
<text class="v off" x="232.5" y="82.0">0.02</text>
<rect x="36" y="98" width="33" height="33" rx="3" style="opacity:0.106"/>
<text class="v off" x="52.5" y="118.0">0.03</text>
<rect x="72" y="98" width="33" height="33" rx="3" style="opacity:1.000"/>
<text class="v on" x="88.5" y="118.0">0.52</text>
<rect x="108" y="98" width="33" height="33" rx="3" style="opacity:0.125"/>
<text class="v off" x="124.5" y="118.0">0.04</text>
<rect x="144" y="98" width="33" height="33" rx="3" style="opacity:0.125"/>
<text class="v off" x="160.5" y="118.0">0.04</text>
<rect x="180" y="98" width="33" height="33" rx="3" style="opacity:0.666"/>
<text class="v on" x="196.5" y="118.0">0.34</text>
<rect x="216" y="98" width="33" height="33" rx="3" style="opacity:0.142"/>
<text class="v off" x="232.5" y="118.0">0.05</text>
<rect x="36" y="134" width="33" height="33" rx="3" style="opacity:0.087"/>
<text class="v off" x="52.5" y="154.0">0.02</text>
<rect x="72" y="134" width="33" height="33" rx="3" style="opacity:0.135"/>
<text class="v off" x="88.5" y="154.0">0.04</text>
<rect x="108" y="134" width="33" height="33" rx="3" style="opacity:0.979"/>
<text class="v on" x="124.5" y="154.0">0.51</text>
<rect x="144" y="134" width="33" height="33" rx="3" style="opacity:0.087"/>
<text class="v off" x="160.5" y="154.0">0.02</text>
<rect x="180" y="134" width="33" height="33" rx="3" style="opacity:0.114"/>
<text class="v off" x="196.5" y="154.0">0.03</text>
<rect x="216" y="134" width="33" height="33" rx="3" style="opacity:0.762"/>
<text class="v on" x="232.5" y="154.0">0.39</text>
<rect x="36" y="170" width="33" height="33" rx="3" style="opacity:0.904"/>
<text class="v on" x="52.5" y="190.0">0.47</text>
<rect x="72" y="170" width="33" height="33" rx="3" style="opacity:0.151"/>
<text class="v off" x="88.5" y="190.0">0.05</text>
<rect x="108" y="170" width="33" height="33" rx="3" style="opacity:0.093"/>
<text class="v off" x="124.5" y="190.0">0.02</text>
<rect x="144" y="170" width="33" height="33" rx="3" style="opacity:0.749"/>
<text class="v on" x="160.5" y="190.0">0.38</text>
<rect x="180" y="170" width="33" height="33" rx="3" style="opacity:0.171"/>
<text class="v off" x="196.5" y="190.0">0.06</text>
<rect x="216" y="170" width="33" height="33" rx="3" style="opacity:0.096"/>
<text class="v off" x="232.5" y="190.0">0.02</text>
<rect x="36" y="206" width="33" height="33" rx="3" style="opacity:0.146"/>
<text class="v off" x="52.5" y="226.0">0.05</text>
<rect x="72" y="206" width="33" height="33" rx="3" style="opacity:0.912"/>
<text class="v on" x="88.5" y="226.0">0.47</text>
<rect x="108" y="206" width="33" height="33" rx="3" style="opacity:0.125"/>
<text class="v off" x="124.5" y="226.0">0.04</text>
<rect x="144" y="206" width="33" height="33" rx="3" style="opacity:0.172"/>
<text class="v off" x="160.5" y="226.0">0.06</text>
<rect x="180" y="206" width="33" height="33" rx="3" style="opacity:0.667"/>
<text class="v on" x="196.5" y="226.0">0.34</text>
<rect x="216" y="206" width="33" height="33" rx="3" style="opacity:0.143"/>
<text class="v off" x="232.5" y="226.0">0.05</text>
<rect x="36" y="242" width="33" height="33" rx="3" style="opacity:0.095"/>
<text class="v off" x="52.5" y="262.0">0.02</text>
<rect x="72" y="242" width="33" height="33" rx="3" style="opacity:0.174"/>
<text class="v off" x="88.5" y="262.0">0.06</text>
<rect x="108" y="242" width="33" height="33" rx="3" style="opacity:0.895"/>
<text class="v on" x="124.5" y="262.0">0.46</text>
<rect x="144" y="242" width="33" height="33" rx="3" style="opacity:0.096"/>
<text class="v off" x="160.5" y="262.0">0.02</text>
<rect x="180" y="242" width="33" height="33" rx="3" style="opacity:0.141"/>
<text class="v off" x="196.5" y="262.0">0.04</text>
<rect x="216" y="242" width="33" height="33" rx="3" style="opacity:0.765"/>
<text class="v on" x="232.5" y="262.0">0.39</text>
<rect x="301" y="62" width="33" height="33" rx="3" style="opacity:1.000"/>
<text class="v on" x="317.5" y="82.0">0.86</text>
<rect x="337" y="62" width="33" height="33" rx="3" style="opacity:0.179"/>
<text class="v off" x="353.5" y="82.0">0.11</text>
<rect x="373" y="62" width="33" height="33" rx="3" style="opacity:0.062"/>
<text class="v off" x="389.5" y="82.0">0.00</text>
<rect x="409" y="62" width="33" height="33" rx="3" style="opacity:0.060"/>
<text class="v off" x="425.5" y="82.0">0.00</text>
<rect x="445" y="62" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="461.5" y="82.0">0.00</text>
<rect x="481" y="62" width="33" height="33" rx="3" style="opacity:0.097"/>
<text class="v off" x="497.5" y="82.0">0.03</text>
<rect x="301" y="98" width="33" height="33" rx="3" style="opacity:0.171"/>
<text class="v off" x="317.5" y="118.0">0.10</text>
<rect x="337" y="98" width="33" height="33" rx="3" style="opacity:0.935"/>
<text class="v on" x="353.5" y="118.0">0.80</text>
<rect x="373" y="98" width="33" height="33" rx="3" style="opacity:0.171"/>
<text class="v off" x="389.5" y="118.0">0.10</text>
<rect x="409" y="98" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="425.5" y="118.0">0.00</text>
<rect x="445" y="98" width="33" height="33" rx="3" style="opacity:0.060"/>
<text class="v off" x="461.5" y="118.0">0.00</text>
<rect x="481" y="98" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="497.5" y="118.0">0.00</text>
<rect x="301" y="134" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="317.5" y="154.0">0.00</text>
<rect x="337" y="134" width="33" height="33" rx="3" style="opacity:0.170"/>
<text class="v off" x="353.5" y="154.0">0.10</text>
<rect x="373" y="134" width="33" height="33" rx="3" style="opacity:0.934"/>
<text class="v on" x="389.5" y="154.0">0.80</text>
<rect x="409" y="134" width="33" height="33" rx="3" style="opacity:0.170"/>
<text class="v off" x="425.5" y="154.0">0.10</text>
<rect x="445" y="134" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="461.5" y="154.0">0.00</text>
<rect x="481" y="134" width="33" height="33" rx="3" style="opacity:0.060"/>
<text class="v off" x="497.5" y="154.0">0.00</text>
<rect x="301" y="170" width="33" height="33" rx="3" style="opacity:0.060"/>
<text class="v off" x="317.5" y="190.0">0.00</text>
<rect x="337" y="170" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="353.5" y="190.0">0.00</text>
<rect x="373" y="170" width="33" height="33" rx="3" style="opacity:0.170"/>
<text class="v off" x="389.5" y="190.0">0.10</text>
<rect x="409" y="170" width="33" height="33" rx="3" style="opacity:0.934"/>
<text class="v on" x="425.5" y="190.0">0.80</text>
<rect x="445" y="170" width="33" height="33" rx="3" style="opacity:0.170"/>
<text class="v off" x="461.5" y="190.0">0.10</text>
<rect x="481" y="170" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="497.5" y="190.0">0.00</text>
<rect x="301" y="206" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="317.5" y="226.0">0.00</text>
<rect x="337" y="206" width="33" height="33" rx="3" style="opacity:0.060"/>
<text class="v off" x="353.5" y="226.0">0.00</text>
<rect x="373" y="206" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="389.5" y="226.0">0.00</text>
<rect x="409" y="206" width="33" height="33" rx="3" style="opacity:0.171"/>
<text class="v off" x="425.5" y="226.0">0.10</text>
<rect x="445" y="206" width="33" height="33" rx="3" style="opacity:0.935"/>
<text class="v on" x="461.5" y="226.0">0.80</text>
<rect x="481" y="206" width="33" height="33" rx="3" style="opacity:0.171"/>
<text class="v off" x="497.5" y="226.0">0.10</text>
<rect x="301" y="242" width="33" height="33" rx="3" style="opacity:0.097"/>
<text class="v off" x="317.5" y="262.0">0.03</text>
<rect x="337" y="242" width="33" height="33" rx="3" style="opacity:0.061"/>
<text class="v off" x="353.5" y="262.0">0.00</text>
<rect x="373" y="242" width="33" height="33" rx="3" style="opacity:0.060"/>
<text class="v off" x="389.5" y="262.0">0.00</text>
<rect x="409" y="242" width="33" height="33" rx="3" style="opacity:0.062"/>
<text class="v off" x="425.5" y="262.0">0.00</text>
<rect x="445" y="242" width="33" height="33" rx="3" style="opacity:0.179"/>
<text class="v off" x="461.5" y="262.0">0.11</text>
<rect x="481" y="242" width="33" height="33" rx="3" style="opacity:1.000"/>
<text class="v on" x="497.5" y="262.0">0.86</text>
</g><g class="lbl-ax">
<text x="52.5" y="51">t0</text>
<text x="88.5" y="51">t1</text>
<text x="124.5" y="51">t2</text>
<text x="160.5" y="51">t3</text>
<text x="196.5" y="51">t4</text>
<text x="232.5" y="51">t5</text>
<text class="r" x="27" y="82.0">t0</text>
<text class="r" x="27" y="118.0">t1</text>
<text class="r" x="27" y="154.0">t2</text>
<text class="r" x="27" y="190.0">t3</text>
<text class="r" x="27" y="226.0">t4</text>
<text class="r" x="27" y="262.0">t5</text>
<text x="317.5" y="51">t0</text>
<text x="353.5" y="51">t1</text>
<text x="389.5" y="51">t2</text>
<text x="425.5" y="51">t3</text>
<text x="461.5" y="51">t4</text>
<text x="497.5" y="51">t5</text>
<text class="r" x="292" y="82.0">t0</text>
<text class="r" x="292" y="118.0">t1</text>
<text class="r" x="292" y="154.0">t2</text>
<text class="r" x="292" y="190.0">t3</text>
<text class="r" x="292" y="226.0">t4</text>
<text class="r" x="292" y="262.0">t5</text>
<text class="cap l" x="27" y="20">row = from</text>
<text class="ttl2" x="142.5" y="40">head A - content</text>
<text class="ttl2" x="407.5" y="40">head B - position</text>
</g>
</svg>
<figcaption>Two heads attending to the same input. The left finds tokens sharing a topic and gives the partner 0.39; the right ignores content entirely and gives 0.10 to each immediate neighbour. The off-diagonal entries correlate at -0.374: where one head looks, the other looks less.</figcaption>
</figure>

Head A is part eight unchanged: `0.510` to itself, `0.389` to its topic partner,
and only `0.025` to the tokens beside it. Head B is the opposite: `0.797` to
itself, `0.101` to each immediate neighbour, and `0.000` to the topic partner.

B is tridiagonal. Neighbour `0.101`, two away `0.001`, three away `0.000` - two
orders of magnitude per step. It does not look at content at all.

The off-diagonal entries of the two matrices correlate at `-0.374`. Not merely
different by chance: **where one head looks, the other looks less.**

Here I chose which dimensions went to which head. A real model has `Wq` and `Wk`
learn that. What the structure guarantees is only that there is **room** to look
at several things separately; what gets looked at is up to training.

## The second reason: a rank ceiling - and I got this wrong first

Splitting costs something too. One head's logit matrix is `Q_h K_h^T`, and since
`Q_h` and `K_h` are `dh` wide, its **rank cannot exceed `dh`**.

```
1 head  (dh=64)        12 tokens, logits 12x12, rank 12
one of 8 heads (dh=8)  12 tokens, logits 12x12, rank 8
```

That part is true. Writing this the first time, I took one step further from it:
"so a `dh=8` head cannot in principle express 'look three places back' across 12
tokens, and eight of twelve is the ceiling." The evidence was that approximating
that permutation matrix at rank `k` leaves an error of `sqrt((n-k)/n)` with a
fraction `k/n` correct.

**That was wrong.** The arithmetic holds; the thing being measured does not.

Attention does not need to **reconstruct** that logit matrix. After the softmax
what matters is which entry is largest and how much smaller the next one is.
Finding a matrix close to the target and finding a matrix that produces the
target's ordering are different problems.

Optimising directly shows it at once. Constrain the rank to `k`, then train
`A @ B` under cross entropy to hit the right column:

```
target                     fraction correct, SVD   fraction correct, optimised
'three back' at rank 2                      0.17                         1.00
'three back' at rank 4                      0.33                         1.00
'three back' at rank 8                      0.67                         1.00
```

**Rank 2 gets all of them.** And it is not special to a cyclic shift.

```
minimum rank that gets every argmax right
  everyone looks at the same place    1
  'three back' (cyclic shift)         2
  three random permutations           2, 2, 2
  at 4, 8, 12 and 16 tokens           2, 2, 2, 2
```

Rank 1 is `u v^T`, so every row's maximum lands in the same column - it can only
say "all look at one place". At rank 2, **any permutation at any number of
tokens** becomes reachable.

Given part nine this should have been obvious. That part measured a positional
shift as a **rank-2 rotation** per frequency pair, and this one claimed rank 8
cannot express a shift. The two contradicted each other.

## So what a small dh actually costs

Not the logits but the **output**. A head's output is `A @ V_h`, and `V_h` has
only `dh` columns, so its rank cannot exceed `min(n, dh)` - for any `A`
whatsoever.

```
1 head  (dh=64)        output 12x64  rank 12
one of 8 heads (dh=8)  output 12x8   rank 8
```

Measuring how far an arbitrary target output can be matched:

```
dh = 8     no A reaches more than 42.3% of the target
dh = 64    100% reachable
```

That value is exactly `1 - sqrt(1 - dh/n)`: projecting each column of a random
target onto a `dh`-dimensional subspace keeps `dh/n` of the squared norm. Over
200 random targets it measures `42.4%` with a standard deviation of `1.84`.

The `sqrt((n-k)/n)` I misapplied to the logits in the previous section **is the
right formula here**, on the output. The same arithmetic is wrong in one place
and right in another.

What splitting costs is therefore **not where to look but what to write**. The
directions a head can push into the residual stream drop to `dh` of them. Split
into eight and each head gets a narrow channel - and there are eight channels.
The two heads scoring `0.0000` in the previous section were using two of those
eight separately.

Eight is therefore a compromise. More heads means more things watched separately,
and each with fewer dimensions to write with.

## Concatenating is adding

One implementation note to finish. The heads are usually described as
concatenated and then multiplied by `Wo`, but slicing `Wo` by rows per head
shows that this is the same as **summing each head's contribution**.

```python
concat = np.hstack(heads) @ Wo
summed = sum(heads[h] @ Wo[h*dh:(h+1)*dh] for h in range(H))
np.abs(concat - summed).max()        # 6.9e-17
```

Nothing but floating-point noise between them. The heads **never meet** inside
attention. Each takes its own average, and at the end each adds its own result
to the residual stream.

The view is practical too. To see what one head does, keep its term and zero the
others. That works precisely because it is a sum.

## Honestly

Nothing anywhere forces heads to do different jobs. The two above split because
I handed them different dimensions, and in trained models there are steady
reports that many heads end up similar enough to prune with little loss. The
structure only **makes room**; whether the room gets used is another matter.

## So

- Splitting heads adds no parameters and no multiplications. The same four
  `64x64` matrices, `16,384` in total
- One attention is one weighted average. Needing two things loses one - relative
  error `0.7069` against a theoretical `sqrt(1/2)`. Splitting evenly is worse at
  `0.7075`
- Two heads score `0.0000`, because they write to different places and are only
  added at the end
- The price is rank, but of the **output** rather than the logits. A `dh=8` head
  reaches only `42.3%` of an arbitrary target output, exactly
  `1 - sqrt(1 - dh/n)`. Where to look needs rank 2
- Concatenate-then-project equals sum-of-contributions, to `6.9e-17`

Next time, the part sitting next to attention that nobody looks at -
two thirds of the parameters live there and it is called, simply, feed-forward.
