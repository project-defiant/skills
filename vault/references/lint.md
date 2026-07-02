# Mode: lint

Cheap health check over `$SZYMON_WIKI/`. Reports findings; does NOT auto-fix.

## Inputs

- **check** (optional): one of `broken | orphans | spine | sources`. If missing, run all four.

## Checks

### 1. Broken wikilinks

- Extract every `[[X]]` and `[[X|display]]` from every `*.md` under `$SZYMON_WIKI/`:
  `rg -o -n "\[\[([^\]|]+)(\|[^\]]+)?\]\]" -r '$1' "$SZYMON_WIKI" --glob '*.md'`
- For each target `X`:
  - Consider it resolved if a file named `X.md` exists ANYWHERE under `$SZYMON_WIKI/` (Obsidian resolves globally by filename).
  - Also consider it resolved if some `.md` file contains a heading `# X`.
- Report unresolved as:
  `- {source-path}:{line} → [[X]] (no target)`

### 2. Orphan pages

- List every `.md` file under `$SZYMON_WIKI/Projects/**` and `$SZYMON_WIKI/KnowledgeBase/**`.
- Exclude the natural entry points: `index.md`, `log.md`, `CHANGELOG.md` at any depth.
- For each file `F`, count incoming wikilinks:
  `rg -c "\[\[{basename(F, .md)}(\|[^\]]+)?\]\]" "$SZYMON_WIKI" --glob '*.md'`
  Sum across all matching files, EXCLUDING self-references.
- Report files with zero incoming links:
  `- {path} (no incoming wikilinks)`

### 3. Missing spine files

- Top-level:
  - `$SZYMON_WIKI/index.md`
  - `$SZYMON_WIKI/log.md`
- For each `$SZYMON_WIKI/Projects/{X}/`:
  - `index.md`
  - `log.md`
  - `ImplementationStatus/CHANGELOG.md`
- Report each missing file:
  `- {path} (missing)`

### 4. Sources without summaries

- For each file `S` under any `$SZYMON_WIKI/Projects/**/Research/sources/`:
  - Extract `basename(S, .md)` (strip the leading date if desired, but the slug is enough).
  - Look for a file `<slug>-summary.md` in the sibling `Research/` folder.
  - If not found, ripgrep the sibling `Research/` for a file whose frontmatter contains `source_file: [[{basename(S)}]]`.
  - If still no match, flag it.
- Report as:
  `- {source-path} (no summary in sibling Research/)`

## Output

Print a report grouped by check with a header count per section, e.g.:

~~~
Wiki lint — {YYYY-MM-DD HH:MM}

Broken wikilinks (3)
  - Projects/decode-pqtl/index.md:42 → [[gentropy-input-transfer]] (no target)
  - ...

Orphan pages (2)
  - Projects/decode-pqtl/Research/random-note.md (no incoming wikilinks)
  - ...

Missing spine files (1)
  - Projects/pineco-zgred/log.md (missing)

Sources without summaries (0)
  (none)
~~~

## Notes

- Lint never modifies files. If the user asks to fix something specific, exit lint and invoke the appropriate mode (`project-init` to create a missing spine, edit calls for others).
- Cost: even on vaults of thousands of files, all four checks are ripgrep-bound; sub-second on this hardware.
- Deep checks (stale status, duplicates, contradictions) are deferred; see `SKILL.md` "what this skill does NOT do".
