# Prepend content to an existing Markdown note

Prepend supplied content to one existing Markdown note. This is one mutation and must not be combined with discovery, reading, or another edit.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact vault-relative `.md` path exists.
- The caller supplies the exact content to prepend.
- Use `path`, never the active file, to identify the target.

## Command

```bash
obsidian vault="My Vault" prepend path="Projects/Plan.md" content="# Summary\n\n"
```

The CLI places prepended content after existing frontmatter. Use `inline` only when the caller explicitly requires no automatic newline. Encode multiline content with `\\n` and tabs with `\\t`.

## Out of scope

This operation does not discover or select a note, replace full note content, append content, update frontmatter, or perform another mutation.
