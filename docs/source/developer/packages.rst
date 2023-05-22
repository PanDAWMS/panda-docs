================================
Package Distribution
================================

PanDA packages are automatically built using `hatch <https://hatch.pypa.io/latest/>`_
and gz source distribution files (sdist files) are published to PyPI by GitHub actions
when new release versions are tagged.
Sdist is distributed instead of wheel for most PanDA packages since they need to generate
configuration files and/or executables based on client's environment.
On the other hand, installation of those packages are still done using setup.py by default through pip
to keep backward compatibility with legacy Python or pip without PEP 517 support.
Internally pip invokes "python setup.py install" in this case. This is the reason
why PanDA package repositories have the following structure:

::

    root_dir
    ├── package
    │   ├── hatch_build.py
    │   └── pyproject.toml
    ├── setup.cfg
    ├── setup.py
    └── ...


:green:`pyproject.toml` will move to the root directly and :green:`setup.*` will retire once all clients migrate to
Python 3.7 or higher, so that pip will directly use hatching to install packages.

------

|br|

Installation
^^^^^^^^^^^^^^^^^^^

Installation with pip from PyPI
++++++++++++++++++++++++++++++++++
All PanDA packages are available on PyPI. It is generally enough to install PanDA packages using pip

.. prompt:: bash

  pip install <package_name>


Installation with hatch from source tarball
+++++++++++++++++++++++++++++++++++++++++++++

Source tarballs are available in the :doc:`/developer/repository`.

:green:`hatch_build.py` is included in the ``package`` directory implementing the build hooks to generate
configuration files and/or executables according to client's environment, and add them into wheel.
Eventually pip uses wheel to install the package.
Currently most PanDA end-users and system components are running with Python :raw-html:`&le;` 3.6,
so :green:`pyproject.toml` is not placed in the root direct of the package to prevent pip from using hatch.
Github actions use hatch to build and publish packages since higher version of Python is available there.

If you are using newer Python, download and extract a tarball, then

.. prompt:: bash

  cd root_dir/package
  pip install .


Installation with setup.py from source tarball
++++++++++++++++++++++++++++++++++++++++++++++++

Although :green:`setup.py` is becoming obsolete it is still supported and should be used with old Python.

.. prompt:: bash

  cd root_dir
  python setup.py install

or

.. prompt:: bash

  cd root_dir
  pip install .


------

|br|

panda-client
^^^^^^^^^^^^^^^^^^^

The panda-client package is special in terms of supported Python versions. It needs to support both Python 2.7
and 3.6 for a long period as they are the system Python versions on Scientific Linux CERN 6 and CentOS 7.
Also, it is distributed as a full ``panda-client`` sdist and a lightweight ``panda-client-light`` wheel.
The former is used for end-users and contains configuration files and executables in addition to package
modules, while the latter is used for system components and contains only package modules.
The repository has the following structure:

::

    panda-client
    ├── packages
    │   ├── hatch_build.py
    │   ├── full
    │   │   └── pyproject.toml
    │   └── light
    │       └── pyproject.toml
    ├── setup.cfg
    ├── setup.py
    └── ...


:green:`./packages/full/pyproject.toml` is used by a github action to build and publish sdist files for
``panda-client``, and will move to the root dir once all end-users migrate to Python :raw-html:`&ge;` 3.7.
To install ``panda-client`` from local sources, for old Python :raw-html:`&le;` 3.6

.. prompt:: bash

  python setup.py install

or for newer Python :raw-html:`&ge;` 3.7

.. prompt:: bash

  cd packages/full
  pip install .

On the other hand, green:`./packages/light/pyproject.toml` is used by the same github action to build
and publish wheel files for ``panda-client-light``. So it is enough to do

.. prompt:: bash

  pip install panda-client-light

|br|
