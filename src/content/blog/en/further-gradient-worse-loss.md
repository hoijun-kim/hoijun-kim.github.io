---
title: "Sending the gradient further made the loss worse"
description: "How far back the loss at the last position reaches, measured for five architectures. Gates barely extend it - PyTorch starts the forget gate at bias 0, so half the signal dies every step. Open it and the gradient reaches the whole context, and the loss gets monotonically worse."
date: 2025-12-31
lang: en
kind: guide
series:
  id: not-attention
  part: 8
---

Part four of the first series watched gradients disappear through twenty stacked
layers. In a recurrent network, **time** takes the place of depth. An RNN reading
128 characters is a 128-layer network passing through the same weights 128 times,
so what part four measured against depth gets measured here against length.

## How far back does it reach

Send the loss from one position - the last - backward, and measure the size of
the gradient arriving at each position's input embedding. Set the last position
to 1 and what survives at each distance reads straight off.

<figure class="fig">
<svg viewBox="0 0 460 336" role="img" aria-label="Gradient the loss at the last position sends back. Above, five architectures: the CNN hits exactly zero at 17, the three recurrent models decay at almost the same rate, and only the transformer flattens far away. Below, the LSTM forget-gate bias from 0 to 3, taking the reach from underflow to the whole context">
<text class="ttl2 l" x="36.0" y="22">after training, five architectures</text>
<g class="axis">
<line x1="66.0" y1="38.7" x2="442.0" y2="38.7"/>
<text class="tick-lbl" x="60.0" y="42.2" text-anchor="end">1</text>
<line x1="66.0" y1="69.9" x2="442.0" y2="69.9"/>
<text class="tick-lbl" x="60.0" y="73.4" text-anchor="end">1e-2</text>
<line x1="66.0" y1="101.2" x2="442.0" y2="101.2"/>
<text class="tick-lbl" x="60.0" y="104.7" text-anchor="end">1e-4</text>
<line x1="66.0" y1="132.4" x2="442.0" y2="132.4"/>
<text class="tick-lbl" x="60.0" y="135.9" text-anchor="end">1e-6</text>
</g>
<path class="curve ok" d="M66.0,38.7 L69.0,38.3 L71.9,39.1 L74.9,40.8 L77.8,43.7 L80.8,45.1 L83.8,47.6 L86.7,47.1 L89.7,48.9 L92.6,50.6 L95.6,52.1 L98.6,53.5 L101.5,54.2 L104.5,56.0 L107.4,58.1 L110.4,59.1 L113.4,59.7 L116.3,57.0 L119.3,62.3 L122.3,62.3 L125.2,63.9 L128.2,62.4 L131.1,62.2 L134.1,64.2 L137.1,66.8 L140.0,62.1 L143.0,66.6 L145.9,66.6 L148.9,64.8 L151.9,63.4 L154.8,68.4 L157.8,66.5 L160.7,64.8 L163.7,62.9 L166.7,62.9 L169.6,65.5 L172.6,67.8 L175.5,64.0 L178.5,65.0 L181.5,66.2 L184.4,65.4 L187.4,66.9 L190.3,65.8 L193.3,64.9 L196.3,64.5 L199.2,65.2 L202.2,64.8 L205.1,65.1 L208.1,66.1 L211.1,67.7 L214.0,67.0 L217.0,65.3 L220.0,68.0 L222.9,66.9 L225.9,65.1 L228.8,68.6 L231.8,69.5 L234.8,67.7 L237.7,68.6 L240.7,68.6 L243.6,67.6 L246.6,67.7 L249.6,68.0 L252.5,69.3 L255.5,68.0 L258.4,68.9 L261.4,68.8 L264.4,68.0 L267.3,68.1 L270.3,68.2 L273.2,67.9 L276.2,68.4 L279.2,68.7 L282.1,68.4 L285.1,67.6 L288.0,68.7 L291.0,67.2 L294.0,69.1 L296.9,69.6 L299.9,69.1 L302.9,69.4 L305.8,66.8 L308.8,70.0 L311.7,69.1 L314.7,69.2 L317.7,70.6 L320.6,69.1 L323.6,70.4 L326.5,68.6 L329.5,68.5 L332.5,69.5 L335.4,68.5 L338.4,69.5 L341.3,68.6 L344.3,70.0 L347.3,69.5 L350.2,68.7 L353.2,68.4 L356.1,69.4 L359.1,69.1 L362.1,68.3 L365.0,69.3 L368.0,68.2 L370.9,69.4 L373.9,69.1 L376.9,68.7 L379.8,67.6 L382.8,68.2 L385.7,67.6 L388.7,68.1 L391.7,67.4 L394.6,67.7 L397.6,69.2 L400.6,68.5 L403.5,68.4 L406.5,68.0 L409.4,68.6 L412.4,69.0 L415.4,67.7 L418.3,67.6 L421.3,68.5 L424.2,67.9 L427.2,68.2 L430.2,67.8 L433.1,68.5 L436.1,67.6 L439.0,69.1 L442.0,68.7" fill="none"/>
<path class="curve bad2" d="M66.0,38.7 L69.0,41.1 L71.9,41.8 L74.9,42.2 L77.8,42.1 L80.8,44.6 L83.8,45.7 L86.7,46.9 L89.7,48.5 L92.6,51.6 L95.6,53.4 L98.6,55.7 L101.5,58.7 L104.5,63.4 L107.4,66.0 L110.4,69.4 L113.4,74.1" fill="none"/>
<path class="curve bad" d="M66.0,38.7 L69.0,40.2 L71.9,41.5 L74.9,43.1 L77.8,44.9 L80.8,46.5 L83.8,47.9 L86.7,49.5 L89.7,51.1 L92.6,52.6 L95.6,54.0 L98.6,55.3 L101.5,56.6 L104.5,57.9 L107.4,59.0 L110.4,60.3 L113.4,61.4 L116.3,62.5 L119.3,63.4 L122.3,64.5 L125.2,65.3 L128.2,66.2 L131.1,67.1 L134.1,67.9 L137.1,68.8 L140.0,69.5 L143.0,70.3 L145.9,71.0 L148.9,71.8 L151.9,72.4 L154.8,73.3 L157.8,73.9 L160.7,74.8 L163.7,75.5 L166.7,76.3 L169.6,77.0 L172.6,77.8 L175.5,78.6 L178.5,79.3 L181.5,80.0 L184.4,80.6 L187.4,81.2 L190.3,81.9 L193.3,82.6 L196.3,83.1 L199.2,83.7 L202.2,84.4 L205.1,85.1 L208.1,85.7 L211.1,86.5 L214.0,87.1 L217.0,87.8 L220.0,88.6 L222.9,89.1 L225.9,89.9 L228.8,90.4 L231.8,91.2 L234.8,91.8 L237.7,92.6 L240.7,93.3 L243.6,93.9 L246.6,94.4 L249.6,95.0 L252.5,95.5 L255.5,96.2 L258.4,96.8 L261.4,97.4 L264.4,98.0 L267.3,98.7 L270.3,99.3 L273.2,99.9 L276.2,100.6 L279.2,101.1 L282.1,101.7 L285.1,102.4 L288.0,103.2 L291.0,103.6 L294.0,104.2 L296.9,104.9 L299.9,105.5 L302.9,106.1 L305.8,106.6 L308.8,107.3 L311.7,108.0 L314.7,108.7 L317.7,109.2 L320.6,109.8 L323.6,110.3 L326.5,110.9 L329.5,111.6 L332.5,112.2 L335.4,112.9 L338.4,113.5 L341.3,114.2 L344.3,114.9 L347.3,115.4 L350.2,116.0 L353.2,116.6 L356.1,117.3 L359.1,117.9 L362.1,118.5 L365.0,119.2 L368.0,119.8 L370.9,120.6 L373.9,121.1 L376.9,121.8 L379.8,122.4 L382.8,123.1 L385.7,123.7 L388.7,124.3 L391.7,125.0 L394.6,125.6 L397.6,126.2 L400.6,126.8 L403.5,127.4 L406.5,128.1 L409.4,128.6 L412.4,129.3 L415.4,130.0 L418.3,130.5 L421.3,131.1 L424.2,131.7 L427.2,132.2 L430.2,132.7 L433.1,133.2 L436.1,133.7 L439.0,134.2 L442.0,133.7" fill="none"/>
<path class="curve ok3" d="M66.0,38.7 L69.0,40.9 L71.9,42.6 L74.9,44.3 L77.8,45.9 L80.8,47.3 L83.8,48.6 L86.7,49.9 L89.7,51.2 L92.6,52.4 L95.6,53.6 L98.6,54.8 L101.5,56.0 L104.5,57.1 L107.4,58.1 L110.4,59.0 L113.4,60.1 L116.3,61.2 L119.3,62.0 L122.3,62.9 L125.2,63.8 L128.2,64.7 L131.1,65.5 L134.1,66.3 L137.1,67.2 L140.0,68.2 L143.0,68.9 L145.9,69.6 L148.9,70.4 L151.9,71.3 L154.8,71.9 L157.8,72.8 L160.7,73.5 L163.7,74.1 L166.7,74.8 L169.6,75.4 L172.6,76.0 L175.5,76.8 L178.5,77.5 L181.5,78.3 L184.4,79.1 L187.4,79.7 L190.3,80.4 L193.3,81.1 L196.3,81.7 L199.2,82.3 L202.2,82.9 L205.1,83.7 L208.1,84.4 L211.1,85.1 L214.0,85.7 L217.0,86.4 L220.0,87.1 L222.9,87.6 L225.9,88.2 L228.8,88.9 L231.8,89.6 L234.8,90.1 L237.7,90.9 L240.7,91.7 L243.6,92.4 L246.6,92.9 L249.6,93.8 L252.5,94.8 L255.5,95.6 L258.4,96.1 L261.4,96.8 L264.4,97.6 L267.3,98.2 L270.3,98.7 L273.2,99.3 L276.2,100.0 L279.2,100.6 L282.1,101.3 L285.1,102.0 L288.0,102.8 L291.0,103.6 L294.0,104.4 L296.9,104.9 L299.9,105.6 L302.9,106.3 L305.8,106.9 L308.8,107.3 L311.7,108.2 L314.7,109.1 L317.7,109.7 L320.6,110.6 L323.6,111.3 L326.5,112.0 L329.5,112.6 L332.5,113.3 L335.4,114.1 L338.4,114.8 L341.3,115.4 L344.3,116.2 L347.3,116.7 L350.2,117.3 L353.2,117.9 L356.1,118.6 L359.1,119.0 L362.1,119.4 L365.0,120.0 L368.0,120.5 L370.9,121.1 L373.9,121.6 L376.9,122.3 L379.8,122.7 L382.8,123.2 L385.7,123.9 L388.7,124.3 L391.7,125.1 L394.6,125.6 L397.6,126.2 L400.6,126.7 L403.5,127.4 L406.5,128.3 L409.4,128.7 L412.4,129.5 L415.4,130.1 L418.3,131.1 L421.3,132.0 L424.2,132.7 L427.2,133.1 L430.2,133.9 L433.1,134.3 L436.1,135.3 L439.0,136.2 L442.0,137.4" fill="none"/>
<path class="curve ok2" d="M66.0,38.7 L69.0,40.8 L71.9,42.9 L74.9,44.9 L77.8,46.8 L80.8,48.5 L83.8,50.1 L86.7,51.5 L89.7,53.2 L92.6,54.5 L95.6,55.6 L98.6,57.0 L101.5,58.2 L104.5,59.3 L107.4,60.2 L110.4,61.3 L113.4,62.2 L116.3,63.3 L119.3,64.2 L122.3,65.1 L125.2,65.7 L128.2,66.6 L131.1,67.4 L134.1,68.2 L137.1,69.2 L140.0,70.1 L143.0,70.8 L145.9,71.1 L148.9,72.3 L151.9,73.1 L154.8,74.0 L157.8,75.1 L160.7,75.7 L163.7,76.7 L166.7,77.7 L169.6,78.2 L172.6,79.0 L175.5,79.9 L178.5,80.6 L181.5,81.2 L184.4,82.1 L187.4,83.1 L190.3,83.8 L193.3,84.5 L196.3,85.5 L199.2,86.2 L202.2,87.1 L205.1,87.8 L208.1,88.4 L211.1,89.1 L214.0,89.9 L217.0,90.5 L220.0,91.2 L222.9,90.4 L225.9,90.9 L228.8,92.2 L231.8,93.3 L234.8,94.8 L237.7,95.6 L240.7,96.5 L243.6,96.7 L246.6,97.0 L249.6,97.2 L252.5,97.7 L255.5,98.8 L258.4,100.0 L261.4,100.8 L264.4,101.7 L267.3,102.4 L270.3,102.5 L273.2,103.2 L276.2,104.3 L279.2,105.0 L282.1,105.1 L285.1,105.6 L288.0,106.3 L291.0,107.3 L294.0,108.6 L296.9,108.8 L299.9,110.1 L302.9,111.0 L305.8,112.2 L308.8,112.7 L311.7,113.2 L314.7,113.4 L317.7,114.0 L320.6,114.5 L323.6,114.9 L326.5,115.6 L329.5,115.6 L332.5,116.9 L335.4,117.6 L338.4,119.0 L341.3,119.2 L344.3,120.1 L347.3,120.6 L350.2,121.5 L353.2,121.7 L356.1,122.1 L359.1,122.4 L362.1,122.8 L365.0,123.9 L368.0,124.6 L370.9,125.7 L373.9,125.9 L376.9,126.9 L379.8,127.0 L382.8,128.1 L385.7,128.1 L388.7,128.2 L391.7,129.5 L394.6,130.2 L397.6,130.3 L400.6,131.4 L403.5,132.1 L406.5,132.5 L409.4,133.0 L412.4,133.9 L415.4,134.5 L418.3,136.1 L421.3,136.0 L424.2,135.9 L427.2,136.8 L430.2,137.6 L433.1,137.4 L436.1,138.8 L439.0,139.6 L442.0,140.5" fill="none"/>
<text class="lbl" x="435.0" y="61.7" text-anchor="end">transformer</text>
<text class="lbl" x="120.4" y="86.1" text-anchor="start">CNN</text>
<text class="lbl" x="314.7" y="101.1" text-anchor="middle">RNN, LSTM, GRU</text>
<text class="ttl2 l" x="36.0" y="192">at init, varying only the LSTM forget-gate bias</text>
<g class="axis">
<line x1="66.0" y1="208.4" x2="442.0" y2="208.4"/>
<text class="tick-lbl" x="60.0" y="211.9" text-anchor="end">1</text>
<line x1="66.0" y1="245.0" x2="442.0" y2="245.0"/>
<text class="tick-lbl" x="60.0" y="248.5" text-anchor="end">1e-4</text>
<line x1="66.0" y1="281.7" x2="442.0" y2="281.7"/>
<text class="tick-lbl" x="60.0" y="285.2" text-anchor="end">1e-8</text>
</g>
<path class="curve ok" d="M66.0,208.4 L69.0,211.1 L71.9,211.4 L74.9,211.6 L77.8,211.7 L80.8,211.8 L83.8,211.9 L86.7,212.0 L89.7,212.1 L92.6,212.2 L95.6,212.3 L98.6,212.3 L101.5,212.4 L104.5,212.4 L107.4,212.5 L110.4,212.5 L113.4,212.5 L116.3,212.6 L119.3,212.6 L122.3,212.6 L125.2,212.6 L128.2,212.6 L131.1,212.7 L134.1,212.7 L137.1,212.7 L140.0,212.7 L143.0,212.7 L145.9,212.7 L148.9,212.7 L151.9,212.7 L154.8,212.7 L157.8,212.7 L160.7,212.6 L163.7,212.7 L166.7,212.6 L169.6,212.6 L172.6,212.6 L175.5,212.6 L178.5,212.6 L181.5,212.6 L184.4,212.5 L187.4,212.6 L190.3,212.5 L193.3,212.5 L196.3,212.5 L199.2,212.5 L202.2,212.5 L205.1,212.4 L208.1,212.4 L211.1,212.4 L214.0,212.4 L217.0,212.4 L220.0,212.3 L222.9,212.3 L225.9,212.4 L228.8,212.3 L231.8,212.3 L234.8,212.3 L237.7,212.3 L240.7,212.2 L243.6,212.2 L246.6,212.1 L249.6,212.2 L252.5,212.1 L255.5,212.1 L258.4,212.1 L261.4,212.0 L264.4,212.0 L267.3,212.0 L270.3,211.9 L273.2,211.9 L276.2,211.8 L279.2,211.8 L282.1,211.8 L285.1,211.7 L288.0,211.7 L291.0,211.7 L294.0,211.6 L296.9,211.6 L299.9,211.5 L302.9,211.5 L305.8,211.4 L308.8,211.4 L311.7,211.4 L314.7,211.3 L317.7,211.2 L320.6,211.2 L323.6,211.2 L326.5,211.1 L329.5,211.1 L332.5,211.0 L335.4,211.0 L338.4,210.9 L341.3,210.8 L344.3,210.8 L347.3,210.7 L350.2,210.6 L353.2,210.6 L356.1,210.5 L359.1,210.4 L362.1,210.3 L365.0,210.2 L368.0,210.2 L370.9,210.1 L373.9,209.9 L376.9,209.9 L379.8,209.7 L382.8,209.7 L385.7,209.6 L388.7,209.4 L391.7,209.3 L394.6,209.2 L397.6,209.0 L400.6,208.9 L403.5,208.7 L406.5,208.5 L409.4,208.4 L412.4,208.2 L415.4,208.1 L418.3,207.9 L421.3,207.7 L424.2,207.5 L427.2,207.3 L430.2,207.0 L433.1,206.8 L436.1,206.5 L439.0,206.3 L442.0,206.0" fill="none"/>
<path class="curve ok2" d="M66.0,208.4 L69.0,209.5 L71.9,210.0 L74.9,210.4 L77.8,210.8 L80.8,211.1 L83.8,211.4 L86.7,211.7 L89.7,212.0 L92.6,212.2 L95.6,212.4 L98.6,212.6 L101.5,212.8 L104.5,213.0 L107.4,213.2 L110.4,213.3 L113.4,213.5 L116.3,213.7 L119.3,213.8 L122.3,214.0 L125.2,214.1 L128.2,214.3 L131.1,214.5 L134.1,214.6 L137.1,214.7 L140.0,214.8 L143.0,215.0 L145.9,215.1 L148.9,215.2 L151.9,215.4 L154.8,215.5 L157.8,215.6 L160.7,215.7 L163.7,215.8 L166.7,216.0 L169.6,216.1 L172.6,216.2 L175.5,216.3 L178.5,216.4 L181.5,216.5 L184.4,216.6 L187.4,216.7 L190.3,216.9 L193.3,217.0 L196.3,217.1 L199.2,217.2 L202.2,217.3 L205.1,217.4 L208.1,217.5 L211.1,217.6 L214.0,217.7 L217.0,217.9 L220.0,218.0 L222.9,218.1 L225.9,218.2 L228.8,218.3 L231.8,218.4 L234.8,218.5 L237.7,218.6 L240.7,218.7 L243.6,218.8 L246.6,218.9 L249.6,219.0 L252.5,219.1 L255.5,219.2 L258.4,219.3 L261.4,219.4 L264.4,219.5 L267.3,219.6 L270.3,219.7 L273.2,219.9 L276.2,219.9 L279.2,220.1 L282.1,220.2 L285.1,220.2 L288.0,220.3 L291.0,220.4 L294.0,220.5 L296.9,220.6 L299.9,220.8 L302.9,220.8 L305.8,220.9 L308.8,221.1 L311.7,221.2 L314.7,221.3 L317.7,221.3 L320.6,221.5 L323.6,221.6 L326.5,221.6 L329.5,221.8 L332.5,221.9 L335.4,221.9 L338.4,222.1 L341.3,222.1 L344.3,222.3 L347.3,222.3 L350.2,222.4 L353.2,222.5 L356.1,222.7 L359.1,222.7 L362.1,222.8 L365.0,222.9 L368.0,223.0 L370.9,223.1 L373.9,223.2 L376.9,223.3 L379.8,223.4 L382.8,223.5 L385.7,223.6 L388.7,223.7 L391.7,223.8 L394.6,223.8 L397.6,223.9 L400.6,224.0 L403.5,224.1 L406.5,224.1 L409.4,224.2 L412.4,224.3 L415.4,224.4 L418.3,224.4 L421.3,224.5 L424.2,224.5 L427.2,224.5 L430.2,224.6 L433.1,224.6 L436.1,224.7 L439.0,224.7 L442.0,224.7" fill="none"/>
<path class="curve ok3" d="M66.0,208.4 L69.0,209.8 L71.9,210.9 L74.9,211.9 L77.8,212.8 L80.8,213.7 L83.8,214.6 L86.7,215.4 L89.7,216.2 L92.6,217.0 L95.6,217.7 L98.6,218.4 L101.5,219.2 L104.5,219.9 L107.4,220.6 L110.4,221.3 L113.4,222.0 L116.3,222.7 L119.3,223.4 L122.3,224.1 L125.2,224.7 L128.2,225.4 L131.1,226.0 L134.1,226.8 L137.1,227.4 L140.0,228.1 L143.0,228.8 L145.9,229.4 L148.9,230.1 L151.9,230.8 L154.8,231.4 L157.8,232.1 L160.7,232.8 L163.7,233.5 L166.7,234.1 L169.6,234.8 L172.6,235.5 L175.5,236.2 L178.5,236.8 L181.5,237.5 L184.4,238.1 L187.4,238.8 L190.3,239.4 L193.3,240.1 L196.3,240.8 L199.2,241.4 L202.2,242.0 L205.1,242.7 L208.1,243.4 L211.1,244.0 L214.0,244.7 L217.0,245.3 L220.0,246.0 L222.9,246.6 L225.9,247.3 L228.8,247.9 L231.8,248.6 L234.8,249.2 L237.7,249.8 L240.7,250.5 L243.6,251.1 L246.6,251.8 L249.6,252.4 L252.5,253.1 L255.5,253.7 L258.4,254.3 L261.4,254.9 L264.4,255.6 L267.3,256.3 L270.3,256.9 L273.2,257.6 L276.2,258.2 L279.2,258.8 L282.1,259.5 L285.1,260.1 L288.0,260.7 L291.0,261.4 L294.0,262.0 L296.9,262.7 L299.9,263.3 L302.9,264.0 L305.8,264.6 L308.8,265.2 L311.7,265.9 L314.7,266.6 L317.7,267.2 L320.6,267.9 L323.6,268.5 L326.5,269.2 L329.5,269.8 L332.5,270.4 L335.4,271.1 L338.4,271.8 L341.3,272.4 L344.3,273.1 L347.3,273.7 L350.2,274.3 L353.2,275.0 L356.1,275.7 L359.1,276.3 L362.1,276.9 L365.0,277.5 L368.0,278.2 L370.9,278.9 L373.9,279.5 L376.9,280.2 L379.8,280.8 L382.8,281.5 L385.7,282.1 L388.7,282.7 L391.7,283.3 L394.6,284.0 L397.6,284.6 L400.6,285.3 L403.5,285.9 L406.5,286.5 L409.4,287.2 L412.4,287.8 L415.4,288.5 L418.3,289.1 L421.3,289.8 L424.2,290.4 L427.2,291.0 L430.2,291.7 L433.1,292.3 L436.1,292.9 L439.0,293.5 L442.0,294.1" fill="none"/>
<path class="curve bad" d="M66.0,208.4 L69.0,211.0 L71.9,213.4 L74.9,215.6 L77.8,217.7 L80.8,219.8 L83.8,221.8 L86.7,223.8 L89.7,225.8 L92.6,227.7 L95.6,229.6 L98.6,231.5 L101.5,233.4 L104.5,235.3 L107.4,237.1 L110.4,239.0 L113.4,240.9 L116.3,242.7 L119.3,244.5 L122.3,246.4 L125.2,248.3 L128.2,250.1 L131.1,251.9 L134.1,253.8 L137.1,255.7 L140.0,257.5 L143.0,259.4 L145.9,261.2 L148.9,263.1 L151.9,264.9 L154.8,266.7 L157.8,268.6 L160.7,270.4 L163.7,272.3 L166.7,274.1 L169.6,275.9 L172.6,277.7 L175.5,279.6 L178.5,281.4 L181.5,283.2 L184.4,285.0 L187.4,286.8 L190.3,288.5 L193.3,290.3 L196.3,292.1 L199.2,293.9 L202.2,295.7 L205.1,297.5 L208.1,299.3 L211.1,300.0 L214.0,300.0 L217.0,300.0 L220.0,300.0 L222.9,300.0 L225.9,300.0 L228.8,300.0 L231.8,300.0 L234.8,300.0 L237.7,300.0 L240.7,300.0 L243.6,300.0 L246.6,300.0 L249.6,300.0 L252.5,300.0 L255.5,300.0 L258.4,300.0 L261.4,300.0 L264.4,300.0 L267.3,300.0 L270.3,300.0 L273.2,300.0 L276.2,300.0 L279.2,300.0 L282.1,300.0 L285.1,300.0 L288.0,300.0 L291.0,300.0 L294.0,300.0 L296.9,300.0 L299.9,300.0 L302.9,300.0 L305.8,300.0 L308.8,300.0 L311.7,300.0 L314.7,300.0 L317.7,300.0 L320.6,300.0 L323.6,300.0 L326.5,300.0 L329.5,300.0 L332.5,300.0 L335.4,300.0 L338.4,300.0 L341.3,300.0 L344.3,300.0 L347.3,300.0 L350.2,300.0 L353.2,300.0 L356.1,300.0 L359.1,300.0 L362.1,300.0 L365.0,300.0 L368.0,300.0 L370.9,300.0 L373.9,300.0 L376.9,300.0 L379.8,300.0 L382.8,300.0 L385.7,300.0 L388.7,300.0" fill="none"/>
<path class="curve bad2" d="M66.0,208.4 L69.0,210.9 L71.9,213.3 L74.9,215.8 L77.8,218.3 L80.8,220.8 L83.8,223.3 L86.7,225.8 L89.7,228.3 L92.6,230.9 L95.6,233.3 L98.6,235.7 L101.5,238.2 L104.5,240.7 L107.4,243.2 L110.4,245.7 L113.4,248.1 L116.3,250.6 L119.3,253.1 L122.3,255.5 L125.2,258.0 L128.2,260.4 L131.1,263.0 L134.1,265.5 L137.1,267.9 L140.0,270.4 L143.0,273.0 L145.9,275.4 L148.9,277.8 L151.9,280.3 L154.8,282.7 L157.8,285.2 L160.7,287.7 L163.7,290.2 L166.7,292.6 L169.6,295.1 L172.6,297.6 L175.5,300.0 L178.5,300.0 L181.5,300.0 L184.4,300.0 L187.4,300.0 L190.3,300.0 L193.3,300.0 L196.3,300.0 L199.2,300.0 L202.2,300.0 L205.1,300.0 L208.1,300.0 L211.1,300.0 L214.0,300.0 L217.0,300.0 L220.0,300.0 L222.9,300.0 L225.9,300.0 L228.8,300.0 L231.8,300.0 L234.8,300.0 L237.7,300.0 L240.7,300.0 L243.6,300.0 L246.6,300.0 L249.6,300.0 L252.5,300.0 L255.5,300.0 L258.4,300.0 L261.4,300.0 L264.4,300.0 L267.3,300.0 L270.3,300.0 L273.2,300.0 L276.2,300.0 L279.2,300.0 L282.1,300.0 L285.1,300.0 L288.0,300.0 L291.0,300.0 L294.0,300.0 L296.9,300.0 L299.9,300.0" fill="none"/>
<text class="lbl" x="435.0" y="199.0" text-anchor="end">b=3</text>
<text class="lbl" x="435.0" y="237.7" text-anchor="end">b=2</text>
<text class="lbl" x="402.4" y="280.2" text-anchor="end">b=1</text>
<text class="lbl" x="209.2" y="308.7" text-anchor="start">b=0</text>
<text class="lbl" x="147.8" y="295.7" text-anchor="end">no gate</text>
<g class="lbl-ax">
<text x="66.0" y="316">0</text>
<text x="116.3" y="316">17</text>
<text x="160.7" y="316">32</text>
<text x="255.5" y="316">64</text>
<text x="350.2" y="316">96</text>
<text x="442.0" y="316">127</text>
<text class="cap l" x="66.0" y="331">characters back from the last position</text></g>
</svg>
<figcaption>The gradient each position's input embedding receives when the loss at the last position is sent backward, with the last position set to 1 and a log vertical axis. Above: five architectures after training. The CNN stops at 17, the three recurrent models die at almost the same rate, and only the transformer flattens far away. Below: an untrained LSTM with only the forget-gate bias changed. The axis floor is 1e-10 and anything under it is drawn on the floor.</figcaption>
</figure>

Taking the five architectures from part seven, each trained to its own minimum:

```
             17 back    64 back   127 back
transformer  6.76e-02   1.32e-02   1.19e-02
RNN          2.98e-02   2.09e-04   8.24e-07
LSTM         3.65e-02   2.28e-04   4.78e-07
GRU          2.67e-02   1.41e-04   3.04e-07
CNN          0.00e+00   0.00e+00   0.00e+00
```

The transformer stops falling somewhere past 64. At 127 back it is still at
`1.19e-02`, which is **39,145 times** the GRU's `3.04e-07` at the same distance.
Attention wires positions to each other directly, so distance does not lengthen
the path.

## The convolution is exactly zero at 17

The CNN's entries are `0.00e+00`. Not small - zero.

Part seven put its receptive field at `4 x 4 + 1 = 17` characters for four layers
of kernel 5. That means positions further back than 17 are not in the computation
graph at all, and what is not in the graph has no gradient rather than a small
one. Part seven's sentence is confirmed exactly here.

## Gates do not extend the reach

The textbook says LSTM and GRU solve vanishing gradients. It is not visible in
that table. At 127 back the ungated RNN is at `8.24e-07`, the LSTM at `4.78e-07`
and the GRU at `3.04e-07` - **the gated ones are smaller.**

A trained model may simply have decided to forget, so measure again before
training. The recurrent models have no context limit, so they can also be
unrolled to 512.

```
                  half    1/100   1/10000
RNN                  2        8        15
LSTM                 2        9        19
GRU                  2        9        19
```

Three seeds agree to the character. Unrolling to 512 changes nothing. **What
gating buys is the 1/10000 reach going from 15 characters to 19.** Four
characters.

## The cause is one bias

An LSTM carries its cell state as `c_t = f_t · c_{t-1} + ...`, so a gradient
travelling backward is multiplied by `f_t` at every step. What sets the reach is
the forget gate.

PyTorch starts every bias near `0`, forget gate included, so `sigmoid(0) = 0.5`.
**Half the signal dies every step.** `0.5^127` is `5.88e-39`, below float32's
smallest normal number of `1.18e-38`, which is why an untrained model's gradient
at 127 back underflows to exactly `0` - the same as the ungated RNN.

Changing only that bias to `b` and measuring again:

```
   b   sigmoid(b)   half   1/100     1/10000
   0        0.500      2       9          19
   1        0.731      3      23          51
   2        0.881      5     117    never dies
   3        0.953      1  never dies never dies
```

At `b = 2` the gradient never falls below 1/10000 within the 128-character
context. At `b = 3` the gradient 127 back is `1.80` times the last position's -
larger than its source, the other side of vanishing.

**Gating does not solve the problem; gating held open solves it.** The old advice
to initialise the forget-gate bias at 1 or 2 is this table.

## And then the loss gets worse

That would be a tidy story, except for what comes next. Changing only the bias
and training again under the same protocol:

```
   b   1/10000 reach   best val (3 seeds)              median
   0        19 chars   1.6771  1.6739  1.6787       1.6771
   1        51 chars   1.7204  1.6983  1.7258       1.7204
   2      never dies   1.7546  1.7350  1.7463       1.7463
```

**Monotonically worse.** The three seeds at `b = 0` span `1.6739~1.6787` and at
`b = 2` span `1.7350~1.7546`, ranges that do not overlap. The further the
gradient travels, the higher the loss.

Which makes sense. The task is next-character prediction over 128 characters. A
character a hundred back rarely decides the one now. Holding the forget gate open
makes the hidden state keep carrying old material, and material with no use is
noise. **Forgetting is a feature.**

Part seven already showed the same shape: the transformer sends gradient forty
thousand times further than the GRU and loses to it by `11.6%`. Reach does not
predict performance.

## What is left

This conclusion is attached to **128 characters of context and next-character
prediction**. On a task where the front of the sequence genuinely matters -
matching brackets, long dependencies, copying - reach would be performance. No
such task was built here.

The cell-state path was not isolated either. What is measured is the gradient
arriving at the input embedding, which mixes the cell route with the gate route.
Separating out the identity path the textbook talks about might look different.

And whether `b = 2` hurt because of the reach or because the state saturates
early in training is not distinguished here. Telling those apart means pulling
the gate values out directly, which is the next part.

## So

- Measuring what the loss at the last position sends backward, the three
  recurrent models nearly coincide: `8.24e-07` / `4.78e-07` / `3.04e-07` at 127
- The transformer stops falling past 64 and is `39,145` times the GRU at 127 back
- The CNN is **exactly zero** at 17. Not in the graph means no gradient, not a
  small one
- At init, gating buys `15 -> 19` characters of 1/10000 reach. Four characters
- The cause is a forget-gate bias of `0`, making `sigmoid(0) = 0.5` and killing
  half per step. `0.5^127` underflows in float32
- Opening the bias to `2` stops it dying inside 128 characters; at `3` the
  gradient 127 back is `1.80` times its source
- But the loss goes `1.6771 -> 1.7204 -> 1.7463`, monotonically worse. On this
  task, forgetting is a feature
