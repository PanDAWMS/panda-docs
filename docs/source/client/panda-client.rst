================
panda-client
================

The panda-client package includes python modules and command-line tools to allow end-users to submit/manage
their analysis on the PanDA system. This package is supposed to be used by end-users as functionality is simplified
and limited. System administrators or developers should refer to :doc:`API reference <rest>`.

Installation
==============
panda-client works either python 2 and 3, and is self-contained so that you don't have to install an external
package or software. The installation step can be skipped if panda-client has been centrally installed like ATLAS.
Otherwise, simply run the following pip command in a virtual environment to install all python modules,
command-line tools and configuration files:

.. prompt:: bash

    pip install panda-client

If you install panda-client in JupyterLab,

.. prompt:: bash

    pip install panda-client[jupyter]

will install extra packages in addition to panda-client.

If you want to install panda-client to a non-standard location, get the tarball from
https://github.com/PanDAWMS/panda-client/releases

.. prompt:: bash

    wget https://github.com/PanDAWMS/panda-client/archive/refs/tags/x.y.z.tar.gz
    tar xvfz *.tar.gz
    rm *.tar.gz
    cd panda_client*

and then

.. tabs::

   .. tab:: Python 3.7 or higher with new pip supporting PEP517

     .. prompt:: bash

        cd packages/full
        export PANDA_INSTALL_TARGET=<where to be installed>
        pip install . --target ${PANDA_INSTALL_TARGET}

   .. tab:: legacy Python or pip

     .. prompt:: bash

        python setup.py install --prefix=<where to be installed>


Setup
==============
When panda-client is installed to a standard location via pip,
the setup file ``panda_setup.(c)sh`` is automatically generated under the directory shown by the following command:

.. prompt:: bash

    python -c "import sys; print(sys.prefix+'/etc/panda')"


You need to source the file to setup the required environment variables before using the
python modules and command-line tools. It is good to define a shell function to source the setup file as shown
in the ATLAS users tag.

.. tabs::

   .. tab:: pip-installed

     .. prompt:: bash

       source `python -c "import sys; print(sys.prefix)"`/etc/panda/panda_setup.sh

     Replace *`python ...`* properly if you install panda-client to a non-standard location.

   .. code-tab:: bash ATLAS users

       export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
       setupATLAS
       lsetup panda


The following environment variables need to change if necessary.

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Example
   * - PANDA_URL_SSL
     - Base HTTPS URL of PanDA server
     - https://pandaserver-doma.cern.ch/server/panda
   * - PANDA_URL
     - Base HTTP URL of PanDA server
     - http://pandaserver-doma.cern.ch:25080/server/panda
   * - PANDAMON_URL
     - URL of PanDA monitor
     - https://panda-doma.cern.ch
   * - PANDACACHE_URL
     - Base URL of PanDA sandbox server
     - https://pandaserver-doma.cern.ch/server/panda
   * - PANDA_AUTH
     - Authentication mechanism. oidc to enable OIDC/OAuth2.0. x509_no_grid to use X509 without grid niddleware
     - oidc
   * - PANDA_AUTH_VO
     - Virtual organization name (required only when PANDA_AUTH=oidc)
     - wlcg
   * - PANDA_VERIFY_HOST
     - Set off to disable the host verification
     - off
   * - PANDA_USE_NATIVE_HTTPLIB
     - Set 1 to use native http lib instead of curl
     - 1
   * - X509_USER_PROXY
     - Grid proxy file path (required only when PANDA_AUTH = x509_no_grid)
     - /tmp/x509up_u`id -u`
   * - PANDA_NICKNAME
     - Grid nickname (required only when PANDA_AUTH = x509_no_grid)
     - my_nickname

.. tabs::

   .. code-tab:: bash DOMA users

      export PANDA_URL_SSL=https://pandaserver-doma.cern.ch/server/panda
      export PANDA_URL=http://pandaserver-doma.cern.ch:25080/server/panda
      export PANDACACHE_URL=https://pandaserver-doma.cern.ch/server/panda
      export PANDAMON_URL=https://panda-doma.cern.ch
      export PANDA_AUTH=oidc
      export PANDA_AUTH_VO=<your organization>
      export PANDA_USE_NATIVE_HTTPLIB=1

   .. code-tab:: bash ATLAS users

      export PANDA_AUTH=oidc
      export PANDA_AUTH_VO=atlas
      export PANDA_USE_NATIVE_HTTPLIB=1

|br|
