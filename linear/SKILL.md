---
name: linear
description: "Managing Linear issues, projects, and milestones. Use when working with Linear tasks, creating issues, updating status, querying projects and milestones."
---

# linear - issue and task management on projects

## Prerequisites

- `$SZYMON_WIKI` must be exported. If unset STOP and tell the user:
  > vault skill requires `$SZYMON_WIKI` to be exported. Set it to the wiki root (e.g. `/Users/ss60/Documents/v/Wiki`) and retry.
- Prefer `ripgrep` (`rg`); fall back to `grep -r` if absent.

## Better ask then regret

Follow the notion, that if the answer is ambiguous can cause misunderstanding, ask user to clarify.

## Main responsibility

There are two locations, where we host the projects:

1. WIKI - project description, requirements and PRD files (single source of truth about the project)
2. Linear - project implementation details (single source of truth about issues linked to projects and alined PRDs to milestones)

Your task is to do the bookkeeping and ensure that the WIKI projects are in sync with the linear projects.

## Mode dispatch

Use following modes when accessing/editing linear project boards.

| Intent (triggers) | mode | reference |
| "Init / create a project in the linear" | create-project(project_name, link_to_wiki_project) | `references/project/create_project.md` |
| "List available projects in the linear" | list-projects() | `references/project/list_project.md` |
| "Query project in the linear" | query-project(project_name) | `references/project/query_project.md` |
| "Sync project between linear and WIKI" | sync-project(project_name, link_to_wiki_project) | `references/project/sync_project.md` |
| "Create a milestone in the linear" | create-milestone(project_name, milestone_name, content) | `references/milestone/create_milestone.md` |
| "Assign issue to milestone" | issue-to-milestone(project_name, milestone_name, issue_id) | `references/milestone/issue_to_milestone.md` |
| "Create issue in project" | issue-to-project(project_name, issue_id, content) | `references/issue/create_issue.md` |
| "Update issue in project" | update-issue(project_name, issue_id, content) | `references/issue/update_issue.md` |

## Shared conventions

- Always first search for project in linear before attempting to create a new project
- If the link between WIKI project and listed linear projects is not obvious, ask user for conformation what is correct project
- Linear project shall have a link to the wiki project (relative path from the `$SZYMON_WIKI` to the project)
- Whenever the project in WIKI is missing a linear project, ask user if we should create a linear project for that WIKI project
- Ensure that the linear project exist with sync to the WIKI projects, use `../vault` skills to reference the WIKI.
- When finished grilling session with user and filled a PRD document under WIKI's project, ask user if they want to transfer the knowledge from PRD to linear issues.
- Ensure that linear issues are filled completely
  - responsible user
  - deadline
  - milestone
  - project
  - priority
  - status
- ALWAYS verify with the user the issue before you write it into linear and iterate until user approves the transfer or stop when user asks you not to put the issue to the linear
- ALWAYS after transferring all issues from a PRD document to linear, return to the user the full list of links to the newly created issues, so they can verify them directly.
- NEVER start the transfer or do any changes to the issues without user explicit permissions
