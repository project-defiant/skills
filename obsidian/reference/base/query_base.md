# Query an existing Base

Query one existing Base definition and return its results. This is one read-only query operation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact vault-relative `.base` path exists.
- The Base already contains the required filters and views. For tag filtering, its filter must use the frontmatter `tags` property.
- The caller supplies any required view name and output format.

## Command

```bash
obsidian vault="My Vault" base:query path="Bases/Projects.base" view="Projects" format=json
```

Use the Base’s existing filters to query by frontmatter tags. Do not use full-text search or change the Base as part of this operation. Confirm available parameters and formats with `obsidian help base:query`.

## Output

Return the query result to the upstream workflow. Prefer `format=json` when supported and suitable for the caller.

## Out of scope

This operation does not create, update, or delete a Base, add an item, design filters, validate Base schema, list tags, or mutate notes.
