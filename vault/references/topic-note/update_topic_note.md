# Update topic note

Atomic append-only topic-note task.

## Function

```text
update-topic-note(vault, topic, content, source_link)
```

Append one new source block to the existing `Topic/{topic}.md` without changing its frontmatter or existing content:

```markdown
### {source_link}

{content}
```

Topic notes do not contain dates. Return success or failure only. Do not search for the note, create missing notes, synthesize across sources, or make workflow decisions.

Invoke one Obsidian CLI `append` operation against the existing exact path. Preserve all existing content and frontmatter.
