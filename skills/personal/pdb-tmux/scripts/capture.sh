#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   capture.sh [session] [lines]
# Example:
#   ./capture.sh dbg 400

session="${1:-dbg}"
lines="${2:-200}"
target="${session}:0.0"

tmux capture-pane -p -t "$target" -S "-${lines}"
