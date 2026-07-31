---
title: "메모리를 1.6배 아끼고 시간을 1.7배 잃었다"
description: "10편은 조밀한 캐시 텐서의 길이를 제일 긴 행이 정한다는 데서 끝났다. 고정 크기 블록으로 쪼개면 최대 할당이 4,064에서 2,560 슬롯으로 준다. 그런데 흩어진 블록을 모아 오는 값이 아낀 것보다 컸다."
date: 2025-11-01
lang: ko
kind: guide
series:
  id: after-training
  part: 11
---

10편은 연속 배치가 캐시를 늘린다는 자리에서 멈췄다. 캐시를 하나의 조밀한
텐서로 들고 있으면 그 텐서의 길이는 항상 제일 긴 행이 정하고, 연속 배치는
오래 도는 긴 행 옆에 갓 들어온 짧은 행을 일부러 붙여 놓는다. 마지막 문단에
캐시를 고정 크기 블록으로 쪼개면 그 값이 사라진다고 적고 넘어갔다.

쪼개 봤다. 메모리는 적어 둔 대로 줄었고, 시간은 반대로 갔다.

## 쪼개면 얼마가 남나

블록 크기를 `S` 로 두면 캐시 길이가 `L` 인 행은 `ceil(L/S)` 개의 블록을 갖는다.
블록은 공용 풀에 있고, 행마다 블록 표가 어느 블록이 자기 것인지 가리킨다. 한
행의 블록들이 풀 안에서 붙어 있을 필요는 없다.

10편의 연속 배치 트레이스에서 할당이 제일 큰 스텝을 꺼내면

<figure class="fig">
<svg viewBox="0 0 460 322" role="img" aria-label="한 스텝의 캐시 할당. 왼쪽 조밀 배치는 32행이 모두 제일 긴 행 길이까지 채워진 직사각형이고, 오른쪽 블록 방식은 행마다 필요한 블록까지만 들쭉날쭉하게 찬다. 아래 곡선은 블록 크기가 커질수록 슬롯 합이 늘어 128에서는 조밀보다 나빠지는 것을 보여준다">
<text class="ttl2" x="130" y="24">조밀 - 모든 행이 제일 긴 행까지</text>
<text class="ttl2" x="342" y="24">블록 16 - 행마다 필요한 블록만</text>
<g class="alloc"><rect class="pad" x="46.0" y="34.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="34.0" width="22.3" height="2.7"/><rect class="pad" x="46.0" y="37.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="37.3" width="22.3" height="2.7"/><rect class="pad" x="46.0" y="40.6" width="166.7" height="2.7"/><rect class="use" x="46.0" y="40.6" width="47.2" height="2.7"/><rect class="pad" x="46.0" y="43.9" width="166.7" height="2.7"/><rect class="use" x="46.0" y="43.9" width="59.1" height="2.7"/><rect class="pad" x="46.0" y="47.2" width="166.7" height="2.7"/><rect class="use" x="46.0" y="47.2" width="61.7" height="2.7"/><rect class="pad" x="46.0" y="50.5" width="166.7" height="2.7"/><rect class="use" x="46.0" y="50.5" width="61.7" height="2.7"/><rect class="pad" x="46.0" y="53.8" width="166.7" height="2.7"/><rect class="use" x="46.0" y="53.8" width="65.6" height="2.7"/><rect class="pad" x="46.0" y="57.1" width="166.7" height="2.7"/><rect class="use" x="46.0" y="57.1" width="70.9" height="2.7"/><rect class="pad" x="46.0" y="60.4" width="166.7" height="2.7"/><rect class="use" x="46.0" y="60.4" width="72.2" height="2.7"/><rect class="pad" x="46.0" y="63.7" width="166.7" height="2.7"/><rect class="use" x="46.0" y="63.7" width="76.1" height="2.7"/><rect class="pad" x="46.0" y="67.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="67.0" width="78.8" height="2.7"/><rect class="pad" x="46.0" y="70.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="70.3" width="90.6" height="2.7"/><rect class="pad" x="46.0" y="73.6" width="166.7" height="2.7"/><rect class="use" x="46.0" y="73.6" width="93.2" height="2.7"/><rect class="pad" x="46.0" y="76.9" width="166.7" height="2.7"/><rect class="use" x="46.0" y="76.9" width="93.2" height="2.7"/><rect class="pad" x="46.0" y="80.2" width="166.7" height="2.7"/><rect class="use" x="46.0" y="80.2" width="93.2" height="2.7"/><rect class="pad" x="46.0" y="83.5" width="166.7" height="2.7"/><rect class="use" x="46.0" y="83.5" width="94.5" height="2.7"/><rect class="pad" x="46.0" y="86.8" width="166.7" height="2.7"/><rect class="use" x="46.0" y="86.8" width="95.8" height="2.7"/><rect class="pad" x="46.0" y="90.1" width="166.7" height="2.7"/><rect class="use" x="46.0" y="90.1" width="101.1" height="2.7"/><rect class="pad" x="46.0" y="93.4" width="166.7" height="2.7"/><rect class="use" x="46.0" y="93.4" width="101.1" height="2.7"/><rect class="pad" x="46.0" y="96.7" width="166.7" height="2.7"/><rect class="use" x="46.0" y="96.7" width="103.7" height="2.7"/><rect class="pad" x="46.0" y="100.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="100.0" width="105.0" height="2.7"/><rect class="pad" x="46.0" y="103.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="103.3" width="105.0" height="2.7"/><rect class="pad" x="46.0" y="106.6" width="166.7" height="2.7"/><rect class="use" x="46.0" y="106.6" width="110.2" height="2.7"/><rect class="pad" x="46.0" y="109.9" width="166.7" height="2.7"/><rect class="use" x="46.0" y="109.9" width="112.9" height="2.7"/><rect class="pad" x="46.0" y="113.2" width="166.7" height="2.7"/><rect class="use" x="46.0" y="113.2" width="120.8" height="2.7"/><rect class="pad" x="46.0" y="116.5" width="166.7" height="2.7"/><rect class="use" x="46.0" y="116.5" width="123.4" height="2.7"/><rect class="pad" x="46.0" y="119.8" width="166.7" height="2.7"/><rect class="use" x="46.0" y="119.8" width="123.4" height="2.7"/><rect class="pad" x="46.0" y="123.1" width="166.7" height="2.7"/><rect class="use" x="46.0" y="123.1" width="128.6" height="2.7"/><rect class="pad" x="46.0" y="126.4" width="166.7" height="2.7"/><rect class="use" x="46.0" y="126.4" width="149.6" height="2.7"/><rect class="pad" x="46.0" y="129.7" width="166.7" height="2.7"/><rect class="use" x="46.0" y="129.7" width="157.5" height="2.7"/><rect class="pad" x="46.0" y="133.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="133.0" width="160.1" height="2.7"/><rect class="pad" x="46.0" y="136.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="136.3" width="166.7" height="2.7"/><rect class="pad" x="258.0" y="34.0" width="42.0" height="2.7"/><rect class="use" x="258.0" y="34.0" width="22.3" height="2.7"/><line class="blk" x1="279.0" y1="34.0" x2="279.0" y2="36.7"/><rect class="pad" x="258.0" y="37.3" width="42.0" height="2.7"/><rect class="use" x="258.0" y="37.3" width="22.3" height="2.7"/><line class="blk" x1="279.0" y1="37.3" x2="279.0" y2="40.0"/><rect class="pad" x="258.0" y="40.6" width="63.0" height="2.7"/><rect class="use" x="258.0" y="40.6" width="47.2" height="2.7"/><line class="blk" x1="279.0" y1="40.6" x2="279.0" y2="43.3"/><line class="blk" x1="300.0" y1="40.6" x2="300.0" y2="43.3"/><rect class="pad" x="258.0" y="43.9" width="63.0" height="2.7"/><rect class="use" x="258.0" y="43.9" width="59.1" height="2.7"/><line class="blk" x1="279.0" y1="43.9" x2="279.0" y2="46.6"/><line class="blk" x1="300.0" y1="43.9" x2="300.0" y2="46.6"/><rect class="pad" x="258.0" y="47.2" width="63.0" height="2.7"/><rect class="use" x="258.0" y="47.2" width="61.7" height="2.7"/><line class="blk" x1="279.0" y1="47.2" x2="279.0" y2="49.9"/><line class="blk" x1="300.0" y1="47.2" x2="300.0" y2="49.9"/><rect class="pad" x="258.0" y="50.5" width="63.0" height="2.7"/><rect class="use" x="258.0" y="50.5" width="61.7" height="2.7"/><line class="blk" x1="279.0" y1="50.5" x2="279.0" y2="53.2"/><line class="blk" x1="300.0" y1="50.5" x2="300.0" y2="53.2"/><rect class="pad" x="258.0" y="53.8" width="84.0" height="2.7"/><rect class="use" x="258.0" y="53.8" width="65.6" height="2.7"/><line class="blk" x1="279.0" y1="53.8" x2="279.0" y2="56.5"/><line class="blk" x1="300.0" y1="53.8" x2="300.0" y2="56.5"/><line class="blk" x1="321.0" y1="53.8" x2="321.0" y2="56.5"/><rect class="pad" x="258.0" y="57.1" width="84.0" height="2.7"/><rect class="use" x="258.0" y="57.1" width="70.9" height="2.7"/><line class="blk" x1="279.0" y1="57.1" x2="279.0" y2="59.8"/><line class="blk" x1="300.0" y1="57.1" x2="300.0" y2="59.8"/><line class="blk" x1="321.0" y1="57.1" x2="321.0" y2="59.8"/><rect class="pad" x="258.0" y="60.4" width="84.0" height="2.7"/><rect class="use" x="258.0" y="60.4" width="72.2" height="2.7"/><line class="blk" x1="279.0" y1="60.4" x2="279.0" y2="63.1"/><line class="blk" x1="300.0" y1="60.4" x2="300.0" y2="63.1"/><line class="blk" x1="321.0" y1="60.4" x2="321.0" y2="63.1"/><rect class="pad" x="258.0" y="63.7" width="84.0" height="2.7"/><rect class="use" x="258.0" y="63.7" width="76.1" height="2.7"/><line class="blk" x1="279.0" y1="63.7" x2="279.0" y2="66.4"/><line class="blk" x1="300.0" y1="63.7" x2="300.0" y2="66.4"/><line class="blk" x1="321.0" y1="63.7" x2="321.0" y2="66.4"/><rect class="pad" x="258.0" y="67.0" width="84.0" height="2.7"/><rect class="use" x="258.0" y="67.0" width="78.8" height="2.7"/><line class="blk" x1="279.0" y1="67.0" x2="279.0" y2="69.7"/><line class="blk" x1="300.0" y1="67.0" x2="300.0" y2="69.7"/><line class="blk" x1="321.0" y1="67.0" x2="321.0" y2="69.7"/><rect class="pad" x="258.0" y="70.3" width="105.0" height="2.7"/><rect class="use" x="258.0" y="70.3" width="90.6" height="2.7"/><line class="blk" x1="279.0" y1="70.3" x2="279.0" y2="73.0"/><line class="blk" x1="300.0" y1="70.3" x2="300.0" y2="73.0"/><line class="blk" x1="321.0" y1="70.3" x2="321.0" y2="73.0"/><line class="blk" x1="342.0" y1="70.3" x2="342.0" y2="73.0"/><rect class="pad" x="258.0" y="73.6" width="105.0" height="2.7"/><rect class="use" x="258.0" y="73.6" width="93.2" height="2.7"/><line class="blk" x1="279.0" y1="73.6" x2="279.0" y2="76.3"/><line class="blk" x1="300.0" y1="73.6" x2="300.0" y2="76.3"/><line class="blk" x1="321.0" y1="73.6" x2="321.0" y2="76.3"/><line class="blk" x1="342.0" y1="73.6" x2="342.0" y2="76.3"/><rect class="pad" x="258.0" y="76.9" width="105.0" height="2.7"/><rect class="use" x="258.0" y="76.9" width="93.2" height="2.7"/><line class="blk" x1="279.0" y1="76.9" x2="279.0" y2="79.6"/><line class="blk" x1="300.0" y1="76.9" x2="300.0" y2="79.6"/><line class="blk" x1="321.0" y1="76.9" x2="321.0" y2="79.6"/><line class="blk" x1="342.0" y1="76.9" x2="342.0" y2="79.6"/><rect class="pad" x="258.0" y="80.2" width="105.0" height="2.7"/><rect class="use" x="258.0" y="80.2" width="93.2" height="2.7"/><line class="blk" x1="279.0" y1="80.2" x2="279.0" y2="82.9"/><line class="blk" x1="300.0" y1="80.2" x2="300.0" y2="82.9"/><line class="blk" x1="321.0" y1="80.2" x2="321.0" y2="82.9"/><line class="blk" x1="342.0" y1="80.2" x2="342.0" y2="82.9"/><rect class="pad" x="258.0" y="83.5" width="105.0" height="2.7"/><rect class="use" x="258.0" y="83.5" width="94.5" height="2.7"/><line class="blk" x1="279.0" y1="83.5" x2="279.0" y2="86.2"/><line class="blk" x1="300.0" y1="83.5" x2="300.0" y2="86.2"/><line class="blk" x1="321.0" y1="83.5" x2="321.0" y2="86.2"/><line class="blk" x1="342.0" y1="83.5" x2="342.0" y2="86.2"/><rect class="pad" x="258.0" y="86.8" width="105.0" height="2.7"/><rect class="use" x="258.0" y="86.8" width="95.8" height="2.7"/><line class="blk" x1="279.0" y1="86.8" x2="279.0" y2="89.5"/><line class="blk" x1="300.0" y1="86.8" x2="300.0" y2="89.5"/><line class="blk" x1="321.0" y1="86.8" x2="321.0" y2="89.5"/><line class="blk" x1="342.0" y1="86.8" x2="342.0" y2="89.5"/><rect class="pad" x="258.0" y="90.1" width="105.0" height="2.7"/><rect class="use" x="258.0" y="90.1" width="101.1" height="2.7"/><line class="blk" x1="279.0" y1="90.1" x2="279.0" y2="92.8"/><line class="blk" x1="300.0" y1="90.1" x2="300.0" y2="92.8"/><line class="blk" x1="321.0" y1="90.1" x2="321.0" y2="92.8"/><line class="blk" x1="342.0" y1="90.1" x2="342.0" y2="92.8"/><rect class="pad" x="258.0" y="93.4" width="105.0" height="2.7"/><rect class="use" x="258.0" y="93.4" width="101.1" height="2.7"/><line class="blk" x1="279.0" y1="93.4" x2="279.0" y2="96.1"/><line class="blk" x1="300.0" y1="93.4" x2="300.0" y2="96.1"/><line class="blk" x1="321.0" y1="93.4" x2="321.0" y2="96.1"/><line class="blk" x1="342.0" y1="93.4" x2="342.0" y2="96.1"/><rect class="pad" x="258.0" y="96.7" width="105.0" height="2.7"/><rect class="use" x="258.0" y="96.7" width="103.7" height="2.7"/><line class="blk" x1="279.0" y1="96.7" x2="279.0" y2="99.4"/><line class="blk" x1="300.0" y1="96.7" x2="300.0" y2="99.4"/><line class="blk" x1="321.0" y1="96.7" x2="321.0" y2="99.4"/><line class="blk" x1="342.0" y1="96.7" x2="342.0" y2="99.4"/><rect class="pad" x="258.0" y="100.0" width="105.0" height="2.7"/><rect class="use" x="258.0" y="100.0" width="105.0" height="2.7"/><line class="blk" x1="279.0" y1="100.0" x2="279.0" y2="102.7"/><line class="blk" x1="300.0" y1="100.0" x2="300.0" y2="102.7"/><line class="blk" x1="321.0" y1="100.0" x2="321.0" y2="102.7"/><line class="blk" x1="342.0" y1="100.0" x2="342.0" y2="102.7"/><rect class="pad" x="258.0" y="103.3" width="105.0" height="2.7"/><rect class="use" x="258.0" y="103.3" width="105.0" height="2.7"/><line class="blk" x1="279.0" y1="103.3" x2="279.0" y2="106.0"/><line class="blk" x1="300.0" y1="103.3" x2="300.0" y2="106.0"/><line class="blk" x1="321.0" y1="103.3" x2="321.0" y2="106.0"/><line class="blk" x1="342.0" y1="103.3" x2="342.0" y2="106.0"/><rect class="pad" x="258.0" y="106.6" width="126.0" height="2.7"/><rect class="use" x="258.0" y="106.6" width="110.2" height="2.7"/><line class="blk" x1="279.0" y1="106.6" x2="279.0" y2="109.3"/><line class="blk" x1="300.0" y1="106.6" x2="300.0" y2="109.3"/><line class="blk" x1="321.0" y1="106.6" x2="321.0" y2="109.3"/><line class="blk" x1="342.0" y1="106.6" x2="342.0" y2="109.3"/><line class="blk" x1="363.0" y1="106.6" x2="363.0" y2="109.3"/><rect class="pad" x="258.0" y="109.9" width="126.0" height="2.7"/><rect class="use" x="258.0" y="109.9" width="112.9" height="2.7"/><line class="blk" x1="279.0" y1="109.9" x2="279.0" y2="112.6"/><line class="blk" x1="300.0" y1="109.9" x2="300.0" y2="112.6"/><line class="blk" x1="321.0" y1="109.9" x2="321.0" y2="112.6"/><line class="blk" x1="342.0" y1="109.9" x2="342.0" y2="112.6"/><line class="blk" x1="363.0" y1="109.9" x2="363.0" y2="112.6"/><rect class="pad" x="258.0" y="113.2" width="126.0" height="2.7"/><rect class="use" x="258.0" y="113.2" width="120.8" height="2.7"/><line class="blk" x1="279.0" y1="113.2" x2="279.0" y2="115.9"/><line class="blk" x1="300.0" y1="113.2" x2="300.0" y2="115.9"/><line class="blk" x1="321.0" y1="113.2" x2="321.0" y2="115.9"/><line class="blk" x1="342.0" y1="113.2" x2="342.0" y2="115.9"/><line class="blk" x1="363.0" y1="113.2" x2="363.0" y2="115.9"/><rect class="pad" x="258.0" y="116.5" width="126.0" height="2.7"/><rect class="use" x="258.0" y="116.5" width="123.4" height="2.7"/><line class="blk" x1="279.0" y1="116.5" x2="279.0" y2="119.2"/><line class="blk" x1="300.0" y1="116.5" x2="300.0" y2="119.2"/><line class="blk" x1="321.0" y1="116.5" x2="321.0" y2="119.2"/><line class="blk" x1="342.0" y1="116.5" x2="342.0" y2="119.2"/><line class="blk" x1="363.0" y1="116.5" x2="363.0" y2="119.2"/><rect class="pad" x="258.0" y="119.8" width="126.0" height="2.7"/><rect class="use" x="258.0" y="119.8" width="123.4" height="2.7"/><line class="blk" x1="279.0" y1="119.8" x2="279.0" y2="122.5"/><line class="blk" x1="300.0" y1="119.8" x2="300.0" y2="122.5"/><line class="blk" x1="321.0" y1="119.8" x2="321.0" y2="122.5"/><line class="blk" x1="342.0" y1="119.8" x2="342.0" y2="122.5"/><line class="blk" x1="363.0" y1="119.8" x2="363.0" y2="122.5"/><rect class="pad" x="258.0" y="123.1" width="147.0" height="2.7"/><rect class="use" x="258.0" y="123.1" width="128.6" height="2.7"/><line class="blk" x1="279.0" y1="123.1" x2="279.0" y2="125.8"/><line class="blk" x1="300.0" y1="123.1" x2="300.0" y2="125.8"/><line class="blk" x1="321.0" y1="123.1" x2="321.0" y2="125.8"/><line class="blk" x1="342.0" y1="123.1" x2="342.0" y2="125.8"/><line class="blk" x1="363.0" y1="123.1" x2="363.0" y2="125.8"/><line class="blk" x1="384.0" y1="123.1" x2="384.0" y2="125.8"/><rect class="pad" x="258.0" y="126.4" width="168.0" height="2.7"/><rect class="use" x="258.0" y="126.4" width="149.6" height="2.7"/><line class="blk" x1="279.0" y1="126.4" x2="279.0" y2="129.1"/><line class="blk" x1="300.0" y1="126.4" x2="300.0" y2="129.1"/><line class="blk" x1="321.0" y1="126.4" x2="321.0" y2="129.1"/><line class="blk" x1="342.0" y1="126.4" x2="342.0" y2="129.1"/><line class="blk" x1="363.0" y1="126.4" x2="363.0" y2="129.1"/><line class="blk" x1="384.0" y1="126.4" x2="384.0" y2="129.1"/><line class="blk" x1="405.0" y1="126.4" x2="405.0" y2="129.1"/><rect class="pad" x="258.0" y="129.7" width="168.0" height="2.7"/><rect class="use" x="258.0" y="129.7" width="157.5" height="2.7"/><line class="blk" x1="279.0" y1="129.7" x2="279.0" y2="132.4"/><line class="blk" x1="300.0" y1="129.7" x2="300.0" y2="132.4"/><line class="blk" x1="321.0" y1="129.7" x2="321.0" y2="132.4"/><line class="blk" x1="342.0" y1="129.7" x2="342.0" y2="132.4"/><line class="blk" x1="363.0" y1="129.7" x2="363.0" y2="132.4"/><line class="blk" x1="384.0" y1="129.7" x2="384.0" y2="132.4"/><line class="blk" x1="405.0" y1="129.7" x2="405.0" y2="132.4"/><rect class="pad" x="258.0" y="133.0" width="168.0" height="2.7"/><rect class="use" x="258.0" y="133.0" width="160.1" height="2.7"/><line class="blk" x1="279.0" y1="133.0" x2="279.0" y2="135.7"/><line class="blk" x1="300.0" y1="133.0" x2="300.0" y2="135.7"/><line class="blk" x1="321.0" y1="133.0" x2="321.0" y2="135.7"/><line class="blk" x1="342.0" y1="133.0" x2="342.0" y2="135.7"/><line class="blk" x1="363.0" y1="133.0" x2="363.0" y2="135.7"/><line class="blk" x1="384.0" y1="133.0" x2="384.0" y2="135.7"/><line class="blk" x1="405.0" y1="133.0" x2="405.0" y2="135.7"/><rect class="pad" x="258.0" y="136.3" width="168.0" height="2.7"/><rect class="use" x="258.0" y="136.3" width="166.7" height="2.7"/><line class="blk" x1="279.0" y1="136.3" x2="279.0" y2="139.0"/><line class="blk" x1="300.0" y1="136.3" x2="300.0" y2="139.0"/><line class="blk" x1="321.0" y1="136.3" x2="321.0" y2="139.0"/><line class="blk" x1="342.0" y1="136.3" x2="342.0" y2="139.0"/><line class="blk" x1="363.0" y1="136.3" x2="363.0" y2="139.0"/><line class="blk" x1="384.0" y1="136.3" x2="384.0" y2="139.0"/><line class="blk" x1="405.0" y1="136.3" x2="405.0" y2="139.0"/></g>
<text class="lbl" x="130" y="152" text-anchor="middle">4,064 슬롯</text>
<text class="lbl" x="342" y="152" text-anchor="middle">2,560 슬롯</text>
<text class="ttl2 l" x="62.0" y="198">블록 크기에 따른 슬롯 합</text>
<g class="axis">
<line x1="62.0" y1="292.0" x2="440.0" y2="292.0"/>
<text class="tick-lbl" x="56.0" y="295.5" text-anchor="end">0k</text>
<line x1="62.0" y1="262.0" x2="440.0" y2="262.0"/>
<text class="tick-lbl" x="56.0" y="265.5" text-anchor="end">500k</text>
<line x1="62.0" y1="232.0" x2="440.0" y2="232.0"/>
<text class="tick-lbl" x="56.0" y="235.5" text-anchor="end">1000k</text>
</g>
<line class="ref" x1="62.0" y1="231.4" x2="440.0" y2="231.4"/>
<text class="lbl bad" x="66.0" y="226.4">조밀 1,009,601</text>
<line class="ref ok" x1="62.0" y1="258.0" x2="440.0" y2="258.0"/>
<text class="lbl ok" x="440.0" y="269.0" text-anchor="end">실제 토큰 567,139</text>
<polyline class="curve ok" fill="none" points="62.0,258.0 116.0,257.7 170.0,257.1 224.0,256.0 278.0,253.6 332.0,249.1 386.0,240.5 440.0,218.0"/>
<circle class="dot" cx="62.0" cy="258.0" r="2.4"/>
<circle class="dot" cx="116.0" cy="257.7" r="2.4"/>
<circle class="dot" cx="170.0" cy="257.1" r="2.4"/>
<circle class="dot" cx="224.0" cy="256.0" r="2.4"/>
<circle class="dot" cx="278.0" cy="253.6" r="2.4"/>
<circle class="dot" cx="332.0" cy="249.1" r="2.4"/>
<circle class="dot" cx="386.0" cy="240.5" r="2.4"/>
<circle class="dot" cx="440.0" cy="218.0" r="2.4"/>
<g class="lbl-ax">
<text x="62.0" y="307">1</text>
<text x="116.0" y="307">2</text>
<text x="170.0" y="307">4</text>
<text x="224.0" y="307">8</text>
<text x="278.0" y="307">16</text>
<text x="332.0" y="307">32</text>
<text x="386.0" y="307">64</text>
<text x="440.0" y="307">128</text>
<text class="cap l" x="62.0" y="322">블록 크기</text></g>
</svg>
<figcaption>10편 연속 배치 트레이스에서 할당이 제일 큰 스텝. 32개 행이 각자 다른 길이의 캐시를 들고 있는데, 조밀 텐서는 전부 제일 긴 행인 127까지 채워 4,064 슬롯을 잡는다. 블록 16으로 쪼개면 행마다 마지막 블록만 덜 차서 2,560 슬롯이다. 아래는 블록 크기를 바꿔 가며 전체 실행의 슬롯 합을 잰 것 - 블록이 커질수록 늘어 128에서는 조밀보다 나빠진다.</figcaption>
</figure>

그 스텝의 32개 행에 실제로 담긴 토큰은 `2,337` 개다. 조밀 텐서는 제일 긴 행이
`127` 이라 `32 x 127 = 4,064` 슬롯을 잡는다. 블록 16이면 `2,560` 이고, 남는
`223` 칸은 행마다 마지막 블록이 덜 찬 몫이다.

실행 전체로는 이렇다.

```
블록      슬롯 합    점유     최대 동시    풀어야 할 블록 수
   1     567,139  100.0%      2,353            2,353
   2     571,956   99.2%      2,368            1,184
   4     581,580   97.5%      2,400              600
   8     600,824   94.4%      2,448              306
  16     639,184   88.7%      2,560              160
  32     714,240   79.4%      2,848               89
  64     858,944   66.0%      3,456               54
 128   1,232,640   46.0%      4,096               32
조밀   1,009,601   56.2%      4,064               32
```

블록 16에서 최대 동시 슬롯이 `4,064` 에서 `2,560` 으로, `1.59` 배 적다. 슬롯
하나가 블록 3개 x (k,v) x 헤드 4 x 32 x float32 = `3,072` 바이트니까
`12,192 KB` 에서 `7,680 KB` 다. 이 숫자들은 구현과 무관하게 정확하다.

## 블록이 크면 조밀보다 나쁘다

표 맨 아래 두 줄을 나란히 보면 블록 128이 조밀보다 슬롯을 더 쓴다. 조밀은
그 순간 **살아 있는 행 중 제일 긴 것**까지만 채우는데, 블록 128은 길이가
얼마든 무조건 128칸을 잡기 때문이다. 최대 문맥과 같은 블록은 페이징을 끄고
낭비만 남긴 것이다.

반대쪽 끝도 공짜가 아니다. 블록 1이면 점유가 정확히 `100%` 지만 관리해야 할
블록이 `2,353` 개다. 블록 16의 `160` 개와 비교하면 표가 15배 길어진다.

## 시간은 반대로 간다

행 32, 캐시 104에서 걸음 하나를 재면

```
             행당 슬롯    시간(us)   조밀 대비
조밀              104       1010       1.00
블록 4            104       1923       1.90
블록 8            104       1825       1.81
블록 16           112       1850       1.83
블록 32           128       1893       1.87
블록 64           128       1725       1.71
```

블록 크기에 따른 경향이 없다. 사분위가 서로 겹치고, 슬롯을 제일 적게 쓰는
블록 4가 제일 느리다. 블록 크기는 메모리 손잡이지 시간 손잡이가 아니다.

그리고 어느 블록 크기든 조밀보다 `1.7` 에서 `1.9` 배 느리다.

## 값은 모으는 데서 나간다

어텐션을 돌리기 전에 블록 표를 따라가 행마다 자기 블록들을 모아 와야 한다.
그 한 번을 따로 재면

```
같은 모양 (32 x 4 x 112 x 32) 을 만드는 값
  무작위로 흩어진 블록      65.8 us
  행 안에서만 연속          64.1 us
  풀 전체가 순서대로        66.1 us
  같은 크기 조밀 복사       14.5 us
```

블록이 풀 안에서 어떻게 놓여 있든 `4.5` 배다. 처음에는 내 블록 표가 무작위
인덱스라 최악을 재고 있는 줄 알았는데, 이어 붙여 놓아도 같았다. 값은 주소가
흩어져서가 아니라 **새 텐서를 만들기 때문에** 나간다. 실제 시스템이 블록
조회를 어텐션 커널 안으로 넣어 버리는 이유가 그것이고, 그러면 이 복사가
아예 없다. 여기서는 안 넣었다.

## 아낀 메모리를 배치로 바꿔도

메모리를 아낀 값은 배치로 받는다. 조밀 배치 32가 쓰는 `4,064` 슬롯이면 블록
16으로는 배치 `54` 가 들어간다. 그러면 만회되는가.

같은 라운드 안에서 두 설정을 바로 나누고 순서도 번갈아 21회 재면

```
                            중앙값    사분위          21회 중
조밀 32 / 페이지드 32          1.663   1.509 ~ 1.766     21 승
조밀 32 / 페이지드 54          1.551   1.482 ~ 1.655     21 승
조밀 54 / 조밀 32             1.224   1.142 ~ 1.361     21 승
```

같은 배치에서 `1.663` 배 진다. 배치를 54로 올려도 `1.551` 까지밖에 안 돌아온다.
그 사이가 좁은 이유는 모아 오는 값도 행 수에 비례해서 늘기 때문이다.

셋째 줄이 이 편의 핵심이다. 배치를 32에서 54로 올리는 것 자체가 `1.224` 배다.
10편에서 걸음의 `49%` 가 고정분이고 행에 붙는 분이 `21%` 였으니, 행을 1.7배로
늘려도 거기까지다. **`1.66` 배를 내고 `1.22` 배를 사는 거래다.**

## 예산을 조이면

그렇다면 메모리가 진짜 빠듯할 때는 어떤가. 예산을 정하고 그 안에 들어가는
최대 배치를 각 방식에 주면

```
   예산   조밀   블록      스텝(조밀/블록)   조밀/페이지드      사분위
    400      3      3      3216 / 3216         1.308   1.280 ~ 1.332
    600      4      5      2418 / 1948         1.108   1.071 ~ 1.119
    900      7     10      1402 /  991         0.990   0.966 ~ 1.012
  1,200      9     13      1097 /  775         1.113   1.067 ~ 1.138
  1,500     11     17       908 /  602         1.102   1.070 ~ 1.130
  2,560     20     32       518 /  336         1.212   1.183 ~ 1.287
  4,064     32     54       336 /  214         1.457   1.427 ~ 1.543
  6,000     47     75       237 /  164         1.703   1.690 ~ 1.775
```

`1` 보다 크면 조밀이 빠르다는 뜻이다. 예산이 넉넉할수록 조밀이 벌어지고,
조일수록 붙는다. 여덟 줄 중 `900` 한 줄에서만 페이지드가 이긴다 - `0.990`,
사분위 `0.966~1.012` 로 사실상 비긴 것에 가깝다.

`400` 에서 다시 지는 이유는 명확하다. 그 예산에서는 둘 다 배치 3까지밖에 못
넣어서 페이지드가 살 배치가 없다. 모으는 값만 내고 아무것도 안 받는다.

## 남는 것

이 편이 잰 것은 조밀 텐서를 만드는 페이징이다. 블록 조회를 어텐션 안으로
넣으면 `4.5` 배짜리 복사가 사라지고 표가 전부 바뀔 것이다 - 안 넣었으니
모른다. 여기 숫자로 페이징 자체를 판단할 수는 없고, "커널을 안 고치고
할당만 바꾸면" 이라는 조건이 붙는다.

규모도 다르다. 이 모델의 캐시 최대치는 `12 MB` 라 메모리가 한 번도 못 돌게
막은 적이 없다. 캐시가 기가바이트로 가는 쪽에서는 배치를 조금 더 넣는 문제가
아니라 아예 돌아가느냐 마느냐가 되고, 그때는 `1.22` 배와 비교할 것이 아니라
0과 비교하게 된다.

메모리 표는 그런 사정과 무관하다. 슬롯 수는 길이 목록이 정해지면 정확히
재현되고, 조밀 대 블록 16의 `4,064` 대 `2,560` 은 어느 기계에서 돌리든 같다.

## 그래서

- 블록으로 쪼개면 최대 동시 슬롯이 `4,064` 에서 `2,560` 으로 `1.59` 배 준다.
  점유는 `56.2%` 에서 `88.7%`
- 블록이 최대 문맥만큼 크면 조밀보다 나쁘다. `1,232,640` 대 `1,009,601`
- 블록 1은 점유 `100%` 지만 블록을 `2,353` 개 관리해야 한다
- 시간은 블록 크기와 무관하게 조밀보다 `1.7~1.9` 배 느리다
- 값은 흩어짐이 아니라 복사다. 블록을 순서대로 깔아도 조밀 복사의 `4.5` 배
- 아낀 메모리로 배치를 `32` 에서 `54` 로 올려도 그건 `1.224` 배짜리다.
  `1.66` 을 내고 `1.22` 를 산다
- 예산 여덟 개 중 `900` 한 곳에서만 페이지드가 앞선다. 그것도 `0.990`
