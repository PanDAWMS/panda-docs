==========================================================
Dynamic Optimization of Task Parameters
==========================================================

JEDI automatically optimizes task parameters for compute/storage resource requirements
and strategies to partition workload while running those tasks. In the early stage of
the task execution, JEDI generates several jobs for each task using only a small portion of input data,
collects various metrics such as data processing rate and memory footprints, and adjusts the following task parameters.
Those first jobs are called scout jobs. The automatic optimization is triggered twice for each task;
1) when half of the scout jobs finish, and 2) when the first 100 jobs finish after the task avalanches.
Some task parameters specify the resource amount per event. If input data don't have event information,
the number of events in each file is internally regarded as 1.


cpuTime
-----------
``cpuTime`` is calculated for each job using the following formula:

.. math::

 cpuTime = \frac {max(0, endTime-startTime-baseTime) \times corePower \times coreCount \times cpuEfficiency \times 1.5}{nEvents}

where *corePower* is the HS06 core-power at the compute resource, *cpuEfficiency* is a task parameter representing
CPU efficiency and defaults to 90%,
*coreCount* is the number of CPU cores that the job used, *baseTime* is another task parameter representing
the part of the job not scaling with CPU power, such as initialization and finalization steps, and *nEvents* is
the number of events processed in the job.
The 95th percentile of ``cpuTime`` of scout jobs

* with *nEvents* :raw-html:`&GreaterEqual;` 10 :raw-html:`&times;` *coreCount*, or

* with fewer *nEvents* but *endTime*-*startTime* :raw-html:`&GreaterEqual;` 6h

is used as a task parameter to estimate the expected execution time for
remaining jobs.
Other scout jobs with fewer events and short execution time are ignored since they tend to skew the estimation.

``cpuTimeUnit`` is a task parameter for the unit of ``cpuTime`` and is one of HS06sPerEvent,
mHS06sPerEvent, HS06sPerEventFixed,
mHS06sPerEventFixed. The *m* prefix means that the ``cpuTime`` value is in milliseconds.
If the *Fixed* suffix is used, scout jobs don't overwrite the preset ``cpuTime`` value.

Tasks can set *cpuEfficiency* to 0 to disable scaling with the number of events.


ramCount
------------------
The pilot monitors the memory usage of the job and reports the information to the PanDA server.
``ramCount`` is calculated for each job using the following formula:

.. math::

  ramCount = frac{maxPSS-baseRamCount}{coreCount}

It is the RSS per core, allowing some offset (*baseRamCount*) independent of core count (*coreCount*).
*baseRamCount* is a preset task parameter ad is not very important for single-core tasks.
The 75th percentile of ``ramCount`` of scout jobs
is used as a task parameter to estimate the expected memory usage for
remaining jobs.

``ramCountUnit`` is a task parameter for the unit of ``ramCount`` and is either MBPerCore or MBPerCoreFixed.
If the latter,
scout jobs don't overwrite the preset value.


outDiskCount and workDiskCount
----------------------------------
The 75th percentile of the total output size per event of scout jobs ``outDiskCount``
is used to estimate the output size of
remaining jobs. Scout jobs with less than ten events are ignored.

The pilot reports the total size of the working directory ``workDiskCount`` while the job is running.
The maximum value of ``workDiskCount`` of scout jobs is used to estimate the expected scratch disk usage of
the remaining jobs.
Note that scout jobs don't overwrite the preset ``workDisCount`` value when the measured value is smaller.


ioIntensity
---------------------------
``ioIntensity`` is the total size of job input and output divided by the job execution time which
roughly corresponds to the data traffics over the wide-area network. The maximum value of ``ioIntensity`` is
used in the job brokerage to avoid redundant heavy data motion over WAN.


diskIO
----------------
The pilot reports the data size the job read and wrote from and to the local disk storage.
``diskIO`` is the total size of job input and output divided by the job execution time, roughly corresponding to
the data traffics over the local-area network. The maximum value of ``diskIO`` is
used in the job brokerage to distribute IO-intensive workloads over many disk storages.


nGBPerJob
------------------
JEDI generates jobs so that the expected disk usage of those jobs is less than ``nGBPerJob`` if this task
parameter is specified.
The parameter is adjusted based on ``outDiskCount`` and ``workDiskCout`` optimized by scout jobs,
if the task sets the target size of the output size ``tgtMaxOutputForNG``.

taskStatus=exhausted
-----------------------
The task status is set to **exhausted** when scouts detect

* huge memory leaks,

* too many jobs with short execution time,

* the calculated ``ramCount`` or ``cpuTime`` so different from preset values,

* very low CPU efficiency, or

* non-allocated CPUs being abused

to ask for user's actions since they indicate those tasks are wrongly configured.

|br|