====================
PanDA Daemon
====================

PanDA daemon is a sub-component of the PanDA server. Here is the configuration guide.


Configurations
-----------------

Configuration File
^^^^^^^^^^^^^^^^^^^^^^

The configurations of PanDA daemon should be written under ``[daemon]`` section in
``panda_server.cfg``.

Example
^^^^^^^^^^^^^^

The configurations may look like this:

.. code-block:: text

    [daemon]
    # whether to run daemons for PanDA
    enable = True

    # user and group name to run daemons
    uname = atlpan
    gname = zp

    # package path of script modules to run in daemon
    package = pandaserver.daemons.scripts

    # number of worker processes to run daemons
    n_proc = 4

    # when exceeding lifetime, worker process will be respawned
    proc_lifetime = 14400

    # configuration in json about daemons
    # of the form {"daemon_name": {"module": <module_name>, "period": <period>, ...}, ...}
    config = {
        "dummy_test": {
            "enable": true, "period": 120, "timeout": 300},
        "add_main": {
            "enable": true, "period": 240, "loop": true},
        "add_sub": {
            "enable": true, "period": 240},
        "evpPD2P": {
            "enable": true, "period": 600},
        "recover_lost_files_daemon": {
            "enable": true, "period": 600},
        "process_workflow_files_daemon": {
            "enable": true, "period": 60},
        "copyArchive": {
            "enable": true, "period": 2400, "sync": true},
        "datasetManager": {
            "enable": true, "period": 2400, "sync": true},
        "proxyCache": {
            "module": "panda_activeusers_query", "enable": true, "period": 600},
        "pilot_streaming": {
            "module": "pilotStreaming", "enable": true, "period": 300, "sync": true},
        "worker_synchronization": {
            "module": "worker_synchronization", "enable": true, "period": 1800, "sync": true},
        "configurator": {
            "enable": true, "module": "configurator", "period": 200, "sync": true},
        "network_configurator": {
            "enable": true, "module": "configurator", "arguments": ["--network"], "period": 400, "sync": true},
        "schedconfig_json": {
            "enable": true, "module": "configurator", "arguments": ["--json_dump"], "period": 200, "sync": true},
        "sw_tags": {
            "enable": true, "module": "configurator", "arguments": ["--sw_tags"], "period": 200, "sync": true},
        "metric_collector": {
            "enable": true, "period": 300},
        "task_evaluator": {
            "enable": true, "period": 300}
        }



Descriptions of Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``enable``: Whether to enable PanDA daemon. When False, one will fail to start PanDA daemon service . Default is False
* ``uname`` and ``gname``: The user name and group name to run daemon processes with. Default is "nobody" for both
* ``package``: The path of python package which contains the daemon scripts. Mandatory, while the existing scripts are put under "pandaserver.daemons.scripts" in PanDA code
* ``n_proc``: Number of worker processes to run daemons. Default is 1
* ``proc_lifetime``: Lifetime of worker processes in seconds to run daemons. When a worker process is found expired, it will terminate and PanDA Daemon will spawn a new worker. Meant to neutralize memory leak or corruptions by daemon scripts. Default is 28800 seconds, i.e. 6 hours
* ``config``: Configurations about the daemons in JSON format. Mandatory. More details below


Descriptions of ``config``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Written as an object in JSON format.

Each element in the main object defines a daemon, as a key-value pair in form of ``"<daemon_name>": {...(daemon config)...}`` , where

* ``"<daemon_name>"``: The name of the daemon. Can be an arbitrary string

* daemon config: A json object to set attributes of the daemon. Possible attributes are:

   * ``"enable"``: Whether to run this daemon. Useful when one wants to temporary disable the daemon without removing its configuration. Default
   * ``"period"``: The time period in second in which the daemon runs. This attribute is mandatory. (Note that if the run duration of a daemon script is longer than its period configured, PanDA daemon will not start to run the same script until the existing one finishes. In this case, the actual period in real world is longer than the period configured, and warning message is thrown out)
   * ``"timeout"``: Timeout in second of which the daemon runs. When a daemon worker running the daemon script exceeds ``timeout``, the worker process will be killed (with SIGKILL) and a new worker will be launched. This prevents PanDA daemon from hanging. If omitted, its value will be ``min(period*3, period + 3600)`` by default
   * ``"sync"``: Whether to synchronize among all PanDA servers. If true, only one PanDA server at a time can run this daemon (implemented with process lock in DB), and the period of the daemon is considered among all PanDA servers (it counts when any one PanDA server runs the script). Default is false
   * ``"loop"``: Loop mode, whether to loop the daemon script. If true, the daemon script will be run in a loop. The loop will keep going if daemon script returns True and will exit if the daemon script returns False. This is useful for the scripts that needs to be run constantly (e.g. add_main, message-consumer like stuff). Note that in loop mode, the loop of script is allowed to run longer than the daemon period configured, and there will be no warning message if the script runs longer than the period. Default is false
   * ``"module"``: The module name (under the package defined in ``package`` above) of the script to run in this daemon. If omitted, its value will be the same as the ``"<daemon_name>"`` by default
   * ``"arguments"``: An json array of additional arguments of the script. For example, if the daemon should run the script as this command: ``run-me.py dump -n 100`` , then in configuration in can be: ``"module": "run-me", "arguments": ["dump", "-n", 100]`` . Default is empty array


-----------

|br|

Service Control
---------------------

One can control PanDA daemon with the ``panda_daemon`` service script:

.. prompt:: bash

  /opt/panda/etc/rc.d/init.d/panda_daemon start
  /opt/panda/etc/rc.d/init.d/panda_daemon stop

which will start/stop PanDA daemon.

Or equivalently, one can control PanDA daemon with the ``httpd-pandasrv`` init.d script, with special argument:

.. prompt:: bash

  /sbin/service httpd-pandasrv start-daemon
  /sbin/service httpd-pandasrv stop-daemon

which will also start/stop PanDA daemon.


Note that, about the ``httpd-pandasrv`` init.d script, the ``start`` and ``stop`` argument:

.. prompt:: bash

  /sbin/service httpd-pandasrv start
  /sbin/service httpd-pandasrv stop

will start/stop **both** PanDA web application **and** PanDA daemon.

------------

|br|

Logs
---------------

Daemon Master process:

.. code-block:: text

  <logdir>/panda_daemon_stdout.log
  <logdir>/panda_daemon_stderr.log

Daemon Worker processes:

.. code-block:: text

  /var/log/panda/panda-daemons.log

------------

|br|

Translation from Crontab to Daemon Configuration
--------------------------------------------------

The script needs to run on every panda server independently
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One can set them to have ``"sync": false`` (or just omit ``sync``), and its period to be the same as the cron period.

E.g. add.py

.. code-block:: text

 0-59/4 * * * * atlpan /opt/panda/usr/bin/panda_server-add > /dev/null 2>&1

It runs every 4 minutes = 240 seconds. Thus, its daemon config can be

.. code-block:: text

  "add": {"period": 240}

The script can run (and had better run) on one panda server at a time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One can set them to have ``"sync": true``.

The period in daemon configuration should be set as the period in which ANY PanDA server run the script.

E.g. copyArchive.py

.. code-block:: text

  5 1-19/6 * * * atlpan /opt/panda/usr/bin/panda_server-copyArchive > /dev/null 2>&1

Note that we set different time offsets in crontab on different PanDA servers to stagger the run of
copyArchive by PanDA servers.

Here, the script runs every 6 hours = 21600 seconds in crontab, on each PanDA server.

Say we have 9 PanDA servers; then on average, the script run in the period of 21600 / 9 = 2400 seconds

Thus, its daemon config can be

.. code-block:: text

  "copyArchive": {"period": 2400, "sync": true}

Exception
^^^^^^^^^^^^^^^^

If the script needs to be run pretty frequently, and does not matter to run by multiple panda servers at a time,
then one may not need the ``sync``.


E.g. pilotStreaming.py

.. code-block:: text

  0-59/5 * * * * atlpan /opt/panda/usr/bin/panda_server-pilot_streaming > /dev/null 2>&1

Here, the script runs every 5 minutes = 300 seconds in crontab, on each PanDA server.

Say we have 9 PanDA servers; then on average, the script run in the period of 300 / 9 = 33 seconds,
which is rather short. It is kinda overkill to have an unnecessary process lock in DB for a time less
than one minute.

Hence we can just the script to run on every panda server independently. Thus, its daemon config can be

.. code-block:: text

  "pilot_streaming": {"module": "pilotStreaming", "period": 300}

|br|
