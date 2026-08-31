# Create source note

Atomic source-note creation task. It receives prepared metadata and summary content and performs only the source-note creation operation.

## Function

```text
create-source-note(vault, metadata, summary, topics)
```

## Task

Create `Source/{metadata.source_key}.md` using the agreed source-note frontmatter and body structure. Use the exact publication title in `title` and the `#` heading. Authors, journal, and `source_path` are Obsidian links where applicable. Include `source` plus every `topic.name` in `tags`.

The body is the supplied summary. Do not modify the PDF, add page references, create highlights, or process topic notes. Return success or failure only.

Invoke one Obsidian CLI `create` operation with the complete prepared Markdown content. The task does not perform discovery, confirmation, duplicate checks, or topic-note writes.
