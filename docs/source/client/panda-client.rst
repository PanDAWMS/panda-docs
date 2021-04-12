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

The following environment variables need to change if necessary.

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Example
   * - PANDA_URL_SSL
     - Base HTTPS URL of PanDA server
     - https://ai-idds-01.cern.ch:25443/server/panda
   * - PANDA_URL
     - Base HTTP URL of PanDA server
     - http://ai-idds-01.cern.ch:25080/server/panda
   * - PANDA_AUTH_VO
     - Virtual organization name (required only when PANDA_AUTH=oidc)
     - wlcg
   * - PANDA_AUTH
     - Authentication mechanism. oidc to enable OIDC/OAuth2.0. x509_no_grid to use X509 without grid niddleware
     - oidc
   * - PANDA_VERIFY_HOST
     - Set off to disable the host verification
     - off
   * - PANDA_USE_NATIVE_HTTPLIB
     - Set 1 to use native http lib instead of curl
     - 1

|br|
