import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    /** posts are written in one language or the other, never both */
    lang: z.enum(["en", "ko"]).default("en"),
    /**
     * log   - building the tools: what broke, what it cost
     * guide - explaining something, usually with a figure
     * note  - short, one idea
     */
    kind: z.enum(["log", "guide", "note"]).default("log"),
    /** membership in an ordered run of posts; the id keys src/data/series.ts */
    series: z.object({ id: z.string(), part: z.number().int().positive() }).optional(),
    /** true keeps it out of the build, but `astro dev` still shows it */
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
