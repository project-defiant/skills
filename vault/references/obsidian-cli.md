# Obsidian CLI operations

Use the Obsidian CLI for vault-aware operations when Obsidian is running and the CLI is available.

1. Run `obsidian help` first. Treat it as the source of truth for commands supported by the installed Obsidian version.
2. Pass parameters as `key=value`; quote values containing spaces or special characters.
3. `file=` resolves like an Obsidian link. `path=` identifies an exact vault-relative file path. Prefer `path=` when a skill has resolved an unambiguous target.
4. Use the target vault explicitly whenever the available CLI supports a vault parameter.
5. Useful operations are reading, searching, creating, appending, setting properties, finding links, and opening a file to inspect a rendered result.
6. Obtain approval immediately before commands that create, append, rename, set properties, or otherwise change a note.

Do not rely on plugin-development commands or copied command syntax. If the CLI is unavailable, state that clearly and use the approved local-file workflow only when it can preserve the requested Obsidian structure.
