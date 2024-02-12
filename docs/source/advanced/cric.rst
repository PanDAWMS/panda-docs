======================
Integration with CRIC
======================

The Computing Resource Information System
(`CRIC <https://core-cric-docs.web.cern.ch/core-cric-docs/latest/index.html>`_) is a framework
providing a centralized and flexible way
to describe resources and their usage.

It is possible to integrate PanDA and CRIC so that administrators register various resources in CRIC
by using WebUI and PanDA fetches information from CRIC, avoiding manual registration in the database.
One of the scripts launched by PanDA daemon, ``configurator``, periodically retrieves information from CRIC
and populates database tables. To enable PanDA daemon and ``configurator``, you need in ``panda_server.cfg``

.. code-block:: text

    [daemon]
    # whether to run daemons for PanDA
    enable = True

    config = {
        ...
        "configurator": {
            "enable": true, "module": "configurator", "period": 200, "sync": true},

and set the following parameters:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Example
   * - CRIC_URL_SCHEDCONFIG
     - URL to get schedconfig json
     - https://datalake-cric.cern.ch/api/atlas/pandaqueue/query/?json
   * - CRIC_URL_SITES
     - URL to get site json
     - https://datalake-cric.cern.ch/api/atlas/site/query/?json
   * - CRIC_URL_DDMENDPOINTS
     - URL to get storage json
     - https://datalake-cric.cern.ch/api/atlas/ddmendpoint/query/?json
   * - CRIC_URL_DDMBLACKLIST
     - URL to get blacklist json
     - https://datalake-cric.cern.ch/api/atlas/ddmendpointstatus/query/?json&activity=write_wan&fstate=OFF
   * - CRIC_URL_CM
     - URL to get site matrix json
     - https://atlas-cric.cern.ch/api/core/sitematrix/query/?json&json_pretty=0

If you don't have a real CRIC instance or have a partially functional instance,
you can use local json files to describe resources.
In this case the above parameters take the form of: ``file://<path_to_file>`` instead of ``https://<url>``.
It is possible to use local json files only for some parameters while others are taken from the real CRIC instance.

|br|