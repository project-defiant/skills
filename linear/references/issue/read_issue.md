---
name: read-issue
description: Read one Linear issue within a project.
---

# Read an issue

Atomic operation used by the `READ ISSUE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_get_issue({
  id: issue
})
```

Return the issue record. The workflow resolves the project before this task is called; do not notify the user or make workflow decisions.
