---
name: update-project-requirements
description: Transfer explicitly selected discussion into an existing project's requirements.md in the Obsidian Wiki. Use when the user asks to update project requirements or transfer grilled knowledge to requirements.
---

# Update project requirements

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` before acting.

1. Resolve the project and read its existing `requirements.md`.
2. Extract only the information the user explicitly asks to transfer. Preserve unrelated content and do not infer new decisions.
3. Show a concise, section-by-section proposed delta and the target path.
4. Obtain approval before writing.
5. Update `requirements.md`, including its `updated` date, and append one concise entry to `log.md`.
6. Confirm that Base filters still expose the requirements note. Do not alter the Base unless the user approves a Base update.

If the project is absent, route to `create-project-in-wiki` rather than creating partial files here.
