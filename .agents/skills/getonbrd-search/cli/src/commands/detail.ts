import { htmlFetch, stripHtml, decodeHtmlEntities, writeError, SITE, type JobDetail } from "../helpers.js"

export interface DetailOpts {
  id: string
  format: "json" | "plain"
}

/** Accept a bare slug, a getonbrd job URL (/jobs/<slug> or /jobs/<cat>/<slug>). */
export function normalizeSlug(input: string): string | null {
  const url = input.match(/getonbrd\.com\/jobs\/(?:[^/?#]+\/)?([^/?#]+)/i)
  if (url) return url[1]
  if (/^[a-z0-9][a-z0-9-]{5,}$/i.test(input)) return input
  return null
}

function metaContent(html: string, prop: string): string | null {
  const re = new RegExp(
    `<meta[^>]+(?:property|name)=["']${prop}["'][^>]+content=["']([^"']*)["']`,
    "i",
  )
  const m = html.match(re)
  if (m) return decodeHtmlEntities(m[1]).trim()
  const re2 = new RegExp(
    `<meta[^>]+content=["']([^"']*)["'][^>]+(?:property|name)=["']${prop}["']`,
    "i",
  )
  const m2 = html.match(re2)
  return m2 ? decodeHtmlEntities(m2[1]).trim() : null
}

/**
 * Extract the readable job body. The public API's single-job endpoint is paywalled,
 * so we read the public page. Prefer the <main> content; fall back to og:description.
 */
function extractDescription(html: string): string | null {
  // Get on Board marks the full posting body with schema.org microdata.
  const open = html.match(/itemprop=["']description["'][^>]*>/i)
  if (open && open.index !== undefined) {
    let chunk = html.slice(open.index + open[0].length, open.index + 14000)
    // Trim at the page chrome that follows the posting body.
    chunk = chunk.split(/<footer|id=["']apply|class=["'][^"']*(?:job-actions|similar-jobs|company-jobs)/i)[0]
    const text = stripHtml(chunk)
      .replace(/©\s*Get on Board\.?[^\n]*?reserved\.?/gi, "")
      .replace(/\n{3,}/g, "\n\n")
      .trim()
    if (text.length > 150) return text
  }
  return metaContent(html, "og:description")
}

export async function runDetail(opts: DetailOpts): Promise<number> {
  const slug = normalizeSlug(opts.id)
  if (!slug) {
    writeError(`Could not parse a Get on Board job slug/URL from "${opts.id}"`, "BAD_ID")
    return 1
  }
  try {
    const html = await htmlFetch(`${SITE}/jobs/${slug}`)
    if (!html) {
      writeError("Job not found", "NOT_FOUND")
      return 1
    }
    const ogTitle = metaContent(html, "og:title")
    const title = ogTitle ? ogTitle.replace(/\s*[-|]\s*Get on Board.*$/i, "").trim() : slug
    const description = extractDescription(html)

    const job: JobDetail = {
      id: slug,
      title,
      company: null,
      location: null,
      date: null,
      url: `${SITE}/jobs/${slug}`,
      remote: /remote/i.test(metaContent(html, "og:description") || ""),
      modality: null,
      salary: null,
      category: null,
      description,
    }

    if (opts.format === "plain") {
      const lines = [title, "", description || "(no description)", "", `URL: ${job.url}`]
      process.stdout.write(lines.join("\n") + "\n")
    } else {
      process.stdout.write(JSON.stringify(job, null, 2) + "\n")
    }
    return 0
  } catch (e) {
    writeError(e instanceof Error ? e.message : String(e), "DETAIL_FAILED")
    return 1
  }
}
