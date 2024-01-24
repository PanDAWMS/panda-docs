================================
ATLAS PanDA cache instances
================================

Operating systems and python versions
-------------------------------------
PanDA cache is currently running on CentOS7 instances and python3.10.

Nodes
-----

The nodes are `aipanda047` and `aipanda048`.

Installation
------------

The cache is a skimmed PanDA server running just a subset of functionalities. The full installation guide is the same as PanDA server: https://panda-wms.readthedocs.io/en/latest/installation/server.html. The objective of this wiki is just to give an overview of the ATLAS production instances.

Python virtual environment
--------------------------

System env variable: `VIRTUAL_ENV`

Location: `/opt/panda`

.. prompt:: bash

 /opt/panda/bin/python -V

.. code-block:: none

 Python 3.10.7


The PanDA code will be under: `/opt/panda/lib/python3.10/site-packages/pandaserver`

Installing and updating the code
--------------------------------

The first time you install the code, you will want to bring in all `atlasprod` dependencies to install e.g. cx_oracle and the Rucio client:

.. prompt:: bash

 /opt/panda/bin/pip install panda-server[atlasprod]

In order to install just the latest PanDA server code from github:

.. prompt:: bash

 /opt/panda/bin/pip install --no-deps --force-reinstall git+https://github.com/PanDAWMS/panda-server.git

`systemd` service
-----------------

The environment for systemd services has to be passed in a new format. The environment file is `/etc/sysconfig/panda_server_env`.

PanDA cache only runs the httpd service (not the daemons). The service unit file for ATLAS is `/etc/systemd/system/panda.service`

**The very first time after setting up a machine, you need to enable the services.**

.. prompt:: bash

 systemctl enable panda.service


You can start/stop/restart the service like this:

.. prompt:: bash

 systemctl start panda.service
 systemctl stop panda.service
 systemctl restart panda.service

Systemd will not print anything out to the console. Instead you need to query the output by running:

.. prompt:: bash

 systemctl status panda.service

Here you will find information, for example if the DB Schema check was passed.

If there are issues starting the service, you can get additional information using `journalctl`.

.. prompt:: bash

 journalctl -xeu panda.service



