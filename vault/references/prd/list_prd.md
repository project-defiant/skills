# List PRDs

Isolated PRD-discovery task used by PRD workflows.

This task lists immutable PRD files only. It does not resolve projects, select a PRD, read contents, ask for confirmation, or mutate the Wiki.

## Function

```text
list-prds(vault, project_path)
```

- `vault`: explicit Obsidian vault name or ID.
- `project_path`: exact resolved project path, for example `Projects/Project Name`.

## Preconditions

- `vault` and `project_path` are present.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- `jq` is installed.
- Use the explicit vault and the exact `PRD` folder scope.

If `jq` is unavailable, stop with an error:

```text
list-prds requires jq
```

## Task

List Markdown files under the project PRD folder and normalize each filename:

```bash
command -v jq >/dev/null || {
  echo "list-prds requires jq" >&2
  exit 1
}

obsidian vault="$vault" files folder="$project_path/PRD" ext=md |
sed 's/^[[:space:]-]*//' |
awk -v prefix="$project_path/PRD/" 'index($0, prefix) == 1 && $NF ~ /\.md$/ {
  name = $NF
  sub(/\.md$/, "", name)
  print name "\t" $0
}' |
sort -u |
jq -Rn '
  [inputs | split("\t") | {name: .[0], path: .[1]}]
  | {prds: .}
'
```

If no PRD files exist, return:

```json
{
  "prds": []
}
```

## Output schema

```json
{
  "type": "object",
  "required": ["prds"],
  "properties": {
    "prds": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "path"],
        "properties": {
          "name": { "type": "string" },
          "path": { "type": "string" }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```
