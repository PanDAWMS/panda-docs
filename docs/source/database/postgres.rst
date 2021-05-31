===================================================
Exporting Oracle Database Schemas to PostgreSQL
===================================================

PostgreSQL Setup
======================

Information about the yum repository is at `<https://www.postgresql.org/download/linux/redhat/>`_.

Here is an example of PostgreSQL 13 setup on a puppet-managed CC7.

.. prompt:: bash

  yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
  cp /etc/yum.repos.d/pgdg-redhat-all.repo /etc/yum-puppet.repos.d/
  yum install -y postgresql13-server pg_cron_13 pg_partman13 postgresql13-contrib
  /usr/pgsql-13/bin/postgresql-13-setup initdb
  systemctl enable postgresql-13

Edit /var/lib/pgsql/13/data/postgresql.conf

.. code-block:: text

  password_encryption = md5
  listen_addresses = '*'
  # port = 3130
  shared_preload_libraries = 'pg_cron, pg_partman_bgw'
  cron.database_name = 'postgres'
  pg_partman_bgw.dbname = 'panda_db'

Add

.. code-block:: text

  local  all  panda trust
  host   all  panda localhost trust
  local  all  postgres trust
  host   all  postgres localhost trust
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
  \c panda_db;
  CREATE SCHEMA partman;
  CREATE EXTENSION pg_partman SCHEMA partman;

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

The DBA or schema owner account is required to access Oracle since only they can export database objects in the schema.

.. prompt:: bash

  export ORA2PG_PASSWD=<Oracle password>
  ./usr/local/bin/ora2pg -t SHOW_VERSION -u <Oracle schema> -c ora2pg.conf
  ./usr/local/bin/ora2pg -t SHOW_REPORT -u <Oracle schema> --estimate_cost -c ora2pg.conf

|br|

Exporting Schemas
===========================

It is possible to export tables and sequences almost automatically. Procedures need many patches, while
functions are directory created since they are very few.

Tables and Sequences
^^^^^^^^^^^^^^^^^^^^^^

Loop over PANDA, PANDAARCH, and PANDAMETA.

.. prompt:: bash $, auto

    $ # set the core name of the Oracle schema and its password
    $ export PANDA_SCHEMA=<core name of schema>
    $ export ORA2PG_PASSWD=<the password>

    $ # make DLL to create tables and sequences
    $ ./usr/local/bin/ora2pg -t "TABLE SEQUENCE" -u ATLAS_${PANDA_SCHEMA} -n ATLAS_${PANDA_SCHEMA} \
          -N DOMA_${PANDA_SCHEMA} -c ora2pg.conf -o ${PANDA_SCHEMA}.sql

    $ # reset sequence values
    $ mv SEQUENCE_${PANDA_SCHEMA}.sql a.sql
    $ sed -E "s/START +[0-9]+/START 1/" a.sql | sed  -E "s/MINVALUE +([0-9]+)/MINVALUE 1/" \
       > SEQUENCE_${PANDA_SCHEMA}.sql

    $ # create tables
    $ psql -d panda_db -f TABLE_${PANDA_SCHEMA}.sql

    $ # create sequences
    $ psql -d panda_db -f SEQUENCE_${PANDA_SCHEMA}.sql

    $ # delete tables when failed
    $ psql -d panda_db -c \
       "select 'drop table doma_"${PANDA_SCHEMA,,}".' || table_name || ' cascade;'
       FROM information_schema.tables  where table_schema='doma_"${PANDA_SCHEMA,,}"'" \
       | grep drop | psql -d panda_db

    $ # delete sequences when failed
    $ psql -d panda_db -c \
       "select 'drop sequence doma_"${PANDA_SCHEMA,,}".' || sequence_name || ' cascade;'
       FROM information_schema.sequences where sequence_schema='doma_"${PANDA_SCHEMA,,}"'" \
       | grep drop | psql -d panda_db


Note that the DDL script to create the PANDA tables requires small correction.

.. code-block:: text

    652c652
    < CREATE UNIQUE INDEX jedi_job_retry_history_uq ON jedi_job_retry_history (jeditaskid, newpandaid, oldpandaid, originpandaid);
    ---
    > CREATE UNIQUE INDEX jedi_job_retry_history_uq ON jedi_job_retry_history (jeditaskid, newpandaid, oldpandaid, originpandaid, ins_utc_tstamp);
    655c655
    < ALTER TABLE jedi_job_retry_history ADD UNIQUE (jeditaskid,oldpandaid,newpandaid,originpandaid);
    ---
    > ALTER TABLE jedi_job_retry_history ADD UNIQUE (jeditaskid,oldpandaid,newpandaid,originpandaid,ins_utc_tstamp);

Functions
^^^^^^^^^^^^^^^^^^^^^^

For PANDA.

.. prompt:: bash $ auto

   $ psql -d panda_db << EOF

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

.. prompt:: bash $ auto

    $ export ORA2PG_PASSWD=<the password of Oracle PANDA>
    $ export PANDA_SCHEMA=PANDA

    $ # make DLL to create procedures
    $ ./usr/local/bin/ora2pg -t PROCEDURE -u ATLAS_${PANDA_SCHEMA} -n ATLAS_${PANDA_SCHEMA} \
           -N DOMA_${PANDA_SCHEMA} -c ora2pg.conf -o a.sql

    $ # patches
    $ sed -E "s/atlas_(panda[^\.]*)/doma_\L\1/gi" a.sql | sed -E "s/ default [0-9]+\) owner/\) owner/gi" \
       | sed "s/DBMS_APPLICATION_INFO/--DBMS_APPLICATION_INFO/gi" | sed "s/COMMIT;/--COMMIT;/ig" \
       | sed -E "s/MEDIAN\(([^\)]+)\)/PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY \1)/gi" \
       | sed -E "s/(GROUP BY vo, gshare, prodsourcelabel, resource_type,) [^ +]/\1 agg_type/gi" \
       | sed -E "s/(vo, workqueue_id::varchar, prodsourcelabel, resource_type,) [^ +]/\1 agg_type/gi" \
       > PROCEDURE_${PANDA_SCHEMA}.sql

    $ # create procedures
    $ psql -d panda_db -f PROCEDURE_${PANDA_SCHEMA}.sql

    $ # patch for MERGE
    $ psql -d panda_db << EOF

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


BIGPANDAMON
^^^^^^^^^^^^^^^^^


For PANDABIGMON.

.. prompt:: bash $ auto

    $ export ORA2PG_PASSWD=<the password of Oracle PANDABIGMON>
    $ export PANDA_SCHEMA=PANDABIGMON

    $ # make DLL to create procedures
    $ ./usr/local/bin/ora2pg -t "TABLE SEQUENCE FUNCTION TYPE TRIGGER VIEW " -u ATLAS_${PANDA_SCHEMA} -n ATLAS_${PANDA_SCHEMA} \
           -N DOMA_${PANDA_SCHEMA} -c ora2pg.conf -o a.sql

    $ # reset sequence values
    $ sed -E "s/START +[0-9]+/START 1/" SEQUENCE_a.sql | sed  -E "s/MINVALUE +([0-9]+)/MINVALUE 1/" \
       > SEQUENCE_${PANDA_SCHEMA}.sql

    $ # create tables
    $ mv  TABLE_a.sql TABLE_${PANDA_SCHEMA}.sql
    $ psql -d panda_db -f TABLE_${PANDA_SCHEMA}.sql

    $ # create sequences
    $ psql -d panda_db -f SEQUENCE_${PANDA_SCHEMA}.sql

    $ # patch views
    $ sed -E "s/atlas_(panda[^\.]*)/doma_\L\1/gi" VIEW_a.sql | sed "s/@ADCR_ADG//ig" > VIEW_${PANDA_SCHEMA}.sql

    $ # create views
    $ psql -d panda_db -f VIEW_${PANDA_SCHEMA}.sql

    $ # patches types since pandamon_jobpage_* are not correctly exported
    $ grep -v pandamon_jobspage TYPE_a.sql > TYPE_${PANDA_SCHEMA}.sql
    $ echo << EOF >> TYPE_${PANDA_SCHEMA}.sql

    CREATE TYPE pandamon_jobpage_obj AS (
        PANDA_ATTRIBUTE VARCHAR(100),
        ATTR_VALUE VARCHAR(300),
        NUM_OCCURRENCES bigint
    );
    ALTER TYPE pandamon_jobpage_obj OWNER TO panda;

    CREATE TYPE pandamon_jobspage_coll AS (pandamon_jobspage_coll pandamon_jobpage_obj[]);
    ALTER TYPE pandamon_jobspage_coll OWNER TO panda;

    EOF

    $ # create types before triggers, functions, and procedures
    $ psql -d panda_db -f TYPE_${PANDA_SCHEMA}.sql

    $ # create triggers
    $ mv TRIGGER_a.sql TRIGGER_${PANDA_SCHEMA}.sql
    $ psql -d panda_db -f TRIGGER_${PANDA_SCHEMA}.sql

    $ # create functions
    $ sed -E "s/atlas_(panda[^\.]*)/doma_\L\1/gi" FUNCTION_a.sql \
       | awk 'BEGIN{IGNORECASE=1}/ALTER FUNCTION/ {gsub(" default ('\''[^'\'']+'\'')", "", $0); print $0;next}{print $0}' \
       | sed "s/default TO_CHAR(CURRENT_TIMESTAMP,'DD-MM-YYYY HH24:MI:SS.FF TZR') DEFAULT NULL/DEFAULT NULL/" \
       | awk 'BEGIN{IGNORECASE=1}/ALTER FUNCTION/ {gsub(" default [^,)]+","", $0); print $0;next}{print $0}' \
       > FUNCTION_${PANDA_SCHEMA}.sql
    $ psql -d panda_db -f FUNCTION_${PANDA_SCHEMA}.sql

   $ create procedures
   $ sed -E "s/atlas_(panda[^\.]*)/doma_\L\1/gi" PROCEDURE_a.sql | sed "s/ATL DEFAULT NULL/ATL text DEFAULT NULL/" \
      | awk 'BEGIN{IGNORECASE=1}/ALTER PROCEDURE/ {gsub(" default ('\''[^'\'']+'\'')", "", $0); print $0;next}{print $0}' \
      | sed "s/default TO_CHAR(CURRENT_TIMESTAMP,'DD-MM-YYYY HH24:MI:SS.FF TZR') DEFAULT NULL/DEFAULT NULL/" \
      | awk 'BEGIN{IGNORECASE=1}/ALTER PROCEDURE/ {gsub(" default [^,)]+","", $0); print $0;next}{print $0}' \
      | sed "s/(( REQUEST_TOKEN/( REQUEST_TOKEN/" > PROCEDURE_${PANDA_SCHEMA}.sql

DEFT
^^^^^^^^^

.. prompt:: bash $ auto

    $ wget https://raw.githubusercontent.com/PanDAWMS/panda-docs/main/docs/source/database/sql/pg_DEFT_TABLE.sql
    $ psql -d panda_db -f pg_DEFT_TABLE.sql

|br|

Registration of Scheduler Jobs
================================

Aggregation jobs are functional, while backup and deletion jobs to be studied.

.. prompt:: bash $ auto

    $ psql << EOF

    SELECT cron.schedule ('* * * * *', 'call doma_panda.jedi_refr_mintaskids_bystatus()');
    SELECT cron.schedule ('* * * * *', 'call doma_panda.update_jobsdef_stats_by_gshare()');
    SELECT cron.schedule ('* * * * *', 'call doma_panda.update_jobsact_stats_by_gshare()');
    SELECT cron.schedule ('* * * * *', 'call doma_panda.update_jobsactive_stats()');
    SELECT cron.schedule ('* * * * *', 'call doma_panda.update_num_input_data_files()');
    SELECT cron.schedule ('* * * * *', 'call doma_panda.update_total_walltime()');
    SELECT cron.schedule ('* * * * *', 'call doma_panda.update_ups_statss()');
    SELECT cron.schedule ('* * * * *', 'call doma_panda.update_job_stats_hp()');
    UPDATE cron.job SET database='panda_db',username='panda' WHERE command like '%doma_panda.%';
    SELECT cron.schedule ('@daily', $$DELETE FROM cron.job_run_details WHERE end_time < now() – interval '3 days'$$);
    SELECT cron.schedule ('@daily', 'call partman.run_maintenance_proc()');
    UPDATE cron.job SET database='panda_db' WHERE command like '%partman.run_maintenance_proc%';

    EOF

|br|

Partitioning
====================

.. prompt:: bash $ auto

    $ wget https://raw.githubusercontent.com/PanDAWMS/panda-docs/main/docs/source/database/sql/pg_PARTITION.sql
    $ psql -d panda_db -f pg_PANDA_SCHEDULER_JOBS.sql

--------------

|br|
