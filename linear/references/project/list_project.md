---
name: list-projects
description: List open Linear projects.
---

# List projects

Atomic operation used by the `LIST PROJECTS WORKFLOW` and `CREATE PROJECT WORKFLOW` in `linear/SKILL.md`.

Retrieve all Linear projects available to the user, handling pagination if the API returns pages. Return projects that are not closed, completed, cancelled, or archived. Do not compare project names, notify the user, or decide how the results should be used.

Invoke:

```text
mcp__codex_apps__linear_list_projects({
  includeArchived: false,
  limit: 50,
  fields: ["id", "name", "summary", "description", "url", "status", "lead", "teams"]
})
```

Return the project records needed by the caller, including the project ID and name, plus any available status, description, lead, and URL fields.
