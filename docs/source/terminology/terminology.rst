============
Terminology
============

.. contents::
    :local:

----------

|br|

Compute and storage resources
------------------------------
Compute resource providers, such as the grid, HPC centers, and commercial cloud services, offer compute resources with
processing capabilities. The minimum unit in each compute resource is a (virtual) host, a host cluster, or a slot on a host,
depending on workload or resource configuration.
The object with the minimum unit represents a combination of CPUs, memory, and a scratch disk to process workload.
Storage resource providers accommodate data storage needs. A storage resource is composed of a persistent data storage
with disk, tape, or their hybrid, and a storage management service running on top of it.
Association between compute and storage resources can be arbitrary, but in most cases
resources from the same provider are associated with each other.

PanDA integrates heterogeneous compute and storage resources to provide a consistent interface to users. Users
can seamlessly process their workload on compute resources while taking input data from storage resources and
uploading
output data to storage resources, without paying attention on the details of compute and storage technologies.


-----

|br|

PanDA components
-----------------
.. figure:: images/PandaSys.png

There are 5 components in the PanDA system as shown in the schematic view above.

* **JEDI** is the high-level engine to dynamically tailor workload for optimal usage of heterogeneous resources.

* **PanDA server** is the central hub implemented as a stateless REST web service to allow asynchronous communication from users, Pilot, and Harvester over HTTPS.

* **Pilot** is a transient agent to execute workload with actual compute and storage resources, periodically reporting various metrics to PanDA server throughout its lifetime.

* **Harvester** provisions Pilot on resources using the relevant communication protocol for each resource provider, and communicates with PanDA server on behalf of Pilot if necessary.

* **PanDA monitor** is a web based monitoring and browsing that provides a common interface to PanDA for users and system administrators.

JEDI and PanDA server share the central database
for workload management.
PanDA monitor has only read access to the central database,
while Harvester uses own database which is ether central or local
depending on its deployment model.
PanDA components and database are explained in :doc:`System Architecture </architecture/architecture>`
and :doc:`Database </database/database>` pages, respectively.

----------

|br|

Task
-----

A task is a unit of workload to accomplish an indivisible scientific objective.
If an objective is done in multiple steps each step is mapped to a task.
A task takes input and produces output. The goal of the task is to process the input
entirely.
Generally input and output are collections
of data files but there are also other formats, such as a group of sequence numbers,
metadata, notification, void, and so on. Each task has a unique
identifier **JediTaskID** in the system.

Task status changes as shown in the following figure.

.. figure:: images/jediTaskStatus.png

|br|

Yellow boxes in the figure show commands sent to PanDA by external actors to trigger
task status transition. Here is the list of task statuses and their descriptions.

registered
   The task was injected to PanDA.

defined
   All task parameters were properly parsed.

assigning
   The task is being assigned to a storage resource.

ready
   The task is ready to generate jobs which are explained in the :ref:`terminology/terminology:Job` section.

pending
   The task has a temporary problem, e.g. there is no free compute resources to work for new jobs.

scouting
   The task is running scout jobs to gather job metrics.

scouted
   Enough number of scout jobs were successfully finished and job metrics were calculated.

running
   The task avalanches to generate more jobs.

prepared
   The workload of the task was done and the task is ready to run the post-processing step.

done
   The entire workload of the task was successfully processed.

failed
   The entire workload of the task was failed.

finished
   The workload of the task partially succeeded.

aborting
   The task got the kill command.

aborted
   The task was killed.

finishing
   The task got the finish command to terminate processing in the middle.

topreprocess
   The task is ready to run the pre-processing step.

preprocessing
   The task is running pre-processing.

tobroken
   The task is going to be broken.

broken
   The task is broken, e.g., due to wrong parameters.

toretry
   The task got the retry command.

toincexec
   The task got the incexec (incremental execution) command.

rerefine
   The task is changing parameters for incremental execution.

paused
   The task is paused and doesn't do anything until it is resumed.

throttled
   The task is throttled not to generate new jobs.

-------

|br|

Job
-------
A job is an artificial unit of sub-workload partitioned from a task. A single task is composed of multiple jobs,
and each job runs on the minimum unit of the compute resource.
Each job is tailored based on user's preference (if any) and/or constraints on the compute resource.
For example, if job size is flexible, jobs are generated to have short execution time and produce small output files
when they are processed on resources with limited time slots and local scratch disk spaces.
The task input is logically split to multiple subsets and each job gets a subset to produce output.
The collection of job output is the task output.

Job status sequentially changes as follows:

pending
   The job is generated.

defined
   The job is ready to work for global input data motion if necessary. E.g., data transfer from a remote storage
   resource to the "local" storage resource close to the compute resource.

assigned
   Input data are being transferred to the "local" storage resource. This status is skipped if the job doesn't need
   global input data motion or physical input data.

activated
   The job is ready to be dispatched as soon as the compute resource becomes available.

sent
   The job was dispatched to the compute resource.

starting
   The job is working for the last-mile input data motion, such as data stage-in from the "local" storage to
   the scratch disk attached to the compute resource.

running
   The job is processing input data.

holding
   The job finished processing, reported the final metrics, and released the compute resource.

merging
   Output data are being merged. This status is skipped unless the task is configured to merge job output.

transferring
   Output data are being transferred to the final destination.

|br|

And goes to one of the final statues described below:

finished
   The job successfully produced output and it is available at the final destination.

failed
   The job failed in the middle.

closed
   The system terminated the job before running on a compute resource.

cancelled
   The job was manually aborted.

----------

|br|

Push and Pull
--------------

Brokerage
----------


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
