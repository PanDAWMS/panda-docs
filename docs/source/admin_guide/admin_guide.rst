===========================
Administrator Guide
===========================

Here is a a quick setup guide of a minimum PanDA system.

.. contents::
    :local:
    :depth: 1

Hardware requirements
--------------------------------------
It is recommended to install JEDI and the PanDA server on separate virtual machines (VMs), but it is possible to
install them on a single VM for small testing purposes. 3 VMs are required to have a minimum PanDA system;
the first VM for JEDI and the PanDA server, the second VM for Harvester, and the third VM.
The following table shows the minimum hardware configuration.

.. list-table:: Minimum hardware configuration
   :header-rows: 1

   * - Component
     - Cores
     - RAM (GB)
     - Disk (GB)
   * - JEDI + PanDA server
     - 4
     - 8
     - 100
   * - Harvester
     - 4
     - 8
     - 100
   * - BigPandaMon
     - 8
     - 16
     - 70

Setup database
------------------


Install the PanDA server
--------------------------------------

Install JEDI
-----------------