===================================
JEDI Watchdogs
===================================

JEDI Watchdogs are dogs. Each watchdog has specific periodic mission to execute.

Watchdogs run independently of JEDI agents and of other watchdogs; i.e. they can run in parallel without blocking one another.

Watchdog is plugin-based so one can write new watchdogs to extend features of JEDI.

|br|

JEDI Configuration
""""""""""""""""""

General watchdog configuration is in :ref:`jedi configuration <installation/jedi:panda_jedi.cfg>`

Specific configuration is mentioned in the section of each watchdog below.

|br|


Data Locality Updater
---------------------

module path: ``pandajedi.jedidog.AtlasDataLocalityUpdaterWatchDog``
class name: ``AtlasDataLocalityUpdaterWatchDog``

configuration example:

.. code-block:: text

    [watchdog]
    modConfig = (...),atlas:managed:pandajedi.jedidog.AtlasDataLocalityUpdaterWatchDog:AtlasDataLocalityUpdaterWatchDog:DataLocalityUpdater,(...)
    procConfig = (...);atlas:managed:1:DataLocalityUpdater:43200;(...)

Here we ask JEDI to run 1 process of Data Locality Updater with a period of 43200 seconds (12 hours).

requirement: ``JEDI_Dataset_Locality`` table exists in PanDA DB.


**Description**

Data Locality Updater queries Rucio periodically about the RSEs which store input datasets of all active production tasks.

The results are stored in ``JEDI_Dataset_Locality`` table.

This allows other JEDI components to find the available RSEs (and hence PQs) for a task from the DB, which is more efficient than to query Rucio for the task on the fly.


**GDPconfig Parameters**

(None)


|br|

Task Withholder
---------------------

module path: ``pandajedi.jedidog.AtlasTaskWithholderWatchDog``
class name: ``AtlasTaskWithholderWatchDog``

configuration example:

.. code-block:: text

    [watchdog]
    modConfig = (...),atlas:managed:pandajedi.jedidog.AtlasTaskWithholderWatchDog:AtlasTaskWithholderWatchDog:TaskWithholder,(...)
    procConfig = (...);atlas:managed:1:TaskWithholder:1800;(...)

Here we ask JEDI to run 1 process of Task Withholder with a period of 1800 seconds (30 minutes).

requirement: Data Locality Updater watchdog is running


**Description**

A tasks can become temporarily hopeless to run when all sites containing the required inputs are too busy or offline.

Task Withholder finds out these apparent hopeless tasks and withhold them by setting them to be in pending status, so that JEDI brokerage does not need to broker for these tasks temporarily and thus increase performance.

The tasks set to be pending will be released as other pending tasks for other reasons will.


**GDPconfig Parameters**

- ``jedi.task_withholder.LIMIT_IOINTENSITY_managed`` : For prodSourceLabel=managed, only tasks with ioIntensity higher than this value will be considered to be withheld
- ``jedi.task_withholder.LIMIT_PRIORITY_managed`` : For prodSourceLabel=managed, only tasks with currentPriority lower than this value will be considered to be withheld


|br|

Queue Filler
---------------------

module path: ``pandajedi.jedidog.AtlasQueueFillerWatchDog``
class name: ``AtlasQueueFillerWatchDog``

configuration example:

.. code-block:: text

    [watchdog]
    modConfig = (...),atlas:managed:pandajedi.jedidog.AtlasQueueFillerWatchDog:AtlasQueueFillerWatchDog:QueueFiller,(...)
    procConfig = (...);atlas:managed:1:QueueFiller:600;(...)

Here we ask JEDI to run 1 process of Queue Filler with a period of 600 seconds (10 minutes).

requirement: Data Locality Updater watchdog is running


**Description**

Queue Filler finds out empty sites and pre-assigns some proper production tasks to these sites to fill them with jobs.

Here a proper production tasks satisfies:
* The certain site to be filled has the input datasets of the task
* The tasks satisfies the constraints about the site (defined on CRIC); e.g. memory
* The task still has enough ready but un-processed files, so that it will have enough jobs to fill the queue

When a site is no longer empty, the tasks pre-assign to the site by Queue Filler will be released.


**GDPconfig Parameters**

- ``jedi.queue_filler.MAX_PREASSIGNED_TASKS_managed`` : Max number of production tasks to pre-assign to an empty queue per resource type
- ``jedi.queue_filler.MIN_FILES_READY_managed`` : Min number of ready files a task which can be pre-assigned should have
- ``jedi.queue_filler.MIN_FILES_REMAINING_managed`` : Min number of remaining files a task which can be pre-assigned should have


|br|

|br|
