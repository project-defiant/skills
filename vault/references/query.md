# Mode: query

Answer a question against the wiki using the Karpathy pattern: catalog first (`$SZYMON_WIKI/index.md`), then targeted search (ripgrep), then LLM synthesis with citations.

## Inputs

- **question** (required): the user's query.

## Steps

1. **Read the catalog**: `$SZYMON_WIKI/index.md`. Extract the list of projects and any queries already filed.
2. **Read per-project index files that look relevant** (based on the question's noun phrases): `$SZYMON_WIKI/Projects/{X}/index.md`.
3. **Ripgrep**: for each salient keyword from the question, run
   `rg -l -i "{keyword}" "$SZYMON_WIKI"`
   (fall back to `grep -r -l -i "{keyword}" "$SZYMON_WIKI"` if `rg` is missing).
4. **KB fallback**: if the question is conceptual (e.g. "what is X", "explain Y") AND no strong Wiki/ hits, ALSO ripgrep `/Users/ss60/Documents/v/KnowledgeBase/` READ-ONLY. Note any hits from there for the copy-on-first-use offer in step 8.
5. **Shortlist**: pick the top ~10 candidate files, preferring `index.md`, `log.md`, `CHANGELOG.md`, summaries, and recent status snapshots.
6. **Read the shortlist** with the Read tool.
7. **Synthesise**:
   - Write a plain-prose answer.
   - Cite every claim with `[[wikilink]]` back to the source page(s).
   - Do NOT include claims that no cited page supports. If the answer is thin, say so.
8. **KB copy-on-first-use offer**: for each match found in step 4 that is NOT already in `$SZYMON_WIKI/KnowledgeBase/`:
   > Found `[[{page-name}]]` in the wider vault's KnowledgeBase (at `{path}`). Copy into the wiki so future queries can cite it directly? (y/N)
   On yes: copy the file preserving its subpath (e.g. `Statistics/Bayes theorem.md` → `$SZYMON_WIKI/KnowledgeBase/Statistics/Bayes theorem.md`).
9. **File-back offer** (Karpathy's compounding step). After presenting the synthesis, ask:
   > File this answer as `$SZYMON_WIKI/KnowledgeBase/queries/YYYY-MM-DD-{slug}.md`? (y/N)
   Default is NO. On yes:
   - Derive `slug` from the question (short, dash-separated).
   - Write the file using the template below.
   - Add `- [[YYYY-MM-DD-{slug}]] — {short question}` under `## Queries` in `$SZYMON_WIKI/index.md`.
   - Append to `$SZYMON_WIKI/log.md`:
     `- YYYY-MM-DD HH:MM — query — {short question} — [[YYYY-MM-DD-{slug}]]`

## Template — filed query answer

### `$SZYMON_WIKI/KnowledgeBase/queries/YYYY-MM-DD-{slug}.md`

~~~
---
title: {question}
kind: query
asked_at: {YYYY-MM-DD HH:MM}
tags: []
---

# {question}

{synthesised answer with [[wikilinks]] to sources}

## Sources cited

- [[source-1]]
- [[source-2]]
~~~

## Notes

- Never fabricate citations. A wikilink in the answer must point to a file you actually read in step 6.
- Query mode is read-only by default. Files are only created in step 8 (KB copy) and step 9 (file-back), both gated on explicit user consent.
- If ripgrep finds zero hits AND `$SZYMON_WIKI/index.md` yields no leads, say so plainly and suggest ingest-source or project-init to fill the gap.
