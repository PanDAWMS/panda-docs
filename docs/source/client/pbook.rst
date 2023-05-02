=========================
Bookkeeping
=========================

.. contents:: Table of Contents
    :local:

-----------

|br|

Introduction
--------------

``pbook`` is the command-line tool for users to manage their analysis, e.g., to check task status,
and finish/kill/retry tasks. ``pbook`` launches an interactive session on the terminal where the user enters
bookkeeping commands such as *show* and *kill*. ``pbook`` can also be executed in batch mode to process a single
command without human intervention.

.. tabs::

   .. tab:: Interactive

      Usage:

      .. prompt:: bash $,>>> auto

         $ pbook [options]
         >>> command(*args, **kwargs)

      E.g

      .. prompt:: bash $,>>> auto

         >>> show(123, format='long', sync=True)


      The interactive session can be terminated by entering Ctrl+D.

      To see the list of commands and help of each command,

      .. prompt:: bash $,>>> auto

         >>> help()
         >>> help(<command_name>)


   .. tab:: Batch

      Usage:

      .. prompt:: bash $,>>> auto

         $ pbook [options] command [arg1 arg2 ... argN] [kwarg1=value1 kwarg2=value2 ... kwargN=valueN]

      E.g

      .. prompt:: bash $,>>> auto

         $ pbook show 123 format='long' sync=True


      If arg or value is a list in interactive mode, it is represented as a comma-separate list in batch mode.
      E.g. to kill three tasks in one go:

      .. prompt:: bash $,>>> auto

         $ pbook kill 123,456,789

      which is equivalent in interactive mode to

      .. prompt:: bash $,>>> auto

         $ pbook
         >>> kill([123, 456, 789])

      To see the list of commands and help of each command,

      .. prompt:: bash $,>>> auto

         $ pbook help
         $ pbook help <command_name>


      Note that pbook skips sanity checks like the credential validation check to get rid of execution overhead,
      when it is executed in batch mode. You need to generate a credential by yourself if necessary:

      .. prompt:: bash $,>>> auto

         $ pbook generate_credential


------------

|br|

Misc commands
------------------

Show all commands
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   In interactive mode:
   >>> help()

   In batch mode:
   $ pbook help


See help of each command
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> help(<command_name>)
   >>> help(show)

        Print task records. The first argument (non-keyword) can be an jediTaskID or reqID, or 'run' (show active tasks only), or 'fin' (show terminated tasks only), or can be omitted. The following keyword arguments are available in the way of panda monitor url query: [username, limit, taskname, days, jeditaskid].
        If sync=True, it forces panda monitor to get the latest records rather than get from cache.
        Specify display format with format='xxx', available formats are ['standard', 'long', 'json', 'plain'].
        The default filter conditions are: username=(name from user voms proxy), limit=1000, days=14, sync=False, format='standard'.

        example:
        >>> show()
        >>> show(123)
        >>> show(12345678, format='long')
        >>> show(taskname='my_task_name')
        >>> show('run')
        >>> show('fin', days=7, limit=100)
        >>> show(format='json', sync=True)

   $ pbook help <command_name>
   $ pbook help show


|br|

Task bookkeeping
------------------

Kill tasks
^^^^^^^^^^^^^

.. code-block:: bash

   >>> kill(arg)

   $ pbook kill arg

This command can take a jediTaskID, a list of jediTaskIDs, or 'all' as the input argument.
If it is 'all', it kills all active tasks of the user.

Finish tasks
^^^^^^^^^^^^^

.. code-block:: bash

   >>> finish(arg, soft=False)

   $ pbook finish arg
   $ pbook finish arg soft=True

This command enforces running tasks to finish immediately.
The arg is a jediTaskID, a list of jediTaskIDs, or 'all'. If ``soft`` is set to True,
the system doesn't generate new jobs but waits until all existing jobs are done.

Retry tasks
^^^^^^^^^^^^

.. code-block:: bash

   >>> retry(arg, newOpts=None)

   $ pbook retry arg
   $ pbook retry arg key1=value1 ... keyN=valueN

This command is used to retry only failed PanDA jobs in a `finished` task.
The arg is a jediTaskID or a list of jediTaskIDs.
It is possible to specify ``newOpts``, which is None by default and can be a map of options and new arguments like
*{'nFilesPerJob': 10,'excludedSite': 'ABC,XYZ'}* to overwrite task parameters.
If values of some arguments are *None*, corresponding task parameters are removed. For example,
*{'nFilesPerJob': None,'excludedSite': None}* will remove --nFilesPerJob and --excludedSite so that
jobs will be generated and assigned without those constraints.
For batch mode, *key1=value1 ... keyN=valueN* are internally converted to a dictionary
*{key1: value1, ..., key2: valueN}* that is given to ``newOpts``.

Show all own tasks
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> show()

    $ pbook show

By default, it shows only tasks submitted within last 14 days and at most 1000 tasks.
One can specify ``days`` and ``limit`` keyword arguments to show more (or less) tasks.

Show one or more tasks with JediTaskIDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> show(arg)

    $ pbook show arg

The arg can be a jediTaskID or a list of jediTaskIDs.
Note that it is possible to use ReqID instead of jediTaskID, however, mixture of JediTaskID and ReqID doesn't work.


Show in long detailed format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> showl()

    $ pbook showl

which is a wrapper of show(format='long').

Show tasks matching certain filters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> show(username='Hage Chabin', limit=7, days=30)

    $ pbook show username='Hage Chabin' limit=7 days=30

which shows at most 7 tasks submitted by Hage Chabin for last 30 days.

Show tasks in other format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> show(format='plain')

   $ pbook show format='plain'

where available formats are 'standard', 'long', 'json', 'plain'.

|br|

----------

Workflow bookkeeping
-------------------------

All workflow bookkeeping commands take the request ID of the workflow as the argument.

Show status of a workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> show_workflow(request_id)

   $ pbook show_workflow request_id

This command shows the workflow status of interest.


Finish a workflow
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> finish_workflow(request_id)

   $ pbook finish_workflow request_id

This command enforces to finish all active tasks in the workflow.


Kill a workflow
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> kill_workflow(request_id)

   $ pbook kill_workflow request_id

This command kills all active tasks in the workflow.


Retry a workflow
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> retry_workflow(request_id)

   $ pbook retry_workflow request_id

This command retries tasks unsuccessful in the previous attempt and activate subsequent tasks if necessary.


Pause a workflow
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> pause_workflow(request_id)

   $ pbook pause_workflow request_id

This command pauses all active tasks in the workflow.


Resume a workflow
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> resume_workflow(request_id)

   $ pbook resume_workflow request_id

This command resume paused tasks in the workflow.

-----

|br|

Trouble shooting
-----------------
``pbook`` goes into the verbose mode to show shows what's exactly going on when being launched with ``-v`` option.

.. prompt:: bash

 prun -v ...

which would give clues if there are problems.
