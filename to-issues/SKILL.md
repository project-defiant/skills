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
3. Inspect the relevant codebase when it materially affects the issue boundary or acceptance criteria.
4. Draft independently actionable slices. Prefer a narrow end-to-end slice over a horizontal layer split when that makes the outcome testable. Each proposed issue includes a title, purpose, acceptance criteria, dependencies, and type (`AFK` or `HITL`) when that distinction is useful.
5. Present the milestone and breakdown. Grill the user on scope, granularity, dependencies, assignment, deadline, labels, priority, and cycle. Iterate until the user approves.
6. Present the exact Linear changes and obtain explicit approval.
7. Create the approved milestone and issues in dependency order.
8. Report the resulting Linear links and identifiers.

After creation, keep the Wiki record limited to the raw Linear project URL in project requirements. Individual issue details remain in Linear.
