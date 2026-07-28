// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://hoijun-kim.github.io",
  trailingSlash: "ignore",
  integrations: [sitemap()],
  build: {
    // one stylesheet in the head rather than a pile of <link>s; the whole site
    // is a few KB of CSS
    inlineStylesheets: "auto",
  },
  markdown: {
    shikiConfig: {
      themes: { light: "github-light", dark: "github-dark" },
      wrap: false,
    },
  },
});
