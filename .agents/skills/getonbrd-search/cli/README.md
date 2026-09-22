# getonbrd-search CLI

En este proyecto, usá Argentina como país: agregá `--location "Argentina"` al ejecutar búsquedas directas. La entrada recomendada es `python buscar.py "PUESTO"` desde la raíz.


Search jobs on [Get on Board](https://www.getonbrd.com) (LatAm tech & design job board)
via its **public API**. Zero runtime dependencies — runs with just `bun`.

**Authentication**: None required (public API).

## Install (optional)

Zero runtime deps; `bun install` only pulls TypeScript dev types for `typecheck`.

```bash
cd .agents/skills/getonbrd-search/cli && bun install
```

## Usage

```bash
# Design/UX jobs (recommended: browse the category), human-readable
bun run src/cli.ts search --location "Argentina" --category design-ux --limit 15 --format table

# Fully remote design/UX
bun run src/cli.ts search --location "Argentina" --category design-ux --remote --format table

# Diseño/UX en Argentina
bun run src/cli.ts search --category design-ux --location "Argentina" --format table

# Full-text keyword search
bun run src/cli.ts search --location "Argentina" --query "product designer" --format table

# Full detail of one job
bun run src/cli.ts detail product-designer-lemontech-santiago-441b --format plain
```

Run with no args (or `--help`) for the full flag reference.

## Commands & contract

- `search` and `detail <slug|url>`.
- JSON output: `{ "meta": { "count", "page" }, "results": [ { id, title, company, location, date, url } ] }`.
- Errors go to **stderr** as `{ "error", "code" }`, exit code `1`.

## Design notes

- **Public API**, JSON:API envelope. Company name is resolved via a second public
  endpoint (`/companies/:id`) and cached per run.
- The single-job API endpoint is paywalled (401), so `detail` reads the public job
  page HTML and extracts the `itemprop="description"` body.
- Location/remote/jobage filters are applied client-side (the public search endpoint
  has no direct params for them). See `../url-reference.md`.

## Tests

```bash
bun run typecheck
bun run test        # live smoke test: search --location "Argentina" returns results; error paths exit 1
```
