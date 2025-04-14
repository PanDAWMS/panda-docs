================================
PanDA UI Development Guide
================================

--------------------------------
Setting up the project with PyCharm Professional
--------------------------------

.. note:: This guide is for PyCharm Professional only, as it supports remote development.

It is extremely difficult to set up a local instance of the project that is absolutely identical to the production ones working on CERN VMs.
That is why we are using a paradigm of remote development supported by PyCharm.
In this case there are 2 copies of the project, one is local, another is on a remote development machine (aipanda033).
You make changes to the local one, upload changes to the remote one,
then PyCharm runs the project on the remote node and transfers debugging data to the locally running PyCharm.

To be able to do it outside the CERN network we use SSH tunneling through lxplus. Example of such command::

``ssh -N -p 22 -D 1234 <username>@lxplus.cern.ch -L localhost:13322:aipanda033.cern.ch:22 -L localhost:1330X:aipanda033.cern.ch:800X  -L localhost:1330X:aipanda033.cern.ch:800X``

Where ``X`` is any of 1...9 (1, 2, 3, 7 are taken), you may need 2 of them, one for backend and another for frontend.

There is `SSH Tunnel Manager app <https://www.tynsoe.org/stm/>`_ for MacOS, we are using it to establish tunnels.
In the browser you can use a proxy extension (e.g. SwitchyOmega) with a SOCKS4 protocol to ``localhost:1234``.

""""""""""""""""""""""""""""""""
Setting up Django REST framework backend
""""""""""""""""""""""""""""""""

The following instruction is for Linux (or MacOS):

0. Install PyCharm:
   - Pre installation requirements:
     - Open JDK
     - Get PyCharm Professional from official website

1. Creating a project:
   - Run PyCharm
   - Choose 'Check out from repository':
     - Link to repo: ``https://github.com/PanDAWMS/panda-ui.git``
     - Directory: ``/home/<username>/PyCharmProjects/panda-ui``

2. Turn on git support in the created project:
   - **File** → **Settings** → **Version Control**: put the local directory of the project and VCS - Git

3. Then create your dev branch from main branch:
   - Git → Branches → origin/main → checkout as → main
   - Git → New branch → ``<some name>``
   - You should see it on top left, next to the project name

4. Setup mapping:
   - Go to **Tools** → **Deployment** → **Configuration**
   - In the **Connection** tab select a SFTP connection to the dev machine (from ssh tunnel command):
     - SFTP host: ``localhost``
     - Port: ``13322``
     - Root path: path to the project code: ``/data_aipanda163/<username>`` (you may need to create this folder)
   - In the **Mappings** tab:
     - Local path: e.g. ``/home/<username>/PyCharmProjects/panda-ui``
     - Deployment path: ``/PyCharmProjects/panda-ui`` (it is a tail to root path in the connection tab)
   - Check if the mapping really works: try to upload the project code to the remote dev node via **Tools** → **Deployment** → **Upload to**.
You should see the code in your folder.

5. Connect to remote Python interpreter:
   - Go to **File** → **Settings** → **Project**: ``<name>`` → **Project Interpreter**
   - Click on ‘gear’ icon → Add, choose **SSH Interpreter** and **Existing server configuration** (the one already created for mapping)
   - Interpreter: ``/data/venv313/bin/python3.13`` (our python virtualenv with all necessary packages installed)
   - Path mappings: ``/data_aipanda163/<username>/PyCharmProjects/panda-ui``

6. Setup Debugging:
   - Turn on Django support:
     - **File** → **Settings** → **Languages & Frameworks** → **Django**
     - Django project root: full path to the local directory of the project, e.g.: ``/home/<username>/PyCharmProjects/panda-ui``
     - Settings: path to the settings folder of the project: ``backend/rest_api/settings``
     - Manage script: full path to manage.py: ``backend/rest_api/manage.py``
   - Then go to **Run** → **Edit Configurations** and create a Django server configuration:
     - Host: ``aipanda033.cern.ch``
     - Port: ``800X`` (1, 2, 3, 5, and 7 are already taken)
     - Environment:
       - Python interpreter: check if there is the remote one that was created earlier
       - Path mappings: ``/home/<username>/PyCharmProjects/panda-ui=/data_aipanda163/<username>/PyCharmProjects/panda-ui``

7. Setup local logging:
   - Create a folder outside of git repo, e.g. ``/data_aipanda163/<username>/PyCharmProjects/logs/panda-ui/``
   - Make sure that the folder is writable by the user running the Django server (``chmod 777 <folder>``)

8. Setup connection to DB:
   - Copy ``backend/rest_api/settings/.env-config-template`` file and rename the copy to ``.env``.
   - Add all needed configuration to the file, or ask to share the file with you.
   - Upload the changes to the remote dev machine

9. That is it. Now you should be able to run the project and see it in your browser under ``http://aipanda033.cern.ch:<800X>`` (should be the same X as in the ssh tunnel command) with the proxy switched on.

10. To set up Django tests to run unit tests:
    - Run → Edit configurations
    - Click on ``+`` → Select ``Django tests``:
      - Fill target as ``backend/rest_api/`` – where Django will search for tests
      - Select the proper Python interpreter
      - Save & run

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
    - Put your port for runnin frontend in ``frontend/ui/angular.json`` file ``projects.frontend.architect.serve.options.port``. The default port is 8000.
    - Put the port you set for running backend to ``frontend/src/environments/environment.dev.ts`` file ``apiUrl``.
