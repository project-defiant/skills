---
name: create-source-note
description: Interactively review a publication passage by passage and create a user-directed Obsidian source note with PDF annotation links. Use when the user asks to review a publication in the Wiki or on the web.
---

# Create source note

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` before acting.

## Interactive review

1. Locate the publication and its PDF. If a local vault PDF is unavailable, ask the user before importing a PDF or choosing its storage location.
2. Read one paragraph, or one small coherent passage, at a time.
3. Give a short factual summary and its PDF annotation link. Wait for the user's direction before continuing.
4. The user decides which findings matter, whether to examine supplementary material, and whether a concept should become a topic note. Do not make those choices on the user's behalf.

## Persisting a source note

Create a note only when the user explicitly asks. Name it `{Last author surname} {publication year}.md` under `$SZYMON_WIKI/../Source-notes/`.

Before writing, show the note title, path, metadata, and selected content for approval. Include complete publication metadata: title, authors, last author, publication date, year, journal, DOI, URL, PDF link, tags, and project identifiers.

Use this body structure:

```markdown
# Citation

## Summary

## Findings

## Limitations

## Benchmarks

> [!definition]
> …

> [!claim]
> …
```

Every source-derived statement ends with an Obsidian link to its exact PDF annotation or selection. Do not replace those links with plain citation text. Do not update a project `log.md`.
