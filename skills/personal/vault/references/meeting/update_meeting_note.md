# Update meeting note

Isolated in-place meeting-note mutation task used by the `update-meeting-note` workflow.

This task does not resolve projects, list files, ask for confirmation, notify the user, or log a separate project update.

## Function

```text
update-meeting-note(vault, project, meeting, date, context)
```

- `vault`: vault root directory (`$SZYMON_WIKI`).
- `project`: resolved Wiki project object containing `path`.
- `meeting`: meeting title.
- `date`: meeting date in `YYYY-MM-DD` format.
- `context`: information from the meeting used to prepare the summary.

## Preconditions

- All inputs are present.
- `Projects/{project_name}/meetings.md` already exists.
- The caller has already resolved the project and received user confirmation.
- `$SZYMON_WIKI` resolves to the vault root directory.
- Use the explicit vault and exact vault-relative paths.

## Task

1. Set `project_path = project.path`.
2. Generate a concise `meeting_summary` from `context`. Do not copy the context verbatim.
3. Append one dated meeting entry to the existing note:

   ```bash
   printf '\n### %s — %s\n\n%s\n' "$date" "$meeting" "$meeting_summary" >> "$vault/$project_path/meetings.md"
   ```

Preserve all existing meeting summaries and use exactly one file mutation.

## Result

- Return `success` when the append completes.
- Return `failure` when the file operation fails.
