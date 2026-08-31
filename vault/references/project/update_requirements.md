# Update project requirements

Atomic in-place requirements-note update task.

## Function

```text
update-project-requirements(vault, requirements_path, update_content)
```

Append the supplied update content to the existing requirements note with one Obsidian CLI `append` operation. Preserve existing frontmatter and content. Return success or failure only. Do not read, discover, confirm, or make workflow decisions.
