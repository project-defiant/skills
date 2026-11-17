---
name: pdb-tmux
description: Drive an interactive Python pdb session inside tmux by capturing pane output and sending keys. Use when debugging Python interactively: stepping through code, setting breakpoints, or inspecting variables and stack frames at runtime, especially when the environment cannot attach to an interactive TTY directly. Supports start/capture/send and common pdb shortcuts (n/s/c/r/w/l/b/p/pp).
argument-hint: "start -- <[uv run] python -m pdb ...> | capture [lines] | send <pdb-cmd> | n|s|c|r|w|l|b ... | p <expr> | pp <expr>"
allowed-tools: Bash
---

# pdb-tmux (tmux-driven pdb REPL)

## Goal
Provide a reliable “pseudo-interactive” pdb workflow:
- Run pdb in a tmux pane (the real interactive TTY lives in tmux)
- Read output via `tmux capture-pane`
- Send pdb commands via `tmux send-keys`

This is ideal when the agent/tooling cannot attach to interactive stdin, but can run shell commands.

## Safety & constraints
- Default target is `SESSION=dbg`, `WINDOW=0`, `PANE=0`. Do not touch other tmux sessions unless the user explicitly requests.
- Never run destructive tmux commands (`kill-server`, killing unrelated sessions, etc.) unless explicitly asked.
- Assume commands may contain quotes/spaces; prefer the provided scripts in `scripts/` for robust quoting.
- Always follow this loop for “interactive steps”:
  1) capture (pre-state if needed)
  2) send one pdb command
  3) capture and show the new output (post-state)
- If the pane output does NOT include a pdb prompt like `(Pdb)` or `ipdb>`, capture more context and diagnose (program exited? waiting for input? crashed?).

## Quick start (what you should do)
### A. Start a pdb session in tmux
User invokes:
- `/pdb-tmux start -- python -m pdb path/to/script.py`
- `/pdb-tmux start -- python -m pdb -c continue path/to/script.py` (if they want auto-continue until breakpoint)

**With uv (recommended when project has pyproject.toml):**
- `/pdb-tmux start -- uv run python -m pdb path/to/script.py`
- `/pdb-tmux start -- uv run python -m pdb -c continue path/to/script.py`

Implementation:
- Use `scripts/start.sh` if present.
- Otherwise:
  - `tmux has-session -t dbg || tmux new-session -d -s dbg`
  - `tmux rename-window -t dbg:0 pdb || true`
  - `tmux send-keys -t dbg:0.0 "<COMMAND>" Enter`
  - `tmux capture-pane -p -t dbg:0.0 -S -200`

### B. Capture screen (read current output)
User invokes:
- `/pdb-tmux capture`
- `/pdb-tmux capture 400`

Implementation:
- Use `scripts/capture.sh` if present.
- Default lines=200.
- Command: `tmux capture-pane -p -t dbg:0.0 -S -<lines>`

### C. Send a pdb command
User invokes:
- `/pdb-tmux send n`
- `/pdb-tmux send "p x"`
- `/pdb-tmux send "b my_func"`
- `/pdb-tmux send "b file.py:123, x>0"`

Implementation:
- Use `scripts/send.sh` if present.
- Command: `tmux send-keys -t dbg:0.0 "<PDB_CMD>" Enter`
- Immediately follow with capture to show results.

## Shorthand commands (map to `send ...`)
If the user runs:
- `/pdb-tmux n` → send `n`
- `/pdb-tmux s` → send `s`
- `/pdb-tmux c` → send `c`
- `/pdb-tmux r` → send `r`
- `/pdb-tmux w` → send `w`
- `/pdb-tmux l` → send `l`
- `/pdb-tmux b` → send `b`
- `/pdb-tmux p <expr>` → send `p <expr>`
- `/pdb-tmux pp <expr>` → send `pp <expr>`

Always capture after sending.

## Output formatting
When responding to the user:
- Show the captured pane output in a fenced block.
- If output is long, show the last ~80-120 lines and mention it’s truncated.
- If pdb prompt is missing, explain likely causes and suggest next step (e.g., capture more lines; check exit; restart).

## Advanced: allow specifying session target
If user passes `SESSION=<name>` in arguments, honor it. Otherwise use `dbg`.
Do NOT auto-discover sessions; keep behavior predictable.