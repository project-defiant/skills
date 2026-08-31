---
name: issue-to-milestone
description: Assign one existing Linear issue to one existing milestone.
---

# Assign an issue to a milestone

Atomic operation used by the `ISSUE TO MILESTONE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_save_issue({
  id: issue.id,
  project: project,
  milestone: milestone.id
})
```

Assign the issue to the milestone and return the updated issue. Do not change any other issue fields, ask questions, or perform workflow decisions.
