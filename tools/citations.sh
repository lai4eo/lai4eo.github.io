#!/usr/bin/env bash
#
# Regenerate _data/citations.yaml from _data/sources.yaml.
#
# _data/sources.yaml is the hand-maintained list of DOIs shown on the Research
# page. This script resolves each one with Manubot and rewrites
# _data/citations.yaml, which is what the page actually renders. Run it after
# every edit to sources.yaml, and commit BOTH files.
#
# CI checks the two agree and fails the build if they do not, so a forgotten
# run is loud rather than silent.
#
#   ./tools/citations.sh
#
# The first run builds a venv in _cite/.venv (gitignored) and takes a couple of
# minutes. Later runs are seconds.

set -euo pipefail
cd "$(dirname "$0")/.."

VENV="_cite/.venv"

# cite.py shells out to the `manubot` CLI, so the venv's bin/ has to be on PATH
# — running _cite/.venv/bin/python is not enough. That failure is silent: every
# source "errors", cite.py still writes a citations.yaml, and every title and
# author is quietly dropped. Do not "simplify" this by calling python directly.

if [ ! -x "$VENV/bin/manubot" ]; then
  # manubot needs Python >= 3.8. `python3` on Nikhil's Mac is 3.7.9, so probe.
  PY=""
  for c in python3.13 python3.12 python3.11 python3.10 python3.9 python3.8 python3; do
    if command -v "$c" >/dev/null 2>&1; then
      v=$("$c" -c 'import sys; print(sys.version_info >= (3,8))' 2>/dev/null || echo False)
      if [ "$v" = "True" ]; then PY="$c"; break; fi
    fi
  done
  if [ -z "$PY" ]; then
    echo "error: no Python >= 3.8 found. Manubot needs one." >&2
    exit 1
  fi
  echo "Creating $VENV with $PY (first run only)…"
  rm -rf "$VENV"
  "$PY" -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade pip
  "$VENV/bin/pip" install --quiet -r _cite/requirements.txt
fi

before=$(cat _data/citations.yaml 2>/dev/null || true)
PATH="$PWD/$VENV/bin:$PATH" "$VENV/bin/python" _cite/cite.py
after=$(cat _data/citations.yaml)

# Run the same check CI runs, so a problem surfaces here rather than on push.
# Use the venv's python: `python3` on this Mac is 3.7.9 with no PyYAML.
echo
"$VENV/bin/python" tools/check_citations.py

echo
if [ "$before" = "$after" ]; then
  echo "citations.yaml unchanged."
else
  echo "citations.yaml updated. Review it, then commit it with sources.yaml:"
  echo "    git diff _data/sources.yaml _data/citations.yaml"
fi
