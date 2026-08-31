# Create project requirements

Atomic requirements-note creation task.

## Function

```text
create-project-requirements(vault, project_path, content)
```

Create exactly `{project_path}/requirements.md` with the supplied complete Markdown content using one Obsidian CLI `create` operation. The caller must provide the exact resolved project path and establish that the target does not exist. Return success or failure only. Do not list projects, confirm, or make workflow decisions.
