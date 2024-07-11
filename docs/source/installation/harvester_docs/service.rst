=========================================
Starting and Stopping Harvester Service
=========================================

*This documentation is for Harvester v0.5.0 or above*

The following contents cover how to manage the service running Harvester with uWSGI (the most common approach to run Harvester)


|br|

.. _ref-service-systemd:

With systemd service 
--------------------

(Recommended for OS el9 or above)

As of v0.3.2, after pip installed harvester, a new configuration template about environment variables is available at `${VIRTUAL_ENV}/etc/sysconfig/panda_harvester_env.systemd.rpmnew` (some fields should already be automatically filled during installation).
Similarly, the uWSGI configuration template is available at  `${VIRTUAL_ENV}/etc/panda/panda_harvester-uwsgi.ini.rpmnew`.

Copy both template files to the specific paths `${VIRTUAL_ENV}/etc/sysconfig/panda_harvester_env` and `${VIRTUAL_ENV}/etc/panda/panda_harvester-uwsgi.ini` respectively. 
Edit the new files if necessary. 

.. code-block:: text

    # cd ${VIRTUAL_ENV}
    # cp etc/sysconfig/panda_harvester_env.systemd.rpmnew etc/sysconfig/panda_harvester_env
    # cp etc/panda/panda_harvester-uwsgi.ini.rpmnew etc/panda/panda_harvester-uwsgi.ini

Usually, the uWSGI configuration file `${VIRTUAL_ENV}/etc/panda/panda_harvester-uwsgi.ini` should be good to run before any change.
If one wants to modify the uWSGI configuration file, check `uWSGI docs <https://uwsgi-docs.readthedocs.io/en/latest/Options.html>`_ for more details.



A template of the systemd script is available at `${VIRTUAL_ENV}/etc/systemd/system/panda_harvester-uwsgi.service` . 
Copy the template to a new file named `/etc/systemd/system/panda_harvester-uwsgi.service` , edit the new file if necessary, and run systemd daemon-reload:

.. code-block:: text

    # cp ${VIRTUAL_ENV}/etc/systemd/system/panda_harvester-uwsgi.service /etc/systemd/system/panda_harvester-uwsgi.service

    # systemctl daemon-reload





And then, one can start, stop, restart, or reload harvester: 

.. code-block:: text

    # systemctl start panda_harvester-uwsgi.service
    # systemctl stop panda_harvester-uwsgi.service
    # systemctl restart panda_harvester-uwsgi.service
    # systemctl reload panda_harvester-uwsgi.service


where\:

* ``start``: start Harvester service - The master uWSGI process starts, and it spawns sub-processes (uWSGI workers, which run Harvester)
* ``stop``: stop Harvester service - Terminates all uWSGI processes (master and sub-)
* ``restart``: equivalent to stop and then start
* ``reload``: run uWSGI reload - The master uWSGI process remains alive, terminates all sub-processes and then re-spawns new ones. In most cases, reload can do the same work as restart


|br|

With service script
-------------------

(Only recommended when systemd service is not available. E.g. in a container)

After the installation of Harvester, a template of service script is available at `${VIRTUAL_ENV}/etc/rc.d/init.d/panda_harvester-uwsgi.rpmnew.template` for easy start. 
Copy the template to new file named `${VIRTUAL_ENV}/etc/rc.d/init.d/panda_harvester-uwsgi` , and then edit the new file.

In the CONFIGURATION SECTION, `userName`, `groupName`, `VIRTUAL_ENV`, `LOG_DIR` need to be modified at least. 
Other variables can be modified as well, say `nProcesses` and `nThreads` defines the number of processes and the number of threads in each process.

Also, there is option to run uWSGI with an independent configuration file for more configuration flexibility: 
One can uncomment the line of `uwsgiConfig` In the CONFIGURATION SECTION and set it to be the path of the uWSGI ini configuration file (filename must end in extension ".ini"). 
A template of uWSGI ini configuration file is available at `${VIRTUAL_ENV}/etc/panda/panda_harvester-uwsgi.ini.rpmnew` -- one can copy it to `${VIRTUAL_ENV}/etc/panda/panda_harvester-uwsgi.ini` (it should be functional before any modification).

Then, one can use this script to start, stop, or reload harvester:  

.. code-block:: text

    $ etc/rc.d/init.d/panda_harvester-uwsgi start
    $ etc/rc.d/init.d/panda_harvester-uwsgi stop
    $ etc/rc.d/init.d/panda_harvester-uwsgi reload

where reload can be used after harvester code or configurations (e.g. harvester.cfg) change.
