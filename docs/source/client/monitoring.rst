=================
PanDA Monitoring
=================

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
   .. tab:: Arbitrary monitoring instance

      `https://<monitoringhost>/tasks/`


There are different parameters could be used together with tasks list to provide narrow selection of tasks:

* **days=<number>**, **hours=<number>** defines the left boundary of the time window used for the query. Right boundary
  is the current time.
* **date_from=<YYYY-MM-DDThh:mm or YYYY-MM-DD>**, **date_to=(YYYY-MM-DDThh:mm or YYYY-MM-DD)** defines exact time range of modification time for
  tasks selection
* **endtime_from=<YYYY-MM-DDThh:mm or YYYY-MM-DD>**, **endtime_to=<YYYY-MM-DDThh:mm or YYYY-MM-DD>**,
  **endtimerange=<YYYY-MM-DDThh:mm|YYYY-MM-DDThh:mm>** defines time boundaries for task end time.
* **earlierthan=<number>**, **earlierthandays=<number>** defines the right boundary in hours or days of the time window of tasks selection
  relative to the current time.
* **username=<string>** selects tasks by user name of a person who submitted them. This parameter supports asterisks,
  e.g. **username=James\***.
* **tasktype=<prod, anal>** filters tasks by the payload origin - production or analysis.
* **limit=<number>** limits the size of the data to be retrieved from the PanDA database in order to serve the
  current query. This parameter could require some big value (e.g. 100000) in order to deliver more data. By default this
  value is limited to 20000.
* **display_limit=<number>** number of tasks with extended information provided to the query results.
* **status=<failed, done, running, >** selects tasks which are in one of the status enlisted
  :ref:`here <terminology/terminology:Task>`.
* **taskname=<string>** filters tasks by its name. This parameter supports asterisks,
  e.g. **taskname=shared_pipecheck_20210301T161238Z\***.

Here are few examples of such queries:

.. tabs::

   .. tab:: ATLAS PanDA

      `https://bigpanda.cern.ch/tasks/?display_limit=100 <https://bigpanda.cern.ch/tasks/?display_limit=100>`_

      `https://bigpanda.cern.ch/tasks/?date_from=2021-02-01&date_to=2021-02-03&limit=1000 <https://bigpanda.cern.ch/tasks/?date_from=2021-02-01&date_to=2021-02-03&limit=1000>`_

   .. tab:: DOMA PanDA

      `http://panda-doma.cern.ch/tasks/?display_limit=100 <http://panda-doma.cern.ch/tasks/?display_limit=100>`_

      `https://panda-doma.cern.ch/tasks/?days=120&taskname=shared_pipecheck_20210301T161238Z* <http://panda-doma.cern.ch/tasks/?days=120&taskname=shared_pipecheck_20210301T161238Z*>`_

   .. tab:: Arbitrary monitoring instance

      https://<monitoringhost>/tasks/?<task_filter_parameters>


An individual task is accessible by its ID:

.. tabs::

   .. tab:: ATLAS PanDA

      `https://bigpanda.cern.ch/task/24559935/ <https://bigpanda.cern.ch/task/24559935/>`_

   .. tab:: DOMA PanDA

      `https://panda-doma.cern.ch/task/909/ <https://panda-doma.cern.ch/task/909/>`_

   .. tab:: Arbitrary monitoring instance

      https://<monitoringhost>/task/?<task_id>


Jobs monitoring
===============
Task view provides links to associated jobs in the "Job status summary" table. However jobs could be also accessed
independently to the task view. Jobs list query parameters are the similar to ones as for the tasks list:

.. tabs::

   .. tab:: ATLAS PanDA

      `https://bigpanda.cern.ch/jobs/?jobstatus=finished <https://bigpanda.cern.ch/jobs/?jobstatus=finished>`_

      `https://bigpanda.cern.ch/jobs/?jobstatus=failed&endtimerange=2021-03-15T10:00|2021-03-15T10:30
      <https://bigpanda.cern.ch/jobs/?jobstatus=failed&endtimerange=2021-03-15T10:00|2021-03-15T10:30>`_

      `https://bigpanda.cern.ch/jobs/?jobstatus=failed&date_from=2021-03-15T10:00&date_to=2021-03-15T10:30
      <https://bigpanda.cern.ch/jobs/?jobstatus=failed&date_from=2021-03-15T10:00&date_to=2021-03-15T10:30>`_

   .. tab:: DOMA PanDA

      `https://panda-doma.cern.ch/jobs/?jobstatus=finished <https://panda-doma.cern.ch/jobs/?jobstatus=finished>`_

      `https://panda-doma.cern.ch/jobs/?jobstatus=failed&endtimerange=2021-03-15T10:00|2021-03-15T10:30
      <https://bigpanda.cern.ch/jobs/?jobstatus=failed&endtimerange=2021-03-15T10:00|2021-03-15T10:30>`_

      `https://panda-doma.cern.ch/jobs/?jobstatus=failed&date_from=2021-03-15T10:00&date_to=2021-03-15T10:30
      <https://panda-doma.cern.ch/jobs/?jobstatus=failed&date_from=2021-03-15T10:00&date_to=2021-03-15T10:30>`_

   .. tab:: Arbitrary monitoring instance

      https://<monitoringhost>/jobs/?<jobs_filter_parameters>


An individual job is accessible by its ID:

.. tabs::

   .. tab:: ATLAS PanDA

      `https://bigpanda.cern.ch/job?pandaid=5000107972 <https://bigpanda.cern.ch/job?pandaid=5000107972>`_

   .. tab:: DOMA PanDA

      `https://panda-doma.cern.ch/job?pandaid=253627 <https://panda-doma.cern.ch/job?pandaid=253627>`_

   .. tab:: Arbitrary monitoring instance

      `<https://\<monitoringhost\>/job?pandaid=\<panda_id\>>`_



Retrieving job log
==================
PanDA monitoring provides access to logs generated by a payload or/and correspondent Pilot:

.. tabs::

   .. tab:: ATLAS PanDA

      .. figure:: images/logs_bigpanda.png

   .. tab:: DOMA PanDA

      .. figure:: images/logs_doma.png

Logs become available when a job in the final state.


Information retrieval
=====================

PanDA monitoring can be used as a data source for your scripts and applications. Every page in the web
interface is also available as an API endpoint that returns JSON. To get JSON, either add the ``json``
flag to the query, e.g. `https://bigpanda.cern.ch/task/24559935/?json <https://bigpanda.cern.ch/task/24559935/?json>`_,
or send an ``Accept: application/json`` header.

.. important::

   Do not scrape the HTML pages. If you can't find the data you need through the API, ask how to get it.

Authentication
--------------

There are two ways to authenticate API requests.

Option 1: Personal API token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use this for your own Python scripts, command-line clients, or developer tools that call the API directly.

1. Log in and open your **Profile** page (click your name in the top-right corner, then **Profile**).
2. Your token is in the table on that page. It expires after a limited time. If you need a token that
   lasts longer, use a `CERN service account <https://auth.docs.cern.ch/user-documentation/account-lifecycle/#service-accounts>`_
   or Option 2.
3. Put the token in the ``Authorization`` header, prefixed with ``Token``:

.. code-block:: bash

   curl -X GET https://bigpanda.cern.ch/api/auth_test/ \
        -H "Authorization: Token a1b2c3d4e5f6a8b9c1" \
        -H "Accept: application/json"

Option 2: IAM-issued tokens
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This uses short-lived tokens from your local OIDC agent. It works best when your scripts run on the same
machine as the OIDC agent. Then the script can ask the agent for a fresh token whenever it needs one, so
you don't have to copy tokens around or keep track of when they expire. If your scripts run somewhere
else (a batch node, a server, a CI job), use Option 1 or a service account.

1. Set up the OIDC agent with device flow by following the
   `ATLAS IAM documentation <https://atlas-computing.docs.cern.ch/operations/IAM/index.html#oidc-agent>`_.
2. Generate a token with the ``openid``, ``profile`` and ``wlcg`` scopes:

   .. code-block:: bash

      oidc-token --scope="openid profile wlcg" YOUR-USER-DEVICE-FLOW-CLIENT

3. Put the token in the ``Authorization`` header as a ``Bearer`` token:

.. code-block:: bash

   curl -X GET https://bigpanda.cern.ch/api/auth_test/ \
        -H "Authorization: Bearer $(oidc-token --scope='openid profile wlcg' YOUR-USER-DEVICE-FLOW-CLIENT)" \
        -H "Accept: application/json"

Python example
--------------

.. code-block:: python

   import requests

   url = "https://bigpanda.cern.ch/api/auth_test/"  # replace with the endpoint you need

   # Option 1: personal API token
   api_token = "a1b2c3d4e5f6a8b9c1"  # replace with your token
   headers = {
       "Authorization": f"Token {api_token}",
       "Accept": "application/json",
   }
   response = requests.get(url, headers=headers)
   print("Status:", response.status_code)
   print("Response:", response.json())

   # Option 2: IAM-issued token, fetched from the local OIDC agent
   import requests
   import subprocess

   bearer_token = subprocess.run(
       ["oidc-token", "--scope=openid profile wlcg", "YOUR-USER-DEVICE-FLOW-CLIENT"],
       capture_output=True, text=True, check=True,
   ).stdout.strip()
   headers = {
       "Authorization": f"Bearer {bearer_token}",
       "Accept": "application/json",
   }
   response = requests.get(url, headers=headers)
   print("Status:", response.status_code)
   print("Response:", response.json())

.. tip::

   Use ``/api/auth_test/`` to check that your token works before you call other endpoints.