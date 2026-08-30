---
name: get-milestone
description: Retrieve one milestone from a Linear project.
---

# Get a milestone

Atomic operation used by the `ISSUE TO MILESTONE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_get_milestone({
  project: project,
  query: milestone
})
```

`project` identifies the Linear project. `milestone` is the milestone name or ID. Return the specific milestone or the connector’s not-found result.
