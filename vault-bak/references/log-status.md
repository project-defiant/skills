# Mode: log-status

Snapshot the implementation state of a project: where the code lives, current branch, latest commit, status, next steps. Writes a dated file and appends to the project's CHANGELOG index.

## Inputs

- **project** (required, via routing).
- **code_location** (optional): repo URL or local path. Infer from context if possible.
- **branch** (optional): current git branch. Infer with `git -C {code_location} branch --show-current`.
- **last_commit** (optional): short hash + one-line message. Infer with `git -C {code_location} log -1 --oneline`.
- **status** (optional): one of `planning | active | blocked | dormant | done`. Read current from project `index.md` frontmatter; only change if the user says so.
- **summary** (required): one-line change since previous snapshot.
- **next_steps** (optional): bullets.
- **notes** (optional): free-form paragraphs.

## Steps

1. Resolve **project**. If it doesn't exist, run `project-init` first.
2. Set `DEST="$SZYMON_WIKI/Projects/{project}"`.
3. Gather fields:
   - Read current `status` from `$DEST/index.md` frontmatter.
   - If `code_location` known, shell out for `branch` and `last_commit`.
   - If a field can't be inferred and the user hasn't provided it, ask before proceeding.
4. If the user wants to change `status`, confirm the transition explicitly:
   > Change status from `{old}` to `{new}`? (y/N)
   Only update `$DEST/index.md` frontmatter after explicit yes.
5. Write `$DEST/ImplementationStatus/YYYY-MM-DD.md` from the template below.
   - If a file with that date already exists, append `-2`, `-3`, … to the filename.
6. Append to `$DEST/ImplementationStatus/CHANGELOG.md`:
   `- YYYY-MM-DD — {summary} — [[YYYY-MM-DD]]`
7. Append project log entry:
   `- YYYY-MM-DD HH:MM — log-status — {summary} — [[YYYY-MM-DD]]`
8. Append global log entry:
   `- YYYY-MM-DD HH:MM — [[{project}]] — log-status — {summary} — [[YYYY-MM-DD]]`
9. **GitHub sync** (only if `github_repo` is set in `$DEST/index.md` frontmatter):
   a. Read `github_repo` and `github_issues` from the frontmatter.
   b. If `github_repo` is empty OR `github_issues` is empty, skip this step.
   c. Check `gh` availability with `gh auth status`. If it fails or `gh` is not installed, print `(gh unavailable — skipping GitHub sync)` and continue to step 10. Do NOT edit the GH section on failure.
   d. For each issue number `N` in `github_issues`, run:
      `gh issue view {N} --repo {github_repo} --json number,state,title,assignees,updatedAt`
      Collect the JSON results. If one issue fails, keep going with the others and note the failure.
   e. Replace the content BETWEEN the `<!-- GH-SYNC-START -->` and `<!-- GH-SYNC-END -->` markers in `$DEST/index.md` with:
      ~~~
      _Synced {YYYY-MM-DD HH:MM}._

      - #{N} [{state}] {title} — {assignees_joined_or_"unassigned"}
      - ...
      ~~~
      Keep the markers themselves in place. If any issues failed, add a `_Skipped: #A, #B (fetch failed)._` line under the timestamp.
10. Report all paths to the user, including whether GH sync ran (and its issue count).

## Template

### `$DEST/ImplementationStatus/YYYY-MM-DD.md`

~~~
---
title: Status — {project} — {YYYY-MM-DD}
kind: status-snapshot
project: [[{project}]]
date: {YYYY-MM-DD}
status: {status}
---

# Status — {project} — {YYYY-MM-DD}

- **Code location**: {code_location}
- **Branch**: `{branch}`
- **Last commit**: `{last_commit}`
- **Status**: {status}

## Summary

{one-line}

## Detail

{notes}

## Next steps

- {next step}
- ...
~~~

## Notes

- Status snapshots are append-only history. Do not edit past dated files — write a new one for corrections.
- CHANGELOG.md acts as the project's status `index.md` for `ImplementationStatus/` — always keep it in sync.
- If `code_location` is unknown, leave the field blank in the template rather than fabricating one.
