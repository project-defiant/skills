---
name: vault
description: Manages the user's Obsidian LLM-wiki at $SZYMON_WIKI following Andrej Karpathy's LLM-wiki pattern (raw sources, project-scoped knowledge, entity pages, index/log spine). Use when the user's request contains "vault" or "wiki" AND one of these intents: project-init, ingest-source, log-day, log-decision, log-status, query, lint. ALSO use for the day-start mode when the user says "standup" (e.g. "it's time for the standup", "standup time") — day-start is the ONLY mode that triggers on "standup" without "vault"/"wiki". Does NOT touch the wider Obsidian vault outside $SZYMON_WIKI. Does NOT replace Claude Code's private auto-memory.
---

# vault — Obsidian LLM-wiki skill

## Prerequisites

- `$SZYMON_WIKI` must be exported. If unset, STOP and tell the user:
  > vault skill requires `$SZYMON_WIKI` to be exported. Set it to the wiki root (e.g. `/Users/ss60/Documents/v/Wiki`) and retry.
- Prefer `ripgrep` (`rg`); fall back to `grep -r` if absent.

## Vault layout (read + write scope = `$SZYMON_WIKI` only)

```
$SZYMON_WIKI/
├── index.md                    # global catalog
├── log.md                      # global chronological flat log
├── KnowledgeBase/              # cross-project entity pages
└── Projects/{Project}/
    ├── index.md                # Karpathy-lite frontmatter
    ├── log.md                  # project chronological
    ├── Plan/                   # planning decisions
    ├── Research/
    │   ├── sources/            # raw IMMUTABLE ingested content
    │   └── <summaries>
    ├── ImplementationStatus/
    │   ├── CHANGELOG.md        # wikilink-index of dated notes
    │   └── YYYY-MM-DD.md
    └── Meetings/
```

## Mode dispatch

Match the user's request against the intents below and READ the matching reference file before acting. Do not act from memory of previous invocations — always load the reference.

| Intent (paraphrased triggers)                                                   | Mode          | Reference                     |
| ------------------------------------------------------------------------------- | ------------- | ----------------------------- |
| "init / scaffold / create a project in the wiki"                                | project-init  | `references/project-init.md`  |
| "ingest / add / save this URL/PDF/file to the wiki"                             | ingest-source | `references/ingest-source.md` |
| "log today to the wiki" / "end of day wiki log"                                 | log-day       | `references/log-day.md`       |
| "log this decision" / "file this plan to the wiki"                              | log-decision  | `references/log-decision.md`  |
| "log wiki status" / "snapshot X status"                                         | log-status    | `references/log-status.md`    |
| "query the wiki" / "what do I know about X in the wiki"                         | query         | `references/query.md`         |
| "lint / check the wiki"                                                         | lint          | `references/lint.md`          |
| "standup" / "it's time for the standup" / "day-start the wiki" / "morning wiki" | day-start     | `references/day-start.md`     |

If the intent is ambiguous, list matching modes and ask which.

## Shared conventions (all modes)

- **Wikilinks**: `[[Note-Name]]` (Obsidian style, filename without .md).
- **Dates**: `YYYY-MM-DD`. Timestamps: `YYYY-MM-DD HH:MM` (24-hour, local time).
- **Sources are IMMUTABLE**: once written under `Research/sources/`, never edit — write a new summary instead.
- **Global log**: every mode that touches a project MUST append one line to `$SZYMON_WIKI/log.md`:
  `- YYYY-MM-DD HH:MM — [[project-name]] — <mode> — one-line — [[detail-note]]`
- **Project log**: same format minus the project column, appended to `$SZYMON_WIKI/Projects/{X}/log.md`.
- **KB copy-on-first-use**: when a mode references a concept whose file exists in `/Users/ss60/Documents/v/KnowledgeBase/` but NOT in `$SZYMON_WIKI/KnowledgeBase/`, OFFER to copy it. Never auto-copy.

## Project routing (context-inference + confirm)

Modes that operate on a project (ingest-source, log-day, log-decision, log-status) must resolve one:

1. **Infer** from recent conversation context (project names mentioned, files edited, active branch of a nearby repo).
2. **Confirm** briefly: `Filing to [[project-name]]. Continue?` — proceed unless the user objects.
3. If nothing inferable, **ask**: list existing folders under `$SZYMON_WIKI/Projects/` and let the user pick.
4. If the chosen project doesn't exist, run **project-init** first.

## Frontmatter schema (project `index.md`)

```yaml
---
title: Project Name
status: planning # planning | active | blocked | dormant | done
priority: medium # high | medium | low (default: medium)
created_at: 2026-07-02
tags: []
github_repo: # https://github.com/owner/repo (empty if project has no repo)
github_issues: [] # list of issue numbers, e.g. [1234, 1240]
---
```

Never mutate `status` or `priority` without confirming with the user.

The `## GitHub` section in each project's `index.md` is auto-managed by `log-status` between `<!-- GH-SYNC-START -->` / `<!-- GH-SYNC-END -->` markers. Do not hand-edit content between the markers — it will be overwritten on the next sync.

## What this skill does NOT do (v1)

- Meeting notes (`log-meeting`) — deferred; `Meetings/` folder is scaffolded but no mode fills it yet.
- Promote-scratchpad-to-KB (`promote`) — deferred.
- Contradiction detection (`lint --deep`) — deferred.
- Migration of existing project folders outside `$SZYMON_WIKI` — out of scope.
