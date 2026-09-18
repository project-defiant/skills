---
name: obsidian-by-file
description: Directly read or mutate files inside the Obsidian vault at `$SZYMON_WIKI` when the Obsidian CLI cannot perform the requested operation or is unavailable.
---

# Obsidian by file

Use this as the fallback after the normal Obsidian CLI skill has been loaded and a CLI operation is unavailable or out of scope. Do not ask for a vault name when `$SZYMON_WIKI` is defined; it is the vault root.

Resolve every requested path relative to `$SZYMON_WIKI`, require the resolved target to remain inside that directory, and operate only on the exact file the user or upstream workflow selected. Preserve the intended CLI operation where practical: list, read, create, append, prepend, move, rename, recoverable delete, and simple text search.

If `$SZYMON_WIKI` is unset, empty, or not a directory, ask the user explicitly for the vault root before proceeding. Do not use the active Obsidian vault implicitly.

This is a lightweight fallback, not a replacement for Obsidian CLI behavior. Do not attempt plugin APIs, workspace state changes, automatic wikilink rewriting, Base transactions, or broad recursive mutations. Refuse accidental overwrites and ambiguous or destructive targets; otherwise keep the operation proportional to the user’s request.
