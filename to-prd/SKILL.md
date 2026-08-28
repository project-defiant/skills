---
name: to-prd
description: Transfer an explicitly selected implementation discussion into a new or updated project PRD in the Obsidian Wiki. Use when the user asks to create or update a PRD from a grilling session.
---

# To PRD

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` before acting.

A PRD records one implementation phase. It is created only when the user explicitly asks to transfer a discussion into a new or existing PRD.

## Process

1. Resolve the project and read its `requirements.md`.
2. Identify whether the user requested a new PRD or named an existing PRD to update. Ask if this is unclear.
3. Inspect the relevant codebase when it materially clarifies the implementation boundary, interfaces, or validation approach.
4. Synthesize only implementation decisions already agreed in the conversation and supported by relevant evidence. Do not turn unresolved research into a PRD or invent technical choices.
5. Draft the PRD using this structure:
   - outcome and problem context;
   - scoped deliverables and non-goals;
   - agreed functional and implementation requirements;
   - validation and testing decisions;
   - dependencies and constraints.
6. Show the target path and a concise draft summary. Obtain approval before writing.
7. For a new PRD, create `PRDs/YYYY-MM-DD-{slug}.md`; for an update, change only the selected PRD.
8. Append one matching entry to `log.md`.
9. Confirm that the project's Base will surface the PRD through its filters; repair the Base only with separate approval.

Linear issue planning begins only when the user asks to use `to-issues`.
