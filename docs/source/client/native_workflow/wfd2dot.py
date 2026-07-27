#!/usr/bin/env python3
"""
wfd2dot.py -- draw PanDA native workflow descriptions (WFD) as Graphviz DAGs.

The WFD reference grammar has only two forms, ``{input_name}`` and ``step/outDS``,
so the graph can be recovered from the yaml without involving the server-side parser:

  * every entry of ``steps`` becomes a node,
  * ``inDS`` gives the solid edge into a step, ``secondaryDSs`` the dashed ones,
  * a ``type: workflow`` step becomes a cluster holding the steps of the sub-workflow,
    whether those are written inline, pulled in via ``workflow_ref``, or scattered.

Usage:

    wfd2dot.py <wfd.yaml> [<wfd.yaml> ...] [-o OUTDIR] [-T FORMAT]

Writes ``<OUTDIR>/<stem>.dot`` for each input file. With ``-T`` it also renders to
that format, which requires the Graphviz ``dot`` executable on PATH. To regenerate
everything this page uses, from this directory:

    ./regen_dags.sh

which runs this script over every example with the per-figure options it needs, then
renders. That overwrites the DOT sources from the yaml. To re-render after editing a
.dot file by hand, run ./render_dags.sh instead.

Sub-workflows pulled in with ``workflow_ref`` are looked up next to the referring
file, matching how the sandbox is laid out at submission time.
"""

import argparse
import os
import re
import subprocess
import sys

import yaml

# the two reference forms of the description language
INPUT_REF_RE = re.compile(r"^\{([^{}]+)\}$")
STEP_OUT_RE = re.compile(r"^([^/]+)/outDS$")

# node styling per role
STYLE = {
    "input": 'shape=folder, style=filled, fillcolor="#e8eef7", color="#5a7fb0", fontcolor="#1f3552"',
    "output": 'shape=folder, style=filled, fillcolor="#e6f2e6", color="#5a9a5a", fontcolor="#1f4d1f"',
    "prun": 'shape=box, style="rounded,filled", fillcolor="#fdf3e0", color="#c08b3e", fontcolor="#4d3410"',
    "other": 'shape=box, style="rounded,filled", fillcolor="#f2eaf7", color="#8b5aa8", fontcolor="#3d1f4d"',
    "opaque": 'shape=box3d, style=filled, fillcolor="#f0f0f0", color="#888888", fontcolor="#333333"',
}
CLUSTER_STYLE = 'graph [style="rounded,filled", fillcolor="#fafafa", color="#9aa5b1", fontcolor="#48525c", fontsize=11];'
# a step drawn without its text, used when only the shape of a sub-workflow matters
COMPACT_NODE = 'label="", fixedsize=true, width=0.42, height=0.28'
EDGE_SECONDARY = 'style=dashed, color="#7a7a7a"'

# set from --abstract-subworkflows: draw sub-workflow internals as shape only
ABSTRACT_SUBS = False


class DotWriter:
    """Accumulates DOT source with block indentation."""

    def __init__(self):
        self.lines = []
        self.depth = 0

    def line(self, text=""):
        self.lines.append(("  " * self.depth + text).rstrip())

    def open(self, header):
        self.line(header + " {")
        self.depth += 1

    def close(self):
        self.depth -= 1
        self.line("}")

    def text(self):
        return "\n".join(self.lines) + "\n"


def quote(text):
    """Quote a DOT string, turning real newlines into the escape Graphviz expects."""
    escaped = str(text).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return '"' + escaped + '"'


def load_yaml(path):
    with open(path) as stream:
        return yaml.safe_load(stream) or {}


def step_type(step_spec):
    return (step_spec or {}).get("type", "prun")


def output_types_of(step_spec):
    """The --outputs list of a prun step, used to label what a step produces."""
    args = (step_spec or {}).get("args") or ""
    match = re.search(r"--outputs[= ]+(\S+)", args)
    return match.group(1).split(",") if match else []


def resolve_sub_workflow(step_spec, wfd, base_dir):
    """
    Return the sub-workflow definition of a ``type: workflow`` step, or None when it
    cannot be resolved locally. Inline steps win over workflow_ref, a ref is first
    looked up in workflow_blocks and then as a file next to the referring description.
    """
    if "steps" in step_spec:
        return step_spec
    ref = step_spec.get("workflow_ref")
    if not ref:
        return None
    blocks = wfd.get("workflow_blocks") or {}
    if ref in blocks:
        return blocks[ref]
    ref_path = os.path.join(base_dir, ref)
    if os.path.isfile(ref_path):
        return load_yaml(ref_path)
    return None


class Scope:
    """
    One workflow level: its steps, the node ids they were emitted under, and the
    entry/exit nodes used to attach edges when the level is drawn as a cluster.
    """

    def __init__(self, prefix):
        self.prefix = prefix
        self.node_of_step = {}  # step name -> node id an edge should point at
        self.sub_of_step = {}  # step name -> Scope, for steps drawn as a cluster
        self.entries = []  # nodes with no in-scope parent
        self.exits = []  # nodes feeding the level's outputs
        self.external_names = set()  # input names supplied by the parent scope
        self.deferred_edges = []  # edges from the parent scope, emitted once the cluster closes
        self.output_types = []  # output_types this level declares, shown on the edge leaving it

    def node_id(self, name):
        return f"{self.prefix}__{name}" if self.prefix else str(name)


def emit_workflow(writer, wfd, base_dir, prefix="", external_inputs=None, detail=True):
    """
    Emit the nodes and edges of one workflow level and return its Scope.

    external_inputs maps an input name of this level onto an (node id, edge label)
    pair in the parent scope. A scattered sub-workflow uses it to bind its own inputs
    to the parent lists it is scattered over, so no node is drawn for them here.

    With detail=False only the shape of the level is drawn: its steps, inputs and edges
    all lose their text. Used for sub-workflows whose steps are already spelled out in
    their own figure.
    """
    scope = Scope(prefix)
    steps = wfd.get("steps") or {}
    declared_inputs = wfd.get("inputs") or {}
    outputs = wfd.get("outputs") or {}
    input_node = dict(external_inputs or {})
    scope.external_names = set(input_node)

    # workflow inputs, as source nodes of this level
    if isinstance(declared_inputs, dict):
        for input_name, value in declared_inputs.items():
            if input_name in input_node:
                continue  # supplied by the parent, drawn there
            node = scope.node_id(f"in_{input_name}")
            if not detail:
                writer.line(f"{quote(node)} [{COMPACT_NODE}, {STYLE['input']}];")
            else:
                label = input_name if isinstance(value, list) else f"{input_name}\n{shorten(value)}"
                writer.line(f"{quote(node)} [label={quote(label)}, {STYLE['input']}];")
            input_node[input_name] = (node, None)

    # one node, or one cluster, per step
    for step_name, step_spec in steps.items():
        step_spec = step_spec or {}
        node = scope.node_id(step_name)
        scope.node_of_step[step_name] = node
        if step_type(step_spec) == "workflow":
            emit_sub_workflow(writer, step_name, step_spec, wfd, base_dir, scope, input_node, detail)
        else:
            style = STYLE["prun"] if step_type(step_spec) == "prun" else STYLE["other"]
            if detail:
                label = step_name
                produced = output_types_of(step_spec)
                if produced:
                    label += "\n" + ", ".join(produced)
                writer.line(f"{quote(node)} [label={quote(label)}, {style}];")
            else:
                writer.line(f"{quote(node)} [{COMPACT_NODE}, {style}];")

    # edges, from the inDS and secondaryDSs of every step
    for step_name, step_spec in steps.items():
        step_spec = step_spec or {}
        target = scope.node_of_step[step_name]
        head = cluster_attr("lhead", scope, step_name, steps, wfd, base_dir)
        connected = False

        primary = step_spec.get("inDS")
        primary_type = step_spec.get("inDsType") if detail else None
        if primary and emit_edge(writer, primary, target, scope, input_node, steps, wfd, base_dir, head, primary_type):
            connected = True

        secondaries = step_spec.get("secondaryDSs") or []
        sec_types = step_spec.get("secondaryDsTypes") or [] if detail else []
        for index, source in enumerate(secondaries):
            data_type = sec_types[index] if index < len(sec_types) else None
            if emit_edge(writer, source, target, scope, input_node, steps, wfd, base_dir, head, data_type, EDGE_SECONDARY):
                connected = True

        if not connected:
            scope.entries.append(target)

    # tail steps, i.e. those the workflow outputs point at
    for output_name, output_spec in (outputs or {}).items():
        if not isinstance(output_spec, dict):
            continue
        source_step = (output_spec.get("from") or "").split("/")[0]
        if source_step in scope.node_of_step:
            scope.exits.append(exit_node_of(scope, source_step))
    if not scope.exits:
        consumed = collect_consumed_steps(steps)
        scope.exits = [exit_node_of(scope, name) for name in scope.node_of_step if name not in consumed]

    return scope, outputs


def shorten(dataset, width=34):
    """Datasets are far too long to draw; keep the tail, which is the telling part."""
    text = str(dataset)
    return text if len(text) <= width else "..." + text[-(width - 3):]


def collect_consumed_steps(steps):
    """Names of steps whose output is consumed by another step of the same level."""
    consumed = set()
    for step_spec in steps.values():
        step_spec = step_spec or {}
        sources = [step_spec.get("inDS")] + list(step_spec.get("secondaryDSs") or [])
        for source in sources:
            match = STEP_OUT_RE.match(str(source)) if source else None
            if match:
                consumed.add(match.group(1))
    return consumed


def cluster_attr(which, scope, step_name, steps, wfd, base_dir):
    """lhead/ltail attribute so an edge clips at the border of a sub-workflow cluster."""
    step_spec = steps.get(step_name) or {}
    if step_type(step_spec) != "workflow":
        return ""
    if resolve_sub_workflow(step_spec, wfd, base_dir) is None:
        return ""
    return f", {which}={quote('cluster_' + scope.node_id(step_name))}"


def edge_line(origin, target, attrs):
    """One edge statement, without the bracket list when there is nothing to say."""
    body = ", ".join(a for a in attrs if a)
    return f"{quote(origin)} -> {quote(target)}" + (f" [{body}];" if body else ";")


def write_edge(writer, origin, target, attrs):
    writer.line(edge_line(origin, target, attrs))


def emit_edge(writer, source, target, scope, input_node, steps, wfd, base_dir, head_attr, data_type=None, extra=""):
    """Draw one dependency edge. Returns True when the source could be resolved."""
    source = str(source)
    attrs = []
    if data_type:
        attrs.append(f"label={quote(data_type)}")
    if extra:
        attrs.append(extra)

    match = INPUT_REF_RE.match(source)
    if match:
        bound = input_node.get(match.group(1))
        if bound is None:
            return False
        origin, origin_label = bound
        if origin_label and not data_type:
            attrs.insert(0, f"label={quote(origin_label)}")
        line = edge_line(origin, target, attrs + [head_attr.lstrip(", ")])
        if match.group(1) in scope.external_names:
            scope.deferred_edges.append(line)
        else:
            writer.line(line)
        return True

    match = STEP_OUT_RE.match(source)
    if match and match.group(1) in scope.node_of_step:
        parent_name = match.group(1)
        if not data_type:
            sub_scope = scope.sub_of_step.get(parent_name)
            if sub_scope and sub_scope.output_types:
                attrs.insert(0, f"label={quote(', '.join(sub_scope.output_types))}")
        # leave the parent cluster at its border when the parent is a sub-workflow
        tail_attr = cluster_attr("ltail", scope, parent_name, steps, wfd, base_dir)
        origin = exit_node_of(scope, parent_name)
        write_edge(writer, origin, target, attrs + [tail_attr.lstrip(", "), head_attr.lstrip(", ")])
        return True

    return False


def exit_node_of(scope, step_name):
    """The node an edge starts from when it leaves the given step of this scope."""
    sub_scope = scope.sub_of_step.get(step_name)
    if sub_scope and sub_scope.exits:
        return sub_scope.exits[0]
    return scope.node_of_step[step_name]


def emit_sub_workflow(writer, step_name, step_spec, wfd, base_dir, scope, parent_input_node, detail=True):
    """Emit a ``type: workflow`` step, as a cluster when its definition can be resolved."""
    node = scope.node_of_step[step_name]
    sub_wfd = resolve_sub_workflow(step_spec, wfd, base_dir)

    if sub_wfd is None:
        # referenced file is not available here; keep the step opaque rather than guess
        ref = step_spec.get("workflow_ref", "sub-workflow")
        writer.line(f"{quote(node)} [label={quote(step_name + chr(10) + ref)}, {STYLE['opaque']}];")
        return

    scatter_inputs = step_spec.get("scatter_inputs") or {}
    label = step_name
    if scatter_inputs:
        # the scatter mode is deliberately left out: "zip" reads as a file type next to
        # the output types on the surrounding edges
        label += "  (scatter)"
    elif step_spec.get("workflow_ref") and not ABSTRACT_SUBS:
        label += f"  ({step_spec['workflow_ref']})"

    # a scattered sub-workflow reads the parent lists rather than its own declared inputs
    external = {}
    for child_input, parent_input in scatter_inputs.items():
        if parent_input in parent_input_node:
            external[child_input] = (parent_input_node[parent_input][0], None)

    # inputs given on the step override the ones the sub-workflow declares for itself
    inner_wfd = dict(sub_wfd)
    overrides = dict(step_spec.get("inputs") or {})
    if overrides:
        inner_wfd["inputs"] = {**(sub_wfd.get("inputs") or {}), **overrides}

    writer.open(f"subgraph {quote('cluster_' + node)}")
    writer.line(f"label={quote(label)};")
    writer.line(CLUSTER_STYLE)
    sub_scope = emit_workflow(writer, inner_wfd, base_dir, prefix=node, external_inputs=external, detail=detail and not ABSTRACT_SUBS)[0]
    writer.close()
    for line in sub_scope.deferred_edges:
        writer.line(line)

    for output_spec in (inner_wfd.get("outputs") or {}).values():
        if isinstance(output_spec, dict):
            sub_scope.output_types += output_spec.get("output_types") or []
    scope.sub_of_step[step_name] = sub_scope
    # edges into the cluster land on one of its entry nodes
    if sub_scope.entries:
        scope.node_of_step[step_name] = sub_scope.entries[0]


def build_dot(path):
    """Turn one workflow description into DOT source."""
    wfd = load_yaml(path)
    base_dir = os.path.dirname(os.path.abspath(path))
    name = wfd.get("name") or os.path.splitext(os.path.basename(path))[0]

    writer = DotWriter()
    writer.open(f"digraph {quote(name)}")
    writer.line("compound=true;")
    writer.line("rankdir=TB;")
    writer.line('graph [fontname="Helvetica", bgcolor="transparent", nodesep=0.35, ranksep=0.55];')
    writer.line('node [fontname="Helvetica", fontsize=11, margin="0.16,0.09"];')
    writer.line('edge [fontname="Helvetica", fontsize=9, color="#555555", arrowsize=0.8];')
    writer.line()

    scope, outputs = emit_workflow(writer, wfd, base_dir)

    # final outputs of the workflow
    for output_name, output_spec in (outputs or {}).items():
        if not isinstance(output_spec, dict):
            continue
        source_step = (output_spec.get("from") or "").split("/")[0]
        if source_step not in scope.node_of_step:
            continue
        node = f"out_{output_name}"
        types = output_spec.get("output_types") or []
        label = output_name + ("\n" + ", ".join(types) if types else "")
        writer.line(f"{quote(node)} [label={quote(label)}, {STYLE['output']}];")
        steps = wfd.get("steps") or {}
        tail = cluster_attr("ltail", scope, source_step, steps, wfd, base_dir)
        origin = exit_node_of(scope, source_step)
        write_edge(writer, origin, node, [tail.lstrip(", ")])

    writer.close()
    return writer.text()


def main():
    parser = argparse.ArgumentParser(description="Draw PanDA native workflow descriptions as Graphviz DAGs.")
    parser.add_argument("wfd", nargs="+", help="workflow description yaml file(s)")
    parser.add_argument("-o", "--outdir", default=".", help="where rendered images go (default: current directory)")
    parser.add_argument("--dotdir", default=None, help="where the DOT sources go (default: the output directory)")
    parser.add_argument("-T", "--format", default=None, help="also render with dot to this format, e.g. png or svg")
    parser.add_argument(
        "--abstract-subworkflows",
        action="store_true",
        help="draw sub-workflow internals as shape only, dropping the text of their steps, "
        "inputs and edges. Use when the sub-workflow has its own figure",
    )
    parser.add_argument("--prefix", default="", help="prepended to the output file names")
    args = parser.parse_args()

    global ABSTRACT_SUBS
    ABSTRACT_SUBS = args.abstract_subworkflows

    dotdir = args.dotdir or args.outdir
    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(dotdir, exist_ok=True)
    exit_code = 0

    for path in args.wfd:
        stem = args.prefix + os.path.splitext(os.path.basename(path))[0]
        dot_path = os.path.join(dotdir, stem + ".dot")
        with open(dot_path, "w") as stream:
            stream.write(build_dot(path))
        print(f"wrote {dot_path}")

        if args.format:
            out_path = os.path.join(args.outdir, f"{stem}.{args.format}")
            try:
                subprocess.run(["dot", f"-T{args.format}", dot_path, "-o", out_path], check=True)
                print(f"wrote {out_path}")
            except FileNotFoundError:
                print("the dot executable was not found; install Graphviz to render", file=sys.stderr)
                exit_code = 1
                break
            except subprocess.CalledProcessError as exc:
                print(f"dot failed on {dot_path}: {exc}", file=sys.stderr)
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
