===================================
Harvester Configuration
===================================

*This documentation is for Harvester v0.5.0 or above*


.. contents:: Table of Contents
    :local:
    :depth: 2


|br|

================================================================

Configuration of panda-common
-----------------------------

Harvester has a dependency on `panda-common <https://github.com/PanDAWMS/panda-common>`_, which needs to be configured.

The configuration file of panda-common is at `${VIRTUAL_ENV}/etc/panda/panda_common.cfg`

The ``logdir`` needs to be set in panda_common.cfg to specify the directory for harvester logs.
It is recommended to use a non-NFS directory to avoid buffering. 

The following parameters are available\: 

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Example

   * - ``logdir``
     - A directory for log files (of Harvester).
     - ``logdir = /var/log/harvester``, ``logdir = /var/log/panda``

   * - ``log_level``
     - Logging level, compatible with python logging. Can be ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, ``DEBUG`` (default), or ``NOTSET``. NOTE: It is also possible to set logging level for each logger in the ``log_level`` section in main harvester configuration (e.g. in panda_harvester.cfg); thus it is better to leave ``DEBUG`` here in panda-common configuration.
     - ``log_level = DEBUG``

   * - ``rotating_policy``
     - Policy for log rotation. Can be ``time`` (rotation at certain timed intervals), ``size`` (rotation at a predetermined size), or ``none`` (default, no rotation).
     - 

   * - ``rotating_backup_count``
     - How many old log files should be kept. Effective unless ``rotating_policy=none``. Default is 1 .
     - 

   * - ``rotating_max_size``
     - Rotation happens when the file size in MB is about to be exceeded. Effective only when ``rotating_policy=size``. Default is 1024 .
     - 

   * - ``rotating_interval``
     - Rotation interval in hours. Effective only when rotating_policy=time. Default is 24 .
     - 


|br|

================================================================

Setup of environment variables (sysconfig files)
------------------------------------------------

There are two ways to set up environment variables for Harvester service\:

Traditional sysconfig file
""""""""""""""""""""""""""

The sysconfig file for Harvester is a script which sets environment variables via linux export commands.
When Harvester service starts, the sysconfig file will be executed first before launching Harvester processes so that the Harvester processes can inherit the very environment variables.

Several parameters may need to be adjusted in the setup sysconfig file (etc/sysconfig/panda_harvester).

The following parameters need to be set correctly in etc/sysconfig/panda_harvester .

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Example

   * - ``VIRTUAL_ENV``
     - The virtual environment of python to run Harvester
     - ``export VIRTUAL_ENV=/opt/harvester``

   * - ``PANDA_HOME``
     - Config files must be under $PANDA_HOME/etc
     - ``export PANDA_HOME=${VIRTUAL_ENV}``

   * - ``PYTHONPATH``
     - Must contain the pandacommon package and site-packages where the pandaharvester package is available
     - ``export PYTHONPATH=$VIRTUAL_ENV/lib/python3.11/site-packages/pandacommon:${VIRTUAL_ENV}/lib/python3.11/site-packages``
    


EnvironmentFile of systemd service
""""""""""""""""""""""""""""""""""

If one runs harvester with systemd service, one should set the environment variables with EnvironmentFile of systemd (instead of traditional sysconfig file).

The EnvironmentFile defines the environment variables as the sysconfig file does. However, the EnvironmentFile is NOT a script to be executed, and its syntax to set variables is ``<variable_name>=<value>`` (without "export" command!)

See `here <https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#EnvironmentFile=>`_ for more details about EnvironmentFile of systemd.

When installing Harvester with pip (under the python virtual environment with meant to run Harvester), a pre-configured EnvironmentFile is generated automatically at `${VIRTUAL_ENV}/etc/sysconfig/panda_harvester_env.systemd.rpmnew`.
One can copy the pre-configured EnvironmentFile and edit the new file if necessary.

See :ref:`setting up Harvester systemd service <ref-service-systemd>` for the details steps.


|br|

================================================================

Configure main Harvester configuration
--------------------------------------

The main Harvester configuration (or just Harvester configuration) is where to configure Harvester software itself.
It contains configurations of Harvester ID, of backend database (DB), of each agent of harvester, etc.


Sources of Harvester configuration
""""""""""""""""""""""""""""""""""

The Harvester configuration can come from several places\:

* **Local configuration file**: A configuration file on the Harvester instance, written in the format of python configparser. Its filename must be `panda_harvester.cfg`. Its default location is under `${VIRTUAL_ENV}/etc/panda/` or `${PANDA_HOME}/etc/panda/`. This is the common use case of Harvester running on bare metal or VM instance.
* **Remote configuration file**: A configuration file on a remote server accessible via the http/https URL given by the environment variable ``HARVESTER_INSTANCE_CONFIG_URL``. Harvester will load the remote configuration file before starting its agents. See for more details :ref:`here <ref-misc-remote_config_files>`.
* **Local configmap (configuration map in JSON)**: A configuration file on the Harvester instance, written in JSON format. Its filename must be `panda_harvester_configmap.json`. Its default location is under `${VIRTUAL_ENV}/etc/configmap/` or `${PANDA_HOME}/etc/configmap/`. The local configmap has the same way to set parameters as the local configuration file, while written in JSON format. If both local configmap and local configuration files exist on the instance, the values in the local configmap prevail. The local configmap is often used in Kubernetes (K8s) containers, where the local configmap of harvester is shared via *K8s ConfigMaps* to the pods.


Examples of Harvester configuration in the following documentation will be shown in the format of local configuration file.



Parameters in Harvester configuration
"""""""""""""""""""""""""""""""""""""

Harvester main configuration has sections, and each section has a couple of parameters\:

* In local configuration file, the sections are shown in brackets like ``[section1]``, and below each section their are parameters are set in the manner of ``parameter1 = <value1>``. Beware of the syntax (of python configparser): The boolean and none/null values should be written as ``True``, ``False`` and ``None`` respectively (first letter capitalized!).
* In local configmap, sections and parameters form nested JSON objects. For example: ``{ "section1": {"parameter1": <value1>, "parameter2": <value2>}, ... }``. Beware of the JSON syntax: The boolean and none/null values should be written as ``true``, ``false`` and ``null`` respectively (all in lowercase!), and all the keys and the string values must be written between double quotes, like ``"key1": "string_value1"``.

Parameter values can be set to be environment variables written as ``$XYZ`` or ``${XYZ}``.

After pip installed harvester, a template of local Harvester configuration file is available at `${VIRTUAL_ENV}/etc/panda/panda_harvester.cfg.rpmnew`.
One can copy the template to the path for the local configuration file `${VIRTUAL_ENV}/etc/panda/panda_harvester.cfg`, and then configure Harvester by editing the new file.

See :ref:`here <ref-harvester-harvester_config_params>` for descriptions of all configurable sections and parameters in Harvester main configuration.

|br|

================================================================

High-performance configuration
------------------------------

It is possible to increase performance of Harvester via the following setups\:

  * MariaDB or MySQL DB - more powerful database backend than SQLite (the DB needs to be installed and set up additionally by the admin)
  * Multi-processing python application service based on uWSGI
  * Messaging mechanism with FIFO


.. _ref-harvester-mysql-setup:

MariaDB/MySQL DB setup
""""""""""""""""""""""

First, make the database schema named "HARVESTER" and the user account "harvester" (with a password) on MariaDB/MySQL. E.g.  

.. code-block:: text

    $ mysql -u root
    MariaDB > CREATE DATABASE HARVESTER;
    MariaDB > CREATE USER 'harvester'@'localhost' IDENTIFIED BY 'your_password';
    MariaDB > GRANT ALL PRIVILEGES ON HARVESTER.* TO 'harvester'@'localhost';


Then Harvester tables will be automatically created when the Harvester service starts, so no need to create tables manually. 

Next, make sure that one does not have ``STRICT_TRANS_TABLES`` set in DB\:

.. code-block:: text

    MariaDB [(none)]> SELECT REPLACE(@@SQL_MODE, ',', '\n');
    +--------------------------------+
    | REPLACE(@@SQL_MODE, ',', '\n') |
    +--------------------------------+
    |                                |
    +--------------------------------+
    1 row in set (0.01 sec)


Then, edit /etc/my.cnf (or one's configuration file of MariaDB/MySQL) if having need to optimize the database. For example\:

.. code-block:: text

    [mysqld]
    max_allowed_packet=1024M

(Setting max_allowed_packet to be 1024MB is recommended)


To connect to MariaDB/MySQL, one needs *mysqlclient* or *mysql-connector* package.


with mysqlclient
~~~~~~~~~~~~~~~~

This is the recommended way to connect MariaDB/MySQL currently.

If one wants to use mysqlclient (whose python module is called MySQLdb) to access to MariaDB/MySQL, pip install mysqlclient under the virtual environment of Harvester\:

.. code-block:: text

    $ pip install mysqlclient


Note that since mysqlclient requires compilation from MySQL lib, one may need to install additional package in advance: ``yum install mysql-devel`` or ``yum install MariaDB-devel MariaDB-shared`` (For el9 or above, replace ``yum`` with ``dnf``)

And the following parameters are required in local configuration file\:

.. _ref-harvester-mysql-local-conf:

.. code-block:: text

  [db]

  # engine sqlite or mariadb
  engine = mariadb

  # use MySQLdb for mariadb access
  useMySQLdb = True

  # user name
  user = harvester

  # password
  password = FIXME
  
  # schema
  schema = HARVESTER 


where ``engine = mariadb`` , ``useMySQLdb = True``, and ``password`` should be changed according to the password set :ref:`here <ref-harvester-mysql-setup>`.


with mysql-connector
~~~~~~~~~~~~~~~~~~~~

Harvester uses mysql-connector by default to access to MariaDB.
However, it is NOT recommended now to use mysql-connector now.

If one wants to use mysql-connector to access to MariaDB/MySQL, pip install mysql-connector-python under the virtual environment of Harvester\:

.. code-block:: text

  $ pip install mysql-connector-python<=8.0.11


Warning: It was tested that mysql-connector-python 8.0.12 does not work!

The local configuration file should be changed as :ref:`here <ref-harvester-mysql-local-conf>`, but with the only difference: ``useMySQLdb = False``.


uWSGI setup
""""""""""""

Pip install uwsgi under the virtual environment of Harvester:

.. code-block:: text

    $ pip install uwsgi

Then one can check :doc:`here </installation/harvester_docs/service>` about how to configure Harvester service which runs Harvester with uWSGI.


FIFO setup
""""""""""

Check :doc:`Harvester FIFO </installation/harvester_docs/fifo>` for the details.




|br|

================================================================

.. _ref-harvester-harvester_config_params:

All Harvester configuration parameters
--------------------------------------

* ``master``: Section for Harvester master processes and general parameters
    - ``uname``: User name to run Harvester processes. Mandatory
    - ``gname``: Group name to run Harvester processes. Mandatory
    - ``harvester_id``: HarvesterID is a unique ID to represent the Harvester instance: one or multiple nodes sharing the same Harvester DB. The new HarvesterID will be registered in the PanDA server when the Harvester and PanDA server connect. Mandatory
    - ``debugger_port``: Port number for Harvester debugger, which opens this port for debugging messages. Default is 19550
    - ``dynamic_plugin_change``: Enable dynamically change plugins. If True, when one modifies plugin modules in the queue configuration, Harvester will automatically reload the new plugin modules after some period (convenient, at risk of errors in unloading/reloading buggy plugins); otherwise, it requires Harvester service restart for the plugin changes to take effect (more reliable). Default is False
* ``db``: Section for Harvester DB backend
    - ``verbose``: Whether to have more verbose dbproxy logs. Mandatory
    - ``useInspect``: Whether to use python inspect for more debugging messages. Note that enabling useInspect may be CPU intensive. Default is False
    - ``nConnections``: Number of database connections in each Harvester process. Mandatory
    - ``engine``: Database engine. Must be either ``sqlite`` (for **SQLite**) or ``mariadb`` (for **MariaDB** or **MySQL**). Mandatory
    - ``database_filename``: Database file path for SQLite. Recommend a path on local disk as SQLite does not work well on NAS. Mandatory and useful only if ``engine = sqlite``
    - ``useMySQLdb``: Whether to use mysqlclient (MySQLdb) to connect MariaDB or MySQL. If False, Harvester will connect the DB with mysql-connector. In either case, the required interface package must be installed with pip. Useful only if ``engine = mariadb``. Default is False
    - ``user``: DB user name of MariaDB or MySQL for Harvester. Mandatory and useful only if ``engine = mariadb``
    - ``password``: DB password of MariaDB or MySQL Harvester DB user. Mandatory and useful only if ``engine = mariadb``
    - ``schema``: DB schema (database name) for MariaDB or MySQL for Harvester. Mandatory and useful only if ``engine = mariadb``
    - ``host``: Host of the MariaDB or MySQL instance. Mandatory and useful only if ``engine = mariadb``
    - ``port``: Port of the MariaDB or MySQL instance. Useful only if ``engine = mariadb``. Default is 3306
    - ``reconnectTimeout``: Timeout in seconds to keep trying to auto-reconnect the MariaDB or MySQL DB (auto-reconnection is convenient when having temporary DB disconnections expected to be recovered soon). After the timeout (which usually means DB issues requiring manual intervention), Harvester will not try to connect the DB anymore and stop running, and it requires Harvester service restart to bring up the service again (after DB issue addressed of course). Useful only if ``engine = mariadb``. Default is 300, aka 5 minutes
    - ``syncMaxWorkerID``: Whether to synchronize max workerID when starting up Harvester. If True, Harvester will updated the max workerID with that stored from PanDA server (give the HarvesterID). This is useful when one wants to start over a new Harvester (by purging the Harvester DB) but also wants to continue from the max workerID to avoid overwriting records of old workers (with smaller workerID) stored on PanDA servers. Default is False
* ``fifo``: Section for FIFO component. More details :doc:`here </installation/harvester_docs/fifo>`
    - ``fifoModule`` and ``fifoClass``: FIFO plugin module and class name. Mandatory
    - ``database_filename``: Database file path for the FIFO with SQLite backend. Mandatory only if using sqlite_fifo plugin
* ``communicator``: Section for communicator agent
    - ``moduleName`` and ``className``: Communicator plugin module and class name. Currently the only plugin available is panda_communicator; i.e. ``moduleName = pandaharvester.harvestercommunicator.panda_communicator`` and ``className = PandaCommunicator``. Mandatory
    - ``nConnections``: Number of connections for communicator agent to connect PanDA server. Mandatory
* ``pandacon``: Section for communication to PanDA server
    - ``timeout``: Timeout in seconds for Harvester to connect PanDA server. Mandatory
    - ``auth_type``: Type of authentication credential. Must be either ``x509`` (X509 proxy certificate) or ``oidc`` (OIDC token). Mandatory
    - ``ca_cert``: Path of the CA file (bundle of CA certificates). Mandatory
    - ``cert_file`` and ``key_file``: Path of pair of certificate and key respectively to authenticate PanDA server. Or, if X509 proxy file is used, both ``cert_file`` and ``key_file`` should be set to be the path of the X509 proxy. Mandatory only if ``auth_type = x509``
    - ``auth_token``: Path of the token to authenticate PanDA server. Mandatory only if ``auth_type = oidc``
    - ``auth_origin``: OIDC origin of the token. Usually related to the VO. Mandatory only if ``auth_type = oidc``
    - ``pandaURL``: The base URL of PanDA server API via http (for read-only requests). Mandatory
    - ``pandaURLSSL``: The base URL of PanDA server API via https (for write requests which requires authentication). Mandatory
    - ``pandaCacheURL_W``: The base URL of for write access to log cache server. Mandatory only if using plugins that requires pandacache server
    - ``pandaCacheURL_R``: The base URL of for read access to log cache server. Mandatory only if using plugins that requires pandacache server
    - ``verbose``: Whether to have more verbose communicator logs about PanDA connection. Default is False
    - ``useInspect``: Whether to use python inspect for more debugging messages. Note that enabling useInspect may be CPU intensive. Default is False
    - ``getEventsChunkSize``: Number of events in a chunk in a single request to get events from PanDA server. Default is 5120
    - ``multihost_auth_config``: Path of an additional configuration file if there are multiple hosts and each host requires different credentials to authenticate. The configuration file should be written in JSON, in the form of ``{"host:port": {"auth_type": "x509 or oidc", "cert_file": /path/to/cert, "key_file": /path/to/key, "ca_cert": /path/to/ca_cert, "auth_token": "token or file:/path/to/token"}, ...}``. Default is None
    

(To be continued...)


Most agents define `lockInterval` and `xyzInterval` (where 'xyz' is 'check', 'trigger', and so on, depending on agent actions) parameters in local configuration file. 
Each agent runs multiple threads in parallel and each thread processes job and/or worker objects independently. First each thread retrieves objects from the database, processes them, and finally releases them. The behaviors of the agents can be tuned with these parameters\:

* **lockInterval**: defines how long the objects are kept for a thread after they are retrieved. During the period other threads cannot touch the objects. Another thread can take those objects after `lockInterval`, which is useful when harvester is restarted after it was killed and the objects were not properly released. Note that `lockInterval` must be longer than the process time of each thread. Otherwise, multiple threads would try to process the same objects concurrently. 
* **xyzInterval**: defines how often the objects are processed by threads, i.e. once the objects are released by a thread, they are processed again after the interval of `xyzInterval`. 
* **maxJobsXYZ**: defines how many job objects are retrieved by a thread. Generally large `maxJobsXYZ` doesn't make sense since jobs are sequentially processed by the thread and the process time of the thread simply becomes longer. Also large `maxJobsXYZ` could be problematic in terms of memory usage since many job objects are loaded into RAM from the database before being processed.

     
===============


Name | Description  
--- | --- 
master.uname | User name of the daemon process
master.gname | Group name of the daemon process
master.harvester_id  | Unique ID of the harvester instance. See [link](https://github.com/HSF/harvester/wiki/Developer-Q&A#what-is-harvester_id) for the details
db.engine | database engine : sqlite or mariadb
db.database_filename | Filename of the local database. Note that sqlite doesn't like NAS
db.verbose | Set True to dump all SQL queries in the log file
pandacon.ca_cert | CERN CA certificate file
pandacon.cert_file | A grid proxy file to access the panda server
pandacon.key_file | The same as pandacon.cert_file
pandacon.auth_token | Token for oidc (put this line only if authenticating PanDA server with oidc token to instead of grid proxy)
pandacon.auth_origin | Origin for oidc (put this line only if authenticating PanDA server with oidc token to instead of grid proxy)
qconf.configFile | The queue configuration file. See the next section for details
qconf.queueList | The list of PandaQueues for which the harvester instance works
credmanager.moduleName | The module name of the credential manager
credmanager.className | The class name of the credential manager
credmanager.inCertFile | A grid proxy without VOMS extension. CredManager plugin generates VOMS proxy using the file
credmanager.outCertFile | A grid proxy with VOMS extension which is generated by CredManager plugin

