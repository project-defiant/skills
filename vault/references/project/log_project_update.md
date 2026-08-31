# Log project update

Isolated in-place log mutation task used by project workflows.

This task does not resolve a project, list files, ask for confirmation, notify the user, or decide whether the calling workflow should continue.

## Function

```text
log-project-update(vault, project_path, context)
```

- `vault`: explicit Obsidian vault name or ID.
- `project_path`: exact project path resolved from conversation context, for example `Projects/Project Name`.
- `context`: information about the completed action or project change.

## Preconditions

- `vault`, `project_path`, and `context` are present.
- `Projects/{project_name}/log.md` already exists.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- The caller has already handled project resolution and confirmation.

## Task

1. Generate a concise `update_content` from `context`. Do not copy the context verbatim.
2. Generate the current local date.
3. Append one entry to the existing log:

   ```bash
   today=$(date +%F)

   obsidian vault="$vault" append \
     path="$project_path/log.md" \
     content="### $today — Update\n\n$update_content"
   ```

Preserve all existing log content and use exactly one Obsidian CLI mutation.

## Result

- Return `success` when the append completes.
- Return `failure` when the Obsidian CLI operation fails.
- Do not return project metadata, file contents, generated content, or a JSON schema.
