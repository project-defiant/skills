---
name: create-issue
description: Create one Linear issue in a project.
---

# Create an issue

Atomic operation used by the `CREATE ISSUE WORKFLOW` in `linear/SKILL.md`.

Invoke:

```text
mcp__codex_apps__linear_save_issue({
  title: title,
  description: content,
  team: "Szymon",
  assignee: "Szymon Szyszkowski",
  project: project,
  milestone: milestone,
  dueDate: dueDate,
  priority: priority,
  state: status,
  blockedBy: blockedBy,
  blocks: blocks
})
```

Required inputs:

- `title` — the issue title.
- `team` — always `Szymon`.

Optional inputs:

- `description` — free-form issue content.
- `project` — the target Linear project.
- `milestone` — the target milestone.
- `dueDate` — an ISO date.
- `priority` — `0` None, `1` Urgent, `2` High, `3` Medium, or `4` Low.
- `state` — a valid issue status for the Szymon team.
- `blockedBy` — optional array of existing Linear issue IDs or identifiers that block this issue.
- `blocks` — optional array of existing Linear issue IDs or identifiers that this issue blocks.

Always set `assignee` to Szymon Szyszkowski. Create exactly one issue and return the created issue. Do not perform duplicate checks, ask questions, or make workflow decisions.
