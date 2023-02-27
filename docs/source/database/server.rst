=============================
Database server requirements
=============================

DB node specifications
============================
The database server needs to be hosted on a server that is powerful enough
to sustain the scale of the experiment's operations. One important metric that
will dictate the specifications of the DB node is the number of daily
jobs that an experiment is running. Each job requires one entry in the jobs table
and will also have entries in multiple auxiliary tables (files, metadata).

Below are the specifications for the DB node used in the ATLAS experiment.

CPU and memory
-----------------
The current database server (since June 2021) has 768 GB memory and 2 x ``Intel Xeon Silver 4216 CPU @ 2.10GHz (16 cores)``.
The large memory is important so that the active tables are kept in memory and I/O is avoided.

This setup is preferred to a RAC environment with multiple smaller nodes with less memory. It is also important not to share
the node with other applications to avoid them overwriting each other's memory.

Storage
------------
The active database is currently occupying 40 TB of storage. Only a fraction of tables (job and file) are archived.
For other tables the active database contains the full history. This storage should be performant for fast data access.
The archive database is currently occupying 30 TB archive and is storing 10 years of jobs. These tables
are rarely/never accessed, but kept in case there would be an exceptional case to investigate.

Database service
================
In the case of ATLAS the database service is provided by the CERN IT Oracle DB team
and they ensure high availability of the service:
- The node is part of a RAC cluster. During normal operation, the applications are split across the nodes. I.e. there is one node for PanDA, one node for Rucio (data management) and one node for monitoring. Only if one of the nodes would fail, the applications would fail over to the other nodes.
- The nodes are replicated through Active Data Guard. The secondary nodes are not used by the applications. Sparsely, some people use the Active Data Guard instance for data analytics.
