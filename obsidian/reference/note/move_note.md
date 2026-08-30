# Move an existing Markdown note

Move one existing Markdown note to the exact destination supplied by the caller. This is one mutation and must not be combined with discovery or another operation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact source `.md` path exists.
- The caller has already established that the destination is valid and does not create an unintended collision.
- Use exact vault-relative paths for both source and destination.

## Command

```bash
obsidian vault="My Vault" move path="Projects/Plan.md" to="Archive/Plan.md"
```

Obsidian may update internal links according to the vault’s configured link-update setting.

## Out of scope

This operation does not discover a source, select a destination, rename the note independently, or perform another mutation.
