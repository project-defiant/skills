# Link Linear project

Isolated Wiki mutation task used by the `link-linear` workflow.

This task writes the Linear project URL into the Wiki project. It does not access or mutate Linear, resolve either project, ask for confirmation, or decide whether the workflow should continue.

## Function

```text
link-linear(vault, wiki_project, linear_project_url)
```

- `vault`: explicit Obsidian vault name or ID.
- `wiki_project`: resolved Wiki project object containing `path`.
- `linear_project_url`: verified Linear project URL.

## Preconditions

- `vault`, `wiki_project`, and `linear_project_url` are present.
- `Projects/{project_name}/requirements.md` already exists.
- The caller has already resolved the Wiki project and verified the Linear project through the Linear skill.
- The caller has already received user confirmation.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.

## Task

Set `wiki_project_path = wiki_project.path`, then set the `linear_project` frontmatter property on the existing requirements note:

```bash
obsidian vault="$vault" property:set \
  path="$wiki_project_path/requirements.md" \
  name=linear_project \
  value="$linear_project_url" \
  type=text
```

Preserve all existing frontmatter and note content. Do not write a Wiki URL to Linear.

## Result

- Return `success` when the property update completes.
- Return `failure` when the Obsidian CLI operation fails.
