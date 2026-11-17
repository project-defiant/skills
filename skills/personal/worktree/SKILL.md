---
name: worktree
description: Bare-repo worktree hub with frozen branch prefixes (feat, fix, chore, perf, run). Use when cloning a repo as a worktree hub, adding, listing or removing a worktree, or choosing a branch name for one.
argument-hint: "init <repo-url> [dir] | add <prefix> <slug> [base] | rm <prefix>/<slug> | ls"
allowed-tools: Bash
---

# worktree

Every repo is a **hub**: one bare repository in `.bare/`, a one-line `.git` file pointing at it, and each branch checked out as a directory under the hub, nested by prefix.

```
<hub>/
├── .bare/            bare repository (shared history, config, hooks)
├── .git              "gitdir: ./.bare"
├── main/             default branch
├── feat/
│   └── login-form/   branch feat/login-form
└── fix/
    └── null-gene/    branch fix/null-gene
```

Drive the hub through [`scripts/wt.sh`](scripts/wt.sh) (path relative to this skill's base directory). It enforces the naming contract below, so every worktree goes through it.

## Naming contract

A worktree lives at `<hub>/<prefix>/<slug>`, on the branch of the same name `<prefix>/<slug>`. The prefix is frozen to one of:

| Prefix  | Use for                                                   |
| ------- | --------------------------------------------------------- |
| `feat`  | new capability                                            |
| `fix`   | bug fix                                                   |
| `chore` | tooling, deps, CI, refactors with no behaviour change     |
| `perf`  | performance work                                          |
| `run`   | a pipeline run (e.g. a Nextflow or Spark run pinned to a config/code state) |

The slug is kebab-case (`[a-z0-9]` words joined by single hyphens), naming the work in 2–4 words. The default-branch worktree (`main/`) is the one exception, created by `init`.

When the user's request does not name the prefix, pick it from the table and state the chosen name in your reply. When the work fits two prefixes, ask.

## Steps

1. **Locate the hub.** Run `wt.sh ls`. A worktree list means you are in a hub. An error saying "not a bare-repo hub" means the repo is a normal clone: run `init` into a fresh directory with the remote URL from `git remote get-url origin` and leave the old clone in place. Do not convert it.
2. **Act.**
   - `wt.sh init <repo-url> [dir]` creates the hub, sets the fetch refspec, fetches, and adds the default-branch worktree.
   - `wt.sh add <prefix> <slug> [base]` checks out an existing local or `origin` branch of that name, or else creates one from `base` (default `origin/<default-branch>`).
   - `wt.sh rm <prefix>/<slug>` removes the worktree and prunes. The branch is kept. Pass `--force` only when the user confirms that uncommitted changes in it can be lost.
3. **Done** when `wt.sh ls` shows the expected worktree at `<hub>/<prefix>/<slug>` on `[<prefix>/<slug>]`, and further work runs with that directory as its cwd.

## Gotchas

- **Blind clone.** A bare clone has no `remote.origin.fetch` refspec, so `git fetch` never creates `origin/*` refs. `init` sets it. For a hub made by hand, run `git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"`.
- **Removal goes through `wt.sh rm`** (or `git worktree remove`). A directory deleted with `rm -rf` stays registered until `git worktree prune`.
- **One branch, one worktree.** Git refuses to check out a branch already checked out in another worktree. `cd` to the existing worktree instead.
- **Untracked setup is per worktree.** `.venv/`, `node_modules/`, `.env` and other untracked files do not carry over: set them up again in each new worktree (e.g. `uv sync`).
