---
name: developer
description: Develop or implement new functionality, fix bug or answer user questions, optimize spark job in requested repository using a WIKI PRD or previous instructions. Use when asked to develop new feature, fix bug in existing codebase.
---

# Develop

# Development flow

1. When working in local repository always start novel developments from a new worktree.
2. Create it with the `worktree` skill, which owns the naming contract (prefixes, layout). Confirm the worktree name with the user before creating it.

3. Undestand the task at hand, read the WIKI PRD or follow previously described plan by the user
4. Use the `tdd` skill to do the test driven development
5. Once finished ask if you shall create a pull request to the repository.
6. If user confirms, create new pull request from branch to the base branch, that worktree was based on using `gh`
7. Add the brief description to the pull request, focus on implementation details
8. If started from a WIKI project, log the pull request link with the `vault` log-project-update mode and notify user

## Spark optimization

When user asks you to optimize spark job, follow `./spark-optimization/SKILL.md`

## Nextflow pipeline development

When user asks you to contribute to the nextflow pipeline, follow `./nextflow/SKILL.md`

## Improve codebase architecture

When user asks you to refactor or improve codebase architecture, use the `improve-codebase-architecture` skill
