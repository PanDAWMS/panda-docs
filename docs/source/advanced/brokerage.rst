====================================
Job Brokerage
====================================

The job brokerage is the most crucial component in the system to distribute workload among computing resources
with the following goals:

* To assign enough jobs to computing resources to utilize all available CPUs continuously.

* To minimize the waiting time for each job to produce output data.

* To execute jobs in such a way that the jobs respect their priorities and resource allocations.

* To choose computing resources for each job based on characteristics of the job and constraints of the computing resources.

It is not straightforward to satisfy the goals for all jobs since some of them are logically contradictory.
The job brokerage has a plugin structure so that organizations can provide their algorithms according to
their needs and use-cases.

This page explains the algorithms of some plugins.

------------

|br|

ATLAS Production
---------------------

This is the general ATLAS production job brokerage flow:

#. Generate the list of preliminary candidates from one of the following:

   * All queues while excluding any queue with case-insensitive 'test' in the name.

   * A list of pre-assigned queues. Unified queues are resolved to pseudo-queues. Although merge jobs are pre-assigned
     to avoid transferring small pre-merged files, the pre-assignment is ignored if the relevant queues have been skipped
     for 24 hours.

#. Filter out preliminary candidates that don't pass any of the following checks:

   * The queue status must be *online* unless the queues are pre-assigned.

   * Skip queues if their links to the nucleus are blocked.

   * Skip queues if over the ``NQUEUED_SAT_CAP`` (defined in :doc:`gdpconfig </advanced/gdpconfig>`) files queued
     on their links to the nucleus.

   * Skip all queues if the number of files to be aggregated to the nucleus is larger than ``NQUEUED_NUC_CAP_FOR_JOBS``
     (defined in :doc:`gdpconfig </advanced/gdpconfig>`).

   * If priority :raw-html:`&GreaterEqual;` 800 or scout jobs, skip queues unless associated with the nucleus.

   * If priority :raw-html:`&GreaterEqual;` 800 or scout jobs or merging jobs or pre-merged jobs, skip inactive queues
     (where no jobs got started in the last 2 hours although activated jobs had been there).

   * Zero Share, which is defined in the ``fairsharepolicy`` field in CRIC. For example *type=evgensimul:100%*,
     in this case, only evgen or simul jobs can be assigned as others have zero shares.

   * If the task ``ioIntensity`` is larger than ``IO_INTENSITY_CUTOFF`` (defined in :doc:`gdpconfig </advanced/gdpconfig>`),
     the total size of missing files must be less than ``SIZE_CUTOFF_TO_MOVE_INPUT`` (defined in :doc:`gdpconfig </advanced/gdpconfig>`)
     and the number of missing files must be less than ``NUM_CUTOFF_TO_MOVE_INPUT`` (defined in :doc:`gdpconfig </advanced/gdpconfig>`).
     I.e., if a queue needs to transfer more input files, the queue is skipped.

   * There is a general ``MAX_DISKIO_DEFAULT`` limit in :doc:`gdpconfig </advanced/gdpconfig>`.
     It is possible to overwrite the limit for a particular queue through the ``maxDiskIO`` (in kB/sec per core)
     field in CRIC. The limit is applied in job brokerage: when the average diskIO per core for running jobs in
     a queue exceeds the limit, the next cycles of job brokerage will exclude tasks with ``diskIO`` higher than
     the defined limit to progressively get the diskIO under the threshold.

   * CPU Core count matching.

   * Availability of ATLAS release/cache. This check is skipped when queues have *ANY* in the ``releases`` filed in CRIC.
     If queues have *AUTO* in the ``releases`` filed, the brokerage uses the information published in a json by CRIC as
     explained at :ref:`this section <ref_auto_check>`.

   * Queues publish maximum (and minimum) memory size per core. The expected memory site of each job is estimated
     for each queue as

     .. math::

        (baseRamCount + ramCount \times coreCount) \times compensation

     where *compensation* is 0.9, avoiding sending jobs to high-memory queues when their expected memory usage is
     close to the lower limit. Queues are skipped if the estimated memory usage is not included in the acceptable
     memory ranges.

   * Skip queues if they don't support direct access to read input files from the local storage, although the task is
     configured to use only direct access.

   * The disk usage for a job is estimated as

     .. math::

        inputDiskCount + max (0.5 GB, outDiskCount \times nEvents) + workDiskCount

     where *inputDiskCount* is the total size of job input files, a discrete function of *nEvents*,
     and *nEvents* is the smalles1t number allowed based on the task requirements. *inputDiskCount* is zero
     if the queues are configured to read input files directly from the local storage. ``maxwdir`` is divided by
     *coreCount* at each queue and the resultant value must be larger than the expected disk usage.

   * DISK size check, free space in the local storage has to be over 200GB.

   * Skip blacklisted storage endpoints.

   * If scout or merge jobs, skip queues if their ``maxtime`` is less than 24 hours.

   * The estimated walltime for a job is

     .. math::

        \frac {cpuTime \times nEvents} {C \times P \times cpuEfficiency} + baseTime

     *nEvents* is the same as the one used to estimate the disk usage. The estimated walltime must be less than
     ``maxtime`` of the queue.

   * ``wnconnectivity`` of the queue must be consistent if the task specifies ``ipConnectivity``.

   * Settings for event service and the dynamic number of events.

   * Too many transferring jobs: skip if transferring > max(transferring_limit, 2 x running), where transferring_limit limit is defined by site or 2000 if undefined.

   * Use only the queues associated with the nucleus if the task sets ``t1Weight=-1`` and normal jobs are being generated.

   * Skip queues without pilots for the last 3 hours.

   * If processingType=*urgent* or priority :raw-html:`&GreaterEqual;` 1000, the :ref:`Network weight <ref_network_weight>`
     must be larger than or equal to ``NW_THRESHOLD`` :raw-html:`&times;` ``NW_WEIGHT_MULTIPLIER``
     (both defined in :doc:`gdpconfig </advanced/gdpconfig>`).

#. Calculate brokerage weight for remaining candidates.
   The initial weight is based on running vs queued jobs.
   The brokerage uses the largest one as the number of running jobs among the following numbers:

   * The actual number of running jobs at the queue, *R*\ :sub:`real`.

   * min(*nBatchJob*, 20) if *R*\ :sub:`real` < 20 and *nBatchJob* (the number of running+submitted
     batch workers at PQ) > *R*\ :sub:`real`. Mainly for bootstrap.

   * *numSlots* if it is set to a positive number for the queue to the `proactive job assignment <https://github.com/HSF/harvester/wiki/Workflows#proactive-job-assignment>`_.

   * The number of starting jobs if *numSlots* is set to zero, which is typically useful for Harvester to fetch
     jobs when the number of available slots dynamically changes.

   The number of assigned jobs is ignored for the weight calculation and the subsequent filtering if the input for
   the jobs being considered is already
   available locally. Jobs waiting for data transfer do not block new jobs needing no transfer.

   .. math::

     manyAssigned = max(1, min(2, \frac {assigned} {activated}))

   .. math::

     weight = \frac {running + 1} {(activated + assigned + starting + defined + 10) \times manyAssigned}

   Take data availability into consideration.

   .. math::

     weight = weight \times \frac {availableSize + totalSize} {totalSize \times (numMissingFiles / 100 + 1)}

   Apply a :ref:`Network weight <ref_network_weight>` based on connectivity between nucleus and satellite,
   since the output files are aggregated to the nucleus.

   .. math::

     weight = weight \times networkWeight

#. Apply further filters.

   * Skip queues if activated + starting > 2 :raw-html:`&times;` running.

   * Skip queues if defined+activated+assigned+starting > 2 :raw-html:`&times;` running.

#. If all queues are skipped, the task is pending for 1 hour.
   Otherwise, the remaining candidates are sorted by weight, and the best 10 candidates are taken.


.. _ref_auto_check:

Release/cache Availability Check for releases=AUTO
=========================================================
Each queue publishes something like

.. code-block:: python

  "AGLT2": {
    "cmtconfigs": [
      "x86_64-centos7-gcc62-opt",
      "x86_64-centos7-gcc8-opt",
      "x86_64-slc6-gcc49-opt",
      "x86_64-slc6-gcc62-opt",
      "x86_64-slc6-gcc8-opt"
    ],
    "containers": [
      "any",
      "/cvmfs"
    ],
    "cvmfs": [
      "atlas",
      "nightlies"
    ],
    "tags": []
  }

If the task uses a container, i.e., the ``container_name`` attribute is set,


.. _ref_network_weight:

Network weight
==========================
The network data sources are

* the `Network Weather Service <http://atlas-adc-netmetrics-lb.cern.ch/metrics/latest.json>`_ as the dynamic source, and

* the `CRIC closeness <https://atlas-cric.cern.ch/api/core/sitematrix/query/?json&json_pretty=0>`_ as a semi static source.

Given the accuracy of the data and the timelapse from decision to action, the network weight only aims to provide
a simple, dynamic classification of links. It is currently calculated as:

.. math::

  netWorkWeight = 0.5 \times (queuedWeight + throughputWeight)

where the queued and throughput weight are calculated as in the plot below:

.. figure:: images/queued.png
  :align: center

  queuedWeight

.. figure:: images/throughput.png
  :align: center

  throughputWeight

It uses the most recent available data, so preferably data of the last 1 hour, in not available of last 1 day,
if not available of last 1 week. FTS Mbps are used, which are filled from Chicago elastic search.
If there are no available network metrics, the AGIS closeness (0 best to 11 worst) is used in a normalized way

.. math::

  weightNwThroughput = 1+ \frac {MAX\_CLOSENESS - closeness} {MAX\_CLOSENESS - MIN\_CLOSENESS}
