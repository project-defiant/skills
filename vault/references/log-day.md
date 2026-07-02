# Mode: log-day

Append an end-of-day work summary to the global `Wiki/log.md` and to each touched project's `log.md`.

## Inputs

- **summary** (optional): one line per project. If missing, ask the user or infer from git activity.
- **projects** (optional list): projects touched today. If missing, infer.

## Steps

1. Compute `TODAY=YYYY-MM-DD` and `NOW=YYYY-MM-DD HH:MM`.
2. Determine touched projects:
   - Run `git -C "$SZYMON_WIKI" log --since="$TODAY 00:00" --name-only --pretty=format: | grep -E "^Projects/" | cut -d/ -f2 | sort -u` (adjust for your shell). Anything that surfaces is a candidate.
   - If the user mentions code repos in conversation, also inspect those: `git -C {repo} log --since="$TODAY 00:00" --oneline`.
   - Merge with any projects the user names explicitly.
3. If no projects were touched, ask the user which project(s) today's work belongs to. Offer the list of existing folders under `$SZYMON_WIKI/Projects/`.
4. For each project, elicit or confirm the one-line summary. Keep it under ~25 words.
5. Append one line PER project to `$SZYMON_WIKI/log.md`:
   `- YYYY-MM-DD HH:MM — [[{project}]] — log-day — {one-line}`
6. Append one line PER project to `$SZYMON_WIKI/Projects/{project}/log.md`:
   `- YYYY-MM-DD HH:MM — log-day — {one-line}`
7. If the user offers a longer narrative for a specific project, DO NOT invent a new file — instead, offer to run `log-status` for that project so the narrative lands in `ImplementationStatus/YYYY-MM-DD.md` where it belongs.
8. Report the number of log entries appended and to which files.

## Notes

- log-day is deliberately narrow: one line per project per invocation. Rich content flows through `log-status` or `log-decision`.
- If the user says "log today" without mentioning any project, propose the inferred list first before writing anything.
- Timestamp uses the local clock at invocation time.
