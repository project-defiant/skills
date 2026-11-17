# Search text in Markdown notes

Search text in an explicitly selected vault. This is a single, read-only query operation. The CLI search is vault-wide and does not provide an extension filter; the upstream workflow must ensure that the intended results are Markdown notes and ignore non-`.md` results.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller supplies the exact search query.
- The caller understands that the CLI may return matches outside Markdown notes because search is vault-wide.
- Use `path` only when the caller has already supplied a vault-relative folder to limit the search.

## Search commands

Return matching file paths:

```bash
obsidian vault="My Vault" search query="architecture" path="Projects" limit=20 format=json
```

Return matching lines with file paths and line numbers:

```bash
obsidian vault="My Vault" search:context query="architecture" path="Projects" limit=20 format=json
```

Use `case` only when the caller requires case-sensitive matching. The supported output formats are `format=text` (the default) and `format=json`; use `format=json` for downstream parsing when appropriate.

## Output

Return search results to the upstream workflow. Do not open, select, read, or mutate a note as part of this operation.

## Out of scope

This reference does not list tags, query a Base, add tags, or perform any mutation.
