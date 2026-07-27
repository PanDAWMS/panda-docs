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
        self.node_of_step = {}  # step name -> node id
        self.subs_of_step = {}  # step name -> [Scope], one per cluster drawn for that step
        self.entries = []  # nodes with no in-scope parent
        self.exits = []  # nodes feeding the level's outputs
        self.deferred_edges = []  # edges from the parent scope, emitted once the cluster closes
        self.output_types = []  # output_types this level declares, shown on the edge leaving it

    def node_id(self, name):
        return f"{self.prefix}__{name}" if self.prefix else str(name)

    @property
    def cluster(self):
        return "cluster_" + self.prefix


def emit_workflow(writer, wfd, base_dir, prefix="", scatter_sources=None, detail=True):
    """
    Emit the nodes and edges of one workflow level and return its Scope.

    scatter_sources maps an input name of this level onto a node id in the parent scope.
    One iteration of a scattered sub-workflow consumes one element of that parent list,
    so the input is still drawn here, with an edge coming in from the parent.

    With detail=False only the shape of the level is drawn: its steps, inputs and edges
    all lose their text. Used for sub-workflows whose steps are already spelled out in
    their own figure.
    """
    scope = Scope(prefix)
    steps = wfd.get("steps") or {}
    declared_inputs = wfd.get("inputs") or {}
    outputs = wfd.get("outputs") or {}
    scatter_sources = scatter_sources or {}
    input_node = {}

    # workflow inputs, as source nodes of this level
    if isinstance(declared_inputs, dict):
        for input_name, value in declared_inputs.items():
            node = scope.node_id(f"in_{input_name}")
            if not detail:
                writer.line(f"{quote(node)} [{COMPACT_NODE}, {STYLE['input']}];")
            else:
                # a scattered input holds one element of the parent list, not the list itself
                if input_name in scatter_sources or isinstance(value, list):
                    label = input_name
                else:
                    label = f"{input_name}\n{shorten(value)}"
                writer.line(f"{quote(node)} [label={quote(label)}, {STYLE['input']}];")
            input_node[input_name] = node
            if input_name in scatter_sources:
                scope.deferred_edges.append(edge_line(scatter_sources[input_name], node, []))

    # one node, or one cluster per iteration, for each step
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
        connected = False

        primary = step_spec.get("inDS")
        primary_type = step_spec.get("inDsType") if detail else None
        if primary and emit_edge(writer, primary, step_name, scope, input_node, primary_type):
            connected = True

        secondaries = step_spec.get("secondaryDSs") or []
        sec_types = step_spec.get("secondaryDsTypes") or [] if detail else []
        for index, source in enumerate(secondaries):
            data_type = sec_types[index] if index < len(sec_types) else None
            if emit_edge(writer, source, step_name, scope, input_node, data_type, EDGE_SECONDARY):
                connected = True

        if not connected:
            scope.entries += [n for n, _ in entry_anchors(scope, step_name)]

    # tail steps, i.e. those the workflow outputs point at
    for output_spec in (outputs or {}).values():
        if not isinstance(output_spec, dict):
            continue
        source_step = (output_spec.get("from") or "").split("/")[0]
        if source_step in scope.node_of_step:
            scope.exits += [n for n, _ in exit_anchors(scope, source_step)]
    if not scope.exits:
        consumed = collect_consumed_steps(steps)
        for name in scope.node_of_step:
            if name not in consumed:
                scope.exits += [n for n, _ in exit_anchors(scope, name)]

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


def entry_anchors(scope, step_name):
    """
    (node, lhead) pairs an edge into this step should point at. A step drawn as one or
    more clusters is entered at each cluster's head node, clipped at its border.
    """
    subs = scope.subs_of_step.get(step_name)
    if not subs:
        return [(scope.node_of_step[step_name], "")]
    return [(sub.entries[0], f"lhead={quote(sub.cluster)}") for sub in subs if sub.entries]


def exit_anchors(scope, step_name):
    """(node, ltail) pairs an edge leaving this step should start from."""
    subs = scope.subs_of_step.get(step_name)
    if not subs:
        return [(scope.node_of_step[step_name], "")]
    return [(sub.exits[0], f"ltail={quote(sub.cluster)}") for sub in subs if sub.exits]


def edge_line(origin, target, attrs):
    """One edge statement, without the bracket list when there is nothing to say."""
    body = ", ".join(a for a in attrs if a)
    return f"{quote(origin)} -> {quote(target)}" + (f" [{body}];" if body else ";")


def write_edge(writer, origin, target, attrs):
    writer.line(edge_line(origin, target, attrs))


def emit_edge(writer, source, target_step, scope, input_node, data_type=None, extra=""):
    """
    Draw the dependency edges for one source of a step, one per (source, target) cluster
    instance. Returns True when the source could be resolved.
    """
    source = str(source)
    attrs = []
    if data_type:
        attrs.append(f"label={quote(data_type)}")
    if extra:
        attrs.append(extra)
    targets = entry_anchors(scope, target_step)

    match = INPUT_REF_RE.match(source)
    if match:
        origin = input_node.get(match.group(1))
        if origin is None:
            return False
        for node, lhead in targets:
            write_edge(writer, origin, node, attrs + [lhead])
        return True

    match = STEP_OUT_RE.match(source)
    if match and match.group(1) in scope.node_of_step:
        parent_name = match.group(1)
        if not data_type:
            # a sub-workflow step has no --outputs of its own; the types it hands on are
            # the ones its own outputs section declares
            subs = scope.subs_of_step.get(parent_name)
            if subs and subs[0].output_types:
                attrs.insert(0, f"label={quote(', '.join(subs[0].output_types))}")
        for origin, ltail in exit_anchors(scope, parent_name):
            for node, lhead in targets:
                write_edge(writer, origin, node, attrs + [ltail, lhead])
        return True

    return False


def scatter_count(scatter_inputs, wfd):
    """Number of iterations a zip-mode scatter expands into."""
    parent_inputs = wfd.get("inputs") or {}
    lengths = [len(parent_inputs[name]) for name in scatter_inputs.values() if isinstance(parent_inputs.get(name), list)]
    return min(lengths) if lengths else 0


def emit_sub_workflow(writer, step_name, step_spec, wfd, base_dir, scope, parent_input_node, detail=True):
    """
    Emit a ``type: workflow`` step, as a cluster when its definition can be resolved.

    A scattered step is drawn as one cluster per iteration, since that is what actually
    runs: the yaml holds a single template, but the parent's lists are consumed
    element-wise and each element gets its own copy of the sub-workflow.
    """
    node = scope.node_of_step[step_name]
    sub_wfd = resolve_sub_workflow(step_spec, wfd, base_dir)

    if sub_wfd is None:
        # referenced file is not available here; keep the step opaque rather than guess
        ref = step_spec.get("workflow_ref", "sub-workflow")
        writer.line(f"{quote(node)} [label={quote(step_name + chr(10) + ref)}, {STYLE['opaque']}];")
        return

    # inputs given on the step override the ones the sub-workflow declares for itself
    inner_wfd = dict(sub_wfd)
    overrides = dict(step_spec.get("inputs") or {})
    if overrides:
        inner_wfd["inputs"] = {**(sub_wfd.get("inputs") or {}), **overrides}

    scatter_inputs = step_spec.get("scatter_inputs") or {}
    if scatter_inputs:
        # the scatter mode is deliberately left out of the label: "zip" reads as a file
        # type next to the output types on the surrounding edges
        count = scatter_count(scatter_inputs, wfd) or 1
        instances = [(f"{node}_s{i + 1}", f"{step_name}  (scatter s{i + 1})") for i in range(count)]
        scatter_sources = {child: parent_input_node[parent] for child, parent in scatter_inputs.items() if parent in parent_input_node}
    else:
        suffix = f"  ({step_spec['workflow_ref']})" if step_spec.get("workflow_ref") and not ABSTRACT_SUBS else ""
        instances = [(node, step_name + suffix)]
        scatter_sources = {}

    declared_types = []
    for output_spec in (inner_wfd.get("outputs") or {}).values():
        if isinstance(output_spec, dict):
            declared_types += output_spec.get("output_types") or []

    sub_scopes = []
    for cluster_prefix, label in instances:
        writer.open(f"subgraph {quote('cluster_' + cluster_prefix)}")
        writer.line(f"label={quote(label)};")
        writer.line(CLUSTER_STYLE)
        sub_scope = emit_workflow(
            writer,
            inner_wfd,
            base_dir,
            prefix=cluster_prefix,
            scatter_sources=scatter_sources,
            detail=detail and not ABSTRACT_SUBS,
        )[0]
        writer.close()
        # edges crossing into the cluster belong to this scope, or Graphviz would pull
        # their source node inside the box
        for line in sub_scope.deferred_edges:
            writer.line(line)
        # Every iteration of a scatter produces the same output name, so putting it on
        # each outgoing edge suggests the iterations differ in what they produce. Only a
        # plain sub-workflow advertises its type here.
        sub_scope.output_types = [] if scatter_inputs else list(declared_types)
        sub_scopes.append(sub_scope)

    scope.subs_of_step[step_name] = sub_scopes


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
        for origin, ltail in exit_anchors(scope, source_step):
            write_edge(writer, origin, node, [ltail])

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
