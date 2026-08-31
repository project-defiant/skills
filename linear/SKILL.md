---
name: linear
description: "Manage Linear projects, milestones, and issues through the connected Linear connector. Use when creating, listing, reading, updating, or assigning Linear projects, milestones, and issues."
---

# linear - issue and task management on projects

## Prerequisites

- The Linear connector must be installed, connected, and authenticated. If it is unavailable, stop and tell the user that the Linear connector is required before using this skill.

## Better ask then regret

Follow the notion, that if the answer is ambiguous can cause misunderstanding, ask user to clarify.

## Main responsibility

This skill manages Linear projects, milestones, and issues. Workflows orchestrate user interaction; reference files describe the atomic Linear operations they invoke.

## Mode dispatch

Use following modes when accessing/editing linear project boards.

| Intent (triggers) | mode | reference |
| "Create a project in Linear" | create-project(name, content) | `references/project/create_project.md` |
| "List available projects in Linear" | list-projects() | `references/project/list_project.md` |
| "Get a project in Linear" | get-project(project) | `references/project/query_project.md` |
| "List milestones in a project" | list-milestones(project) | `references/milestone/list_milestones.md` |
| "Get a milestone in a project" | get-milestone(project, milestone) | `references/milestone/read_milestone.md` |
| "Create a milestone in a project" | create-milestone(project, name, content?, targetDate?) | `references/milestone/create_milestone.md` |
| "Read an issue in a project" | read-issue(project, issue) | `references/issue/read_issue.md` |
| "List issues in a project" | list-issues(project) | `references/issue/list_issues.md` |
| "List issue statuses for a team" | list-issue-statuses(team) | `references/issue/list_statuses.md` |
| "Assign an issue to a milestone" | issue-to-milestone(project, milestone, issue) | `references/milestone/issue_to_milestone.md` |
| "Create an issue in a project" | create-issue(project, title, content?, milestone?, dueDate?, priority?, status?, blockedBy?, blocks?) | `references/issue/create_issue.md` |
| "Update an issue in a project" | update-issue(project, issue, changes) | `references/issue/update_issue.md` |

## Shared conventions

- Always use the workflow mode when a user asks to create or list projects.
- A project name and brief description may come from conversation context or direct user input.
- A project creation requires user confirmation before the atomic create operation is invoked.
- The project lead is always Szymon Szyszkowski.
- Use the `Szymon` team by default when creating a project; do not ask the user to select a team.
- Every issue is assigned to Szymon Szyszkowski and a project. Milestone, deadline, priority, and status are optional and are set when supplied or selected by the user.
- ALWAYS verify with the user the issue before you write it into linear and iterate until user approves the transfer or stop when user asks you not to put the issue to the linear
- ALWAYS after transferring all issues from a PRD document to linear, return to the user the full list of links to the newly created issues, so they can verify them directly.
- NEVER start the transfer or do any changes to the issues without user explicit permissions

## Project workflows

### Create project workflow

Use when the user asks to create a new Linear project.

```text
CREATE PROJECT WORKFLOW(name, content):
  confirmed = confirm-user("Create Linear project " + name + " with description: " + content)
  if confirmed.confirmed is false:
    STOP

  projects = list-projects()
  if any project.name == name in projects:
    notify-user("project exists")
    STOP
  else:
    result = create-project(name, content)
    return result
```

### List projects workflow

Use when the user asks to see available open Linear projects.

```text
LIST PROJECTS WORKFLOW():
  list-projects()
```

### Create milestone workflow

Use when the user asks to create a milestone in an existing Linear project.

```text
CREATE MILESTONE WORKFLOW(project, name, content?, targetDate?):
  project = get-project(project)

  if project does not exist:
    notify-user("project does not exist")
    stop

  milestones = list-milestones(project.name)

  if any milestone.name == name in milestones:
    notify-user("milestone exists")
    stop

  confirmed = confirm-user("Create milestone " + name + " in " + project.name)
  if confirmed.confirmed is false:
    stop

  result = create-milestone(project.name, name, content?, targetDate?)
  return result
```

### Issue-to-milestone workflow

Use when the user asks to assign an existing Linear issue to an existing project milestone.

```text
ISSUE TO MILESTONE WORKFLOW(project, milestone, issue):
  project = get-project(project)

  if project does not exist:
    notify-user("project does not exist")
    stop

  milestone = get-milestone(project.name, milestone)

  if milestone does not exist:
    notify-user("milestone does not exist")
    stop

  issue = read-issue(project.name, issue)

  if issue does not exist:
    notify-user("issue does not exist")
    stop

  confirmed = confirm-user("Assign issue " + issue.title + " to milestone " + milestone.name)
  if confirmed.confirmed is false:
    stop

  result = issue-to-milestone(project.name, milestone, issue)
  return result
```

### Create issue workflow

Use when the user asks to create a new issue in an existing Linear project.

```text
CREATE ISSUE WORKFLOW(project, title, content?, milestone?, dueDate?, priority?, status?, blockedBy?, blocks?):
  project = get-project(project)

  if project does not exist:
    notify-user("project does not exist")
    stop

  if milestone is provided:
    milestone = get-milestone(project.name, milestone)

    if milestone does not exist:
      notify-user("milestone does not exist")
      stop

  issues = list-issues(project.name)

  if any issue.title == title in issues:
    notify-user("issue exists")
    stop

  if status is provided:
    statuses = list-issue-statuses("Szymon")
    status = status from statuses

  confirmed = confirm-user(
    "Create issue " + title + " in " + project.name +
    " with content and fields: " +
    {content, milestone, dueDate, priority, status, blockedBy, blocks}
  )
  if confirmed.confirmed is false:
    stop

  result = create-issue(project.name, title, content?, milestone?, dueDate?, priority?, status?, blockedBy?, blocks?)
  return result
```

### Read issue workflow

Use when the user asks to inspect an existing issue in a specific Linear project.

```text
READ ISSUE WORKFLOW(project, issue):
  project = get-project(project)

  if project does not exist:
    notify-user("project does not exist")
    stop

  issues = list-issues(project.name)
  issue = find issue in issues

  if issue does not exist:
    notify-user("issue does not exist")
    stop

  return issue
```

### Update issue workflow

Use when the user asks to change an existing issue in a specific Linear project.

```text
UPDATE ISSUE WORKFLOW(project, issue, changes):
  issue = read-issue(project, issue)

  if issue does not exist:
    stop

  confirmed = confirm-user("Update issue " + issue.title + " with: " + changes)
  if confirmed.confirmed is false:
    stop

  result = update-issue(project.name, issue, changes)
  return result
```

`create-project(name, content)` and `list-projects()` in the workflows are atomic operations defined in the referenced files. The workflows contain the user-facing decision logic; the reference files contain only the Linear operation details.
