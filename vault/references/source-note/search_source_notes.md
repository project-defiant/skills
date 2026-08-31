# Search source note

Isolated source-note discovery task used by publication workflows.

This task checks one exact source-note identity. It does not read note contents, create or update notes, resolve publication metadata, or make workflow decisions.

## Function

```text
search-source-note(vault, source_key)
```

- `vault`: explicit Obsidian vault name or ID.
- `source_key`: exact source identity in `{last_author} {year}` format, for example `Tang 2024`.

## Preconditions

- `vault` and `source_key` are present.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- `jq` is installed.
- Use the explicit vault and the `Source` folder scope.

If `jq` is unavailable, stop with an error:

```text
search-source-note requires jq
```

## Task

List Markdown files under `Source/` and return the exact matching source-note path:

```bash
command -v jq >/dev/null || {
  echo "search-source-note requires jq" >&2
  exit 1
}

target="Source/$source_key.md"
path=$(
  obsidian vault="$vault" files folder="Source" ext=md |
  sed 's/^[[:space:]-]*//' |
  awk -v target="$target" '$0 == target { print; exit }'
)

jq -Rn --arg path "$path" \
  'if $path == "" then null else $path end'
```

## Output

Return the exact path when found, otherwise `null`:

```text
"Source/Tang 2024.md"
```

```text
null
```

## Output schema

```json
{
  "oneOf": [
    {
      "type": "null"
    },
    {
      "type": "string",
      "pattern": "^Source/.+\\.md$"
    }
  ]
}
```
