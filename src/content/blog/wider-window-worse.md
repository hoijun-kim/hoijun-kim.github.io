---
title: "창을 공짜로 넓혔더니 나빠졌다"
description: "합성곱의 수용장을 17자에서 125자까지 넓혀 같은 예산으로 학습시켰다. 넓힐수록 손실이 오른다. 파라미터도 채널도 층도 그대로 두고 팽창으로만 17을 61로 넓힌 경우조차 0.10 나빠진다 - 팽창은 넓히는 게 아니라 성기게 하기 때문이다."
date: 2025-12-13
lang: ko
kind: guide
series:
  id: not-attention
  part: 5
---

4편에서 합성곱 모형이 왼쪽으로 열일곱 자까지만 본다는 것을 봤다. 다른 넷은
128자를 다 본다. 그러면 창을 넓히면 따라잡아야 한다.

넓혀 봤다.

## 창 넓이는 계산으로 나온다

커널 `k` 짜리 층을 팽창 `d` 로 쌓으면 수용장은

```
1 + Σ d_i · (k - 1)
```

이다. 커널 5짜리 4층이면 `1 + 4·4 = 17` 이고, 팽창을 `1, 2, 4, 8` 로 주면
`1 + 4·(1+2+4+8) = 61` 이다.

식이 맞는지는 재 보면 된다. 마지막 자리의 출력을 받아 두고, 뒤로 `d` 자 떨어진
글자를 다른 글자로 바꿔 다시 돌린다. 출력 차이가 **정확히 `0.0`** 이 되는 첫
`d` 가 수용장이다.

```
                  채널    파라미터    식      실측
k5 x4              171   639,273     17      17
k5 x8              122   639,370     33      33
k9 x4              128   633,828     33      33
k5 팽창 1-8         171   639,273     61      61
k5 팽창 1-16        153   635,763    125     125
```

다섯 다 식과 한 자도 안 틀린다. 4편에서 "그래프에 없으니 작은 게 아니라 없다"
고 한 것이 이것이다.

## 넓히는 세 가지 방법

층을 더 쌓거나, 커널을 키우거나, 팽창을 주는 것이다. 앞의 둘은 파라미터를
먹으므로 같은 예산에서는 채널을 줄여야 한다. 팽창은 **아무것도 안 먹는다.**

<figure class="fig">
<svg viewBox="0 0 460 348" role="img" aria-label="위: 커널 3 으로 세 층을 쌓았을 때 마지막 자리가 닿는 입력 자리들. 팽창 없이 쌓으면 7자, 1-2-4 로 벌리면 15자다. 아래: 수용장을 17에서 125까지 바꿔 같은 예산으로 학습한 검증 손실">
<text class="ttl2 l" x="30" y="30">팽창 없이 쌓으면</text>
<circle class="nd off" cx="30.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="138.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="150.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="162.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="174.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="186.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="198.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="30.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="138.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="150.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="162.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="174.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="186.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="198.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="30.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="138.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="150.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="162.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="174.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="186.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="198.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="30.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="42.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="54.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="66.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="78.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="90.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="102.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="114.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="126.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="138.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="150.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="162.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="174.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="186.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="198.0" cy="48.0" r="2.6"/>
<circle class="nd on" cx="210.0" cy="48.0" r="2.6"/>
<line class="lk" x1="162.0" y1="126.0" x2="162.0" y2="100.0"/>
<line class="lk" x1="150.0" y1="126.0" x2="162.0" y2="100.0"/>
<line class="lk" x1="138.0" y1="126.0" x2="162.0" y2="100.0"/>
<line class="lk" x1="174.0" y1="126.0" x2="174.0" y2="100.0"/>
<line class="lk" x1="162.0" y1="126.0" x2="174.0" y2="100.0"/>
<line class="lk" x1="150.0" y1="126.0" x2="174.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="126.0" x2="186.0" y2="100.0"/>
<line class="lk" x1="174.0" y1="126.0" x2="186.0" y2="100.0"/>
<line class="lk" x1="162.0" y1="126.0" x2="186.0" y2="100.0"/>
<line class="lk" x1="198.0" y1="126.0" x2="198.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="126.0" x2="198.0" y2="100.0"/>
<line class="lk" x1="174.0" y1="126.0" x2="198.0" y2="100.0"/>
<line class="lk" x1="210.0" y1="126.0" x2="210.0" y2="100.0"/>
<line class="lk" x1="198.0" y1="126.0" x2="210.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="126.0" x2="210.0" y2="100.0"/>
<line class="lk" x1="186.0" y1="100.0" x2="186.0" y2="74.0"/>
<line class="lk" x1="174.0" y1="100.0" x2="186.0" y2="74.0"/>
<line class="lk" x1="162.0" y1="100.0" x2="186.0" y2="74.0"/>
<line class="lk" x1="198.0" y1="100.0" x2="198.0" y2="74.0"/>
<line class="lk" x1="186.0" y1="100.0" x2="198.0" y2="74.0"/>
<line class="lk" x1="174.0" y1="100.0" x2="198.0" y2="74.0"/>
<line class="lk" x1="210.0" y1="100.0" x2="210.0" y2="74.0"/>
<line class="lk" x1="198.0" y1="100.0" x2="210.0" y2="74.0"/>
<line class="lk" x1="186.0" y1="100.0" x2="210.0" y2="74.0"/>
<line class="lk" x1="210.0" y1="74.0" x2="210.0" y2="48.0"/>
<line class="lk" x1="198.0" y1="74.0" x2="210.0" y2="48.0"/>
<line class="lk" x1="186.0" y1="74.0" x2="210.0" y2="48.0"/>
<text class="lbl ok" x="210" y="38" text-anchor="end">수용장 7자</text>
<text class="ttl2 l" x="250" y="30">1-2-4 로 벌리면</text>
<circle class="nd off" cx="250.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="262.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="274.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="286.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="298.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="310.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="322.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="334.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="346.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="358.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="370.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="382.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="394.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="406.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="418.0" cy="126.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="126.0" r="2.6"/>
<circle class="nd off" cx="250.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="262.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="274.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="286.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="298.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="310.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="322.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="334.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="346.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="358.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="370.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="382.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="394.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="406.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="418.0" cy="100.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="100.0" r="2.6"/>
<circle class="nd off" cx="250.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="262.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="274.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="286.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="298.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="310.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="322.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="334.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="346.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="358.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="370.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="382.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="394.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="406.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="418.0" cy="74.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="74.0" r="2.6"/>
<circle class="nd off" cx="250.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="262.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="274.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="286.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="298.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="310.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="322.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="334.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="346.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="358.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="370.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="382.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="394.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="406.0" cy="48.0" r="2.6"/>
<circle class="nd off" cx="418.0" cy="48.0" r="2.6"/>
<circle class="nd on" cx="430.0" cy="48.0" r="2.6"/>
<line class="lk" x1="286.0" y1="126.0" x2="286.0" y2="100.0"/>
<line class="lk" x1="274.0" y1="126.0" x2="286.0" y2="100.0"/>
<line class="lk" x1="262.0" y1="126.0" x2="286.0" y2="100.0"/>
<line class="lk" x1="310.0" y1="126.0" x2="310.0" y2="100.0"/>
<line class="lk" x1="298.0" y1="126.0" x2="310.0" y2="100.0"/>
<line class="lk" x1="286.0" y1="126.0" x2="310.0" y2="100.0"/>
<line class="lk" x1="334.0" y1="126.0" x2="334.0" y2="100.0"/>
<line class="lk" x1="322.0" y1="126.0" x2="334.0" y2="100.0"/>
<line class="lk" x1="310.0" y1="126.0" x2="334.0" y2="100.0"/>
<line class="lk" x1="358.0" y1="126.0" x2="358.0" y2="100.0"/>
<line class="lk" x1="346.0" y1="126.0" x2="358.0" y2="100.0"/>
<line class="lk" x1="334.0" y1="126.0" x2="358.0" y2="100.0"/>
<line class="lk" x1="382.0" y1="126.0" x2="382.0" y2="100.0"/>
<line class="lk" x1="370.0" y1="126.0" x2="382.0" y2="100.0"/>
<line class="lk" x1="358.0" y1="126.0" x2="382.0" y2="100.0"/>
<line class="lk" x1="406.0" y1="126.0" x2="406.0" y2="100.0"/>
<line class="lk" x1="394.0" y1="126.0" x2="406.0" y2="100.0"/>
<line class="lk" x1="382.0" y1="126.0" x2="406.0" y2="100.0"/>
<line class="lk" x1="430.0" y1="126.0" x2="430.0" y2="100.0"/>
<line class="lk" x1="418.0" y1="126.0" x2="430.0" y2="100.0"/>
<line class="lk" x1="406.0" y1="126.0" x2="430.0" y2="100.0"/>
<line class="lk" x1="334.0" y1="100.0" x2="334.0" y2="74.0"/>
<line class="lk" x1="310.0" y1="100.0" x2="334.0" y2="74.0"/>
<line class="lk" x1="286.0" y1="100.0" x2="334.0" y2="74.0"/>
<line class="lk" x1="382.0" y1="100.0" x2="382.0" y2="74.0"/>
<line class="lk" x1="358.0" y1="100.0" x2="382.0" y2="74.0"/>
<line class="lk" x1="334.0" y1="100.0" x2="382.0" y2="74.0"/>
<line class="lk" x1="430.0" y1="100.0" x2="430.0" y2="74.0"/>
<line class="lk" x1="406.0" y1="100.0" x2="430.0" y2="74.0"/>
<line class="lk" x1="382.0" y1="100.0" x2="430.0" y2="74.0"/>
<line class="lk" x1="430.0" y1="74.0" x2="430.0" y2="48.0"/>
<line class="lk" x1="382.0" y1="74.0" x2="430.0" y2="48.0"/>
<line class="lk" x1="334.0" y1="74.0" x2="430.0" y2="48.0"/>
<text class="lbl ok" x="430" y="38" text-anchor="end">수용장 15자</text>
<text class="ttl2 l" x="30.0" y="192">수용장에 따른 최소 검증 손실</text>
<g class="axis">
<line x1="76.0" y1="296.0" x2="430.0" y2="296.0"/>
<text class="tick-lbl" x="70.0" y="299.5" text-anchor="end">1.65</text>
<line x1="76.0" y1="276.0" x2="430.0" y2="276.0"/>
<text class="tick-lbl" x="70.0" y="279.5" text-anchor="end">1.75</text>
<line x1="76.0" y1="256.0" x2="430.0" y2="256.0"/>
<text class="tick-lbl" x="70.0" y="259.5" text-anchor="end">1.85</text>
<line x1="76.0" y1="236.0" x2="430.0" y2="236.0"/>
<text class="tick-lbl" x="70.0" y="239.5" text-anchor="end">1.95</text>
<line x1="76.0" y1="216.0" x2="430.0" y2="216.0"/>
<text class="tick-lbl" x="70.0" y="219.5" text-anchor="end">2.05</text>
</g>
<line class="ref ok" x1="76.0" y1="297.0" x2="430.0" y2="297.0"/>
<text class="lbl ok" x="430.0" y="293.0" text-anchor="end">GRU 1.6449</text>
<line class="ref" x1="76.0" y1="272.4" x2="430.0" y2="272.4"/>
<text class="lbl bad" x="430.0" y="268.4" text-anchor="end">트랜스포머 1.7679</text>
<path class="curve ok2" d="M96.2,251.8 L203.0,239.1 L203.0,213.6 L302.0,231.7 L417.6,226.7" fill="none"/>
<circle class="dot" cx="96.2" cy="251.8" r="3"/>
<text class="lbl" x="96.2" y="243.8" text-anchor="middle">k5 x4</text>
<circle class="dot" cx="203.0" cy="239.1" r="3"/>
<text class="lbl" x="203.0" y="253.1" text-anchor="middle">k5 x8</text>
<circle class="dot" cx="203.0" cy="213.6" r="3"/>
<text class="lbl" x="203.0" y="205.6" text-anchor="middle">k9 x4</text>
<circle class="dot" cx="302.0" cy="231.7" r="3"/>
<text class="lbl" x="302.0" y="245.7" text-anchor="middle">k5 팽창 1-8</text>
<circle class="dot" cx="417.6" cy="226.7" r="3"/>
<text class="lbl" x="417.6" y="218.7" text-anchor="middle">k5 팽창 1-16</text>
<g class="lbl-ax">
<text x="96.2" y="321">17</text>
<text x="203.0" y="321">33</text>
<text x="302.0" y="321">61</text>
<text x="417.6" y="321">125</text>
<text class="cap l" x="76.0" y="336">수용장 (자, 로그)</text></g>
</svg>
<figcaption>위: 그리기 좋게 커널 3 으로 세 층을 쌓았을 때 마지막 자리가 닿는 입력들. 팽창 없이 쌓으면 7자, 1-2-4 로 벌리면 15자인데 선 개수는 같다. 실제 모형은 커널 5 다. 아래: 수용장만 17에서 125까지 바꿔 같은 예산으로 학습한 결과. 넓힐수록 나빠지고, 어느 것도 GRU 나 트랜스포머 근처에 못 간다.</figcaption>
</figure>

그림 위쪽이 그 차이다. 팽창을 주면 선 개수는 그대로인데 닿는 자리가 넓어진다.

## 넓힐수록 나빠진다

```
              수용장   채널    파라미터   최소 검증 (시드 3개)          중앙값
k5 x4            17    171   639,273   1.8748 1.8709 1.8695    1.8709
k5 x8            33    122   639,370   1.9437 1.9346 1.9326    1.9346
k9 x4            33    128   633,828   2.0592 2.0652 2.0621    2.0621
k5 팽창 1-8       61    171   639,273   1.9716 1.9795 1.9556    1.9716
k5 팽창 1-16     125    153   635,763   1.9967 2.0020 1.9907    1.9967
```

제일 좁은 것이 제일 낫다. `17` 자짜리가 `1.8709`, `125` 자짜리가 `1.9967` 이다.
그리고 어느 것도 GRU 의 `1.6449` 나 트랜스포머의 `1.7679` 근처에 못 간다.

층을 쌓거나 커널을 키우는 쪽은 설명이 있다. 예산이 고정이라 채널을 `171` 에서
`122` 나 `128` 로 줄여야 했으니, 창을 넓힌 값을 채널로 낸 것이다.

## 공짜로 넓혀도 나빠진다

팽창 쪽은 그 설명이 안 통한다. `k5 팽창 1-8` 은 `k5 x4` 와 채널 `171`,
파라미터 `639,273`, 층 4, 커널 5 가 **전부 같다.** 다른 것은 창이 `17` 이 아니라
`61` 이라는 것뿐이다.

그런데 `1.9716` 대 `1.8709` 로 `0.10` 나쁘다. 시드 범위가 `1.9556~1.9795` 대
`1.8695~1.8748` 로 겹치지도 않는다.

**공짜로 넓혔는데 손해다.**

## 팽창은 넓히는 게 아니라 성기게 한다

왜 그런지는 셀 수 있다. 출력에서 각 입력 자리로 가는 **경로가 몇 개**인지
세면 된다. 경로가 많을수록 그 자리에 배정된 계산이 많다는 뜻이다.

```
                수용장   경로 총수   닿는 자리   가까운 4자가 가진 몫
팽창 없이 x4        17       625        17개              11.2%
팽창 1-8           61       625        61개               1.6%
```

**경로 총수가 `625` 로 같다.** 팽창은 계산을 안 늘린다. 같은 `625` 개를 17자에
뿌리던 것을 61자에 뿌릴 뿐이다.

자리별로 보면 더 분명하다.

```
뒤로       0    1    2    3    4    5    6
팽창 없음   1    4   10   20   35   52   68
팽창 1-8   1    1    2    2    4    3    5
```

바로 앞 글자에 가는 경로가 `4` 개에서 `1` 개로, 네 배 줄었다. 1편에서 상태의
기억이 네 자 남짓이었고 2편에서 게이트도 그랬다. 그 네 자가 중요한 자리인데,
팽창은 거기 쓰던 계산을 멀리 가져가 버린다.

넓히는 게 아니라 **옮기는** 것이다.

## 같은 33자라도 만드는 법이 다르다

`k5 x8` 과 `k9 x4` 는 수용장이 둘 다 `33` 인데 `1.9346` 과 `2.0621` 로 `0.13`
차이가 난다. 층을 여덟 개 쌓는 쪽이 커널을 아홉으로 키우는 쪽보다 훨씬 낫다.

커널 하나를 키우면 파라미터가 `k` 에 비례해 늘고, 그만큼 채널이 깎인다. 층을
쌓으면 층마다 비선형이 하나씩 더 붙는다. **수용장이 같아도 그것을 어떻게 만드는
지가 손실을 가른다.**

## 7편의 문장 하나를 고친다

7편은 "CNN 은 왼쪽으로 17자만 본다. 예산이 아니라 시야에서 진다" 로 끝난다.
그 문장의 앞쪽은 맞고 뒤쪽은 틀렸다.

시야를 `125` 자로 넓혀도 `1.9967` 로 더 나빠진다. **CNN 이 지는 것은 시야가
좁아서가 아니다.** 이 과제에서 필요한 것이 좁은 시야이고, 넓히는 데 쓴 것은
어디서 빼 온 것이기 때문이다.

7편의 그 대목은 고쳐 두었다.

## 남는 것

여기서 비교한 것은 전부 1200걸음까지다. 다섯 설정이 모두 300~900걸음에서 바닥을
찍으므로 문제는 없지만, 더 긴 학습에서 순서가 그대로인지는 안 봤다.

그리고 "넓히면 나빠진다" 는 이 코퍼스, 이 과제 이야기다. 앞쪽 글자가 실제로
필요한 일 - 괄호 맞추기, 긴 복사 - 이라면 정반대일 것이다. 8편에서 재귀 쪽으로
같은 얘기를 한 번 더 한다.

팽창 조합도 `1-2-4-8` 과 `1-2-4-8-16` 둘만 봤다. `1-1-2-2` 처럼 가까운 데를
남기면서 조금만 벌리는 조합은 안 재 봤다.

## 그래서

- 수용장은 `1 + Σ d·(k-1)` 이고, 밖의 글자를 바꿔도 출력이 **정확히 0** 만큼
  달라지는 것으로 확인된다. 다섯 설정 다 식과 일치
- 넓힐수록 나빠진다. `17` 자 `1.8709` 에서 `125` 자 `1.9967` 까지
- 층·커널로 넓히면 채널을 깎아야 하니 그럴 만하다. 그런데 **팽창은 공짜인데도**
  `1.8709` 에서 `1.9716` 으로 나빠진다. 시드 범위가 안 겹친다
- 팽창은 경로를 안 늘린다. `625` 개를 17자에 뿌리던 것을 61자에 뿌릴 뿐이고,
  가까운 4자의 몫이 `11.2%` 에서 `1.6%` 로 준다
- 바로 앞 글자로 가는 경로가 `4` 개에서 `1` 개가 된다. 1편의 "기억은 네 자
  남짓" 이 중요한 자리인데 거기서 계산을 빼 간다
- 수용장이 같아도 만드는 법이 다르면 결과가 다르다. `33` 자를 층으로 만들면
  `1.9346`, 커널로 만들면 `2.0621`
- 7편의 "예산이 아니라 시야에서 진다" 는 틀렸다. 고쳤다
