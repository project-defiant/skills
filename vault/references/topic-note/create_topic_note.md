# Create topic note

Atomic topic-note creation task.

## Function

```text
create-topic-note(vault, topic, content, source_link)
```

Create `Topic/{topic}.md` with the agreed frontmatter and one append-only source block:

```markdown
---
type: topic
title: "{Topic title}"
tags:
  - topic
  - {topic}
---

# {Topic title}

### {source_link}

{content}
```

Use the normalized topic for the filename and exact topic tag. Return success or failure only. Do not search, update existing notes, or make workflow decisions.

Invoke one Obsidian CLI `create` operation with the complete prepared content. The parent `Topic/` folder must already exist.
