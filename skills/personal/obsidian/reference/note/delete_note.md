# Delete an existing Markdown note to trash

Move one existing Markdown note to Obsidian trash. This is one mutation and must not be combined with discovery or another operation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact vault-relative `.md` path exists.
- Use `path`, never the active file, to identify the target.

## Command

```bash
obsidian vault="My Vault" delete path="Projects/Old Plan.md"
```

Do not pass `permanent`. Permanent deletion is out of scope; the default trash behavior is required.

## Out of scope

This operation does not discover or select a note, permanently delete a file, or perform another mutation.
