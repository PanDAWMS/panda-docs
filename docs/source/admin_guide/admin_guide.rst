===========================
Administrator Guide
===========================

Here is a quick tutorial to setup a minimum PanDA system.


.. contents:: Table of Contents
    :local:
    :depth: 2

|br|

0. Hardware Requirements
--------------------------------------
It is recommended to install JEDI and the PanDA server on separate virtual machines (VMs), but it is possible to
install them on a single VM for small testing purposes. A minimum PanDA system would be composed of 3 VMs;
the first VM for JEDI and the PanDA server, the second VM for Harvester, and the third VM for the PanDA monitor.
The following table shows the minimum hardware configuration.

.. list-table:: Minimum hardware configuration
   :header-rows: 1

   * - Component
     - Cores
     - RAM (GB)
     - Disk (GB)
   * - JEDI + PanDA server
     - 4
     - 8
     - 100
   * - Harvester
     - 4
     - 8
     - 100
   * - BigPandaMon
     - 8
     - 16
     - 70

|br|

1. Database Setup
------------------
The database is the backbone of the PanDA server and JEDI, so it needs to be setup before start
installation of those components. You should go through :doc:`the Database page </database/database>`.

|br|

2. PanDA Server Setup
--------------------------------------
The next step is to install the PanDA server on a VM following :doc:`PanDA server installation guide </installation/server>`.
You need to decide the userid and group under which the PanDA server runs before editing configuration files.
Make sure that the userid and group are consistent in ``panda_server.cfg`` and ``panda_server-httpd.conf``,
the permission of log directories is set accordingly.
It would be good to optimize the number of processes in the httpd.conf based on your VM's configuration,
e.g,

.. code-block:: text

 StartServers         4
 MinSpareServers      4
 ServerLimit          64
 MaxSpareServers      64
 MaxClients           64
 MaxRequestsPerChild  2000

 WSGIDaemonProcess pandasrv_daemon processes=4 threads=1 home=/home/iddssv1 inactivity-timeout=600

Then add a new virtual organization following :ref:`this section <architecture/iam:Adding a new VO to the PanDA server>`.
Make sure that the organization is added to PanDA IAM.
We use the ``wlcg`` organization in this tutorial.
You also need to configure the firewall on the VM to allow access to 25080 and 25443 from outside.

---------

|br|

3. JEDI Setup
--------------------
Once the PanDA server is ready, you can install JEDI on the same VM following :doc:`JEDI installation guide </installation/jedi>`.
You need to use the name of the virtual organization when configuring plugins in ``panda_jedi.cfg``.
For testing purposes it would be enough to use generic plugins as shown below:

.. code-block:: text

 [ddm]
 modConfig = wlcg:1:pandajedi.jediddm.GenDDMClient:GenDDMClient

 [confeeder]
 procConfig = wlcg:any:1

 [taskrefine]
 modConfig = wlcg:any:pandajedi.jedirefine.GenTaskRefiner:GenTaskRefiner
 procConfig = ::1

 [jobbroker]
 modConfig = wlcg:any:pandajedi.jedibrokerage.GenJobBroker:GenJobBroker

 [jobthrottle]
 modConfig = wlcg:any:pandajedi.jedithrottle.GenJobThrottler:GenJobThrottler

 [jobgen]
 procConfig = wlcg:any:1:

 [postprocessor]
 modConfig = wlcg:any:pandajedi.jedipprocess.GenPostProcessor:GenPostProcessor
 procConfig = ::1

 [watchdog]
 modConfig = wlcg:any:pandajedi.jedidog.GenWatchDog:GenWatchDog
 procConfig = wlcg:any:1

 [taskbroker]
 modConfig = wlcg:any:pandajedi.jedibrokerage.GenTaskBroker:GenTaskBroker
 procConfig = wlcg:any:1

 [tcommando]
 procConfig = ::1

 [tasksetup]
 modConfig = wlcg:any:pandajedi.jedisetup.GenTaskSetupper:GenTaskSetupper

-------------

|br|

4. Registration of Resource Groups, Global Shares, and computing resources in the Database
--------------------------------------------------------------------------------------------
You need to manually register VO, global shares, and computing resources unless they are automatically
registered through information system. If you integrate CRIC as explained at
:doc:`CRIC integration guide </advanced/cric>`, you can register them through CRIC.

4.1. Resource Group Registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is possible to define grouping among computing resources but generally it is enough to have one
group for each organization. Groups are registered in the ``CLOUDCONFIG`` table in the PANDAMETA schema
using the following SQL statement.

.. code-block:: sql

  INSERT INTO PANDAMETA.CLOUDCONFIG (NAME,DESCRIPTION,TIER1,TIER1SE,WEIGHT,SERVER,STATUS,
     TRANSTIMELO,TRANSTIMEHI,WAITTIME,SPACE,MODTIME,MCSHARE,NPRESTAGE)
     VALUES('A_GROUP0','some description','NA','NA',0,'NA','online',0,0,0,0,CURRENT_DATE,0,0)

where *NAME* is an arbitrary group name and *STATUS* needs to be set to "online". Replace "PANDAMETA" with your
schema name for the meta tables.

4.2. Global Share Registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each organization defines computing resource allocation among various working groups and/or user activities
using global shares. Normal global shares are registered in the ``GLOBAL_SHARES`` table, while special and/or
resource-specific shares are registered in the ``JEDI_WORK_QUEUE`` table. The following SQL statement
adds a special test share.

.. code-block:: sql

 INSERT INTO PANDA.JEDI_WORK_QUEUE (QUEUE_ID,QUEUE_NAME,QUEUE_TYPE,VO,QUEUE_FUNCTION)
     VALUES(1,'test_queue','test','wlcg','Resource')

where *VO* and *QUEUE_TYPE* are organization and activity names, respectively. Replace "PANDA" with your
schema name for the JEDI tables.

4.3. Computing resource Registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following SQL statement adds a test resource.

.. code-block:: sql

 INSERT INTO PANDAMETA.SCHEDCONFIG (NAME,NICKNAME,SYSTEM,SITE,LASTMOD,NQUEUE,NODES,STATUS,QUEUEHOURS,
     MEMORY,MAXTIME,SPACE,TSPACE) VALUES('TEST_SITE','TEST_SITE','NA','NA',CURRENT_DATE,0,0,'online',
     0,0,0,0,CURRENT_DATE)

where *NAME* and *NICKNAME* are the resource name, and *STATUS* needs to be 'online'.

-----------------

|br|

5. Testing JEDI and the PanDA server
----------------------------------------
At this stage, you can submit a test task to the PanDA server and let JEDI generate jobs.
Before start testing, start the PanDA server and JEDI.

.. prompt:: bash

 /sbin/service httpd-pandasrv start
 /sbin/service panda-jedi start

Then setup panda-client as explained at :doc:`panda-client setup guide </client/panda-client>`.
You need to set *PANDA_URL_SSL* and *PANDA_URL* after sourcing panda_setup.sh, to point to your PanDA server, e.g.,

.. code-block:: text

 export PANDA_URL_SSL=https://ai-idds-01.cern.ch:25443/server/panda
 export PANDA_URL=http://ai-idds-01.cern.ch:25080/server/panda

in addition to the parameters mentioned at :ref:`client setup for OIDC-based auth <architecture/iam:Client setup>`,
e.g.,

.. code-block:: text

 export PANDA_AUTH=oidc
 export PANDA_AUTH_VO=wlcg
 export PANDA_VERIFY_HOST=off

An example of a test task is available
at `this link <https://github.com/PanDAWMS/panda-jedi/blob/master/pandajedi/jeditest/addNonAtlasTask.py>`_.

.. prompt:: bash

  wget https://raw.githubusercontent.com/PanDAWMS/panda-jedi/master/pandajedi/jeditest/addNonAtlasTask.py

In this script

.. code-block:: text

  taskParamMap['vo'] = 'wlcg'
  taskParamMap['prodSourceLabel'] = 'test'
  taskParamMap['site'] = 'TEST_SITE'

they would need to be changed to organization, activity, computing resource names registered in the previous step.
Then

.. prompt:: bash

  python addNonAtlasTask.py

You will see a jediTaskID if successful.

The task is passed to JEDI through the PanDA server, and goes through ``TaskRefiner``, ``ContentsFeeder``,
and ``JobGenerator`` agents in JEDI. Each agent should give logging messages in ``logdir/panda-AgentName.log`` like

.. code-block:: text

  2021-02-24 07:34:13,694 panda.log.TaskRefiner: DEBUG    < jediTaskID=24326915 > start

And once jobs are submitted there should be messages like

.. code-block:: text

  2021-02-24 07:34:52,905 panda.log.JobGenerator: INFO     <jediTaskID=24326915 datasetID=359212908> submit njobs=1 jobs

in *logdir/panda-JobGenerator.log*. There should be also many messages in ``logdir/panda-JediDBProxy.log``
about database interactions.

Jobs are passed to the PanDA server. If you see
something like

.. code-block:: text

  2021-02-24 07:34:29,399 panda.log.DBProxy: DEBUG    activateJob : 4981974846

in ``logdir/panda-DBProxy.log`` this means that the job successfully went through PanDA server components
and is ready to be pickup by the pilot.

------------

|br|

6. Harvester Setup
-------------------------
In this tutorial we use HTCondor as submission backend, so first you need to install HTCondor on the VM where
Harvester will be installed. `HTCondor documentation <https://htcondor.readthedocs.io/en/latest/>`_ will help.

Then refer to `Harvester installation guide <https://github.com/HSF/harvester/wiki/Installation-and-configuration>`_
to install Harvester on the same VM. For small scale tests it is enough to use the sqlite3 database backend.
Make sure that ``harvester_id`` in ``panda_harvester.cfg`` can be an arbitrary unique string but it needs to be
registered in the database of JEDI and the PanDA server (i.e., not the harvester database),

.. code-block:: sql

 INSERT INTO PANDA.HARVESTER_INSTANCES (HARVESTER_ID,DESCRIPTION) VALUES('your_harvester_id','some description')

6.1. Queue Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In this tutorial, queues are specified in a local json file, so ``panda_harvester.cfg`` has

.. code-block:: text

    [qconf]

    configFile = panda_queueconfig.json

    queueList =
     ALL

``panda_queueconfig.json`` could be something like
`a config example <https://github.com/HSF/harvester/blob/master/examples/panda_queueconfig_doma.json>`_
where the computing resource defined in the previous step `TEST_SITE` is set to "online".

.. code-block:: text

    "TEST_SITE": {
        "queueStatus": "online",
        "prodSourceLabel": "test",
        "templateQueueName": "production.pull",
        "maxWorkers": 1,
        "nQueueLimitWorkerMin": 1,
        "nQueueLimitWorkerMax": 2,
        "submitter": {
                        "templateFile": "/opt/panda/misc/grid_submit_pilot.sdf"
          }
      },
    }

where the ``templateFile`` is a template file to generate sdf files like
`an sdf template example <https://github.com/HSF/harvester/blob/master/examples/htcondor_submit_doma_pilot.sdf>`_
Each sdf file has

.. code-block:: text

 executable = /opt/panda/misc/runpilot2-wrapper.sh
 arguments = -s {computingSite} -r {computingSite} -q {pandaQueueName} -j {prodSourceLabel} -i {pilotType} \
      -t -w generic --pilot-user generic --url https://ai-idds-01.cern.ch -d --harvester-submit-mode PULL \
      --allow-same-user=False --job-type={jobType} {pilotResourceTypeOption} {pilotUrlOption}

to launch the pilot on a worker node. ``runpilot2-wrapper.sh`` is available in
`the pilot-wrapper repository <https://github.com/PanDAWMS/pilot-wrapper>`_.
You need to put a template file and the pilot wrapper on the VM, and edit the template file and
``panda_queueconfig.json`` accordingly. Note that the ``--url`` argument must take the URL of your PanDA server
so that the pilot will talk to your PanDA server.

6.2 Testing Harvester
^^^^^^^^^^^^^^^^^^^^^^^^
Now you can start Harvester to submit the pilot and see if the pilot properly communicates with the PanDA server.

.. prompt:: bash

 etc/rc.d/init.d/panda_harvester start

Harvester logs are available in the directory specified in ``panda_common.cfg``. It is good to check
``panda_harvester_stdout.log``, ``panda_harvester_stderr.log``, and ``panda-submitter.log``.
Once the pilot is sent out through HTCondor, there should be log files in the directly specified in the sdf template
file.

.. code-block:: text

 log = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).log
 output = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).out
 error = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).err

where ``{logDir}`` is specified in ``panda_queueconfig.json`` and ``{logSubdir}`` is automatically defined
by Harvester based on the timestamp.

If communication between the pilot and the PanDA server is successful there will be messages in PanDA
server's log files such as ``panda_server_access_log`, `panda-JobDispatcher.log``, and ``panda-DBProxy.log``.

-------------

|br|


7. PanDA Monitor Setup
----------------------------