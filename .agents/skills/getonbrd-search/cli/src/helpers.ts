// Data source: Get on Board public API (https://www.getonbrd.com/api/v0).
// The public API is open to anyone and returns the same data visible on the site
// without logging in (categories, company profiles, published jobs). The single-job
// endpoint (/jobs/:slug) requires a paid key and returns 401, so `detail` reads the
// public job page HTML instead. Personal use, low volume.

export const API_BASE = "https://www.getonbrd.com/api/v0"
export const SITE = "https://www.getonbrd.com"

export function writeError(error: string, code: string): void {
  process.stderr.write(JSON.stringify({ error, code }) + "\n")
}

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

/** Fetch with exponential backoff + jitter on 429/5xx (max 6 retries). */
async function fetchWithBackoff(url: string, accept: string): Promise<Response> {
  const maxRetries = 6
  let delay = 500
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const response = await fetch(url, {
      headers: { "User-Agent": UA, Accept: accept, "Accept-Language": "es,en;q=0.9" },
      redirect: "follow",
    })
    if (response.status === 429 || response.status >= 500) {
      if (attempt === maxRetries) {
        throw new Error(`Request failed: ${response.status} ${response.statusText}`)
      }
      const jitter = Math.floor(Math.random() * 500)
      await new Promise((r) => setTimeout(r, delay + jitter))
      delay = Math.min(delay * 2, 8000)
      continue
    }
    return response
  }
  throw new Error("Request failed after max retries")
}

/** Fetch JSON from the public API. Returns null on 401/404 (private or gone). */
export async function apiFetch<T = unknown>(path: string): Promise<T | null> {
  const res = await fetchWithBackoff(`${API_BASE}${path}`, "application/json")
  if (res.status === 401 || res.status === 404) return null
  if (!res.ok) throw new Error(`Request failed: ${res.status} ${res.statusText}`)
  return (await res.json()) as T
}

/** Fetch HTML (public job page). Returns "" on 404. */
export async function htmlFetch(url: string): Promise<string> {
  const res = await fetchWithBackoff(url, "text/html,application/xhtml+xml")
  if (res.status === 404) return ""
  if (!res.ok) throw new Error(`Request failed: ${res.status} ${res.statusText}`)
  return res.text()
}

// ---------- HTML / entity helpers ----------

function numericEntity(cp: number): string {
  return cp >= 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : ""
}

export function decodeHtmlEntities(text: string): string {
  return text
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, dec) => numericEntity(parseInt(dec, 10)))
    .replace(/&#[xX]([0-9a-fA-F]+);/g, (_, hex) => numericEntity(parseInt(hex, 16)))
    .replace(/&nbsp;/g, " ")
}

/** Strip tags to readable text, preserving paragraph/list breaks as newlines. */
export function stripHtml(html: string): string {
  const withBreaks = html
    .replace(/<\s*br\s*\/?>/gi, "\n")
    .replace(/<\/(p|li|ul|ol|div|h[1-6])>/gi, "\n")
  return decodeHtmlEntities(withBreaks.replace(/<[^>]+>/g, " "))
    .replace(/[ \t]+/g, " ")
    .replace(/\n[ \t]+/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim()
}

// ---------- Types ----------

export interface JobCard {
  id: string
  title: string
  company: string | null
  location: string | null
  date: string | null
  url: string
}

export interface JobDetail extends JobCard {
  remote: boolean
  modality: string | null
  salary: string | null
  category: string | null
  description: string | null
}

export interface RawJob {
  id: string
  type?: string
  attributes?: Record<string, unknown>
  links?: { public_url?: string }
}

export interface ApiList {
  data?: RawJob[]
  meta?: { page?: number; per_page?: number; total_pages?: number }
}

// ---------- Field mappers ----------

export function unixToDate(ts: unknown): string | null {
  if (typeof ts !== "number") return null
  const d = new Date(ts * 1000)
  if (isNaN(d.getTime())) return null
  return d.toISOString().slice(0, 10)
}

function attrs(raw: RawJob): Record<string, unknown> {
  return raw.attributes ?? {}
}

export function jobLocation(raw: RawJob): string | null {
  const a = attrs(raw)
  const countries = Array.isArray(a.countries) ? (a.countries as unknown[]).filter(Boolean).map(String) : []
  if (a.remote === true) {
    const named = countries.filter((c) => !/^remot[eo]$/i.test(c.trim()))
    return named.length ? `Remote (${named.join(", ")})` : "Remote"
  }
  return countries.length ? countries.join(", ") : null
}

export function salaryOf(raw: RawJob): string | null {
  const a = attrs(raw)
  const min = typeof a.min_salary === "number" ? a.min_salary : null
  const max = typeof a.max_salary === "number" ? a.max_salary : null
  if (!min && !max) return null
  if (min && max) return `USD ${min}-${max}`
  return `USD ${min || max}`
}

export function companyIdOf(raw: RawJob): number | null {
  const c = attrs(raw).company as { data?: { id?: unknown } } | undefined
  return typeof c?.data?.id === "number" ? c.data.id : null
}

export function mapJobCard(raw: RawJob, companyName: string | null): JobCard {
  const a = attrs(raw)
  return {
    id: raw.id,
    title: a.title ? String(a.title) : "(untitled)",
    company: companyName,
    location: jobLocation(raw),
    date: unixToDate(a.published_at),
    url: raw.links?.public_url || `${SITE}/jobs/${raw.id}`,
  }
}

/** Resolve company ids to names via the public /companies/:id endpoint, cached. */
export async function resolveCompanyNames(
  ids: number[],
  cache: Map<number, string | null>,
): Promise<void> {
  const unresolved = [...new Set(ids)].filter((id) => !cache.has(id))
  await Promise.all(
    unresolved.map(async (id) => {
      try {
        const d = await apiFetch<{ data?: { attributes?: { name?: string } } }>(`/companies/${id}`)
        cache.set(id, d?.data?.attributes?.name ?? null)
      } catch {
        cache.set(id, null)
      }
    }),
  )
}
