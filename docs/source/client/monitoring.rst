===========
Monitoring
===========

PanDA provides advanced Web based monitoring for different groups of PanDA users: scientists, developers, operators,
managers, shifters. Panda monitor can also serve a data source for users scripts and custom automatizing.
In this section we basic information, needed to monitor jobs and tasks submitted into PanDA.

Task monitoring
===============
:ref:`terminology/terminology:Task` is the basic entity creating when a new payload comes to PanDA. There are two views
in the PanDA monitoring for navigation over tasks: Tasks list and a Task view. The former view displays the
selection of tasks:

.. tabs::

   .. tab:: ATLAS PanDA

      `https://bigpanda.cern.ch/tasks/ <https://bigpanda.cern.ch/tasks/>`_
   .. tab:: DOMA PanDA

      `http://panda-doma.cern.ch/tasks/ <http://panda-doma.cern.ch/tasks/>`_
   .. tab:: Arbitary monitoring instance

      `https://<monitoringhost>/tasks/`


There are different parameters could be used together with tasks list to provide narrow selection of tasks:

* **days=<number>**, **hours=<number>** defines the left boundary of the time window used for query.
* **date_from=(2021-02-01T23:30)**, **date_to=(2021-02-03)** defines exact time range for tasks selection
* **endtime_from=()**, **endtime_to=()**, **endtimerange=(2021-02-01T23:30|2021-02-01T23:30)**
* **earlierthan**, **earlierthandays**
* **username=**
* **cloud=**
* **tasktype=prod**
* **limit**
* **display_limit**

* **status=(failed, done, running, )** selects tasks which are in one of the status enlisted
  :ref:`here <terminology/terminology:Task>`.
* **name=(user.kikwok.year2015_test.00310341.physics_Main.r9264_p3083_p4077/, shared_pipecheck_20210220T020538Z\*,)**

.. tabs::

   .. tab:: ATLAS PanDA

      `https://bigpanda.cern.ch/tasks/?days=10 <https://bigpanda.cern.ch/tasks/?days=10>`_
      `https://bigpanda.cern.ch/tasks/?date_from=2021-02-01&date_to=2021-02-03 <https://bigpanda.cern.ch/tasks/?date_from=2021-02-01&date_to=2021-02-03>`_
   .. tab:: DOMA PanDA

      `http://panda-doma.cern.ch/tasks/?days=10 <http://panda-doma.cern.ch/tasks/?days=10>`_
   .. tab:: Arbitary monitoring instance

      `https://<monitoringhost>/tasks/**?days=10**`


