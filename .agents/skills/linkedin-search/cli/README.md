# linkedin-cli

En este proyecto, usá Argentina como país: agregá `--location "Argentina"` al ejecutar búsquedas directas. La entrada recomendada es `python buscar.py "PUESTO"` desde la raíz.


Guía de uso en español de Argentina: [Cómo buscar trabajo en LinkedIn](../../../../LINKEDIN.md).

CLI for searching jobs on LinkedIn's public job listings, for **any country/region**
(and remote), across any sector.

**Data source**: LinkedIn `jobs-guest` endpoints (`seeMoreJobPostings/search` and `jobPosting/<id>`).
**Authentication**: None required.
**Dependencies**: None (plain `bun` + `fetch`). `bun install` is optional and only pulls dev type defs.

> **Personal use only.** This uses LinkedIn's public job pages; automated access is against
> LinkedIn's Terms of Service. Keep volume low, don't use it commercially or for bulk data
> collection, and run it on your own responsibility.

## Installation

```bash
cd .agents/skills/linkedin-search/cli
bun install   # optional — only installs TypeScript dev types
```

The CLI runs without any install because it has zero runtime dependencies.

## Commands

| Command | Description |
|---------|-------------|
| `search` | Search for job listings (`--location` required) |
| `detail` | Fetch full detail for a single job listing |

`search` accepts `--format json|table|plain` (default `json`); `detail` accepts `--format json|plain`.
All errors are written to **stderr** as `{ "error": "...", "code": "..." }` with exit code `1`.

## Quick examples

```bash
# Puestos de software en La Plata, últimos 7 días
bun run src/cli.ts search -q "backend engineer" -l "La Plata, Argentina" --jobage 7 --format table

# Puestos de diseño en Rosario
bun run src/cli.ts search -q "product designer" -l "Rosario, Argentina" --format table

# Fully remote
bun run src/cli.ts search -q "technical writer" -l "Argentina" --remote remote --format table

# Full detail for one job
bun run src/cli.ts detail 4426311357 --format plain
```

See `../SKILL.md` for the full flag reference and the Terms-of-Service note.

## Search flags

| Flag | Alias | Description |
|------|-------|-------------|
| `--location` | `-l` | **Required.** Place string, e.g. `"Buenos Aires, Argentina"`, `"Córdoba, Argentina"`, `"Remote"`. |
| `--query` | `-q` | Keywords (title / skill / role). Recommended. |
| `--jobage` | | Posted within N days: `1`, `7`, `14`, `30`. |
| `--remote` | | `remote` \| `hybrid` \| `onsite`. |
| `--page` | | 1-indexed page (10 results/page). |
| `--limit` | `-n` | Cap results emitted. |
| `--format` | | `json` \| `table` \| `plain`. |
