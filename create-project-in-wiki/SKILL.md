---
name: create-project-in-wiki
description: Interactively scope a new project in the Obsidian Wiki and create its requirements only when the user explicitly transfers the grilled discussion. Use when the user asks to create or scope a Wiki project.
---

# Create project in Wiki

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` and `/Users/ss60/.agents/skills/vault/references/obsidian-bases.md` before acting.

1. Resolve the requested project name and search `$SZYMON_WIKI/Projects/`.
2. If the folder exists, report the exact path and ask what additional information the user wants to consider. Do not overwrite or scaffold a second project.
3. If absent, use `grill-me` to explore the project idea. Grilling is read-only.
4. Wait until the user explicitly asks to transfer the discussion into requirements.
5. Draft `requirements.md`, `log.md`, `Meetings.md`, and `project.base`. Show the proposed paths and concise contents, then obtain approval.
6. Create the project files. Append the initial requirements-created entry to `log.md`.
7. Validate the Base YAML and inspect its rendered views in Obsidian.

Do not create a PRD, Linear project, milestone, or issue as part of project creation.
