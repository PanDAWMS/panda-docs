==========================================================
Generating native workflow descriptions programmatically
==========================================================

:doc:`PanDA native workflows </client/pchain_native>` are normally described in a hand-written
yaml file. When the shape of the workflow is not known in advance, for instance because the number
of steps depends on the data, or when the description is produced by another tool, the yaml can be
generated instead.

``panda-client`` ships :brown:`pandaclient.workflow_description.WorkflowDescription`, a small
builder that writes workflow descriptions. It is the same module the built-in workflow templates
are made of.

.. contents:: Table of Contents
    :local:

-----------

|br|

Building a description
=============================

.. code-block:: python

    from pandaclient.workflow_description import WorkflowDescription

    wf = WorkflowDescription(name="my_chain")
    wf.add_input("raw", "user.me:my.input.dataset")
    wf.add_prun_step(
        "step1",
        in_ds=WorkflowDescription.input_ref("raw"),
        args="--outputs out.root --nGBPerJob 10",
        executable="run.sh",
    )
    wf.add_prun_step(
        "step2",
        in_ds=WorkflowDescription.step_output("step1"),
        args="--outputs final.root",
        executable="run.sh",
    )
    wf.add_output("result", from_ref=WorkflowDescription.step_output("step2"),
                  output_types=["final.root"])
    wf.set_option("allow_partial_inputs", True)
    wf.validate()
    wf.save("my_chain.yaml")

Every mutating method returns the builder, so the calls can be chained.

.. list-table::
   :header-rows: 1

   * - Method
     - Purpose
   * - add_input(name, dataset)
     - Register a named entry of the workflow ``inputs`` section
   * - add_prun_step(name, in_ds, args, executable, ...)
     - Add a ``prun`` step. Also takes in_ds_type, secondary_dss, secondary_ds_types,
       use_athena_packages and container_image
   * - add_step(name, step_type, ...)
     - The same for a step of any other type
   * - add_output(name, from_ref, output_types)
     - Register a named entry of the workflow ``outputs`` section
   * - set_option(key, value)
     - Set a workflow-level option, e.g. ``allow_partial_inputs``
   * - input_ref(name) / step_output(name)
     - Produce the :hblue:`{name}` and :hblue:`step/outDS` references of the description
       language, so they do not have to be spelled out as strings
   * - validate()
     - Check the references locally, see below
   * - to_dict() / to_json() / to_yaml() / save(path)
     - Serialize the result

The resulting file is submitted with ``pchain_native --wfd`` like any hand-written description.

|br|

Validating before submission
==============================

``validate()`` checks that every reference resolves to a declared input or an existing step, and
that ``secondaryDsTypes`` has as many entries as ``secondaryDSs``. It raises ``ValueError`` listing
all the problems it found, so it is worth calling before ``save()``.

It is a local, structural check only. Whether the ``prun`` options in ``args`` are valid, and
whether the input datasets exist, is decided when the server parses the submitted description.

|br|

Adding a workflow template
==============================

The :ref:`workflow templates <client/pchain_native:Using workflow templates>` of
``pchain_native`` are ordinary Python modules built on this class. To add one to ``panda-client``,
put a module exposing a ``build(**kwargs)`` function that returns a ``WorkflowDescription`` under
:brown:`pandaclient/workflow_templates/`, and register it in
:brown:`pandaclient/workflow_template_dispatcher.py`.

``build()`` receives the ``--inDS`` value as :brown:`in_ds`, the parsed ``--prunFlags`` as a
:brown:`prun_flags` dict, and :brown:`verbose`. Whatever else the template needs, it works out for
itself: :brown:`multistep_merge`, for example, asks Rucio how many files the input dataset holds
in order to decide how many merge steps to generate.

|br|
