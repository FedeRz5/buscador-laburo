---
name: getonbrd-search
version: 1.0.0
description: >
  Use this skill to search tech and design/UX job listings on Get on Board
  (getonbrd.com) across Latin America and remote roles. Covers Argentina, Chile,
  Uruguay, Mexico, Peru, Colombia and remote-LatAm positions in design, UX/UI,
  product, programming, data, DevOps and more. Trigger phrases: get on board,
  getonbrd, buscar trabajo diseño, empleos UX, diseñador remoto, trabajo remoto
  LatAm, ofertas de diseño, design jobs Latin America, remote design jobs,
  UX/UI jobs, product designer, empleos tech remoto.
context: fork
allowed-tools: Bash(bun run .agents/skills/getonbrd-search/cli/src/cli.ts *)
---

# Get on Board Search Skill

Search live job listings from **Get on Board** (getonbrd.com), the Latin-American
tech and design job board, via its **public API**. Strong for **design/UX** and
**remote LatAm** roles (Argentina, Chile, Uruguay, Mexico, and remote). Zero runtime
dependencies — runs with just `bun`.

> Country-agnostic within LatAm: results come structured (company, remote modality,
> salary range, seniority) because they come from Get on Board's public JSON API,
> not HTML scraping.

## Data source & fair use

This uses Get on Board's **public API** (`getonbrd.com/api`), which the platform
documents as open and which returns the same data visible on the site without
logging in (categories, company profiles, published jobs). Keep volume low and for
personal use. The single-job API endpoint is paywalled, so `detail` reads the
public job page instead.

## When to use this skill

- Find **design / UX** roles in LatAm or remote (this is the strongest category here)
- Find tech roles (programming, data, DevOps, product) in a specific LatAm country or remote
- Filter to fully remote roles, or to a country (Chile, Argentina, Uruguay, …)
- Read a specific job's full description

## Commands

### Search job listings

```bash
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search [--category <id>] [--query "<text>"] [flags]
```

Provide **`--category`** (recommended for a focused field) **or** `--query`, or both.

Key flags:
- `--category <id>` / `-c <id>` — browse a category. Best signal for a field. Common ids:
  `design-ux`, `programming`, `data-science-analytics`, `machine-learning-ai`,
  `sysadmin-devops-qa`, `sales`. (List all: see `url-reference.md`.)
- `--query <text>` / `-q <text>` — full-text keyword search. Alone it hits the search
  endpoint; combined with `--category` it narrows that category by title.
- `--location <text>` / `-l <text>` — client-side filter on country/remote, e.g. `"Chile"`, `"Remote"`.
- `--remote` — only fully-remote roles.
- `--jobage <days>` — posted within N days (client-side filter).
- `--page <n>` — 1-indexed page.
- `--limit <n>` / `-n <n>` — cap results (also sets page size). Default 20.
- `--format json|table|plain` — default `json`.

### Fetch full job detail

```bash
bun run .agents/skills/getonbrd-search/cli/src/cli.ts detail <slug|url> [--format json|plain]
```

`slug` is the `id` from search results (e.g. `product-designer-lemontech-santiago-441b`).
A full `getonbrd.com/jobs/...` URL also works. Returns the full description text.

## Usage examples

```bash
# All Design/UX jobs, most recent, human-readable
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --category design-ux --limit 15 --format table

# Design/UX, fully remote only
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --category design-ux --remote --limit 15 --format table

# Design/UX based in Chile
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --category design-ux --location "Chile" --format table

# Narrow a category by keyword (UI roles within Design/UX, last 30 days)
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search -c design-ux -q "ui" --jobage 30 --format table

# Full-text search across all categories
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search -q "product designer" --format table

# Full detail for a specific job
bun run .agents/skills/getonbrd-search/cli/src/cli.ts detail product-designer-lemontech-santiago-441b --format plain
```

## Output formats

| Format | Best for |
|--------|----------|
| `json` | Default — programmatic use, passing the `id`/`url` to `detail` |
| `table` | Quick human-readable scanning |
| `plain` | Reading a single job's full detail (`detail` command) |

All errors are written to **stderr** as `{ "error": "...", "code": "..." }` with exit code `1`.

## Notes

- Data is from Get on Board's public API — company name is resolved via a second
  public endpoint (`/companies/:id`), cached per run.
- **Location filtering is client-side and coarse.** Fully-remote postings list their
  country as `Remoto`, not a specific country, so `--location "Chile" --remote` will
  usually return nothing — use `--location "Chile"` (which returns Chile-based roles)
  or `--remote` (any remote), not both.
- `--jobage` is a client-side filter on the posting's published date.
- The single-job API endpoint requires a paid key (401), so `detail` reads the public
  job page HTML and extracts the description from its schema.org microdata.
- Salary ranges (when present) are USD and available in the raw API; the table view
  omits them for width.
