=====================================
Production Native Workflows
=====================================

Running a production chain as a single PanDA native workflow: the description language a chain is written in, the endpoints that submit and follow it, and a complete worked example.

The engine is data-driven. A step starts when the data it consumes is good enough to start on, not when a parent step announces it has finished, so a chain is described by saying what each step takes and produces and letting the engine derive the order. A production description differs from an analysis one in carrying raw PanDA task parameters per step rather than a command line, which is what lets a chain be translated from tasks that already exist.

For native workflows submitted as analysis work, see :doc:`/advanced/native_workflow_analysis/index`. For the client-side command and the workflow description language as an end user meets it, see :doc:`/client/pchain_native`.

.. toctree::
   :maxdepth: 1

   description
   example
