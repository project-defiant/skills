# Create project

Isolated project-scaffolding task invoked by the `create-project` workflow in `vault/SKILL.md`.

This task does not list projects, check for duplicates, ask for confirmation, or decide whether the workflow should continue.

## Inputs

```text
create-project(vault, project_name)
```

- `vault`: explicit Obsidian vault name or ID supplied by the user.
- `project_name`: confirmed project folder name.

## Preconditions

- `vault` and `project_name` are present.
- The caller has already confirmed that `Projects/{project_name}/` does not exist.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- Use exact vault-relative paths and never use the active vault.
- Do not use `overwrite`.

## Task

Create these three Markdown notes with exactly the initial content defined by `project_structure.md`:

1. `Projects/{project_name}/log.md`
2. `Projects/{project_name}/requirements.md`
3. `Projects/{project_name}/meetings.md`

Use three separate Obsidian CLI `create` actions, each with `vault=<name|id>` first. Use the current local date for `created` in `requirements.md`.

Do not create an empty `PRD/` folder.

## Successful output

Return:

```json
{
  "project": {
    "name": "Project Name",
    "path": "Projects/Project Name"
  },
  "files": [
    "Projects/Project Name/log.md",
    "Projects/Project Name/requirements.md",
    "Projects/Project Name/meetings.md"
  ]
}
```

The output must conform to this schema:

```json
{
  "type": "object",
  "required": ["project", "files"],
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
    "files": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 3
    }
  },
  "additionalProperties": false
}
```
