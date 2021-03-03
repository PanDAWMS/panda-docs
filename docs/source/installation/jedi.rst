=================
JEDI
=================

Here is the setup guide of JEDI.

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

The following parameters need to be modified if any.

.. list-table:: master parameters
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - uname
     - The userid under which JEDI runs
     - atlpan
   * - gname
     - The group under which JEDI runs
     - zp

.. list-table:: database parameters
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - dbhost
     - The database hostname
     -
   * - dbuser
     - The database username
     -
   * - dbpasswd
     - The database password
     -
   * - nWorkers
     - The number of database connections
     - 5
   * - schemaPANDA
     - The schema name of PanDA database tables
     - ATLAS_PANDA
   * - schemaMETA
     - The schema name of meta database tables
     - ATLAS_PANDAMETA
   * - schemaPANDAARCH
     - The schema name of archive database tables
     - ATLAS_PANDAARCH
   * - schemaJEDI
     - The schema name of JEDI database tables
     - ATLAS_PANDA
   * - schemaDEFT
     - The schema name of DEFT database tables
     - ATLAS_DEFT

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
    Message processor


Common Parameters
~~~~~~~~~~~~~~~~~

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


Msgprocessor Parameters
~~~~~~~~~~~~~~~~~~~~~~~

JEDI Message Processor can talk to other systems through message brokers which supports STOMP protocol (e.g. ActiveMQ, RabbitMQ, etc.).


JEDI Configuration
""""""""""""""""""

The ``configFile`` parameter: Specify the path of the json configuration file for ``Message Processor`` . If commented, JEDI Message Processor will be disabled.

.. code-block:: text

    [msgprocessor]

    # json config file of message processors
    configFile = /etc/panda/jedi_msg_proc_config.json


JSON Configuration File
"""""""""""""""""""""""

An example of the JSON content in ``configFile``:

.. code-block:: text

    {
    "mb_servers": {
        "iDDS_mb": {
            "host_port_list": ["some-mb.cern.ch:1234"],
            "use_ssl": false,
            "username": "<username>",
            "passcode": "<passcode>",
            "verbose": true
        },
        "rucio_mb": {
            "host_port_list": ["another-mb.cern.ch:5678"],
            "use_ssl": true,
            "cert_file": "/path/of/cert",
            "key_file": "/path/of/key",
            "vhost": "/"
        }
    },
    "queues": {
        "idds": {
            "server": "iDDS_mb",
            "destination": "/queue/Consumer.jedi.atlas.idds"
        },
        "rucio-events": {
            "server": "rucio_mb",
            "destination": "/queue/Consumer.panda.rucio.events"
        }
    },
    "processors": {
        "atlas-idds": {
            "enable": true,
            "module": "pandajedi.jedimsgprocessor.atlas_idds_msg_processor",
            "name": "AtlasIddsMsgProcPlugin",
            "in_queue": "idds",
            "verbose": true
        },
        "panda-callback": {
            "enable": true,
            "module": "pandajedi.jedimsgprocessor.panda_callback_msg_processor",
            "name": "PandaCallbackMsgProcPlugin",
            "in_queue": "rucio-events"
        }
    }
    }


In the JSON object, the configuration of **message broker servers**, **queues**, and **message processors** are defined.


**Message Broker Servers**

Defined under ``"mb_servers"`` object.
In the ``"mb_servers"`` object, a key can be any arbitrary name standing for the message broker server.
In the example above, there are 2 message broker servers, named "iDDS_mb" and "rucio_mb".

Parameters of a message broker server\:

* ``"host_port_list"``: A list of host\:port of the message broker servers. If multiple host\:port are put in the list, only random one of them will be connected and the others will be failover candidates. Also in host\;port if a hostname is used instead of IP address, all IP addresses mapped to the hostname according to DNS resolution will be connected. Mandatory
* ``"use_ssl"``: STOMP option, whether to use SSL in authentication. Default is false
* ``"username"`` and ``"passcode"``: STOMP option, authenticate the message broker server with username and passcode. Default is null
* ``"cert_file"`` and ``"key_file"``: STOMP option, authenticate the message broker server with key/cert pair. Default is null
* ``"vhost"``: STOMP option, vhost of the message broker. Default is null
* ``"verbose"``: Whether to log verbosely about communication details with this message broker server. Default is false


**Queues**

Defined under ``"queues"`` object.
In the ``"queues"`` object, a key can be any arbitrary name standing for a message queue.
In the example above, there are 2 message queues, named "idds" and "rucio-events".

Parameters of a message queue\:

* ``"server"``: Name of the message broker server defined under ``"mb_servers"`` for this message queue. Mandatory
* ``"destination"``: STOMP option, destination path on the message broker server for this message queue. Mandatory


**Message Processors**

Defined under ``"processors"`` object

In the ``"processors"`` object, a key can be any arbitrary name standing for a message processor.
A message processor running on JEDI consumes a message from a message queue and processes the message (and some message processor sends a new message to another message queue).
There are various message processor plugins for different workflows. All message processors available in JEDI are in the `message processor plugin repository <https://github.com/PanDAWMS/panda-jedi/tree/master/pandajedi/jedimsgprocessor>`_.


Parameters of a message broker server\:

* ``"enable"``: Whether to enable this message processor. Useful when one needs to stop the message processor temporarily but still wants to keep it the configuration file. Default is true
* ``"module"`` and ``"name"``: Module and class name of the message processor plugin in JEDI. Mandatory
* ``"in_queue"``: Queue name defined under ``"queues"`` object, where the message processor consumes messages from this queue. Default is null
* ``"out_queue"``: Queue name defined under ``"queues"`` object, where the message processor sends messages to this queue. Not required if the processor does not send out messages. Default is null
* ``"verbose"``: Whether to log verbosely about this message processor. Default is false



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
