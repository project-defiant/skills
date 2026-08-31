# Update project requirements

Atomic in-place requirements-note update task.

## Function

```text
update-project-requirements(vault, requirements_path, update_content)
```

Append the supplied update content to the existing requirements note with one Obsidian CLI `append` operation. Preserve existing frontmatter and content. The update must not contain frontmatter, a second frontmatter block, `# Requirements`, `## Decisions`, or dated `###` headings. If the note has no body sections, the upstream workflow may include exactly one of `## Context` or `## Requirements` before the new content. If the section already exists, append body content only and do not repeat its header. Each structural header may occur at most once; `## Decisions` and dated entries are not permitted. Return success or failure only. Do not read, discover, confirm, or make workflow decisions.
