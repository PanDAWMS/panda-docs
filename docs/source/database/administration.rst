=========================
Database Administration
=========================
Oracle and PostgreSQL DB schema
=================================
You can find the database schema within the "schema" folder in the panda-database github module at `<https://github.com/PanDAWMS/panda-database/>`_. For a new database installation, you can execute the sql statements found in the schema folder for either Oracle or PostgreSQL. 

Whenever there is a new version of the PanDA DB schema, the version number needs to increase in order to reflect the change. For PostgreSQL you can find the version number in schema/postgres/version and for Oracle inside the schema/oracle/ATLAS_PANDA.sql file (at the top).

Whenever there is a schema change that increases the version number, a diff file needs to be provided within the "patches" folder for all the schema changes between the previous and current version. At the end of the diff file, we need to also increase the DB schema version number in the pandadb_version table.

When PanDA server and JEDI run, they check if the version in the versioning table is the minimum required for the PanDA server/JEDI to work/fully function with. If the database schema version is lower than the one required, PanDA server/JEDI will exit with the following message: “This version of PanDA Server/JEDI requires DB schema version X.Y.Z. but found Z.Y.X. installed instead. Please run the DB update scripts to install the required version”. 
