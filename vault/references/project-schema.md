# Project schema

## Project layout

```text
$SZYMON_WIKI/Projects/{project}/
├── requirements.md
├── PRDs/
│   └── YYYY-MM-DD-{slug}.md
├── Meetings.md
├── log.md
└── project.base
```

The project identifier is the folder name. Store it as a plain `project` value in project documents. Research notes that can belong to more than one project use `projects: [{project}, ...]`.

## Requirements frontmatter

```yaml
title: Project name
kind: requirements
project: project-id
status: planning
tags: []
linear_project: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

`linear_project` holds the raw Linear project URL once it is resolved. The body contains the purpose, context, scope, non-scope, agreed decisions, constraints, success criteria, relevant references, and a `## Linear` section containing that same raw URL.

## PRD frontmatter

```yaml
title: PRD title
kind: prd
project: project-id
status: proposed
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
```

A PRD contains: outcome, implementation scope, deliverables, agreed implementation decisions, validation and acceptance criteria, dependencies, and non-goals. It represents an implementation phase, not open-ended research.

## Meetings

`Meetings.md` is one append-only note per project. Each entry contains a date, purpose, and decisions only.

## Log

Append only for a requirements or PRD creation/update:

```markdown
- YYYY-MM-DD HH:MM — requirements created|updated — summary — [[requirements]]
- YYYY-MM-DD HH:MM — PRD created|updated — summary — [[YYYY-MM-DD-slug]]
```

## Research metadata

Source-note frontmatter records `title`, `authors`, `last_author`, `publication_date`, `year`, `journal`, `doi`, `url`, `source_paper`, `tags`, and `projects`.

Topic-note frontmatter records `title`, `kind: topic-note`, `tags`, `projects`, `source_notes`, and `source_papers`.

Use `[[...]]` links for local notes and PDFs. A statement derived from a PDF ends with a link to its exact annotation or selection, not plain citation text.
