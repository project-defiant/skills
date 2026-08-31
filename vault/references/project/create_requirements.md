# Create project requirements

Atomic requirements-note creation task.

## Function

```text
create-project-requirements(vault, project_path, content)
```

Create exactly `{project_path}/requirements.md` with one Obsidian CLI `create` operation. The caller must provide the exact resolved project path and establish that the target does not exist. The initial content must contain the project frontmatter only; do not include Markdown headings, dated entries, a `## Decisions` section, or a second frontmatter block. Return success or failure only. Do not list projects, confirm, or make workflow decisions.
