import {
  apiFetch,
  mapJobCard,
  companyIdOf,
  resolveCompanyNames,
  writeError,
  type ApiList,
  type RawJob,
  type JobCard,
} from "../helpers.js"

export interface SearchOpts {
  query?: string
  category?: string
  location?: string
  remote: boolean
  jobage: number
  page: number
  limit?: number
  format: "json" | "table" | "plain"
}

/**
 * Build the API path. Category browse (`/categories/<cat>/jobs`) is preferred for a
 * focused field like design; keyword search (`/search/jobs`) is full-text and looser.
 */
function buildPath(opts: SearchOpts, perPage: number): string {
  const params = new URLSearchParams()
  params.set("page", String(opts.page))
  params.set("per_page", String(perPage))
  if (opts.category) {
    return `/categories/${encodeURIComponent(opts.category)}/jobs?${params.toString()}`
  }
  params.set("query", opts.query ?? "")
  return `/search/jobs?${params.toString()}`
}

/** Client-side filters (the public API has no direct params for these). */
function applyFilters(raws: RawJob[], opts: SearchOpts): RawJob[] {
  let out = raws
  if (opts.remote) out = out.filter((r) => r.attributes?.remote === true)
  if (opts.location) {
    const q = opts.location.toLowerCase()
    out = out.filter((r) => {
      const cs = Array.isArray(r.attributes?.countries)
        ? (r.attributes!.countries as unknown[]).join(" ").toLowerCase()
        : ""
      const rem = r.attributes?.remote ? "remote" : ""
      return `${cs} ${rem}`.includes(q)
    })
  }
  // When browsing a category, an optional --query narrows client-side by title.
  if (opts.category && opts.query) {
    const q = opts.query.toLowerCase()
    out = out.filter((r) => String(r.attributes?.title ?? "").toLowerCase().includes(q))
  }
  if (opts.jobage && opts.jobage < 9999) {
    const cutoff = Math.floor(Date.now() / 1000) - opts.jobage * 86400
    out = out.filter((r) => {
      const ts = r.attributes?.published_at
      return typeof ts === "number" && ts >= cutoff
    })
  }
  return out
}

function renderTable(cards: JobCard[]): string {
  if (cards.length === 0) return "No results."
  const rows = cards.map((c) => {
    const id = c.id.slice(0, 36).padEnd(36)
    const title = (c.title || "").slice(0, 34).padEnd(34)
    const company = (c.company || "—").slice(0, 22).padEnd(22)
    const loc = (c.location || "—").slice(0, 18).padEnd(18)
    return `${id} ${title} ${company} ${loc} ${c.date || "—"}`
  })
  const header =
    "ID".padEnd(36) + " " + "TITLE".padEnd(34) + " " + "COMPANY".padEnd(22) + " " + "LOCATION".padEnd(18) + " DATE"
  return [header, "-".repeat(header.length), ...rows].join("\n")
}

export async function runSearch(opts: SearchOpts): Promise<number> {
  try {
    const perPage = opts.limit && opts.limit > 0 ? Math.min(Math.max(opts.limit, 10), 50) : 20
    const list = await apiFetch<ApiList>(buildPath(opts, perPage))
    let raws: RawJob[] = list?.data ?? []
    raws = applyFilters(raws, opts)
    if (opts.limit !== undefined && opts.limit >= 0) raws = raws.slice(0, opts.limit)

    const cache = new Map<number, string | null>()
    const ids = raws.map(companyIdOf).filter((x): x is number => x !== null)
    await resolveCompanyNames(ids, cache)

    const cards: JobCard[] = raws.map((r) => {
      const cid = companyIdOf(r)
      return mapJobCard(r, cid !== null ? (cache.get(cid) ?? null) : null)
    })

    if (opts.format === "table") {
      process.stdout.write(renderTable(cards) + "\n")
    } else if (opts.format === "plain") {
      process.stdout.write(
        cards
          .map(
            (c) =>
              `${c.title}\n  ${c.company || "—"} · ${c.location || "—"} · ${c.date || "—"}\n  id: ${c.id}\n  ${c.url}`,
          )
          .join("\n\n") + "\n",
      )
    } else {
      process.stdout.write(
        JSON.stringify({ meta: { count: cards.length, page: opts.page }, results: cards }, null, 2) + "\n",
      )
    }
    return 0
  } catch (e) {
    writeError(e instanceof Error ? e.message : String(e), "SEARCH_FAILED")
    return 1
  }
}
