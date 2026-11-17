# Obsidian CLI Skill — First-Part PRD

## Status

Drafted from the agreed design discussion. This PRD covers the first implementation part of the local `obsidian` skill.

## Problem

The repository contains an Obsidian skill entry point and reference files, but the entry point is only metadata and the references are empty. The skill needs a precise, atomic interface for operating on Markdown notes and Obsidian Bases through the Obsidian CLI.

The skill must provide CLI primitives, not workflow orchestration. Upstream workflow skills are responsible for discovery, sequencing, validation, and deciding which target should be operated on.

## Goal

Document a focused Obsidian CLI skill whose operations are deterministic, single-purpose, and safe to call from higher-level workflows.

## Scope

The first part includes only these operations:

- List existing Markdown notes (`.md`) and Base definitions (`.base`).
- Search Markdown note body and frontmatter.
- Read an existing Markdown note.
- Create a new Markdown note at an exact path.
- Append content to an existing Markdown note.
- Prepend content to an existing Markdown note.
- Move an existing Markdown note.
- Rename an existing Markdown note.
- Delete an existing Markdown note to Obsidian trash.
- Add one tag to the frontmatter `tags` property of an existing Markdown note.
- Create a new `.base` definition file at an exact path.
- Query an existing Base, including queries filtered by the frontmatter `tags` property.

## Atomicity and preconditions

Every documented operation must perform one CLI action and one thing only.

The skill must:

- Require an explicit vault target for every operation.
- Never use the active/open file as an implicit target.
- Never combine discovery and mutation.
- Never choose a target file on the caller’s behalf.
- Require exact paths for mutations.
- Assume the upstream workflow has already established whether a target exists or does not exist.
- Treat ambiguous or missing preconditions as upstream workflow errors, not as reasons to guess.
- Prefer structured output where the command supports it.
- Avoid permission prompts and workflow-level confirmation questions.

### Mutation preconditions

- Create operations require that the exact destination path is known not to exist.
- Read, append, prepend, move, rename, tag-add, and delete operations require that the exact target path is known to exist.
- Delete means move to Obsidian trash; permanent deletion is out of scope.
- Adding a tag must preserve all other frontmatter and note content, add only the requested frontmatter tag, and avoid duplicates.

## Note API

The local note references should be atomic CLI references:

- `reference/note/read_note.md` — read an existing Markdown note.
- `reference/note/create_note.md` — create a new Markdown note from caller-supplied content.
- `reference/note/append_note.md` — append content to an existing Markdown note.
- `reference/note/prepend_note.md` — prepend content to an existing Markdown note.
- `reference/note/move_note.md` — move an existing Markdown note.
- `reference/note/rename_note.md` — rename an existing Markdown note.
- `reference/note/delete_note.md` — send an existing Markdown note to trash.

There is no native `obsidian update` command. `update_note.md` should therefore be replaced by the separate append and prepend references. Full-content replacement is an upstream workflow, not a single CLI primitive.

Note creation is limited to exact `.md` paths and caller-supplied content. Template expansion is out of scope.

## Search and tags

### Text search

`query_text.md` should document only non-mutating full-text search commands:

- `search`
- `search:context`

General text search may inspect Markdown body and frontmatter. It must not be used for tag listing or tag-based filtering.

### Frontmatter tags

`tag_note.md` should document only these behaviors:

- Add a tag to an existing note’s YAML frontmatter `tags` property.
- Query notes by tag through an existing Base whose filters use the frontmatter `tags` property.

The skill must not support inline tags such as `#project`, tag counts, or content-based tag listing.

## Base API

Base operations are limited to:

- Creating a new `.base` definition file at an exact, non-existing path using content supplied by the upstream workflow.
- Querying an existing Base.

Base creation must not design or validate the Base schema. Base design and validation happen upstream.

`base:create` must not be interpreted as creating a Base definition; in the Obsidian CLI it creates an item in an existing Base, which is out of scope.

Base update, Base deletion, and adding items to an existing Base are out of scope.

## File discovery

The discovery reference should list only `.md` and `.base` files. Attachments and other file types are out of scope for this part.

## Explicit non-goals

The first part must not include:

- Bookmarks
- Tag counts or tag inventories
- Inline tags
- Tasks
- Daily notes
- Plugin development
- Theme development
- JSON Canvas
- Defuddle
- Template expansion
- Permanent file deletion
- Base item creation
- Base update or deletion
- Full-content note replacement as a CLI primitive
- User permission or confirmation prompts
- Multi-step discovery-plus-mutation workflows

## Operational guidance

The skill should document the Obsidian CLI requirements and syntax:

- Obsidian 1.12 installer, as required by the official CLI documentation.
- Obsidian must be running.
- `vault=<name>` or `vault=<id>` must be the first parameter.
- `file` and `path` have different resolution semantics; mutations should use exact vault-relative paths.
- Parameters use `name=value`; flags do not take values.
- Quoted values and escaped `\\n`/`\\t` are required for spaces and multiline content.
- `obsidian help <command>` is the source of truth when CLI behavior is version-sensitive.

## Acceptance criteria

- `obsidian/SKILL.md` explains the atomic primitive model and dispatches to the reference files.
- No in-scope reference file remains empty.
- `update_note.md` is removed or replaced by `append_note.md` and `prepend_note.md`.
- Every mutation reference states its existence precondition and exact-path requirement.
- No reference defaults to the active file.
- Tag guidance operates only on frontmatter and never uses text search to list tags.
- Base guidance distinguishes creating a `.base` definition from creating an item in an existing Base.
- Bookmarks, tasks, daily notes, developer commands, Canvas, and Defuddle are absent from the implemented scope.
- Examples use structured output where supported and do not claim unsupported CLI commands.
- The documentation links to the [official Obsidian CLI documentation](https://obsidian.md/help/cli) and uses `obsidian help` for current command details.

## References

- [Obsidian CLI documentation](https://obsidian.md/help/cli)
- [Kepano’s Obsidian skills](https://github.com/kepano/obsidian-skills/tree/main/skills)
- [Upstream Obsidian CLI skill](https://raw.githubusercontent.com/kepano/obsidian-skills/main/skills/obsidian-cli/SKILL.md)
