=========================================
Exporting Database Schemas to PostgreSQL
=========================================

PostgreSQL Setup
======================

Information about the yum repository is at `<https://www.postgresql.org/download/linux/redhat/>`_.

Here is an example of PostgreSQL 13 setup on a puppet-managed CC7.

.. prompt:: bash

  yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
  cp /etc/yum.repos.d/pgdg-redhat-all.repo /etc/yum-puppet.repos.d/
  yum install -y postgresql13-server pg_cron_13
  /usr/pgsql-13/bin/postgresql-13-setup initdb
  systemctl enable postgresql-13

Edit /var/lib/pgsql/13/data/postgresql.conf

.. code-block:: text

  password_encryption = md5
  listen_addresses = '*'
  # port = 3130
  shared_preload_libraries = 'pg_cron'
  cron.database_name = 'postgres'

Add

.. code-block:: text

  local  all  panda trust
  host   all  panda localhost trust
  host   all  all 0.0.0.0/0 md5
  host   all  all ::0/0 md5

to /var/lib/pgsql/13/data/pg_hba.conf.

Start PostgreSQL, make the database and the user, and enable pg_cron.

.. prompt:: bash $ auto

  $ systemctl start postgresql-13
  $ su - postgres
  $ psql << EOF
  CREATE DATABASE panda_db;
  CREATE USER panda PASSWORD 'password'
  ALTER ROLE panda SET search_path = doma_panda,public;
  CREATE EXTENSION pg_cron;
  GRANT USAGE ON SCHEMA cron TO panda;
  EOF

|br|

Setup `ora2pg <https://ora2pg.darold.net/>`_
===============================================

The latest ora2pg is available at `<https://github.com/darold/ora2pg/releases>`_.

.. prompt:: bash

  yum install perl-devel
  yum install perl-DBD-Oracle
  wget https://github.com/darold/ora2pg/archive/refs/tags/v21.1.zip
  unzip v*
  cd ora2pg-*/
  perl Makefile.PL PREFIX=../
  make && make install
  cd ..
  export PERL5LIB=$PWD/ora2pg-21.1/lib

Preparation of Config File
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    # PostgreSQL version
    PG_VERSION      13

    # Oracle database connection
    ORACLE_DSN dbi:Oracle:INT8R

    # Schema
    EXPORT_SCHEMA   1

    # Non-privileged Oracle access
    USER_GRANTS 1
    TRANSACTION READONLY

    # Username in PostgreSQL
    FORCE_OWNER panda

    # Skip foreign keys since in PostgreSQL a foreign key must reference columns that either are a primary key
    # or form a unique constraint, which is not always the case in Oracle
    SKIP fkeys

    # Show progress
    DEBUG 1


Testing
^^^^^^^^^^^^^^^^

.. prompt:: bash

  ./usr/local/bin/ora2pg -t SHOW_VERSION -c ora2pg.conf
  ./usr/local/bin/ora2pg -t SHOW_REPORT --estimate_cost -c ora2pg.conf

|br|

Exporting Schemas
===========================

It is possible to export tables and sequences almost automatically. Procedures need many patches, while
functions need few since their usage is very limited.

Tables and Sequences
^^^^^^^^^^^^^^^^^^^^^^

Loop over PANDA, PANDAARCH, and PANDAMETA.

.. prompt:: bash $, auto

    $# set the password and the core name of the Oracle schema
    $export ORA2PG_PASSWD=<the password>
    $export PANDA_SCHEMA=<core name of schema>

    $# make DLL to create tables and sequences
    $./usr/local/bin/ora2pg -t "TABLE SEQUENCE" -u ATLAS_${PANDA_SCHEMA} -n ATLAS_${PANDA_SCHEMA} \
          -N DOMA_${PANDA_SCHEMA} -c ora2pg.conf -o ${PANDA_SCHEMA}.sql

    $# reset sequence values
    $mv SEQUENCE_${PANDA_SCHEMA}.sql a.sql
    $sed -E "s/START +[0-9]+/START 1/" a.sql | sed  -E "s/MINVALUE +([0-9]+)/MINVALUE 1/" \
      > SEQUENCE_${PANDA_SCHEMA}.sql

    $# create tables
    $qsql -d panda_db -f TABLE_${PANDA_SCHEMA}.sql

    $# create sequences
    $qsql -d panda_db -f SEQUENCE_${PANDA_SCHEMA}.sql

    $# delete tables when failed
    $psql -d panda_db -c \
      "select 'drop table doma_"${PANDA_SCHEMA,,}".' || table_name || ' cascade;'
      FROM information_schema.tables  where table_schema='doma_"${PANDA_SCHEMA,,}"'" \
      | grep drop | psql -d panda_db

    $# delete sequences when failed
    $psql -d panda_db -c \
      "select 'drop sequence doma_"${PANDA_SCHEMA,,}".' || sequence_name || ' cascade;'
      FROM information_schema.sequences where sequence_schema='doma_"${PANDA_SCHEMA,,}"'" \
      | grep drop | psql -d panda_db


Functions
^^^^^^^^^^^^^^^^^^^^^^

Only PANDA.

.. prompt:: bash $ auto

   $psql -d panda_db << EOF
   CREATE OR REPLACE FUNCTION doma_panda.bitor ( P_BITS1 integer, P_BITS2 integer ) RETURNS integer AS \$body$
   BEGIN
         RETURN P_BITS1 | P_BITS2;
   END;
   \$body$
   LANGUAGE PLPGSQL
   ;
   ALTER FUNCTION doma_panda.bitor ( P_BITS1 integer, P_BITS2 integer ) OWNER TO panda;
   EOF


Procedures
^^^^^^^^^^^^^^^^^^

Only PANDA.

.. prompt:: bash $, auto

    $export ORA2PG_PASSWD=<the password of Oracle PANDA>
    $export PANDA_SCHEMA=PANDA

    $# make DLL to create procedures
    $./usr/local/bin/ora2pg -t PROCEDURE -u ATLAS_${PANDA_SCHEMA} -n ATLAS_${PANDA_SCHEMA} \
          -N DOMA_${PANDA_SCHEMA} -c ora2pg.conf -o a.sql

    $# patch for namespace
    $sed -E "s/atlas_panda/doma_panda/i" a.sql | sed -E "s/ default [0-9]+\) owner/\) owner/i" \
      > PROCEDURE_${PANDA_SCHEMA}.sql

    $# create procedures
    $qsql -d panda_db -f PROCEDURE_${PANDA_SCHEMA}.sql

    $# patch for MERGE
    $psql -d panda_db << EOF
    SET search_path = doma_panda,public;
    CREATE OR REPLACE PROCEDURE doma_panda.jedi_refr_mintaskids_bystatus () AS \$body$
    BEGIN

    INSERT INTO JEDI_AUX_STATUS_MINTASKID
    (status, min_jeditaskid)
    SELECT status, MIN(jeditaskid) min_taskid from JEDI_TASKS WHERE status NOT IN ('broken', 'aborted', 'finished', 'failed') GROUP By status
    ON CONFLICT (status)
    DO
      UPDATE SET min_jeditaskid=EXCLUDED.min_jeditaskid;

    END;
    \$body$
    LANGUAGE PLPGSQL
    SECURITY DEFINER
    ;
    ALTER PROCEDURE jedi_refr_mintaskids_bystatus () OWNER TO panda;
    EOF

Schedule Jobs
^^^^^^^^^^^^^^^^^^^

.. prompt:: bash $,>>, auto

  $psql

  >> SELECT cron.schedule ('jedi_refr_mintaskids_bystatus', '* * * * *', 'call doma_panda.jedi_refr_mintaskids_bystatus()');
  >> UPDATE cron.job SET database='panda_db',username='panda' WHERE jobid=<id>;
  >> SELECT * FROM cron.job_run_details;
