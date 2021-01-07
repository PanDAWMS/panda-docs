================
panda-client
================

panda-client is a package including python modules and command-line tools to allow end-users to submit/manage
their analysis on the PanDA system. This package is supposed to be used by end-users as functionality is simplified
and limited. System administrators or developers should refer to :doc:`API reference <rest>`.

Installation
==============
panda-client works either python 2 and 3, and is self-contained so that you don't have to install external
package or software. You just do

.. prompt:: bash

    pip install panda-client

so that all python modules, command-line tools, and configuration files are installed properly.

Setup
==============
The setup file ``panda_setup.(c)sh`` is automatically generated under *$VIRTUAL_ENV/etc/panda* when panda-client
is installed. The file needs to be sourced before using python modules and command-line tools.

.. prompt:: bash

    source $VIRTUAL_ENV/etc/panda/panda_setup.sh

