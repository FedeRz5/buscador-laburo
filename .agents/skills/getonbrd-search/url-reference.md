# Get on Board API Reference

Public JSON API used by this skill. Base URL:

```
https://www.getonbrd.com/api/v0
```

The public API is open (no key) and returns the same data visible without logging in.
JSON:API-style envelope: `{ "data": [...], "meta": {...} }`; each resource has
`{ id, type, attributes, links }`.

## Search / browse jobs

Two ways to list jobs, both public:

### By category (recommended for a focused field)

```
GET /api/v0/categories/<category_id>/jobs?page=<n>&per_page=<n>
```

### Full-text keyword search

```
GET /api/v0/search/jobs?query=<text>&page=<n>&per_page=<n>
```

| Param | Meaning | Example |
|-------|---------|---------|
| `query` | Free-text (search endpoint) | `product designer` |
| `page` | 1-indexed page | `1`, `2`, … |
| `per_page` | Page size | `20` |

Response `meta`: `{ "page", "per_page", "total_pages" }`.

### Categories

```
GET /api/v0/categories
```

Returns `data[].{ id, attributes.name }`. Known ids include:
`sales`, `data-science-analytics`, `machine-learning-ai`, `sysadmin-devops-qa`,
`programming`, `education-coaching`, `design-ux`, and more.

## Job object (per result)

Each job's `attributes` include:

| Field | Meaning |
|-------|---------|
| `title` | Job title |
| `description`, `functions`, `projects`, `benefits`, `desirable` | Rich HTML sections (+ `*_headline`) |
| `remote` | Boolean |
| `remote_modality` | e.g. `remote_local`, `full_remote` |
| `countries` | Array, e.g. `["Chile"]` or `["Remoto"]` for remote |
| `min_salary`, `max_salary` | USD range (may be null) |
| `published_at` | Unix timestamp |
| `seniority`, `modality`, `company` | JSON:API references `{ data: { id, type } }` (id only) |
| `category_name` | e.g. `Design / UX` |

Top-level `links.public_url` is the human job page URL.

**Company name** is not inline — resolve the `company.data.id` via:

```
GET /api/v0/companies/<company_id>
```

→ `data.attributes.name` (public endpoint). This skill caches these per run.

## Job detail (public page)

The single-job API endpoint is **paywalled**:

```
GET /api/v0/jobs/<slug>      → HTTP 401 Unauthorized (paid key required)
```

So `detail` reads the **public HTML page** instead:

```
GET https://www.getonbrd.com/jobs/<slug>
```

- Returns `301` → `https://www.getonbrd.com/jobs/<category>/<slug>`; follow the redirect
  and send a browser `User-Agent`.
- The full posting body lives in the element with `itemprop="description"` (schema.org
  microdata). The parser slices from that opening tag, strips the `© Get on Board … reserved`
  watermark, and cuts at the page chrome (`<footer`, `id="apply"`, similar-jobs blocks).
- `og:title` / `og:description` meta tags are reliable fallbacks.

## Notes

- No authentication for the public endpoints used here; keep volume low.
- Backoff on 429/5xx with jitter (max 6 retries); `null`/`""` on 401/404.
- Location filtering is client-side: remote jobs list `Remoto` as the country, not a
  specific nation, so combining `--remote` with a country `--location` yields nothing.
