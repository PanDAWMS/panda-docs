===================================
Installation
===================================

Requirements
------------

Python: 3.8 or higher
Database backend: SQLite or MySQL/MariaDB
  * SQLite: sqlite3 3.7.0
  * MySQL/MariaDB: MySQL 8 or higher; or MariaDB 10 or higher


Install Harvester
-----------------

Harvester can be installed with or without root privilege


Setup virtual environment
"""""""""""""""""""""""""

.. tabs::

   .. code-tab:: text Python native venv

        $ cd your_installation_directory
        $ python3 -m venv harvester
        $ cd harvester
        $ . bin/activate

   .. code-tab:: text Others

        # For Cori@NERSC
        $ module load python
        $ mkdir harvester
        $ conda create -p ~/harvester python
        $ source activate ~/harvester


Install Harvester package
"""""""""""""""""""""""""""""

.. tabs::

   .. code-tab:: text General

        # upgrade pip
        $ pip install pip --upgrade

        # install Harvester
        $ pip install git+https://github.com/HSF/harvester.git

   .. code-tab:: text ATLAS

        # upgrade pip
        $ pip install pip --upgrade

        # install Harvester
        $ pip install git+https://github.com/HSF/harvester.git
        # For ATLAS GRID instances, install with:
        $ pip install pandaharvester[atlasgrid]@git+https://github.com/HSF/harvester


.. code-block:: text

    # upgrade pip
    $ pip install pip --upgrade

    # install Harvester
    $ pip install git+https://github.com/HSF/harvester.git
    # for ATLAS GRID instance, install with this instead
    # (deprecated)
    $ pip install git+https://github.com/HSF/harvester#egg=pandaharvester[atlasgrid]
    # new syntax
    $ pip install pandaharvester[atlasgrid]@git+https://github.com/HSF/harvester

    # copy sample setup and config files
    $ mv etc/sysconfig/panda_harvester.rpmnew.template  etc/sysconfig/panda_harvester
    $ mv etc/panda/panda_common.cfg.rpmnew etc/panda/panda_common.cfg
    $ mv etc/panda/panda_harvester.cfg.rpmnew.template etc/panda/panda_harvester.cfg


Upgrade Harvester package (if Harvester is already installed)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. tabs::

   .. code-tab:: text General

        $ cd your_installation_directory/harvester
        $ . bin/activate
        # Upgrade all dependencies
        $ pip install --upgrade git+https://github.com/HSF/harvester.git
        # Upgrade harvester package only
        $ pip install --no-deps --force-reinstall git+https://github.com/HSF/harvester.git

   .. code-tab:: text ATLAS

        $ cd your_installation_directory/harvester
        $ . bin/activate
        # Upgrade harvester package only
        $ pip install --no-deps --force-reinstall pandaharvester[atlasgrid]@git+https://github.com/HSF/harvester

