========================
Partitioning
========================

Whenever possible, old temporary entries are deleted through a sliding window procedure. However for many tables
the information is preferred to be kept over extended periods of time (years) in order to be able to browse the
data in the monitoring. This leads to very large databases with many million rows. In addition to the usage of
several indexes, Oracle partitioning is also used to optimize data access. Below are the current partitioning
strategies and how new partitions are added (automatically, in a procedure or manually).

- ATLAS_PANDA

+----------------------------+------------------+---------+------------------------+
| Table                      | Partitioned by   | Range   | Handled                |
+============================+==================+=========+========================+
| Datasets                   | modificationtime | 1 month | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Filestable4                | modificationtime | 1 day   | **ADD_DAILYPART** proc |
+----------------------------+------------------+---------+------------------------+
| Harvester_dialogs          | creationtime     | 1 day   | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Harvester_metrics          | creation_time    | 1 day   | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Harvester_rel_jobs_workers | pandaid          | 1E8     | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Harvester_workers          | lastupdate       | 1 month | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Jedi_datasets              | Jeditaskid       | 500k    | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Jedi_dataset_contents      | Jeditaskid       | 500k    | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Jedi_events                | Jeditaskid       | 500k    | **MANUAL**             |
+----------------------------+------------------+---------+------------------------+
| Jedi_jobparams_template    | Ins_UTC_TSTAMP   | 1 day   | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Jedi_output_template       | Jeditaskid       | 500k    | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Jedi_taskparams            | Jeditaskid       | 500k    | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| Jedi_tasks                 | Jeditaskid       | 500k    | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| JOBPARAMSTABLE             | MODIFICATIONTIME | 1 day   | **ADD_DAILYPART** proc |
+----------------------------+------------------+---------+------------------------+
| JOBSARCHIVED4              | MODIFICATIONTIME | 1 day   | **ADD_DAILYPART** proc |
+----------------------------+------------------+---------+------------------------+
| JOBS_STATUSLOG             | MODIFICATIONTIME | 1 day   | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| METATABLE                  | MODIFICATIONTIME | 1 day   | **ADD_DAILYPART** proc |
+----------------------------+------------------+---------+------------------------+
| PANDALOG                   | BINTIME          | 1 day   | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| PANDALOG_FAX               | BINTIME          | 1 month | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| TABLEPART4COPYING          | COPIED_TO_ARCH   | values  | STATIC                 |
+----------------------------+------------------+---------+------------------------+
| TASKS_STATUSLOG            | MODIFICATIONTIME | 1 day   | AUTO                   |
+----------------------------+------------------+---------+------------------------+
| TASKS_STATUSLOG            | MODIFICATIONTIME | 1 day   | AUTO                   |
+----------------------------+------------------+---------+------------------------+

- ATLAS_PANDAARCH

+----------------------------+------------------+---------+------------------------+
| Table                      | Partitioned by   | Range   | Handled                |
+============================+==================+=========+========================+
| FILESTABLE_ARCH            | MODIFICATIONTIME | 1 month | **MANUAL**             |
+----------------------------+------------------+---------+------------------------+
| JOBPARAMSTABLE_ARCH        | MODIFICATIONTIME | 1 month | **MANUAL**             |
+----------------------------+------------------+---------+------------------------+
| JOBSARCHIVED               | MODIFICATIONTIME | 3 days  | **MANUAL**             |
+----------------------------+------------------+---------+------------------------+
| METATABLE_ARCH             | MODIFICATIONTIME | 1 month | **MANUAL**             |
+----------------------------+------------------+---------+------------------------+