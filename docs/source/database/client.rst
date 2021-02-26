========================
Client configuration
========================

DB clients
==============
The connection to the DBs is done through cx_Oracle or mysqlclient packages.
There is a PanDA in-house library for connection pooling.

Configuration
==============

Below is an annotated excerpt of the PanDA configuration file that describes the DB settings.

::

  ##########################
  #
  # Database parameters
  #

  # PanDA server connection pooling
  # The number of connections to the DB **for each server process**
  # If you are using FastCGI or WSGI, only the second value will be used
  nDBConnection = 2
  nDBConForFastCGIWSGI = 1

  # JEDI workers
  nWorkers = 8

  # Timeout configuration
  usedbtimeout = True
  dbtimeout = 300

  # Logging configuration, can generate heavy logs if enabled
  dbbridgeverbose = False
  dump_sql = False

  # Schemas
  schemaPANDA = ATLAS_PANDA
  schemaMETA = ATLAS_PANDAMETA
  schemaGRISLI = ATLAS_GRISLI
  schemaPANDAARCH = ATLAS_PANDAARCH
  schemaJEDI = ATLAS_PANDA
  schemaDEFT = ATLAS_DEFT

  ##########################
  #
  # Oracle specific configuration
  #

  dbhost = <DB HOST>
  dbuser = <DB USER>>
  dbpasswd = <PASSWORD>
  dbname = <DB NAME>>

  ##########################
  #
  # MySQL specific configuration
  #

  # activate MySQL option
  backend = mysql

  # server configuration
  dbhostmysql = <DB HOST>
  dbportmysql = <PORT>
  dbnamemysql = <DB NAME>
  dbusermysql = <DB USER>
  dbpasswdmysql = <PASSWORD>
