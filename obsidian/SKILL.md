---
name: obsidian
description: Use the Obsidian CLI for atomic operations on explicitly targeted Markdown notes and Base definitions: list files, search and read notes, create notes, append or prepend content, move, rename, delete to trash, add frontmatter tags, create Base definitions, and query Bases. Use when an upstream workflow has already resolved the exact vault and target path.
---

# Obsidian CLI atomic operations

Use this skill only for one CLI operation at a time. It is a primitive layer for upstream workflows; it does not discover targets, choose files, sequence commands, validate content, or ask the user for permission.

## Non-negotiable rules

- Require `vault=<name>` or `vault=<id>` as the first parameter on every command.
- Never use the active or open file as an implicit target.
- Before a mutation, the upstream workflow must already know the exact vault-relative path and whether it exists.
- Create only a path known not to exist; read or mutate only a path known to exist.
- Perform exactly one CLI action. Do not combine listing/searching with a mutation.
- Operate only on Markdown notes (`.md`) and Base definitions (`.base`).
- Prefer structured output where the command supports it.
- Treat `obsidian help <command>` as the version-specific source of truth.

## Available atomic operations

- File discovery: [reference/file/list_files.md](reference/file/list_files.md)
- Note reading and text search: [reference/note/read_note.md](reference/note/read_note.md), [reference/query_text.md](reference/query_text.md)
- Note creation: [reference/note/create_note.md](reference/note/create_note.md)
- Note append and prepend: [reference/note/append_note.md](reference/note/append_note.md), [reference/note/prepend_note.md](reference/note/prepend_note.md)
- Note move, rename, and delete-to-trash: [reference/note/move_note.md](reference/note/move_note.md), [reference/note/rename_note.md](reference/note/rename_note.md), [reference/note/delete_note.md](reference/note/delete_note.md)
- Frontmatter tag addition: [reference/tag/add_frontmatter_tag.md](reference/tag/add_frontmatter_tag.md)
- Base definition creation and querying: [reference/base/create_base.md](reference/base/create_base.md), [reference/base/query_base.md](reference/base/query_base.md)

## CLI prerequisites and syntax

The Obsidian application must be running and the CLI must be enabled and registered. Use `vault=<name>` or `vault=<id>` first, then the command. Parameters use `name=value`; flags do not take values. Quote values containing spaces and encode multiline content with `\\n` and `\\t`.

Mutations in this skill do not request confirmation. Their safety comes from the upstream workflow’s preconditions and exact paths. Deletion means moving a note to Obsidian trash; permanent deletion is not supported.

Adding a tag means updating only the existing note’s YAML frontmatter `tags` property. It must preserve the rest of the note and avoid duplicates. Tag filtering means querying an existing Base using that frontmatter property; it does not mean searching note content.

Creating a Base means creating a new `.base` definition file. It does not mean using `base:create` to add an item to an existing Base.

## Out of scope

This skill does not handle bookmarks, tag counts, inline tags, tasks, daily notes, templates, plugin or theme development, JSON Canvas, Defuddle, Base item creation, Base update or deletion, or full-content note replacement.

References: [official Obsidian CLI documentation](https://obsidian.md/help/cli).
