==============================
Site & Task Classification
==============================

Site & task classification is made to provide information for the purpose of improving analysis user experience.

Site & task classification-related metrics are updated periodically (by default, 5 ~ 10 minutes) by the following PanDA daemons: **metric_collector** and **task_evaluator**


|br|

Site Classification
-------------------

Site classification considers mainly wait-time of analysis jobs in sites


Definitions
''''''''''''

* Historical data: For a given site (or say, PanDA queue, PQ) that runs analysis, metric collector fetches 4 days of the **pmerge** and **HammerCloud** User Analysis finished jobs (in jobsArchived4 table) in the PQ. The reason for fetching pmerge and HammerCloud jobs is that they are usually given the highest priority values in the PQ; i.e. they have the shortest wait-time in the PQ. Also they usually have short run-time; thus they are less dependent on payload run-time

* Current data: For a given site (or say, PanDA queue, PQ) that runs analysis, metric collector fetches all current **pmerge** User Analysis **waiting** (status in activated or starting) jobs (in jobsArchived4 table) in the PQ. The reason for fetching pmerge jobs is that they have the highest priority values in the PQ (higher than HammerCloud jobs); i.e. they have the shortest wait-time in the PQ.

* **Sample weight** for historical data: When computing statistical metrics below, more recent jobs (according to startTime) are given higher sample weight. The weight decays and halves every 6 hours; i.e. the relation between the weight and age of the job is:

.. math::

  weight = 0.5^{({age}/\text{6 hours})}

* **w_mean** (weighted mean of wait-time): Computed by historical data with sample weight of a site. It is the mean value of wait-time of sample jobs in historical data

* **w_cl95upp** (weighted upper CL95 of wait-time): Computed by historical data with sample weight of a site. Its value is evaluated with the percent point function of Student-t distribution at upper limit = 0.95 about wait-time of sample jobs in historical data. It means statistically, at 95% chance wait-time of a job in this site is shorter than w_cl95upp

* **long_q_n** (number of long-queuing jobs): Computed by current data of a site. It is the number of current queuing pmerge jobs that have queuing time (now - creationtime) > w_mean

* **long_q_mean** (mean wait-time of long-queuing jobs): Computed by current data of a site. It is the mean value of wait-time of long-queuing pmerge jobs, which are counted in long_q_n



Algorithms
''''''''''''
Three classes of sites about appropriateness to run analysis:

* **hi-sites** (high appropriateness): fast sites, satisfying ALL of conditions below

  * max(w_cl95upp, long_q_mean) < max(1 hour, 33th-percentile of w_cl95upp among all sites)
  * long_q_n < 3
  * at least one analysis job (not just pmerge) has got running in last 24 hours

* **lo-sites** (low appropriateness): slow or spiky sites, satisfying ANY of conditions below

  * max(w_cl95upp, long_q_mean) > max(3 hour, 67th-percentile of w_cl95upp among all sites)

* **mid-sites** (medium appropriateness): anything else



|br|

Task Classification
-------------------


Task classification considers task completion progress and user current usage.

Definitions
''''''''''''

* Two **thresholds** gdpconfig: ``USER_USAGE_THRESHOLD_A`` and ``USER_USAGE_THRESHOLD_B``
* **Completion Progress** of a task: calculated as n_finished_input_files/n_total_input_files


Algorithms
''''''''''''

* **S-class**: User Analysis tasks with completion progress >= 90% . Besides, these tasks will be moved to Express Analysis share by analysis watchdog
* **A-class**: User Analysis tasks that user of them has running slots in hi-sites <= ``USER_USAGE_THRESHOLD_A``
* **B-class**: User Analysis tasks that user of them has running slots in hi-sites > ``USER_USAGE_THRESHOLD_A`` and running slots in hi-sites and mid-sites <= ``USER_USAGE_THRESHOLD_B``
* **C-class**: User Analysis tasks that user of them has running slots in hi-sites and mid-sites > ``USER_USAGE_THRESHOLD_B``


|br|
