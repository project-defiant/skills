#!/usr/bin/env bash
# Bare-repo worktree hub (https://dev.to/metal3d/git-worktree-like-a-boss-2j1b)
# with frozen branch prefixes.
#
#   wt.sh init <repo-url> [dir]        clone into a new hub, add default-branch worktree
#   wt.sh add <prefix> <slug> [base]   branch and dir <prefix>/<slug>
#   wt.sh rm <prefix>/<slug> [--force] remove a worktree (branch is kept)
#   wt.sh ls                           list worktrees
#
# Prefixes are frozen: feat fix chore perf run. Slugs are kebab-case.
set -euo pipefail

PREFIXES="feat fix chore perf run"

die() { echo "wt: $*" >&2; exit 1; }

check_prefix() {
  case "$1" in
    feat|fix|chore|perf|run) ;;
    *) die "prefix '$1' not allowed; use one of: $PREFIXES" ;;
  esac
}

check_slug() {
  [[ "$1" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] \
    || die "slug '$1' must be kebab-case: lowercase letters, digits, single hyphens"
}

# Resolve the hub root (the directory holding .bare) from anywhere inside it.
hub_root() {
  local common
  common=$(git rev-parse --git-common-dir 2>/dev/null) || die "not inside a git repository"
  common=$(cd "$common" && pwd)
  [[ "$(basename "$common")" == ".bare" ]] \
    || die "not a bare-repo hub (git dir is $common, expected <hub>/.bare); run 'wt.sh init' first"
  dirname "$common"
}

default_branch() {
  git -C "$1" symbolic-ref --short HEAD
}

cmd_init() {
  local url="${1:-}" dir="${2:-}"
  [[ -n "$url" ]] || die "usage: wt.sh init <repo-url> [dir]"
  [[ -n "$dir" ]] || dir=$(basename "$url" .git)
  if [[ -e "$dir" ]] && [[ -n "$(ls -A "$dir")" ]]; then
    die "'$dir' exists and is not empty"
  fi
  mkdir -p "$dir"
  cd "$dir"

  git clone --bare "$url" .bare
  # printf, not echo: avoids a stray CR on Windows shells corrupting the pointer.
  printf 'gitdir: ./.bare\n' > .git
  # A bare clone has no fetch refspec, so 'git fetch' would never create origin/* refs.
  git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
  git fetch --all --prune

  local main
  main=$(default_branch .)
  git worktree add "$main" "$main"
  git -C "$main" branch --set-upstream-to="origin/$main" "$main" >/dev/null
  echo "wt: hub ready at $(pwd); default worktree: $main/"
}

cmd_add() {
  local prefix="${1:-}" slug="${2:-}" base="${3:-}"
  [[ -n "$prefix" && -n "$slug" ]] || die "usage: wt.sh add <prefix> <slug> [base]"
  check_prefix "$prefix"
  check_slug "$slug"

  local root branch dir
  root=$(hub_root)
  branch="$prefix/$slug"
  dir="$root/$prefix/$slug"
  [[ ! -e "$dir" ]] || die "'$dir' already exists"

  git -C "$root" fetch origin --prune

  if git -C "$root" show-ref --verify --quiet "refs/heads/$branch"; then
    git -C "$root" worktree add "$dir" "$branch"
  elif git -C "$root" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
    git -C "$root" worktree add -b "$branch" "$dir" "origin/$branch"
  else
    [[ -n "$base" ]] || base="origin/$(default_branch "$root")"
    git -C "$root" worktree add --no-track -b "$branch" "$dir" "$base"
  fi
  # A bare clone copies remote branches as local heads with no upstream; track origin when it exists.
  if git -C "$root" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
    git -C "$dir" branch --set-upstream-to="origin/$branch" "$branch" >/dev/null
  fi
  echo "wt: $branch -> $dir"
}

cmd_rm() {
  local name="${1:-}" force="${2:-}"
  name="${name%/}"
  [[ "$name" == */* ]] || die "usage: wt.sh rm <prefix>/<slug> [--force]"
  check_prefix "${name%%/*}"
  local root
  root=$(hub_root)
  if [[ "$force" == "--force" ]]; then
    git -C "$root" worktree remove --force "$root/$name"
  else
    git -C "$root" worktree remove "$root/$name"
  fi
  git -C "$root" worktree prune
  rmdir "$root/${name%%/*}" 2>/dev/null || true  # drop the prefix dir once empty
  echo "wt: removed $name (branch kept)"
}

cmd_ls() {
  git -C "$(hub_root)" worktree list
}

sub="${1:-}"; shift || true
case "$sub" in
  init) cmd_init "$@" ;;
  add)  cmd_add "$@" ;;
  rm)   cmd_rm "$@" ;;
  ls)   cmd_ls ;;
  *)    sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
