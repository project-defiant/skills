# Mode: project-init

Scaffold a new project under `$SZYMON_WIKI/Projects/`.

## Inputs

- **project_name** (required): human-readable name; used verbatim as the folder name (Obsidian tolerates spaces).
- **status** (optional, default `planning`): one of `planning | active | blocked | dormant | done`.
- **priority** (optional, default `medium`): one of `high | medium | low`.
- **tags** (optional): YAML list. Empty by default.
- **github_repo** (optional): URL of the GitHub repo (empty if none).
- **github_issues** (optional): list of GitHub issue numbers (empty by default).

If `project_name` is missing, ask the user for it. All other inputs use their defaults if not provided.

## Steps

1. Compute `DEST="$SZYMON_WIKI/Projects/{project_name}"`.
2. If `$DEST` already exists, STOP and report: `Project already exists at $DEST — use log-status or ingest-source to add to it.`
3. Create directories:
   - `$DEST/Plan/`
   - `$DEST/Research/sources/`
   - `$DEST/ImplementationStatus/`
   - `$DEST/Meetings/`
4. Write `$DEST/index.md` from the `index.md` template below.
5. Write `$DEST/log.md` from the `log.md` template below.
6. Write `$DEST/ImplementationStatus/CHANGELOG.md` from the `CHANGELOG.md` template below.
7. Update `$SZYMON_WIKI/index.md`:
   - Under the `## Projects` section, insert `- [[{project_name}]] — status: {status} — priority: {priority}` in alphabetical order.
   - Replace the placeholder `_None yet. ..._` line if it is still present.
8. Append project log entry to `$DEST/log.md`:
   `- YYYY-MM-DD HH:MM — project-init — Created project.`
9. Append global log entry to `$SZYMON_WIKI/log.md`:
   `- YYYY-MM-DD HH:MM — [[{project_name}]] — project-init — Created project.`
10. Report all created paths back to the user.

The two-log pattern (project + global) is the shared convention for **every** mode that touches a project — see the "Shared conventions" section of `SKILL.md`. Project-init is not an exception even though it creates the project log in the same call.

## Templates

### `$DEST/index.md`

~~~
---
title: {project_name}
status: {status}
priority: {priority}
created_at: {YYYY-MM-DD}
tags: {tags_yaml}
github_repo: {github_repo}
github_issues: {github_issues_yaml}
---

# {project_name}

Structure:
- `Plan/` — planning decisions and design notes
- `Research/sources/` — raw, immutable ingested sources
- `Research/*.md` — summaries and derived notes
- `ImplementationStatus/CHANGELOG.md` — running wikilink-index of dated status snapshots
- `Meetings/` — dated meeting notes (deferred; scaffolded for future)
- `log.md` — chronological project log

## GitHub

<!-- GH-SYNC-START -->
_No GitHub sync yet. Set `github_repo` and `github_issues` in the frontmatter, then run `log-status` to fetch._
<!-- GH-SYNC-END -->

## Plan

_No decisions filed yet._

## Research

_No sources ingested yet._

## Implementation status

See [[CHANGELOG]].
~~~

### `$DEST/log.md`

~~~
# Log — {project_name}

Chronological log. Newest entries appended at bottom.

Format: `- YYYY-MM-DD HH:MM — <mode> — one-line — [[detail-note]]`

~~~

### `$DEST/ImplementationStatus/CHANGELOG.md`

~~~
# Changelog — {project_name}

Wikilink-index of dated status snapshots in this folder. Newest at bottom.

Format: `- YYYY-MM-DD — one-line summary — [[YYYY-MM-DD]]`

~~~
