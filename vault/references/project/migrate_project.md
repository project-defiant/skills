# Migrate project

Isolated project-migration task used by the `migrate-project` workflow.

This task applies an already-approved migration plan to already-read source content. It does not list projects, resolve destinations, ask the user questions, confirm the plan, or decide what to preserve.

## Function

```text
migrate-project(
  vault,
  source_path,
  project_name,
  source_content,
  migration_plan
)
```

- `vault`: explicit Obsidian vault name or ID.
- `source_path`: exact source path supplied by the workflow.
- `project_name`: confirmed destination project name.
- `source_content`: source material already read by the workflow.
- `migration_plan`: user-approved instructions describing what to preserve, remove, reshape, discard, and where retained material belongs.

## Preconditions

- All inputs are present.
- The destination `Projects/{project_name}/` does not exist.
- `source_content` has already been read.
- `migration_plan` has already been confirmed by the user.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- Use the explicit vault and exact vault-relative paths.
- Do not create an empty `PRD/` folder.

## Task

1. Transform `source_content` according to `migration_plan`. Do not preserve, remove, or reshape material based on an unapproved assumption.
2. Ensure the resulting project conforms exactly to `project_structure.md`.
3. Create the required initial notes with their canonical headers:

   ```text
   Projects/{project_name}/log.md
   Projects/{project_name}/requirements.md
   Projects/{project_name}/meetings.md
   ```

4. Create approved PRD files only when the migration plan retains PRD material. PRD files must follow `PRD/YYYY-MM-DD-{prd-name}.md`.
5. Use one separate Obsidian CLI `create` action for each destination Markdown note:

   ```bash
   obsidian vault="$vault" create \
     path="$destination_path" \
     content="$destination_content"
   ```

Preserve the canonical headers and required project metadata. Do not overwrite existing files or create files outside the canonical project structure.

## Result

- Return `success` when all approved destination files are created.
- Return `failure` when any Obsidian CLI operation fails.
