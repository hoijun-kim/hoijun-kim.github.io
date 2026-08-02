---
title: "첫 층 커널이 배운 것은 줄 끝이었다"
description: "합성곱은 상태를 이고 가지 않는다. 자리마다 다섯 글자를 보는 커널 하나가 미끄러질 뿐이다. 학습된 첫 층에서 채널마다 제일 크게 반응하는 다섯 글자를 찾아 보면, 개행·소수점·백틱·쉼표를 잡는 것들이 나온다."
date: 2025-12-07
lang: ko
kind: guide
series:
  id: not-attention
  part: 4
---

1편부터 3편까지는 상태를 하나 들고 다니는 것들이었다. 합성곱은 아무것도 안
들고 다닌다. 자리마다 그 주변 몇 글자만 보고 답을 내고, 그게 전부다.

## 커널 하나가 하는 계산

커널은 **가중치 몇 개짜리 창**이다. 자리 `t` 에서 창 안의 글자들에 가중치를
곱해 더하고, 창을 한 칸 옮겨 또 한다.

<figure class="fig">
<svg viewBox="0 0 460 300" role="img" aria-label="위: 커널 5개짜리가 글자를 다섯 개씩 보면서 한 자리씩 미끄러지는 그림. 세 자리 모두 같은 커널을 쓴다. 아래: 학습된 채널 12 의 값이 개행마다 크게 올라간다">
<text class="ttl2 l" x="40.0" y="18">커널 하나가 자리마다 미끄러진다</text>
<g class="chars2">
<text x="96.0" y="42.0" text-anchor="middle">t</text>
<text x="122.0" y="42.0" text-anchor="middle">h</text>
<text x="148.0" y="42.0" text-anchor="middle">e</text>
<text x="174.0" y="42.0" text-anchor="middle">&#183;</text>
<text x="200.0" y="42.0" text-anchor="middle">c</text>
<text x="226.0" y="42.0" text-anchor="middle">a</text>
<text x="252.0" y="42.0" text-anchor="middle">t</text>
<text x="278.0" y="42.0" text-anchor="middle">&#183;</text>
<text x="304.0" y="42.0" text-anchor="middle">s</text>
<text x="330.0" y="42.0" text-anchor="middle">a</text>
<text x="356.0" y="42.0" text-anchor="middle">t</text>
</g>
<rect class="win" x="85.0" y="60.0" width="126.0" height="14" rx="3"/>
<path class="hop c" d="M200.0,74.0 L200.0,117.0" fill="none"/>
<circle class="dot" cx="200.0" cy="122.0" r="3"/>
<rect class="win" x="137.0" y="78.0" width="126.0" height="14" rx="3"/>
<path class="hop c" d="M252.0,92.0 L252.0,117.0" fill="none"/>
<circle class="dot" cx="252.0" cy="122.0" r="3"/>
<rect class="win" x="189.0" y="96.0" width="126.0" height="14" rx="3"/>
<path class="hop c" d="M304.0,110.0 L304.0,117.0" fill="none"/>
<circle class="dot" cx="304.0" cy="122.0" r="3"/>
<text class="lbl" x="452" y="71.0" text-anchor="end">세 자리 모두 같은 커널</text>
<text class="lbl" x="77.0" y="125.5" text-anchor="end">출력</text>
<text class="ttl2 l" x="40.0" y="172">그렇게 배운 채널 12 가 실제 글에서 내는 값</text>
<g class="axis">
<line x1="40.0" y1="258.0" x2="446.0" y2="258.0"/>
<text class="tick-lbl" x="34.0" y="261.5" text-anchor="end">-1</text>
<line x1="40.0" y1="228.0" x2="446.0" y2="228.0"/>
<text class="tick-lbl" x="34.0" y="231.5" text-anchor="end">+0</text>
<line x1="40.0" y1="198.0" x2="446.0" y2="198.0"/>
<text class="tick-lbl" x="34.0" y="201.5" text-anchor="end">+1</text>
</g><g class="guide">
<line x1="175.3" y1="182.0" x2="175.3" y2="280.0"/>
<line x1="258.6" y1="182.0" x2="258.6" y2="280.0"/>
<line x1="269.0" y1="182.0" x2="269.0" y2="280.0"/>
</g>
<path class="curve ok" d="M40.0,234.8 L50.4,216.6 L60.8,234.5 L71.2,208.9 L81.6,229.3 L92.1,228.6 L102.5,226.4 L112.9,212.6 L123.3,236.5 L133.7,201.0 L144.1,232.7 L154.5,229.9 L164.9,215.9 L175.3,191.1 L185.7,259.7 L196.2,233.3 L206.6,244.1 L217.0,209.8 L227.4,240.6 L237.8,222.3 L248.2,230.4 L258.6,193.3 L269.0,218.7 L279.4,243.3 L289.8,232.4 L300.3,233.1 L310.7,224.3 L321.1,208.8 L331.5,234.2 L341.9,228.0 L352.3,213.0 L362.7,237.6 L373.1,209.4 L383.5,229.4 L393.9,236.3 L404.4,220.2 L414.8,242.5 L425.2,220.9 L435.6,212.6 L446.0,238.7" fill="none"/>
<g class="chars">
<text x="40.0" y="278.0" text-anchor="middle">n</text>
<text x="50.4" y="278.0" text-anchor="middle">k</text>
<text x="60.8" y="278.0" text-anchor="middle">s</text>
<text x="71.2" y="278.0" text-anchor="middle">&#183;</text>
<text x="81.6" y="278.0" text-anchor="middle">a</text>
<text x="92.1" y="278.0" text-anchor="middle">n</text>
<text x="102.5" y="278.0" text-anchor="middle">d</text>
<text x="112.9" y="278.0" text-anchor="middle">&#183;</text>
<text x="123.3" y="278.0" text-anchor="middle">`</text>
<text x="133.7" y="278.0" text-anchor="middle">m</text>
<text x="144.1" y="278.0" text-anchor="middle">+</text>
<text x="154.5" y="278.0" text-anchor="middle">1</text>
<text x="164.9" y="278.0" text-anchor="middle">`</text>
<text x="175.3" y="278.0" text-anchor="middle">&#182;</text>
<text x="185.7" y="278.0" text-anchor="middle">p</text>
<text x="196.2" y="278.0" text-anchor="middle">i</text>
<text x="206.6" y="278.0" text-anchor="middle">e</text>
<text x="217.0" y="278.0" text-anchor="middle">c</text>
<text x="227.4" y="278.0" text-anchor="middle">e</text>
<text x="237.8" y="278.0" text-anchor="middle">s</text>
<text x="248.2" y="278.0" text-anchor="middle">.</text>
<text x="258.6" y="278.0" text-anchor="middle">&#182;</text>
<text x="269.0" y="278.0" text-anchor="middle">&#182;</text>
<text x="279.4" y="278.0" text-anchor="middle">H</text>
<text x="289.8" y="278.0" text-anchor="middle">e</text>
<text x="300.3" y="278.0" text-anchor="middle">r</text>
<text x="310.7" y="278.0" text-anchor="middle">e</text>
<text x="321.1" y="278.0" text-anchor="middle">&#183;</text>
<text x="331.5" y="278.0" text-anchor="middle">i</text>
<text x="341.9" y="278.0" text-anchor="middle">s</text>
<text x="352.3" y="278.0" text-anchor="middle">&#183;</text>
<text x="362.7" y="278.0" text-anchor="middle">`</text>
<text x="373.1" y="278.0" text-anchor="middle">s</text>
<text x="383.5" y="278.0" text-anchor="middle">i</text>
<text x="393.9" y="278.0" text-anchor="middle">n</text>
<text x="404.4" y="278.0" text-anchor="middle">(</text>
<text x="414.8" y="278.0" text-anchor="middle">3</text>
<text x="425.2" y="278.0" text-anchor="middle">x</text>
<text x="435.6" y="278.0" text-anchor="middle">)</text>
<text x="446.0" y="278.0" text-anchor="middle">`</text>
</g>
<text class="lbl" x="40.0" y="293">개행 &#182;</text>
</svg>
<figcaption>위: 커널 5개짜리가 자리마다 다섯 글자를 보면서 한 칸씩 미끄러진다. 세 자리 모두 같은 커널이고, 창이 왼쪽으로만 뻗으므로 뒤를 못 본다. 아래: 그렇게 학습된 첫 층 채널 12 가 실제 글에서 내는 값. 세로선이 개행 자리인데 거기서 1.2 근처로 튀고, 개행이 아닌 자리 평균은 0.02 다.</figcaption>
</figure>

```python
xp = F.pad(x, (k-1, 0))            # 왼쪽으로만 k-1 만큼 채운다
for t in range(L):
    win = xp[:, :, t:t+k]          # (배치, 채널, k)
    out[:, :, t] = (win * W).sum() + b
```

이 줄을 학습된 가중치로 돌려서 `nn.Conv1d` 와 최대 `1.79e-06` 차이인 것을
확인했다. 아래 숫자는 거기서 나온다.

그림 위쪽에서 창 세 개가 **같은 커널**이다. 재귀가 걸음마다 같은 행렬을 쓰는
것과 같은 얘기인데, 방향이 다르다. 재귀는 시간축을 따라 같은 것을 쓰고 순서대로
가야 하지만, 합성곱은 자리축을 따라 같은 것을 쓰고 **자리들을 한꺼번에 계산**
할 수 있다.

## 길이가 늘어도 파라미터는 그대로

첫 합성곱 층의 가중치는 `(171, 171, 5)` 로 `146,205` 개다. 문맥이 128자든
1024자든 이 숫자는 안 변한다. 커널은 자리 하나 주변만 보기 때문이다.

자리를 자리에 다 잇는 촘촘한 층으로 같은 일을 하려면 `128 x 171 = 21,888` 개
입력을 그만큼의 출력에 이어야 하니 `479,084,544` 개가 필요하다. **3,277배**다.

모형 전체로는

```
tok.weight        (100, 128)      12,800
inp.weight     (171, 128, 1)      21,888
convs.0~3   (171, 171, 5) x 4    585,504    91.6%
head.weight       (100, 171)      17,100
바이어스와 정규화                    1,981
                                 639,273
```

커널 넷이 `91.6%` 다. 1편의 RNN 이 상태를 상태로 옮기는 데 73% 를 쓴 것처럼,
합성곱은 커널에 거의 다 쓴다.

## 인과로 만들려면 왼쪽만 채운다

다음 글자를 맞히는 일에서는 자리 `t` 가 `t` 뒤를 보면 안 된다. 답을 미리 보는
셈이 된다.

보통 합성곱은 양쪽을 대칭으로 채워서 창이 좌우로 뻗는데, 여기서는 **왼쪽으로만
`k-1` 만큼** 채운다. 그러면 자리 `t` 의 창이 `t-4` 에서 `t` 까지가 되고 뒤가
안 들어온다. 위 코드의 `F.pad(x, (k-1, 0))` 한 줄이 그것이다.

앞 시리즈 13편이 어텐션에서 마스크로 한 일을, 합성곱에서는 패딩 위치로 한다.

## 커널이 무엇에 반응하나

첫 층 채널마다 검증 데이터 `7,000` 자를 훑어 제일 크게 반응하는 다섯 글자를
찾으면 읽을 수 있는 것들이 나온다.

```
채널  12   'd^2`\n'  'arts\n'  'why.\n'  '887`\n'
채널 134   '# So\n'  ' the\n'  'd^2`\n'  'or a\n'
채널  20   'ver.\n'  'sum.\n'  'ces.\n'  'full\n'
채널 169   'um.\n\n'  '0`.\n\n'  'ad.\n\n'  '0885\n'
채널  59   ' 0.10'  ' 0.80'  '/0.80'  '`0.80'
채널 105   '`m+1`'  ' = 0`'  ' = 8`'  '0.02`'
채널  63   'bias,'  'ches,'  'ides,'  'odels'
채널  51   ' add '  'y `Σ '  ' 90% '  'eads '
```

세 채널이 **줄 끝**을 잡는다. `169` 번은 개행이 두 개 붙은 자리, 즉 **빈 줄**
이다. `59` 번은 **소수점 숫자**, `105` 번은 **백틱**, `63` 번은 **쉼표와 복수형
s**, `51` 번은 **띄어쓰기로 끝나는 것**이다.

그림 아래쪽이 채널 `12` 를 실제 글에 대고 그린 것이다. 개행 자리에서 `1.23` 과
`1.16` 으로 튀고, 개행이 아닌 자리 평균은 `0.02` 다.

첫 층이 하는 일이 이런 것이다. 다섯 글자짜리 창으로 볼 수 있는 것 - 줄이
끝났는지, 숫자인지, 코드인지 - 을 잡아 놓고, 위층이 그것들을 재료로 쓴다.

## 남는 것

여기서 본 것은 **첫 층**이다. 층을 올라가면 창이 넓어지는데 (2층은 9자, 4층은
17자) 위층 채널이 무엇을 잡는지는 안 봤다. 5편이 그 창 넓이 이야기다.

그리고 이 모형은 300걸음에서 검증 손실이 바닥이었다. 7편 표에서 다섯 구조 중
제일 빨리 바닥에 닿는데, 더 오래 돌리면 채널이 무엇으로 변하는지는 모른다.

커널 크기도 5 하나만 썼다. 3이나 7로 바꾸면 무엇이 달라지는지 안 쟀다.

## 그래서

- 합성곱은 상태를 안 들고 다닌다. 자리마다 다섯 글자짜리 창을 곱해 더할 뿐이다
- 손으로 돈 것과 `nn.Conv1d` 가 최대 `1.79e-06` 차이다
- 창 세 개가 전부 같은 커널이다. 재귀는 시간축으로, 합성곱은 자리축으로 같은
  가중치를 쓴다
- 첫 층 커널은 `(171, 171, 5)` 로 `146,205` 개이고 문맥 길이와 무관하다. 촘촘한
  층으로 같은 일을 하면 `479,084,544` 개, `3,277` 배가 든다
- 모형 파라미터의 `91.6%` 가 커널 넷이다
- 인과성은 왼쪽으로만 `k-1` 채워서 만든다. 어텐션이 마스크로 하는 일을 패딩
  위치로 한다
- 첫 층 채널은 개행, 빈 줄, 소수점 숫자, 백틱, 쉼표 같은 것을 잡는다. 채널
  `12` 는 개행에서 `1.23`, 나머지 자리 평균 `0.02` 다
