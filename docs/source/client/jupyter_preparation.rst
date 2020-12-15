===============
Preparation
===============

First, you need Python 3 and JupyterLab.
`Downloading Python <https://wiki.python.org/moin/BeginnersGuide/Download>`_ and
`JupyterLab installation guide <https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html>`_
would help if you have to install them by yourself on your computer.

Here is an example of setup procedures with macOS X Big Sur, Python 3.9, venv, JupyterLab, and pip.

#. Download macOS 64-bit installer from `python 3.9.0 download page <https://www.python.org/downloads/release/python-390/>`_ and double-click the pkg file.

#. In Finder, go to Applications &rarr; Python 3.9 and double-click `Install Certificates.command` to install trusted root certificates.

#. Open a Terminal and make a virtual environment.

.. prompt:: bash

    python3 -m venv ~/mywork
    cd ~/mywork
    . bin/activate

4. Install JupyterLab via pip.

.. prompt:: bash

    pip install jupyterlab


5. Start JupyterLab in a subdirectory.

.. prompt:: bash

    mkdir jupyter_home
    cd jupyter_home
    jupyter lab

JupyterLab will open automatically in your browser.
You may access JupyterLab by entering the local notebook server’s `URL <http://localhost:8888/lab>`_ into the browser.

You should do hereafter all procedures in Jupyter notebook.