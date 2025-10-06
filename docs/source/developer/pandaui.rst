================================
PanDA UI Development Guide
================================

------------------------------------------------
Setting up the project with PyCharm Professional
------------------------------------------------

.. note:: This guide is for PyCharm Professional only, as it supports remote development.

It is extremely difficult to set up a local instance of the project that is absolutely identical to the production ones working on CERN VMs.
That is why we are using a paradigm of remote development supported by PyCharm.
In this case there are 2 copies of the project, one is local, another is on a remote development machine (aipanda033).
You make changes to the local one, upload changes to the remote one,
then PyCharm runs the project on the remote node and transfers debugging data to the locally running PyCharm.

To be able to do it outside the CERN network we use SSH tunneling through lxplus. Example of such command:

.. code-block:: bash

    ssh -N -p 22 -D 1234 <username>@lxplus.cern.ch -L localhost:13322:aipanda033.cern.ch:22 -L localhost:1330X:aipanda033.cern.ch:800X  -L localhost:1330X:aipanda033.cern.ch:800X

where ``X`` is any of ``1...9`` (1, 2, 3, 7 are taken), you may need 2 of them, one for backend and another for frontend.

There is `SSH Tunnel Manager app <https://www.tynsoe.org/stm/>`_ for MacOS, we are using it to create and use tunnels.

In the browser you can use a proxy extension (e.g. SwitchyOmega) with a SOCKS5 protocol to ``localhost:1234``.

""""""""""""""""""""""""""""""""""""""""
Setting up Django REST framework backend
""""""""""""""""""""""""""""""""""""""""

.. note:: The following instruction is for MacOS and PyCharm Professional 2025.2.2. In newer or older versions of PyCharm the UI may differ.

0. Install PyCharm:
________________________________

Pre installation requirements:

 * Open JDK
 * Get PyCharm Professional from official website

1. Creating a project:
________________________________

Open PyCharm and choose **Clone repository** in the welcome screen. Fill in the fields:

 * Link to repo: ``https://github.com/PanDAWMS/panda-ui.git``
 * Local directory: ``/Users/<username>/PyCharmProjects/panda-ui`` (or any other you like)

It can ask if you trust the project, say yes

2. Turn on git support and create your dev branch:
______________________________________________

Go to: **PyCharm** → **Settings** → **Version Control**:
 * in **Directory mapping** make sure you have at least your local directory of the project and VCS - Git
 * in **Git** make sure the path to git executable is correct (``which git`` command in terminal can help you to find it)
 * in **GitHub** add your GitHub account (you may need to create a token in GitHub and use it as a password)

Checkout main branch: **Git** → **Branches** → **Remote branches** -> **origin/main** → **checkout** → **main**

Create your own dev branch: **Git** → **New branch** → ``<some name>`` (usually ``dev-`` + your name, e.g. ``dev-tania``).
Then you should see it on top left, next to the project name.


3. Setup mapping of your local project copy to the remote dev machine:
______________________________________________________________________

Go to **Tools** → **Deployment** → **Configuration** or **PyCharm** → **Settings** → **Build, Execution, Deployment** → **Deployment**

Click on **+** to add a new configuration, choose **SFTP**, and name it ``panda-ui-dev``.

In the **Connection** tab for SSH configuration click on **...** and then on **+** to add a new SSH configuration:

 * Host: ``localhost``
 * Port: ``13322`` (the same as in the ssh tunnel command for ssh port forwarding)
 * Username: ``<your_username>`` (your CERN username you use to login to lxplus)
 * Authentication type: **Password**
 * Password: your CERN password
 * Test connection: should be successful, then you can save the configuration

Back to the **Connection** tab:

 * Root path: path to the project code: ``/data_aipanda163/<username>`` (you may need to create this folder in advance via ssh)

In the **Mappings** tab:

 * Local path: e.g. ``/Users/<username>/PyCharmProjects/panda-ui``
 * Deployment path: ``/PyCharmProjects/panda-ui`` (it is a tail to root path from the connection tab)


Now you can check if the mapping really works by uploading the project code to the remote dev node.
To do it, right-click the root folder **panda-ui** in the project tree on the left and select **Deployment** → **Upload to** -> **panda-ui-dev**.
Then, you should see all files in your folder on the remote dev node.

4. Connect to remote Python interpreter:
________________________________________

We have a python virtualenv with all necessary packages installed on the remote dev node.
Here we configure PyCharm to use it.

Go to **PyCharm** → **Settings** → **Python** → **Interpreter**, click on **Add Interpreter** and select **On SSH...**.
In the opened window, choose existing SSH configuration (the one already created for mapping).
After the connection inspection is done, fill in the fields:

 * Environment: select **Existing**
 * Interpreter: ``/data/venv313/bin/python3.13``
 * For path synching, make sure it is the same as in the mapping config you did previously, i.e. local path: ``/Users/<username>/PyCharmProjects/panda-ui`` and remote path: ``/data_aipanda163/<username>/PyCharmProjects/panda-ui``

5. Setup Run configuration for debugging:
_________________________________________

Turn on Django support by going to **PyCharm** → **Settings** → **Python** → **Django** and fill in the fields:

 * Enable Django Support: checked
 * Django project root: full path to the local directory of the project, e.g.: ``/Users/<username>/PyCharmProjects/panda-ui``
 * Settings: path to the settings folder of the project: ``backend/rest_api/settings``
 * Manage script: full path to manage.py: ``backend/rest_api/manage.py``

Then go to **Run** → **Edit Configurations** and create a new **Django server** configuration. In the opened window fill in the fields:

 * Name: ``backend dev`` (or any other you like)
 * Run: choose the remote interpreter we created earlier
 * Host: ``aipanda033.cern.ch``
 * Port:  ``800X`` (the same as in the ssh tunnel command for http port forwarding)

Also, we need to create a separate configuration to run unit tests. Go to **Run** → **Edit configurations** and create
a new **Django tests** configuration. In the opened window fill in the fields:

 * Name: ``backend tests all`` (or any other you like)
 * Target: ``backend.rest_api`` (Django will run all tests in this folder and its subfolders)
 * Python interpreter: choose the remote interpreter created earlier

6. Secrets and logs:
____________________

For security and common sense reasons, we do not store secrets and logs in the git repository.

So, we need to create a folder for logs on remote node outside of the git repo, e.g. ``/data_aipanda163/<username>/PyCharmProjects/logs/panda-ui/``,
and make sure that the folder is writable by the user running the Django server (``chmod 777 <folder>``)

For secrets, we use environment variables stored in a file ``.env`` that is not tracked by git.
All required variables are listed in the template file ``.env-config-template``.
So you may copy ``backend/rest_api/settings/.env-config-template`` file and rename the copy to ``.env``.
Then, add all needed configuration values including the ``LOG_PATH`` you just created to the file (ask to share an example file),
and upload the changes to the remote dev machine.

7. Run & enjoy:
_______________

Now you should be able to run the Django server on the remote dev node by clicking the Run button on the top right of PyCharm.
You can also run unit tests by selecting the corresponding configuration and clicking the Run button.
Next steps are to set up the Angular frontend to work with the REST API backend.


""""""""""""""""""""""""""""""""
Setting up Angular frontend
""""""""""""""""""""""""""""""""

Here we use the same remote dev node (aipanda033) and PyCharm Professional.

1. Install Node.js and dependences on the remote machine
________________________________________________________

.. code-block:: bash

    # Go to dev node
    ssh <your_username>@lxplus.cern.ch
    ssh aipanda033
    # Download and install nvm:
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
    # Restart the shell
    \. "$HOME/.nvm/nvm.sh"
    # Download and install Node.js:
    nvm install 22
    # Verify the Node.js and npm version:
    node -v
    nvm current
    npm -v
    # get the path to node and npm for later
    which node

    # Go to the project frontend directory, where package.json is located
    cd frontend
    # Install the dependencies
    npm install
    # optionally you may need to fix the permissions
    chmod -R 755 node_modules


2. Set up remote Node.js interpreter in PyCharm
_______________________________________________

Go to **PyCharm** -> **Settings** > **Plugin** and make sure the following plugins installed and activated:
``Node.js``, ``Node.js Remote Interpreter``, ``JavaScript and TypeScript``

Open **Settings** > **Languages & Frameworks** > **Node.js**, click on **...** -> **+** -> **Add remote**. In the opened window fill in the fields:

 * Choose already existing SSH configuration to dev node
 * Node interpreter: path to node on the remote machine, where Node.js has been installed just before, output of ``which node`` command

3. Set up remote Node.js run configuration in PyCharm
______________________________________________________

Go to **Run** > **Edit Configurations** > **Add New Configuration** > **npm**. In the opened window fill in the fields:

 * Name: ``frontend dev`` (or any other you like)
 * Package.json: path to package.json on local machine
 * Command: run
 * Script: start
 * Node interpreter: Choose remote Node interpreter we just created
 * Package manager: should be path to npm on the remote machine
 * Mapping: check it is correct, local path to project root should be mapped to remote path to project root
 * Apply & Save

Put your port for running frontend in ``frontend/angular.json`` file to ``projects.frontend.architect.serve.options.port``.

Put the port you set for running backend to ``frontend/src/environments/environment.ts`` file, ``apiUrl`` varuable.

4. Run & enjoy:
_________________________

Now you should be able to run the Angular frontend on the remote dev node by clicking the Run button on the top right of PyCharm.
Depending on port you set for frontend, you can access it in the browser at ``http://aipanda033.cern.ch:800X``,
and make sure the ssh tunnel is running and proxy is set up in the browser.


--------------------------------
Building images for development
--------------------------------

From the root of the repository you can build docker images for backend and frontend.

``docker build --platform=linux/amd64 -f docker/Dockerfile.backend -t pandaui-backend:latest .``

