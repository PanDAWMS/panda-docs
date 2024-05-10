=================
PanDA server
=================

This is the setup guide of the PanDA server.

.. note::

  This is a complete guide. It is recommended to have a look at :doc:`Quick Admin Tutorial </admin_guide/admin_guide>`
  beforehand.

Software requirements
------------------------
The PanDA server requires:

* CentOS 7 or similar Linux distribution
* httpd :raw-html:`&GreaterEqual;` 2.4
* httpd-devel
* python :raw-html:`&GreaterEqual;` 3.6
* pip
* gridsite

Dependent python packages are automatically installed by pip.

---------

|br|

Installation
----------------
It is a good practice to do installation in virtual environment.

.. prompt:: bash

  python3 -m venv <install dir>
  . <install dir>/bin/activate
  pip install -U pip setuptools

Then

.. prompt:: bash

 pip install panda-server[<database type>]

which will install panda-server, panda-common, and dependent python packages. The ``<database type>`` is
oracle, postgres, or mysql depending on your database backend.

If the latest panda-server in the git master repository is required,

.. prompt:: bash

 pip install git+https://github.com/PanDAWMS/panda-server.git

-------------

|br|

Configuration
-----------------


There are two python, one httpd, and one system configuration files under ``${VIRTUAL_ENV}/etc/panda``.

panda_common.cfg
=====================

This configuration file sets various parameters for logging.

.. prompt:: bash

 cd ${VIRTUAL_ENV}/etc/panda
 mv panda_common.cfg.rpmnew panda_common.cfg

The following parameters need to be modified if any.

.. list-table:: panda-common parameters
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - loghost
     - The hostname of PanDA monitor
     - panda.cern.ch
   * - logdir
     - The directory name where common log files are placed
     - /var/log/panda
   * - log_level
     - Logging level
     - DEBUG


panda_server.cfg
=====================

This configuration file sets various parameters of the PanDA server.

.. prompt:: bash

 cd ${VIRTUAL_ENV}/etc/panda
 mv panda_server.cfg.rpmnew panda_server.cfg

The following parameters need to be modified if any.

.. list-table:: panda-server parameters
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - logdir
     - The directory name where server's log files are placed
     - /var/log/panda
   * - dbhost
     - The database hostname
     -
   * - dbuser
     - The database username
     -
   * - dbpasswd
     - The database password
     -
   * - nDBConForFastCGIWSGI
     - The number of database connections in each Web application
     - 1
   * - backend
     - Set mysql to use MySQL database
     - oracle
   * - pserveralias
     - The common name of the http server
     - pandaserver.cern.ch
   * - adder_plugins
     - Adder plugins
     -
   * - setupper_plugins
     - Setupper plugins
     -
   * - token_authType
     - Set to oidc to enable OIDC-based auth
     - x509
   * - auth_config
     - The directory name for OIDC-based auth configuration files
     -
   * - auth_policies
     - The policy file of OIDC-based auth
     -

Parameters of PanDA Daemon are descrribed in :doc:`/advanced/daemon`.


panda_server-httpd.conf
===========================

This configuration file set varous parameters of httpd.

.. prompt:: bash

 cd ${VIRTUAL_ENV}/etc/panda
 mv panda_server-httpd-FastCGI.conf.rpmnew panda_server-httpd.conf

The following parameters need to be modified.
See `Apache doc <https://httpd.apache.org/docs/current/mod/directives.html>`_ for detailed explanation of each
directive.

.. list-table:: httpd parameters
   :header-rows: 1

   * - Name
     - Description
   * - User
     - The userid under which httpd runs
   * - Group
     - The group under which httpd runs
   * - LoadModule wsgi_module
     - The file path of the mod_wsgi module
   * - ServerName
     - The httpd server name
   * - Alias /auth/
     - The directory name for OIDC-based auth configuration files. Must be consistent with panda_server.cfg
   * - WSGIDaemonProcess
     - Config of WSGI daemons. Change ``processes`` and ``home`` if any

Also you need to get/generate host certificate and key files and place them at ``/etc/grid-security/hostcert.pem``
and ``/etc/grid-security/hostkey.pem``, respectively.

The following httpd parameters can be configured dynamically by setting corresponding environment variables
when the service gets started. The default values of those variables are defined in
``${VIRTUAL_ENV}/etc/panda/panda_server.sysconfig``.

.. list-table:: httpd parameters dynamically configurable
   :header-rows: 1

   * - Name
     - Environment variable
     - Default value
   * - PANDA_SERVER_CONF_SERVERNAME
     - The common name of httpd service
     - pandaserver.cern.ch
   * - PANDA_SERVER_CONF_MIN_WORKERS
     - The minimum number of httpd workers
     - 25
   * - PANDA_SERVER_CONF_MAX_WORKERS
     - The maximum number of httpd workers
     - 512
   * - PANDA_SERVER_CONF_NUM_WSGI
     - The number of WSGI deamons
     - 12


sysconfig and environment files for systemd
==============================================

.. prompt:: bash

 mv ${VIRTUAL_ENV}/etc/panda/panda_server.sysconfig_for_systemd /etc/sysconfig/panda_server
 mv ${VIRTUAL_ENV}/etc/panda/panda_server_env.systemd.rpmnew /etc/sysconfig/panda_server_env

.. list-table:: httpd parameters
   :header-rows: 1

   * - Name
     - Description
   * - HOME
     - The non-NFS home directory to run the service
   * - X509_USER_PROXY
     - Proxy file path


------------

|br|

System Setup
-------------------
Then you need to register the PanDA server as a system service, make some directories, and setup log rotation if any.

.. prompt:: bash $, auto

    $ # register the PanDA server in the system
    $ mkdir -p /etc/panda
    $ ln -s ${VIRTUAL_ENV}/etc/panda/*.cfg /etc/panda/
    $ mv ${VIRTUAL_ENV}/etc/idds/idds.cfg.client.template ${VIRTUAL_ENV}/etc/idds/idds.cfg
    $ ln -fs ${VIRTUAL_ENV}/etc/panda/systemd/*.service /etc/systemd/system/
    $ systemctl daemon-reload
    $ systemctl enable panda.service
    $ systemctl enable panda_daemon.service
    $ systemctl enable panda_httpd.service

    $ # make dirs
    $ mkdir -p <logdir in panda_common.cfg>/wsgisocks
    $ chown -R <userid in httpd.conf>:<group in httpd.conf> <logdir in panda_common.cfg>

    $ # setup log rotation if necessary
    $ ln -fs ${VIRTUAL_ENV}/etc/panda/panda_server.logrotate /etc/logrotate.d/panda_server

--------------

|br|

Service Control
----------------------------------

.. prompt:: bash $, auto

 $ # start
 $ systemctl start panda.service

 $ # stop
 $ systemctl stop panda.service

There should be log files in the ``logdir``.
If httpd doesn't get started there could be clues in ``panda_server_error_log``.

----------

|br|

Test
------------

.. prompt:: bash

  curl http://localhost:25080/server/panda/isAlive

It will show the following message if successful.

.. code-block:: text

  alive=yes

If not, see log files under ``logdir``, especially ``panda_server_access_log``, ``panda_server_error_log``,
``panda-Entry.log``, ``panda-DBProxyPool.log``, and ``panda-DBProxy.log`` would help.

|br|

-------------

Deployment with Helm
-----------------------

It is possible to deploy PanDA server instances on Kubernetes cluster using Helm.

.. prompt:: bash

  wget https://github.com/PanDAWMS/helm-k8s/raw/master/panda-server/panda-server-helm.tgz
  tar xvfz panda-server-helm.tgz
  cd panda-server-helm

First, copy your host certificate and key files in the current directory.

.. prompt:: bash

  cp /somewhere/hostcert.pem .
  cp /somewhere/hostkey.pem .

Next, edit ``panda_server_configmap.json`` where each json entry corresponds to the attribute in ``panda_server.cfg``.
For example,

.. code-block:: python

    {
        "server": {
            ...
            "dbuser": "FIXME",

in ``panda_server_configmap.json`` corresponds to

.. code-block:: text

    [server]
    ...
    dbuser = FIXME

in ``panda_server.cfg``.

Finally, you can install the PanDA server.

.. prompt:: bash

  helm install mysrv ./

The service doesn't get started automatically. To start it, set :green:`autoStart` to :hblue:`true` in
`values.yaml` before installing the PanDA server.

.. code-block:: yaml

  autoStart: true

Or

.. prompt:: bash

  helm install mysrv ./ --set autoStart=true

|br|
