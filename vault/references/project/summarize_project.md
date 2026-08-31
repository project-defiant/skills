# Summarize project

Isolated read-only task used by the `read-project` workflow.

This task reads the resolved project files and produces an agent-generated summary. It does not check whether the project exists, notify the user, ask for confirmation, or mutate the Wiki.

## Function

```text
summarize-project(vault, project)
```

- `vault`: explicit Obsidian vault name or ID.
- `project`: resolved project object containing `name` and `path`.

## Preconditions

- `vault` and a resolved `project` are present.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- Use exact vault-relative paths and never use the active vault.

## Task

Set `project_path = project.path`, then list Markdown files under that exact project path:

   ```bash
   obsidian vault="$vault" files folder="$project_path" ext=md
   ```

2. For every returned path, read the note with a separate CLI operation:

   ```bash
   obsidian vault="$vault" read path="$file_path"
   ```

3. Synthesize the contents into a concise narrative. The agent must generate this synthesis and place it in the `summary` field; do not return raw file contents as the summary.

4. Return the exact project identity, the generated summary, and the paths used as sources.

## Successful output

```json
{
  "project": {
    "name": "Project Name",
    "path": "Projects/Project Name"
  },
  "summary": "The project aims to...",
  "files": [
    "Projects/Project Name/requirements.md",
    "Projects/Project Name/log.md",
    "Projects/Project Name/meetings.md"
  ]
}
```

## Output schema

```json
{
  "type": "object",
  "required": ["project", "summary", "files"],
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
    "summary": {
      "type": "string"
    },
    "files": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
```
