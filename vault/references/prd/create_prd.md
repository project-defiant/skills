# Create PRD

Isolated immutable PRD creation task used by the `create-prd` workflow.

This task does not resolve projects, check filename collisions, grill the user, ask for confirmation, log the creation, or decide whether the workflow should continue.

## Function

```text
create-prd(vault, prd_path, prd_content)
```

- `vault`: explicit Obsidian vault name or ID.
- `prd_path`: exact destination path, for example `Projects/Project Name/PRD/2026-08-31-Project Plan.md`.
- `prd_content`: complete PRD content generated and approved by the workflow.

## Preconditions

- All inputs are present.
- `prd_path` ends with `.md` and follows `Projects/{project_name}/PRD/YYYY-MM-DD-{prd_name}.md`.
- The exact destination path does not exist.
- `prd_content` conforms to the canonical immutable PRD structure in `project_structure.md`.
- The caller has already performed collision checks and received confirmation.
- Obsidian CLI is available and Obsidian is running with CLI access enabled.
- Use the explicit vault and exact vault-relative paths.

## Task

Create the complete immutable PRD with one Obsidian CLI operation:

```bash
obsidian vault="$vault" create \
  path="$prd_path" \
  content="$prd_content"
```

The `PRD/` folder is created implicitly when the first PRD file is created. Do not create an empty folder or use `overwrite`.

## Result

- Return `success` when the PRD is created.
- Return `failure` when the Obsidian CLI operation fails.
