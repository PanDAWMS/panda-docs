===================================
FIFO
===================================

FIFO in harvester is an optional feature that harvester agents can take advantage of messaging mechanism. 
Main purpose of FIFO is to reduce DB polling frequency and lower CPU usage of the node.

The FIFO has "Priority Queue" data structure.
Different plugins can be chosen as fifo backend. Existing plugins: SQLite and MariaDB/MySQL

So far, only monitor agent has option to enable FIFO. 

.. contents:: Table of Contents
    :local:
    :depth: 2


================================================================


Configuration FIFO backend
--------------------------

Choose a FIFO backend (SQLite or MariaDB/MySQL) and set up related service. 
Then configure in harvester.


SQLite
""""""

Backend setup\:
    * Make sure sqlite3 is installed in OS
    * No special service configuration required

Harvester configuration\:
    * In Harvester local configuration file ``[fifo]`` section, one should set ``fifoModule = pandaharvester.harvesterfifo.sqlite_fifo`` and ``fifoClass = SqliteFifo`` to use the `SqliteFifo` fifo plugin.
    * The ``database_filename`` should be specified as the database filename for sqlite. This must be different from main Harvester DB and other fifo DBs if using sqlite.
    * It is recommended to use placeholder ``$(AGENT)`` in filename to make different DBs for fifo of different agents.
    * One can set DB file located in ramdisk for better performance.
    * E.g.

        .. code-block:: text

            [fifo]
            fifoModule = pandaharvester.harvesterfifo.sqlite_fifo
            fifoClass = SqliteFifo
            database_filename = /dev/shm/$(AGENT)_fifo.db


MariaDB/MySQL
"""""""""""""

Note\:
    * One can use the same MariaDB/MySQL DB server of Harvester DB for FIFO backend (and create a schema dedicate to FIFO), but this is reasonable if and only if the Harvester DB is shared across multiple Harvester nodes (thus FIFO should be shared as well).

Backend setup\:
    * An empty database schema must created and grated to specific db user beforehand.
    * Make sure harvester node has rw access as the db user to a database of MariaDB/MySQL.

Harvester configuration\:
    * In Harvester local configuration file ``[fifo]`` section, one should set ``fifoModule = pandaharvester.harvesterfifo.mysql_fifo`` and ``fifoClass = MysqlFifo`` to use the `MysqlFifo` fifo plugin.
    * The ``db_host``, ``db_port``, ``db_user``, ``db_password``, ``db_schema`` should be specified properly to access backend DB. This can (and had better) be different from main Harvester DB and other fifo DBs if using MariaDB/MySQL.
    * E.g. (Say a database named **HARVESTER_FIFO** was created and granted to db user **harvester_fifo** in advance)

        .. code-block:: text

            [fifo]

            fifoModule = pandaharvester.harvesterfifo.mysql_fifo
            fifoClass = MysqlFifo

            # database attributes for MySQL
            db_host = db-server@cern.ch
            db_port = 12345
            db_user = harvester_fifo
            db_password = paswordforfifo
            db_schema = HARVESTER_FIFO



Configure Monitor FIFO
-----------------------


Worker chunks with shorter fifoCheckInterval has higher priority and will be checked more frequently.

Here it shows the steps to configure and enable FIFO in for harvester monitor agent.

To enable monitor FIFO, at least `fifoEnable = True` and `fifoCheckInterval` line need to be added in monitor section of harvester.cfg .

Besides, it is reasonable to adjust some existing variables in monitor section. Typically when monitor fifo is enabled, one may want to decrease the frequency of worker check in DB cycles (because almost all checks can now be done in fifo cycles) via increasing `sleepTime` (and maybe `checkInterval` as well).

A minimal configuration may look like this\:

.. code-block:: text

    [monitor]

    nThreads = 3
    maxWorkers = 500
    lockInterval = 600
    checkInterval = 900
    sleepTime = 1800
    checkTimeout = 3600
    
    fifoEnable = True
    fifoCheckInterval = 300


Repopulate monitor fifo
""""""""""""""""""""""""

The monitor FIFO is empty (or not existing) when being set up for the first time or reset (say, sqlite db in ramdisk after node reboot). To let monitor agent utilize the monitor fifo, one needs to (re)populate monitor fifo (with active worker chunks).

[Harvester Admin Tool](https://github.com/HSF/harvester/wiki/Admin-FAQ#harvester-admin-tool) allows one to do this in one line:

.. code-block:: text

    # harvester-admin fifo repopulate monitor
    Repopulated monitor fifo


N.B.\:
    * This operation removes everything from monitor FIFO first, and then populates it with active worker chunks queried from Harvester DB. It may take some time (several minutes) if one has many (say 100k) worker records in Harvester DB.
    * It is recommended to repopulate monitor fifo when harvester service stops; i.e. when the FIFO is not accessed by other processes. And restart harvester service afterwards.  (Though it is possible to repopulate monitor fifo when harvester service running)


================================================================

Setup monitor plugin cache with FIFO
------------------------------------

Some monitor plugins (e.g. htcondor_monitor) have cache functionality utilizing Harvester FIFO.

To enable and configure it, modify pluginCache* in [monitor] section in harvester.cfg . E.g.\:

.. code-block:: text

    [monitor]

    # plugin cache parameters (used if monitor plugin supports)
    pluginCacheEnable = True
    pluginCacheRefreshInterval = 300



Setup monitor event-based check mechanism
-----------------------------------------

Beside periodic polling the resource for status update all workers, now monitor agent can also check only partial workers at a time where the monitor agent gets the workers' update "event". 
(Note here the "event" means an update event of the worker, including batch status change etc. so it can be checked; **nothing to do with** PanDA job events.)

Note the monitor event-based check mechanism has to run with monitor fifo mechanism enabled.


Requirements on monitor plugin
""""""""""""""""""""""""""""""

To run harvester monitor agent with event-based check mechanism, the monitor plugin needs to have the method `report_updated_workers` which reports the workers just updated and their update timestamp (Check DummyMonitor for details of this method).

Note that the method should report the `workerID` (NOT `batchID` !!) of the workers. Thus, it is the batch/resource-facing system that has the responsibility to record the workerID in the batch jobs, which the monitor plugin can access.

Harvester monitor agent calls `report_updated_workers` of the plugin periodically to get all newly updated workers in one go.

For example, htcondor_monitor plugin has this feature.

Harvester configuration
""""""""""""""""""""""""

In Harvester local configuration file ``[monitor]`` section, one needs to have ``fifoEnable`` and ``eventBasedEnable`` to be ``True``, and specify which plugin(s) in ``eventBasedPlugins`` in json format (array of objects).

Besides, specify the parameters: ``eventBasedCheckInterval``, ``eventBasedTimeWindow``, ``eventBasedCheckMaxEvents``, ``eventBasedEventLifetime``, ``eventBasedRemoveMaxEvents``.

A complete configuration of monitor section may look like: 

.. code-block:: text

    [monitor]
    nThreads = 6 
    maxWorkers = 750
    lockInterval = 300
    checkInterval = 3600
    sleepTime = 2400
    workerQueueTimeLimit = 172800

    fifoEnable = True
    fifoSleepTimeMilli = 5000
    fifoCheckInterval = 1800
    fifoCheckDuration = 15
    checkTimeout = 3600
    #fifoMaxWorkersToPopulate = 10000
    fifoMaxWorkersPerChunk = 500
    fifoForceEnqueueInterval = 10800
    fifoMaxPreemptInterval = 60

    pluginCacheEnable = True
    pluginCacheRefreshInterval = 300

    eventBasedEnable = True
    eventBasedPlugins = 
    [
        {
        "module": "pandaharvester.harvestermonitor.htcondor_monitor",
        "name": "HTCondorMonitor",
        "condorHostConfig_list": [
            "/opt/harvester/etc/panda/condor_host_config.json"
            ]
        }
    ]
    eventBasedCheckInterval = 300
    eventBasedTimeWindow = 450
    eventBasedCheckMaxEvents = 500
    eventBasedEventLifetime = 1800
    eventBasedRemoveMaxEvents = 2000



================================================================

Benchmark FIFO
--------------

It is possible to benchmark the FIFO backend to understand its performance.

Harvester Admin Tool (link) provides a FIFO benchmark command. For example\:

.. code-block:: text

    # harvester-admin fifo benchmark -n 500
    Start fifo benchmark ...
    Cleared fifo
    Put 500 objects by 1 threads : took 0.624 sec
    Now fifo size is 500
    Get 500 objects by 1 threads : took 0.719 sec
    Now fifo size is 0
    Put 500 objects by 1 threads : took 0.557 sec
    Now fifo size is 500
    Get 500 objects protective dequeue by 1 threads : took 0.755 sec
    Now fifo size is 500
    Put 500 objects by 1 threads : took 0.545 sec
    Now fifo size is 1000
    Cleared fifo : took 0.008 sec
    Now fifo size is 0
    Finished fifo benchmark
    Summary:
    FIFO plugin is: MysqlFifo
    Benchmark with 500 objects by 1 threads
    Put            : 1.151 ms / obj
    Get            : 1.438 ms / obj
    Get protective : 1.510 ms / obj
    Clear          : 0.015 ms / obj

where one can specify the number of objects to benchmark with ``-n`` option.

Note the benchmark is undergone on a separate table from those used by Harvester agent fifos (e.g. monitor fifo) so that the data will not mix.
However, it is better to run benchmark when Harvester service is stopped.
