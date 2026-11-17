---
name: obsidian-by-file
description: Default primitive for reading and mutating Markdown notes in the Obsidian vault at `$SZYMON_WIKI` through direct file operations. Use when an upstream workflow has resolved the operation and exact vault-relative path for listing, searching, reading, creating, appending, prepending, moving, renaming, deleting, or tagging a note. Fall back to the `obsidian` CLI skill only for Base queries, rename with wikilink rewriting, or when the user asks for the CLI.
---

# Obsidian by file

Use exactly one mode from the dispatcher table. This skill is a primitive layer: it does not discover targets, choose files, sequence operations, validate content, or ask for permission.

## Vault root

`$SZYMON_WIKI` is the vault root. Do not ask for a vault when it is defined.

If `$SZYMON_WIKI` is unset, empty, or not a directory, ask the user explicitly for the vault root before proceeding. Never use the active Obsidian vault implicitly.

Reference files may use `$vault` as a placeholder; it always means the resolved vault root directory.

## Global constraints

- Every target is an exact vault-relative path resolved against `$SZYMON_WIKI`. Reject paths that escape the vault (`..`, absolute paths, symlinks out of the root).
- Never touch `.obsidian/` or `.trash/` except when a mode says so.
- The upstream workflow must establish existence before mutation: create requires absent; all other mutations require present.
- Perform exactly one file action per mode.
- Operate only on `.md` notes. `.base` files may be created or read as plain YAML; querying them is a CLI operation.
- Prefer the agent's Read/Write/Edit tools over shell redirection when available; the commands below are the shell equivalents.
- Write UTF-8 with real newlines. Obsidian picks up file changes automatically.

## Mode dispatcher

| Mode / trigger | File operation | Precondition |
|---|---|---|
| “List notes in folder…” | `cd "$SZYMON_WIKI" && find "$folder" -type f -name '*.md' \| sort` | None; prints vault-relative paths |
| “Search notes for…” | `cd "$SZYMON_WIKI" && rg -n --glob '*.md' --glob '!.obsidian/**' --glob '!.trash/**' "$query" "${folder:-.}"` (fallback `grep -rn --include='*.md'`) | Query known |
| “Read/show note…” | Read `"$SZYMON_WIKI/$path"` | Path exists |
| “Create a note…” | `mkdir -p "$(dirname "$SZYMON_WIKI/$path")" && (set -C; printf '%s' "$content" > "$SZYMON_WIKI/$path")` | Path does not exist; `set -C` refuses to overwrite |
| “Append this to note…” | `printf '\n%s\n' "$content" >> "$SZYMON_WIKI/$path"` | Path exists |
| “Prepend this to note…” | Edit the file, inserting `content` immediately after the frontmatter block (or at the top if there is none) | Path exists |
| “Move note…” | `mkdir -p "$(dirname "$SZYMON_WIKI/$to")" && mv -n "$SZYMON_WIKI/$path" "$SZYMON_WIKI/$to"` | Source exists; destination absent |
| “Rename note…” | `mv -n` within the same folder | Source exists; new name absent. Wikilinks are **not** rewritten; use the CLI `rename` when backlinks must follow |
| “Delete/remove note…” | `mkdir -p "$SZYMON_WIKI/.trash" && mv -n "$SZYMON_WIKI/$path" "$SZYMON_WIKI/.trash/"` | Path exists; never `rm` |
| “Add frontmatter tag…” | Edit the YAML `tags:` list in the frontmatter, preserving every other key | Resulting list prepared upstream |

## Delegate to the Obsidian CLI

Load the `obsidian` skill instead when the request needs:

- `base:query` or any evaluated Base view;
- rename or move that must rewrite wikilinks across the vault;
- Obsidian's search index (e.g. `search:context` across aliases);
- the user explicitly asks for the CLI.

## Out of scope

Plugin APIs, workspace state, automatic wikilink rewriting, Base transactions, and broad recursive mutations. Refuse accidental overwrites and ambiguous or destructive targets.
