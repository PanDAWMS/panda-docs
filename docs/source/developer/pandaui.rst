================================
PanDA UI Development Guide
================================

--------------------------------
Setting up the project with PyCharm Professional
--------------------------------

.. note:: This guide is for PyCharm Professional only, as it supports remote development.

""""""""""""""""""""""""""""""""
Setting up Django REST framework backend
""""""""""""""""""""""""""""""""

TBF

""""""""""""""""""""""""""""""""
Setting up Angular frontend
""""""""""""""""""""""""""""""""
1. install Node.js on the remote machine

.. code-block:: bash

    # Go to dev node
    ssh <your_username>@lxplus.cern.ch
    ssh aipanda033
    # Download and install nvm:
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
    # in lieu of restarting the shell
    \. "$HOME/.nvm/nvm.sh"
    # Download and install Node.js:
    nvm install 22
    # Verify the Node.js and npm version:
    node -v
    nvm current
    npm -v


2. install all dependencies on the remote machine

.. code-block:: bash

    # Go to the project frontend directory, where package.json is located
    cd frontend/ui
    # Install the dependencies
    npm install
    # optionally you may need to fix the permissions
    chmod -R 755 node_modules


3. set up remote Node.js interpreter in PyCharm
    - Open **Settings** > **Plugin** and make sure the following plugins installed and activated: ``Node.js``, ``TypeScript``, ``Node.js Remote Interpreter``
    - Open **Settings** > **Languages & Frameworks** > **Node.js** and add Remote Node.js Interpreter
    - Choose already existing SSH configuration to dev node
    - Node interpreter: path to node on the remote machine, where Node.js has been installed just before, output of ``which node`` command
    - Package manager: path to npm on the remote machine, output of ``which npm`` command

4. set up remote Node.js run configuration in PyCharm
    - In the PyCharm open **Run** > **Edit Configurations** > **Add New Configuration** > **npm**
    - Package.json: path to package.json on local machine
    - Command: run
    - Script: start
    - Node interpreter: Choose remote Node interpreter we just created
    - Package manager: should be path to npm on the remote machine
    - Mapping: check it is correct, local path to project root should be mapped to remote path to project root
