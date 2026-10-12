=====================================
A Production Workflow End to End
=====================================

One complete production chain, from the description that defines it to the calls that submit it and follow it to the end.

The description language and the endpoints are covered in :doc:`/advanced/native_workflow_production/description`; this page is the worked example, meant to be copied and run against a real server. It uses no sandbox and no client installation, only an X509 proxy and ``requests``.

.. contents:: Table of Contents
    :local:

-----------

|br|

The chain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nine steps, taken from a real ATLAS production chain with its request and account identifiers replaced by example values. Generation runs first, each stage merges before the next consumes it, and two derivations branch off the merged AOD:

.. code-block:: text

    evgen -> merge_evnt -> simul -> merge_hits -> recon -> merge_aod -> deriv_prw -> merge_ntup
                                      ^                        |
                                   {rdo_bkg}                   +-> deriv_phys

Two properties of the chain are worth noticing before reading the description itself.

``recon`` has two inputs. One is the output of ``merge_hits``, named by reference; the other is the pileup dataset named by the ``rdo_bkg`` workflow input, which exists outside the workflow. A step takes as many inputs as it needs, from either source.

``deriv_phys`` runs under a different account. The rest of the chain is submitted under one ``userName``, ``workingGroup`` and ``reqID``; ``deriv_phys`` carries its own, as a chain does when it hands a derivation to another group. Because these are authored in the description rather than taken from the submitter, a submitter holding a production role keeps them exactly as written.

.. list-table::
   :header-rows: 1

   * - Step
     - Takes
     - Produces
   * - ``evgen``
     - nothing; generates from a seed
     - ``EVNT``
   * - ``merge_evnt``
     - ``{evgen/EVNT}``
     - ``EVNT``
   * - ``simul``
     - ``{merge_evnt/EVNT}``
     - ``HITS``
   * - ``merge_hits``
     - ``{simul/HITS}``
     - ``HITS``
   * - ``recon``
     - ``{merge_hits/HITS}`` and ``{rdo_bkg}``
     - ``AOD``
   * - ``merge_aod``
     - ``{recon/AOD}``
     - ``AOD``
   * - ``deriv_prw``
     - ``{merge_aod/AOD}``
     - ``NTUP_PILEUP``
   * - ``merge_ntup``
     - ``{deriv_prw/NTUP_PILEUP}``
     - ``NTUP_PILEUP``
   * - ``deriv_phys``
     - ``{merge_aod/AOD}``
     - ``DAOD_PHYS`` and ``DAOD_PHYSLITE``

|br|

The description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: wfd/production_full_chain.json
    :language: json
    :caption: production_full_chain.json

|br|

Submitting it
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The description is posted as JSON. Nothing else is needed: a description made of ``task`` steps carries its parameters verbatim and takes its transformations from cvmfs.

.. code-block:: python

    import json
    import os

    import requests

    PANDA_URL = "https://pandaserver.cern.ch:25443/api/v1"
    PROXY = os.environ["X509_USER_PROXY"]
    SESSION_ARGS = {"cert": (PROXY, PROXY), "verify": os.environ["X509_CERT_DIR"]}

    with open("production_full_chain.json") as description_file:
        description = json.load(description_file)

    response = requests.post(
        f"{PANDA_URL}/workflow/submit_workflow_description",
        json={"workflow_description": description},
        **SESSION_ARGS,
    )
    body = response.json()
    if not body["success"]:
        raise SystemExit(f"submission refused: {body['message']}")

    workflow_id = body["data"]["workflow_id"]
    print(f"registered workflow_id={workflow_id}")
    if body["message"]:
        print(f"warning: {body['message']}")

Whether the steps run as production work is decided by the submitter's credentials, not by the description: a submitter holding a production role gets ``managed`` work that keeps the ``userName`` and ``taskType`` the description authored. A request that claims a production role in its body is ignored.

The response means the description was accepted and stored, not that anything has started. It is checked for structure before the call returns, so a mistake in a reference or a missing required field comes back on the request itself. A ``taskName`` that already exists is reported in ``message`` as a warning and does not prevent registration. Turning the description into steps happens afterwards, on the server.

|br|

Following it
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:brown:`/v1/workflow/get_workflow_status` answers for the workflow as a whole. It is the call to poll.

.. code-block:: python

    import time

    FINAL_STATUSES = {"done", "failed", "cancelled"}

    while True:
        response = requests.get(
            f"{PANDA_URL}/workflow/get_workflow_status",
            params={"workflow_id": workflow_id},
            **SESSION_ARGS,
        )
        status_info = response.json()["data"]
        print(f"{status_info['status']}  {status_info['step_status_counts']}")
        if status_info["status"] in FINAL_STATUSES:
            break
        time.sleep(600)

A production chain takes days, so poll at the pace of the work rather than of the loop above. The counts move as the chain progresses:

.. code-block:: json

    {"workflow_id": 133, "name": "example_full_chain", "status": "running", "parent_id": null,
     "creation_time": "2026-10-12T09:14:03", "start_time": "2026-10-12T09:15:01",
     "end_time": null, "n_steps": 9,
     "step_status_counts": {"done": 3, "running": 1, "pending": 5}}

|br|

Reading it as tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:brown:`/v1/workflow/get_task_relations` reports the same chain in terms of JEDI tasks, which is what a consumer that models production as related tasks wants. Each entry carries the task the step produced and the keys of the tasks feeding it.

.. code-block:: python

    response = requests.get(
        f"{PANDA_URL}/workflow/get_task_relations",
        params={"workflow_id": workflow_id},
        **SESSION_ARGS,
    )
    tasks = response.json()["data"]["tasks"]

    task_of_key = {entry["key"]: entry["task_id"] for entry in tasks}
    for entry in tasks:
        parents = [task_of_key[key] for key in entry["parents"]]
        print(f"{entry['name']:<12} task_id={entry['task_id']}  parents={parents}")

Parents are a set rather than a single task, because a step may consume the outputs of several; ``recon`` has one parent here only because its other input comes from outside the workflow. A step that has not been submitted yet appears with ``task_id`` null, so that a task whose producer has not started is not mistaken for a task with no producer. Keys are ``"<workflow_id>:<step_id>"``, since a step without a task has no task ID to be named by.

A task's own status comes from the task API, as for any other task:

.. code-block:: python

    response = requests.get(
        f"{PANDA_URL}/task/get_status",
        params={"task_id": task_of_key["133:516"]},
        **SESSION_ARGS,
    )
    print(response.json()["data"])

|br|

What a failure looks like from here
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If one task of the chain fails, the workflow fails, and the engine cancels the steps that had not finished and kills their tasks. Polling then returns something of this shape:

.. code-block:: json

    {"workflow_id": 133, "status": "failed",
     "reason": "step recon (step_id=525) failed: task 48810706 reported broken",
     "end_time": "2026-10-12T11:02:44", "n_steps": 9,
     "step_status_counts": {"done": 4, "failed": 1, "cancelled": 4}}

The single ``failed`` is the step that broke; the ``cancelled`` ones are the steps stopped behind it, whether they were running or had never started. ``reason`` names the step and what its task reported. For the error itself, take that step's ``target_id`` from :brown:`/v1/workflow/get_step_relations` and read it on the task.

Each step of :brown:`/v1/workflow/get_step_relations` carries its own ``reason``, so a cancelled step says it went with the workflow rather than leaving the reader to guess.

A failed workflow is final, and there is no retry or cancel endpoint. Recovery is to submit a description again. :ref:`When a step fails <advanced/native_workflow_production/description:When a step fails>` sets out the rules in full.

|br|
