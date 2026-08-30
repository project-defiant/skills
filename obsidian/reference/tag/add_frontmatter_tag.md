# Add a tag to existing note frontmatter

Set the frontmatter `tags` property on one existing Markdown note to the complete resulting tag list supplied by the caller. This is one property mutation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact vault-relative `.md` path exists.
- The upstream workflow has read the existing frontmatter, preserved every existing property, added the requested tag, and removed duplicates.
- The caller supplies the complete resulting `tags` value.
- Use `path`, never the active file, to identify the target.

## Command

```bash
obsidian vault="My Vault" property:set path="Projects/Plan.md" name=tags value="project,active" type=list
```

The exact list-value syntax is version-sensitive. Confirm it with `obsidian help property:set` and pass the complete resulting list in the syntax accepted by the installed CLI. Do not use an inline `#tag` or content append.

## Output and limits

Return the CLI result to the upstream workflow. This primitive does not read the note, discover tags, query note content, query a Base, or perform a second operation. The upstream workflow is responsible for verifying that other frontmatter and note content remain unchanged.
