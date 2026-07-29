#!/usr/bin/env bash
#
# regen_dags.sh -- rebuild every workflow DAG from its yaml description.
#
# Runs wfd2dot.py over the examples with the options each figure needs, then
# renders. Use this after editing a .yaml; it overwrites the DOT sources, so any
# hand edits to dag/*.dot are lost. To re-render those, run ./render_dags.sh.
#
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${here}"

python="${PYTHON:-python3}"
common=(-o images --dotdir dag -T png --prefix pchain_native_dag_)

# Homebrew is not always on PATH in non-login shells
if ! command -v dot >/dev/null 2>&1; then
    for candidate in /opt/homebrew/bin /usr/local/bin; do
        if [ -x "${candidate}/dot" ]; then
            PATH="${candidate}:${PATH}"
            export PATH
            break
        fi
    done
fi

# Only the yaml examples the page shows a DAG for are listed. multistep_merge_wfd.yaml
# is deliberately absent: its section illustrates the template with a hand-drawn
# schematic instead, and images/multistep_merge_template.png is not generated here.

# figures that show every step in full
"${python}" wfd2dot.py \
    wfd/simple_chain.yaml \
    wfd/signal_background_combine_wfd.yaml \
    "${common[@]}"

# These two are about nesting and scatter, not about what the sub-workflow does: its
# steps are already spelled out under "More complicated chain", so the boxes show only
# structure. Of the two nested variants only the reference-based one gets a figure, the
# inline one has the same DAG.
"${python}" wfd2dot.py \
    wfd/nested_workflow_sig_bg_comb_wfd.yaml \
    wfd/scatter_sig_bg_comb_wfd.yaml \
    --abstract-subworkflows \
    "${common[@]}"
