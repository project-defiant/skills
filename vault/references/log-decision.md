# Mode: log-decision

Record a planning decision into a project's `Plan/` folder. Use for outputs from planning-heavy skills (superpowers, to_prd, to_issues) and for any decision that shapes future direction.

## Inputs

- **decision** (required): the decision itself, in the user's words.
- **project** (optional): resolved via project routing.
- **rationale** (optional): why this decision, why not the alternatives.
- **alternatives** (optional): list of alternatives considered.
- **short_title** (optional): 3–6 word summary used as the filename slug. Derive from `decision` if missing.

## Steps

1. Resolve **project**. If it doesn't exist, run `project-init` first.
2. Set `DEST="$SZYMON_WIKI/Projects/{project}"`.
3. Derive **slug** from `short_title` (lowercase, dashes, alphanumeric only, max 60 chars).
4. Write `$DEST/Plan/YYYY-MM-DD-{slug}.md` from the template below.
5. Update `$DEST/index.md`:
   - Under `## Plan`, replace the placeholder if still present.
   - Append `- [[YYYY-MM-DD-{slug}]] — {short_title}`.
6. Append project log entry:
   `- YYYY-MM-DD HH:MM — log-decision — {short_title} — [[YYYY-MM-DD-{slug}]]`
7. Append global log entry:
   `- YYYY-MM-DD HH:MM — [[{project}]] — log-decision — {short_title} — [[YYYY-MM-DD-{slug}]]`
8. Report the created file path to the user.

## Template

### `$DEST/Plan/YYYY-MM-DD-{slug}.md`

~~~
---
title: {short_title}
kind: decision
project: [[{project}]]
date: {YYYY-MM-DD}
tags: []
---

# {short_title}

**Decision**: {decision text}

## Rationale

{rationale — why this, why now}

## Alternatives considered

- {alternative} — {why rejected}
- ...

## Consequences

- {what changes as a result}
- {what to watch for}

## Related

- ...
~~~

## Notes

- Decisions are append-only. If a later decision reverses this one, write a NEW decision file that wikilinks back to this one under "Related"; do not edit history.
- If the caller has structured artifacts from `to_prd` or `to_issues`, either attach them under `Plan/` alongside this decision file or wikilink them from the "Related" section.
