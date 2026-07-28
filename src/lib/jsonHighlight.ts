/**
 * Serialise a value to syntax-highlighted HTML, one <span class="l"> per line,
 * at build time. The text it produces is character-for-character what
 * JSON.stringify(value, null, 2) produces, so the rendered view and the file
 * served at /work.json cannot disagree.
 *
 * `tint` marks a sub-object whose strings should carry a project's colour: the
 * lines are wrapped in a .jobj that sets --c-light/--c-dark.
 */

type Tint = { light: string; dark: string };

const esc = (s: unknown) =>
  String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]!);

const p = (s: string) => `<span class="p">${esc(s)}</span>`;
const key = (k: string) => `<span class="k">"${esc(k)}"</span>${p(":")} `;

function scalar(v: unknown): string {
  if (typeof v === "string") return `<span class="s">"${esc(v)}"</span>`;
  if (v === null) return `<span class="n">null</span>`;
  return `<span class="n">${esc(v)}</span>`;
}

function emit(out: string[], v: unknown, indent: number, prefix: string, tail: string): void {
  const pad = "  ".repeat(indent);
  const line = (s: string) => out.push(`<span class="l">${pad}${s}</span>`);

  if (v && typeof v === "object") {
    const arr = Array.isArray(v);
    const keys = arr ? [] : Object.keys(v as object);
    const n = arr ? (v as unknown[]).length : keys.length;
    if (n === 0) {
      line(prefix + p(arr ? "[]" : "{}") + tail);
      return;
    }
    line(prefix + p(arr ? "[" : "{"));
    for (let i = 0; i < n; i++) {
      const k = arr ? null : keys[i]!;
      const child = arr ? (v as unknown[])[i] : (v as Record<string, unknown>)[k!];
      const sep = i < n - 1 ? p(",") : "";
      if (child && typeof child === "object") {
        emit(out, child, indent + 1, arr ? "" : key(k!), sep);
      } else {
        out.push(`<span class="l">${pad}  ${arr ? "" : key(k!)}${scalar(child)}${sep}</span>`);
      }
    }
    line(p(arr ? "]" : "}") + tail);
  } else {
    line(prefix + scalar(v) + tail);
  }
}

/**
 * @param doc    the object to render
 * @param tints  key of the array whose items get a colour, and the colours in
 *               the same order as that array
 */
export function highlight(
  doc: Record<string, unknown>,
  tints?: { arrayKey: string; colours: Tint[] },
): string {
  const out: string[] = [];
  const keys = Object.keys(doc);
  out.push(`<span class="l">${p("{")}</span>`);

  keys.forEach((k, i) => {
    const sep = i < keys.length - 1 ? p(",") : "";
    const value = doc[k];

    if (tints && k === tints.arrayKey && Array.isArray(value)) {
      out.push(`<span class="l">  ${key(k)}${p("[")}</span>`);
      value.forEach((item, j) => {
        const lines: string[] = [];
        emit(lines, item, 2, "", j < value.length - 1 ? p(",") : "");
        const c = tints.colours[j];
        out.push(
          c
            ? `<span class="jobj" data-c style="--c-light:${c.light};--c-dark:${c.dark}">${lines.join("")}</span>`
            : lines.join(""),
        );
      });
      out.push(`<span class="l">  ${p("]")}${sep}</span>`);
    } else if (value && typeof value === "object") {
      emit(out, value, 1, key(k), sep);
    } else {
      out.push(`<span class="l">  ${key(k)}${scalar(value)}${sep}</span>`);
    }
  });

  out.push(`<span class="l">${p("}")}</span>`);
  return out.join("");
}
