---
name: get-project
description: Retrieve one specific Linear project.
---

# Get a project

Atomic operation used by the `CREATE MILESTONE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_get_project({
  query: project
})
```

`project` is the project name, ID, identifier, or slug. Return the specific project record. If no project exists, return the connector’s not-found result to the calling workflow.
