---
name: list-milestones
description: List milestones in one Linear project.
---

# List milestones

Atomic operation used by the `CREATE MILESTONE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_list_milestones({
  project: project
})
```

Return the milestones belonging to the specified project. Do not compare names, notify the user, or decide how the results should be used.
