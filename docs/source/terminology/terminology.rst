============
Terminology
============


.. toctree::

Task, and its Input and Output
-------------------------------

A task is a unit of workload to accomplish an indivisible scientific objective.
If an objective is done in multiple steps each step is mapped to a task.
A task takes input and produces output. Generally input and output are collections
of data files but there are also other formats, such as a group of sequence numbers,
metadata, notification, void, and so on. Each task has a unique
identifier in the system.

Task status changes as shown in the following figure.

.. figure:: images/jediTaskStatus.png

Yellow boxes in the figure show commands sent to PanDA by external actors which trigger
task status transition. Here is the list of task statuses and their descriptions.

* registered
   The task was injected to PanDA.

* defined
   All task parameters were properly parsed.

* assigning
   The :ref:`terminology/terminology:Brokerage` is assigning the task to a storage resource.

* ready
   The task is ready to generate jobs which are explained in the :ref:`terminology/terminology:Job` section.

* pending
   The task has a temporary problem, e.g. there is no free compute resources to work for new jobs.

* scouting
   The task is running scout jobs to gather job metrics.

* scouted
   Enough number of scout jobs were successfully finished and job metrics were calculated.

* running
   The task avalanches to generate more jobs.

* prepared
   The workload of the task was done and the task is ready to run the post-processing step.

* done
   The entire workload of the task was successfully processed.

* failed
   The entire workload of the task was failed.

* finished
   The workload of the task partially succeeded.

* aborting
   The task got the kill command.

* aborted
   The task was killed.

* finishing
   The task got the finish command to terminate processing in the middle.

* topreprocess
   The task is ready to run the pre-processing step.

* preprocessing
   The task is running pre-processing.

* tobroken
   The task is going to be broken.

* broken
   The task is broken, e.g., due to wrong parameters.

* toretry
   The task got the retry command.

* toincexec
   The task got the incexec (incremental execution) command.

* rerefine
   The task is changing parameters for incremental execution.

* paused
   The task is paused and doesn't do anything until it is resumed.

* throttled
   The task is throttled not to generate new jobs.


Job
-------

Brokerage
----------

Worker node
------------

Heartbeat
----------

Walltime
---------

Global share
-------------

Priority
---------

Resource type
--------------

Users
---------

User's identity and group
--------------------------

Retry
-----
