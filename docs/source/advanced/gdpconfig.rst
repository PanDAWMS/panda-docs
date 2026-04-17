=================================================
System Configuration Parameters in Database
=================================================

There is the ``PANDA.CONFIG`` table, so-called :blue:`gdpconfig` table in the database where you can define
any configuration parameter
shared by all PanDA applications, so that system admins don't have to tweak the static cfg files every time
they optimize the system.

The table has the following columns:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - APP
     - The application name which uses the parameter
   * - COMPONENT
     - The component name which uses the parameter
   * - KEY
     - The parameter name
   * - VALUE
     - The parameter value
   * - TYPE
     - The parameter type
   * - VO
     - The organization name which defines the parameter
   * - DESCR
     - Description of the parameter

Applications get those parameters through the ``pandaserver.taskbuffer.TaskBuffer`` module.

.. code-block:: python

  from pandaserver.taskbuffer.TaskBuffer import taskBuffer
  p = taskBuffer.getConfigValue(COMPONENT, KEY, APP, VO)

The method returns None if the parameter is undefined.

|br|

Parameter List
--------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Key
     - Description
   * - ANALY_TIMEOUT[_<project>]
     - Timeout value for analysis rebrokerage in hours. A project-specific override can be set via ``ANALY_TIMEOUT_<project>`` (e.g. ``ANALY_TIMEOUT_proj-evind``)
   * - BASE_DEFAULT_QUEUE_LENGTH_PER_PQ_USER
     - Base minimal number of queued jobs per PQ per user (nQ(PQ, user))
   * - BASE_EXPECTED_WAIT_HOUR_ON_PQ
     - If the expected wait time to digest all queued jobs on the PQ is shorter than this value (hours), analysis throttle will skip the PQ
   * - BASE_QUEUE_LENGTH_PER_PQ
     - If the number of queued jobs on the PQ is lower than this value, analysis throttle will skip the PQ
   * - BASE_QUEUE_RATIO_ON_PQ
     - Base minimal ratio of nQ(PQ, user)/nR(PQ): queued jobs of one user on a PQ divided by all running jobs on the PQ under the same prodsourcelabel
   * - BUILD_JOB_MAX_WALLTIME
     - Max walltime for build jobs in hours
   * - CAP_RUNNING_GROUP_CORES
     - Cap on running cores per group
   * - CAP_RUNNING_GROUP_JOBS
     - Cap on running jobs per group
   * - CAP_RUNNING_USER_CORES
     - Cap on running cores per user
   * - CAP_RUNNING_USER_JOBS
     - Cap on running jobs per user
   * - DATA_CAROUSEL_CONFIG
     - Configuration of Data Carousel in JSON format
   * - DATA_CHECK_TIMEOUT_USER
     - Time limit in hours after which analysis brokerage allows input transfer
   * - DATA_LOCATION_CHECK_PERIOD
     - Time limit for the task brokerage to skip data locality check
   * - DISK_THRESHOLD[_<gshare>]
     - Disk size threshold in TB to skip the nucleus when available space minus reserved space is insufficient. A gshare-specific override can be set via ``DISK_THRESHOLD_<gshare>`` (e.g. ``DISK_THRESHOLD_MC 16 simul``)
   * - EVP_DATASET_LIFETIME
     - Lifetime of temporary datasets for event picking
   * - FAST_REBRO_THRESHOLD_NQNR_RATIO
     - Threshold on nQ_pq(gshare)/nR_pq(gshare) ratio to trigger fast rebrokerage at the PQ
   * - FAST_REBRO_THRESHOLD_NQUEUE_FRAC
     - Threshold on fraction of nQ_pq(gshare)/nQ_total(gshare) to trigger fast rebrokerage at the PQ
   * - FAST_REBRO_THRESHOLD_NQUEUE_<gshare>
     - Min nQ_pq to trigger fast rebrokerage at the PQ for the given gshare (e.g. ``FAST_REBRO_THRESHOLD_NQUEUE_MC 16 simul``)
   * - FREE_DISK_CUTOFF
     - Maximum free disk space value in TB factored into the weight calculation
   * - GROUPBYATTR_<activity>
     - Attribute to group tasks when generating jobs for the given activity (e.g. ``GROUPBYATTR_Analysis``, ``GROUPBYATTR_User Analysis``)
   * - HEARTBEAT_TIMEOUT_<workflow>
     - Heartbeat timeout for the given workflow in hours (e.g. ``HEARTBEAT_TIMEOUT_analysis``, ``HEARTBEAT_TIMEOUT_production``, ``HEARTBEAT_TIMEOUT_push_noheartbeat``)
   * - IGNORE_MEANRSS
     - Flag to indicate whether to ignore mean RSS throttling in job dispatcher and pilot streaming
   * - INPUT_NUM_FRACTION
     - Minimum percentage of available files in the input dataset which allows the task to go to the nucleus
   * - INPUT_NUM_THRESHOLD
     - Minimum number of files in the input dataset to enable data availability check
   * - INPUT_SIZE_FRACTION
     - Minimum percentage of available file size in the input dataset which allows the task to go to the nucleus
   * - INPUT_SIZE_THRESHOLD
     - Minimum size of input dataset in GB to enable data availability check
   * - IO_INTENSITY_CUTOFF
     - Brokerage IO intensity cutoff in kB/sec to prevent input transfers for heavy jobs
   * - IO_INTENSITY_CUTOFF_USER
     - Analysis brokerage IO intensity cutoff in kB/sec to allow input transfers for light-weight jobs
   * - JOB_MAX_ATTEMPT_user
     - Max number of attempts for a job. Tasks cannot be retried if some jobs exceed the limit. 0 to disable
   * - JOB_SUBMISSION
     - Enable/disable job submission in JEDI
   * - JUMBO_MAX_CURR_PRIO
     - Max priority of tasks which can enable jumbo jobs
   * - JUMBO_MAX_EVENTS
     - Total number of events in tasks with jumbo jobs
   * - JUMBO_MAX_FILES_TO_BOOST
     - Max number of remaining files in tasks with jumbo jobs when priorities are boosted
   * - JUMBO_MAX_TASKS
     - Max number of tasks with jumbo jobs
   * - JUMBO_MIN_EVENTS_DISABLE
     - Min number of events in a task to disable jumbo jobs
   * - JUMBO_MIN_EVENTS_ENABLE
     - Min number of events in a task to enable jumbo jobs
   * - JUMBO_PER_SITE
     - Number of jumbo jobs per task per site
   * - JUMBO_PER_TASK
     - Number of jumbo jobs per task
   * - JUMBO_PROG_TO_BOOST
     - Percentage of events processed in tasks with jumbo jobs when priorities are boosted
   * - LIMIT_IOINTENSITY_managed
     - For prodSourceLabel=managed, only tasks with ioIntensity higher than this value will be considered
   * - LIMIT_PRIORITY_managed
     - For prodSourceLabel=managed, only tasks with currentPriority lower than this value will be considered
   * - MAX_ACTIVE_TASKS_PER_USER_user
     - Max number of active user tasks per user
   * - MAX_DISKIO_DEFAULT
     - Max average DiskIO limit per core in kB/sec
   * - MAX_EXPECTED_WAIT_HOUR
     - Max allowed expected wait time (hours) of queued jobs on one PQ per user, before excluding the PQ in brokerage
   * - MAX_FAILED_HEP_SCORE_HOURS_user
     - Max HEP score hours used by failed jobs. Tasks go to exhausted if a retry is requested and the limit has been reached. 0 to disable
   * - MAX_FAILED_HEP_SCORE_RATE_TO_PAUSE_managed
     - Max acceptable HEP score rate of failed jobs within a managed task, triggering an automatic pause when reached. 0 to disable
   * - MAX_FAILED_HEP_SCORE_RATE_user
     - Max rate of failed/total HEP score. Tasks go to exhausted if further reattempts are requested and the limit is reached. 0 to disable
   * - MAX_JOB_FAILURE_RATE_TO_PAUSE_managed
     - Max acceptable job failure rate within a managed task, triggering an automatic pause when reached. 0 to disable
   * - MAX_JOB_FAILURE_RATE_user
     - Max single job failure rate. Tasks go to exhausted if a retry is requested and the limit has been reached. 0 to disable
   * - MAX_MISSING_INPUT_FILES
     - The brokerage sends the task to pending if, at all online storage endpoints, the number of missing files exceeds this value and the ratio of available files drops below MIN_INPUT_COMPLETENESS
   * - MAX_PREASSIGNED_TASKS_managed
     - Max number of production tasks to preassign to an empty queue per resource type
   * - MAX_PRIO_TO_BOOTSTRAP
     - Max currentpriority of tasks used to bootstrap PQs where no jobs are running or queued
   * - MAX_TASK_PRIO_WITH_LOCAL_DATA
     - Maximum task priority to assign the task only to a nucleus which has the input data locally
   * - MERGE_JOB_MAX_WALLTIME_user
     - Max walltime for user merge jobs in hours
   * - MIN_BAD_JOBS_TO_SKIP_PQ
     - Skip PQs if the total number of failed or closed jobs is larger than this value
   * - MIN_CPU_EFFICIENCY_user
     - Minimum average CPU efficiency (%) across finished jobs in a task. User tasks go to exhausted upon retry if the average falls below the limit
   * - MIN_FILES_READY_managed
     - Min number of ready files a task must have to be eligible for preassignment
   * - MIN_FILES_REMAINING_managed
     - Min number of remaining files a task must have to be eligible for preassignment
   * - MIN_INPUT_COMPLETENESS
     - The brokerage sends the task to pending if, at all online storage endpoints, the number of missing files exceeds MAX_MISSING_INPUT_FILES and the ratio of available files drops below this percentage
   * - MIN_INPUT_SIZE_WITH_LOCAL_DATA
     - Minimum input data size in GB to assign the task only to a nucleus which has the input data locally
   * - MIN_IO_INTENSITY_WITH_LOCAL_DATA
     - Minimum IO intensity in kBPerS to assign the task only to a nucleus which has the input data locally
   * - MIN_JOBS_TO_PAUSE_managed
     - Minimum total number of jobs within a managed task required to trigger an automatic pause when the failure rate reaches the limit
   * - MIN_REMAINING_JOBS_TO_PAUSE_managed
     - Minimum number of remaining jobs within a managed task required to trigger an automatic pause when the failure rate reaches the limit
   * - MIN_WEIGHT_<activity>
     - Minimum brokerage weight for tasks of the given activity (``MIN_WEIGHT_managed``, ``MIN_WEIGHT_user``)
   * - NFILES_<gshare>
     - Number of files to generate jobs for the given gshare in one cycle (e.g. ``NFILES_Data Derivations``)
   * - NQUEUECAP_<gshare>
     - Maximum number of queued jobs for the given gshare (e.g. ``NQUEUECAP_Frontier``)
   * - NQUEUED_NUC_CAP
     - Cap on the aggregated number of files to the nucleus
   * - NQUEUED_NUC_CAP_FOR_JOBS
     - Cap in the job brokerage on the aggregated number of files being transferred to the nucleus
   * - NQUEUED_SAT_CAP
     - Cap on the number of files queued from satellite to nucleus
   * - NQUEUELIMIT_<gshare>
     - Minimum number of queued jobs for the given gshare or resource label. Use ``-GSHARE-`` keys for gshare-based limits (e.g. ``NQUEUELIMIT_MC 16``) and ``-RESOURCE-`` keys for resource-based limits (e.g. ``NQUEUELIMIT_eventservice``)
   * - NQUEUELIMITSITE_<activity>
     - Min number of jobs to assign to a PQ in the brokerage when the number of running jobs is small at the PQ, for the given activity (e.g. ``NQUEUELIMITSITE_MC merge``)
   * - NRUNNINGCAP_<gshare>
     - Maximum number of running jobs for the given gshare. Optionally scoped to core type via ``_MCORE*`` or ``_SCORE*`` suffix (e.g. ``NRUNNINGCAP_Frontier_MCORE*``)
   * - NTASKS_<gshare>
     - Number of tasks to generate jobs for the given gshare in one cycle (e.g. ``NTASKS_Group production``)
   * - NUM_CUTOFF_TO_MOVE_INPUT
     - Cutoff on the number of missing input files to move for IO intensive tasks
   * - NW_ACTIVE
     - Activate the network weights in job brokerage
   * - OUTDISKCOUNT_ANALY_KB
     - Default outdiskcount for analysis jobs in kB
   * - OVERLOAD_MIN_QUEUE
     - Minimum number of queued jobs to skip overloaded PQs
   * - OVERLOAD_RATIO_OFFSET
     - Offset for nQ/nR ratio to skip overloaded PQs
   * - PENDING_TIMEOUT_user
     - Timeout value for pending tasks in hours
   * - PROD_TASKS_PUSH_STATUS_CHANGES_PERCENT
     - Percentage of production tasks which enable push messages of status changes
   * - RAM_THR_EXAUSTED
     - Threshold for ramcount/core. Tasks are set to exhausted when their actual ramcount/core is larger than the threshold and preset ramcount/core is less than the threshold
   * - SCOUT_CHANGE_SR_user
     - Allow scouts to change splitRule for user tasks
   * - SCOUT_CPUTIME_RANK
     - Percentile rank for cpuTime calculation based on scouts
   * - SCOUT_DISK_IO_CAP
     - Cap on disk IO in kBPerS measured by scout jobs
   * - SCOUT_LOW_CPU_EFFICIENCY_user
     - Upper limit on CPU efficiencies of inefficient scout jobs for analysis (in %)
   * - SCOUT_MAX_IO_INTENSITY_FOR_EXHAUSTED_user
     - Max IO intensity above which scout jobs are exempt from being sent to exhausted for analysis
   * - SCOUT_MEM_LEAK_PER_CORE_<activity>
     - Maximum acceptable memory leak in kB/s for the given activity (``SCOUT_MEM_LEAK_PER_CORE_managed``, ``SCOUT_MEM_LEAK_PER_CORE_user``)
   * - SCOUT_MIN_OK_RATE_EXHAUSTED_user
     - Min scout success rate to send tasks to exhausted. Tasks below the threshold go to broken
   * - SCOUT_NUM_CPU_INEFFICIENT_user
     - Max number of acceptable CPU-inefficient scout jobs for analysis
   * - SCOUT_NUM_SHORT_user
     - Max number of acceptable short scout jobs for analysis
   * - SCOUT_RAMCOUNT_MARGIN
     - Safety margin in % for ramCount calculation based on scouts
   * - SCOUT_RAMCOUNT_MIN
     - Minimum value of RAM count set by scouts
   * - SCOUT_RAMCOUNT_RANK
     - Percentile rank for ramCount calculation based on scouts
   * - SCOUT_SHORT_EXECTIME_user
     - Upper limit on execution time of short scout jobs for analysis (in minutes)
   * - SCOUT_THR_CPU_INEFFICIENT_user
     - Cutoff on the expected number of jobs to send analysis tasks to exhausted based on CPU-inefficient scout jobs
   * - SCOUT_THR_SHORT_user
     - Cutoff on the expected number of jobs to send analysis tasks to exhausted based on short scout jobs
   * - SCOUT_WRONG_CPUTIME_THRESHOLD
     - Tasks go to exhausted when actual cpuTime is larger than this threshold times the original cpuTime. 0 to disable
   * - SIZE_CUTOFF_TO_MOVE_INPUT
     - Cutoff on the total size (GB) of missing input files to move for IO intensive tasks
   * - SLOPPY_DISPATCH_RATIO
     - Ratio (%) of jobs to dispatch without considering gshare
   * - STATIC_MAX_QUEUE_RUNNING_RATIO
     - Static max allowed nQ(PQ, user)/nR(PQ, user) ratio per user per PQ, before excluding the PQ in brokerage
   * - SUPER_HIGH_PRIO_TASK_RATIO
     - Percentage of super high priority tasks to generate jobs in a single job generation cycle
   * - TASK_MAX_ATTEMPT_user
     - Max number of attempts for a task. Tasks go to exhausted if a retry is requested and the number of attempts has reached the limit
   * - TEST_JSON_INTERFACE
     - Not used; present to test the JSON interface
   * - THROTTLE_THRESHOLD
     - Throttle threshold on Nqueue/Nrunning for job generation
   * - THROTTLE_THRESHOLD_FOR_WORK_SHORTAGE
     - Throttle threshold on Nqueue/Nrunning for job generation in case of work shortage
   * - TIMEOUT_defined
     - Timeout value for defined jobs in hours
   * - TIMEOUT_holding
     - Timeout value for holding jobs in hours
   * - TW_DONE_JOB_STAT
     - Finished/failed/closed jobs in the last N hours are considered in the analysis job brokerage decision
   * - TYPNFILES_<activity>__<type>
     - Typical number of input files per job of the given type for the given activity (e.g. ``TYPNFILES_managed__archive``)
   * - USER_JOB_PRIO_BOOST_DICTS
     - JSON-serialized list of ``{"name": Name, "type": Type(user or group), "prio": Priority, "expire": ExpirationDate(YYYYMMDD or null)}`` defining users/groups that get a job priority boost
   * - USER_JOB_TARGET_WALLTIME
     - Target walltime of user jobs in hours
   * - USER_PRESTAGE_LIMIT
     - Max amount of data in GB to read from TAPE per user
   * - USER_TASKS_MAX_CORE_COUNT
     - Maximum number of CPU cores per job that a single user task is allowed to utilize
   * - USER_TASKS_MESSAGE_DRIVEN_PERCENT
     - Percentage of user tasks which enable message-driven mode
   * - USER_TASKS_MOVE_INPUT
     - Percentage of user tasks which enable data motion for input
   * - USER_TASKS_PUSH_STATUS_CHANGES_PERCENT
     - Percentage of user tasks which enable push messages of status changes
   * - USER_TRANSFER_LIMIT
     - Max amount of transferring input data in GB per user
   * - USER_USAGE_THRESHOLD_A
     - Threshold of user running slots in hi-sites for their tasks to stay in class A
   * - USER_USAGE_THRESHOLD_B
     - Threshold of user running slots in hi and mid-sites for their tasks to stay in class B
   * - WORK_SHORTAGE
     - Set to True when there is insufficient work available and jobs should be assigned exclusively to pledged resources

|br|