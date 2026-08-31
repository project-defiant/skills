---
name: vault
description: Manage a user's Obsidian LLM-wiki through Obsidian CLI workflows. Use when the user provides an explicit `vault=<name|id>` and requests project, requirements, PRD, meeting, source-note, or topic-note work.
---

# vault - Obsidian LLM-wiki skill

## Prerequisites

- The user must provide `vault=<name|id>` directly or use the `v` as the default vault. Do not infer or use Obsidian's active vault.
- Obsidian CLI 1.12.7+ must be installed, and Obsidian must be running with CLI access enabled. If unavailable, STOP and tell the user that the Obsidian CLI and a CLI-enabled running Obsidian instance are required.
- Every operation must pass the explicit `vault=<name|id>` first and use an exact vault-relative path.
- Prefer `ripgrep` (`rg`); fall back to `grep -r` if absent.

## Better ask then regret

Follow the notion, that if the answer is ambiguous can cause misunderstanding, ask user to clarify.

## Project structure

Project structure in the vault is specified in `references/project/project_structure.md`.
Project workflows accept a project name, resolve it to an exact `Projects/{Project}/` path through Obsidian CLI file listing, and only then read or mutate files.

```
{vault}/
├── Source/{source_note}.md
├── Topic/{topic}.md
└── Projects/{Project}/
    ├── log.md                     # project chronological
    ├── requirements.md             # project requirements and Linear mapping
    ├── PRD/                       # project PRD files
    │   ├── {date}-{prd name}.md
    └── meetings.md                # project meetings
```

## Mode dispatch

Match the user's request against the intends below and READ the matching reference files before acting. Do not act from memory or previous invocations. Always load the reference

When using modes, ensure the user has provided input parameters directly or they are available from the previous conversation. Do not act before collecting all mode inputs.

Example

> User: I want to create a project
> Agent: I need to get the vault and project name before I can call `create-project(vault, project_name)` mode to generate a new project in the wiki
> add `New-project` to the wiki
> Agent: creating new project (`New-project`) in the wiki

| Intent (triggers) | mode | reference |
| "Init / scaffold / create a project in the wiki" | create-project(vault, project_name) | `references/project/create_project.md` |
| "Create project requirements file in project folder" | create-project-requirements(vault, project_name, content) | `references/project/create_requirements.md` |
| "Find existing project in the wiki" | find-project(vault, project_name) | `references/project/find_project.md` |
| "Link Wiki project to Linear project" | link-linear(vault, project_name, linear_project) | `references/project/link_linear_project.md` |
| "List all projects in the wiki" | list-projects(vault) | `references/project/list_projects.md` |
| "Migrate existing project structure to `Project structure`" | migrate-project(vault, source_path, project_name) | `references/project/migrate_project.md` |
| "Summarize work done over project" | summarize-project(vault, project_name) | `references/project/summarize_project.md` |
| "Update existing project" | update-project(vault, project) | `references/project/update_project.md` |
| "Verify project structure and report issues" | lint-project(vault, project_name) | `references/project/lint_project.md` |
| "Create PRD document in the project" | create-prd(vault, project_name, prd_name, context) | `references/prd/create_prd.md` |
| "List existing PRD documents in the project" | list-prds(vault, project_path) | `references/prd/list_prd.md` |
| "Query existing PRD in the project" | query-prd(vault, prd_path) | `references/prd/query_prd.md` |
| "Update a project's meeting note" | update-meeting-note(vault, project_name, meeting, date, context) | `references/meeting/update_meeting_note.md` |
| "Review a publication and prepare source-note" | review-publication(vault, path_to_publication) | `references/source-note/create_source_note.md`, `references/source-note/read_publication.md`, `references/source-note/summarize_publication.md`, `references/source-note/extract_topics.md` |
| "Search for the source note linked to a publication" | search-source-note(vault, source_key) | `references/source-note/search_source_notes.md` |
| "Read a source note" | read-source-note(vault, source_key) | `references/source-note/search_source_notes.md` + Obsidian `read` |
| "Create a topic-note from source" | create-topic-note(vault, topic, content, source_link) | `references/topic-note/create_topic_note.md` |
| "Update a topic-note with information from source" | update-topic-note(vault, topic, content, source_link) | `references/topic-note/update_topic_note.md` |
| "Search for topic in topic-notes" | search-topic-note(vault, topic) | `references/topic-note/search_topic_notes.md` |
| "Read a topic note" | read-topic-note(vault, topic) | `references/topic-note/search_topic_notes.md` + Obsidian `read` |
| "Log project update" | log-project-update(vault, project_path, context) | `references/project/log_project_update.md` |
| "Extract publication metadata from PDF" | extract-publication-metadata(publication_path) | `references/source-note/extract_publication_metadata.md` |
| "Read publication text from PDF" | read-publication(publication_path) | `references/source-note/read_publication.md` |
| "Summarize publication text" | summarize-publication(metadata, publication_text) | `references/source-note/summarize_publication.md` |
| "Extract topics from publication text" | extract-topics(metadata, publication_text, summary, curated_topics) | `references/source-note/extract_topics.md` |

If the intent is ambiguous, list matching modes and ask which. Always state the intent, so user can understand what you are doing. In case of ambiguity do not
assume answer, always ask

## Shared conventions (all modes)

- **Wikilinks**: `[[Note-Name]]` (Obsidian style, filename without .md).
- **Dates**: `YYYY-MM-DD`. Timestamps: `YYYY-MM-DD HH:MM` (24-hour, local time).
- **Project log**: same format minus the project column, appended to `Projects/{X}/log.md`.
- **Topic notes**: written to `Topic/{topic}.md`.
- **Source notes**: written to `Source/{source_note}.md`.
- **Log file**: written to `Projects/{project}/log.md`.

### Linear project mapping

The WIKI is the source of truth for project intent and requirements. Linear is the source of truth for execution state.

When linked, each WIKI project stores one clickable Linear project URL in `Projects/{Project}/requirements.md` frontmatter:

```yaml
linear_project: https://linear.app/example/project/project-name
```

The `link-linear` operation writes this property to the Wiki only. It does not modify the Linear project or require a Wiki URL. The WIKI skill does not mirror Linear issue status, assignees, priorities, milestones, deadlines, or comments back into project notes.

When resolving a mapping, use `linear_project` first. If it is absent, search by exact project name as a discovery fallback. If multiple Linear projects are possible matches, ask the user to select one before linking or changing anything.

## Project routing (context-inference + confirm)

Modes that operate on a project must resolve one:

1. **Infer** from recent conversation context (project names mentioned).
2. **Confirm** briefly: `Filing to [[project-name]]. Continue?` — proceed unless the user objects.
3. If nothing inferable, **ask**: list existing folders under `Projects/` through Obsidian CLI and let the user pick.
4. If the chosen project doesn't exist, run **create-project(project_name)** first.

Resolution must use Obsidian CLI file listing with the explicit vault and an exact `Projects` folder scope. Do not access the filesystem through `$SZYMON_WIKI` or rely on the active vault.

## Notes

### Source note

The source note is created when user wants to review a source material - ex. Publication and dump the most important facts, claims and results from it into separate note

- Are immutable
- Must host one source at a time
- May have one source (ex. publication + supplementary methods)
- Filename and source-note identity use the last author surname and publication year (ex. `Source/Tang 2024.md`). The frontmatter `title` and Markdown heading use the exact publication title.

### Topic note

The topic notes are created when user wants to collect information about specific topic across many sources that reference it.

- Are append-only
- Must host one topic at a time
- May have multiple sources
- Must have a title referring to the topic name (ex. `Melanoma`)
- Must refer to `Source note` as the source reference

## Project Workflows

- grill means - perform targeted grilling session with the user

### Create project workflow

```
CREATE PROJECT WORKFLOW(vault, project_name):
  projects = list-projects(vault)

  if exact project_name exists in projects:
    notify-user("project exists")
    STOP

  confirmed = confirm-user(
    "Create project {project_name} with files: " +
    [
      "Projects/{project_name}/log.md",
      "Projects/{project_name}/requirements.md",
      "Projects/{project_name}/meetings.md"
    ]
  )

  if confirmed.confirmed is false:
    STOP

  result = create-project(vault, project_name)

  return result
```

### List projects workflow

Use when the user asks to list Wiki projects.

```
LIST PROJECTS WORKFLOW(vault):
  projects = list-projects(vault)
  return projects
```

### read project {project_name}

```
READ PROJECT WORKFLOW(vault, project_name):
  projects = list-projects(vault)

  if exact project_name does not exist in projects:
    notify-user("project does not exist")
    STOP

  project = find-project(vault, project_name)
  result = summarize-project(vault, project)

  return result
```

### update project {project_name}

```
UPDATE PROJECT WORKFLOW(vault, project_name, changes):
  projects = list-projects(vault)

  if exact project_name does not exist:
    notify-user("project does not exist")
    STOP

  project = find-project(vault, project_name)
  current = summarize-project(vault, project)

  confirmed = confirm-user(
    "Update project {project_name} with: " + changes
  )

  if confirmed.confirmed is false:
    STOP

  result = update-project(vault, project, changes)

  return result
```

### Link Wiki project to Linear workflow

Use when the user asks to link an existing Wiki project to an explicitly identified Linear project.

```
LINK LINEAR WORKFLOW(vault, project_name, linear_project):
  wiki_project = find-project(vault, project_name)

  if wiki_project does not exist:
    notify-user("project does not exist")
    STOP

  linear_project = linear.get-project(linear_project)

  if linear_project does not exist:
    notify-user("Linear project does not exist")
    STOP

  confirmed = confirm-user(
    "Link Wiki project {project_name} to Linear project {linear_project.name}"
  )

  if confirmed.confirmed is false:
    STOP

  result = link-linear(
    vault,
    wiki_project,
    linear_project.url
  )

  return result
```

### Update meeting note workflow

```
UPDATE MEETING NOTE WORKFLOW(vault, project_name, meeting, date, context):
  projects = list-projects(vault)

  if exact project_name does not exist:
    notify-user("project does not exist")
    STOP

  project = find-project(vault, project_name)

  confirmed = confirm-user(
    "Add the meeting summary for {meeting} on {date} to {project_name}"
  )

  if confirmed.confirmed is false:
    STOP

  result = update-meeting-note(
    vault,
    project,
    meeting,
    date,
    context
  )

  log_result = log-project-update(vault, project.path, context)

  if log_result failed:
    notify-user("Meeting note was updated, but the project log update failed")

  return result
```

### Migrate project from {path} to project {project_name}

```
MIGRATE PROJECT WORKFLOW(vault, source_path, project_name):
  projects = list-projects(vault)

  if exact project_name exists in projects:
    notify-user("project exists")
    STOP

  source_content = obsidian.read(vault, source_path)

  migration_plan = grill(user):
    what to preserve
    what to remove
    what to reshape
    where each retained item belongs
    what should be discarded as obsolete

  confirmed = confirm-user(migration_plan)

  if confirmed.confirmed is false:
    STOP

  result = migrate-project(
    vault,
    source_path,
    project_name,
    source_content,
    migration_plan
  )

  return result
```

### Lint project structure for project {project_name}

```
LINT PROJECT WORKFLOW(vault, project_name):
  projects = list-projects(vault)

  if exact project_name does not exist:
    notify-user("project does not exist")
    STOP

  project = find-project(vault, project_name)
  result = lint-project(vault, project)

  return result
```

## PRD Workflows

### Create PRD workflow

Use when the user asks to create a new immutable PRD for an existing Wiki project.

```
CREATE PRD WORKFLOW(vault, project_name, prd_name, context):
  projects = list-projects(vault)

  if exact project_name does not exist in projects:
    notify-user("project does not exist")
    STOP

  project = find-project(vault, project_name)
  prd_name, prd_content = grill(user, prd_name, context)
  date = current local date
  path = "Projects/{project_name}/PRD/{date}-{prd_name}.md"
  prds = list-prds(vault, project.path)

  if exact path exists in prds:
    notify-user("PRD path already exists")
    STOP

  confirmed = confirm-user(
    "Create immutable PRD {path}"
  )

  if confirmed.confirmed is false:
    STOP

  result = create-prd(vault, path, prd_content)

  return result

```

### Read PRD {prd_name} in project {project_name}

```
READ PRD WORKFLOW(vault, project_name, prd_name):

  projects = list-projects(vault)

  if exact project_name does not exist in projects:
    notify-user("project does not exist")
    STOP

  project = find-project(vault, project_name)
  prds = list-prds(vault, project.path)
  prd = exact match for prd_name in prds

  if prd does not exist:
    notify-user("PRD does not exist")
    STOP

  content = query-prd(vault, prd.path)

  return content
```

## Note workflows

### Read source note {source_key}

```text
READ SOURCE NOTE WORKFLOW(vault, source_key):

  note_path = search-source-note(vault, source_key)

  if note_path is null:
    notify-user("Source note does not exist")
    STOP

  content = obsidian.read(vault, note_path)

  return content
```

### Read topic note {topic}

```text
READ TOPIC NOTE WORKFLOW(vault, topic):

  note_path = search-topic-note(vault, topic)

  if note_path is null:
    notify-user("Topic note does not exist")
    STOP

  content = obsidian.read(vault, note_path)

  return content
```

### Search topic note {topic}

```
search-topic-note(vault, topic)
STOP
```

### Create topic note {topic, content, source}

```
If search-topic-note(vault, topic):
  notify-user("Topic note exists")
  STOP
Else:
  create-topic-note(vault, topic, content, source_link)
  STOP
```

### Update topic note {topic, content, source}

```
If not search-topic-note(vault, topic):
  notify-user("Topic note does not exist")
  STOP
Else:
  update-topic-note(vault, topic, content, source_link)
  STOP
```

### Search source note for {publication_path}

```
metadata = extract-publication-metadata(publication_path)
note = search-source-note(vault, metadata.source_key)
If not note:
  notify-user("Source note does not exist")
  STOP
Else:
  note
  STOP
```

### Review publication {publication_path} to source note

```
REVIEW PUBLICATION WORKFLOW(vault, publication_path):

  metadata = extract-publication-metadata(publication_path)

  source_note = search-source-note(vault, metadata.source_key)

  if source_note exists:
    notify-user("A source note already exists for this publication")
    STOP

  publication_text = read-publication(publication_path)

  summary = summarize-publication(metadata, publication_text)

  candidate_topics = extract-topics(metadata, publication_text, summary)

  if candidate_topics.topics is empty:
    notify-user("No substantive topics were detected")

  curated_topics = ask-user-to-select-remove-or-add-topics(candidate_topics)

  topics = extract-topics(
    metadata,
    publication_text,
    summary,
    curated_topics
  )

  confirmed = confirm-user(
    "Create source note with this metadata and summary: " + summary
  )

  if confirmed.confirmed is false:
    STOP

  source_note_path = "Source/" + metadata.source_key + ".md"
  source_note_link = "[[" + metadata.source_key + "]]"
  result = create-source-note(vault, metadata, summary, topics)

  if result failed:
    STOP

  failures = []

  for topic in topics:
    topic_note = search-topic-note(vault, topic.name)

    if topic_note exists:
      result = update-topic-note(vault, topic.name, topic.content, source_note_link)
    else:
      result = create-topic-note(vault, topic.name, topic.content, source_note_link)

    if result failed:
      failures.append(topic.name)

  if failures is not empty:
    notify-user("Some topic-note operations failed: " + failures)

  return {
    "source_note": source_note_path,
    "topics": topics,
    "failures": failures
  }
```
