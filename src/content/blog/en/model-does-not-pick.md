---
title: "The model does not pick the next character"
description: "What a trained model emits is a distribution, not a character. Choosing is a separate rule bolted on afterwards, and this measures how much that rule changes the result using the model built in part thirteen."
date: 2025-09-02
lang: en
kind: guide
series:
  id: after-training
  part: 1
---

The previous series was about building a model. Its last part trained a 637k
parameter character predictor down to a loss of `1.7510`.

Ask that model what the next character is, though, and no character comes back.
What comes back is **a distribution over 100 of them**. Pulling one character
out of that is not something the model does; it is a rule we supply separately.
This series measures the things that get bolted on after training ends.

The first is that rule. Same model, same weights, only the rule changing - and
how far the output moves. The model is the one trained in part thirteen,
unchanged.

## The most plausible rule is the worst one

The obvious rule is to **take the highest-probability character**: at every
position write whatever the model believes most. It is hard to see the harm.

Run it.

```
greedy   repetition 0.997
'                                                        '
```

Spaces. Out of 400 characters generated, `99.7%` of the eight-character windows
are duplicates.

The reason is simple. Choosing the highest-probability character also **fixes
the context for the next position**. Pick the highest again there and it leads
back to the same place. Once the loop closes on itself there is no way out,
because nothing random was ever mixed in.

Stringing together the most plausible next characters does not give the most
plausible text.

## Temperature

So sample in proportion instead. But the distribution need not be used as it
came: divide the logits by `T` and take the softmax again, and the sharpness
changes.

```python
p = softmax(logits / T)
```

Small `T` sharpens it, piling mass on the leader; large `T` flattens it. `T=0`
is greedy and `T=1` is the model untouched. It is the same dial part eight used
when dividing by `sqrt(d)` to keep the softmax off saturation.

```
greedy        repetition 0.997
T = 0.5       repetition 0.438
T = 0.8       repetition 0.000
T = 1.0       repetition 0.010
T = 1.3       repetition 0.000
```

At `0.5` it still catches in a loop. From `0.8` it does not. The price is that
the higher the temperature, the looser the choice of character.

```
T = 0.5   '```\n                                          0.6621\n4  '
T = 0.8   '```\nFlattent `11 above the same\nrank 64   means - residu'
T = 1.3   '`16, a=0, 336.11  b=0.00350 steps\n`3.8203` wOth `t0`. He'
```

`Flattent` at `0.8` and `wOth` at `1.3` show what temperature buys and what it
sells. It escapes repetition by making typos.

## The tail is the real problem

Why does raising the temperature produce typos? Because of the distribution's
**tail**. Among the 100 characters are ones the model gave essentially zero, and
raising the temperature lifts them far enough to get drawn. We end up choosing
what the model said no to.

The fix is to cut the tail: keep the top `k` (top-k), or keep characters until
the cumulative probability reaches `p` (top-p). Which is better falls out of
measuring **how many candidates each position actually needs**.

<figure class="fig">
<svg viewBox="0 0 460 262" role="img" aria-label="Distribution of how many candidate characters are needed to reach 0.9 of the probability mass. One suffices at 34.4% of positions and more than ten are needed at 10.4%">
<g class="axis">
<line x1="54" y1="206.0" x2="446" y2="206.0"/>
<text class="tick-lbl" x="45" y="209.5" text-anchor="end">0%</text>
<line x1="54" y1="158.6" x2="446" y2="158.6"/>
<text class="tick-lbl" x="45" y="162.1" text-anchor="end">10%</text>
<line x1="54" y1="111.3" x2="446" y2="111.3"/>
<text class="tick-lbl" x="45" y="114.8" text-anchor="end">20%</text>
<line x1="54" y1="63.9" x2="446" y2="63.9"/>
<text class="tick-lbl" x="45" y="67.4" text-anchor="end">30%</text>
<line class="frame" x1="54" y1="26" x2="54" y2="206"/><line class="frame" x1="54" y1="206" x2="446" y2="206"/>
<line class="frame" x1="64.9" y1="206" x2="64.9" y2="210"/>
<text class="tick-lbl" x="64.9" y="222" text-anchor="middle">1</text>
<line class="frame" x1="152.0" y1="206" x2="152.0" y2="210"/>
<text class="tick-lbl" x="152.0" y="222" text-anchor="middle">5</text>
<line class="frame" x1="260.9" y1="206" x2="260.9" y2="210"/>
<text class="tick-lbl" x="260.9" y="222" text-anchor="middle">10</text>
<line class="frame" x1="369.8" y1="206" x2="369.8" y2="210"/>
<text class="tick-lbl" x="369.8" y="222" text-anchor="middle">15</text>
<line class="frame" x1="435.1" y1="206" x2="435.1" y2="210"/>
<text class="tick-lbl" x="435.1" y="222" text-anchor="middle">18</text>
<text class="tick-lbl" x="250.0" y="256" text-anchor="middle">candidates needed to reach 0.9</text>
<text class="tick-lbl" x="54" y="16" text-anchor="start">share of positions</text></g><g class="hm">
<rect x="55.0" y="43.2" width="19.8" height="162.8" rx="1.5" style="opacity:0.95"/>
<rect x="76.8" y="116.3" width="19.8" height="89.7" rx="1.5" style="opacity:0.95"/>
<rect x="98.6" y="136.6" width="19.8" height="69.4" rx="1.5" style="opacity:0.95"/>
<rect x="120.3" y="175.9" width="19.8" height="30.1" rx="1.5" style="opacity:0.95"/>
<rect x="142.1" y="188.4" width="19.8" height="17.6" rx="1.5" style="opacity:0.95"/>
<rect x="163.9" y="189.8" width="19.8" height="16.2" rx="1.5" style="opacity:0.95"/>
<rect x="185.7" y="194.9" width="19.8" height="11.1" rx="1.5" style="opacity:0.95"/>
<rect x="207.4" y="194.9" width="19.8" height="11.1" rx="1.5" style="opacity:0.95"/>
<rect x="229.2" y="195.8" width="19.8" height="10.2" rx="1.5" style="opacity:0.95"/>
<rect x="251.0" y="199.5" width="19.8" height="6.5" rx="1.5" style="opacity:0.95"/>
<rect x="272.8" y="196.7" width="19.8" height="9.3" rx="1.5" style="opacity:0.42"/>
<rect x="294.6" y="190.3" width="19.8" height="15.7" rx="1.5" style="opacity:0.42"/>
<rect x="316.3" y="200.9" width="19.8" height="5.1" rx="1.5" style="opacity:0.42"/>
<rect x="338.1" y="200.4" width="19.8" height="5.6" rx="1.5" style="opacity:0.42"/>
<rect x="359.9" y="198.6" width="19.8" height="7.4" rx="1.5" style="opacity:0.42"/>
<rect x="381.7" y="202.3" width="19.8" height="3.7" rx="1.5" style="opacity:0.42"/>
<rect x="403.4" y="203.7" width="19.8" height="2.3" rx="1.5" style="opacity:0.42"/>
<rect x="425.2" y="206.0" width="19.8" height="0.0" rx="1.5" style="opacity:0.42"/>
</g>
<line class="floor" x1="271.8" y1="26" x2="271.8" y2="206"/>
<text class="lbl bad" x="277.8" y="42" text-anchor="start">k=10 sits here</text>
<text class="lbl ok" x="80.1" y="34.2" text-anchor="start">34.4%</text>
</svg>
<figcaption>How many candidates it takes to reach 0.9 of the probability mass, counted at 1024 positions over the validation data. One is enough at 34.4% of them, and more than ten are needed at 10.4%. The vertical line is k=10, and it fits neither end.</figcaption>
</figure>

Counting, at 1024 positions over the validation data, how many candidates it
takes to reach a cumulative `0.9`:

```
candidates to reach 0.90   median 2    Q1 1    Q3 5     range 1 - 17
candidates to reach 0.99   median 5    Q1 3    Q3 12    range 1 - 41
```

**Every position is different.** At `34.4%` of them a single candidate fills
`0.9` - positions where the model is sure, mid-word or halfway through closing a
code fence. At `10.4%` of them ten candidates are not enough, as at the start of
a sentence.

Entropy says the same. The median is `0.804` while the minimum is `0.0003` and
the maximum `2.969`, against `4.605` for being uniformly torn. It runs nearly
end to end.

## Which is why a fixed k is always wrong

Put `k=10` against those numbers.

```
average mass held by top-10                                       0.9751
mass held by ranks 2-10 where one candidate suffices (34.4%)      0.0316
mass top-10 discards where ten are not enough (10.4%)             0.1609
```

On average `0.9751` looks excellent. But the average is hiding something at each
end.

Where the model is sure, ranks two through ten hold `0.0316` between them, and
those nine pieces of junk are kept as candidates. Where ten are not enough,
`0.1609` of legitimate mass is thrown away.

`k` is a quantity that should differ per position and is nailed to a constant,
so tuning it for one end breaks the other. Top-p **recomputes that `k` from the
distribution at every position**, which shrinks the candidate set to one where
the model is sure and grows it past twenty where it is torn.

```
top-k 10    repetition 0.003   '```\n\n(16, 4)`, all scale mether the settyon: `(44n) + 1 '
top-p 0.9   repetition 0.008   '```\nlambda = a @ Ws * in independent of a the minimum bu'
```

In a model this small both read about the same. With a vocabulary of only 100 the
tail is short - everything from rank 11 down holds `0.0249` on average.

From here on this is **extrapolation, not measurement**. With a vocabulary of
50,000 the 49,000 in the tail would presumably add up to a larger share and the
two schemes would separate more. This experiment has one vocabulary of 100 and
does not confirm that.

## So

- What the model emits is a distribution, not a character. The rule for choosing
  is ours, decided apart from training
- Always taking the highest catches in a loop: repetition `0.997`, effectively
  one character forever
- Temperature trades repetition against typos. `0.5` still loops; `1.3` writes
  things like `wOth`
- How many candidates a position needs runs from `1` to `17`, and its entropy
  from `0.0003` to `2.969`
- So a fixed `k` is wrong at both ends. `k=10` admits `0.0316` of junk where the
  model is sure and discards `0.1609` of legitimate mass where it is torn

Next time, speed. Every character drawn recomputes the entire preceding context,
and it will turn out that none of that was necessary.
