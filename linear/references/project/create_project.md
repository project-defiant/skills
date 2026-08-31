---
name: create-project
description: Create one Linear project from a name and free-form description.
---

# Create a project

Atomic operation used by the `CREATE PROJECT WORKFLOW` in `linear/SKILL.md`.

## Inputs

- `name` — the Linear project name.
- `content` — the free-form project description. Markdown is allowed.

## Operation

Invoke:

```text
mcp__codex_apps__linear_save_project({
  name: name,
  description: content,
  lead: "Szymon Szyszkowski",
  addTeams: ["Szymon"]
})
```

Create exactly one Linear project using the supplied `name` and `content` as its description.

- Set the project lead to Szymon Szyszkowski.
- Assign the project to the default `Szymon` team (`355211af-d264-497b-afc8-b36c7b6271d6`).
- Do not perform duplicate checks.
- Do not ask the user questions or perform workflow decisions.

Return the created project, including its ID and URL. Propagate Linear API errors to the calling workflow.
