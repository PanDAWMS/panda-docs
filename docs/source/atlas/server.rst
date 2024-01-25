==================================
ATLAS PanDA server instances
==================================

Operating systems and python versions
-------------------------------------
We are currently running ALMA9 instances and python3.11

Puppet prerequisites
--------------------

* Puppet environment: production, Roger
* state: production
* Foreman ALMA9 hostgroup: `vopanda/pandaserver/server_alma9_py3`

Node aliases
------------

Our PanDA server nodes have the aliases `atlas-pandaserver-<2 digit number>.cern.ch`, running from 00 to 08.

Installation
------------

Full installation guide can be found under: https://panda-wms.readthedocs.io/en/latest/installation/server.html. The objective of this wiki is just to give an overview of the ATLAS production instances.

Python virtual environment
-------------------------

System env variable: `VIRTUAL_ENV`

Location: `/opt/panda`

.. prompt:: bash

 /opt/panda/bin/python -V

.. code-block:: none

 Python 3.11.2

The PanDA code will be under: `/opt/panda/lib/python3.11/site-packages/pandaserver`

Installing and updating the code
--------------------------------

The first time you install the code, you will want to bring in all `atlasprod` dependencies to install e.g. cx_oracle and the Rucio client:

.. prompt:: bash

 /opt/panda/bin/pip install panda-server[atlasprod]

In order to install just the latest PanDA server code from github:

.. prompt:: bash

 /opt/panda/bin/pip install --no-deps --force-reinstall git+https://github.com/PanDAWMS/panda-server.git

`systemd` services
------------------

The environment for systemd services has to be passed in a new format. The environment file is `/etc/sysconfig/panda_server_env`.

We have a parent (fake) service for `panda`, and two dependent (real) services `panda_daemon` and `panda_httpd`.

.. prompt:: bash

 ls -lrt /etc/systemd/system/panda*

.. code-block:: none

 -rw-r--r--. 1 root root 320 May 17 12:24 /etc/systemd/system/panda.service
 -rw-r--r--. 1 root root 519 May 17 12:24 /etc/systemd/system/panda_daemon.service
 -rw-r--r--. 1 root root 390 May 17 12:24 /etc/systemd/system/panda_httpd.service

**The very first time after setting up a machine, you need to enable the services.**

.. prompt:: bash

 systemctl enable panda.service
 systemctl enable panda_daemon.service
 systemctl enable panda_httpd.service

You can start/stop the parent service and it should trigger the start/stop of the dependent services.

.. prompt:: bash

 systemctl start panda.service
 systemctl stop panda.service

You can also start/stop the dependent services by themselves.

.. prompt:: bash

 systemctl start panda_httpd.service
 systemctl stop panda_httpd.service

 systemctl start panda_daemon.service
 systemctl stop panda_daemon.service

Systemd will not print anything out to the console. Instead you need to query the output by running:

.. prompt:: bash

 systemctl status panda.service

Here you will find information, for example if the DB Schema check was passed.


The parent service does not give any information about the status of the sub-services. For this you need to query the dependent services directly.

.. prompt:: bash

 systemctl status panda_httpd.service

.. code-block:: none

  ● panda_httpd.service - PanDA server httpd service
      Loaded: loaded (/etc/systemd/system/panda_httpd.service; enabled; vendor preset: disabled)
      Active: active (running) since Wed 2023-05-17 12:45:31 CEST; 35min ago
    Main PID: 1530 (httpd)
      Status: "Total requests: 24631; Idle/Busy workers 94/6;Requests/sec: 11.7; Bytes served/sec: 320KB/sec"
       Tasks: 214 (limit: 91328)
      Memory: 2.6G
         CPU: 16min 15.406s
      CGroup: /system.slice/panda_httpd.service
              ├─ 1530 /usr/sbin/httpd -f /etc/panda/panda_server-httpd.conf -k start -D FOREGROUND
              ├─ 1943 /usr/sbin/httpd -f /etc/panda/panda_server-httpd.conf -k start -D FOREGROUND
...

If there are issues starting the service, you can get additional information using `journalctl`.

.. prompt:: bash

 journalctl -xeu panda_httpd.service


Logs and log rotation
---------------------

Logs are under `/var/log/panda`.

Log rotate running times are now handled by `systemd timers`. You can see the time using this command:

.. prompt:: bash

 systemctl list-timers logrotate

.. code-block:: none

 NEXT                         LEFT     LAST                         PASSED       UNIT            ACTIVATES
 Tue 2023-06-27 09:14:58 CEST 16h left Mon 2023-06-26 16:12:08 CEST 4min 52s ago logrotate.timer logrotate.service

 1 timers listed.
 Pass --all to see loaded but inactive timers, too.

Steps to online new node
------------------------

* Install panda server code through pip
* Start panda server and squid
* Open the ports 25080 (http), 25085 (squid), 25443 (https) (CSOps/CERN Firewall)
* Add to squid config as new peer (CSOps)
* Add to LB of pandaserver.cern.ch (CSOps)
* New nodes have to be registered to the `bigpanda` group host certificate (CSOps and CERN IT)
* Enable the services
