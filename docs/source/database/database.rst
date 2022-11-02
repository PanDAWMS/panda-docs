===================
Database
===================

All operations in PanDA are handled and checkpointed through a central database
that is shared by all the PanDA and JEDI servers. ATLAS operation at scale (O(1M)
jobs per day) is performed using an Oracle backend and several optimizations have been
build over the years. There is also a more limited experience and support
for MySQL/MariaDB. A few PanDA instances are operated by different experiments, but
the scale is several orders of magnitude lower requiring far less optimization. Also
not the full functionalities of PanDA and JEDI are used. Currently PanDA SQL code is
written and tested for the ATLAS Oracle case and is translated to MySQL dialect
through a in-house function. I.e. there is no usage of ORM layers as SQL Alchemy.

You can find more information in the following sections.

.. toctree::
   :maxdepth: 1

   client
   server
   er_diagrams
   partitioning
   archival
   postgres
   administration

