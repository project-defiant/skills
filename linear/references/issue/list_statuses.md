---
name: list-issue-statuses
description: List available issue statuses for a Linear team.
---

# List issue statuses

Atomic operation used by the `CREATE ISSUE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_list_issue_statuses({
  team: team
})
```

Return the issue statuses available to the specified team. Do not select a status, notify the user, or make workflow decisions.
