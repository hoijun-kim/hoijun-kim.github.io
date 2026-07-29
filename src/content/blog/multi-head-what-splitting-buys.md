---
title: "머리를 여덟으로 쪼개면 무엇이 달라지나"
description: "파라미터 수가 똑같은데 왜 헤드를 나누나. 평균 하나로는 두 가지를 못 나른다는 것을 재고, 헤드 하나에 걸린 랭크 상한이 어떤 패턴을 아예 불가능하게 만드는지 본다."
date: 2026-08-10
lang: ko
kind: guide
series:
  id: seeing-deep-learning
  part: 10
---

9편까지 오면 어텐션 한 덩이가 완성된다. 내용으로 가중치를 만들고, 위치를
더해 순서를 알게 했다. 실제 트랜스포머는 여기서 하나를 더 한다. 이 덩이를
**여덟 개로 쪼갠다.**

쪼개면 뭐가 좋아지는지가 이번 편이다. 먼저 이상한 점부터.

## 파라미터는 하나도 안 는다

`d_model = 64` 를 헤드 하나로 쓰든 여덟로 쪼개든 가중치 행렬은 똑같다.

```
헤드 1개 (dh=64)   Wq, Wk, Wv, Wo 각 64x64 = 4,096 개  |  넷 합쳐 16,384 개
헤드 8개 (dh=8)    Wq, Wk, Wv, Wo 각 64x64 = 4,096 개  |  넷 합쳐 16,384 개
```

쪼갠다는 건 같은 `64` 차원을 `8` 씩 여덟 토막으로 잘라 각 토막에서 **따로**
어텐션을 하고, 결과를 다시 이어 붙여 `Wo` 를 곱하는 것이다. 파라미터도
곱셈 횟수도 같다. 공짜로 얻는 게 있다면 그건 구조에서 나온다.

## 평균 하나로는 두 가지를 못 나른다

핵심은 8편의 한 문장에 이미 있다. 어텐션은 **가중평균**이다. 행 하나가 확률
분포 하나고, 분포 하나는 결과를 **한 점**으로 만든다.

토큰이 두 가지를 동시에 필요로 하면 어떻게 되나. 주제가 같은 짝의 값도
필요하고, 바로 옆자리의 값도 필요하다고 하자. 층 출력에서 그 둘을 **모두**
읽어낼 수 있는지 재 본다. 판독은 최적 선형사상으로 하고, 토큰을 값 차원의
1600배로 두어 우연히 맞을 여지를 없앤다.

```
헤드 1개, 짝에만 주기 (a=1.00)     상대오차 0.7069
헤드 1개, 반반 나누기 (a=0.50)     상대오차 0.7075
헤드 1개, 비율을 어떻게 잡아도      최선이 0.7069
헤드 2개, 각각 하나씩              상대오차 0.0000
```

절반만 복원했을 때의 값이 `sqrt(1/2) = 0.7071` 이다. 헤드 하나는 정확히 그
자리에 있다 - **둘 중 하나는 통째로 잃는다.**

주목할 것은 가운데 줄이다. 반씩 나눠 주는 게 도움이 될 것 같지만 `0.7075` 로
오히려 **더 나쁘다.** 섞어 놓으면 둘 다 못 쓰게 되기 때문이다. `0.5(v_짝 + v_이웃)`
이라는 한 점에서 `v_짝` 과 `v_이웃` 을 따로 뽑아낼 방법이 없다.

비율을 0에서 1까지 훑어도 최선은 한쪽에 다 주는 것이다. 헤드 하나에게는
**타협이 손해다.** 골라야 한다.

헤드가 둘이면 고를 필요가 없다. 각자 하나씩 맡고, 결과가 `Wo` 의 서로 다른
행 블록을 통과해 더해지므로 섞이지 않는다. 오차가 `0.0000` 이다.

## 그래서 헤드는 서로 다른 것을 본다

8편의 토큰 여섯 개에 9편의 위치 인코딩을 붙이고, 앞 네 차원(내용)과 뒤 네
차원(위치)을 각각 다른 헤드에 주면 이렇게 갈린다.

<figure class="fig">
<svg viewBox="0 0 522 293" role="img" aria-label="같은 입력에 대한 두 헤드의 어텐션 행렬. 왼쪽은 주제가 같은 토큰을 찾고 오른쪽은 양옆 자리만 본다">
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
<text class="cap l" x="27" y="20">행 = 보는 쪽</text>
<text class="ttl2" x="142.5" y="40">헤드 A - 내용</text>
<text class="ttl2" x="407.5" y="40">헤드 B - 위치</text>
</g>
</svg>
<figcaption>같은 입력에 대한 두 헤드의 어텐션. 왼쪽은 주제가 같은 토큰을 찾아 짝에 0.39 를 주고, 오른쪽은 내용을 전혀 안 보고 양옆에만 0.10 씩 준다. 비대각 성분의 상관계수가 -0.374 로, 한쪽이 보는 자리를 다른 쪽은 오히려 덜 본다.</figcaption>
</figure>

헤드 A 는 8편 그대로다. 자기 자신에 `0.510`, 주제 짝에 `0.389`, 양옆에는
`0.025` 밖에 안 준다. 헤드 B 는 정반대다. 자기 자신 `0.797`, 양옆에 `0.101`
씩, 그리고 주제 짝에는 `0.000` 이다.

B 는 삼중대각이다. 이웃 `0.101`, 두 칸 `0.001`, 세 칸 `0.000` 으로 한 칸 멀어질
때마다 두 자릿수씩 떨어진다. 내용은 아예 안 본다.

두 행렬의 비대각 성분 상관계수가 `-0.374` 다. 우연히 다른 게 아니라 **한쪽이
보는 자리를 다른 쪽은 오히려 덜 본다.**

여기서는 어느 차원을 어느 헤드에 줄지 내가 정했다. 실제 모델은 그걸 `Wq`, `Wk`
가 배운다. 구조가 보장하는 건 "여러 개를 따로 볼 자리가 있다" 까지고, 무엇을
볼지는 학습이 정한다.

## 두 번째 이유: 랭크 상한

헤드를 쪼개면 잃는 것도 있다. 헤드 하나의 로짓 행렬은 `Q_h K_h^T` 이고, `Q_h`
와 `K_h` 의 폭이 `dh` 이므로 **랭크가 `dh` 를 못 넘는다.**

```
헤드 1개 (dh=64)         토큰 12개 로짓 12x12  랭크 12
헤드 8개 중 하나 (dh=8)  토큰 12개 로짓 12x12  랭크 8
```

이게 진짜 제약인지 보려면 랭크가 높은 패턴을 시켜 보면 된다. "세 칸 뒤를
봐라" 는 순열 행렬이고 랭크가 `12` 다. 랭크 `k` 로 근사하면 이렇게 된다.

```
랭크  2   상대오차 0.9129   목표를 맞힌 토큰 비율 0.17
랭크  4   상대오차 0.8165   목표를 맞힌 토큰 비율 0.33
랭크  8   상대오차 0.5774   목표를 맞힌 토큰 비율 0.67
랭크 12   상대오차 0.0000   목표를 맞힌 토큰 비율 1.00
```

오차가 정확히 `sqrt((n-k)/n)` 이다. 순열 행렬은 특잇값이 전부 같아서 랭크를
하나 버릴 때마다 정확히 `1/n` 씩 잃는다. 맞히는 비율도 정확히 `k/n` 이다.

즉 `dh=8` 인 헤드는 토큰 12개짜리 "세 칸 뒤" 를 **원리상 완전히 표현할 수
없다.** 12개 중 8개까지가 한계다. 헤드를 잘게 쪼갤수록 이 천장이 낮아진다.

여덟이라는 숫자는 그래서 타협이다. 많이 쪼갤수록 따로 볼 수 있는 것이 늘지만,
하나하나가 표현할 수 있는 패턴이 단순해진다.

## 이어 붙이는 것은 더하는 것이다

마지막으로 구현 한 줄. 보통 헤드들을 이어 붙인 뒤 `Wo` 를 곱한다고 쓰는데,
`Wo` 를 행 방향으로 헤드마다 잘라 보면 그건 **헤드별 기여의 합**과 같다.

```python
concat = np.hstack(heads) @ Wo
summed = sum(heads[h] @ Wo[h*dh:(h+1)*dh] for h in range(H))
np.abs(concat - summed).max()        # 6.9e-17
```

부동소수점 잡음 말고는 차이가 없다. 헤드끼리는 어텐션 안에서 **한 번도 만나지
않는다.** 각자 자기 평균을 내고, 마지막에 각자의 결과를 잔차 흐름에 더할 뿐이다.

이 관점이 실용적이기도 하다. 헤드 하나가 무엇을 하는지 보려면 그 항만 남기고
나머지를 0으로 두면 된다. 더하기라서 그게 성립한다.

## 정직하게 덧붙이면

헤드가 반드시 서로 다른 일을 하도록 강제하는 장치는 어디에도 없다. 위 그림에서
둘이 갈린 건 내가 차원을 나눠 줬기 때문이고, 실제로 학습된 모델에서는 상당수
헤드가 서로 비슷해져서 잘라내도 성능이 거의 안 떨어진다는 보고가 꾸준히 있다.
구조는 **자리를 마련해 줄 뿐**이고, 그 자리를 다 쓰는지는 별개 문제다.

## 그래서

- 헤드를 나눠도 파라미터와 곱셈 횟수는 같다. `64x64` 넉 장, 합쳐 `16,384` 개 그대로다
- 어텐션 하나는 가중평균 하나다. 두 가지가 필요하면 하나는 잃는다 - 상대오차
  `0.7069`, 이론값 `sqrt(1/2)`. 반씩 섞으면 `0.7075` 로 더 나쁘다
- 헤드 둘이면 오차가 `0.0000` 이다. 서로 다른 자리에 써 놓고 마지막에 더하기
  때문이다
- 대가는 랭크다. `dh=8` 짜리 헤드는 랭크 12 패턴을 8까지밖에 못 흉내 낸다.
  맞히는 비율이 정확히 `k/n`
- 이어 붙인 뒤 곱하는 것은 헤드별 기여를 더하는 것과 같다. 차이 `6.9e-17`

열 편이다. 다음 편에서는 어텐션 옆에 붙어 있는데 아무도 안 보는 쪽을 본다.
파라미터의 3분의 2가 거기 있는데도 이름이 그냥 '피드포워드' 인 층이다.
