===========================
Job Sizing
===========================

JEDI generates jobs based on the following task parameters:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - nFilesPerJob
     - The number of input files per job
   * - nGBPerJob
     - The total size of input/output files and working directory
   * - nEventsPerJob
     - The number of events per job
   * - cpuTime
     - HS06sec per event
   * - cpuEfficiency
     - CPU efficiency (0.9 by default)
   * - baseTime
     - The part of the job execution time not scaling with CPU power
   * - outDiskCount
     - The expect output size per event
   * - workDiskCount
     - The working directory size

If one of the first three parameters *n\*PerJob* is specified, jobs are generated accordingly.
If some computing resources cannot accept those jobs due to resource limitation, such as
small scratch disks and short walltime, the brokerage avoids those resources.

If they are not specified, jobs are generated to meet the limitation of each computing resource.
The number of events *nEvents* in each job must satisfy the following formulae:

.. math::

   S \geq inputDiskCount + max (0.5 GB, outDiskCount \times nEvents) + workDiskCount

.. math::

   W \geq \frac {cpuTime \times nEvents} {C \times P \times cpuEfficiency} + baseTime

where *S*, *W*, *C*, and *P* are the scratch disk size, the wall time limit, the number of CPU cores,
and the HS06 core-power at the computing resource, respectively.
*inputDiskCount* is the total size of job input files, a discrete function of *nEvents*.
Note that *inputDiskCount* is zero if the computing resource is configured to read input files
directly from the local storage resource.

|br|