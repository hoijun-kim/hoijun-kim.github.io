import type { APIRoute } from "astro";
import { workDocument } from "../data/work";

/** The raw view on the home page shows this file. Same object, one source. */
export const GET: APIRoute = () =>
  new Response(JSON.stringify(workDocument(), null, 2) + "\n", {
    headers: { "content-type": "application/json; charset=utf-8" },
  });
