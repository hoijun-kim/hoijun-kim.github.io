---
title: "텐서는 사실 1차원이다"
description: "reshape 은 왜 공짜이고 transpose 는 왜 데이터를 옮기지 않는가. 배열이 메모리에 어떻게 놓여 있는지 한 번 보고 나면, 나중에 만날 에러 메시지 절반이 미리 설명된다."
date: 2026-07-29
lang: ko
kind: guide
series:
  id: seeing-deep-learning
  part: 1
draft: true
---

`(3, 4)` 짜리 배열을 `(4, 3)` 으로 바꾸는 데 얼마나 걸릴까. 12개를 옮겨 담아야
하니 12번쯤 걸릴 것 같지만, 실제로는 **아무것도 옮기지 않는다**. 왜 그런지
보려면 배열이 메모리에 어떻게 누워 있는지부터 봐야 한다.

## 다차원 배열 같은 건 없다

메모리는 1차원이다. 주소가 0, 1, 2 로 이어지는 한 줄이고, 그 위에 2차원이나
3차원을 올려놓을 방법은 없다. NumPy 배열도 예외가 아니다. 값들은 한 줄로
놓여 있고, "2차원"은 그 줄을 **어떤 보폭으로 읽을지** 정한 규칙일 뿐이다.

그 보폭을 stride 라고 부른다.

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

`int32` 하나가 4바이트다. `b` 의 stride 가 `(16, 4)` 라는 건, **행을 하나 내려가려면
16바이트를 건너뛰고, 열을 하나 옮기려면 4바이트를 건너뛰라**는 뜻이다. 16은
4바이트 × 4열이다. 그게 전부다. `reshape` 은 값을 만지지 않았다. 숫자 두 개를
바꿔 적었을 뿐이고, `shares_memory` 가 True 인 이유가 그것이다.

<figure class="fig">
<svg viewBox="0 0 460 210" role="img" aria-label="한 줄로 놓인 12개 값 위에서, 서로 다른 stride 두 개가 같은 버퍼를 다르게 읽는 그림">
  <text class="cap" x="0" y="14">메모리 (버퍼 하나, 4바이트씩 12칸)</text>
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
  <text class="cap" x="0" y="92">b, strides (16, 4) - 옆으로 4씩</text>
  <g class="hop a">
    <path d="M 19 100 L 57 100 L 95 100 L 133 100"/><circle cx="19" cy="100" r="3.2"/><circle cx="57" cy="100" r="3.2"/><circle cx="95" cy="100" r="3.2"/><circle cx="133" cy="100" r="3.2"/>
    <path d="M 171 100 L 209 100 L 247 100 L 285 100"/><circle cx="171" cy="100" r="3.2"/><circle cx="209" cy="100" r="3.2"/><circle cx="247" cy="100" r="3.2"/><circle cx="285" cy="100" r="3.2"/>
    <path d="M 323 100 L 361 100 L 399 100 L 437 100"/><circle cx="323" cy="100" r="3.2"/><circle cx="361" cy="100" r="3.2"/><circle cx="399" cy="100" r="3.2"/><circle cx="437" cy="100" r="3.2"/>
  </g>
  <g class="row-lbl">
    <text x="19" y="122">행 0</text><text x="171" y="122">행 1</text><text x="323" y="122">행 2</text>
  </g>
  <text class="cap" x="0" y="158">b.T, strides (4, 16) - 두 숫자를 맞바꿨을 뿐</text>
  <g class="hop c">
    <path d="M 19 166 L 171 166 L 323 166"/><circle cx="19" cy="166" r="3.2"/><circle cx="171" cy="166" r="3.2"/><circle cx="323" cy="166" r="3.2"/>
    <path d="M 57 180 L 209 180 L 361 180"/><circle cx="57" cy="180" r="3.2"/><circle cx="209" cy="180" r="3.2"/><circle cx="361" cy="180" r="3.2"/>
    <path d="M 95 194 L 247 194 L 399 194"/><circle cx="95" cy="194" r="3.2"/><circle cx="247" cy="194" r="3.2"/><circle cx="399" cy="194" r="3.2"/>
  </g>
</svg>
<figcaption>같은 버퍼, 같은 12개 값. 바뀐 것은 읽는 보폭뿐이다.</figcaption>
</figure>

## 전치는 숫자 두 개를 맞바꾸는 일이다

```python
c = b.T
print(c.shape, c.strides)          # (4, 3) (4, 16)
print(np.shares_memory(a, c))      # True
```

```
(4, 3) (4, 16)
True
```

`(16, 4)` 가 `(4, 16)` 이 됐다. 그것뿐이다. 값은 그대로 두고 "행으로 갈 때 4,
열로 갈 때 16" 이라고 다시 적으니, 같은 메모리가 전치된 행렬로 읽힌다.
100만 × 100만 행렬을 전치해도 이 비용은 똑같다.

주소 계산은 한 줄짜리 공식이다.

```
offset = index[0]*stride[0] + index[1]*stride[1] + ...
```

확인해 보자. `b[2, 1]` 의 오프셋은 `2×16 + 1×4 = 36` 바이트고, 4로 나누면 버퍼의
9번 칸이다.

```python
print(b[2, 1])                                    # 9
print(2 * b.strides[0] + 1 * b.strides[1])        # 36
```

```
9
36
```

인덱싱은 곱셈 두 번과 덧셈 한 번이다. 슬라이스도 마찬가지여서, `b[:, 1:3]` 은
시작 오프셋만 옮기고 stride 는 그대로 물려받는다.

## 공짜가 아닌 순간

여기까지만 보면 모든 게 공짜 같지만, 아니다. stride 로 표현할 수 없는 요구가
들어오면 그때 복사가 일어난다.

```python
c = b.T                       # (4, 3), strides (4, 16)
print(np.shares_memory(a, c.reshape(12)))
print(np.shares_memory(a, c.ravel()))
```

```
False
False
```

`c` 를 한 줄로 펴려면 값들이 `0, 4, 8, 1, 5, 9, ...` 순서로 나와야 하는데, 이
순서를 **하나의 일정한 보폭**으로 훑을 방법이 없다. 그래서 NumPy 는 새 버퍼에
옮겨 담는다. 이때 걸리는 비용이 진짜 O(n) 이다.

이게 딥러닝 프레임워크에서 만나는 그 메시지의 정체다. PyTorch 는 같은 상황에서
`view size is not compatible with input tensor's size and stride` 라고 거절한다.
`view` 는 "stride 만 고쳐서 되는 일"만 하겠다는 약속이고, `reshape` 은 안 되면
복사까지 하겠다는 뜻이다. 이름이 다른 이유가 성능이었다.

`ravel` 과 `flatten` 의 차이도 여기서 갈린다. `ravel` 은 가능하면 뷰를 주고,
`flatten` 은 언제나 복사한다. 위 예에서는 `c` 가 비연속이라 둘 다 복사했다.

## 브로드캐스팅의 정체는 stride 0 이다

마지막으로 하나 더. `(2, 3)` 배열을 `(4, 2, 3)` 으로 늘리면 메모리가 4배로
늘어날 것 같지만,

```python
e = np.arange(6, dtype=np.int32).reshape(2, 3)
print(np.broadcast_to(e, (4, 2, 3)).strides)
```

```
(0, 12, 4)
```

첫 축의 stride 가 **0** 이다. "그 축으로 한 칸 가도 주소는 그대로" 라는 뜻이고,
그래서 같은 6개 값을 네 번 읽는다. 복사는 없다. 브로드캐스팅이 빠른 이유는
영리한 알고리즘이 아니라, 그냥 0을 적어둔 것이다.

## 그래서

배열은 값의 격자가 아니라 **버퍼 하나 + 읽는 규칙**이다. 이 그림을 갖고 있으면
다음이 전부 같은 이야기로 보인다.

- `reshape`, `transpose`, 슬라이스가 왜 즉시 끝나는가
- 왜 어떤 연산은 "contiguous 하지 않다" 며 거절하는가
- 왜 `.contiguous()` 를 한 번 부르면 그다음이 빨라지는가
- 왜 브로드캐스팅에 메모리가 안 드는가

다음 편에서는 값이 아니라 **손실**을 볼 차례다. 파라미터 두 개짜리 문제의 손실
지형을 그려놓고, 경사하강법이 그 위에서 정확히 어떤 걸음을 걷는지 따라간다.
