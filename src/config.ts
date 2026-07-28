/**
 * The parts that live on someone else's server. Each is off until switched on,
 * and off means nothing renders at all - no markup, no stylesheet, no request -
 * so the site is always shippable half-configured.
 */

export const analytics = {
  /**
   * The subdomain at goatcounter.com - "hoijun" for hoijun.goatcounter.com.
   * Sign up at https://www.goatcounter.com/signup, then paste the code here.
   * Cookieless and ~3.5 KB, so there is nothing to ask consent for.
   */
  goatcounter: "hoijun-kim",
};

export const views = {
  /**
   * Print the count on each post. Needs `analytics.goatcounter`, plus "Allow
   * public access to counts" in GoatCounter's settings. Counts under 25 stay
   * hidden - a number that small says nothing worth saying.
   */
  show: true,
};

export const comments = {
  /**
   * giscus, which stores comments as GitHub Discussions on this repo.
   * Flip `enabled` after installing https://github.com/apps/giscus on the
   * repo - until it is installed the widget only renders its own error.
   * The ids came from the GitHub API and match the repo below.
   */
  enabled: true,
  repo: "hoijun-kim/hoijun-kim.github.io",
  repoId: "R_kgDOTk6TBg",
  /** Announcements: only maintainers can open threads, giscus does it for them */
  category: "Announcements",
  categoryId: "DIC_kwDOTk6TBs4DCKUr",
};

export const analyticsOn = analytics.goatcounter.length > 0;
export const viewsOn = analyticsOn && views.show;
export const commentsOn =
  comments.enabled && comments.repoId.length > 0 && comments.categoryId.length > 0;
