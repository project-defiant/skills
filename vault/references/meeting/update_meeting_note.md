# Update meeting note

Isolated in-place meeting-note mutation task used by the `update-meeting-note` workflow.

This task does not resolve projects, list files, ask for confirmation, notify the user, or log a separate project update.

## Function

```text
update-meeting-note(vault, project, meeting, date, context)
```

- `vault`: explicit Obsidian vault name or ID.
- `project`: resolved Wiki project object containing `path`.
- `meeting`: meeting title.
- `date`: meeting date in `YYYY-MM-DD` format.
- `context`: information from the meeting used to prepare the summary.

## Preconditions

- All inputs are present.
- `Projects/{project_name}/meetings.md` already exists.
- The caller has already resolved the project and received user confirmation.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- Use the explicit vault and exact vault-relative paths.

## Task

1. Set `project_path = project.path`.
2. Generate a concise `meeting_summary` from `context`. Do not copy the context verbatim.
3. Append one dated meeting entry to the existing note:

   ```bash
   obsidian vault="$vault" append \
     path="$project_path/meetings.md" \
     content="### $date — $meeting\n\n$meeting_summary"
   ```

Preserve all existing meeting summaries and use exactly one Obsidian CLI mutation.

## Result

- Return `success` when the append completes.
- Return `failure` when the Obsidian CLI operation fails.
