#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   send.sh [session] <pdb command...>
# Example:
#   ./send.sh dbg p x
#   ./send.sh dbg "b file.py:123, x>0"

session="${1:-dbg}"
shift || true

if [[ $# -eq 0 ]]; then
  echo "ERROR: Missing pdb command" >&2
  exit 2
fi

target="${session}:0.0"

# Send as a single line (preserve spaces)
cmd="$*"
tmux send-keys -t "$target" "$cmd" Enter
tmux capture-pane -p -t "$target" -S -200
