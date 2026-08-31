---
name: update-issue
description: Update one existing Linear issue.
---

# Update an issue

Atomic operation used by the `UPDATE ISSUE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_save_issue({
  id: issue.id,
  ...changes
})
```

`changes` may contain supported Linear issue fields such as `description`, `state`, `priority`, `dueDate`, `milestone`, `project`, `assignee`, `blockedBy`, or `blocks`. `blockedBy` and `blocks` accept arrays of existing Linear issue IDs or identifiers. Update only the requested fields and return the updated issue. Do not ask questions or make workflow decisions.
