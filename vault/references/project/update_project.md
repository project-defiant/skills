# Update project

Isolated in-place project update task used by the `update-project` workflow.

This task does not list or resolve projects, read project summaries, ask for confirmation, or decide whether the workflow should continue.

## Function

```text
update-project(vault, project, changes)
```

`changes` must identify one existing Markdown file and the exact content to append:

```json
{
  "path": "Projects/Project Name/requirements.md",
  "content": "\n## New requirement\n..."
}
```

## Preconditions

- `vault` and a resolved `project` are present.
- `changes.path` is an exact vault-relative path inside `project.path`.
- The target Markdown file already exists.
- The caller has already confirmed the proposed change.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- Use the explicit vault and never the active file.
- Do not replace full note content or use `overwrite`.

## Task

Append the supplied content to the existing target note with one Obsidian CLI operation:

```bash
obsidian vault="$vault" append \
  path="$changes_path" \
  content="$changes_content"
```

Preserve all existing frontmatter, headers, and entries. Use `inline` only when explicitly requested by the caller.

## Successful output

```json
{
  "project": {
    "name": "Project Name",
    "path": "Projects/Project Name"
  },
  "updated_file": "Projects/Project Name/requirements.md",
  "operation": "append"
}
```

## Output schema

```json
{
  "type": "object",
  "required": ["project", "updated_file", "operation"],
  "properties": {
    "project": {
      "type": "object",
      "required": ["name", "path"],
      "properties": {
        "name": { "type": "string" },
        "path": { "type": "string" }
      },
      "additionalProperties": false
    },
    "updated_file": {
      "type": "string"
    },
    "operation": {
      "const": "append"
    }
  },
  "additionalProperties": false
}
```
