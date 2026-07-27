#!/usr/bin/env bash
#
# render_dags.sh -- render the workflow DAGs from their DOT sources.
#
# Use this after editing the .dot files by hand. It only runs Graphviz, so the
# edits survive; wfd2dot.py would regenerate the DOT from the yaml and overwrite
# them.
#
# Usage:
#   ./render_dags.sh                  # render every DOT source
#   ./render_dags.sh dag/foo.dot ...  # render only the given ones
#   FORMAT=svg ./render_dags.sh       # render to something other than png
#
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dot_dir="${here}/dag"
image_dir="${here}/images"
format="${FORMAT:-png}"

# Homebrew is not always on PATH in non-login shells
if ! command -v dot >/dev/null 2>&1; then
    for candidate in /opt/homebrew/bin /usr/local/bin; do
        if [ -x "${candidate}/dot" ]; then
            PATH="${candidate}:${PATH}"
            break
        fi
    done
fi
if ! command -v dot >/dev/null 2>&1; then
    echo "the dot executable was not found; install Graphviz to render" >&2
    exit 1
fi

if [ "$#" -gt 0 ]; then
    sources=("$@")
else
    sources=("${dot_dir}"/*.dot)
fi

mkdir -p "${image_dir}"
for source in "${sources[@]}"; do
    target="${image_dir}/$(basename "${source%.dot}").${format}"
    dot "-T${format}" "${source}" -o "${target}"
    echo "wrote ${target}"
done
