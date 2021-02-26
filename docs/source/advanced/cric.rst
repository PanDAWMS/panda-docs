======================
Integration with CRIC
======================

The Computing Resource Information System
(`CRIC <https://core-cric-docs.web.cern.ch/core-cric-docs/latest/index.html>`_) is a framework
providing a centralized and flexible way
to describe resources and their usage.

It is possible to integrate PanDA and CRIC so that administrators registers various resources in CRIC
by using WebUI and PanDA fetches information from CRIC, to avoid manual registration in the database.
One of scripts launched by PanDA daemon, ``configurator``, periodically retrieves information from CRIC
and populate database tables. To enable PanDA daemon and ``configurator``, you need in ``panda_server.cfg``

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

|br|