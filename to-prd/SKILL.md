---
name: to-prd
description: Transfer an explicitly selected implementation discussion into a new or updated project PRD in the Obsidian Wiki. Use when the user asks to create or update a PRD from a grilling session.
---

# To PRD

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` before acting.

A PRD represents one implementation phase. It is not created merely because a grilling session ended; the user must explicitly ask to create or update one.

## Process

1. Resolve the project and read its `requirements.md`.
2. Identify whether the user requested a new PRD or named an existing PRD to update. If this is unclear, ask.
3. Synthesize only the implementation decisions already agreed in the current conversation and relevant codebase evidence. Do not turn unresolved research into requirements or invent technical choices.
4. Draft the proposed PRD, including outcome, scope, deliverables, implementation decisions, validation, dependencies, and non-goals.
5. Show the target path and concise draft summary. Obtain approval before writing.
6. For a new PRD, create `PRDs/YYYY-MM-DD-{slug}.md`. For an update, change only the selected PRD.
7. Append one matching entry to `log.md`.
8. Confirm that the project's Base will surface the PRD through its filters; repair the Base only with separate approval.

Linear issue planning begins only when the user asks to use `to-issues`.
