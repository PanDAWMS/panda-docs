===================================
Installation
===================================

Requirements
------------

Python: 3.8 or higher
Database backend: SQLite or MySQL/MariaDB
  * SQLite: sqlite3 3.7.0
  * MySQL/MariaDB: MySQL 8 or higher; or MariaDB 10 or higher


Install Harvester
-----------------

Harvester can be installed with or without root privilege


Setup virtual environment
"""""""""""""""""""""""""

.. tabs::

   .. code-tab:: Python native venv

        $ cd your_installation_directory
        $ python3 -m venv harvester
        $ cd harvester
        $ . bin/activate

   .. code-tab:: Others

        # For Cori@NERSC
        $ module load python
        $ mkdir harvester
        $ conda create -p ~/harvester python
        $ source activate ~/harvester


Install Harvester package
"""""""""""""""""""""""""""""

.. tabs::

   .. code-tab:: General

        # upgrade pip
        $ pip install pip --upgrade

        # install Harvester
        $ pip install git+https://github.com/HSF/harvester.git

   .. code-tab:: ATLAS

        # upgrade pip
        $ pip install pip --upgrade

        # install Harvester
        $ pip install git+https://github.com/HSF/harvester.git
        # For ATLAS GRID instances, install with:
        $ pip install pandaharvester[atlasgrid]@git+https://github.com/HSF/harvester



.. code-block:: text

    # upgrade pip
    $ pip install pip --upgrade

    # install Harvester
    $ pip install git+https://github.com/HSF/harvester.git
    # for ATLAS GRID instance, install with this instead
    # (deprecated)
    $ pip install git+https://github.com/HSF/harvester#egg=pandaharvester[atlasgrid]
    # new syntax
    $ pip install pandaharvester[atlasgrid]@git+https://github.com/HSF/harvester

    # copy sample setup and config files
    $ mv etc/sysconfig/panda_harvester.rpmnew.template  etc/sysconfig/panda_harvester
    $ mv etc/panda/panda_common.cfg.rpmnew etc/panda/panda_common.cfg
    $ mv etc/panda/panda_harvester.cfg.rpmnew.template etc/panda/panda_harvester.cfg


Upgrade Harvester package (if Harvester is already installed)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. tabs::

   .. code-tab:: General

        $ cd your_installation_directory/harvester
        $ . bin/activate
        # Upgrade all dependencies
        $ pip install --upgrade git+https://github.com/HSF/harvester.git
        # Upgrade harvester package only
        $ pip install --no-deps --force-reinstall git+https://github.com/HSF/harvester.git

   .. code-tab:: ATLAS

        $ cd your_installation_directory/harvester
        $ . bin/activate
        # Upgrade harvester package only
        $ pip install --no-deps --force-reinstall pandaharvester[atlasgrid]@git+https://github.com/HSF/harvester


Misc
-----------------



### Setup and system configuration files
Several parameters need to be adjusted in the setup file (etc/sysconfig/panda_harvester)
and two config files (etc/panda/panda_common.cfg and etc/panda/panda_harvester.cfg).
panda_harvester.cfg can be put remotely (see [remote configuration files](https://github.com/HSF/harvester/wiki/Installation-and-configuration#remote-configuration-files)).

The following parameters need to be modified in etc/sysconfig/panda_harvester.

Name | Description  
--- | --- 
PANDA_HOME | Config files must be under $PANDA_HOME/etc
PYTHONPATH | Must contain the pandacommon package and site-packages where the pandaharvester package is available

- Example
```
export PANDA_HOME=$VIRTUAL_ENV
export PYTHONPATH=$VIRTUAL_ENV/lib/python3.6/site-packages/pandacommon:$VIRTUAL_ENV/lib/python3.6/site-packages
```

The **logdir** needs to be set in etc/panda/panda_common.cfg. It is recommended to use a non-NFS directory to avoid buffering. [Here](https://github.com/HSF/harvester/wiki/Utilities#logging) are additional explanations for logging parameters.

Name | Description 
--- | --- 
logdir | A directory for log files

- Example
```
logdir = /var/log/panda
```

The following list shows parameters need to be adjusted in etc/panda/panda_harvester.cfg. You can use $XYZ or ${XYZ} if you want to set those parameters through environment variables.

Name | Description  
--- | --- 
master.uname | User name of the daemon process
master.gname | Group name of the daemon process
master.harvester_id  | Unique ID of the harvester instance. See [link](https://github.com/HSF/harvester/wiki/Developer-Q&A#what-is-harvester_id) for the details
db.database_filename | Filename of the local database. Note that sqlite doesn't like NAS
db.engine | database engine : sqlite or mariadb
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

Concerning agent optimization, see the next section.

#### lockInterval, xyzInterval, and maxJobsXYZ/maxWorkersXYZ

Most agents define `lockInterval` and `xyzInterval` (where 'xyz' is 'check', 'trigger', and so on, depending on agent actions) in panda_harvester.cfg. Each agent runs multiple threads in parallel and each thread processes job and/or worker objects independently. First each thread retrieves objects from the database, processes them, and finally releases them. `lockInterval` defines how long the objects are kept for a thread after they are retrieved. During the period other threads cannot touch the objects. Another thread can take those objects after `lockInterval`, which is useful when harvester is restarted after it was killed and the objects were not properly released. Note that `lockInterval` must be longer than the process time of each thread. Otherwise, multiple threads would try to process the same objects concurrently. 
On the other hand, `xyzInterval` defines how often the objects are processed by threads, i.e. once the objects are released by a thread, they are processed again after the interval of `xyzInterval`. maxJobsXYZ defines how many job objects are retrieved by a thread. Generally large maxJobsXYZ doesn't make sense since jobs are sequentially processed by the thread and the process time of the thread simply becomes longer. Also large maxJobsXYZ could be problematic in terms of memory usage since many job objects are loaded into RAM from the database before being processed.   

### Queue configuration file

Plug-ins for each PandaQueue is configured in the queue configuration file.
The filename is defined in **qconf.configFile**. It has to be put in the $PANDA_HOME/etc/panda
directory and/or at URL (see [remote configuration files](https://github.com/HSF/harvester/wiki/Installation-and-configuration#remote-configuration-files)). This file might be integrated in the information system json in the future, but for
now it has to be manually created. Here are examples of the queue configuration file for
[the grid](https://github.com/HSF/harvester/blob/master/examples/panda_queueconfig_grid.json)
and for [HPC](https://github.com/HSF/harvester/blob/master/examples/panda_queueconfig_hpc.json).
The contents is a json dump of 

```python
{
"PandaQueueName1": {
		   "QueueAttributeName1": ValueQ_1,
		   "QueueAttributeName2": ValueQ_2,
		   ...
		   "QueueAttributeNameN": ValueQ_N,
		   "Agent1": {
		   	     "AgentAttribute1": ValueA_1,
			     "AgentAttribute2": ValueA_2,
			     ...
			     "AgentAttributeM": ValueA_M
			     },
		   "Agent2": {
		   	     ...
			     },
		   ...
		   "AgentX": {
		   	     ...
		   	     },
		   },
"PandaQueueName2": {
		   ...
		   },
...
"PandaQueueNameY": {
		   ...
		   },

}
```

#### Queue attributes

Here is the list of queue attributes.

Name | Description  
--- | --- 
prodSourceLabel | Source label of the queue. _managed_ for production
prodSourceLabelRandomWeightsPermille | The probability distribution (in permille) to randomize the source label of the jobs that job_fetcher fetches. E.g. `"prodSourceLabelRandomWeightsPermille": {"rc_test":150, "rc_test2":200, "rc_alrb":250}` makes job_fetcher to fetch rc_test jobs in 15% probability, rc_test2 in 20%, rc_alrb in 25%, and jobs of `prodSourceLabel` (defined above) in the rest 40%
nQueueLimitJob | The max number of jobs pre-fetched and queued, i.e. jobs in starting state. This attribute is ignored if nQueueLimitJobRatio is used. See [this page](https://github.com/HSF/harvester/wiki/Agents-and-Plugins-descriptions#jobfetcher) for the details
nQueueLimitJobRatio | The target ration of the number of starting jobs to the number of running jobs. See [this page](https://github.com/HSF/harvester/wiki/Agents-and-Plugins-descriptions#jobfetcher) for the details
nQueueLimitJobMax | Supplemental attribute for nQueueLimitJobRatio to define the upper limit on the number of starting jobs. See [this page](https://github.com/HSF/harvester/wiki/Agents-and-Plugins-descriptions#jobfetcher) for the details
nQueueLimitJobMin | Supplemental attribute for nQueueLimitJobRatio to define the lower limit on the number of starting jobs. See [this page](https://github.com/HSF/harvester/wiki/Agents-and-Plugins-descriptions#jobfetcher) for the details
nQueueLimitWorker | The max number of workers queued in the batch system, i.e. workers in submitted, pending, or idle state
maxWorkers | The max number of workers. maxWorkers-nQueueLimitWorker is the number of running workers
nQueueLimitWorkerRatio | The limit on the ratio of queued workers to running workers. (the number of queued workers)/(the number of running workers) must be less than nQueueLimitWorkerRatio/100
nQueueLimitWorkerMax | The max number of queued workers
nQueueLimitWorkerMin | The min number of queued workers
maxNewWorkersPerCycle | The max number of workers which can be submitted in a single submission cycle. 0 by default to be unlimited
truePilot | To suppress heartbeats for jobs in running, transferring, finished, failed state
runMode | self (by default) to submit workers based on nQueueLimit* and maxWorkers. slave to be centrally controlled by panda  
allowJobMixture | Jobs from different tasks can be given to a single worker if true
mapType | Mapping between jobs and workers. NoJob = (workers themselves get jobs directly from Panda after they are submitted). OneToOne = (1 job x 1 worker). OneToMany = (1xN, aka the multiple consumer mode). ManyToOne = (Nx1, aka the multi-job pilot mode). Harvester prefetches jobs except NoJob. 
useJobLateBinding | true if the queue uses job-level late-binding. Note that for job-level late-binding harvester prefetches jobs to pass them to workers when those workers get CPUs, so mapType must not be NoJob. If this flag is false or omitted jobs are submitted together with workers.  

Agent is **preparator**, **submitter**, **workMaker**, **messenger**,
**stager**, **monitor**, and **sweeper**. Two agent parameters `name` and `module`
are mandatory to define the class name module names of the agent.
Roughly speaking,
```python
from agentModule import agentName
agent = agentName()
```
is internally invoked. Other agent attributes are set to the agent instance as instance variables.
Parameters for plugins are described in [this page](https://github.com/HSF/harvester/wiki/Plugins-and-Agents-descriptions).


### init.d script
An example of init.d script is available at etc/rc.d/init.d/panda_harvester.rpmnew.template.
You need change
`VIRTUAL_ENV` in the script and rename it to panda_harvester-apachectl. Change log and lock files if necessary.
Then to start/stop harvester 
```sh
$ etc/rc.d/init.d/panda_harvester start
$ etc/rc.d/init.d/panda_harvester stop
```



### High-performance configuration
It is possible to configure harvester instances with more powerful database backend (MariaDB) and multi-processing based on Apache+WSGI (or uWSGI). Note that Apache is used to launch multiple harvester processes, so you don't have to use apache messengers for communication between harvester and workers unless that is needed.

#### MariaDB setup
First you need to make the HARVESTER database and the harvester account on MariaDB. E.g.  

```sh
$ mysql -u root
MariaDB > CREATE DATABASE HARVESTER;
MariaDB > CREATE USER 'harvester'@'localhost' IDENTIFIED BY 'password';
MariaDB > GRANT ALL PRIVILEGES ON HARVESTER.* TO 'harvester'@'localhost';
```

Note that harvester tables are automatically made when the harvester instance gets started,
so you don't have make them by yourself. Make sure that you don't have STRICT_TRANS_TABLES.
```
MariaDB [(none)]> SELECT REPLACE(@@SQL_MODE, ',', '\n');
+--------------------------------+
| REPLACE(@@SQL_MODE, ',', '\n') |
+--------------------------------+
|                                |
+--------------------------------+
1 row in set (0.01 sec)
```

Then edit /etc/my.cnf if need to optimize the database by yourself,
e.g., 

```
[mysqld]
max_allowed_packet=1024M
```

Harvester uses mysql-connector by default to access to MariaDB.

```
$ pip install mysql-connector-python<=8.0.11
```
_(Warning: Is was tested that mysql-connector-python 8.0.12 does not work)_

The following changes are required in panda_harvester.cfg:

```
[db]
# engine sqlite or mariadb
engine = mariadb
# user name
user = harvester
# password
password = FIXME
# schema
schema = HARVESTER 
```
where `engine` should be set to **mariadb** and `password` should be changed accordingly.


If you want to use mysqlclient (whose python module is called MySQLdb) to access to MariaDB instead,
```
$ pip install mysqlclient
```
_(Note: Since mysqlclient requires compilation from MySQL lib, one may need to install additional package in advance: `yum install mysql-devel` or `yum install MariaDB-devel MariaDB-shared`)_

In addition, you need to enable `useMySQLdb` under `[db]` in panda_harvester.cfg :

```
useMySQLdb = True
```





#### uWSGI setup
Another option for multi-processing is uWSGI.

Install uwsgi in the same python environment of harvester:
```sh
$ pip install uwsgi
```

##### How to start/stop harvester

###### With service script

A template of the service script is available at etc/rc.d/init.d/panda_harvester-uwsgi.rpmnew.template for easy start. Copy the template to new file named etc/rc.d/init.d/panda_harvester-uwsgi. In the CONFIGURATION SECTION, `userName`, `groupName`, `VIRTUAL_ENV`, `LOG_DIR` need to be modified at least. Other variables can be modified as well, say `nProcesses` and `nThreads` defines the number of processes and the number of threads in each process.

Also, there is option to run uWSGI with an independent configuration file for more configuration flexibility: One can uncomment the line of `uwsgiConfig` In the CONFIGURATION SECTION and set it to be the path of the uWSGI ini configuration file (filename must end in extension ".ini"). A template of uWSGI ini configuration file is available at etc/panda/panda_harvester-uwsgi.ini.rpmnew.template -- one can copy it to etc/panda/panda_harvester-uwsgi.ini (it should be functional before any modification).

Then, one can use this script to start, stop, or reload harvester:  
```sh
$ etc/rc.d/init.d/panda_harvester-uwsgi start
$ etc/rc.d/init.d/panda_harvester-uwsgi stop
$ etc/rc.d/init.d/panda_harvester-uwsgi reload
```
where reload can be used after harvester code or configurations (e.g. harvester.cfg) change.

###### With systemd service 

(Recommended for el9 or above)

As of v0.3.2, after pip installed harvester, a new configuration template about environment variables is available at etc/sysconfig/panda_harvester_env.systemd.rpmnew (some fields should already be automatically filled during installation). Copy the file etc/sysconfig/panda_harvester_env and edit it if necessary. 

A template of the systemd script is available at etc/systemd/system/panda_harvester-uwsgi.service. Copy the template to a new file named /etc/systemd/system/panda_harvester-uwsgi.service , and run systemd daemon reload:

```
# systemctl daemon-reload
```

And then one can start, stop, restart, or reload (keep the uWSGI master process and restart harvester sub-process) harvester: 

```
# systemctl start panda_harvester-uwsgi.service
# systemctl stop panda_harvester-uwsgi.service
# systemctl restart panda_harvester-uwsgi.service
# systemctl reload panda_harvester-uwsgi.service
```


### Remote configuration files
It is possible to load system and/or queue configuration files via http/https. This is typically useful to have a centralized pool of configuration files, so that it is easy to see with which configuration each harvester instance is running. There are two environment variables *HARVESTER_INSTANCE_CONFIG_URL* and *HARVESTER_QUEUE_CONFIG_URL* to define URLs for system config and queue config files, respectively. If those variable are set, the harvester instance loads config files from those URLs and then overwrites parameters if they are specified in local config files. Sensitive information like database password should be stored only in local config files. System config files are read only when the harvester instance is launched, while queue config files are read every 10 min so that queue configuration can be dynamically changed during the instance is running. Note that remote queue config file is periodically cached in the database by Cacher which automatically gets started when the harvester instance is launched, so you don't have to do anything manually. However, when you edit remote queue config file and then want to run some unit tests which don't run Cacher, you have to manually cache it using cacherTest.py.
```
$ python lib/python*/site-packages/pandaharvester/harvestertest/cacherTest.py
```

----------
