/**
 * An ordered run of posts. Keyed by the id each post's frontmatter names, so a
 * series can be renamed in one place without touching the posts.
 */

export type Series = {
  name: string;
  /** one line, used on the series index and in its search result */
  description: string;
  /** what the reader should already have, in their words not mine */
  audience: string;
  lang: "en" | "ko";
};

export const series: Record<string, Series> = {
  "seeing-deep-learning": {
    name: "보이는 딥러닝",
    description:
      "딥러닝 기초를 그림으로 다시 본다. 매 편이 눈에 안 보이던 것 하나 - 메모리 위의 텐서, 손실 지형 위의 한 걸음, 그래프를 거슬러 흐르는 미분 - 를 그려서 확인한다.",
    audience: "파이썬과 NumPy 를 읽을 수 있으면 충분하다. 미적분은 필요한 만큼만 그 자리에서 짚는다.",
    lang: "ko",
  },
  "after-training": {
    name: "훈련이 끝난 뒤",
    description:
      "학습이 끝난 모델을 실제로 돌릴 때 붙는 것들을 잰다. 다음 글자를 고르는 규칙, 두 번 계산하지 않는 법, 정밀도를 버리고 남는 것 - 앞 시리즈에서 만든 모델을 그대로 쓴다.",
    audience: "앞 시리즈 '보이는 딥러닝' 을 읽었거나, 트랜스포머가 무엇을 계산하는지 알면 된다.",
    lang: "ko",
  },
  "not-attention": {
    name: "어텐션 말고",
    description:
      "순서를 다루는 방법이 어텐션만 있는 것은 아니다. RNN, LSTM, GRU, 1D 합성곱을 같은 코퍼스에 같은 파라미터 예산으로 학습해서 앞 시리즈의 트랜스포머와 직접 겨룬다 - 같은 것에 대고 재야 비교가 성립한다.",
    audience: "앞 시리즈 '보이는 딥러닝' 을 읽었거나, 트랜스포머가 무엇을 계산하는지 알면 된다.",
    lang: "ko",
  },
};

export const seriesOf = (id: string): Series | undefined => series[id];
