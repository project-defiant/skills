# Lint project

Isolated read-only project-structure validation task used by the `lint-project` workflow.

This task does not resolve projects, notify the user, ask for confirmation, or repair files.

## Function

```text
lint-project(vault, project)
```

- `vault`: explicit Obsidian vault name or ID.
- `project`: resolved project object containing `name` and `path`.

## Preconditions

- `vault` and a resolved `project` are present.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- Use exact vault-relative paths and never use the active vault.

## Task

1. Set `project_path = project.path`.
2. List Markdown files under the project path:

   ```bash
   obsidian vault="$vault" files folder="$project_path" ext=md
   ```

3. Compare the returned paths with the canonical structure in `project_structure.md`.

Required files:

```text
log.md
requirements.md
meetings.md
```

Allowed additional files are PRD documents matching:

```text
PRD/YYYY-MM-DD-{prd-name}.md
```

Report required files that are absent in `missing`. Report files outside the required paths and valid PRD paths in `unexpected`. An empty `PRD/` folder is not an issue because folders are not listed or created independently by Obsidian CLI.

## Output

```json
{
  "project": {
    "name": "Project Name",
    "path": "Projects/Project Name"
  },
  "valid": false,
  "missing": [
    "meetings.md"
  ],
  "unexpected": [
    "notes.md"
  ]
}
```

Return `valid: true` only when both `missing` and `unexpected` are empty. Paths in `missing` and `unexpected` are relative to the project path.

## Output schema

```json
{
  "type": "object",
  "required": ["project", "valid", "missing", "unexpected"],
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
    "valid": { "type": "boolean" },
    "missing": {
      "type": "array",
      "items": { "type": "string" }
    },
    "unexpected": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
```
