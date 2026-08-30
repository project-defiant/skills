---
name: list-issues
description: List issues in a Linear project.
---

# List issues

Atomic operation used by the `CREATE ISSUE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_list_issues({
  project: project
})
```

Return the issues belonging to the specified project. Do not compare titles, notify the user, or decide how the results should be used.
