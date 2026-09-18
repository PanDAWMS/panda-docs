===================================
Harvester Admin Tool
===================================

Harvester Admin Tool is available since Harvester version 0.0.20, which provides the command for harvester administrative operations.


.. contents:: Table of Contents
    :local:
    :depth: 2


Setup
-----

After installation of Harvester, under ``{harvester_venv}/local/bin/`` there is a script template harvester-admin.rpmnew.template . Copy it to be **harvester-admin** and modify it: Set the ``userName`` and ``VIRTUAL_ENV`` according to the user to run the admin tool and the harvester venv respectively. E.g. when venv directory is /opt/harvester :

.. code-block:: text

    # cp /opt/harvester/local/bin/harvester-admin.rpmnew.template /opt/harvester/local/bin/harvester-admin
    # vim /opt/harvester/local/bin/harvester-admin


One may also want to make **harvester-admin** a default command (rather than executable file) in the shell by modifying ``$PATH`` .


Usage
-----

Run **harvester-admin** . Option ``-h`` after any command/sub-command provides help message. Some examples below.


Show help
""""""""""

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin -h
    usage: harvester-admin [-h] [-v] {test,get,fifo,cacher,qconf,kill,query} ...

    positional arguments:
      {test,get,fifo,cacher,qconf,kill,query}
        test                for testing only
        get                 get attributes of this harvester
        fifo                fifo related
        cacher              cacher related
        qconf               queue configuration
        kill                kill something alive
        query               query current status about harvester

    options:
      -h, --help            show this help message and exit
      -v, --verbose, --debug
                            Print more verbose output. (Debug mode !)


Admin tool test
""""""""""""""""

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin -v test
    [2019-10-04 00:17:03,197 CRITICAL] Harvester Admin Tool: test CRITICAL
    [2019-10-04 00:17:03,198 ERROR] Harvester Admin Tool: test ERROR
    [2019-10-04 00:17:03,198 WARNING] Harvester Admin Tool: test WARNING
    [2019-10-04 00:17:03,198 INFO] Harvester Admin Tool: test INFO
    [2019-10-04 00:17:03,198 DEBUG] Harvester Admin Tool: test DEBUG
    Harvester Admin Tool: test
    [2019-10-04 00:17:03,198 DEBUG] ARGS: Namespace(debug=True, which='test') ; RESULT: None 
    [2019-10-04 00:17:03,198 DEBUG] Action completed in 0.001 seconds


Show help of qconf (queue configuration) sub-command
""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin qconf -h
    usage: harvester-admin qconf [-h] {list,dump,refresh,purge} ...

    positional arguments:
      {list,dump,refresh,purge}
        list                List queues. Only active queues listed by default
        dump                Dump queue configurations
        refresh             refresh queue configuration immediately
        purge               Purge the queue thoroughly from harvester DB (Be
                            careful !!)

    options:
      -h, --help            show this help message and exit


List all queue configurations in harvester
""""""""""""""""""""""""""""""""""""""""""

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin qconf list -a
    configID : queue name
    --------- ------------
       44795 : pic-htcondor_UCORE
       44796 : NIKHEF-ELPROD_MCORE
    ...
       44974 : INFN-T1_UCORE


Without ``-a`` the command lists the names of the active queues only.


Dump queue configurations
""""""""""""""""""""""""""

``qconf dump`` prints the resolved configuration of queues. One can give one or more queue names, ``-a`` for all active queues, or ``-i`` with one or more configIDs. With ``-J`` the result is printed as JSON instead of the plain text representation.

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin qconf dump -h
    usage: harvester-admin qconf dump [-h] [-J] [-a] [-i <configID> [<configID> ...]]
                                      [<queue_name> ...]

    positional arguments:
      <queue_name>          Name of active queue; not needed with -a or -i

    options:
      -h, --help            show this help message and exit
      -J, --json            Dump configuration in JSON format
      -a, --all             Dump configuration of all active queues
      -i, --id <configID> [<configID> ...]
                            Dump configuration of queue with configID


E.g. dump the configuration of two queues in JSON:

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin qconf dump -J CERN-PROD_UCORE_2 LRZ-LMU_TEST


Note that if no queue is given and neither ``-a`` nor ``-i`` is set, the command errors out instead of dumping everything.


Refresh queue configurations
""""""""""""""""""""""""""""

``qconf refresh`` makes harvester reload the queue configuration immediately, rather than waiting for the next automatic reload. With ``-R`` (``--refill``) the pq_table in the DB is refilled before the refresh, which is cleaner but heavier.

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin qconf refresh -R


|br|

Other commands
--------------

Get attributes of the harvester instance
""""""""""""""""""""""""""""""""""""""""

``get`` prints one attribute of this harvester instance. The available attributes are ``harvesterID``, ``version``, ``commit_info`` and ``harvester_config`` (the latter is printed as JSON).

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin get harvesterID
    CERN_central_B


Cacher
""""""

``cacher refresh`` triggers the cacher to update all its cached information (e.g. the CRIC information) immediately, instead of waiting for the next cacher cycle.

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin cacher refresh


FIFO
""""

``fifo repopulate`` repopulates the fifo of an agent from the DB; currently only the ``monitor`` fifo is supported, and ``ALL`` repopulates every supported fifo. ``fifo benchmark`` measures the performance of the fifo backend (``-n`` for the number of objects, ``-t`` for the number of threads).

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin fifo repopulate monitor
    Repopulated monitor fifo

    # /opt/harvester/local/bin/harvester-admin fifo benchmark -n 500 -t 4


|br|

PanDA Queue management
----------------------


Offline a PQ from harvester
""""""""""""""""""""""""""""

If one just wants the harvester not to submit more workers of the PQ, as temporary manual offline, it suffices to add the following line in the object of the PQ in harvester local queue configuration file. E.g.

.. code-block:: text

    "CERN-EXTENSION_GOOGLE_HARVESTER": {
        "queueStatus": "OFFLINE",
        ...
    }


Remove a PQ from harvester
""""""""""""""""""""""""""

If one wants to remove the PQ completely from harvester (e.g. the PQ is renamed or no longer used), then:

0. Be sure that one really does not need anything jobs/workers/configs of the PQ any longer.
1. Modify the pilot_manager to be "local" of the PQ on AGIS and/or make sure harvester does not grab information about this PQ from AGIS anymore.
2. Remove all lines of the PQ in harvester local queue configuration file.
3. Run qconf purge with harvester admin tool in order to delete all records of this PQ in DB. E.g.:
    .. code-block:: text

        # harvester-admin qconf purge UKI-LT2-IC-HEP_SL6
        Purged UKI-LT2-IC-HEP_SL6 from harvester DB


KaBOOM!

|br|

Worker management
-----------------


Kill workers in a queue or a CE
""""""""""""""""""""""""""""""""

Sometimes one finds plenty of queuing workers submitted to a certain dead CE, preventing more jobs to get activated/submitted to the whole queue. Or may be a queue is totally blocked due to site issue and all workers already submitted to the site will never run.

In such cases, on the harvester instance one can manually kill workers which block the queue -- harvester admin tool allows one to kill workers filtered by worker status, queue (site), CE, and submissionhost (e.g. condor schedd).

E.g. Kill all submitted (queuing) workers submitted to CE "ce13.pic.es:9619" and CE "ce14.pic.es:9619" of site "pic-htcondor_UCORE":

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin kill workers --sites pic-htcondor_UCORE --ces ce13.pic.es:9619 ce14.pic.es:9619  --submissionhosts ALL
    Sweeper will soon kill 7 workers, with status in ['submitted'], computingSite in ['pic-htcondor_UCORE'], computingElement in ['ce13.pic.es:9619', 'ce14.pic.es:9619'], submissionHost in ALL


E.g. Kill all submitted and idle workers submitted via submissionhost "aipanda183.cern.ch,aipanda183.cern.ch:19618" (full submissionhost name of aipanda183 condor schedd) to the CE "ce13.pic.es:9619" (say, condor GAHP processes to some CE are down on a certain schedd):

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin kill workers --status submitted idle --sites ALL --ces ALL --submissionhosts aipanda183.cern.ch,aipanda183.cern.ch:19618
    Sweeper will soon kill 7 workers, with status in ['submitted', 'idle'], computingSite in ALL, computingElement in ['ce13.pic.es:9619'], submissionHost in ['aipanda183.cern.ch,aipanda183.cern.ch:19618']


Rules of command ``harvester-admin kill workers``:

    * Available filter flags are ``--status``, ``--sites``, ``--ces``, ``--submissionhosts``
    * After the filter flags there can be one of the following: a single argument (workers matching the argument), multiple arguments separated by space (workers matching any of these arguments), or the keyword ``ALL`` (no constraint on this flag)
    * ``--sites``, ``--ces``, ``--submissionhosts`` are mandatory. One MUST specify them to be valid argument(s), or ``ALL``
    * ``--status`` is optional. Available status arguments are ``submitted``, ``idle``, ``running``, and their combination, or ``ALL`` for no constraint on status.
      If ``--status`` is omitted, its value is ``submitted`` by default.
    * All workers which match the conditions of all filter flags will be killed by sweeper agent soon (next cycle).
    * Workers already in a final status (``finished``, ``failed``, ``cancelled``) are never killed, even if they match the filters. The number printed is the number of workers actually marked to kill.

_Note: For grid, the feature will be implemented on BigPanDA webpage as well for easier manual operation. Furthermore, in the future the monitoring system will automatically spot dead CEs and kill blocked workers._


|br|

Get statistics of a PQ
----------------------

Harvester admin tool provides ``query workers`` and ``query jobs`` commands to get the number of workers/jobs of the PQs specified, broken down by job type (prodsourcelabel), resource type (SCORE, MCORE, ...), and worker/job status.

One can give one or more queue names, or ``-a`` (``--all``) for all queues. The results are printed as a table by default; with ``-J`` (``--json``) they are printed as JSON instead.

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin query workers -h
    usage: harvester-admin query workers [-h] [-a] [-J] [<queue_name> ...]

    positional arguments:
      <queue_name>  Name of active queue; not needed with -a

    options:
      -h, --help    show this help message and exit
      -a, --all     Show results of all queues
      -J, --json    Show results in JSON format


Note that job stats are available for only PUSH PQs (mapType != NoJob).

In the tables, the rows with ``_total`` in a column are the sums over that column: e.g. the row with jobType ``_total`` and resourceType ``SCORE`` is the number of SCORE workers of all job types, and the row with ``_total`` in both is the total of the PQ.


Worker statistics
"""""""""""""""""

For example, the worker stats of CERN-PROD_UCORE_2 :

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin query workers CERN-PROD_UCORE_2
    +-------------------+---------+--------------+-----------+-----------+---------+----------+--------+-----------+
    | computingSite     | jobType | resourceType | to_submit | submitted | running | finished | failed | cancelled |
    +==============================================================================================================+
    | CERN-PROD_UCORE_2 | managed | MCORE        |         0 |         3 |      10 |       50 |      2 |         0 |
    | CERN-PROD_UCORE_2 | managed | SCORE        |         1 |         2 |       5 |       33 |      0 |        24 |
    | CERN-PROD_UCORE_2 | managed | _total       |         1 |         5 |      15 |       83 |      2 |        24 |
    | CERN-PROD_UCORE_2 | user    | SCORE        |         0 |         1 |       4 |       12 |      0 |         0 |
    | CERN-PROD_UCORE_2 | user    | _total       |         0 |         1 |       4 |       12 |      0 |         0 |
    | CERN-PROD_UCORE_2 | _total  | MCORE        |         0 |         3 |      10 |       50 |      2 |         0 |
    | CERN-PROD_UCORE_2 | _total  | SCORE        |         1 |         3 |       9 |       45 |      0 |        24 |
    | CERN-PROD_UCORE_2 | _total  | _total       |         1 |         6 |      19 |       95 |      2 |        24 |
    +-------------------+---------+--------------+-----------+-----------+---------+----------+--------+-----------+


The status columns follow the life cycle of a worker (``to_submit``, ``ready``, ``submitted``, ``idle``, ``pending``, ``running``, ``finished``, ``failed``, ``cancelled``, ``missed``); only the statuses which actually occur in the result are shown.


Job statistics
""""""""""""""

And the job stats of a PUSH PQ, with the numbers of jobs and of cores in each status:

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin query jobs LRZ-LMU_TEST
    +---------------+--------------+--------+----------+---------+
    | computingSite | resourceType | metric | starting | running |
    +============================================================+
    | LRZ-LMU_TEST  | MCORE        | jobs   |        1 |       5 |
    | LRZ-LMU_TEST  | MCORE        | cores  |        8 |      40 |
    | LRZ-LMU_TEST  | SCORE        | jobs   |        3 |      12 |
    | LRZ-LMU_TEST  | SCORE        | cores  |        3 |      12 |
    | LRZ-LMU_TEST  | _total       | jobs   |        4 |      17 |
    | LRZ-LMU_TEST  | _total       | cores  |       11 |      52 |
    +---------------+--------------+--------+----------+---------+


If the query matches nothing (e.g. ``query jobs`` on a PULL PQ), the table is printed as:

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin query jobs CERN-PROD_UCORE_2
    (no entry)


JSON output
"""""""""""

With ``-J`` the same information is printed as JSON, which is handy for scripting:

.. code-block:: text

    # /opt/harvester/local/bin/harvester-admin query jobs -J LRZ-LMU_TEST
    {
        "LRZ-LMU_TEST": {
            "MCORE": {
                "cores": {
                    "running": 40,
                    "starting": 8
                },
                "jobs": {
                    "running": 5,
                    "starting": 1
                }
            },
            "SCORE": {
                "cores": {
                    "running": 12,
                    "starting": 3
                },
                "jobs": {
                    "running": 12,
                    "starting": 3
                }
            },
            "_total": {
                "cores": {
                    "running": 52,
                    "starting": 11
                },
                "jobs": {
                    "running": 17,
                    "starting": 4
                }
            }
        }
    }
