---
name: read-issue
description: Read one Linear issue within a project.
---

# Read an issue

Atomic operation used by the `READ ISSUE WORKFLOW` in `linear/SKILL.md`.

Invoke `mcp__codex_apps__linear_list_issues` for the resolved project and locate the requested issue by its ID or identifier. Return the issue record. Do not notify the user or make workflow decisions.
