# Extract topics

Atomic topic-extraction task. It consumes publication text already extracted by `read-publication`; it does not read the PDF, access the Wiki, create or update notes, or make workflow decisions.

## Function

```text
extract-topics(metadata, publication_text, summary, curated_topics=null)
```

## Task

Return substantive concepts central to the publication, excluding generic terms such as `study`, `data`, and `analysis`. Normalize every topic to lowercase kebab-case so it maps to `Topic/{topic}.md`.

When `curated_topics` is supplied, return only those topics and generate content for each from the supplied publication text. Content must be publication-specific, concise, standalone, and contain no cross-source synthesis.

## Output schema

```json
{
  "type": "object",
  "required": ["topics"],
  "properties": {
    "topics": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "content"],
        "properties": {
          "name": { "type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$" },
          "content": { "type": "string", "minLength": 1 }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

An empty topic list is valid before user curation. The workflow must notify the user and request topics when that occurs.
