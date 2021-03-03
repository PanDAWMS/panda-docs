===================================
Using Message Processor
===================================

JEDI Message Processor can talk to other systems through message brokers which supports STOMP protocol (e.g. ActiveMQ, RabbitMQ, etc.).


JEDI Configuration
""""""""""""""""""

The ``configFile`` parameter: Specify the path of the json configuration file for ``Message Processor`` . If commented, JEDI Message Processor will be disabled.

.. code-block:: text

    [msgprocessor]

    # json config file of message processors
    configFile = /etc/panda/jedi_msg_proc_config.json


JSON Configuration File
"""""""""""""""""""""""

An example of the JSON content in ``configFile``:

.. code-block:: text

    {
    "mb_servers": {
        "iDDS_mb": {
            "host_port_list": ["some-mb.cern.ch:1234"],
            "use_ssl": false,
            "username": "<username>",
            "passcode": "<passcode>",
            "verbose": true
        },
        "rucio_mb": {
            "host_port_list": ["another-mb.cern.ch:5678"],
            "use_ssl": true,
            "cert_file": "/path/of/cert",
            "key_file": "/path/of/key",
            "vhost": "/"
        }
    },
    "queues": {
        "idds": {
            "server": "iDDS_mb",
            "destination": "/queue/Consumer.jedi.atlas.idds"
        },
        "rucio-events": {
            "server": "rucio_mb",
            "destination": "/queue/Consumer.panda.rucio.events"
        }
    },
    "processors": {
        "atlas-idds": {
            "enable": true,
            "module": "pandajedi.jedimsgprocessor.atlas_idds_msg_processor",
            "name": "AtlasIddsMsgProcPlugin",
            "in_queue": "idds",
            "verbose": true
        },
        "panda-callback": {
            "enable": true,
            "module": "pandajedi.jedimsgprocessor.panda_callback_msg_processor",
            "name": "PandaCallbackMsgProcPlugin",
            "in_queue": "rucio-events"
        }
    }
    }


In the JSON object, the configuration of **message broker servers**, **queues**, and **message processors** are defined.


**Message Broker Servers**

Defined under ``"mb_servers"`` object.
In the ``"mb_servers"`` object, a key can be any arbitrary name standing for the message broker server.
In the example above, there are 2 message broker servers, named "iDDS_mb" and "rucio_mb".

Parameters of a message broker server\:

* ``"host_port_list"``: A list of host\:port of the message broker servers. If multiple host\:port are put in the list, only random one of them will be connected and the others will be failover candidates. Also in host\;port if a hostname is used instead of IP address, all IP addresses mapped to the hostname according to DNS resolution will be connected. Mandatory
* ``"use_ssl"``: STOMP option, whether to use SSL in authentication. Default is false
* ``"username"`` and ``"passcode"``: STOMP option, authenticate the message broker server with username and passcode. Default is null
* ``"cert_file"`` and ``"key_file"``: STOMP option, authenticate the message broker server with key/cert pair. Default is null
* ``"vhost"``: STOMP option, vhost of the message broker. Default is null
* ``"verbose"``: Whether to log verbosely about communication details with this message broker server. Default is false


**Queues**

Defined under ``"queues"`` object.
In the ``"queues"`` object, a key can be any arbitrary name standing for a message queue.
In the example above, there are 2 message queues, named "idds" and "rucio-events".

Parameters of a message queue\:

* ``"server"``: Name of the message broker server defined under ``"mb_servers"`` for this message queue. Mandatory
* ``"destination"``: STOMP option, destination path on the message broker server for this message queue. Mandatory


**Message Processors**

Defined under ``"processors"`` object

In the ``"processors"`` object, a key can be any arbitrary name standing for a message processor.
A message processor running on JEDI consumes a message from a message queue and processes the message (and some message processor sends a new message to another message queue).
There are various message processor plugins for different workflows. All message processors available in JEDI are in the `message processor plugin repository <https://github.com/PanDAWMS/panda-jedi/tree/master/pandajedi/jedimsgprocessor>`_.


Parameters of a message broker server\:

* ``"enable"``: Whether to enable this message processor. Useful when one needs to stop the message processor temporarily but still wants to keep it the configuration file. Default is true
* ``"module"`` and ``"name"``: Module and class name of the message processor plugin in JEDI. Mandatory
* ``"in_queue"``: Queue name defined under ``"queues"`` object, where the message processor consumes messages from this queue. Default is null
* ``"out_queue"``: Queue name defined under ``"queues"`` object, where the message processor sends messages to this queue. Not required if the processor does not send out messages. Default is null
* ``"verbose"``: Whether to log verbosely about this message processor. Default is false

|br|