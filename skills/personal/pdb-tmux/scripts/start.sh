#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   start.sh [session] -- <command...>
#
# Example:
#   ./start.sh dbg -- python -m pdb your_script.py
#   ./start.sh dbg -- uv run python -m pdb your_script.py

session="${1:-dbg}"

if [[ "${session}" == "--" ]]; then
  session="dbg"
fi

# Find the '--' separator
sep_idx=-1
i=0
for arg in "$@"; do
  if [[ "$arg" == "--" ]]; then
    sep_idx=$i
    break
  fi
  i=$((i+1))
done

if [[ $sep_idx -lt 0 ]]; then
  echo "ERROR: Missing '--' separator. Example: start.sh dbg -- python -m pdb script.py" >&2
  exit 2
fi

# Build command array after '--'
cmd=()
j=0
for arg in "$@"; do
  if [[ $j -gt $sep_idx ]]; then
    cmd+=("$arg")
  fi
  j=$((j+1))
done

if [[ ${#cmd[@]} -eq 0 ]]; then
  echo "ERROR: No command after '--'." >&2
  exit 2
fi

target="${session}:0.0"

tmux has-session -t "$session" 2>/dev/null || tmux new-session -d -s "$session"
tmux rename-window -t "${session}:0" "pdb" 2>/dev/null || true

# Send command robustly: join with proper escaping for tmux send-keys (we send as one string)
# Use printf %q to get a shell-escaped string, then send literally.
joined=""
for a in "${cmd[@]}"; do
  # shellcheck disable=SC2059
  joined+=$(printf "%q " "$a")
done
joined="${joined% }"

tmux send-keys -t "$target" "$joined" Enter
tmux capture-pane -p -t "$target" -S -200
