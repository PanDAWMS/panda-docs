=========================
Running workflow using Snakemake
=========================

A workflow can be also described using Python-based workflow description language (WDL) - Snakemake.
In this case the user can use Python language syntax and JSON configuration files.
The following examples demonstrate how to describe common workflows using Snakemake syntax and
snakeparser helper Python module.

.. contents:: Table of Contents
    :local:

-----------

Workflow examples
^^^^^^^^^^^^^^^^^^^^^^

Common JSON configuration file using by examples
======================

.. literalinclude:: examples/config.json
    :language: json
    :caption: config.json

Simple task chain
======================

.. literalinclude:: examples/simple_chain/Snakefile
    :language: yaml
    :caption: simple_chain/Snakefile

``# noinspection`` directives can be used if a workflow is described using PyCharm IDE with SnakeCharm plugin.
In other case these directives can be omitted.
To use parent output as input the user should specify ``rules.${parent_rule_name}.output[0]`` as value
for the corresponding parameter (``opt_inDS``) and specify ``rules.${parent_rule_name}.output`` for ``input`` keyword.

More complicated chain
========================

.. literalinclude:: examples/sig_bg_comb/Snakefile
    :language: yaml
    :caption: sig_bg_comb/Snakefile

To use parameter from another step the user should use the helper function ``param_of`` from
``pandaserver.workflow.snakeparser.utils`` library.
For example, ``param_of("${name_of_parameter}",source=rules.all)``, where ${name_of_parameter} should be replaced by
actual parameter name and source refers to the parameter step.
If step parameter value contains patterns like ``%{SECDS1}`` the helper function ``param_exp`` should be used.
To use multiple inputs (multiple parents) ``input`` keyword should contain all references separated by commas.

Sub-workflow and parallel execution with scatter
=================================================

.. literalinclude:: examples/merge_many/Snakefile
    :language: yaml
    :caption: merge_many/Snakefile

Using Athena
================

.. literalinclude:: examples/athena/Snakefile
    :language: yaml
    :caption: athena/Snakefile

Conditional workflow
======================

.. literalinclude:: examples/cond/Snakefile
    :language: yaml
    :caption: cond/Snakefile

``when`` keyword was added as Snakemake language extension to define step conditions.

Involving hyperparameter optimization
=======================================

.. literalinclude:: examples/hpo/Snakefile
    :language: yaml
    :caption: hpo/Snakefile

Loops in workflows
====================

.. literalinclude:: examples/loop/Snakefile
    :language: yaml
    :caption: loop/Snakefile

.. literalinclude:: examples/loop_body/Snakefile
    :language: yaml
    :caption: loop_body/Snakefile

``loop`` keyword was added as Snakemake language extension to define step as a loop.

Loop + scatter
====================

Running multiple loops in parallel
++++++++++++++++++++++++++++++++++++++

.. literalinclude:: examples/multi_loop/Snakefile
    :language: yaml
    :caption: multi_loop/Snakefile

A sub-workflow filename should be specified in ``shell`` keyword.

Parallel execution of multiple sub-workflows in a single loop
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. literalinclude:: examples/sequential_loop/Snakefile
    :language: yaml
    :caption: sequential_loop/Snakefile

.. literalinclude:: examples/scatter_body/Snakefile
    :language: yaml
    :caption: scatter_body/Snakefile

.. literalinclude:: examples/loop_main/Snakefile
    :language: yaml
    :caption: loop_main/Snakefile

Using REANA
=============

.. literalinclude:: examples/reana/Snakefile
    :language: yaml
    :caption: reana/Snakefile
