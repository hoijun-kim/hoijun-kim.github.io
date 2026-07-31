---
title: "Saved 1.6x the memory, lost 1.7x the time"
description: "Part ten ended with a dense cache tensor sized by its longest row. Cutting it into fixed-size blocks takes the peak allocation from 4,064 slots to 2,560. Then gathering the scattered blocks cost more than the padding it removed."
date: 2025-11-01
lang: en
kind: guide
series:
  id: after-training
  part: 11
---

Part ten stopped at the point where continuous batching makes the cache longer.
Hold the cache as one dense tensor and its length is set by the longest row, and
continuous batching deliberately parks a freshly admitted short row beside a
long-running one. The closing paragraph noted that cutting the cache into
fixed-size blocks would make that price disappear, and left it there.

So I cut it. The memory fell exactly as advertised. The time went the other way.

## What is left after cutting

With block size `S`, a row holding `L` tokens gets `ceil(L/S)` blocks. The blocks
live in a shared pool and each row has a block table saying which ones are its
own. Nothing requires a row's blocks to sit next to each other in the pool.

Taking the step with the largest allocation from part ten's continuous trace:

<figure class="fig">
<svg viewBox="0 0 460 322" role="img" aria-label="Cache allocation on one step. Dense on the left is a rectangle where all 32 rows reach the longest; blocked on the right is ragged, each row stopping at the last block it needs. Below, total slots rise with block size and at 128 exceed dense">
<text class="ttl2" x="130" y="24">Dense - every row padded to the longest</text>
<text class="ttl2" x="342" y="24">Blocks of 16 - only the blocks a row needs</text>
<g class="alloc"><rect class="pad" x="46.0" y="34.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="34.0" width="22.3" height="2.7"/><rect class="pad" x="46.0" y="37.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="37.3" width="22.3" height="2.7"/><rect class="pad" x="46.0" y="40.6" width="166.7" height="2.7"/><rect class="use" x="46.0" y="40.6" width="47.2" height="2.7"/><rect class="pad" x="46.0" y="43.9" width="166.7" height="2.7"/><rect class="use" x="46.0" y="43.9" width="59.1" height="2.7"/><rect class="pad" x="46.0" y="47.2" width="166.7" height="2.7"/><rect class="use" x="46.0" y="47.2" width="61.7" height="2.7"/><rect class="pad" x="46.0" y="50.5" width="166.7" height="2.7"/><rect class="use" x="46.0" y="50.5" width="61.7" height="2.7"/><rect class="pad" x="46.0" y="53.8" width="166.7" height="2.7"/><rect class="use" x="46.0" y="53.8" width="65.6" height="2.7"/><rect class="pad" x="46.0" y="57.1" width="166.7" height="2.7"/><rect class="use" x="46.0" y="57.1" width="70.9" height="2.7"/><rect class="pad" x="46.0" y="60.4" width="166.7" height="2.7"/><rect class="use" x="46.0" y="60.4" width="72.2" height="2.7"/><rect class="pad" x="46.0" y="63.7" width="166.7" height="2.7"/><rect class="use" x="46.0" y="63.7" width="76.1" height="2.7"/><rect class="pad" x="46.0" y="67.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="67.0" width="78.8" height="2.7"/><rect class="pad" x="46.0" y="70.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="70.3" width="90.6" height="2.7"/><rect class="pad" x="46.0" y="73.6" width="166.7" height="2.7"/><rect class="use" x="46.0" y="73.6" width="93.2" height="2.7"/><rect class="pad" x="46.0" y="76.9" width="166.7" height="2.7"/><rect class="use" x="46.0" y="76.9" width="93.2" height="2.7"/><rect class="pad" x="46.0" y="80.2" width="166.7" height="2.7"/><rect class="use" x="46.0" y="80.2" width="93.2" height="2.7"/><rect class="pad" x="46.0" y="83.5" width="166.7" height="2.7"/><rect class="use" x="46.0" y="83.5" width="94.5" height="2.7"/><rect class="pad" x="46.0" y="86.8" width="166.7" height="2.7"/><rect class="use" x="46.0" y="86.8" width="95.8" height="2.7"/><rect class="pad" x="46.0" y="90.1" width="166.7" height="2.7"/><rect class="use" x="46.0" y="90.1" width="101.1" height="2.7"/><rect class="pad" x="46.0" y="93.4" width="166.7" height="2.7"/><rect class="use" x="46.0" y="93.4" width="101.1" height="2.7"/><rect class="pad" x="46.0" y="96.7" width="166.7" height="2.7"/><rect class="use" x="46.0" y="96.7" width="103.7" height="2.7"/><rect class="pad" x="46.0" y="100.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="100.0" width="105.0" height="2.7"/><rect class="pad" x="46.0" y="103.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="103.3" width="105.0" height="2.7"/><rect class="pad" x="46.0" y="106.6" width="166.7" height="2.7"/><rect class="use" x="46.0" y="106.6" width="110.2" height="2.7"/><rect class="pad" x="46.0" y="109.9" width="166.7" height="2.7"/><rect class="use" x="46.0" y="109.9" width="112.9" height="2.7"/><rect class="pad" x="46.0" y="113.2" width="166.7" height="2.7"/><rect class="use" x="46.0" y="113.2" width="120.8" height="2.7"/><rect class="pad" x="46.0" y="116.5" width="166.7" height="2.7"/><rect class="use" x="46.0" y="116.5" width="123.4" height="2.7"/><rect class="pad" x="46.0" y="119.8" width="166.7" height="2.7"/><rect class="use" x="46.0" y="119.8" width="123.4" height="2.7"/><rect class="pad" x="46.0" y="123.1" width="166.7" height="2.7"/><rect class="use" x="46.0" y="123.1" width="128.6" height="2.7"/><rect class="pad" x="46.0" y="126.4" width="166.7" height="2.7"/><rect class="use" x="46.0" y="126.4" width="149.6" height="2.7"/><rect class="pad" x="46.0" y="129.7" width="166.7" height="2.7"/><rect class="use" x="46.0" y="129.7" width="157.5" height="2.7"/><rect class="pad" x="46.0" y="133.0" width="166.7" height="2.7"/><rect class="use" x="46.0" y="133.0" width="160.1" height="2.7"/><rect class="pad" x="46.0" y="136.3" width="166.7" height="2.7"/><rect class="use" x="46.0" y="136.3" width="166.7" height="2.7"/><rect class="pad" x="258.0" y="34.0" width="42.0" height="2.7"/><rect class="use" x="258.0" y="34.0" width="22.3" height="2.7"/><line class="blk" x1="279.0" y1="34.0" x2="279.0" y2="36.7"/><rect class="pad" x="258.0" y="37.3" width="42.0" height="2.7"/><rect class="use" x="258.0" y="37.3" width="22.3" height="2.7"/><line class="blk" x1="279.0" y1="37.3" x2="279.0" y2="40.0"/><rect class="pad" x="258.0" y="40.6" width="63.0" height="2.7"/><rect class="use" x="258.0" y="40.6" width="47.2" height="2.7"/><line class="blk" x1="279.0" y1="40.6" x2="279.0" y2="43.3"/><line class="blk" x1="300.0" y1="40.6" x2="300.0" y2="43.3"/><rect class="pad" x="258.0" y="43.9" width="63.0" height="2.7"/><rect class="use" x="258.0" y="43.9" width="59.1" height="2.7"/><line class="blk" x1="279.0" y1="43.9" x2="279.0" y2="46.6"/><line class="blk" x1="300.0" y1="43.9" x2="300.0" y2="46.6"/><rect class="pad" x="258.0" y="47.2" width="63.0" height="2.7"/><rect class="use" x="258.0" y="47.2" width="61.7" height="2.7"/><line class="blk" x1="279.0" y1="47.2" x2="279.0" y2="49.9"/><line class="blk" x1="300.0" y1="47.2" x2="300.0" y2="49.9"/><rect class="pad" x="258.0" y="50.5" width="63.0" height="2.7"/><rect class="use" x="258.0" y="50.5" width="61.7" height="2.7"/><line class="blk" x1="279.0" y1="50.5" x2="279.0" y2="53.2"/><line class="blk" x1="300.0" y1="50.5" x2="300.0" y2="53.2"/><rect class="pad" x="258.0" y="53.8" width="84.0" height="2.7"/><rect class="use" x="258.0" y="53.8" width="65.6" height="2.7"/><line class="blk" x1="279.0" y1="53.8" x2="279.0" y2="56.5"/><line class="blk" x1="300.0" y1="53.8" x2="300.0" y2="56.5"/><line class="blk" x1="321.0" y1="53.8" x2="321.0" y2="56.5"/><rect class="pad" x="258.0" y="57.1" width="84.0" height="2.7"/><rect class="use" x="258.0" y="57.1" width="70.9" height="2.7"/><line class="blk" x1="279.0" y1="57.1" x2="279.0" y2="59.8"/><line class="blk" x1="300.0" y1="57.1" x2="300.0" y2="59.8"/><line class="blk" x1="321.0" y1="57.1" x2="321.0" y2="59.8"/><rect class="pad" x="258.0" y="60.4" width="84.0" height="2.7"/><rect class="use" x="258.0" y="60.4" width="72.2" height="2.7"/><line class="blk" x1="279.0" y1="60.4" x2="279.0" y2="63.1"/><line class="blk" x1="300.0" y1="60.4" x2="300.0" y2="63.1"/><line class="blk" x1="321.0" y1="60.4" x2="321.0" y2="63.1"/><rect class="pad" x="258.0" y="63.7" width="84.0" height="2.7"/><rect class="use" x="258.0" y="63.7" width="76.1" height="2.7"/><line class="blk" x1="279.0" y1="63.7" x2="279.0" y2="66.4"/><line class="blk" x1="300.0" y1="63.7" x2="300.0" y2="66.4"/><line class="blk" x1="321.0" y1="63.7" x2="321.0" y2="66.4"/><rect class="pad" x="258.0" y="67.0" width="84.0" height="2.7"/><rect class="use" x="258.0" y="67.0" width="78.8" height="2.7"/><line class="blk" x1="279.0" y1="67.0" x2="279.0" y2="69.7"/><line class="blk" x1="300.0" y1="67.0" x2="300.0" y2="69.7"/><line class="blk" x1="321.0" y1="67.0" x2="321.0" y2="69.7"/><rect class="pad" x="258.0" y="70.3" width="105.0" height="2.7"/><rect class="use" x="258.0" y="70.3" width="90.6" height="2.7"/><line class="blk" x1="279.0" y1="70.3" x2="279.0" y2="73.0"/><line class="blk" x1="300.0" y1="70.3" x2="300.0" y2="73.0"/><line class="blk" x1="321.0" y1="70.3" x2="321.0" y2="73.0"/><line class="blk" x1="342.0" y1="70.3" x2="342.0" y2="73.0"/><rect class="pad" x="258.0" y="73.6" width="105.0" height="2.7"/><rect class="use" x="258.0" y="73.6" width="93.2" height="2.7"/><line class="blk" x1="279.0" y1="73.6" x2="279.0" y2="76.3"/><line class="blk" x1="300.0" y1="73.6" x2="300.0" y2="76.3"/><line class="blk" x1="321.0" y1="73.6" x2="321.0" y2="76.3"/><line class="blk" x1="342.0" y1="73.6" x2="342.0" y2="76.3"/><rect class="pad" x="258.0" y="76.9" width="105.0" height="2.7"/><rect class="use" x="258.0" y="76.9" width="93.2" height="2.7"/><line class="blk" x1="279.0" y1="76.9" x2="279.0" y2="79.6"/><line class="blk" x1="300.0" y1="76.9" x2="300.0" y2="79.6"/><line class="blk" x1="321.0" y1="76.9" x2="321.0" y2="79.6"/><line class="blk" x1="342.0" y1="76.9" x2="342.0" y2="79.6"/><rect class="pad" x="258.0" y="80.2" width="105.0" height="2.7"/><rect class="use" x="258.0" y="80.2" width="93.2" height="2.7"/><line class="blk" x1="279.0" y1="80.2" x2="279.0" y2="82.9"/><line class="blk" x1="300.0" y1="80.2" x2="300.0" y2="82.9"/><line class="blk" x1="321.0" y1="80.2" x2="321.0" y2="82.9"/><line class="blk" x1="342.0" y1="80.2" x2="342.0" y2="82.9"/><rect class="pad" x="258.0" y="83.5" width="105.0" height="2.7"/><rect class="use" x="258.0" y="83.5" width="94.5" height="2.7"/><line class="blk" x1="279.0" y1="83.5" x2="279.0" y2="86.2"/><line class="blk" x1="300.0" y1="83.5" x2="300.0" y2="86.2"/><line class="blk" x1="321.0" y1="83.5" x2="321.0" y2="86.2"/><line class="blk" x1="342.0" y1="83.5" x2="342.0" y2="86.2"/><rect class="pad" x="258.0" y="86.8" width="105.0" height="2.7"/><rect class="use" x="258.0" y="86.8" width="95.8" height="2.7"/><line class="blk" x1="279.0" y1="86.8" x2="279.0" y2="89.5"/><line class="blk" x1="300.0" y1="86.8" x2="300.0" y2="89.5"/><line class="blk" x1="321.0" y1="86.8" x2="321.0" y2="89.5"/><line class="blk" x1="342.0" y1="86.8" x2="342.0" y2="89.5"/><rect class="pad" x="258.0" y="90.1" width="105.0" height="2.7"/><rect class="use" x="258.0" y="90.1" width="101.1" height="2.7"/><line class="blk" x1="279.0" y1="90.1" x2="279.0" y2="92.8"/><line class="blk" x1="300.0" y1="90.1" x2="300.0" y2="92.8"/><line class="blk" x1="321.0" y1="90.1" x2="321.0" y2="92.8"/><line class="blk" x1="342.0" y1="90.1" x2="342.0" y2="92.8"/><rect class="pad" x="258.0" y="93.4" width="105.0" height="2.7"/><rect class="use" x="258.0" y="93.4" width="101.1" height="2.7"/><line class="blk" x1="279.0" y1="93.4" x2="279.0" y2="96.1"/><line class="blk" x1="300.0" y1="93.4" x2="300.0" y2="96.1"/><line class="blk" x1="321.0" y1="93.4" x2="321.0" y2="96.1"/><line class="blk" x1="342.0" y1="93.4" x2="342.0" y2="96.1"/><rect class="pad" x="258.0" y="96.7" width="105.0" height="2.7"/><rect class="use" x="258.0" y="96.7" width="103.7" height="2.7"/><line class="blk" x1="279.0" y1="96.7" x2="279.0" y2="99.4"/><line class="blk" x1="300.0" y1="96.7" x2="300.0" y2="99.4"/><line class="blk" x1="321.0" y1="96.7" x2="321.0" y2="99.4"/><line class="blk" x1="342.0" y1="96.7" x2="342.0" y2="99.4"/><rect class="pad" x="258.0" y="100.0" width="105.0" height="2.7"/><rect class="use" x="258.0" y="100.0" width="105.0" height="2.7"/><line class="blk" x1="279.0" y1="100.0" x2="279.0" y2="102.7"/><line class="blk" x1="300.0" y1="100.0" x2="300.0" y2="102.7"/><line class="blk" x1="321.0" y1="100.0" x2="321.0" y2="102.7"/><line class="blk" x1="342.0" y1="100.0" x2="342.0" y2="102.7"/><rect class="pad" x="258.0" y="103.3" width="105.0" height="2.7"/><rect class="use" x="258.0" y="103.3" width="105.0" height="2.7"/><line class="blk" x1="279.0" y1="103.3" x2="279.0" y2="106.0"/><line class="blk" x1="300.0" y1="103.3" x2="300.0" y2="106.0"/><line class="blk" x1="321.0" y1="103.3" x2="321.0" y2="106.0"/><line class="blk" x1="342.0" y1="103.3" x2="342.0" y2="106.0"/><rect class="pad" x="258.0" y="106.6" width="126.0" height="2.7"/><rect class="use" x="258.0" y="106.6" width="110.2" height="2.7"/><line class="blk" x1="279.0" y1="106.6" x2="279.0" y2="109.3"/><line class="blk" x1="300.0" y1="106.6" x2="300.0" y2="109.3"/><line class="blk" x1="321.0" y1="106.6" x2="321.0" y2="109.3"/><line class="blk" x1="342.0" y1="106.6" x2="342.0" y2="109.3"/><line class="blk" x1="363.0" y1="106.6" x2="363.0" y2="109.3"/><rect class="pad" x="258.0" y="109.9" width="126.0" height="2.7"/><rect class="use" x="258.0" y="109.9" width="112.9" height="2.7"/><line class="blk" x1="279.0" y1="109.9" x2="279.0" y2="112.6"/><line class="blk" x1="300.0" y1="109.9" x2="300.0" y2="112.6"/><line class="blk" x1="321.0" y1="109.9" x2="321.0" y2="112.6"/><line class="blk" x1="342.0" y1="109.9" x2="342.0" y2="112.6"/><line class="blk" x1="363.0" y1="109.9" x2="363.0" y2="112.6"/><rect class="pad" x="258.0" y="113.2" width="126.0" height="2.7"/><rect class="use" x="258.0" y="113.2" width="120.8" height="2.7"/><line class="blk" x1="279.0" y1="113.2" x2="279.0" y2="115.9"/><line class="blk" x1="300.0" y1="113.2" x2="300.0" y2="115.9"/><line class="blk" x1="321.0" y1="113.2" x2="321.0" y2="115.9"/><line class="blk" x1="342.0" y1="113.2" x2="342.0" y2="115.9"/><line class="blk" x1="363.0" y1="113.2" x2="363.0" y2="115.9"/><rect class="pad" x="258.0" y="116.5" width="126.0" height="2.7"/><rect class="use" x="258.0" y="116.5" width="123.4" height="2.7"/><line class="blk" x1="279.0" y1="116.5" x2="279.0" y2="119.2"/><line class="blk" x1="300.0" y1="116.5" x2="300.0" y2="119.2"/><line class="blk" x1="321.0" y1="116.5" x2="321.0" y2="119.2"/><line class="blk" x1="342.0" y1="116.5" x2="342.0" y2="119.2"/><line class="blk" x1="363.0" y1="116.5" x2="363.0" y2="119.2"/><rect class="pad" x="258.0" y="119.8" width="126.0" height="2.7"/><rect class="use" x="258.0" y="119.8" width="123.4" height="2.7"/><line class="blk" x1="279.0" y1="119.8" x2="279.0" y2="122.5"/><line class="blk" x1="300.0" y1="119.8" x2="300.0" y2="122.5"/><line class="blk" x1="321.0" y1="119.8" x2="321.0" y2="122.5"/><line class="blk" x1="342.0" y1="119.8" x2="342.0" y2="122.5"/><line class="blk" x1="363.0" y1="119.8" x2="363.0" y2="122.5"/><rect class="pad" x="258.0" y="123.1" width="147.0" height="2.7"/><rect class="use" x="258.0" y="123.1" width="128.6" height="2.7"/><line class="blk" x1="279.0" y1="123.1" x2="279.0" y2="125.8"/><line class="blk" x1="300.0" y1="123.1" x2="300.0" y2="125.8"/><line class="blk" x1="321.0" y1="123.1" x2="321.0" y2="125.8"/><line class="blk" x1="342.0" y1="123.1" x2="342.0" y2="125.8"/><line class="blk" x1="363.0" y1="123.1" x2="363.0" y2="125.8"/><line class="blk" x1="384.0" y1="123.1" x2="384.0" y2="125.8"/><rect class="pad" x="258.0" y="126.4" width="168.0" height="2.7"/><rect class="use" x="258.0" y="126.4" width="149.6" height="2.7"/><line class="blk" x1="279.0" y1="126.4" x2="279.0" y2="129.1"/><line class="blk" x1="300.0" y1="126.4" x2="300.0" y2="129.1"/><line class="blk" x1="321.0" y1="126.4" x2="321.0" y2="129.1"/><line class="blk" x1="342.0" y1="126.4" x2="342.0" y2="129.1"/><line class="blk" x1="363.0" y1="126.4" x2="363.0" y2="129.1"/><line class="blk" x1="384.0" y1="126.4" x2="384.0" y2="129.1"/><line class="blk" x1="405.0" y1="126.4" x2="405.0" y2="129.1"/><rect class="pad" x="258.0" y="129.7" width="168.0" height="2.7"/><rect class="use" x="258.0" y="129.7" width="157.5" height="2.7"/><line class="blk" x1="279.0" y1="129.7" x2="279.0" y2="132.4"/><line class="blk" x1="300.0" y1="129.7" x2="300.0" y2="132.4"/><line class="blk" x1="321.0" y1="129.7" x2="321.0" y2="132.4"/><line class="blk" x1="342.0" y1="129.7" x2="342.0" y2="132.4"/><line class="blk" x1="363.0" y1="129.7" x2="363.0" y2="132.4"/><line class="blk" x1="384.0" y1="129.7" x2="384.0" y2="132.4"/><line class="blk" x1="405.0" y1="129.7" x2="405.0" y2="132.4"/><rect class="pad" x="258.0" y="133.0" width="168.0" height="2.7"/><rect class="use" x="258.0" y="133.0" width="160.1" height="2.7"/><line class="blk" x1="279.0" y1="133.0" x2="279.0" y2="135.7"/><line class="blk" x1="300.0" y1="133.0" x2="300.0" y2="135.7"/><line class="blk" x1="321.0" y1="133.0" x2="321.0" y2="135.7"/><line class="blk" x1="342.0" y1="133.0" x2="342.0" y2="135.7"/><line class="blk" x1="363.0" y1="133.0" x2="363.0" y2="135.7"/><line class="blk" x1="384.0" y1="133.0" x2="384.0" y2="135.7"/><line class="blk" x1="405.0" y1="133.0" x2="405.0" y2="135.7"/><rect class="pad" x="258.0" y="136.3" width="168.0" height="2.7"/><rect class="use" x="258.0" y="136.3" width="166.7" height="2.7"/><line class="blk" x1="279.0" y1="136.3" x2="279.0" y2="139.0"/><line class="blk" x1="300.0" y1="136.3" x2="300.0" y2="139.0"/><line class="blk" x1="321.0" y1="136.3" x2="321.0" y2="139.0"/><line class="blk" x1="342.0" y1="136.3" x2="342.0" y2="139.0"/><line class="blk" x1="363.0" y1="136.3" x2="363.0" y2="139.0"/><line class="blk" x1="384.0" y1="136.3" x2="384.0" y2="139.0"/><line class="blk" x1="405.0" y1="136.3" x2="405.0" y2="139.0"/></g>
<text class="lbl" x="130" y="152" text-anchor="middle">4,064 slots</text>
<text class="lbl" x="342" y="152" text-anchor="middle">2,560 slots</text>
<text class="ttl2 l" x="62.0" y="198">Total slots by block size</text>
<g class="axis">
<line x1="62.0" y1="292.0" x2="440.0" y2="292.0"/>
<text class="tick-lbl" x="56.0" y="295.5" text-anchor="end">0k</text>
<line x1="62.0" y1="262.0" x2="440.0" y2="262.0"/>
<text class="tick-lbl" x="56.0" y="265.5" text-anchor="end">500k</text>
<line x1="62.0" y1="232.0" x2="440.0" y2="232.0"/>
<text class="tick-lbl" x="56.0" y="235.5" text-anchor="end">1000k</text>
</g>
<line class="ref" x1="62.0" y1="231.4" x2="440.0" y2="231.4"/>
<text class="lbl bad" x="66.0" y="226.4">dense 1,009,601</text>
<line class="ref ok" x1="62.0" y1="258.0" x2="440.0" y2="258.0"/>
<text class="lbl ok" x="440.0" y="269.0" text-anchor="end">actual tokens 567,139</text>
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
<text class="cap l" x="62.0" y="322">block size</text></g>
</svg>
<figcaption>The step with the largest allocation in part ten's continuous trace. Its 32 rows hold caches of different lengths, and the dense tensor takes all of them to the longest, 127, for 4,064 slots. Cut into blocks of 16, only each row's last block is short-filled, for 2,560. Below, total slots over the whole run against block size - it rises with the block, and at 128 it is worse than dense.</figcaption>
</figure>

Those 32 rows actually hold `2,337` tokens. The dense tensor takes all of them to
the longest row at `127`, so `32 x 127 = 4,064` slots. Blocks of 16 come to
`2,560`, the extra `223` being each row's short-filled last block.

Over the whole run:

```
block      slots     occ     peak live    blocks to track
    1    567,139  100.0%         2,353              2,353
    2    571,956   99.2%         2,368              1,184
    4    581,580   97.5%         2,400                600
    8    600,824   94.4%         2,448                306
   16    639,184   88.7%         2,560                160
   32    714,240   79.4%         2,848                 89
   64    858,944   66.0%         3,456                 54
  128  1,232,640   46.0%         4,096                 32
dense  1,009,601   56.2%         4,064                 32
```

At block 16 the peak live allocation goes from `4,064` to `2,560`, a factor of
`1.59`. A slot is 3 blocks x (k,v) x 4 heads x 32 x float32 = `3,072` bytes, so
`12,192 KB` becomes `7,680 KB`. These figures are exact and independent of any
implementation.

## A block as large as the context is worse than dense

Set the last two rows of the table side by side and block 128 uses more slots
than dense. Dense fills only to **the longest row currently alive**, while block
128 claims 128 slots whatever the length. A block the size of the maximum context
turns paging off and keeps the waste.

The other end is not free either. Block 1 gives exactly `100%` occupancy but
leaves `2,353` blocks to manage, against 160 at block 16 - a table fifteen times
longer.

## The time goes the other way

Timing one step at 32 rows and cache 104:

```
              slots/row    time (us)   vs dense
dense               104         1010       1.00
block 4             104         1923       1.90
block 8             104         1825       1.81
block 16            112         1850       1.83
block 32            128         1893       1.87
block 64            128         1725       1.71
```

There is no trend in block size. The quartiles overlap each other, and block 4,
which uses the fewest slots, is the slowest of them. Block size is a memory dial,
not a time dial.

And every block size is `1.7` to `1.9` times slower than dense.

## The price is in the gathering

Before attention runs, each row's blocks have to be collected by following the
block table. Timing that alone:

```
building the same shape (32 x 4 x 112 x 32)
  blocks scattered at random       65.8 us
  contiguous within each row       64.1 us
  whole pool in order              66.1 us
  dense copy of the same size      14.5 us
```

`4.5` times, however the blocks are laid out in the pool. I had assumed my random
block table was measuring a worst case; laying the blocks out in order changes
nothing. The price is not scattered addresses, it is **materialising a new
tensor**. That is why real systems fold the block lookup into the attention
kernel, where the copy does not exist at all. This one does not.

## Even after converting the memory into batch

Saved memory gets paid back as batch size. The `4,064` slots dense uses at batch
32 will hold batch `54` with blocks of 16. Does that make it back?

Dividing two configurations against each other in the same round, alternating
which runs first, 21 rounds:

```
                                 median   quartiles         won
dense 32 / paged 32               1.663   1.509 ~ 1.766   21/21
dense 32 / paged 54               1.551   1.482 ~ 1.655   21/21
dense 54 / dense 32               1.224   1.142 ~ 1.361   21/21
```

At the same batch it loses by `1.663`. Raising the batch to 54 recovers it only to
`1.551`, and the gap is narrow because the gathering cost grows with rows too.

The third row is the point of this part. Going from batch 32 to 54 is worth
`1.224` by itself. Part ten put `49%` of a step in fixed cost and `21%` on rows,
so 1.7 times the rows buys about that much and no more. **It is a trade of
`1.66` paid for `1.22` bought.**

## Squeezing the budget

What about when memory really is tight? Fixing a budget and giving each method
the largest batch that fits inside it:

```
 budget  dense  block    steps (dense/block)   dense/paged      quartiles
    400      3      3          3216 / 3216           1.308   1.280 ~ 1.332
    600      4      5          2418 / 1948           1.108   1.071 ~ 1.119
    900      7     10          1402 /  991           0.990   0.966 ~ 1.012
  1,200      9     13          1097 /  775           1.113   1.067 ~ 1.138
  1,500     11     17           908 /  602           1.102   1.070 ~ 1.130
  2,560     20     32           518 /  336           1.212   1.183 ~ 1.287
  4,064     32     54           336 /  214           1.457   1.427 ~ 1.543
  6,000     47     75           237 /  164           1.703   1.690 ~ 1.775
```

Above `1` means dense is faster. The looser the budget the further dense pulls
ahead; the tighter it gets the closer they come. In one row of eight, at `900`,
paging is ahead - `0.990`, quartiles `0.966~1.012`, which is closer to a tie than
a win.

Why it loses again at `400` is plain: that budget holds batch 3 either way, so
there is no batch for paging to buy. It pays the gathering and receives nothing.

## What is left

What this part measured is paging that builds a dense tensor. Fold the block
lookup into attention and the `4.5x` copy disappears and every table here changes
- I did not fold it, so I do not know by how much. These numbers cannot judge
paging itself; they carry the condition "if the allocator changes and the kernel
does not".

The scale is different too. This model's cache peaks at `12 MB`, so memory has
never once stopped it from running. Where caches run to gigabytes the question is
not whether a little more batch fits but whether anything runs at all, and then
the comparison is not against `1.22` but against zero.

The memory table does not depend on any of that. Slot counts reproduce exactly
once the list of lengths is fixed, and `4,064` against `2,560` is the same on any
machine.

## So

- Cutting into blocks takes peak live slots from `4,064` to `2,560`, a factor of
  `1.59`. Occupancy `56.2%` to `88.7%`
- A block as large as the maximum context is worse than dense: `1,232,640`
  against `1,009,601`
- Block 1 is `100%` occupied and leaves `2,353` blocks to manage
- Time is `1.7` to `1.9` times worse than dense at every block size
- The price is the copy, not the scatter: blocks laid out in order still cost
  `4.5` times a dense copy
- Converting the saved memory into batch `32` to `54` is worth `1.224`. A trade of
  `1.66` paid for `1.22` bought
- Paging leads in one budget of eight, at `900`, and only by `0.990`
