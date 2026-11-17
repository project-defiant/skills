# Create a new Markdown note

Create one new Markdown note at an exact path. This is one mutation and must not be combined with discovery, validation, or another operation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact destination path does not exist.
- The destination has a `.md` extension.
- The caller supplies the exact initial content.

## Command

```bash
obsidian vault="My Vault" create path="Projects/New Plan.md" content="# New Plan\n"
```

Do not use the `overwrite` flag. Template expansion, opening the note, and creating a new tab are out of scope.

## Out of scope

This operation does not list files, resolve collisions, update an existing note, or create non-Markdown files.
