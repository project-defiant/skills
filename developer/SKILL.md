---
name: developer
description: Develop or implement new functionality, fix bug or answer user questions, optimize spark job in requested repository using linear issue or previous instructions. Use when asked to develop new feature, fix bug in existing codebase.
---

# Develop

# Development flow

1. When working in local repository always start from local worktree as a base to novel developments.
2. Ask user how the worktree shall be named. Names shall include following prefixes

- `feature` -> new feature development
- `fix` -> fixing existing bug
- `chore` -> typo fixes, lining, formatting, README changes
- `refactor` -> refactoring
- `build` -> updates to dockerfile, build process, Makefile
- `ci` -> update to CI/CD pipeline, github actions

Example:

Given we work on new feature you shall create new worktree in `.worktree/feature/new-stuff` with the name `feature/new-stuff` from the `main` branch

```{bash}
git worktree add .worktree/feature/new-stuff -b feature/new-stuff main
```

3. Undestand the task at hand, read linear issue or follow previously described plan by the user
4. Use './tdd/SKILL.md` to do the test driven development
5. Once finished ask if you shall create a pull request to the repository.
6. If user confirms, create new pull request from branch to the base branch, that worktree was based on using `gh`
7. Add the brief description to the pull request, focus on implementation details
8. If started from linear issue, update the issue with link to the pull request and notify user

## Spark optimization

When user asks you to optimize spark job, follow `./spark-optimization/SKILL.md`

## Nextflow pipeline development

When user asks you to contribute to the nextflow pipeline, follow `./nextflow/SKILL.md`

## Improve codebase architecture

When user asks you to refactor or improve codebase architecture, follow `./improve-codebase-architecture/SKILL.md`
