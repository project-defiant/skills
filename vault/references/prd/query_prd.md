# Query PRD

Isolated immutable PRD read task used by PRD workflows.

This task reads one exact PRD and returns its contents unchanged. It does not resolve projects, select a PRD, summarize content, ask for confirmation, or mutate the Wiki.

## Function

```text
query-prd(vault, prd_path)
```

- `vault`: vault root directory (`$SZYMON_WIKI`).
- `prd_path`: exact vault-relative path to an existing Markdown PRD.

## Preconditions

- `vault` and `prd_path` are present.
- `prd_path` ends with `.md` and is under a project `PRD/` folder.
- The exact PRD path exists.
- `$SZYMON_WIKI` resolves to the vault root directory.
- Use the explicit vault and exact path.

## Task

Read the exact immutable PRD with one file operation:

```bash
cat "$vault/$prd_path"
```

Return the Markdown content exactly as stored on disk. Do not summarize, transform, or rewrite it.
