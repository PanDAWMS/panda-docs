====================================================
Production Workflows and the Native Workflow API
====================================================

How a production chain is expressed as a PanDA native workflow, submitted to the server, and queried afterwards for how its steps and tasks relate.

The engine is data-driven: a step runs when the data it consumes is ready, not when a parent step finishes. :doc:`/client/pchain_native` covers the description language itself; this page covers the parts specific to production, namely steps that carry a task parameter map, the reference and placeholder forms that let dataset names be written before the IDs in them exist, and the server endpoints.

.. contents:: Table of Contents
    :local:

-----------

|br|

A complete description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A description is one JSON object with :hblue:`name`, :hblue:`inputs`, :hblue:`outputs`, :hblue:`steps` and :hblue:`options`. This one reconstructs and then merges, which is enough to show every part fitting together.

.. literalinclude:: native_workflow/wfd/production_two_step.json
    :language: json
    :caption: production_two_step.json

Reading it as the engine does:

* ``inputs`` names the datasets the workflow does not produce. ``reco`` consumes one as :hblue:`{raw}`.
* ``merge`` consumes :hblue:`{reco/AOD}`, and that reference is the whole of the ordering: ``merge`` starts once that data is ready, and nothing says "after reco" anywhere.
* ``reco`` names its output ``--outputAODFile``, so its key is ``AOD``. ``merge`` names its own ``--outputAOD_MRGFile``, whose derived key would be ``AOD_MRG``, so the step-level ``outputs`` map renames it to the plainer ``AOD``.
* ``outputs`` declares what the workflow produces, here ``merge/AOD``.
* Both steps ask for ``parent_tid``. ``merge`` gets the task of ``reco``; ``reco`` takes only an external input, so it has no parent and its task becomes its own, which is how a chain root is recorded. Both set ``noWaitParent``, so JEDI leaves the ordering to the engine.
* ``${WFID}`` and ``${TASKID}`` appear in the dataset names, and ``${SN}`` and ``${IN/L}`` are left for JEDI to expand per job.

The nine-task ATLAS chain this is cut down from lives in the panda-server repository, at :brown:`pandaserver/workflow/examples/production_chain_wfd.json`, with real transformation parameters throughout.

|br|

Steps that carry task parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Other step types build their parameters from a command line. A step of :hblue:`type: task` supplies them directly: :hblue:`task_params` is the :doc:`task parameter map </advanced/task_params>`, and the engine passes it through untouched, as both steps of the example above do.

``taskName``, ``jobParameters``, ``log``, ``transPath``, ``vo`` and ``prodSourceLabel`` are required, and the description is rejected on submission without them. A step whose ``prodSourceLabel`` is a production one is refused unless the submitter holds a production role.

|br|

Inputs: naming another step's output
======================================

An input job parameter names its dataset by reference rather than by name, since the name a producing step will use is not known until its task exists.

.. list-table::
   :header-rows: 1

   * - Reference
     - Resolves to
   * - :hblue:`{step_name/output_key}`
     - The dataset the named step produced, once it has been submitted
   * - :hblue:`{workflow_input}`
     - An entry of the workflow ``inputs`` section, i.e. a dataset the workflow does not produce

Anything else in a ``dataset`` field is taken literally and reaches JEDI as written. Only references take part in the workflow graph, and that graph is what decides when each step may start.

|br|

Outputs: one workflow datum per output parameter
==================================================

Every job parameter with :hblue:`param_type: output` becomes one output of the step, so a step producing several datasets exposes each of them independently and downstream steps consume whichever they need.

The key is derived from the leading command line option, with the ``output`` prefix and ``File`` suffix removed, so ``--outputDAOD_PHYSFile`` becomes ``DAOD_PHYS`` and the output is referenced as :hblue:`{deriv_phys/DAOD_PHYS}`. A step-level :hblue:`outputs` map overrides that where the derived name would be awkward: ``{"HITS": "--outputHITS_MRGFile"}`` exposes the merge step's output as the plainer :hblue:`{merge_hits/HITS}`.

|br|

Late-bound IDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Two IDs are not known when the description is written. PanDA substitutes both before the task parameters reach JEDI.

.. list-table::
   :header-rows: 1

   * - Placeholder
     - Is
     - Resolved
   * - :hblue:`${WFID}`
     - The workflow ID
     - When the workflow is registered and its description parsed
   * - :hblue:`${TASKID}`
     - The JEDI task ID of the step's own task
     - When that step's task is submitted
   * - :hblue:`${PARENT_TASKID}`
     - The JEDI task ID of the step feeding this one
     - Before that step's task is submitted, since it is an input to the submission

``${PARENT_TASKID}`` is the exception to the rest of this: nothing in the engine uses it. A step starts from its data, not from a parent task, so the engine never reads ``parent_tid``. Production machinery does, which is why a step may ask for it to be filled:

.. code-block:: json

    {"task_params": {"parent_tid": "${PARENT_TASKID}", "noWaitParent": true}}

The engine then records the task of the step producing this step's input. A step whose inputs all come from outside the workflow submits with no parent, so JEDI makes its task its own parent, as a chain root is recorded today. It is per step and entirely optional: leave ``parent_tid`` out and nothing is set.

A step fed by more than one step has to say which one is meant, since ``parent_tid`` holds a single task. Name it: :hblue:`${PARENT_TASKID:merge_hits}`, using the step name, which is the part that can be known when the description is written. The named step has to be one of those feeding this one, so that ``parent_tid`` and the relation queries describe the same relation. A task ID outright, ``"parent_tid": 52397622``, is also accepted, and is the way to attach a chain to a task that already exists outside the workflow.

Set ``noWaitParent`` alongside it, as the production examples do. Without it JEDI holds the task until the parent is done, on top of the engine's own ordering; the server logs a warning if it is missing.

Use the other two anywhere in ``task_params``, dataset names included. They are distinct from the JEDI per-job templates such as ``${SN}``, ``${MAXEVENTS}`` and ``${IN_HITS/L}``, which PanDA leaves untouched for JEDI to expand per job, and from ``$JEDITASKID``, which JEDI substitutes into job file names for non-production tasks only.

|br|

Submitting a description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A description made of ``task`` steps needs no sandbox, since the steps carry their parameters verbatim and take their transformation from cvmfs. It is posted as JSON to :brown:`/v1/workflow/submit_workflow_description`.

.. code-block:: python

    import os
    import requests

    pandaurl = "https://pandaserver.cern.ch:25443"
    proxy = os.environ["X509_USER_PROXY"]
    response = requests.post(
        f"{pandaurl}/api/v1/workflow/submit_workflow_description",
        json={"workflow_description": description},
        cert=(proxy, proxy),
        verify=os.environ["X509_CERT_DIR"],
    )
    workflow_id = response.json()["data"]["workflow_id"]

The description is validated structurally before the call returns, so an authoring mistake comes back on the request rather than surfacing later as a cancelled workflow. A ``taskName`` that already exists is reported in the ``message`` field as a warning and does not prevent registration.

Parsing itself is asynchronous. The response means the workflow is registered, not that its steps have started.

|br|

Asking how the steps and tasks relate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since the engine starts a step from its inputs, it holds no step-to-step edge of its own. Consumers that model a chain as related tasks can ask for the relations, which are derived on each call from the data passed between the steps.

A task created by a native workflow carries no ``parent_tid``. The engine decides when each step may start, and a task whose ``parent_tid`` names a real parent is handled differently by JEDI. These queries are what replaces reading that field.

Both are GET, and both answer for a running workflow as readily as for a finished one.

|br|

Step relations
================

:brown:`/v1/workflow/get_step_relations?workflow_id=133` reports every step with its target, whatever kind of target it is.

.. code-block:: json

    {"workflow_id": 133,
     "steps": [
       {"step_id": 516, "name": "evgen", "type": "ordinary", "flavor": "panda_task",
        "status": "done", "target_id": "52382519", "parent_step_ids": []},
       {"step_id": 517, "name": "merge_evnt", "type": "ordinary", "flavor": "panda_task",
        "status": "done", "target_id": "52382898", "parent_step_ids": [516]}
     ]}

A step whose inputs all come from outside the workflow has no parent, rather than being its own parent. A step that has not started yet has no ``target_id``, while its place in the graph is already known.

|br|

Task relations
================

:brown:`/v1/workflow/get_task_relations` reports the same graph in terms of JEDI tasks alone. Give it either ``workflow_id``, for a whole chain, or ``task_id``, to enter at a task without knowing which workflow it belongs to.

.. code-block:: json

    {"workflow_id": 133,
     "tasks": [
       {"key": "133:516", "task_id": 52382519, "workflow_id": 133, "step_id": 516,
        "name": "evgen", "flavor": "panda_task", "status": "done", "parents": []},
       {"key": "133:517", "task_id": 52382898, "workflow_id": 133, "step_id": 517,
        "name": "merge_evnt", "flavor": "panda_task", "status": "done", "parents": ["133:516"]}
     ]}

Three properties of this view are worth knowing:

* **Parents are a set.** A step may consume the outputs of several earlier steps, so a task may have more than one parent. No primary parent is nominated.
* **A step that is not a JEDI task is collapsed**, and a step running a nested workflow is replaced by the tasks inside it. A chain of task, other step, task is therefore reported as one relation between the two tasks rather than as a gap, and the view stays complete as the engine gains step targets that are not tasks.
* **A step not yet submitted is a placeholder** with ``task_id`` null. Dropping it would make a task whose producer has not started look like a task with no producer at all.

Parents are named by ``key`` rather than by task ID, because a placeholder has no ID to be named by. Every entry carries its own ``task_id``, so resolving a key is a lookup in the same list. Entries come back parents first, and entering by ``task_id`` adds ``asked_for``, the key of the task asked about.

|br|

Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every parameter and response of these endpoints is in the `API documentation page <../_static/panda_api.html#tag/workflow>`_, under the ``workflow`` tag.

|br|
