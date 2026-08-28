---
name: to-issues
description: Turn a selected project PRD into an approved Linear milestone and implementation issues. Use when the user asks to plan or create Linear issues from a PRD.
---

# To Issues

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` before acting. Linear is the canonical issue tracker for this workflow.

## Process

1. Require a selected PRD. Read it and the project's `requirements.md`.
2. Resolve the Linear project from `linear_project`.
   - If it is absent, search for an exact corresponding Linear project.
   - If none exists, ask whether to create it.
   - If several candidates are plausible, ask the user to choose.
   - Once resolved, propose the raw Linear project URL for `requirements.md`; write it and append a requirements log entry only after approval.
3. Draft independently actionable implementation slices. Each should have a title, purpose, acceptance criteria, dependencies, and type (`AFK` or `HITL`) when that distinction is useful.
4. Propose the milestone derived from the PRD and the issue breakdown. Grill the user on scope, granularity, dependencies, assignment, deadline, labels, priority, and cycle.
5. Present the final Linear changes and obtain explicit approval.
6. Create the approved milestone and issues in Linear, in dependency order.
7. Report the resulting Linear links and identifiers to the user.

After creation, keep the Wiki record limited to the raw Linear project URL in project requirements. Individual issue details remain in Linear.
