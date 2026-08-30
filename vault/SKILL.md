---

name: vault
description: Manage user's Obsidian LLM-wiki at $SZYMON_WIKI. Use when the user's request contains `vault` or `wiki` AND one of these intents: create, find, list, update, migrate or summarize project, create, update project requirements, create new source or topic note, review an article in the wiki

---

# vault - Obsidian LLM-wiki skill

## Prerequisites

- `$SZYMON_WIKI` must be exported. If unset, STOP and tell the user:
  > vault skill requires `$SZYMON_WIKI` to be exported. Set it to the wiki root (e.g. `/Users/ss60/Documents/v/Wiki`) and retry.
- Prefer `ripgrep` (`rg`); fall back to `grep -r` if absent.

## Better ask then regret

Follow the notion, that if the answer is ambiguous can cause misunderstanding, ask user to clarify.

## Project structure

Project structure in the vault is specified in `references/project/project_structure.md`

```
$SZYMON_WIKI/
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
> Agent: I need to get the project name before I can call `create-project(project_name)` mode to generate new project in the wiki
> add `New-project` to the wiki
> Agent: creating new project (`New-project`) in the wiki

| Intent (triggers) | mode | reference |
| "Init / scaffold / create a project in the wiki" | create-project(project_name) | `references/project/create_project.md` |
| "Create project requirements file in project folder" | create-project-requirements(project_name, content) | `references/project/create_requirements.md` |
| "Find existing project in the wiki" | find-project(project_name) | `references/project/find_project.md` |
| "link Wiki project to linear project | link-linear(project_name) | `references/project/link_linear_project.md` |
| "List all projects in the wiki" | list-projects() | `references/project/list_projects.md` |
| "Migrate existing project structure to `Project structure`" | migrate-project(project_name) | `references/project/migrate_project.md` |
| "Summarize work done over project" | summarize-project(project_name) | `references/project/summarize_project.md` |
| "Update existing project" | update-project(project) | `references/project/update_project.md` |
| "Update existing project requirements" | update-requirements(project_name, content) | `references/project/update_requirements.md` |
| "Verify project structure and report issues" | lint-project(project_name) | `references/project/lint_project.md` |
| "Create PRD document in the project" | create-prd(project_name, prd, content) | `references/prd/create_prd.md` |
| "List existing PRD documents in the project" | list-prds(project_name) | `references/prd/list_prd.md` |
| "Query existing PRD in the project" | query-prd(project_name, prd)| `references/prd/query_prd.md` |
| "Collect feedback from meeting user has attended linked to project | summarize-feedback(project_name, meeting, date, content) | `references/meeting/summarize_meeting.md` |
| "Review a publication and prepare source-note" | review-publication(path_to_publication) | `references/source-note/create_source_node.md` |
| "Search for the source note linked to a publication" | search-source-note(publication) | `references/source-note/search_source_notes.md` |
| "Create a topic-note from source" | create-topic-note(topic, content, source) | `references/topic-note/create_topic_note.md` |
| "Update a topic-note with information from source" | update-topic-note(topic, content, source) | `references/topic-note/update_topic_note.md` |
| "Search for topic in topic-notes" | search-topic-note(topic) | `references/topic-note/search_topic_notes.md` |
| "Log project update" | log-project-update(project_name, content) | `references/project/log_project_update.md` |
| "Extract publication metadata from pdf" | extract-pub-metadata(publication_path) | `references/source-note/extract_publication_metadata.md` |
| "Notify user about alert" | notify-user(alert) | `references/notify_user.md` |
| "Find topics in publication" | find-topics-in-pub(publication_path) | `references/source-note/find_topics_in_publication.md` |
| "Extract topic content from publication" | extract-topic-content(publication_path) | `references/source-note/extract_topic_content_from_publication.md` |

If the intent is ambiguous, list matching modes and ask which. Always state the intent, so user can understand what you are doing. In case of ambiguity do not
assume answer, always ask

## Shared conventions (all modes)

- **Wikilinks**: `[[Note-Name]]` (Obsidian style, filename without .md).
- **Dates**: `YYYY-MM-DD`. Timestamps: `YYYY-MM-DD HH:MM` (24-hour, local time).
- **Project log**: same format minus the project column, appended to `$SZYMON_WIKI/Projects/{X}/log.md`.
- **Topic notes**: written to `$SZYMON_WIKI/topic-notes`
- **Source notes**: written to `$SZYMON_WIKI/source-notes`
- **Log file**: written to `$SZYMON_WIKI/projects/${project}/log.md`

### Linear project mapping

The WIKI is the source of truth for project intent and requirements. Linear is the source of truth for execution state.

Each WIKI project must store its Linear relationship in `Projects/{Project}/requirements.md` frontmatter when linked:

```yaml
linear_project_id: <Linear project ID>
linear_project_url: <Linear project URL>
```

The linked Linear project must store the absolute URL of the WIKI project in its project URL field. The WIKI skill does not mirror Linear issue status, assignees, priorities, milestones, deadlines, or comments back into project notes.

When resolving a mapping, use `linear_project_id` first. If it is absent, search by exact project name as a discovery fallback. If multiple Linear projects are possible matches, ask the user to select one before linking or changing anything.

## Project routing (context-inference + confirm)

Modes that operate on a project must resolve one:

1. **Infer** from recent conversation context (project names mentioned).
2. **Confirm** briefly: `Filing to [[project-name]]. Continue?` — proceed unless the user objects.
3. If nothing inferable, **ask**: list existing folders under `$SZYMON_WIKI/Projects/` and let the user pick.
4. If the chosen project doesn't exist, run **create-project(project_name)** first.

## Notes

### Source note

The source note is created when user wants to review a source material - ex. Publication and dump the most important facts, claims and results from it into separate note

- Are immutable
- Must host one source at a time
- May have one source (ex. publication + supplementary methods)
- Title MUST refer to the last author surname and the publication year (ex. `Tang 2024`)

### Topic note

The topic notes are created when user wants to collect information about specific topic across many sources that reference it.

- Are append-only
- Must host one topic at a time
- May have multiple sources
- Must have a title referring to the topic name (ex. `Melanoma`)
- Must refer to `Source note` as the source reference

## Project Workflows

- grill means - perform targeted grilling session with the user

### create project {project_name}

```
If project_name in list-projects():
  notify-user("project exists")
  STOP
ELSE:
  create-project(project_name)
  content = grill(user)
  create-project-requirements(project_name, content)
  log-project-update(project_name, content)
  STOP
```

### read project {project_name}

```
If project_name not in list-projects():
  create-project(project_name)
  content = grill(user)
  create-project-requirements(project_name, content)
  log-project-update(project_name, content)

Else:
  find-project(project_name)
  summarize-project(project_name)
  STOP
```

### update project {project_name}

```
If project_name not in list-projects():
  notify-user("missing project")
  STOP
Else:
  find_project(project_name)
  new_content = grill(user)
  update-project(project_name, new_content)
  new_requirements = grill(user)
  update-project-requirements(project_name, new_requirements)
  log-project-update(project_name, (new_content + new_requirements))
  STOP
```

### link existing project {project_name} to linear project

```
If project_name not in list-projects():
  notify-user("missing project")
  STOP
Else:
  find_project(project_name)
  link-linear(project_name)
  STOP
```

### Update meeting notes for project {project_name}

```
If project_name not in list-projects():
  notify-user("missing project")
  STOP
Else:
  find_project(project_name)
  content, meeting = grill(user)
  summarize-feedback(project_name, meeting, date, content)
  STOP
```

### Migrate project from {path} to project {project_name}

```
If project_name in list-projects():
  notify-user("project exists")
  STOP
Else:
  bulk-read(path)
  WORKFLOW(create project {project_name})
  STOP
```

### Update requirements to project {project_name}

```
If project_name not in list-projects():
  notify-user("missing project")
  STOP
Else:
  find-project(project_name)
  new_requirements = grill(user)
  update-project-requirements(project_name, new_requirements)
  log-project(project_name)
  STOP
```

### Lint project structure for project {project_name}

```
If project_name not in list-projects():
  notify-user("missing project")
  STOP
Else:
  find-project(project_name)
  lint-project(project_name)
  STOP
```

## PRD Workflows

### Create a PRD in project {project_name}

```
If project_name not in list-projects():
  notify-user("missing project")
  STOP
Else:
  find-project(project_name)
  If prd in list-prds(project_name):
    notify-user("PRD already exists")
    STOP
  Else:
    prd, content = grill(user)
    create-prd(project_name, prd, content)
    log-project(project_name)
    STOP

```

### Read a PRD in project {project_name}

```
If project_name not in list-projects():
  notify-user("missing project")
  STOP
Else:
  find-project(project_name)
  If prd not in list-prds(project_name):
    notify-user("PRD do not exist")
    STOP
  Else:
    query-prd(project_name, prd)
    STOP
```

## Note workflows

### Search topic note {topic}

```
search-topic-note(topic)
STOP
```

### Create topic note {topic, content, source}

```
If search-topic-note(topic):
  notify-user("Topic note exists")
  STOP
Else:
  create-topic-note(topic, content, source)
  STOP
```

### Update topic note {topic, content, source}

```
If not search-topic-note(topic):
  notify-user("Topic note does not exist")
  STOP
Else:
  update-topic-note(topic, content, source)
  STOP
```

### Search source note for {publication_path}

```
publication_date, last_author = extract-pub-metadata(publication_path)
note = search-source-note(publication_date, last_author)
If not note:
  notify-user("Source note does not exist")
  STOP
Else:
  note
  STOP
```

### Review publication {publication_path} to source note

```
publication_date, last_author = extract-pub-metadata(publication_path)
note = search-source-note(publication_date, last_author)
If note:
  notify-user("Source note exist")
  STOP
Else:
  pub_content = review-publication(publication_path)
  create-source-note(publication_date, last_author, pub_content)
  topics = find-topics-in-pub(publication_path)
  for topic in topics:
    content = extract-topic-content(publication_path)
    Try:
      WORKFLOW(Create topic note {topic, content, source})
    Except Topic note exist:
      WORKFLOW(Update topic note {topic, content, source})
  STOP
```
