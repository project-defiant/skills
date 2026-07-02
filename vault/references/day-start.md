# Mode: day-start

Morning ritual. Print a compact summary of the wiki's projects grouped by status and sorted by priority, followed by a next-action suggestion.

**day-start is STRICTLY READ-ONLY.** It does not write, log, sync, or lint. Everything it shows is snapshot data pulled from files that other modes maintain.

## Trigger phrasings

- `standup`, `it's time for the standup`, `standup time`
- `day-start the wiki`, `wiki day-start`
- `morning wiki`, `wiki morning`
- `focus for today` (only when paired with "wiki" or "vault")

Note: `standup` is the ONE trigger that fires the vault skill without needing "vault"/"wiki" in the request — this is documented as an exception in `SKILL.md`.

## Inputs

None.

## Steps

1. Read `$SZYMON_WIKI/index.md` — get the enumerated project list from its `## Projects` section.
2. For each project folder under `$SZYMON_WIKI/Projects/`:
   - Read the project's `index.md`.
   - Extract from frontmatter: `status`, `priority` (default `medium` if missing), `github_repo`, `github_issues`.
   - Extract last-snapshot date: the highest `YYYY-MM-DD.md` filename under `ImplementationStatus/` (if any).
   - Extract open-issue count: count lines matching `- #\d+ \[open\]` between the `<!-- GH-SYNC-START -->` / `<!-- GH-SYNC-END -->` markers. If the markers are absent or empty, mark as `issues not linked`.
   - Extract `blocked_since`: if status is `blocked`, use the date of the most recent status snapshot where status was set to blocked (best-effort: use last-snapshot date; if unknown, omit the date).
3. Partition projects by status:
   - **Group A — Active + Planning**: `status ∈ {active, planning}`.
   - **Group B — Blocked**: `status = blocked`.
   - **Hidden**: `status ∈ {dormant, done}` — do NOT include in the output.
4. Sort:
   - Group A: primary key priority (`high` > `medium` > `low`); tie-break by most-recent last-snapshot descending.
   - Group B: most-recent last-snapshot descending.
5. Identify **top priority**: the FIRST entry of Group A. If Group A is empty, top priority is the FIRST entry of Group B. If both empty, no top priority.
6. Render the report using the template below.
7. Print the report to the user. **Do not write any files.**

## Output template

~~~
Day-start — {YYYY-MM-DD Ddd}

Active + Planning (by priority)
  high
    · [[{project}]] — {status} — {issues_display} — last snapshot {date_or_"never"}
    · ...
    (or "(none)" if empty)
  medium
    · ...
    (or "(none)" if empty)
  low
    · ...
    (or "(none)" if empty)

Blocked
  · [[{project}]] — blocked{" since " + date if known} — {issues_display}
  (or "(none)" if empty)

──
Top priority: [[{project}]] ({priority}, {issues_display}, last snapshot {date})
Run `log-status` on it? (y/N)
~~~

`{issues_display}` is:
- `{N} open issues` when `github_issues` non-empty and sync ran
- `issues not linked` when `github_issues` is empty or `github_repo` unset
- `sync stale` when markers exist but no `_Synced ..._` timestamp is found

## Edge cases

- **No projects at all**: print `No projects yet — run project-init to create one.`
- **Group A and Group B both empty** (all dormant/done): print `All projects are dormant or done — nothing to focus on. Consider revisiting archived projects or starting a new one.`
- **Missing `priority`** on a project: treat as `medium` and include normally.
- **Missing `## GitHub` section or markers**: display `issues not linked`.
- **No `ImplementationStatus/YYYY-MM-DD.md` files** in a project: display `never` for last-snapshot.

## Notes

- Data freshness: GitHub issue counts and states are as fresh as the last `log-status` invocation for that project. day-start does NOT re-fetch from GitHub.
- The next-action suggestion is a soft nudge, not a mandate. If the user ignores or redirects it, do not push.
- If Group B contains items, don't skip mentioning them — blocked projects are exactly the kind of thing you want visible in the morning.
