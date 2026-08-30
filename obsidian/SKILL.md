---
name: obsidian
description: Provides atomic Obsidian CLI operations for explicitly targeted Markdown notes and Base definitions. Use when an upstream workflow has already resolved the vault, operation, and exact path for listing, searching, reading, creating, appending, prepending, moving, renaming, deleting, tagging, or querying a Base.
---

# Obsidian CLI

Use exactly one mode from the dispatcher table. This skill is a primitive layer: it does not discover targets, choose files, sequence commands, validate content, or ask for permission.

Minimal invocation:

```bash
obsidian vault="My Vault" read path="Projects/Plan.md"
```

## Global constraints

- Put `vault=<name>` or `vault=<id>` first in every command.
- Never use the active vault or active file implicitly.
- Use exact vault-relative paths for file targets.
- The upstream workflow must establish existence before mutation: create requires absent; all other mutations require present.
- Perform exactly one CLI action; never combine discovery, selection, validation, and mutation.
- Operate only on `.md` notes and `.base` definitions.
- Prefer `format=json` where the selected command supports it.
- Use `obsidian help <command>` when installed CLI behavior differs from these references.

## Mode dispatcher

| Mode / trigger | CLI command | Expected parameters | Target precondition | Reference |
|---|---|---|---|---|
| “List notes/Bases/files” | `files` | `vault`, one `ext=md` or `ext=base`; optional `folder`, `total` | None | [list_files.md](reference/file/list_files.md) |
| “Search notes for…” | `search` | `vault`, `query`; optional `path`, `limit`, `case`, `format` | Query known; upstream filters results to `.md` | [query_text.md](reference/query_text.md) |
| “Show matching lines for…” | `search:context` | `vault`, `query`; optional `path`, `limit`, `case`, `format` | Query known; upstream filters results to `.md` | [query_text.md](reference/query_text.md) |
| “Read/show note…” | `read` | `vault`, existing `.md` `path` | Path exists | [read_note.md](reference/note/read_note.md) |
| “Create a note…” | `create` | `vault`, new `.md` `path`, `content` | Path does not exist | [create_note.md](reference/note/create_note.md) |
| “Append this to note…” | `append` | `vault`, existing `.md` `path`, `content`; optional `inline` | Path exists | [append_note.md](reference/note/append_note.md) |
| “Prepend this to note…” | `prepend` | `vault`, existing `.md` `path`, `content`; optional `inline` | Path exists | [prepend_note.md](reference/note/prepend_note.md) |
| “Move note…” | `move` | `vault`, existing `.md` `path`, `to` | Source exists; destination resolved | [move_note.md](reference/note/move_note.md) |
| “Rename note…” | `rename` | `vault`, existing `.md` `path`, new `name` | Source exists; name resolved | [rename_note.md](reference/note/rename_note.md) |
| “Delete/remove note…” | `delete` | `vault`, existing `.md` `path` | Path exists; trash only | [delete_note.md](reference/note/delete_note.md) |
| “Add frontmatter tag…” | `property:set` | `vault`, existing `.md` `path`, `name=tags`, complete resulting tag-list `value`, `type=list` | Resulting list prepared upstream | [add_frontmatter_tag.md](reference/tag/add_frontmatter_tag.md) |
| “Create a new `.base` file…” | `create` | `vault`, new `.base` `path`, `content` | Path does not exist; content prepared upstream | [create_base.md](reference/base/create_base.md) |
| “Inspect/query/filter a Base…” | `base:query` | `vault`, existing `.base` `path`; optional `view`, `format=json` | Base exists; tag filters use frontmatter `tags` | [query_base.md](reference/base/query_base.md) |

Each row is one operation. The dispatcher must not reinterpret `create` for a `.base` path as `base:create`; `base:create` adds an item to an existing Base and is out of scope.

## CLI prerequisites

The Obsidian 1.12.7+ installer must be installed, and Obsidian must be running with its CLI enabled and registered. Quote values containing spaces; encode multiline `content` with `\\n` and tabs with `\\t`. Deletion uses the default trash behavior; never pass `permanent`.

## Out of scope

Bookmarks, tag counts, inline tags, tasks, daily notes, templates, plugin/theme development, JSON Canvas, Defuddle, Base item creation/update/deletion, full-content replacement, and workflow-level confirmation.

See the [official Obsidian CLI documentation](https://obsidian.md/help/cli).
