=====================
Working with iDDS
=====================

`iDDS <https://idds.cern.ch/>`_ is an intelligent data delivery service
orchestrating workflow and data management systems to optimize resource usage in various workflows.
It is possible to use iDDS on top of PanDA as a high-level service to support various advanced workflows,
such as

* Fine-grained data carousel

* Hyperparameter optimization among geographically distributed GPU resources

* Task chaining with directed acyclic graph

You need to configure ``Message Processor`` in JEDI so that iDDS and PanDA can talk through ActiveMQ.
There is a parameter in ``panda_jedi.cfg`` to specify the json configuration file for ``Message Processor``.

.. code-block:: text

    [msgprocessor]

    # json config file of message processors
    configFile = /etc/panda/jedi_msg_proc_config.json

The contents of the json is something like

.. code-block:: text

    {
        "mb_servers": {
            "iDDS_mb": {
                "host_port_list": ["atlas-mb.cern.ch:61013"],
                "use_ssl": false,
                "username": <user_name>,
                "passcode": <password>,
                "verbose": true
            }
        },
        "queues": {
            "idds": {
                "server": "iDDS_mb",
                "destination": "/queue/Consumer.jedi.atlas.idds"
            }
        },
        "processors": {
            "atlas-idds": {
                "enable": true,
                "module": "pandajedi.jedimsgprocessor.atlas_idds_msg_processor",
                "name": "IddsMsgProcPlugin",
                "in_queue": "idds",
                "verbose": true
            }
        }
    }

where you specify the ActiveMQ server, user name, and password to connect to ActiveMQ, queue names,
and plugins to consume messages from iDDS.
There is a separate plugin for each workflow in
`the plugin repository <https://github.com/PanDAWMS/panda-jedi/tree/master/pandajedi/jedimsgprocessor>`_.
You choose appropriate plugins based on your needs.