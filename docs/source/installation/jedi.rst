=================
JEDI
=================

Here is the setup guide of JEDI.

.. note::

  This is a complete guide. It is recommended to have a look at :doc:`Quick Admin Tutorial </admin_guide/admin_guide>`
  beforehand.

Software requirements
------------------------
JEDI requires:

* CentOS 7 or similar Linux distribution
* python :raw-html:`&GreaterEqual;` 3.6
* pip

Dependent python packages are automatically installed by pip.

---------

|br|

Installation
----------------
Setup a virtual environment first.

.. prompt:: bash

  python3 -m venv <install dir>
  . <install dir>/bin/activate

Then

.. prompt:: bash

 pip install panda-jedi

which will install panda-jedi and dependent python packages in addition to
panda-server since JEDI runs on PanDA server's modules.

If the latest panda-jedi in the git master repository is required,

.. prompt:: bash

 pip install git+https://github.com/PanDAWMS/panda-jedi.git

-------------

|br|

Configuration
-----------------


There are two configuration files under ``${VIRTUAL_ENV}/etc/panda``.

panda_common.cfg
=====================

See :ref:`installation/server:panda_common.cfg`


panda_jedi.cfg
=====================

This configuration file sets various JEDI parameters.

.. prompt:: bash

 cd ${VIRTUAL_ENV}/etc/panda
 mv panda_jedi.cfg.rpmnew panda_jedi.cfg

* Global Parameters

    The following parameters need to be modified if any.

    .. list-table:: master parameters
       :header-rows: 1

       * - Name
         - Description
       * - uname
         - The userid under which JEDI runs
       * - gname
         - The group under which JEDI runs

    .. list-table:: database parameters
       :header-rows: 1

       * - Name
         - Description
       * - dbhost
         - The database hostname
       * - dbuser
         - The database username
       * - dbpasswd
         - The database password

* Agent Parameters

    As explained in :doc:`JEDI architecture page </architecture/jedi>`,
    JEDI agents/components have plugin structure.
    They need to be configured in the following sections in ``panda_jedi.cfg``:

    ddm
        The component to access the data management system

    confeeder
        Contents Feeder

    taskrefine
        Task Refine

    jobbroker
        Job Brokerage

    jobthrottle
        The component to throttle job submission

    jobgen
        Job Generator

    postprocessor
        Post Processor

    watchdog
        Watch Dog

    taskbroker
        Task Brokerage

    tcommando
        Task Commando

    msgprocessor
        Message Processor


    Most of them have two parameters, ``modConfig`` and ``procConfig``. For example,

    .. code-block:: text

      modConfig = wlcg:managed|test:pandajedi.jedidog.ProdWatchDog:ProdWatchDog

      procConfig = wlcg:managed|test:2

    The first parameter ``modConfig`` defines what module and class is used for each virtual organization and activity.
    The syntax is ``organization:activity:module_import_path:class_name<, ...>``,
    where the first field specifies the organization name, the second field specifies the activity name,
    the third field specifies the import path of the module, and the last field specifies the class name.
    The organization and activity fields can be empty if it work regardless of organization or activity.
    The activity field can also take a string concatenating activity names with ``|`` if it works
    for multiple activities.

    The second parameter in the above config example ``procConfig`` defines the number of processes for each organization
    and activity. The syntax is ``experiment:activity:n_processes<, ...>``,
    where the first field specifies the organization name, the second field specifies the activity name,
    and the third field specifies the number of processes.
    The experiment and activity fields are similar to that of ``modConfig``.
    If activity names are concatenated in the activity field those activities share the same processes.

    Parameters of Message Processor are described in :doc:`/advanced/msg_processor`.


------------

|br|

System Setup
-------------------
Then you need to register JEDI as a system service, make some directories, and setup log rotation if any.
Check contents in ``/etc/sysconfig/panda_server`` and ``/etc/sysconfig/panda_jedi`` just in case.

.. prompt:: bash

 # register the PanDA server
 ln -fs ${VIRTUAL_ENV}/etc/panda/panda_server.sysconfig /etc/sysconfig/panda_server
 ln -fs ${VIRTUAL_ENV}/etc/panda/panda_jedi.sysconfig /etc/sysconfig/panda_jedi
 ln -fs ${VIRTUAL_ENV}/etc/init.d/panda_jedi /etc/rc.d/init.d/panda_jedi
 /sbin/chkconfig --add panda_jedi
 /sbin/chkconfig panda_jedi on

 # make dirs
 mkdir -p <logdir in panda_common.cfg>
 chown -R <userid in panda_jedi.cfg>:<group in panda_jedi.cfg> <logdir in panda_common.cfg>

 # setup log rotation if necessary
 ln -fs ${VIRTUAL_ENV}/etc/panda/panda_jedi.logrotate /etc/logrotate.d/panda_jedi

--------------

|br|

Service Control
----------------------------------

.. prompt:: bash

 # start
 /sbin/service panda_jedi start

 # stop
 /sbin/service panda_jedi stop

There should be log files in ``logdir``.
If it doesn't get started there could be clues in ``panda_jedi_stdout.log`` and ``panda_jedi_stderr.log``.

|br|
