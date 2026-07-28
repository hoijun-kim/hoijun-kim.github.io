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
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
