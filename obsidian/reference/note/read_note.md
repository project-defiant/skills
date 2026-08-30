# Read an existing Markdown note

Read the contents of one Markdown note from an explicitly selected vault. This is a single, read-only CLI operation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` as the first parameter.
- The caller has already established that the exact vault-relative `.md` path exists.
- Use `path`, not the active file, to identify the target.

## Command

```bash
obsidian vault="My Vault" read path="Projects/Plan.md"
```

## Output

Return the note content exactly as emitted by the CLI to the upstream workflow. Do not edit, open, search, or otherwise transform the note as part of this operation.

## Out of scope

This reference does not discover files, resolve ambiguous names, read non-Markdown files, or perform any mutation.
