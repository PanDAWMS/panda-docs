==========================================
Instance overview for ATLAS JEDI instances
==========================================

Operating systems and python versions
-------------------------------------
We are currently running ALMA9 instances with python3.11

Node aliases
------------

Our JEDI nodes have the aliases `atlas-jedi-<2 digit number>.cern.ch`, running from 00 to 08.

Installation
------------

Full installation guide can be found under: https://panda-wms.readthedocs.io/en/latest/installation/jedi.html. The objective of this wiki is just to give an overview of the ATLAS production instances.

Python virtual environment
--------------------------

System env variable: `VIRTUAL_ENV`

Location: `/opt/panda`

.. prompt:: bash
 /opt/panda/bin/python -V

.. code-block:: none
 Python 3.11.2

The PanDA code will be under: `/opt/panda/lib/python3.11/site-packages/pandajedi`


Installing and updating the code
--------------------------------

The first time you install the code, you will want to bring in all `atlasprod` dependencies to install e.g. cx_oracle and the Rucio client:

.. prompt:: bash
 /opt/panda/bin/pip install panda-jedi[atlasprod]

In order to install just the latest JEDI code from github:

.. prompt:: bash
 /opt/panda/bin/pip install --no-deps --force-reinstall git+https://github.com/PanDAWMS/panda-jedi.git

`systemd` services
------------------

The environment for systemd services has to be passed in a new format. The environment file is `/etc/sysconfig/panda_jedi_env`.

The systemd service unit file is `/etc/systemd/system/panda_jedi.service`

**The very first time after setting up a machine, you need to enable the services.**
.. prompt:: bash
 systemctl enable panda_jedi.service

You can also start/stop/restart the service like:
.. prompt:: bash
 systemctl start panda_jedi.service
 systemctl stop panda_jedi.service
 systemctl restart panda_jedi.service

Systemd will not print anything out to the console during a start. Instead you need to query the output by running:
.. prompt:: bash
 systemctl status panda_jedi.service

Here you will find information, for example if the DB Schema check was passed.

If there are issues starting the service, you can get additional information using `journalctl`.
.. prompt:: bash
 journalctl -xeu panda_jedi.service

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