#!/usr/bin/env bun
// Self-contained CLI for searching jobs on Get on Board (getonbrd.com), the LatAm
// tech & design job board, via its PUBLIC API. Zero runtime dependencies — runs
// anywhere `bun` is available.
//
// The public API is sanctioned for reading the same data visible without login.
// Keep volume low; the single-job endpoint is paywalled, so `detail` reads the
// public job page.

import { runSearch, type SearchOpts } from "./commands/search.js"
import { runDetail, type DetailOpts } from "./commands/detail.js"

interface Flags {
  _: string[]
  [k: string]: string | boolean | string[]
}

function parseFlags(argv: string[]): Flags {
  const flags: Flags = { _: [] }
  const alias: Record<string, string> = { q: "query", l: "location", n: "limit", c: "category" }
  const boolFlags = new Set(["remote", "help", "h"])
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a.startsWith("-")) {
      const key = alias[a.replace(/^-+/, "")] ?? a.replace(/^-+/, "")
      const next = argv[i + 1]
      if (boolFlags.has(key) || next === undefined || next.startsWith("-")) {
        flags[key] = true
      } else {
        flags[key] = next
        i++
      }
    } else {
      ;(flags._ as string[]).push(a)
    }
  }
  return flags
}

const HELP = `getonbrd-cli — search jobs on Get on Board (getonbrd.com), LatAm tech & design, remote-friendly

USAGE
  bun run src/cli.ts search --location "Argentina" [--category <id>] [--query "<text>"] [flags]
  bun run src/cli.ts detail <slug|url> [--format json|plain]

SEARCH FLAGS
  --category, -c <id>   Browse a category (recommended for a focused field).
                        e.g. design-ux, programming, data-science-analytics, sysadmin-devops-qa
  --query, -q <text>    Full-text keyword search. Use alone, or with --category to
                        narrow that category by title.
  --location, -l <text> Client-side filter on country/remote, e.g. "Argentina", "Remote".
  --remote              Only fully remote roles.
  --jobage <days>       Posted within N days (client-side). Default: all.
  --page <n>            1-indexed page. Default 1.
  --limit, -n <n>       Cap results emitted (also sets page size). Default 20.
  --format <fmt>        json (default) | table | plain.

  (Provide --category or --query, or both.)

EXAMPLES
  bun run src/cli.ts search --location "Argentina" --category design-ux --limit 15 --format table
  bun run src/cli.ts search --category design-ux --remote --location "Argentina" --format table
  bun run src/cli.ts search --location "Argentina" --query "product designer" --format table
  bun run src/cli.ts search --location "Argentina" -c design-ux -q "ui" --jobage 30 --format table
  bun run src/cli.ts detail product-designer-lemontech-santiago-441b --format plain

Public API (getonbrd.com/api). Personal use, keep volume low.
`

async function main(): Promise<number> {
  const argv = process.argv.slice(2)
  const flags = parseFlags(argv)
  const cmd = (flags._ as string[])[0]

  if (!cmd || flags.help || flags.h) {
    process.stdout.write(HELP)
    return cmd ? 0 : 1
  }

  if (cmd === "search") {
    const query = typeof flags.query === "string" ? flags.query : undefined
    const category = typeof flags.category === "string" ? flags.category : undefined
    if (!query && !category) {
      process.stderr.write(
        JSON.stringify({
          error: 'provide --category <id> (e.g. -c design-ux) or --query "<text>"',
          code: "NO_QUERY_OR_CATEGORY",
        }) + "\n",
      )
      return 1
    }
    const fmt = (flags.format as string) || "json"

    const parseIntFlag = (name: string, raw: string | boolean | string[]): number | null => {
      const val = parseInt(raw as string, 10)
      if (isNaN(val)) {
        process.stderr.write(JSON.stringify({ error: `--${name} must be a number, got "${raw}"`, code: "BAD_ARG" }) + "\n")
        return null
      }
      return val
    }

    for (const f of ["jobage", "page", "limit"] as const) {
      if (flags[f] !== undefined && flags[f] !== true) {
        const v = parseIntFlag(f, flags[f])
        if (v === null) return 1
        flags[f] = String(v)
      }
    }

    const opts: SearchOpts = {
      query,
      category,
      location: typeof flags.location === "string" ? flags.location : undefined,
      remote: flags.remote === true,
      jobage: flags.jobage && flags.jobage !== true ? parseInt(flags.jobage as string, 10) : 9999,
      page: flags.page && flags.page !== true ? Math.max(1, parseInt(flags.page as string, 10)) : 1,
      limit: flags.limit && flags.limit !== true ? parseInt(flags.limit as string, 10) : undefined,
      format: (["json", "table", "plain"].includes(fmt) ? fmt : "json") as SearchOpts["format"],
    }
    return runSearch(opts)
  }

  if (cmd === "detail") {
    const id = (flags._ as string[])[1]
    if (!id) {
      process.stderr.write(JSON.stringify({ error: "detail requires a <slug|url>", code: "NO_ID" }) + "\n")
      return 1
    }
    const fmt = (flags.format as string) || "json"
    const opts: DetailOpts = { id, format: (fmt === "plain" ? "plain" : "json") as DetailOpts["format"] }
    return runDetail(opts)
  }

  process.stderr.write(JSON.stringify({ error: `Unknown command "${cmd}"`, code: "BAD_CMD" }) + "\n")
  return 1
}

main().then((code) => process.exit(code))
