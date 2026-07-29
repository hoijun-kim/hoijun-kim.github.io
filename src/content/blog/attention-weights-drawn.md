---
title: "어텐션 가중치를 직접 꺼내 본다"
description: "어텐션은 가중평균인데, 그 가중치를 데이터가 정한다. 토큰 여섯 개로 행렬을 실제로 계산해 그려 보고, sqrt(d) 로 나누는 한 줄이 없으면 무슨 일이 벌어지는지 잰다."
date: 2026-08-01
lang: ko
kind: guide
series:
  id: seeing-deep-learning
  part: 8
---

앞의 일곱 편은 층을 쌓고 걸음을 재는 이야기였다. 이번 편은 구조가 다른 층
하나를 본다. 어텐션은 결국 **가중평균**이고, 특이한 점은 그 가중치가 학습된
상수가 아니라 **매번 입력에서 계산된다**는 것이다.

그 가중치는 화면에 나오지 않는다. 꺼내서 그려 보자.

## 토큰 여섯 개

주제 세 개를 두 토큰씩 나눠 가진 임베딩을 만든다. `t0`과 `t3`이 한 주제,
`t1`과 `t4`가, `t2`와 `t5`가 각각 한 주제다.

```python
import numpy as np

X = 2.6 * np.array([
    [1.0, 0.2, 0.0, 0.0],   # t0
    [0.0, 1.0, 0.3, 0.0],   # t1
    [0.0, 0.0, 1.0, 0.2],   # t2
    [0.9, 0.3, 0.0, 0.0],   # t3  - t0 과 같은 주제
    [0.1, 0.9, 0.2, 0.0],   # t4  - t1 과 같은 주제
    [0.0, 0.1, 0.9, 0.3],   # t5  - t2 와 같은 주제
])
d = X.shape[1]

def softmax(a):
    a = a - a.max(-1, keepdims=True)
    e = np.exp(a)
    return e / e.sum(-1, keepdims=True)

A = softmax(X @ X.T / np.sqrt(d))     # 어텐션 가중치
out = A @ X                           # 그 가중치로 만든 가중평균
```

`Q`, `K`, `V` 를 만드는 가중치 행렬은 일부러 뺐다. 세 개를 다 넣으면 무엇이
구조에서 나오고 무엇이 학습에서 나오는지가 섞인다. 여기서는 `Q = K = V = X`
로 두고 **구조만** 본다.

<figure class="fig">
<svg viewBox="0 0 431 421" role="img" aria-label="6x6 어텐션 행렬. 각 행의 합이 1이고, 가장 진한 두 칸은 언제나 자기 자신과 같은 주제를 공유하는 토큰이다">
<g class="hm">
<rect x="72" y="60" width="55" height="55" rx="4" style="opacity:0.981"/>
<text class="v on" x="99.5" y="91.5">0.510</text>
<rect x="130" y="60" width="55" height="55" rx="4" style="opacity:0.114"/>
<text class="v off" x="157.5" y="91.5">0.030</text>
<rect x="188" y="60" width="55" height="55" rx="4" style="opacity:0.087"/>
<text class="v off" x="215.5" y="91.5">0.015</text>
<rect x="246" y="60" width="55" height="55" rx="4" style="opacity:0.763"/>
<text class="v on" x="273.5" y="91.5">0.389</text>
<rect x="304" y="60" width="55" height="55" rx="4" style="opacity:0.131"/>
<text class="v off" x="331.5" y="91.5">0.039</text>
<rect x="362" y="60" width="55" height="55" rx="4" style="opacity:0.089"/>
<text class="v off" x="389.5" y="91.5">0.016</text>
<rect x="72" y="118" width="55" height="55" rx="4" style="opacity:0.106"/>
<text class="v off" x="99.5" y="149.5">0.026</text>
<rect x="130" y="118" width="55" height="55" rx="4" style="opacity:1.000"/>
<text class="v on" x="157.5" y="149.5">0.521</text>
<rect x="188" y="118" width="55" height="55" rx="4" style="opacity:0.125"/>
<text class="v off" x="215.5" y="149.5">0.036</text>
<rect x="246" y="118" width="55" height="55" rx="4" style="opacity:0.125"/>
<text class="v off" x="273.5" y="149.5">0.036</text>
<rect x="304" y="118" width="55" height="55" rx="4" style="opacity:0.666"/>
<text class="v on" x="331.5" y="149.5">0.336</text>
<rect x="362" y="118" width="55" height="55" rx="4" style="opacity:0.142"/>
<text class="v off" x="389.5" y="149.5">0.046</text>
<rect x="72" y="176" width="55" height="55" rx="4" style="opacity:0.087"/>
<text class="v off" x="99.5" y="207.5">0.015</text>
<rect x="130" y="176" width="55" height="55" rx="4" style="opacity:0.135"/>
<text class="v off" x="157.5" y="207.5">0.042</text>
<rect x="188" y="176" width="55" height="55" rx="4" style="opacity:0.979"/>
<text class="v on" x="215.5" y="207.5">0.509</text>
<rect x="246" y="176" width="55" height="55" rx="4" style="opacity:0.087"/>
<text class="v off" x="273.5" y="207.5">0.015</text>
<rect x="304" y="176" width="55" height="55" rx="4" style="opacity:0.114"/>
<text class="v off" x="331.5" y="207.5">0.030</text>
<rect x="362" y="176" width="55" height="55" rx="4" style="opacity:0.762"/>
<text class="v on" x="389.5" y="207.5">0.389</text>
<rect x="72" y="234" width="55" height="55" rx="4" style="opacity:0.904"/>
<text class="v on" x="99.5" y="265.5">0.468</text>
<rect x="130" y="234" width="55" height="55" rx="4" style="opacity:0.151"/>
<text class="v off" x="157.5" y="265.5">0.050</text>
<rect x="188" y="234" width="55" height="55" rx="4" style="opacity:0.093"/>
<text class="v off" x="215.5" y="265.5">0.018</text>
<rect x="246" y="234" width="55" height="55" rx="4" style="opacity:0.749"/>
<text class="v on" x="273.5" y="265.5">0.382</text>
<rect x="304" y="234" width="55" height="55" rx="4" style="opacity:0.171"/>
<text class="v off" x="331.5" y="265.5">0.062</text>
<rect x="362" y="234" width="55" height="55" rx="4" style="opacity:0.096"/>
<text class="v off" x="389.5" y="265.5">0.020</text>
<rect x="72" y="292" width="55" height="55" rx="4" style="opacity:0.146"/>
<text class="v off" x="99.5" y="323.5">0.047</text>
<rect x="130" y="292" width="55" height="55" rx="4" style="opacity:0.912"/>
<text class="v on" x="157.5" y="323.5">0.472</text>
<rect x="188" y="292" width="55" height="55" rx="4" style="opacity:0.125"/>
<text class="v off" x="215.5" y="323.5">0.036</text>
<rect x="246" y="292" width="55" height="55" rx="4" style="opacity:0.172"/>
<text class="v off" x="273.5" y="323.5">0.062</text>
<rect x="304" y="292" width="55" height="55" rx="4" style="opacity:0.667"/>
<text class="v on" x="331.5" y="323.5">0.337</text>
<rect x="362" y="292" width="55" height="55" rx="4" style="opacity:0.143"/>
<text class="v off" x="389.5" y="323.5">0.046</text>
<rect x="72" y="350" width="55" height="55" rx="4" style="opacity:0.095"/>
<text class="v off" x="99.5" y="381.5">0.019</text>
<rect x="130" y="350" width="55" height="55" rx="4" style="opacity:0.174"/>
<text class="v off" x="157.5" y="381.5">0.063</text>
<rect x="188" y="350" width="55" height="55" rx="4" style="opacity:0.895"/>
<text class="v on" x="215.5" y="381.5">0.462</text>
<rect x="246" y="350" width="55" height="55" rx="4" style="opacity:0.096"/>
<text class="v off" x="273.5" y="381.5">0.020</text>
<rect x="304" y="350" width="55" height="55" rx="4" style="opacity:0.141"/>
<text class="v off" x="331.5" y="381.5">0.045</text>
<rect x="362" y="350" width="55" height="55" rx="4" style="opacity:0.765"/>
<text class="v on" x="389.5" y="381.5">0.391</text>
</g><g class="lbl-ax">
<text x="99.5" y="46">t0</text>
<text x="157.5" y="46">t1</text>
<text x="215.5" y="46">t2</text>
<text x="273.5" y="46">t3</text>
<text x="331.5" y="46">t4</text>
<text x="389.5" y="46">t5</text>
<text class="r" x="58" y="91.5">t0</text>
<text class="r" x="58" y="149.5">t1</text>
<text class="r" x="58" y="207.5">t2</text>
<text class="r" x="58" y="265.5">t3</text>
<text class="r" x="58" y="323.5">t4</text>
<text class="r" x="58" y="381.5">t5</text>
<text class="cap" x="244.5" y="22">보는 대상 &rarr;</text>
<text class="cap l" x="6" y="22">보는 쪽 &darr;</text>
</g>
</svg>
<figcaption>어텐션 가중치 행렬. 행 하나가 토큰 하나의 시선이고 합이 1이다. 각 행에서 가장 진한 두 칸은 언제나 자기 자신과 같은 주제를 가진 짝이고, 둘이 행의 0.81 에서 0.90 을 가져간다. 무관한 토큰은 0.015 로 사실상 무시된다.</figcaption>
</figure>

## 행 하나가 한 토큰의 시선이다

행 `t0` 을 보면 자기 자신에 `0.510`, 같은 주제인 `t3` 에 `0.389`, 나머지에는
`0.015` 에서 `0.039` 를 준다. 짝과 무관한 토큰의 비가 `0.389 / 0.015`, 약 26배다.
여섯 행이 모두 같은 모양이다. **모든 행에서 상위 두 칸이 자기 자신과 자기 주제
짝이고**, 그 둘이 가져가는 몫이 `0.81` 에서 `0.90` 이다. 나머지 네 칸을 다 합쳐도
`0.2` 가 안 되고, 그중 가장 큰 값이 `0.063` 이다.

다만 상위 두 칸의 **순서**는 행마다 다르다. `t3`, `t4`, `t5` 는 자기 자신보다
짝에게 더 준다 - 예를 들어 `t3` 은 자신에게 `0.382`, `t0` 에게 `0.468` 이다.
내적은 방향뿐 아니라 크기도 보기 때문이다. `t0` 의 노름이 `2.651`, `t3` 이
`2.467` 이라 `t3` 입장에서는 `t0` 과의 내적이 자기 자신과의 내적보다 크다.
어텐션이 "나는 나를 본다" 는 규칙을 갖고 있지 않다는 뜻이다. 규칙은 유사도
하나뿐이고, 크기도 유사도에 들어간다.

행의 합은 1이다. 어텐션이 하는 일이 **선택**이 아니라 **배분**이기 때문이다.
어디에 얼마나 볼지를 정하고, 그 비율로 값을 섞는다. 이 행렬을 곱한 결과
`A @ X` 가 층의 출력이다.

여기까지에 학습된 것은 하나도 없다. 임베딩이 비슷하면 내적이 크고, 내적이
크면 소프트맥스가 큰 몫을 준다. 실제 트랜스포머는 `X` 대신 `XW_q`, `XW_k` 를
쓰지만, 그 `W` 들이 하는 일은 **어떤 유사도를 볼지 고르는 것**이지 이 구조를
바꾸는 게 아니다.

## sqrt(d) 로 나누는 한 줄

`X @ X.T` 뒤에 `/ np.sqrt(d)` 가 붙어 있다. 이게 없으면 어떻게 되는지 차원을
올려 가며 재 본다. 무작위 벡터 여덟 개로 8×8 어텐션을 만든다.

```python
for d in (4, 16, 64, 256, 1024):
    rng = np.random.default_rng(0)
    for _ in range(200):                       # 200회 평균
        q = rng.standard_normal((8, d))
        k = rng.standard_normal((8, d))
        L = q @ k.T
        raw, scaled = softmax(L), softmax(L / np.sqrt(d))
```

```
    d   로짓 표준편차   최대 확률(그대로)   최대 확률(나눔)   엔트로피(그대로)   엔트로피(나눔)
    4          1.93            0.526            0.342            1.290          1.750
   16          3.88            0.755            0.359            0.662          1.732
   64          7.94            0.872            0.357            0.323          1.728
  256         15.81            0.937            0.361            0.157          1.719
 1024         31.89            0.968            0.363            0.078          1.716
```

여덟 개에 고르게 배분했을 때의 엔트로피가 `2.079` 다.

로짓의 표준편차가 차원을 따라 커진다. 성분이 분산 1인 두 벡터의 내적은 항이
`d` 개 더해진 합이라 표준편차가 `sqrt(d)` 다. 측정값이 `1.93, 3.88, 7.94,
15.81, 31.89` 로, `2, 4, 8, 16, 32` 위에 그대로 앉는다.

소프트맥스는 입력 차이가 커지면 뾰족해진다. 그래서 `d=1024` 에서 최대 확률이
`0.968` 로 올라가고 엔트로피가 `0.078` 로 떨어진다. 고르게 볼 때가 `2.079`
니까 **거의 한 곳만 보고 나머지는 버린다.** 가중평균이라기보다 그냥 선택이 된다.

`sqrt(d)` 로 나누면 로짓의 표준편차가 차원과 무관하게 1 부근으로 돌아온다.
표에서 차원이 256배 늘어나는 동안 최대 확률은 `0.342`에서 `0.363`, 엔트로피는
`1.750`에서 `1.716` 으로 사실상 움직이지 않는다.

## 진짜 문제는 기울기다

뾰족해지는 게 왜 나쁜가. 3편의 관점으로 보면 답이 나온다. 소프트맥스의 야코비
행렬은 대각이 `p_i(1-p_i)`, 비대각이 `-p_i p_j` 다. 확률이 한 곳에 몰려 `p` 가
0이나 1에 붙으면 두 항이 모두 0으로 죽는다. 아래는 대각합 `sum p(1-p)` 를 잰
것이고, 이게 작다는 건 야코비 전체가 작다는 뜻이다.

```
    d   sum p(1-p) (그대로)   sum p(1-p) (나눔)
    4               0.6052              0.7747
   16               0.3397              0.7691
   64               0.1809              0.7705
  256               0.0908              0.7668
 1024               0.0465              0.7651
```

나누지 않으면 이 값이 차원을 따라 계속 줄어서 `d=1024` 에서 `0.0465` 가 된다.
나눈 쪽은 `0.77` 근처에서 꿈쩍도 안 한다. **16.5배 차이다.** 4편에서 본 것과
같은 종류의 사고다 - 순전파 값이 포화하면 그 자리의 미분이 사라진다.
`sqrt(d)` 는 성능 튜닝이 아니라 **학습이 시작되게 하는 조건**이다.

## 어텐션은 순서를 모른다

마지막으로 하나. 위 행렬은 토큰의 **내용**만 보고 만들어졌다. 위치는 어디에도
안 들어갔다.

```python
perm = [3, 1, 5, 0, 4, 2]
A2 = softmax(X[perm] @ X[perm].T / np.sqrt(d))
np.allclose(A2 @ X[perm], (A @ X)[perm])   # True
```

입력 순서를 섞으면 출력도 정확히 같은 순서로 섞인다. 값이 달라지는 게 아니라
**자리만 바뀐다.** 즉 어텐션에게 "앞" 과 "뒤" 는 없다.

문장에서 순서는 의미다. 그래서 트랜스포머는 위치 정보를 따로 넣는다. 위치
인코딩이 왜 필요한지는 이 한 줄의 실험이 전부 설명한다 - 넣지 않으면 모델이
단어 순서를 볼 방법이 아예 없다.

## 그래서

- 어텐션은 가중평균이고, 가중치는 입력에서 계산된다. 행의 합이 1이다
- 그 행렬은 꺼내 볼 수 있다. 이 예에서 모든 행의 상위 두 칸이 자기 자신과 주제
  짝이고, 같은 주제 짝 `0.389` 대 무관한 토큰 `0.015` 로 26배 차이가 난다
- `sqrt(d)` 는 로짓이 차원을 따라 `sqrt(d)` 로 커지는 것을 되돌린다. 없으면
  `d=1024` 에서 최대 확률 `0.968`, 엔트로피 `0.078` 로 포화한다
- 포화의 대가는 기울기다. `d=1024` 에서 `0.0465` 대 `0.7651`, 16.5배 차이가 난다
- 어텐션은 순서에 대해 아무것도 모른다. 위치 인코딩은 장식이 아니라 누락된
  정보를 채우는 것이다

여덟 편이다. 텐서가 놓인 자리에서 시작해 걸음, 미분, 층, 배치, 정규화,
일반화를 지나 층 하나가 스스로 가중치를 계산하는 데까지 왔다. 매번 재고 그렸다.

다음 편은 방금 남긴 구멍을 메운다. 어텐션이 순서를 모른다면 순서를 어떻게
집어넣는지, 위치 인코딩을 재 본다.
