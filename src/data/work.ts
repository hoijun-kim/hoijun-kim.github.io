/**
 * The projects, once. The board renders from this and so does /work.json, so
 * the two views cannot disagree - the raw view is literally the endpoint.
 */

export type Project = {
  name: string;
  version: string;
  summary: string;
  /** rendered with <b> around the phrases worth catching at a glance */
  highlight: string[];
  links: { download: string; site: string; source: string };
  stack: string[];
  /** the row's second spec line - key is shown as the label */
  runs: { label: string; items: string[] };
  replaces: string[];
  license: string;
  colour: { light: string; dark: string };
};

export const profile = {
  name: "Hoijun Kim",
  role: "Software engineer",
  links: {
    github: "https://github.com/hoijun-kim",
    email: "mailto:hoijun.kim00@gmail.com",
  },
};

export const work: Project[] = [
  {
    name: "shape",
    version: "v0.1.0",
    summary:
      "Drag in a data file and see the rows that are actually in it. Filter, reshape, edit and export by clicking - and read off the jq and SQL your clicks just wrote, so you leave knowing the query too.",
    highlight: ["clicking", "jq and SQL"],
    links: {
      download: "https://github.com/hoijun-kim/shape/releases",
      site: "https://hoijun-kim.github.io/shape/",
      source: "https://github.com/hoijun-kim/shape",
    },
    stack: ["Go", "Svelte", "Wails", "cgo-free"],
    runs: { label: "reads", items: ["JSON", "NDJSON", "CSV", "TSV", "Parquet", "SQLite"] },
    replaces: ["jq", "SQL"],
    license: "PolyForm NC 1.0.0",
    colour: { light: "#E07C15", dark: "#F2933A" },
  },
  {
    name: "fleet",
    version: "v0.1.0",
    summary:
      "Every git repo under your project roots on one board. See which are dirty, behind or stale at a glance, then fetch, commit, resolve a conflict, or open an editor - without walking the directories yourself.",
    highlight: ["dirty, behind or stale"],
    links: {
      download: "https://github.com/hoijun-kim/fleet/releases",
      site: "https://hoijun-kim.github.io/fleet/",
      source: "https://github.com/hoijun-kim/fleet",
    },
    stack: ["Go", "Wails", "Fly.io", "Neon"],
    runs: { label: "runs on", items: ["Windows", "macOS", "Linux"] },
    replaces: ["git status", "git fetch", "cd .."],
    license: "PolyForm NC 1.0.0",
    colour: { light: "#2F6BFF", dark: "#5B8CFF" },
  },
];

/** what /work.json serves, and what the raw view shows */
export function workDocument() {
  return {
    name: profile.name,
    role: profile.role,
    links: { github: profile.links.github, email: profile.links.email },
    work: work.map((p) => ({
      name: p.name,
      version: p.version,
      summary: p.summary,
      links: p.links,
      stack: p.stack,
      [p.runs.label === "reads" ? "reads" : "platforms"]: p.runs.items,
      replaces: p.replaces,
      license: p.license,
    })),
  };
}

/** wraps the highlighted phrases in <b> without letting anything else through */
export function emphasise(text: string, phrases: string[]): string {
  const escaped = text.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]!);
  return phrases.reduce(
    (out, phrase) => out.replace(phrase, `<b>${phrase}</b>`),
    escaped,
  );
}
