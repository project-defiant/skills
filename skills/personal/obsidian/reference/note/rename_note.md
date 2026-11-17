# Rename an existing Markdown note

Rename one existing Markdown note without moving it. This is one mutation and must not be combined with discovery or another operation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact source `.md` path exists.
- The caller has already established that the new name does not create an unintended collision.
- Use `path` to identify the existing note; supply only the new basename in `name`.

## Command

```bash
obsidian vault="My Vault" rename path="Projects/Plan.md" name="Project Plan.md"
```

Obsidian preserves the file extension when it is omitted from the new name and may update internal links according to the vault’s configured link-update setting.

## Out of scope

This operation does not discover a source, move the note to another folder, or perform another mutation.
