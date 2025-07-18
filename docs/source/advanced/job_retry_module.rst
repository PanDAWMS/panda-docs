===================================
Job Retry Module
===================================

Jobs can fail for different reasons. The Job Retry Module
greatly simplifies operations by taking actions based on error codes/messages.

Actions
--------
Here is a description of the currently available actions.

+-------------------+-------------------------------------------------------------------------------------------------------------+
| NAME              | DESCRIPTION                                                                                                 |
+===================+=============================================================================================================+
| no_retry          | Do not retry the job again for certain hopeless errors.                                                     |
+-------------------+-------------------------------------------------------------------------------------------------------------+
| limit_retry       | Limit the number of retries to a certain maximum.                                                           |
+-------------------+-------------------------------------------------------------------------------------------------------------+
| increase memory   | Submit next job retries with a higher memory requirement.                                                   |
+-------------------+-------------------------------------------------------------------------------------------------------------+
| increase CPU time | If there are no successful jobs, the retry module will try to set the task CPU time based on the number     |
|                   | of events of the currently failed job and the site parameters (maxtime, HS06) x 1.5. If there               |
|                   | are successful jobs, the retry module will simply request the scouting mechanism to recalculate the CPU     |
|                   | time based on all the jobs in the task.                                                                     |
+-------------------+-------------------------------------------------------------------------------------------------------------+

Retry actions are recorded in the database table ``RETRYACTIONS``. New actions need to be
implemented and then registered in the table.

Rules
--------
Rules are recorded in the database table ``RETRYERRORS``. For new rules you have to specify:
 * ID: unique ID
 * Retry action: which action from the previous section you want to invoke
 * Error source: the source of the error (payload, pilot, job dispatcher, task buffer)
 * Error code
 * Error message: a regular expression in python syntax (https://docs.python.org/3/library/re.html) to match the error message. You can check your regular expressions in online services like https://pythex.org/ if you don't want to write the pythong snippet.
 * Active: you can choose to run the rule in passive mode. In this case there will only be a log message indicating that the rule would have been invoked, but it has no effect. This option is useful when you are not sure of the scope of your new rule.
 * Parameters: valid only for certain actions, such as ``limit_retry``, where you want to specify the limit of retries.
 * Scope: there are a couple of columns (architecture, release, workqueue), where you can limit the scope of the new rule. For example if you want to apply the rule only for a certain software release.


