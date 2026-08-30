---
name: create-milestone
description: Create one milestone in a Linear project.
---

# Create a milestone

Atomic operation used by the `CREATE MILESTONE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_save_milestone({
  project: project,
  name: name,
  description: content,
  targetDate: targetDate
})
```

Required inputs:

- `project` — the resolved Linear project name, ID, identifier, or slug.
- `name` — the milestone name.

Optional inputs:

- `content` — the free-form milestone description.
- `targetDate` — the target completion date in ISO format.

Create exactly one milestone and return the created milestone. Do not perform duplicate checks, ask questions, or make workflow decisions.
