=========================================
Exporting Database Schemas to PostgreSQL
=========================================

PostgreSQL Setup
======================

Information about the yum repository is at `<https://www.postgresql.org/download/linux/redhat/>`_.

Here is an example of PostgreSQL setup on a puppet-managed CC7.

.. prompt:: bash

  yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
  cp /etc/yum.repos.d/pgdg-redhat-all.repo /etc/yum-puppet.repos.d/
  yum install -y postgresql13-server
  /usr/pgsql-13/bin/postgresql-13-setup initdb
  systemctl enable postgresql-13

Edit /var/lib/pgsql/13/data/postgresql.conf

.. code-block:: text

  password_encryption = md5
  listen_addresses = '*'
  # port = 3130

Add

.. code-block:: text

  host  all  all 0.0.0.0/0 md5
  host  all  all ::0/0 md5

to /var/lib/pgsql/13/data/pg_hba.conf.

Start PostgreSQL and make the database and the user.

.. prompt:: bash

  systemctl start postgresql-13
  su - postgres
  psql -c "CREATE DATABASE panda_db"
  psql -c "CREATE USER panda PASSWORD 'password'"

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
    ORACLE_USER <user>
    ORACLE_PWD <password>

    # Schema
    EXPORT_SCHEMA   1
    SCHEMA ATLAS_PANDA
    PG_SCHEMA DOMA_PANDA

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

PANDA Schema
^^^^^^^^^^^^^^^^^^^^^^

.. prompt:: bash $ auto

    $ # make DLL to create tables
    $ ./usr/local/bin/ora2pg -t TABLE -c ora2pg.conf -o table.sql

    $ # patch some
    $ patch --dry-run table.sql << 'EOF'
    652c652
    < CREATE UNIQUE INDEX jedi_job_retry_history_uq ON jedi_job_retry_history (jeditaskid, newpandaid, oldpandaid, originpandaid);
    ---
    > CREATE UNIQUE INDEX jedi_job_retry_history_uq ON jedi_job_retry_history (jeditaskid, newpandaid, oldpandaid, originpandaid, ins_utc_tstamp);
    655c655
    < ALTER TABLE jedi_job_retry_history ADD UNIQUE (jeditaskid,oldpandaid,newpandaid,originpandaid);
    ---
    > ALTER TABLE jedi_job_retry_history ADD UNIQUE (jeditaskid,oldpandaid,newpandaid,originpandaid, ins_utc_tstamp);
    EOF

    $ # create tables
    $ qsql -d <database name> -f table.sql

    $ # delete tables when failed
    $ psql -d panda_db -c \
      "select 'drop table doma_panda.' || table_name || ' cascade;' FROM information_schema.tables  where table_schema='doma_panda'" \
      | grep drop | psql -d panda_db

    $ # make DLL to sequences
    $ ./usr/local/bin/ora2pg -t SEQUENCE -c ora2pg.conf -o seq_tmp.sql

    $ # reset values
    $ sed -E "s/START +[0-9]+/START 1/" seq_tmp.sql | sed  -E "s/MINVALUE +([0-9]+)/MINVALUE 1/" > seq.sql

    $ # create sequences
    $ qsql -d <database name> -f seq.sql

    $ # delete sequences when failed
    $ psql -d panda_db -c \
      "select 'drop sequence doma_panda.' || sequence_name || ' cascade;' FROM information_schema.sequences where sequence_schema='doma_panda'" \
      | grep drop | psql -d panda_db