---
name: vault
description: Operate the user's Obsidian project wiki at $SZYMON_WIKI, including project navigation, Bases, queries, and linting. Use for requests about the Wiki, Obsidian project records, or project Bases that do not specifically create requirements, PRDs, meetings, or research notes.
---

# Obsidian project wiki

## Scope and prerequisites

- `$SZYMON_WIKI` must name the Wiki directory. If it is unset, stop and ask the user to configure it.
- Project folders are under `$SZYMON_WIKI/Projects/`.
- Source and topic notes use the sibling directories `$SZYMON_WIKI/../Source-notes/` and `$SZYMON_WIKI/../Topic-notes/`. Do not introduce another root variable.
- Use `rg` for file discovery.
- Before using Obsidian's CLI, read [obsidian-cli.md](references/obsidian-cli.md). Before creating or changing a `.base` file, read [obsidian-bases.md](references/obsidian-bases.md). Read [project-schema.md](references/project-schema.md) before interpreting or changing project metadata.

## Project model

`requirements.md` is the living definition of a project. Each file in `PRDs/` records one implementation phase. `log.md` is append-only and records only creation or updates of requirements and PRDs. `project.base` is the navigational view of the project.

Historical files and folders are preserved. Do not migrate, delete, or rewrite an existing project unless the user explicitly asks to port that project.

Linear is the canonical record for a project's implementation issues. The only Linear data stored in requirements is the raw project URL.

## Persistent updates

Grilling, reading, searching, and drafting are read-only. Before every persistent update, show the target path and a concise description of the exact change, then obtain the user's confirmation.

After an approved change to requirements or a PRD, append the corresponding entry to that project's `log.md`. Do not add global-log entries.

## Routing

Use the specialised skill when its outcome is requested:

| Request | Skill |
| --- | --- |
| Create and scope a Wiki project | `create-project-in-wiki` |
| Transfer knowledge into or revise requirements | `update-project-requirements` |
| Transfer an implementation discussion into a PRD | `to-prd` |
| Plan and create implementation issues in Linear from a PRD | `to-issues` |
| Add an item to today's project meeting summary | `from-meeting` |
| Review a publication and create a source note | `create-source-note` |
| Create a note for a user-selected research concept | `create-topic-note` |

For a Wiki query or lint request, read [query-lint.md](references/query-lint.md) before acting.
