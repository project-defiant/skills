# Search topic note

Atomic exact topic-note discovery task.

## Function

```text
search-topic-note(vault, topic)
```

Resolve only `Topic/{topic}.md`, where `topic` is already normalized to lowercase kebab-case. Return the exact path when present, otherwise `null`. Do not use fuzzy matching, read contents, or make workflow decisions.

Use:

```bash
target="Topic/$topic.md"
path=$(
  obsidian vault="$vault" files folder="Topic" ext=md |
  sed 's/^[[:space:]-]*//' |
  awk -v target="$target" '$0 == target { print; exit }'
)
```

Return the path as a JSON string or `null`.

## Output schema

```json
{
  "oneOf": [
    { "type": "null" },
    { "type": "string", "pattern": "^Topic/.+\\.md$" }
  ]
}
```
