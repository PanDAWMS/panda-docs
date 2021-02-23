=================
PanDA server
=================

Here is the setup guide of the PanDA server.

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

.. prompt:: bash

 pip install panda-server

which will install panda-server, panda-common, and dependent python packages.

-------------

|br|

Configuration
-----------------


There are two python and one httpd configuration files under ``${VIRTUAL_ENV}/etc/panda``.

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
 mv server.cfg.rpmnew server.cfg

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

------------

|br|

System Setup
-------------------
Then you need to register the PanDA server as a system service, make some directories, and setup log rotation if any.

.. prompt:: bash

 # register the PanDA server
 ln -fs ${VIRTUAL_ENV}/etc/panda/panda_server.sysconfig /etc/sysconfig/panda_server
 ln -fs ${VIRTUAL_ENV}/etc/init.d/panda_server /etc/rc.d/init.d/httpd-pandasrv
 /sbin/chkconfig --add httpd-pandasrv
 /sbin/chkconfig httpd-pandasrv on

 # make dirs
 mkdir -p <logdir in panda_common.cfg>/wsgisocks
 chown -R <userid in httpd.conf>:<group in httpd.conf> <logdir in panda_common.cfg>

 # setup log rotation if necessary
 ln -fs ${VIRTUAL_ENV}/etc/panda/panda_server.logrotate /etc/logrotate.d/panda_server

--------------

|br|

Start and Stop the PanDA server
----------------------------------

.. prompt:: bash

 # start
 /sbin/service httpd-pandasrv start

 # stop
 /sbin/service httpd-pandasrv stop

There should be log files in the ``logdir``.
If httpd doesn't get started there could be clues in ``panda_server_error_log``.

|br|