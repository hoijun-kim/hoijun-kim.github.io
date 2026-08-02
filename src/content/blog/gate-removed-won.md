---
title: "게이트 하나를 없앤 쪽이 이겼다"
description: "GRU 는 LSTM 의 입력 게이트와 망각 게이트를 하나로 묶는다. 묶어도 되는 이유가 LSTM 이 원래 둘을 안 따로 쓰기 때문일 거라 봤는데, 재 보니 따로 쓴다 - 상관 0.071. 그런데도 진다. 같은 폭에서 파라미터를 23% 덜 쓰고도 GRU 가 앞선다."
date: 2025-12-01
lang: ko
kind: guide
series:
  id: not-attention
  part: 3
---

2편에서 LSTM 은 게이트 세 개로 셀 상태를 지킨다는 것을 봤다. GRU 는 같은 일을
게이트 두 개로 하고 셀 상태를 따로 두지도 않는다. 뭘 버렸는데 1편에서 잊는
속도가 거의 같았고, 7편에서는 손실이 더 낮다.

## GRU 한 걸음

```python
gi = W_ih @ x + b_ih       # 세 덩어리
gh = W_hh @ h + b_hh

r = sigmoid(gi_r + gh_r)          # 리셋 게이트
z = sigmoid(gi_z + gh_z)          # 갱신 게이트
n = tanh(gi_n + r * gh_n)         # 후보. r 이 옛 상태 쪽에만 곱해진다

h = z * h + (1 - z) * n
```

마지막 줄이 LSTM 의 `c = f * c + i * g` 자리인데 모양이 다르다. LSTM 은 남길
양 `f` 와 넣을 양 `i` 를 **따로** 정하고, GRU 는 `z` 하나로 둘 다 정한다.
`z` 만큼 남기고 나머지 `1 - z` 만큼 넣는다.

`r` 은 LSTM 에 없는 것이다. 후보를 만들 때 옛 상태를 얼마나 볼지 정한다. 그러니
GRU 는 "LSTM 에서 게이트 하나를 뺀 것" 이 아니라 다르게 짠 것이다.

2편처럼 학습된 가중치로 손으로 돌려서 `nn.GRU` 와 최대 `7.90e-07` 차이로 같은
것을 확인하고, 아래 숫자는 거기서 꺼냈다.

```
             평균     5%      50%     95%
갱신 z      0.405  0.032   0.370   0.883
리셋 r      0.629  0.120   0.690   0.971
```

## LSTM 은 그 둘을 따로 쓴다

묶어도 괜찮은 이유로 제일 그럴듯한 것은, LSTM 도 사실은 `i` 를 대충 `1 - f` 로
쓰고 있어서 자유도가 놀고 있다는 것이다. 그러면 GRU 가 묶어도 잃는 게 없다.

재 보면 아니다.

<figure class="fig">
<svg viewBox="0 0 460 250" role="img" aria-label="왼쪽: LSTM 의 입력 게이트와 1 에서 망각 게이트를 뺀 값이 놓인 자리. 대각선에 몰려 있지 않고 사각형 전체에 퍼져 있어서 두 게이트가 따로 움직인다. 오른쪽: LSTM 망각 게이트와 GRU 갱신 게이트에서 나오는 유닛별 반감기로, 둘 다 세 자를 못 넘는다">
<text class="ttl2 l" x="32.0" y="18">입력 게이트 대 1 - 망각 게이트</text>
<g class="hm2">
<rect x="62.0" y="207.0" width="7.4" height="7.4" opacity="0.042"/>
<rect x="69.0" y="207.0" width="7.4" height="7.4" opacity="0.098"/>
<rect x="76.0" y="207.0" width="7.4" height="7.4" opacity="0.246"/>
<rect x="83.0" y="207.0" width="7.4" height="7.4" opacity="0.271"/>
<rect x="90.0" y="207.0" width="7.4" height="7.4" opacity="0.268"/>
<rect x="97.0" y="207.0" width="7.4" height="7.4" opacity="0.291"/>
<rect x="104.0" y="207.0" width="7.4" height="7.4" opacity="0.299"/>
<rect x="111.0" y="207.0" width="7.4" height="7.4" opacity="0.311"/>
<rect x="118.0" y="207.0" width="7.4" height="7.4" opacity="0.348"/>
<rect x="125.0" y="207.0" width="7.4" height="7.4" opacity="0.368"/>
<rect x="132.0" y="207.0" width="7.4" height="7.4" opacity="0.389"/>
<rect x="139.0" y="207.0" width="7.4" height="7.4" opacity="0.383"/>
<rect x="146.0" y="207.0" width="7.4" height="7.4" opacity="0.386"/>
<rect x="153.0" y="207.0" width="7.4" height="7.4" opacity="0.380"/>
<rect x="160.0" y="207.0" width="7.4" height="7.4" opacity="0.406"/>
<rect x="167.0" y="207.0" width="7.4" height="7.4" opacity="0.418"/>
<rect x="174.0" y="207.0" width="7.4" height="7.4" opacity="0.419"/>
<rect x="181.0" y="207.0" width="7.4" height="7.4" opacity="0.439"/>
<rect x="188.0" y="207.0" width="7.4" height="7.4" opacity="0.441"/>
<rect x="195.0" y="207.0" width="7.4" height="7.4" opacity="0.495"/>
<rect x="202.0" y="207.0" width="7.4" height="7.4" opacity="0.541"/>
<rect x="209.0" y="207.0" width="7.4" height="7.4" opacity="0.627"/>
<rect x="216.0" y="207.0" width="7.4" height="7.4" opacity="0.669"/>
<rect x="223.0" y="207.0" width="7.4" height="7.4" opacity="0.571"/>
<rect x="69.0" y="200.0" width="7.4" height="7.4" opacity="0.089"/>
<rect x="76.0" y="200.0" width="7.4" height="7.4" opacity="0.192"/>
<rect x="83.0" y="200.0" width="7.4" height="7.4" opacity="0.286"/>
<rect x="90.0" y="200.0" width="7.4" height="7.4" opacity="0.372"/>
<rect x="97.0" y="200.0" width="7.4" height="7.4" opacity="0.450"/>
<rect x="104.0" y="200.0" width="7.4" height="7.4" opacity="0.502"/>
<rect x="111.0" y="200.0" width="7.4" height="7.4" opacity="0.545"/>
<rect x="118.0" y="200.0" width="7.4" height="7.4" opacity="0.614"/>
<rect x="125.0" y="200.0" width="7.4" height="7.4" opacity="0.663"/>
<rect x="132.0" y="200.0" width="7.4" height="7.4" opacity="0.683"/>
<rect x="139.0" y="200.0" width="7.4" height="7.4" opacity="0.675"/>
<rect x="146.0" y="200.0" width="7.4" height="7.4" opacity="0.680"/>
<rect x="153.0" y="200.0" width="7.4" height="7.4" opacity="0.708"/>
<rect x="160.0" y="200.0" width="7.4" height="7.4" opacity="0.736"/>
<rect x="167.0" y="200.0" width="7.4" height="7.4" opacity="0.746"/>
<rect x="174.0" y="200.0" width="7.4" height="7.4" opacity="0.797"/>
<rect x="181.0" y="200.0" width="7.4" height="7.4" opacity="0.799"/>
<rect x="188.0" y="200.0" width="7.4" height="7.4" opacity="0.804"/>
<rect x="195.0" y="200.0" width="7.4" height="7.4" opacity="0.817"/>
<rect x="202.0" y="200.0" width="7.4" height="7.4" opacity="0.859"/>
<rect x="209.0" y="200.0" width="7.4" height="7.4" opacity="0.826"/>
<rect x="216.0" y="200.0" width="7.4" height="7.4" opacity="0.929"/>
<rect x="223.0" y="200.0" width="7.4" height="7.4" opacity="0.700"/>
<rect x="69.0" y="193.0" width="7.4" height="7.4" opacity="0.105"/>
<rect x="76.0" y="193.0" width="7.4" height="7.4" opacity="0.202"/>
<rect x="83.0" y="193.0" width="7.4" height="7.4" opacity="0.289"/>
<rect x="90.0" y="193.0" width="7.4" height="7.4" opacity="0.402"/>
<rect x="97.0" y="193.0" width="7.4" height="7.4" opacity="0.437"/>
<rect x="104.0" y="193.0" width="7.4" height="7.4" opacity="0.510"/>
<rect x="111.0" y="193.0" width="7.4" height="7.4" opacity="0.566"/>
<rect x="118.0" y="193.0" width="7.4" height="7.4" opacity="0.601"/>
<rect x="125.0" y="193.0" width="7.4" height="7.4" opacity="0.649"/>
<rect x="132.0" y="193.0" width="7.4" height="7.4" opacity="0.715"/>
<rect x="139.0" y="193.0" width="7.4" height="7.4" opacity="0.775"/>
<rect x="146.0" y="193.0" width="7.4" height="7.4" opacity="0.802"/>
<rect x="153.0" y="193.0" width="7.4" height="7.4" opacity="0.806"/>
<rect x="160.0" y="193.0" width="7.4" height="7.4" opacity="0.810"/>
<rect x="167.0" y="193.0" width="7.4" height="7.4" opacity="0.817"/>
<rect x="174.0" y="193.0" width="7.4" height="7.4" opacity="0.850"/>
<rect x="181.0" y="193.0" width="7.4" height="7.4" opacity="0.872"/>
<rect x="188.0" y="193.0" width="7.4" height="7.4" opacity="0.865"/>
<rect x="195.0" y="193.0" width="7.4" height="7.4" opacity="0.857"/>
<rect x="202.0" y="193.0" width="7.4" height="7.4" opacity="0.923"/>
<rect x="209.0" y="193.0" width="7.4" height="7.4" opacity="0.835"/>
<rect x="216.0" y="193.0" width="7.4" height="7.4" opacity="0.844"/>
<rect x="223.0" y="193.0" width="7.4" height="7.4" opacity="0.612"/>
<rect x="62.0" y="186.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="69.0" y="186.0" width="7.4" height="7.4" opacity="0.080"/>
<rect x="76.0" y="186.0" width="7.4" height="7.4" opacity="0.237"/>
<rect x="83.0" y="186.0" width="7.4" height="7.4" opacity="0.318"/>
<rect x="90.0" y="186.0" width="7.4" height="7.4" opacity="0.362"/>
<rect x="97.0" y="186.0" width="7.4" height="7.4" opacity="0.469"/>
<rect x="104.0" y="186.0" width="7.4" height="7.4" opacity="0.506"/>
<rect x="111.0" y="186.0" width="7.4" height="7.4" opacity="0.525"/>
<rect x="118.0" y="186.0" width="7.4" height="7.4" opacity="0.565"/>
<rect x="125.0" y="186.0" width="7.4" height="7.4" opacity="0.622"/>
<rect x="132.0" y="186.0" width="7.4" height="7.4" opacity="0.704"/>
<rect x="139.0" y="186.0" width="7.4" height="7.4" opacity="0.729"/>
<rect x="146.0" y="186.0" width="7.4" height="7.4" opacity="0.782"/>
<rect x="153.0" y="186.0" width="7.4" height="7.4" opacity="0.799"/>
<rect x="160.0" y="186.0" width="7.4" height="7.4" opacity="0.800"/>
<rect x="167.0" y="186.0" width="7.4" height="7.4" opacity="0.832"/>
<rect x="174.0" y="186.0" width="7.4" height="7.4" opacity="0.853"/>
<rect x="181.0" y="186.0" width="7.4" height="7.4" opacity="0.873"/>
<rect x="188.0" y="186.0" width="7.4" height="7.4" opacity="0.864"/>
<rect x="195.0" y="186.0" width="7.4" height="7.4" opacity="0.870"/>
<rect x="202.0" y="186.0" width="7.4" height="7.4" opacity="0.867"/>
<rect x="209.0" y="186.0" width="7.4" height="7.4" opacity="0.819"/>
<rect x="216.0" y="186.0" width="7.4" height="7.4" opacity="0.747"/>
<rect x="223.0" y="186.0" width="7.4" height="7.4" opacity="0.549"/>
<rect x="62.0" y="179.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="69.0" y="179.0" width="7.4" height="7.4" opacity="0.074"/>
<rect x="76.0" y="179.0" width="7.4" height="7.4" opacity="0.229"/>
<rect x="83.0" y="179.0" width="7.4" height="7.4" opacity="0.343"/>
<rect x="90.0" y="179.0" width="7.4" height="7.4" opacity="0.381"/>
<rect x="97.0" y="179.0" width="7.4" height="7.4" opacity="0.425"/>
<rect x="104.0" y="179.0" width="7.4" height="7.4" opacity="0.477"/>
<rect x="111.0" y="179.0" width="7.4" height="7.4" opacity="0.528"/>
<rect x="118.0" y="179.0" width="7.4" height="7.4" opacity="0.577"/>
<rect x="125.0" y="179.0" width="7.4" height="7.4" opacity="0.629"/>
<rect x="132.0" y="179.0" width="7.4" height="7.4" opacity="0.681"/>
<rect x="139.0" y="179.0" width="7.4" height="7.4" opacity="0.722"/>
<rect x="146.0" y="179.0" width="7.4" height="7.4" opacity="0.755"/>
<rect x="153.0" y="179.0" width="7.4" height="7.4" opacity="0.796"/>
<rect x="160.0" y="179.0" width="7.4" height="7.4" opacity="0.831"/>
<rect x="167.0" y="179.0" width="7.4" height="7.4" opacity="0.841"/>
<rect x="174.0" y="179.0" width="7.4" height="7.4" opacity="0.852"/>
<rect x="181.0" y="179.0" width="7.4" height="7.4" opacity="0.862"/>
<rect x="188.0" y="179.0" width="7.4" height="7.4" opacity="0.843"/>
<rect x="195.0" y="179.0" width="7.4" height="7.4" opacity="0.852"/>
<rect x="202.0" y="179.0" width="7.4" height="7.4" opacity="0.837"/>
<rect x="209.0" y="179.0" width="7.4" height="7.4" opacity="0.836"/>
<rect x="216.0" y="179.0" width="7.4" height="7.4" opacity="0.727"/>
<rect x="223.0" y="179.0" width="7.4" height="7.4" opacity="0.554"/>
<rect x="62.0" y="172.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="69.0" y="172.0" width="7.4" height="7.4" opacity="0.074"/>
<rect x="76.0" y="172.0" width="7.4" height="7.4" opacity="0.210"/>
<rect x="83.0" y="172.0" width="7.4" height="7.4" opacity="0.295"/>
<rect x="90.0" y="172.0" width="7.4" height="7.4" opacity="0.354"/>
<rect x="97.0" y="172.0" width="7.4" height="7.4" opacity="0.410"/>
<rect x="104.0" y="172.0" width="7.4" height="7.4" opacity="0.502"/>
<rect x="111.0" y="172.0" width="7.4" height="7.4" opacity="0.533"/>
<rect x="118.0" y="172.0" width="7.4" height="7.4" opacity="0.606"/>
<rect x="125.0" y="172.0" width="7.4" height="7.4" opacity="0.646"/>
<rect x="132.0" y="172.0" width="7.4" height="7.4" opacity="0.672"/>
<rect x="139.0" y="172.0" width="7.4" height="7.4" opacity="0.727"/>
<rect x="146.0" y="172.0" width="7.4" height="7.4" opacity="0.752"/>
<rect x="153.0" y="172.0" width="7.4" height="7.4" opacity="0.786"/>
<rect x="160.0" y="172.0" width="7.4" height="7.4" opacity="0.811"/>
<rect x="167.0" y="172.0" width="7.4" height="7.4" opacity="0.824"/>
<rect x="174.0" y="172.0" width="7.4" height="7.4" opacity="0.837"/>
<rect x="181.0" y="172.0" width="7.4" height="7.4" opacity="0.824"/>
<rect x="188.0" y="172.0" width="7.4" height="7.4" opacity="0.825"/>
<rect x="195.0" y="172.0" width="7.4" height="7.4" opacity="0.825"/>
<rect x="202.0" y="172.0" width="7.4" height="7.4" opacity="0.828"/>
<rect x="209.0" y="172.0" width="7.4" height="7.4" opacity="0.811"/>
<rect x="216.0" y="172.0" width="7.4" height="7.4" opacity="0.729"/>
<rect x="223.0" y="172.0" width="7.4" height="7.4" opacity="0.536"/>
<rect x="69.0" y="165.0" width="7.4" height="7.4" opacity="0.089"/>
<rect x="76.0" y="165.0" width="7.4" height="7.4" opacity="0.208"/>
<rect x="83.0" y="165.0" width="7.4" height="7.4" opacity="0.310"/>
<rect x="90.0" y="165.0" width="7.4" height="7.4" opacity="0.359"/>
<rect x="97.0" y="165.0" width="7.4" height="7.4" opacity="0.436"/>
<rect x="104.0" y="165.0" width="7.4" height="7.4" opacity="0.512"/>
<rect x="111.0" y="165.0" width="7.4" height="7.4" opacity="0.538"/>
<rect x="118.0" y="165.0" width="7.4" height="7.4" opacity="0.591"/>
<rect x="125.0" y="165.0" width="7.4" height="7.4" opacity="0.646"/>
<rect x="132.0" y="165.0" width="7.4" height="7.4" opacity="0.691"/>
<rect x="139.0" y="165.0" width="7.4" height="7.4" opacity="0.725"/>
<rect x="146.0" y="165.0" width="7.4" height="7.4" opacity="0.785"/>
<rect x="153.0" y="165.0" width="7.4" height="7.4" opacity="0.806"/>
<rect x="160.0" y="165.0" width="7.4" height="7.4" opacity="0.822"/>
<rect x="167.0" y="165.0" width="7.4" height="7.4" opacity="0.832"/>
<rect x="174.0" y="165.0" width="7.4" height="7.4" opacity="0.849"/>
<rect x="181.0" y="165.0" width="7.4" height="7.4" opacity="0.832"/>
<rect x="188.0" y="165.0" width="7.4" height="7.4" opacity="0.849"/>
<rect x="195.0" y="165.0" width="7.4" height="7.4" opacity="0.846"/>
<rect x="202.0" y="165.0" width="7.4" height="7.4" opacity="0.856"/>
<rect x="209.0" y="165.0" width="7.4" height="7.4" opacity="0.791"/>
<rect x="216.0" y="165.0" width="7.4" height="7.4" opacity="0.706"/>
<rect x="223.0" y="165.0" width="7.4" height="7.4" opacity="0.498"/>
<rect x="69.0" y="158.0" width="7.4" height="7.4" opacity="0.059"/>
<rect x="76.0" y="158.0" width="7.4" height="7.4" opacity="0.194"/>
<rect x="83.0" y="158.0" width="7.4" height="7.4" opacity="0.291"/>
<rect x="90.0" y="158.0" width="7.4" height="7.4" opacity="0.351"/>
<rect x="97.0" y="158.0" width="7.4" height="7.4" opacity="0.416"/>
<rect x="104.0" y="158.0" width="7.4" height="7.4" opacity="0.475"/>
<rect x="111.0" y="158.0" width="7.4" height="7.4" opacity="0.542"/>
<rect x="118.0" y="158.0" width="7.4" height="7.4" opacity="0.596"/>
<rect x="125.0" y="158.0" width="7.4" height="7.4" opacity="0.664"/>
<rect x="132.0" y="158.0" width="7.4" height="7.4" opacity="0.695"/>
<rect x="139.0" y="158.0" width="7.4" height="7.4" opacity="0.751"/>
<rect x="146.0" y="158.0" width="7.4" height="7.4" opacity="0.779"/>
<rect x="153.0" y="158.0" width="7.4" height="7.4" opacity="0.825"/>
<rect x="160.0" y="158.0" width="7.4" height="7.4" opacity="0.848"/>
<rect x="167.0" y="158.0" width="7.4" height="7.4" opacity="0.856"/>
<rect x="174.0" y="158.0" width="7.4" height="7.4" opacity="0.834"/>
<rect x="181.0" y="158.0" width="7.4" height="7.4" opacity="0.848"/>
<rect x="188.0" y="158.0" width="7.4" height="7.4" opacity="0.854"/>
<rect x="195.0" y="158.0" width="7.4" height="7.4" opacity="0.848"/>
<rect x="202.0" y="158.0" width="7.4" height="7.4" opacity="0.862"/>
<rect x="209.0" y="158.0" width="7.4" height="7.4" opacity="0.813"/>
<rect x="216.0" y="158.0" width="7.4" height="7.4" opacity="0.723"/>
<rect x="223.0" y="158.0" width="7.4" height="7.4" opacity="0.504"/>
<rect x="69.0" y="151.0" width="7.4" height="7.4" opacity="0.083"/>
<rect x="76.0" y="151.0" width="7.4" height="7.4" opacity="0.172"/>
<rect x="83.0" y="151.0" width="7.4" height="7.4" opacity="0.271"/>
<rect x="90.0" y="151.0" width="7.4" height="7.4" opacity="0.354"/>
<rect x="97.0" y="151.0" width="7.4" height="7.4" opacity="0.420"/>
<rect x="104.0" y="151.0" width="7.4" height="7.4" opacity="0.498"/>
<rect x="111.0" y="151.0" width="7.4" height="7.4" opacity="0.530"/>
<rect x="118.0" y="151.0" width="7.4" height="7.4" opacity="0.567"/>
<rect x="125.0" y="151.0" width="7.4" height="7.4" opacity="0.638"/>
<rect x="132.0" y="151.0" width="7.4" height="7.4" opacity="0.718"/>
<rect x="139.0" y="151.0" width="7.4" height="7.4" opacity="0.762"/>
<rect x="146.0" y="151.0" width="7.4" height="7.4" opacity="0.789"/>
<rect x="153.0" y="151.0" width="7.4" height="7.4" opacity="0.807"/>
<rect x="160.0" y="151.0" width="7.4" height="7.4" opacity="0.831"/>
<rect x="167.0" y="151.0" width="7.4" height="7.4" opacity="0.839"/>
<rect x="174.0" y="151.0" width="7.4" height="7.4" opacity="0.861"/>
<rect x="181.0" y="151.0" width="7.4" height="7.4" opacity="0.867"/>
<rect x="188.0" y="151.0" width="7.4" height="7.4" opacity="0.861"/>
<rect x="195.0" y="151.0" width="7.4" height="7.4" opacity="0.880"/>
<rect x="202.0" y="151.0" width="7.4" height="7.4" opacity="0.843"/>
<rect x="209.0" y="151.0" width="7.4" height="7.4" opacity="0.800"/>
<rect x="216.0" y="151.0" width="7.4" height="7.4" opacity="0.693"/>
<rect x="223.0" y="151.0" width="7.4" height="7.4" opacity="0.527"/>
<rect x="69.0" y="144.0" width="7.4" height="7.4" opacity="0.095"/>
<rect x="76.0" y="144.0" width="7.4" height="7.4" opacity="0.183"/>
<rect x="83.0" y="144.0" width="7.4" height="7.4" opacity="0.280"/>
<rect x="90.0" y="144.0" width="7.4" height="7.4" opacity="0.323"/>
<rect x="97.0" y="144.0" width="7.4" height="7.4" opacity="0.405"/>
<rect x="104.0" y="144.0" width="7.4" height="7.4" opacity="0.480"/>
<rect x="111.0" y="144.0" width="7.4" height="7.4" opacity="0.513"/>
<rect x="118.0" y="144.0" width="7.4" height="7.4" opacity="0.584"/>
<rect x="125.0" y="144.0" width="7.4" height="7.4" opacity="0.660"/>
<rect x="132.0" y="144.0" width="7.4" height="7.4" opacity="0.722"/>
<rect x="139.0" y="144.0" width="7.4" height="7.4" opacity="0.753"/>
<rect x="146.0" y="144.0" width="7.4" height="7.4" opacity="0.786"/>
<rect x="153.0" y="144.0" width="7.4" height="7.4" opacity="0.813"/>
<rect x="160.0" y="144.0" width="7.4" height="7.4" opacity="0.832"/>
<rect x="167.0" y="144.0" width="7.4" height="7.4" opacity="0.838"/>
<rect x="174.0" y="144.0" width="7.4" height="7.4" opacity="0.880"/>
<rect x="181.0" y="144.0" width="7.4" height="7.4" opacity="0.877"/>
<rect x="188.0" y="144.0" width="7.4" height="7.4" opacity="0.898"/>
<rect x="195.0" y="144.0" width="7.4" height="7.4" opacity="0.861"/>
<rect x="202.0" y="144.0" width="7.4" height="7.4" opacity="0.822"/>
<rect x="209.0" y="144.0" width="7.4" height="7.4" opacity="0.805"/>
<rect x="216.0" y="144.0" width="7.4" height="7.4" opacity="0.710"/>
<rect x="223.0" y="144.0" width="7.4" height="7.4" opacity="0.525"/>
<rect x="69.0" y="137.0" width="7.4" height="7.4" opacity="0.084"/>
<rect x="76.0" y="137.0" width="7.4" height="7.4" opacity="0.150"/>
<rect x="83.0" y="137.0" width="7.4" height="7.4" opacity="0.253"/>
<rect x="90.0" y="137.0" width="7.4" height="7.4" opacity="0.324"/>
<rect x="97.0" y="137.0" width="7.4" height="7.4" opacity="0.377"/>
<rect x="104.0" y="137.0" width="7.4" height="7.4" opacity="0.462"/>
<rect x="111.0" y="137.0" width="7.4" height="7.4" opacity="0.536"/>
<rect x="118.0" y="137.0" width="7.4" height="7.4" opacity="0.597"/>
<rect x="125.0" y="137.0" width="7.4" height="7.4" opacity="0.681"/>
<rect x="132.0" y="137.0" width="7.4" height="7.4" opacity="0.706"/>
<rect x="139.0" y="137.0" width="7.4" height="7.4" opacity="0.775"/>
<rect x="146.0" y="137.0" width="7.4" height="7.4" opacity="0.794"/>
<rect x="153.0" y="137.0" width="7.4" height="7.4" opacity="0.815"/>
<rect x="160.0" y="137.0" width="7.4" height="7.4" opacity="0.853"/>
<rect x="167.0" y="137.0" width="7.4" height="7.4" opacity="0.867"/>
<rect x="174.0" y="137.0" width="7.4" height="7.4" opacity="0.881"/>
<rect x="181.0" y="137.0" width="7.4" height="7.4" opacity="0.881"/>
<rect x="188.0" y="137.0" width="7.4" height="7.4" opacity="0.881"/>
<rect x="195.0" y="137.0" width="7.4" height="7.4" opacity="0.853"/>
<rect x="202.0" y="137.0" width="7.4" height="7.4" opacity="0.812"/>
<rect x="209.0" y="137.0" width="7.4" height="7.4" opacity="0.805"/>
<rect x="216.0" y="137.0" width="7.4" height="7.4" opacity="0.717"/>
<rect x="223.0" y="137.0" width="7.4" height="7.4" opacity="0.533"/>
<rect x="69.0" y="130.0" width="7.4" height="7.4" opacity="0.064"/>
<rect x="76.0" y="130.0" width="7.4" height="7.4" opacity="0.145"/>
<rect x="83.0" y="130.0" width="7.4" height="7.4" opacity="0.217"/>
<rect x="90.0" y="130.0" width="7.4" height="7.4" opacity="0.282"/>
<rect x="97.0" y="130.0" width="7.4" height="7.4" opacity="0.370"/>
<rect x="104.0" y="130.0" width="7.4" height="7.4" opacity="0.472"/>
<rect x="111.0" y="130.0" width="7.4" height="7.4" opacity="0.542"/>
<rect x="118.0" y="130.0" width="7.4" height="7.4" opacity="0.620"/>
<rect x="125.0" y="130.0" width="7.4" height="7.4" opacity="0.676"/>
<rect x="132.0" y="130.0" width="7.4" height="7.4" opacity="0.695"/>
<rect x="139.0" y="130.0" width="7.4" height="7.4" opacity="0.744"/>
<rect x="146.0" y="130.0" width="7.4" height="7.4" opacity="0.774"/>
<rect x="153.0" y="130.0" width="7.4" height="7.4" opacity="0.828"/>
<rect x="160.0" y="130.0" width="7.4" height="7.4" opacity="0.846"/>
<rect x="167.0" y="130.0" width="7.4" height="7.4" opacity="0.859"/>
<rect x="174.0" y="130.0" width="7.4" height="7.4" opacity="0.867"/>
<rect x="181.0" y="130.0" width="7.4" height="7.4" opacity="0.859"/>
<rect x="188.0" y="130.0" width="7.4" height="7.4" opacity="0.873"/>
<rect x="195.0" y="130.0" width="7.4" height="7.4" opacity="0.852"/>
<rect x="202.0" y="130.0" width="7.4" height="7.4" opacity="0.832"/>
<rect x="209.0" y="130.0" width="7.4" height="7.4" opacity="0.786"/>
<rect x="216.0" y="130.0" width="7.4" height="7.4" opacity="0.739"/>
<rect x="223.0" y="130.0" width="7.4" height="7.4" opacity="0.527"/>
<rect x="69.0" y="123.0" width="7.4" height="7.4" opacity="0.054"/>
<rect x="76.0" y="123.0" width="7.4" height="7.4" opacity="0.133"/>
<rect x="83.0" y="123.0" width="7.4" height="7.4" opacity="0.203"/>
<rect x="90.0" y="123.0" width="7.4" height="7.4" opacity="0.258"/>
<rect x="97.0" y="123.0" width="7.4" height="7.4" opacity="0.344"/>
<rect x="104.0" y="123.0" width="7.4" height="7.4" opacity="0.449"/>
<rect x="111.0" y="123.0" width="7.4" height="7.4" opacity="0.543"/>
<rect x="118.0" y="123.0" width="7.4" height="7.4" opacity="0.617"/>
<rect x="125.0" y="123.0" width="7.4" height="7.4" opacity="0.676"/>
<rect x="132.0" y="123.0" width="7.4" height="7.4" opacity="0.712"/>
<rect x="139.0" y="123.0" width="7.4" height="7.4" opacity="0.753"/>
<rect x="146.0" y="123.0" width="7.4" height="7.4" opacity="0.794"/>
<rect x="153.0" y="123.0" width="7.4" height="7.4" opacity="0.834"/>
<rect x="160.0" y="123.0" width="7.4" height="7.4" opacity="0.858"/>
<rect x="167.0" y="123.0" width="7.4" height="7.4" opacity="0.863"/>
<rect x="174.0" y="123.0" width="7.4" height="7.4" opacity="0.869"/>
<rect x="181.0" y="123.0" width="7.4" height="7.4" opacity="0.862"/>
<rect x="188.0" y="123.0" width="7.4" height="7.4" opacity="0.905"/>
<rect x="195.0" y="123.0" width="7.4" height="7.4" opacity="0.875"/>
<rect x="202.0" y="123.0" width="7.4" height="7.4" opacity="0.861"/>
<rect x="209.0" y="123.0" width="7.4" height="7.4" opacity="0.809"/>
<rect x="216.0" y="123.0" width="7.4" height="7.4" opacity="0.752"/>
<rect x="223.0" y="123.0" width="7.4" height="7.4" opacity="0.513"/>
<rect x="62.0" y="116.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="69.0" y="116.0" width="7.4" height="7.4" opacity="0.086"/>
<rect x="76.0" y="116.0" width="7.4" height="7.4" opacity="0.155"/>
<rect x="83.0" y="116.0" width="7.4" height="7.4" opacity="0.222"/>
<rect x="90.0" y="116.0" width="7.4" height="7.4" opacity="0.300"/>
<rect x="97.0" y="116.0" width="7.4" height="7.4" opacity="0.336"/>
<rect x="104.0" y="116.0" width="7.4" height="7.4" opacity="0.429"/>
<rect x="111.0" y="116.0" width="7.4" height="7.4" opacity="0.537"/>
<rect x="118.0" y="116.0" width="7.4" height="7.4" opacity="0.600"/>
<rect x="125.0" y="116.0" width="7.4" height="7.4" opacity="0.659"/>
<rect x="132.0" y="116.0" width="7.4" height="7.4" opacity="0.717"/>
<rect x="139.0" y="116.0" width="7.4" height="7.4" opacity="0.750"/>
<rect x="146.0" y="116.0" width="7.4" height="7.4" opacity="0.796"/>
<rect x="153.0" y="116.0" width="7.4" height="7.4" opacity="0.826"/>
<rect x="160.0" y="116.0" width="7.4" height="7.4" opacity="0.838"/>
<rect x="167.0" y="116.0" width="7.4" height="7.4" opacity="0.857"/>
<rect x="174.0" y="116.0" width="7.4" height="7.4" opacity="0.871"/>
<rect x="181.0" y="116.0" width="7.4" height="7.4" opacity="0.866"/>
<rect x="188.0" y="116.0" width="7.4" height="7.4" opacity="0.900"/>
<rect x="195.0" y="116.0" width="7.4" height="7.4" opacity="0.893"/>
<rect x="202.0" y="116.0" width="7.4" height="7.4" opacity="0.870"/>
<rect x="209.0" y="116.0" width="7.4" height="7.4" opacity="0.815"/>
<rect x="216.0" y="116.0" width="7.4" height="7.4" opacity="0.720"/>
<rect x="223.0" y="116.0" width="7.4" height="7.4" opacity="0.567"/>
<rect x="62.0" y="109.0" width="7.4" height="7.4" opacity="0.045"/>
<rect x="69.0" y="109.0" width="7.4" height="7.4" opacity="0.098"/>
<rect x="76.0" y="109.0" width="7.4" height="7.4" opacity="0.181"/>
<rect x="83.0" y="109.0" width="7.4" height="7.4" opacity="0.231"/>
<rect x="90.0" y="109.0" width="7.4" height="7.4" opacity="0.323"/>
<rect x="97.0" y="109.0" width="7.4" height="7.4" opacity="0.381"/>
<rect x="104.0" y="109.0" width="7.4" height="7.4" opacity="0.458"/>
<rect x="111.0" y="109.0" width="7.4" height="7.4" opacity="0.528"/>
<rect x="118.0" y="109.0" width="7.4" height="7.4" opacity="0.599"/>
<rect x="125.0" y="109.0" width="7.4" height="7.4" opacity="0.647"/>
<rect x="132.0" y="109.0" width="7.4" height="7.4" opacity="0.711"/>
<rect x="139.0" y="109.0" width="7.4" height="7.4" opacity="0.738"/>
<rect x="146.0" y="109.0" width="7.4" height="7.4" opacity="0.786"/>
<rect x="153.0" y="109.0" width="7.4" height="7.4" opacity="0.829"/>
<rect x="160.0" y="109.0" width="7.4" height="7.4" opacity="0.841"/>
<rect x="167.0" y="109.0" width="7.4" height="7.4" opacity="0.865"/>
<rect x="174.0" y="109.0" width="7.4" height="7.4" opacity="0.873"/>
<rect x="181.0" y="109.0" width="7.4" height="7.4" opacity="0.900"/>
<rect x="188.0" y="109.0" width="7.4" height="7.4" opacity="0.902"/>
<rect x="195.0" y="109.0" width="7.4" height="7.4" opacity="0.905"/>
<rect x="202.0" y="109.0" width="7.4" height="7.4" opacity="0.878"/>
<rect x="209.0" y="109.0" width="7.4" height="7.4" opacity="0.827"/>
<rect x="216.0" y="109.0" width="7.4" height="7.4" opacity="0.743"/>
<rect x="223.0" y="109.0" width="7.4" height="7.4" opacity="0.583"/>
<rect x="62.0" y="102.0" width="7.4" height="7.4" opacity="0.033"/>
<rect x="69.0" y="102.0" width="7.4" height="7.4" opacity="0.095"/>
<rect x="76.0" y="102.0" width="7.4" height="7.4" opacity="0.178"/>
<rect x="83.0" y="102.0" width="7.4" height="7.4" opacity="0.236"/>
<rect x="90.0" y="102.0" width="7.4" height="7.4" opacity="0.319"/>
<rect x="97.0" y="102.0" width="7.4" height="7.4" opacity="0.408"/>
<rect x="104.0" y="102.0" width="7.4" height="7.4" opacity="0.488"/>
<rect x="111.0" y="102.0" width="7.4" height="7.4" opacity="0.530"/>
<rect x="118.0" y="102.0" width="7.4" height="7.4" opacity="0.606"/>
<rect x="125.0" y="102.0" width="7.4" height="7.4" opacity="0.639"/>
<rect x="132.0" y="102.0" width="7.4" height="7.4" opacity="0.694"/>
<rect x="139.0" y="102.0" width="7.4" height="7.4" opacity="0.730"/>
<rect x="146.0" y="102.0" width="7.4" height="7.4" opacity="0.775"/>
<rect x="153.0" y="102.0" width="7.4" height="7.4" opacity="0.817"/>
<rect x="160.0" y="102.0" width="7.4" height="7.4" opacity="0.826"/>
<rect x="167.0" y="102.0" width="7.4" height="7.4" opacity="0.845"/>
<rect x="174.0" y="102.0" width="7.4" height="7.4" opacity="0.880"/>
<rect x="181.0" y="102.0" width="7.4" height="7.4" opacity="0.903"/>
<rect x="188.0" y="102.0" width="7.4" height="7.4" opacity="0.898"/>
<rect x="195.0" y="102.0" width="7.4" height="7.4" opacity="0.899"/>
<rect x="202.0" y="102.0" width="7.4" height="7.4" opacity="0.882"/>
<rect x="209.0" y="102.0" width="7.4" height="7.4" opacity="0.798"/>
<rect x="216.0" y="102.0" width="7.4" height="7.4" opacity="0.764"/>
<rect x="223.0" y="102.0" width="7.4" height="7.4" opacity="0.604"/>
<rect x="62.0" y="95.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="69.0" y="95.0" width="7.4" height="7.4" opacity="0.105"/>
<rect x="76.0" y="95.0" width="7.4" height="7.4" opacity="0.141"/>
<rect x="83.0" y="95.0" width="7.4" height="7.4" opacity="0.226"/>
<rect x="90.0" y="95.0" width="7.4" height="7.4" opacity="0.335"/>
<rect x="97.0" y="95.0" width="7.4" height="7.4" opacity="0.414"/>
<rect x="104.0" y="95.0" width="7.4" height="7.4" opacity="0.499"/>
<rect x="111.0" y="95.0" width="7.4" height="7.4" opacity="0.549"/>
<rect x="118.0" y="95.0" width="7.4" height="7.4" opacity="0.596"/>
<rect x="125.0" y="95.0" width="7.4" height="7.4" opacity="0.655"/>
<rect x="132.0" y="95.0" width="7.4" height="7.4" opacity="0.706"/>
<rect x="139.0" y="95.0" width="7.4" height="7.4" opacity="0.718"/>
<rect x="146.0" y="95.0" width="7.4" height="7.4" opacity="0.773"/>
<rect x="153.0" y="95.0" width="7.4" height="7.4" opacity="0.790"/>
<rect x="160.0" y="95.0" width="7.4" height="7.4" opacity="0.817"/>
<rect x="167.0" y="95.0" width="7.4" height="7.4" opacity="0.847"/>
<rect x="174.0" y="95.0" width="7.4" height="7.4" opacity="0.870"/>
<rect x="181.0" y="95.0" width="7.4" height="7.4" opacity="0.891"/>
<rect x="188.0" y="95.0" width="7.4" height="7.4" opacity="0.892"/>
<rect x="195.0" y="95.0" width="7.4" height="7.4" opacity="0.900"/>
<rect x="202.0" y="95.0" width="7.4" height="7.4" opacity="0.881"/>
<rect x="209.0" y="95.0" width="7.4" height="7.4" opacity="0.818"/>
<rect x="216.0" y="95.0" width="7.4" height="7.4" opacity="0.773"/>
<rect x="223.0" y="95.0" width="7.4" height="7.4" opacity="0.609"/>
<rect x="62.0" y="88.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="69.0" y="88.0" width="7.4" height="7.4" opacity="0.104"/>
<rect x="76.0" y="88.0" width="7.4" height="7.4" opacity="0.145"/>
<rect x="83.0" y="88.0" width="7.4" height="7.4" opacity="0.236"/>
<rect x="90.0" y="88.0" width="7.4" height="7.4" opacity="0.325"/>
<rect x="97.0" y="88.0" width="7.4" height="7.4" opacity="0.418"/>
<rect x="104.0" y="88.0" width="7.4" height="7.4" opacity="0.484"/>
<rect x="111.0" y="88.0" width="7.4" height="7.4" opacity="0.538"/>
<rect x="118.0" y="88.0" width="7.4" height="7.4" opacity="0.574"/>
<rect x="125.0" y="88.0" width="7.4" height="7.4" opacity="0.641"/>
<rect x="132.0" y="88.0" width="7.4" height="7.4" opacity="0.672"/>
<rect x="139.0" y="88.0" width="7.4" height="7.4" opacity="0.725"/>
<rect x="146.0" y="88.0" width="7.4" height="7.4" opacity="0.778"/>
<rect x="153.0" y="88.0" width="7.4" height="7.4" opacity="0.795"/>
<rect x="160.0" y="88.0" width="7.4" height="7.4" opacity="0.811"/>
<rect x="167.0" y="88.0" width="7.4" height="7.4" opacity="0.827"/>
<rect x="174.0" y="88.0" width="7.4" height="7.4" opacity="0.855"/>
<rect x="181.0" y="88.0" width="7.4" height="7.4" opacity="0.872"/>
<rect x="188.0" y="88.0" width="7.4" height="7.4" opacity="0.905"/>
<rect x="195.0" y="88.0" width="7.4" height="7.4" opacity="0.916"/>
<rect x="202.0" y="88.0" width="7.4" height="7.4" opacity="0.902"/>
<rect x="209.0" y="88.0" width="7.4" height="7.4" opacity="0.858"/>
<rect x="216.0" y="88.0" width="7.4" height="7.4" opacity="0.795"/>
<rect x="223.0" y="88.0" width="7.4" height="7.4" opacity="0.607"/>
<rect x="62.0" y="81.0" width="7.4" height="7.4" opacity="0.033"/>
<rect x="69.0" y="81.0" width="7.4" height="7.4" opacity="0.106"/>
<rect x="76.0" y="81.0" width="7.4" height="7.4" opacity="0.151"/>
<rect x="83.0" y="81.0" width="7.4" height="7.4" opacity="0.233"/>
<rect x="90.0" y="81.0" width="7.4" height="7.4" opacity="0.317"/>
<rect x="97.0" y="81.0" width="7.4" height="7.4" opacity="0.405"/>
<rect x="104.0" y="81.0" width="7.4" height="7.4" opacity="0.493"/>
<rect x="111.0" y="81.0" width="7.4" height="7.4" opacity="0.523"/>
<rect x="118.0" y="81.0" width="7.4" height="7.4" opacity="0.579"/>
<rect x="125.0" y="81.0" width="7.4" height="7.4" opacity="0.601"/>
<rect x="132.0" y="81.0" width="7.4" height="7.4" opacity="0.649"/>
<rect x="139.0" y="81.0" width="7.4" height="7.4" opacity="0.707"/>
<rect x="146.0" y="81.0" width="7.4" height="7.4" opacity="0.746"/>
<rect x="153.0" y="81.0" width="7.4" height="7.4" opacity="0.787"/>
<rect x="160.0" y="81.0" width="7.4" height="7.4" opacity="0.828"/>
<rect x="167.0" y="81.0" width="7.4" height="7.4" opacity="0.862"/>
<rect x="174.0" y="81.0" width="7.4" height="7.4" opacity="0.854"/>
<rect x="181.0" y="81.0" width="7.4" height="7.4" opacity="0.889"/>
<rect x="188.0" y="81.0" width="7.4" height="7.4" opacity="0.918"/>
<rect x="195.0" y="81.0" width="7.4" height="7.4" opacity="0.929"/>
<rect x="202.0" y="81.0" width="7.4" height="7.4" opacity="0.926"/>
<rect x="209.0" y="81.0" width="7.4" height="7.4" opacity="0.906"/>
<rect x="216.0" y="81.0" width="7.4" height="7.4" opacity="0.836"/>
<rect x="223.0" y="81.0" width="7.4" height="7.4" opacity="0.643"/>
<rect x="62.0" y="74.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="69.0" y="74.0" width="7.4" height="7.4" opacity="0.100"/>
<rect x="76.0" y="74.0" width="7.4" height="7.4" opacity="0.166"/>
<rect x="83.0" y="74.0" width="7.4" height="7.4" opacity="0.236"/>
<rect x="90.0" y="74.0" width="7.4" height="7.4" opacity="0.334"/>
<rect x="97.0" y="74.0" width="7.4" height="7.4" opacity="0.406"/>
<rect x="104.0" y="74.0" width="7.4" height="7.4" opacity="0.468"/>
<rect x="111.0" y="74.0" width="7.4" height="7.4" opacity="0.517"/>
<rect x="118.0" y="74.0" width="7.4" height="7.4" opacity="0.565"/>
<rect x="125.0" y="74.0" width="7.4" height="7.4" opacity="0.613"/>
<rect x="132.0" y="74.0" width="7.4" height="7.4" opacity="0.674"/>
<rect x="139.0" y="74.0" width="7.4" height="7.4" opacity="0.705"/>
<rect x="146.0" y="74.0" width="7.4" height="7.4" opacity="0.743"/>
<rect x="153.0" y="74.0" width="7.4" height="7.4" opacity="0.791"/>
<rect x="160.0" y="74.0" width="7.4" height="7.4" opacity="0.815"/>
<rect x="167.0" y="74.0" width="7.4" height="7.4" opacity="0.860"/>
<rect x="174.0" y="74.0" width="7.4" height="7.4" opacity="0.878"/>
<rect x="181.0" y="74.0" width="7.4" height="7.4" opacity="0.886"/>
<rect x="188.0" y="74.0" width="7.4" height="7.4" opacity="0.905"/>
<rect x="195.0" y="74.0" width="7.4" height="7.4" opacity="0.926"/>
<rect x="202.0" y="74.0" width="7.4" height="7.4" opacity="0.930"/>
<rect x="209.0" y="74.0" width="7.4" height="7.4" opacity="0.912"/>
<rect x="216.0" y="74.0" width="7.4" height="7.4" opacity="0.820"/>
<rect x="223.0" y="74.0" width="7.4" height="7.4" opacity="0.610"/>
<rect x="69.0" y="67.0" width="7.4" height="7.4" opacity="0.064"/>
<rect x="76.0" y="67.0" width="7.4" height="7.4" opacity="0.137"/>
<rect x="83.0" y="67.0" width="7.4" height="7.4" opacity="0.243"/>
<rect x="90.0" y="67.0" width="7.4" height="7.4" opacity="0.344"/>
<rect x="97.0" y="67.0" width="7.4" height="7.4" opacity="0.373"/>
<rect x="104.0" y="67.0" width="7.4" height="7.4" opacity="0.443"/>
<rect x="111.0" y="67.0" width="7.4" height="7.4" opacity="0.536"/>
<rect x="118.0" y="67.0" width="7.4" height="7.4" opacity="0.593"/>
<rect x="125.0" y="67.0" width="7.4" height="7.4" opacity="0.632"/>
<rect x="132.0" y="67.0" width="7.4" height="7.4" opacity="0.688"/>
<rect x="139.0" y="67.0" width="7.4" height="7.4" opacity="0.715"/>
<rect x="146.0" y="67.0" width="7.4" height="7.4" opacity="0.755"/>
<rect x="153.0" y="67.0" width="7.4" height="7.4" opacity="0.792"/>
<rect x="160.0" y="67.0" width="7.4" height="7.4" opacity="0.810"/>
<rect x="167.0" y="67.0" width="7.4" height="7.4" opacity="0.836"/>
<rect x="174.0" y="67.0" width="7.4" height="7.4" opacity="0.872"/>
<rect x="181.0" y="67.0" width="7.4" height="7.4" opacity="0.900"/>
<rect x="188.0" y="67.0" width="7.4" height="7.4" opacity="0.901"/>
<rect x="195.0" y="67.0" width="7.4" height="7.4" opacity="0.935"/>
<rect x="202.0" y="67.0" width="7.4" height="7.4" opacity="0.935"/>
<rect x="209.0" y="67.0" width="7.4" height="7.4" opacity="0.958"/>
<rect x="216.0" y="67.0" width="7.4" height="7.4" opacity="0.865"/>
<rect x="223.0" y="67.0" width="7.4" height="7.4" opacity="0.680"/>
<rect x="62.0" y="60.0" width="7.4" height="7.4" opacity="0.028"/>
<rect x="69.0" y="60.0" width="7.4" height="7.4" opacity="0.076"/>
<rect x="76.0" y="60.0" width="7.4" height="7.4" opacity="0.192"/>
<rect x="83.0" y="60.0" width="7.4" height="7.4" opacity="0.287"/>
<rect x="90.0" y="60.0" width="7.4" height="7.4" opacity="0.331"/>
<rect x="97.0" y="60.0" width="7.4" height="7.4" opacity="0.410"/>
<rect x="104.0" y="60.0" width="7.4" height="7.4" opacity="0.443"/>
<rect x="111.0" y="60.0" width="7.4" height="7.4" opacity="0.512"/>
<rect x="118.0" y="60.0" width="7.4" height="7.4" opacity="0.579"/>
<rect x="125.0" y="60.0" width="7.4" height="7.4" opacity="0.634"/>
<rect x="132.0" y="60.0" width="7.4" height="7.4" opacity="0.661"/>
<rect x="139.0" y="60.0" width="7.4" height="7.4" opacity="0.709"/>
<rect x="146.0" y="60.0" width="7.4" height="7.4" opacity="0.749"/>
<rect x="153.0" y="60.0" width="7.4" height="7.4" opacity="0.785"/>
<rect x="160.0" y="60.0" width="7.4" height="7.4" opacity="0.796"/>
<rect x="167.0" y="60.0" width="7.4" height="7.4" opacity="0.829"/>
<rect x="174.0" y="60.0" width="7.4" height="7.4" opacity="0.875"/>
<rect x="181.0" y="60.0" width="7.4" height="7.4" opacity="0.910"/>
<rect x="188.0" y="60.0" width="7.4" height="7.4" opacity="0.937"/>
<rect x="195.0" y="60.0" width="7.4" height="7.4" opacity="0.955"/>
<rect x="202.0" y="60.0" width="7.4" height="7.4" opacity="0.983"/>
<rect x="209.0" y="60.0" width="7.4" height="7.4" opacity="1.000"/>
<rect x="216.0" y="60.0" width="7.4" height="7.4" opacity="0.938"/>
<rect x="223.0" y="60.0" width="7.4" height="7.4" opacity="0.749"/>
<rect x="69.0" y="53.0" width="7.4" height="7.4" opacity="0.101"/>
<rect x="76.0" y="53.0" width="7.4" height="7.4" opacity="0.179"/>
<rect x="83.0" y="53.0" width="7.4" height="7.4" opacity="0.217"/>
<rect x="90.0" y="53.0" width="7.4" height="7.4" opacity="0.307"/>
<rect x="97.0" y="53.0" width="7.4" height="7.4" opacity="0.359"/>
<rect x="104.0" y="53.0" width="7.4" height="7.4" opacity="0.386"/>
<rect x="111.0" y="53.0" width="7.4" height="7.4" opacity="0.429"/>
<rect x="118.0" y="53.0" width="7.4" height="7.4" opacity="0.498"/>
<rect x="125.0" y="53.0" width="7.4" height="7.4" opacity="0.541"/>
<rect x="132.0" y="53.0" width="7.4" height="7.4" opacity="0.545"/>
<rect x="139.0" y="53.0" width="7.4" height="7.4" opacity="0.543"/>
<rect x="146.0" y="53.0" width="7.4" height="7.4" opacity="0.606"/>
<rect x="153.0" y="53.0" width="7.4" height="7.4" opacity="0.642"/>
<rect x="160.0" y="53.0" width="7.4" height="7.4" opacity="0.682"/>
<rect x="167.0" y="53.0" width="7.4" height="7.4" opacity="0.701"/>
<rect x="174.0" y="53.0" width="7.4" height="7.4" opacity="0.739"/>
<rect x="181.0" y="53.0" width="7.4" height="7.4" opacity="0.796"/>
<rect x="188.0" y="53.0" width="7.4" height="7.4" opacity="0.880"/>
<rect x="195.0" y="53.0" width="7.4" height="7.4" opacity="0.901"/>
<rect x="202.0" y="53.0" width="7.4" height="7.4" opacity="0.960"/>
<rect x="209.0" y="53.0" width="7.4" height="7.4" opacity="0.990"/>
<rect x="216.0" y="53.0" width="7.4" height="7.4" opacity="0.980"/>
<rect x="223.0" y="53.0" width="7.4" height="7.4" opacity="0.757"/>
<rect x="69.0" y="46.0" width="7.4" height="7.4" opacity="0.020"/>
<rect x="76.0" y="46.0" width="7.4" height="7.4" opacity="0.059"/>
<rect x="83.0" y="46.0" width="7.4" height="7.4" opacity="0.111"/>
<rect x="90.0" y="46.0" width="7.4" height="7.4" opacity="0.139"/>
<rect x="97.0" y="46.0" width="7.4" height="7.4" opacity="0.184"/>
<rect x="104.0" y="46.0" width="7.4" height="7.4" opacity="0.219"/>
<rect x="111.0" y="46.0" width="7.4" height="7.4" opacity="0.222"/>
<rect x="118.0" y="46.0" width="7.4" height="7.4" opacity="0.249"/>
<rect x="125.0" y="46.0" width="7.4" height="7.4" opacity="0.243"/>
<rect x="132.0" y="46.0" width="7.4" height="7.4" opacity="0.278"/>
<rect x="139.0" y="46.0" width="7.4" height="7.4" opacity="0.277"/>
<rect x="146.0" y="46.0" width="7.4" height="7.4" opacity="0.270"/>
<rect x="153.0" y="46.0" width="7.4" height="7.4" opacity="0.310"/>
<rect x="160.0" y="46.0" width="7.4" height="7.4" opacity="0.372"/>
<rect x="167.0" y="46.0" width="7.4" height="7.4" opacity="0.395"/>
<rect x="174.0" y="46.0" width="7.4" height="7.4" opacity="0.445"/>
<rect x="181.0" y="46.0" width="7.4" height="7.4" opacity="0.463"/>
<rect x="188.0" y="46.0" width="7.4" height="7.4" opacity="0.463"/>
<rect x="195.0" y="46.0" width="7.4" height="7.4" opacity="0.499"/>
<rect x="202.0" y="46.0" width="7.4" height="7.4" opacity="0.570"/>
<rect x="209.0" y="46.0" width="7.4" height="7.4" opacity="0.669"/>
<rect x="216.0" y="46.0" width="7.4" height="7.4" opacity="0.751"/>
<rect x="223.0" y="46.0" width="7.4" height="7.4" opacity="0.613"/>
</g>
<line class="ref" x1="62.0" y1="207.0" x2="230.0" y2="46.0"/>
<text class="lbl bad" x="226.0" y="59.0" text-anchor="end">묶였다면 이 선 위</text>
<rect class="frame" x="62.0" y="46.0" width="168.0" height="168.0"/>
<g class="lbl-ax">
<text x="62.0" y="228">0</text>
<text class="r" x="56.0" y="217.5">0</text>
<text x="146.0" y="228">0.5</text>
<text class="r" x="56.0" y="133.5">0.5</text>
<text x="230.0" y="228">1</text>
<text class="r" x="56.0" y="49.5">1</text>
<text class="cap l" x="62.0" y="243">입력 게이트 i</text></g>
<g class="row-lbl"><text x="32.0" y="130" transform="rotate(-90 32.0 130)">1 - 망각 게이트 f</text></g>
<text class="ttl2 l" x="292.0" y="18">유닛별 반감기</text>
<g class="axis">
<line x1="300.0" y1="196.0" x2="440.0" y2="196.0"/>
<text class="tick-lbl" x="294.0" y="199.5" text-anchor="end">0.5</text>
<line x1="300.0" y1="140.0" x2="440.0" y2="140.0"/>
<text class="tick-lbl" x="294.0" y="143.5" text-anchor="end">1</text>
<line x1="300.0" y1="84.0" x2="440.0" y2="84.0"/>
<text class="tick-lbl" x="294.0" y="87.5" text-anchor="end">2</text>
<line x1="300.0" y1="51.2" x2="440.0" y2="51.2"/>
<text class="tick-lbl" x="294.0" y="54.7" text-anchor="end">3</text>
</g>
<path class="curve ok3" d="M300.0,183.1 L300.4,181.4 L300.9,178.9 L301.3,178.3 L301.7,178.3 L302.2,176.1 L302.6,175.6 L303.0,175.2 L303.5,174.0 L303.9,173.5 L304.3,173.0 L304.8,171.2 L305.2,171.0 L305.6,170.6 L306.0,169.9 L306.5,168.5 L306.9,167.5 L307.3,167.1 L307.8,166.8 L308.2,166.6 L308.6,166.2 L309.1,166.2 L309.5,165.9 L309.9,165.7 L310.4,165.7 L310.8,165.1 L311.2,164.9 L311.7,164.9 L312.1,164.8 L312.5,164.7 L313.0,164.0 L313.4,163.7 L313.8,163.7 L314.3,163.2 L314.7,163.2 L315.1,163.1 L315.6,163.0 L316.0,162.9 L316.4,162.8 L316.9,162.4 L317.3,162.3 L317.7,162.2 L318.1,161.7 L318.6,161.6 L319.0,161.4 L319.4,161.1 L319.9,161.0 L320.3,160.4 L320.7,160.0 L321.2,159.1 L321.6,158.9 L322.0,158.9 L322.5,158.9 L322.9,158.8 L323.3,158.7 L323.8,158.5 L324.2,158.5 L324.6,158.4 L325.1,158.2 L325.5,157.9 L325.9,157.9 L326.4,157.9 L326.8,157.6 L327.2,157.5 L327.7,157.4 L328.1,156.8 L328.5,156.6 L329.0,156.6 L329.4,156.2 L329.8,156.2 L330.2,156.1 L330.7,155.8 L331.1,155.1 L331.5,155.0 L332.0,154.6 L332.4,154.6 L332.8,154.3 L333.3,154.0 L333.7,153.9 L334.1,153.9 L334.6,153.9 L335.0,153.8 L335.4,153.6 L335.9,153.5 L336.3,152.7 L336.7,152.7 L337.2,152.7 L337.6,152.4 L338.0,152.4 L338.5,152.2 L338.9,151.9 L339.3,151.4 L339.8,150.9 L340.2,150.9 L340.6,150.7 L341.0,150.7 L341.5,150.6 L341.9,150.5 L342.3,150.5 L342.8,150.5 L343.2,150.3 L343.6,150.3 L344.1,150.3 L344.5,150.2 L344.9,150.2 L345.4,150.0 L345.8,149.3 L346.2,149.0 L346.7,148.8 L347.1,148.8 L347.5,148.6 L348.0,148.6 L348.4,148.5 L348.8,148.4 L349.3,148.3 L349.7,148.3 L350.1,148.1 L350.6,147.4 L351.0,147.2 L351.4,147.2 L351.9,147.1 L352.3,147.0 L352.7,146.9 L353.1,146.4 L353.6,146.4 L354.0,146.3 L354.4,146.3 L354.9,146.2 L355.3,146.2 L355.7,146.2 L356.2,146.0 L356.6,145.9 L357.0,145.8 L357.5,145.7 L357.9,145.7 L358.3,145.6 L358.8,145.4 L359.2,145.4 L359.6,145.3 L360.1,145.2 L360.5,145.1 L360.9,144.9 L361.4,144.8 L361.8,144.7 L362.2,144.3 L362.7,144.3 L363.1,144.0 L363.5,143.9 L364.0,143.9 L364.4,143.8 L364.8,143.8 L365.2,143.6 L365.7,143.6 L366.1,143.4 L366.5,143.2 L367.0,142.9 L367.4,142.4 L367.8,142.4 L368.3,142.2 L368.7,142.2 L369.1,141.9 L369.6,141.8 L370.0,141.4 L370.4,141.4 L370.9,141.3 L371.3,141.3 L371.7,141.2 L372.2,140.8 L372.6,140.7 L373.0,140.6 L373.5,140.3 L373.9,140.3 L374.3,139.9 L374.8,139.9 L375.2,139.7 L375.6,139.7 L376.0,139.6 L376.5,139.5 L376.9,139.4 L377.3,139.3 L377.8,139.3 L378.2,139.3 L378.6,139.1 L379.1,138.9 L379.5,138.9 L379.9,138.7 L380.4,138.5 L380.8,138.3 L381.2,138.1 L381.7,138.0 L382.1,137.9 L382.5,137.9 L383.0,137.7 L383.4,137.3 L383.8,137.0 L384.3,136.9 L384.7,136.9 L385.1,136.7 L385.6,136.7 L386.0,136.4 L386.4,136.3 L386.9,136.3 L387.3,135.9 L387.7,135.7 L388.1,135.5 L388.6,135.5 L389.0,135.4 L389.4,135.4 L389.9,135.1 L390.3,134.7 L390.7,134.5 L391.2,134.4 L391.6,134.4 L392.0,134.4 L392.5,133.8 L392.9,133.3 L393.3,133.3 L393.8,132.8 L394.2,132.7 L394.6,132.4 L395.1,132.3 L395.5,132.2 L395.9,132.0 L396.4,131.9 L396.8,131.8 L397.2,131.8 L397.7,131.8 L398.1,131.7 L398.5,131.7 L399.0,131.3 L399.4,131.3 L399.8,130.7 L400.2,130.3 L400.7,130.0 L401.1,129.9 L401.5,129.8 L402.0,129.7 L402.4,129.6 L402.8,129.3 L403.3,129.0 L403.7,128.1 L404.1,127.9 L404.6,127.9 L405.0,127.8 L405.4,127.7 L405.9,126.9 L406.3,126.6 L406.7,126.4 L407.2,125.8 L407.6,125.5 L408.0,125.5 L408.5,125.2 L408.9,124.9 L409.3,124.8 L409.8,124.8 L410.2,124.2 L410.6,124.0 L411.0,123.9 L411.5,123.8 L411.9,122.8 L412.3,122.7 L412.8,122.7 L413.2,122.6 L413.6,122.5 L414.1,122.4 L414.5,121.7 L414.9,121.6 L415.4,121.6 L415.8,121.4 L416.2,121.3 L416.7,121.1 L417.1,120.9 L417.5,120.6 L418.0,120.4 L418.4,120.3 L418.8,120.1 L419.3,120.0 L419.7,119.9 L420.1,118.9 L420.6,118.3 L421.0,118.2 L421.4,118.2 L421.9,117.7 L422.3,117.7 L422.7,117.6 L423.1,117.1 L423.6,117.0 L424.0,117.0 L424.4,116.1 L424.9,116.1 L425.3,115.5 L425.7,115.2 L426.2,114.5 L426.6,114.2 L427.0,114.1 L427.5,113.8 L427.9,113.6 L428.3,113.5 L428.8,113.3 L429.2,112.9 L429.6,112.8 L430.1,112.4 L430.5,112.3 L430.9,111.4 L431.4,111.3 L431.8,110.7 L432.2,110.3 L432.7,109.9 L433.1,109.5 L433.5,109.4 L434.0,109.1 L434.4,108.6 L434.8,108.3 L435.2,108.3 L435.7,107.8 L436.1,107.5 L436.5,105.9 L437.0,105.6 L437.4,104.4 L437.8,104.1 L438.3,102.7 L438.7,99.6 L439.1,96.6 L439.6,95.8 L440.0,51.5" fill="none"/>
<text class="lbl ok" x="438.0" y="44.5" text-anchor="end">LSTM f</text>
<path class="curve ok2" d="M300.0,205.0 L300.4,200.3 L300.7,199.6 L301.1,198.4 L301.5,197.4 L301.8,196.7 L302.2,195.8 L302.6,195.5 L302.9,195.4 L303.3,194.1 L303.7,193.9 L304.1,191.8 L304.4,191.1 L304.8,190.6 L305.2,190.5 L305.5,190.5 L305.9,189.8 L306.3,189.1 L306.6,188.9 L307.0,188.7 L307.4,187.8 L307.7,187.6 L308.1,187.2 L308.5,186.8 L308.8,186.5 L309.2,186.5 L309.6,186.2 L309.9,185.7 L310.3,185.3 L310.7,185.3 L311.1,185.1 L311.4,185.0 L311.8,184.8 L312.2,184.7 L312.5,184.5 L312.9,183.8 L313.3,183.6 L313.6,183.6 L314.0,183.0 L314.4,182.5 L314.7,182.4 L315.1,182.2 L315.5,182.1 L315.8,182.0 L316.2,182.0 L316.6,181.6 L316.9,181.1 L317.3,181.0 L317.7,181.0 L318.1,180.7 L318.4,180.6 L318.8,180.2 L319.2,180.1 L319.5,180.1 L319.9,180.0 L320.3,179.8 L320.6,179.7 L321.0,179.7 L321.4,179.5 L321.7,179.4 L322.1,179.0 L322.5,178.7 L322.8,178.7 L323.2,178.4 L323.6,178.4 L323.9,178.4 L324.3,178.2 L324.7,178.1 L325.1,178.1 L325.4,177.8 L325.8,177.4 L326.2,177.4 L326.5,177.0 L326.9,176.9 L327.3,176.8 L327.6,176.8 L328.0,176.8 L328.4,176.8 L328.7,176.7 L329.1,176.7 L329.5,176.6 L329.8,176.5 L330.2,176.4 L330.6,176.3 L330.9,176.1 L331.3,176.1 L331.7,176.0 L332.1,175.9 L332.4,175.7 L332.8,175.6 L333.2,175.5 L333.5,175.3 L333.9,175.2 L334.3,174.9 L334.6,174.9 L335.0,174.7 L335.4,174.7 L335.7,174.4 L336.1,174.3 L336.5,174.0 L336.8,173.8 L337.2,173.7 L337.6,173.7 L337.9,173.5 L338.3,173.1 L338.7,173.0 L339.1,173.0 L339.4,172.9 L339.8,172.7 L340.2,172.6 L340.5,172.6 L340.9,172.5 L341.3,172.5 L341.6,172.1 L342.0,171.9 L342.4,171.8 L342.7,171.7 L343.1,171.5 L343.5,171.4 L343.8,171.4 L344.2,171.3 L344.6,171.2 L344.9,171.0 L345.3,171.0 L345.7,170.9 L346.1,170.8 L346.4,170.7 L346.8,170.7 L347.2,170.6 L347.5,170.5 L347.9,170.5 L348.3,170.4 L348.6,170.2 L349.0,170.0 L349.4,169.9 L349.7,169.9 L350.1,169.8 L350.5,169.8 L350.8,169.6 L351.2,169.5 L351.6,169.4 L351.9,169.4 L352.3,169.3 L352.7,169.0 L353.1,169.0 L353.4,169.0 L353.8,168.9 L354.2,168.3 L354.5,168.2 L354.9,168.1 L355.3,168.1 L355.6,167.9 L356.0,167.9 L356.4,167.6 L356.7,167.5 L357.1,167.4 L357.5,167.2 L357.8,166.9 L358.2,166.8 L358.6,166.6 L358.9,166.6 L359.3,166.3 L359.7,166.2 L360.1,166.0 L360.4,165.9 L360.8,165.9 L361.2,165.6 L361.5,165.6 L361.9,165.6 L362.3,165.5 L362.6,165.3 L363.0,165.2 L363.4,165.1 L363.7,164.9 L364.1,164.9 L364.5,164.8 L364.8,164.5 L365.2,164.0 L365.6,163.9 L365.9,163.8 L366.3,163.8 L366.7,163.5 L367.1,163.4 L367.4,163.4 L367.8,163.4 L368.2,163.3 L368.5,163.3 L368.9,163.1 L369.3,163.0 L369.6,163.0 L370.0,163.0 L370.4,162.9 L370.7,162.8 L371.1,162.6 L371.5,162.6 L371.8,162.2 L372.2,162.1 L372.6,161.8 L372.9,161.8 L373.3,161.7 L373.7,161.5 L374.1,161.3 L374.4,161.2 L374.8,161.2 L375.2,161.1 L375.5,161.1 L375.9,161.0 L376.3,160.9 L376.6,160.8 L377.0,160.8 L377.4,160.7 L377.7,160.7 L378.1,160.4 L378.5,160.4 L378.8,160.3 L379.2,160.1 L379.6,160.1 L379.9,160.1 L380.3,160.0 L380.7,159.9 L381.1,159.8 L381.4,159.7 L381.8,159.5 L382.2,159.4 L382.5,159.3 L382.9,159.3 L383.3,159.2 L383.6,158.7 L384.0,158.7 L384.4,158.7 L384.7,158.5 L385.1,158.4 L385.5,158.4 L385.8,158.3 L386.2,158.2 L386.6,158.0 L386.9,157.9 L387.3,157.9 L387.7,157.8 L388.1,157.6 L388.4,157.6 L388.8,157.6 L389.2,157.6 L389.5,157.5 L389.9,157.4 L390.3,157.4 L390.6,157.4 L391.0,157.3 L391.4,156.9 L391.7,156.7 L392.1,156.6 L392.5,156.6 L392.8,156.0 L393.2,156.0 L393.6,156.0 L393.9,155.7 L394.3,155.6 L394.7,155.1 L395.1,154.5 L395.4,154.5 L395.8,154.4 L396.2,154.2 L396.5,154.1 L396.9,154.0 L397.3,154.0 L397.6,153.9 L398.0,153.8 L398.4,153.8 L398.7,153.7 L399.1,153.5 L399.5,153.5 L399.8,153.4 L400.2,153.3 L400.6,152.6 L400.9,152.4 L401.3,152.3 L401.7,152.1 L402.1,151.7 L402.4,151.0 L402.8,151.0 L403.2,150.9 L403.5,150.9 L403.9,150.6 L404.3,150.3 L404.6,150.2 L405.0,150.0 L405.4,149.5 L405.7,149.2 L406.1,149.1 L406.5,149.1 L406.8,148.9 L407.2,148.8 L407.6,148.7 L407.9,148.7 L408.3,148.4 L408.7,148.3 L409.1,147.8 L409.4,147.4 L409.8,147.3 L410.2,146.8 L410.5,146.8 L410.9,146.7 L411.3,146.6 L411.6,146.5 L412.0,146.2 L412.4,146.0 L412.7,145.8 L413.1,145.7 L413.5,145.6 L413.8,145.3 L414.2,144.7 L414.6,144.6 L414.9,144.4 L415.3,144.2 L415.7,144.2 L416.1,143.3 L416.4,143.3 L416.8,143.3 L417.2,142.7 L417.5,142.6 L417.9,142.5 L418.3,142.4 L418.6,142.1 L419.0,142.0 L419.4,141.8 L419.7,141.4 L420.1,141.1 L420.5,141.1 L420.8,140.7 L421.2,140.5 L421.6,140.5 L421.9,140.3 L422.3,140.1 L422.7,140.0 L423.1,138.7 L423.4,138.7 L423.8,138.4 L424.2,138.3 L424.5,137.9 L424.9,137.9 L425.3,137.3 L425.6,136.3 L426.0,135.6 L426.4,135.5 L426.7,135.3 L427.1,135.2 L427.5,134.9 L427.8,134.6 L428.2,133.9 L428.6,133.9 L428.9,132.8 L429.3,132.1 L429.7,131.0 L430.1,130.4 L430.4,130.2 L430.8,129.5 L431.2,129.4 L431.5,129.4 L431.9,129.1 L432.3,128.8 L432.6,128.1 L433.0,128.0 L433.4,127.0 L433.7,126.5 L434.1,125.8 L434.5,124.7 L434.8,123.1 L435.2,123.1 L435.6,122.5 L435.9,120.2 L436.3,119.8 L436.7,119.1 L437.1,118.9 L437.4,116.6 L437.8,116.0 L438.2,115.3 L438.5,105.3 L438.9,104.4 L439.3,101.8 L439.6,93.1 L440.0,88.4" fill="none"/>
<text class="lbl ok" x="438.0" y="100.4" text-anchor="end">GRU z</text>
<g class="lbl-ax"><text class="cap l" x="300.0" y="232">유닛 (정렬)</text></g>
</svg>
<figcaption>왼쪽: LSTM 의 입력 게이트 i 와 1 에서 망각 게이트를 뺀 값이 놓인 자리, 값 131만 개를 24 x 24 칸에 담았다. GRU 처럼 묶여 있다면 점선 위에 몰려야 하는데 사각형 전체에 퍼져 있다. 오른쪽: LSTM 의 망각 게이트와 GRU 의 갱신 게이트에서 나오는 유닛별 반감기. GRU 쪽이 더 짧다.</figcaption>
</figure>

```
i 와 (1 - f) 의 상관, 값 1,331,200 개 전체     +0.071
유닛별 상관   최소 -0.629   중앙 +0.052   최대 +0.768
상관 0.5 넘는 유닛                          13개 / 325
i + f 의 평균 (묶여 있으면 1.0)              1.156
```

왼쪽 그림에서 점들이 점선 위에 안 몰리고 사각형을 채운다. 두 게이트의 2차원
분포를 각자의 주변분포 곱과 대 보면 어긋남이 최대 칸당 `0.175%` 다 - 거의 완전한
독립이다.

**LSTM 은 자유도를 놀리지 않는다. 실제로 따로 쓴다.**

## 그런데도 진다

따로 쓰는데도 7편에서 GRU 가 `1.6449`, LSTM 이 `1.6776` 이다. 남은 설명은
폭이다. 게이트가 셋이면 같은 예산으로 상태를 더 크게 잡을 수 있다.

```
LSTM  게이트 4개  폭 325   4 x 325² = 422,500
GRU   게이트 3개  폭 381   3 x 381² = 435,483
```

같은 63만 예산에서 GRU 가 `17.2%` 넓다. 그래서 GRU 를 **LSTM 과 같은 폭 325**
로 묶어 다시 돌렸다. 상태 크기가 같아지는 대신 파라미터는 오히려 적어진다.

```
                파라미터    최소 검증 (시드 3개)              중앙값
GRU  폭 381     635,835   1.6449  1.6503  1.6276      1.6449
GRU  폭 325     489,675   1.6498  1.6624  1.6611      1.6611
LSTM 폭 325     637,550   1.6776  1.6737  1.6785      1.6776
```

**폭을 맞춰도 GRU 가 이긴다.** 그것도 파라미터를 `23.2%` 덜 쓰고서다. 시드
범위가 `1.6498~1.6624` 대 `1.6737~1.6785` 로 겹치지도 않는다.

이득이 정확히 반반으로 갈린다.

```
LSTM 폭 325   1.6776
GRU  폭 325   1.6611     구조가 사는 것  0.0165
GRU  폭 381   1.6449     폭이 사는 것    0.0162
```

절반은 게이트를 어떻게 짰느냐에서 오고, 절반은 게이트를 하나 덜 두어서 넓힐 수
있게 된 데서 온다.

## 잊는 속도는 GRU 가 더 빠르다

오른쪽 그림이다. 유닛별 게이트에서 반감기를 뽑으면

```
          최소    중앙    최대
LSTM f    0.59   0.98   2.99
GRU  z    0.45   0.75   1.89
```

GRU 가 전 구간에서 더 짧다. 2편에서 LSTM 유닛 중 열 자 넘게 붙드는 것이 하나도
없다고 했는데, GRU 는 두 자 넘는 것도 없다.

**더 빨리 잊는 쪽이 더 잘한다.** 8편에서 망각 게이트를 열어 도달을 늘렸을 때
손실이 나빠진 것과 같은 방향이다. 이 과제에서 오래 붙드는 것은 이득이 아니다.

## 남는 것

리셋 게이트 `r` 이 무엇을 하는지는 안 봤다. 평균이 `0.629` 로 반쯤 열려 있는데,
그것을 1 로 고정하면 무엇이 나빠지는지 재면 `r` 의 값을 알 수 있다. 안 쟀다.

그리고 "구조 절반, 폭 절반" 은 폭 325 한 점에서 잰 것이다. 폭을 더 넓히거나
좁히면 비율이 달라질 수 있다.

이 편의 모형도 전부 1층이다. 재귀를 2층으로 쌓으면 게이트 수와 폭의 거래가
어떻게 되는지는 이 시리즈에서 안 다룬다.

## 그래서

- GRU 한 걸음은 `h = z·h + (1-z)·n` 이다. LSTM 이 `f` 와 `i` 로 따로 정하던 것을
  `z` 하나로 정한다
- 리셋 게이트 `r` 은 LSTM 에 없다. GRU 는 게이트를 뺀 LSTM 이 아니라 다르게 짠
  것이다
- 손으로 돈 것과 `nn.GRU` 가 최대 `7.90e-07` 차이다
- LSTM 은 `i` 와 `1-f` 를 따로 쓴다. 상관 `+0.071`, `i + f` 평균 `1.156`,
  2차원 분포가 독립에서 벗어난 최대가 칸당 `0.175%`
- 그런데도 진다. 폭을 `325` 로 맞추면 GRU 가 `1.6611`, LSTM 이 `1.6776` 이고
  GRU 쪽이 파라미터를 `23.2%` 덜 쓴다. 시드 범위가 안 겹친다
- 이득이 반반이다. 구조에서 `0.0165`, 폭에서 `0.0162`
- 유닛별 반감기가 GRU `0.45~1.89` 자로 LSTM `0.59~2.99` 자보다 짧다. 더 빨리
  잊는 쪽이 더 잘한다
