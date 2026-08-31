# Find project

Isolated project-resolution task used by the `read-project` and other project workflows.

This task verifies one exact project folder and returns its normalized identity. It does not summarize, mutate, or ask the user anything.

## Function

```text
find-project(vault, project_name)
```

## Preconditions

- `vault` and `project_name` are present.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- `jq` is installed.
- The command must use the explicit vault and an exact `Projects/{project_name}` folder scope.

If `jq` is unavailable, stop with an error:

```text
find-project requires jq
```

## Task

```bash
command -v jq >/dev/null || {
  echo "find-project requires jq" >&2
  exit 1
}

obsidian vault="$vault" files folder="Projects/$project_name" ext=md |
sed 's/^[[:space:]-]*//' |
awk -F/ '$1 == "Projects" && NF >= 3 && $NF ~ /\.md$/ {
  print
}' |
head -n 1 |
jq -Rn \
  --arg name "$project_name" \
  --arg path "Projects/$project_name" '
    [inputs] as $files
    | if ($files | length) == 0
      then null
      else {
        name: $name,
        path: $path
      }
      end
  '
```

## Output schema

The task returns the project identity when the exact folder contains at least one Markdown file, otherwise `null`:

```json
{
  "oneOf": [
    {
      "type": "null"
    },
    {
      "type": "object",
      "required": ["name", "path"],
      "properties": {
        "name": { "type": "string" },
        "path": { "type": "string" }
      },
      "additionalProperties": false
    }
  ]
}
```
