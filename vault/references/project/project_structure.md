# Wiki project structure

This reference defines the canonical structure for one project in the Obsidian Wiki. It is a skill reference only; do not create this file inside the Wiki.

## Layout

```text
Projects/{Project}/
├── log.md
├── requirements.md
├── meetings.md
└── PRD/
    └── {date}-{prd-name}.md
```

## Creation rules

- `log.md`, `requirements.md`, and `meetings.md` are created when the project is created.
- `PRD/` is materialized when the first PRD is created; do not create an empty PRD folder.
- PRD filenames use `YYYY-MM-DD-{prd-name}.md`.
- `{Project}` is the exact project folder name supplied or confirmed by the user.
- The project workflow must resolve the exact vault-relative path before creating or reading files.

## File responsibilities

- `log.md`: chronological project updates. It starts with:

  ```markdown
  # Project Log

  ## Updates
  ```

  Updates are appended in place under `## Updates`.
- `requirements.md`: durable project requirements and, when applicable, Linear project mapping frontmatter. It starts with:

  ```yaml
  ---
  type: project
  created: YYYY-MM-DD
  tags:
    - project
  ---

  # Requirements

  ## Context

  ## Requirements

  ## Decisions
  ```

  `linear_project` is added only when the project is linked to Linear:

  ```yaml
  linear_project: https://linear.app/example/project/project-name
  ```
- `meetings.md`: project-related meeting summaries. It starts with:

  ```markdown
  # Meetings

  ## Summaries
  ```

  Summaries are appended in place under `## Summaries`.
- `PRD/{date}-{prd-name}.md`: immutable project PRD documents. Each PRD starts with:

  ```markdown
  ---
  type: prd
  created: YYYY-MM-DD
  tags:
    - prd
  ---

  # {prd-name}

  ## Context

  ## Goals

  ## Requirements

  ## Acceptance Criteria
  ```

  The PRD grill must resolve all open questions before creation. PRDs have no `Decisions` or `Open Questions` sections and are never updated in place.

## Entry format

Updates to persistent project files happen in place. Workflows must preserve existing frontmatter, headers, and entries; they must not recreate or overwrite an existing note.

Entries use dated headings:

```markdown
### YYYY-MM-DD — Entry title
```

- `log.md` entries are added under `## Updates`.
- `meetings.md` entries are added under `## Summaries` and must include the meeting date in the heading.
- Decisions in `requirements.md` are added under `## Decisions` and must include the decision date in the heading.
