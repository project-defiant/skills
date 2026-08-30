# List Markdown notes and Base definitions

List files in an explicitly selected vault. This is a read-only discovery primitive and must not be combined with a mutation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` as the first parameter.
- Use the command once for Markdown notes and once for Base definitions when both are needed. Each invocation performs one listing operation.
- Do not rely on the active vault or active file.

## Commands

List Markdown notes:

```bash
obsidian vault="My Vault" files ext=md
```

List Base definitions:

```bash
obsidian vault="My Vault" files ext=base
```

Limit discovery to a vault-relative folder when the caller already supplies that folder:

```bash
obsidian vault="My Vault" files folder="Projects" ext=md
```

Use `total` when only the number of matching files is required:

```bash
obsidian vault="My Vault" files ext=md total
```

## Output

Return the CLI output to the upstream workflow. Do not select a file, open a file, or mutate the vault. Use the command’s current output behavior from `obsidian help files`; do not assume an unsupported output format.

## Out of scope

This reference does not list attachments or other extensions, infer a target path, or create, edit, move, rename, or delete files.
