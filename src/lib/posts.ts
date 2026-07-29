import { getCollection, type CollectionEntry } from "astro:content";
import { seriesOf } from "../data/series";

export type Post = CollectionEntry<"blog">;

/**
 * Drafts are visible while writing and invisible once built, so a half-written
 * post can be read at its real URL without ever shipping. `astro dev` shows
 * them; so does `DRAFTS=1 npm run build`, which is the only way to see a
 * Korean draft in its real type - the subsetter runs over dist/, not over the
 * dev server.
 */
const showDrafts = import.meta.env.DEV || process.env.DRAFTS === "1";

export async function posts(): Promise<Post[]> {
  const all = await getCollection("blog");
  return all
    .filter((p) => showDrafts || !p.data.draft)
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/**
 * A translation lives at en/<slug> next to <slug>. Pairing by path means a
 * post gains a language toggle by existing, with nothing to register.
 */
export const isTranslation = (p: Post) => p.id.startsWith("en/");
export const baseId = (p: Post) => (isTranslation(p) ? p.id.slice(3) : p.id);

export function alternateOf(post: Post, all: Post[]): Post | undefined {
  const wanted = isTranslation(post) ? baseId(post) : `en/${post.id}`;
  return all.find((p) => p.id === wanted);
}

/** what the listings show: originals only, never both halves of a pair */
export const originals = (all: Post[]) => all.filter((p) => !isTranslation(p));

/** the posts of one series, in reading order rather than by date */
export function partsOf(all: Post[], id: string): Post[] {
  return originals(all)
    .filter((p) => p.data.series?.id === id)
    .sort((a, b) => a.data.series!.part - b.data.series!.part);
}

/** every series that has at least one post, newest first by its latest part */
export function seriesIndex(all: Post[]) {
  const ids = [...new Set(originals(all).map((p) => p.data.series?.id).filter(Boolean) as string[])];
  return ids
    .map((id) => ({ id, meta: seriesOf(id)!, parts: partsOf(all, id) }))
    .filter((s) => s.meta && s.parts.length)
    .sort((a, b) => latest(b.parts) - latest(a.parts));
}

const latest = (parts: Post[]) => Math.max(...parts.map((p) => p.data.date.valueOf()));

export const KIND_LABEL: Record<string, string> = {
  log: "log",
  guide: "guide",
  note: "note",
};

/** One format everywhere: a list of mixed date formats reads as a bug. */
export const fmtDate = (d: Date) =>
  d.toLocaleDateString("en-GB", { year: "numeric", month: "short", day: "numeric" });

export const fmtLong = (d: Date) =>
  d.toLocaleDateString("en-GB", { year: "numeric", month: "long", day: "numeric" });
