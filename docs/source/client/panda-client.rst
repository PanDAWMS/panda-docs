================
panda-client
================

The panda-client package includes python modules and command-line tools to allow end-users to submit/manage
their analysis on the PanDA system. This package is supposed to be used by end-users as functionality is simplified
and limited. System administrators or developers should refer to :doc:`API reference <rest>`.

Installation
==============
panda-client works either python 2 and 3, and is self-contained so that you don't have to install an external
package or software. In order to install all python modules, command-line tools and configuration files, simply run:

.. prompt:: bash

    pip install panda-client

If you install panda-client in JupyterLab,

.. prompt:: bash

    pip install panda-client[jupyter]

will install extra packages in addition to panda-client.


Setup
==============
The setup file ``panda_setup.(c)sh`` is automatically generated under *$VIRTUAL_ENV/etc/panda* when panda-client
is installed. The file needs to be sourced before using the python modules and command-line tools, in order to setup
the required environment.

.. prompt:: bash

    source $VIRTUAL_ENV/etc/panda/panda_setup.sh

