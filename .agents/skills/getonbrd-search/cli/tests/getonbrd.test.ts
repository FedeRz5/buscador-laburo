import { test, expect } from "bun:test"
import { runCLI, parseJSON } from "./helpers.js"

interface SearchResult {
  meta: { count: number; page: number }
  results: Array<{ id: string; title: string; company: string | null; location: string | null; date: string | null; url: string }>
}

test("search --category design-ux returns real results with core fields", async () => {
  const res = await runCLI(["search", "--category", "design-ux", "--limit", "5", "--format", "json"])
  const data = parseJSON<SearchResult>(res)
  expect(Array.isArray(data.results)).toBe(true)
  expect(data.results.length).toBeGreaterThan(0)
  const first = data.results[0]
  expect(typeof first.id).toBe("string")
  expect(first.id.length).toBeGreaterThan(0)
  expect(typeof first.title).toBe("string")
  expect(first.title.length).toBeGreaterThan(0)
  expect(first.url).toContain("getonbrd.com")
}, 30000)

test("search with no query and no category exits 1 with a JSON error on stderr", async () => {
  const res = await runCLI(["search", "--format", "json"])
  expect(res.exitCode).toBe(1)
  const err = JSON.parse(res.stderr)
  expect(err.code).toBe("NO_QUERY_OR_CATEGORY")
})

test("unknown command exits 1 with a JSON error on stderr", async () => {
  const res = await runCLI(["frobnicate"])
  expect(res.exitCode).toBe(1)
  const err = JSON.parse(res.stderr)
  expect(err.code).toBe("BAD_CMD")
})
