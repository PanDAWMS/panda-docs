===========================================
Computing Resource Allocations
===========================================

Each organization needs to
allocate the amount of computing resources dedicated to each activity, to
manage CPU resource sharing among various parallel campaigns and to
make sure that results can be delivered in time for important deadlines.
While
dynamic and static shares on batch systems have been around for a long
time, PanDA requires a global solution since it needs to manage shares
among computing resources distributed world-wide while getting rid of local resource
partitioning. The global solution is
not straightforward, given different requirements of the activities (number
of cores, memory, I/O, and CPU intensity), the heterogeneity of
resources (site/HW capabilities, batch configuration, and queue setup) and
constraints on data locality.

`This paper <https://www.epj-conferences.org/articles/epjconf/abs/2019/19/epjconf_chep2018_03025/epjconf_chep2018_03025.html>`_
describes the details.
Briefly, PanDA implements resource allocations as follows:

1. Global Shares definition
-----------------------------
Global Shares establish the amount of resources available instantaneously to a specific activity
as a fraction of the total amount of resources available to the organization.
Global Shares are a nestable structure, where siblings have the preference to occupy
unused shares, before the unused share goes to upper levels.

2. Tagging of tasks and jobs
------------------------------
Tasks and jobs are tagged with a Global Share at creation time.
The tagging is based on a table that defines regular expressions matched against the
most common task and job attributes.

3. Job generation per Global Share
------------------------------------
There are multiple Job Generator agents concurrently running in JEDI. Each agent takes a Global Share
and exclusively locks it while generating jobs for it. I.e., each Global Share generates jobs
in parallel so they don't interfere with each other.

4. Job dispatch respecting Global Share target
---------------------------------------------------
When a slot is freed up at a computing resource and requests a job, the Job Dispatcher component in the PanDA server
decides which of the assigned jobs should run next at the computing resource, respecting Global Share targets.
Job Dispatcher orders the jobs assigned to the computing resource by Global
Share preference (the share furthest away from its target) and priority inside the Global Share.
This assumes a healthy distribution of jobs of different shares across computing resources, avoiding all jobs
of a particular share assigned to few computing resources. It also assumes that there are enough jobs of each
share available for dispatch, so one share can not block another through the job generation
chain.

|br|