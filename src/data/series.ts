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
};

export const seriesOf = (id: string): Series | undefined => series[id];
