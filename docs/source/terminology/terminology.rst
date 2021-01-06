============
Terminology
============

PanDA components
-----------------
.. figure:: images/PandaSys.png

There are 5 components in the PanDA system as shown in the schematic view above.

* :ref:`architecture/jedi:JEDI` is the high-level engine to dynamically tailor workload for optimal usage of heterogeneous resources.

* :ref:`architecture/server:PanDA server` is the central hub implemented as a stateless REST web service to allow asynchronous communication from users, :ref:`architecture/pilot:Pilot`, and :ref:`architecture/harvester:Harvester` over HTTPS.

* :ref:`architecture/pilot:Pilot` is a transient agent to execute workload with actual compute and storage resources, periodically reporting various metrics to :ref:`architecture/server:PanDA server` throughout its lifetime.

* :ref:`architecture/harvester:Harvester` provisions :ref:`architecture/pilot:Pilot` on resources using the relevant communication protocol for each resource provider, and communicates with :ref:`architecture/server:PanDA server` on behalf of :ref:`architecture/pilot:Pilot` if necessary.

* :ref:`architecture/monitor:PanDA monitor` is a web based monitoring and browsing that provides a common interface to PanDA for users and system administrators.

:ref:`architecture/jedi:JEDI` and :ref:`architecture/server:PanDA server` share the central database
for workload management.
:ref:`architecture/monitor:PanDA monitor` has only read access to the central database,
while :ref:`architecture/harvester:Harvester` uses own database which is ether central or local
depending on its deployment model.
PanDA components and database are explained in :ref:`architecture/architecture:System Architecture`
and :ref:`database/database:Database`, respectively.

----------

|br|

Task
-----

A task is a unit of workload to accomplish an indivisible scientific objective.
If an objective is done in multiple steps each step is mapped to a task.
A task takes input and produces output. Generally input and output are collections
of data files but there are also other formats, such as a group of sequence numbers,
metadata, notification, void, and so on. Each task has a unique
identifier **JediTaskID** in the system.

Task status changes as shown in the following figure.

.. figure:: images/jediTaskStatus.png

|br|

Yellow boxes in the figure show commands sent to PanDA by external actors to trigger
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

-------

|br|

Job
-------


Push and Pull
--------------

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
