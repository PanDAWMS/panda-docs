=========================
Bookkeeping
=========================

``pbook`` is the command-line tool for users to manage their analysis, e.g., to check task status,
and finish/kill/retry tasks. ``pbook`` launches an interactive session on the terminal where the user enters
bookkeeping commands such as *show* and *kill*.

.. prompt:: bash

 pbook

The interactive session can be terminated by entering Ctrl+D.

|br|

Usage
-------

Show all commands
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> help()


See help of each command
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

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


Kill tasks
^^^^^^^^^^^^^

.. code-block:: bash

   >>> kill(arg)

This command can take a jediTaskID, a list of jediTaskIDs, or 'all' as the input argument.
If it is 'all', it kills all active tasks of the user.

Finish tasks
^^^^^^^^^^^^^

.. code-block:: bash

   >>> finish(arg, soft=False)

This command enforces running tasks to finish immediately.
The arg is a jediTaskID, a list of jediTaskIDs, or 'all'. If ``soft`` is set to True,
the system doesn't generate new jobs but waits until all existing jobs are done.

Retry tasks
^^^^^^^^^^^^

.. code-block:: bash

   >>> retry(arg, newOpts=None)

This command is used to retry only failed PanDA jobs in finished task.
The arg is a jediTaskID, a list of jediTaskIDs.
It is possible to specify ``newOpts``, which is None by default and can be a map of options and new arguments like
*{'nFilesPerJob':10,'excludedSite':'ABC,XYZ'}* to overwrite task parameters.

Show all own tasks
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> show()

By default, it shows only tasks submitted within last 14 days and at most 1000 tasks.
One can specify ``days`` and ``limit`` keyword arguments to show more (or less) tasks.

Show one or more tasks with JediTaskIDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> show(arg)

The arg can be a jediTaskID or a list of jediTaskIDs.
Note that it is possible to use ReqID instead of jediTaskID, however, mixture of JediTaskID and ReqID doesn't work.


Show in long detailed format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> showl()

which is a wrapper of show(format='long').

Show tasks matching certain filters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    >>> show(username='XYZ', limit=7, days=30)

which shows at most 7 tasks submitted by Max Barends for last 30 days.

Show tasks in other format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   >>> show(format='plain')

where available formats are 'standard', 'long', 'json', 'plain'.
