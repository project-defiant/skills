# List projects

Isolated project-discovery task used by Vault workflows.

This task lists project folders only. It does not select a project, check for duplicates, ask for confirmation, or mutate the Wiki.

## Function

```text
list-projects(vault)
```

`vault` is the explicit Obsidian vault name or ID supplied by the user.

## Preconditions

- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- `jq` is installed.
- The command must use the explicit vault and the `Projects` folder scope.

If `jq` is unavailable, stop with an error:

```text
list-projects requires jq
```

## Task

Run the Obsidian CLI listing command and convert its newline-delimited paths to JSON:

```bash
command -v jq >/dev/null || {
  echo "list-projects requires jq" >&2
  exit 1
}

obsidian vault="$vault" files folder="Projects" ext=md |
sed 's/^[[:space:]-]*//' |
awk -F/ '$1 == "Projects" && NF >= 3 && $NF ~ /\.md$/ {
  print $2 "\tProjects/" $2
}' |
sort -u |
jq -Rn '
  [inputs | split("\t") | {name: .[0], path: .[1]}]
  | {projects: .}
'
```

A successful listing with no matching Markdown files returns an empty list:

```json
{
  "projects": []
}
```

## Output schema

```json
{
  "type": "object",
  "required": ["projects"],
  "properties": {
    "projects": {
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
