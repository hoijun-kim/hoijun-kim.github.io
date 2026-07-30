---
title: "A tensor is one-dimensional"
description: "Why reshape is free and transpose never moves data. Once you have seen how an array actually lies in memory, half the error messages you will meet later are explained in advance."
date: 2025-07-29
lang: en
kind: guide
series:
  id: seeing-deep-learning
  part: 1
---

How long does it take to turn a `(3, 4)` array into a `(4, 3)` one? Twelve
values to move, so about twelve operations. In fact **nothing moves at all**.
To see why, look at how the array lies in memory.

## There is no such thing as a multidimensional array

Memory is one-dimensional. Addresses run 0, 1, 2 in a single line, and there is
no way to lay a second dimension on top of that. A NumPy array is no exception.
The values sit in one row, and "two-dimensional" is nothing but a rule for
**what step size to read them at**.

That step is called the stride.

```python
import numpy as np

a = np.arange(12, dtype=np.int32)
b = a.reshape(3, 4)

print(a.strides)          # (4,)
print(b.shape, b.strides) # (3, 4) (16, 4)
print(np.shares_memory(a, b))
```

```
(4,)
(3, 4) (16, 4)
True
```

An `int32` is 4 bytes. Strides of `(16, 4)` say: **to move down one row skip 16
bytes, to move across one column skip 4**. Sixteen is 4 bytes times 4 columns.
That is the whole of it. `reshape` touched no values. It wrote down two
different numbers, which is why `shares_memory` is True.

<figure class="fig">
<svg viewBox="0 0 460 214" role="img" aria-label="Twelve values in one row, read at two different strides out of the same buffer">
  <g class="guide"><line x1="19" y1="54" x2="19" y2="204"/><line x1="57" y1="54" x2="57" y2="204"/><line x1="95" y1="54" x2="95" y2="204"/><line x1="133" y1="54" x2="133" y2="204"/><line x1="171" y1="54" x2="171" y2="204"/><line x1="209" y1="54" x2="209" y2="204"/><line x1="247" y1="54" x2="247" y2="204"/><line x1="285" y1="54" x2="285" y2="204"/><line x1="323" y1="54" x2="323" y2="204"/><line x1="361" y1="54" x2="361" y2="204"/><line x1="399" y1="54" x2="399" y2="204"/><line x1="437" y1="54" x2="437" y2="204"/></g>
  <text class="cap" x="0" y="14">memory - one buffer, twelve 4-byte slots</text>
  <g class="cells">
    <rect x="0" y="24" width="456" height="30" rx="5"/>
    <g class="tick">
      <line x1="38" y1="24" x2="38" y2="54"/><line x1="76" y1="24" x2="76" y2="54"/>
      <line x1="114" y1="24" x2="114" y2="54"/><line x1="152" y1="24" x2="152" y2="54"/>
      <line x1="190" y1="24" x2="190" y2="54"/><line x1="228" y1="24" x2="228" y2="54"/>
      <line x1="266" y1="24" x2="266" y2="54"/><line x1="304" y1="24" x2="304" y2="54"/>
      <line x1="342" y1="24" x2="342" y2="54"/><line x1="380" y1="24" x2="380" y2="54"/>
      <line x1="418" y1="24" x2="418" y2="54"/>
    </g>
  </g>
  <g class="val">
    <text x="19" y="44">0</text><text x="57" y="44">1</text><text x="95" y="44">2</text>
    <text x="133" y="44">3</text><text x="171" y="44">4</text><text x="209" y="44">5</text>
    <text x="247" y="44">6</text><text x="285" y="44">7</text><text x="323" y="44">8</text>
    <text x="361" y="44">9</text><text x="399" y="44">10</text><text x="437" y="44">11</text>
  </g>
  <text class="cap" x="0" y="92">b, strides (16, 4) - four in a row</text>
  <g class="hop a">
    <path d="M 19 100 L 57 100 L 95 100 L 133 100"/><circle cx="19" cy="100" r="3.2"/><circle cx="57" cy="100" r="3.2"/><circle cx="95" cy="100" r="3.2"/><circle cx="133" cy="100" r="3.2"/>
    <path d="M 171 100 L 209 100 L 247 100 L 285 100"/><circle cx="171" cy="100" r="3.2"/><circle cx="209" cy="100" r="3.2"/><circle cx="247" cy="100" r="3.2"/><circle cx="285" cy="100" r="3.2"/>
    <path d="M 323 100 L 361 100 L 399 100 L 437 100"/><circle cx="323" cy="100" r="3.2"/><circle cx="361" cy="100" r="3.2"/><circle cx="399" cy="100" r="3.2"/><circle cx="437" cy="100" r="3.2"/>
  </g>
  <g class="row-lbl">
    <text x="76" y="122">row 0</text><text x="228" y="122">row 1</text><text x="380" y="122">row 2</text>
  </g>
  <text class="cap" x="0" y="158">b.T, strides (4, 16) - the two numbers swapped</text>
  <g class="hop c">
    <path d="M 19 162 L 171 162 L 323 162"/><circle cx="19" cy="162" r="3.2"/><circle cx="171" cy="162" r="3.2"/><circle cx="323" cy="162" r="3.2"/>
    <path d="M 57 174 L 209 174 L 361 174"/><circle cx="57" cy="174" r="3.2"/><circle cx="209" cy="174" r="3.2"/><circle cx="361" cy="174" r="3.2"/>
    <path d="M 95 186 L 247 186 L 399 186"/><circle cx="95" cy="186" r="3.2"/><circle cx="247" cy="186" r="3.2"/><circle cx="399" cy="186" r="3.2"/>
    <path d="M 133 198 L 285 198 L 437 198"/><circle cx="133" cy="198" r="3.2"/><circle cx="285" cy="198" r="3.2"/><circle cx="437" cy="198" r="3.2"/>
  </g>
<g class="pulses">
<path class="pulse b" pathLength="1" d="M 19 100 L 57 100 L 95 100 L 133 100" style="--d: 0.0s"/>
<path class="pulse b" pathLength="1" d="M 171 100 L 209 100 L 247 100 L 285 100" style="--d: 0.5s"/>
<path class="pulse b" pathLength="1" d="M 323 100 L 361 100 L 399 100 L 437 100" style="--d: 1.0s"/>
<path class="pulse" pathLength="1" d="M 19 162 L 171 162 L 323 162" style="--d: 0.0s"/>
<path class="pulse" pathLength="1" d="M 57 174 L 209 174 L 361 174" style="--d: 0.45s"/>
<path class="pulse" pathLength="1" d="M 95 186 L 247 186 L 399 186" style="--d: 0.9s"/>
<path class="pulse" pathLength="1" d="M 133 198 L 285 198 L 437 198" style="--d: 1.35s"/>
</g>
</svg>
<figcaption>One buffer, the same twelve values. Only the stride changed.</figcaption>
</figure>

## Transposing swaps two numbers

```python
c = b.T
print(c.shape, c.strides)          # (4, 3) (4, 16)
print(np.shares_memory(a, c))      # True
```

```
(4, 3) (4, 16)
True
```

`(16, 4)` became `(4, 16)`. That is all. Leave the values alone and write down
"4 to move along a row, 16 to move along a column", and the same memory reads
as the transposed matrix. Transposing a million-by-million matrix costs exactly
the same.

Address arithmetic is one line.

```
offset = index[0]*stride[0] + index[1]*stride[1] + ...
```

Check it. The offset of `b[2, 1]` is `2x16 + 1x4 = 36` bytes, which divided by 4
is slot 9 of the buffer.

```python
print(b[2, 1])                                    # 9
print(2 * b.strides[0] + 1 * b.strides[1])        # 36
```

```
9
36
```

Indexing is two multiplications and an addition. Slicing is the same: `b[:, 1:3]`
moves the starting offset and inherits the strides untouched.

## When it is not free

So far everything looks free. It is not. The moment something is asked for that
strides cannot express, a copy happens.

```python
c = b.T                       # (4, 3), strides (4, 16)
print(np.shares_memory(a, c.reshape(12)))
print(np.shares_memory(a, c.ravel()))
```

```
False
False
```

Flattening `c` would have to produce `0, 4, 8, 1, 5, 9, ...`, and there is no
**single constant step** that walks that order. So NumPy copies into a fresh
buffer, and that is the one operation here that genuinely costs O(n).

This is what that message in a deep-learning framework is about. In the same
situation PyTorch refuses with `view size is not compatible with input tensor's
size and stride`. `view` promises to do only what a stride change can do;
`reshape` will fall back to copying. The two names exist because of performance.

The difference between `ravel` and `flatten` is the same line: `ravel` returns a
view where it can, `flatten` always copies. Above, `c` is non-contiguous, so
both copied.

## Broadcasting is a stride of zero

One more. Stretching a `(2, 3)` array to `(4, 2, 3)` looks like it should cost
four times the memory.

```python
e = np.arange(6, dtype=np.int32).reshape(2, 3)
print(np.broadcast_to(e, (4, 2, 3)).strides)
```

```
(0, 12, 4)
```

The first axis has stride **0**. "Moving one step along that axis leaves the
address unchanged", so the same six values are read four times. No copy.
Broadcasting is fast not because of a clever algorithm but because someone
wrote down a zero.

## So

An array is not a grid of values. It is **one buffer plus a rule for reading
it**. Hold that picture and the following are all the same story.

- why `reshape`, `transpose` and slicing return instantly
- why some operations refuse, complaining about contiguity
- why one call to `.contiguous()` makes what follows faster
- why broadcasting costs no memory

The next part looks at loss rather than values. It draws the loss surface of a
two-parameter problem and follows exactly what steps gradient descent takes
across it.
