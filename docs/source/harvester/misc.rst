===================================
Miscellaneous
===================================


Special setups for certain HPCs
-------------------------------

**How to setup virtualenv if unavailable by default**

For NERSC

.. code-block:: text

     $ module load python
     $ module load virtualenv


For others

.. code-block:: text

     $ pip install virtualenv --user


or more details in https://virtualenv.pypa.io/en/stable/installation/


**How to install python-daemon on Edison@NERSC**

.. code-block:: text

     $ module load python
     $ cd harvester
     $ . bin/activate
     $ pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org  python-daemon


**How to install rucio-client on Edison@NERSC (Required only if RucioStager is used)**

.. code-block:: text

     $ cd harvester
     $ . bin/activate
     $ pip install rucio-clients
     $ cat etc/rucio.cfg.atlas.client.template | grep -v ca_cert > etc/rucio.cfg
     $ echo "ca_cert = /etc/pki/tls/certs/CERN-bundle.pem" >> etc/rucio.cfg
     $ echo "auth_type = x509_proxy" >> etc/rucio.cfg
     $
     $ # For tests
     $ export X509_USER_PROXY=...
     $ export RUCIO_ACCOUNT=...
     $ rucio ping



Install local panda-harvester package
-------------------------------------

.. code-block:: text

     $ cd panda-harvester
     $ rm -rf dist
     $ python setup.py sdist
     $ pip install dist/pandaharvester-*.tar.gz --upgrade --force-reinstall --no-deps
     $ pip install dist/pandaharvester-*.tar.gz --upgrade



Run harvester with supervisord
------------------------------

It is possible to automatically restart harvester when it died by using [supervisord](http://supervisord.org/) which can be installed via pip.

.. code-block:: text

     $ pip install supervisor

An example of supervisord configuration file is available at etc/panda/panda_supervisord.cfg.
You need to rename it to panda_supervisord.cfg and change logfile, pidfile, and command parameters accordingly.
The command parameter uses the [init.d script](https://github.com/HSF/harvester/wiki/Installation-and-configuration#initd-script). `PROGNAME` in the init.d script needs to be changed to

.. code-block:: text

     PROGNAME='python -u '${SITE_PACKAGES_PATH}'/pandaharvester/harvesterbody/master.py --foreground'

as applications to be run under supervisord must be executed in the foreground, i.e., not be daemonized.

To start supervisord

.. code-block:: text

     $ supervisord -c etc/panda/panda_supervisord.cfg

then harvester is automatically started.

To stop/start harvester

.. code-block:: text

     $ supervisorctl stop panda-harvester
$ supervisorctl start panda-harvester

To stop supervisord

.. code-block:: text

     $ supervisorctl shutdown

Harvester is automatically stopped when supervisord is stopped.


Running harvester with Apache
-----------------------------

There is the option to run harvester with Apache (httpd) service.

**Apache setup**

First, make sure that httpd and mod_wsgi are installed on your node.
An example of the httpd config file is available at etc/panda/panda_harvester-httpd.conf.rpmnew.template
which needs to be renamed to panda_harvester-httpd.conf before being edited. `User` and `Group` need to be modified at least. In the httpd.conf there is a string like

.. code-block:: text

   WSGIDaemonProcess pandahvst_daemon processes=2 threads=2 home=${VIRTUAL_ENV}

which defines the number of processes and the number of threads in each process. Those
numbers may be increased if necessary.

The following changes are required in panda_harvester.cfg:

.. code-block:: text
     [frontend]
     # type
     type = apache

where `type` should be set to **apache**. Note that the port number for apache is defined in
panda_harvester-httpd.conf.

**Start/stop harvester with apache**

Use panda_harvester-apachectl to start or stop harvester. An example of apachectl is available at
etc/rc.d/init.d/panda_harvester-apachectl.rpmnew.template. You need change `VIRTUAL_ENV` in the script and rename it to panda_harvester-apachectl. Then  

.. code-block:: text

     $ etc/rc.d/init.d/panda_harvester-apachectl start
     $ etc/rc.d/init.d/panda_harvester-apachectl stop

**Test Apache messenger**

.. code-block:: text
     $ curl http://localhost:26080/entry -H "Content-Type: application/json" -d '{"methodName":"test", "workerID":123, "data":"none"}'

It will receive a message like 'workerID=123 not found in DB'. 



Using Apache messenger with frontend service
--------------------------------------------

Apache messenger can also work when harvester running with uWSGI. Once can either let uWSGI spawn an http router process, or setup a frontend web/proxy/router service which can speak in uwsgi protocol (e.g. NGiNX, Apache).

First, the following changes are required in panda_harvester.cfg:

.. code-block:: text

     [frontend]
     # type
     type = apache

where `type` should be set to *apache*. uWSGI will load apache messenger application after harvester restart. (Note that the port number here is ineffective in this case.)

Next, if one wants the http router by uWSGI itself, the address setup of `httpRouter` is required in etc/rc.d/init.d/panda_harvester-uwsgi . For example:

.. code-block:: text

     httpRouter="127.0.0.1:25080"

This opens port 25080 on localhost.

.. code-block:: text

     httpRouter=":25080"

This opens port 25080 to everywhere.

Then, stop and start harvester again with this script, and it's done.
(Note that using this script to reload does not work here since its own uwsgi configuration changed.)

On the other hand, if one wants http service opened on additional service, in etc/rc.d/init.d/panda_harvester-uwsgi the `httpRouter` must **not** be set. 
Instead, just configure one's frontend service to proxy or route to the socket uWSGI is running. 
For example, in etc/rc.d/init.d/panda_harvester-uwsgi say there is

.. code-block:: text

     uwsgiSocket="127.0.0.1:3334"

where uWSGI running with localhost:3334 open. 

Say if one has already set up the nginx service and wants a reverse proxy for harvester apache messenger, then just add the following directives in the nginx config

.. code-block:: text

     uwsgi_pass 127.0.0.1:3334;
     include *path_of_uwsgi_params*;

A complete nginx config may look like

.. code-block:: text

     server {
          listen  8000;
          server_name localhost;
          charset utf-8;
          access_log /var/log/nginx/app.net_access.log;
          error_log /var/log/nginx/app.net_error.log;
          location /harvester {
               uwsgi_pass  127.0.0.1:3334;
               include     /opt/app/extras/uwsgi_params;
          }
     }

Then reload nginx service, and it's done.

The test approach is the same as *Test Apache messenger* section above.
