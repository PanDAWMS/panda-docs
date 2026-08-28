================================
PanDA UI Development Guide
================================

------------------------------------------------
Setting up the project with PyCharm Professional
------------------------------------------------

.. note:: This guide is for PyCharm Professional only, as it supports remote development.

We are using a paradigm of remote development supported by PyCharm.
In this case, there are 2 copies of the project: one is local, another is on a remote development machine (aipanda033).
You make changes to the local one, upload changes to the remote one, and
then PyCharm runs the project on the remote node and transfers debugging data to the locally running PyCharm.

To be able to work outside the CERN network, we use SSH tunneling through lxplus. Example of such command:

.. code-block:: bash

    ssh -N -p 22 -D 1234 <username>@lxplus.cern.ch -L localhost:13322:aipanda033.cern.ch:22 -L localhost:1330X:aipanda033.cern.ch:800X  -L localhost:1330Y:aipanda033.cern.ch:800Y

where ``X`` and ``Y`` are single digits used to construct the backend and frontend ports.
Currently, ports ending in ``0``, ``1``, ``2``, ``7``, and
``9`` are already taken, so choose two different available digits.

There is `SSH Tunnel Manager app <https://www.tynsoe.org/stm/>`_ for MacOS, we are using it to create and use tunnels.

In the browser, you can use a proxy extension (e.g. SwitchyOmega) with a SOCKS5 protocol to ``localhost:1234``.

""""""""""""""""""""""""""""""""""""""""
Setting up Django REST framework backend
""""""""""""""""""""""""""""""""""""""""

.. note:: The following instruction is for MacOS and PyCharm Professional 2025.2.2. In newer or older versions of PyCharm the UI may differ.

0. Install PyCharm:
________________________________

Pre installation requirements:

 * Open JDK
 * Get PyCharm Professional from the official website

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
 * Deployment path: ``/PyCharmProjects/panda-ui`` (it is the path relative to the root path from the connection tab)


Now you can check if the mapping really works by uploading the project code to the remote dev node.
To do it, right-click the root folder **panda-ui** in the project tree on the left and select **Deployment** → **Upload to** -> **panda-ui-dev**.
Then, you should see all files in your folder on the remote dev node.

4. Connect to remote Python interpreter:
________________________________________

We have a python virtualenv with all necessary packages installed on the remote dev node.
Here we configure PyCharm to use it.

Go to **PyCharm** → **Settings** → **Python** → **Interpreter**, click on **Add Interpreter** and select **On SSH...**.
In the window that opens, choose existing SSH configuration (the one already created for mapping).
After the connection inspection is done, fill in the fields:

 * Environment: select **Existing**
 * Interpreter: ``/data/venv314_pandaui/bin/python3.14``
 * In **Advanced** tab below, make sure it is the same as in the mapping config you did previously, i.e. local path: ``/Users/<username>/PyCharmProjects/panda-ui`` and remote path: ``/data_aipanda163/<username>/PyCharmProjects/panda-ui``.

5. Setup Run configuration for debugging:
_________________________________________

Turn on Django support by going to **PyCharm** → **Settings** → **Python** → **Django** and fill in the fields:

 * Enable Django Support: checked
 * Django project root: the full path to the local directory of the project, e.g.: ``/Users/<username>/PyCharmProjects/panda-ui``
 * Settings: the path to the project's settings folder: ``backend/rest_api/settings``
 * Manage script: the full path to ``manage.py``: ``backend/manage.py``

If you do not need to work with WebSockets and only need to run and develop the REST API endpoints, follow section 5.a.
The runserver_plus development server is sufficient for this use case.

If you need to develop using WebSockets, follow section 5.b. In this case, use the Daphne development server,
which supports both REST API and WebSocket connections over HTTPS.

5.a. REST API run configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go to **Run** → **Edit Configurations** and create a new **Python** configuration. In the opened window fill in the fields:

 * Name: ``backend dev`` (or any other you like)
 * Run: choose the remote interpreter we created earlier
 * Select **script** in drop-down menu and put path to the ``manage.py`` file, i.e.  ``/data_aipanda163/<username>/PyCharmProjects/panda-ui/backend/manage.py``
 * Put the following command and params: ``runserver_plus aipanda033.cern.ch:800X --cert-file /tmp/cert.crt``
 * Working directory: ``/data_aipanda163/<username>/PyCharmProjects/panda-ui/backend/``
 * Environment variables: ``DJANGO_ENVIRONMENT=development;DJANGO_SETTINGS_MODULE=rest_api.settings;PATH_ENV_FILE=/data_aipanda163/<username>/private/.env;PYTHONUNBUFFERED=1``, where PATH_ENV_FILE is explained in step 6

5.b. WebSockets and REST API run configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For both WebSockets and REST API we use the Daphne test server, which serves Django REST API and WebSocket connections over HTTPS.
The Daphne test server requires the certificates, so you need to generate them.

SSH to the dev node, create a folder in your space for certificates

 * ``cd /data_aipanda163/<your_folder>/``
 * ``mkdir certs``

Generate a private key and a self-signed certificate with the following command:

 * ``openssl req -x509 -newkey rsa:2048 -keyout certs/daphne.key -out certs/daphne.crt -days 365 -nodes``
 * it will ask you additional information, e.g. ``CH`` for country, ``GE`` for state, ``Geneva`` for city, ``CERN`` for organisation, ``aipanda033.cern.ch`` for hostname etc

Go to **Run** → **Edit Configurations** and create a new **Python** configuration. In the opened window fill in the fields:

 * Name: ``backend daphne`` (or any other you like)
 * Run: choose the remote interpreter we created earlier
 * Select **module** in the drop-down menu and put ``daphne``
 * Put the following params to the next input below (do not forget to change the port and username in the certificate paths): ``--verbosity 3 -p 0 -b 127.0.0.1 -e "ssl:800X:privateKey=/data_aipanda163/<username>/certs/daphne.key:certKey=/data_aipanda163/<username>/certs/daphne.crt" rest_api.asgi:application``
 * Working directory: ``/data_aipanda163/<username>/PyCharmProjects/panda-ui/backend/``
 * Environment variables: ``DJANGO_ENVIRONMENT=development;DJANGO_SETTINGS_MODULE=rest_api.settings;PATH_ENV_FILE=/data_aipanda163/<username>/private/.env;PYTHONUNBUFFERED=1``,
    where PATH_ENV_FILE is explained in step 6.

5.c. Tests runner configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We also need to create a separate configuration to run the unit tests. Go to **Run** → **Edit configurations** and create
a new **Django Tests** configuration. In the opened window fill in the fields:

 * Name: ``backend tests all`` (or any other you like)
 * Target: ``backend.rest_api`` (Django will run all tests in this folder and its subfolders)
 * Python interpreter: choose the remote interpreter created earlier

6. Secrets and logs:
____________________

For security reasons, we do not store secrets and logs in the git repository.

So, you need to create a folder for logs on the remote VM outside of the git repo, e.g. ``/data_aipanda163/<username>/PyCharmProjects/logs/panda-ui/``,
and make sure that the folder is writable by the user running the Django server (``chmod 700 <folder>``)

For secrets, we use environment variables stored in a file ``.env`` that is not tracked by git.
All required variables are listed in the template file ``.env-config-template``.
You can copy ``backend/rest_api/settings/.env-config-template`` file and rename the copy to ``.env``.
Then, add all needed configuration values including the ``LOG_PATH`` you just created to the file (ask someone to share an example file),
and upload the changes to the remote dev machine.

7. Run & enjoy:
_______________

Now you should be able to run the test server on the remote dev node by clicking the Run button on the top right of PyCharm.
It should display the URL where it is running. Because the development server uses the self-signed certificate you created,
Firefox and other browsers may reject HTTPS and WebSocket connections until the certificate is trusted.
Open the link in your browser, it will display a certificate/security warning. Accept/trust the certificate and then reload the page.
Normally you should see a ``401`` error, which is expected.

You can also run unit tests by selecting the corresponding configuration and clicking the Run button.
Next steps are to set up the Angular frontend to work with the REST API backend.


""""""""""""""""""""""""""""""""
Setting up Angular frontend
""""""""""""""""""""""""""""""""

Here we use the same remote dev node (aipanda033) and PyCharm Professional.

1. Install Node.js and dependencies on the remote machine
________________________________________________________

.. code-block:: bash

    # Go to dev node
    ssh <your_username>@lxplus.cern.ch
    ssh aipanda033
    # Download and install NVM:
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
    # Restart the shell
    \. "$HOME/.nvm/nvm.sh"
    # Download and install Node.js:
    nvm install 24
    # Verify the Node.js and npm version:
    node -v
    nvm current
    npm -v
    # get the path to node and npm for later
    which node

    # Go to the project frontend directory, where package.json is located
    cd /data_aipanda163/<username>/PyCharmProjects/panda-ui/frontend
    # Install the dependencies
    npm install
    # optionally, you may need to fix the permissions
    chmod -R 755 node_modules


2. Set up remote Node.js interpreter in PyCharm
_______________________________________________

Make sure you have **Node.js** installed on you computer locally, so that PyCharm's Node.js plugins work correctly [`PyCharm docs <https://www.jetbrains.com/help/pycharm/developing-node-js-applications.html#ws_node_before_you_start/>`_]

Go to **PyCharm** -> **Settings** > **Plugin** and make sure the following plugins are installed and activated:
``Node.js``, ``Node.js Remote Interpreter``, ``JavaScript and TypeScript``

Open **Settings** > **Languages & Frameworks** > **Node.js**, click on **...** -> **+** -> **Add remote**. In the opened window fill in the fields:

 * Choose already existing SSH configuration to dev node
 * Node interpreter: path to node on the remote machine, where Node.js was installed in the previous step, the output of ``which node`` command

3. Set up remote Node.js run configuration in PyCharm
______________________________________________________

Go to **Run** > **Edit Configurations** > **Add New Configuration** > **npm**. In the opened window fill in the fields:

 * Name: ``frontend dev`` (or any other you like)
 * Package.json: path to package.json on local machine
 * Command: run
 * Script: start
 * Arguments: ``-- --configuration development --host aipanda033.cern.ch --port 800Y`` - this is where the frontend will be accessed
 * Node interpreter: Choose remote Node interpreter we just created
 * Package manager: should be path to npm on the remote machine
 * Mapping: check that it is correct, local path to project root should be mapped to remote path to project root
 * Apply & Save

Put the API URL of your Django backend in ``frontend/src/environments/environment.development.ts`` file,
``apiUrl`` variable, it must end with ``/api``, e.g. ``http://aipanda033.cern.ch:800X/api``


4. Running version script
_________________________

To display the current version of the app which is running in the footer, we need to generate it.
To avoid doing it manually add it to the PyCharm Tools runners:

Go to **Settings** -> **Tools** -> **External tools**, and add a new one by clicking on **+** sign. In the window that opens:

 * Name: ``update version`` (or whatever you like)
 * Program: ``node``
 * Arguments: put the path to the script: ``frontend/src/scripts/version-gen-dev.js``
 * Working directory: put the path to the project: ``/Users/<username>/PyCharmProjects/panda-ui``


5. Run & enjoy:
_________________________

Now you should be able to run the Angular frontend on the remote dev node by clicking the Run button on the top right of PyCharm.
Depending on the port you set for the frontend, you can access it in the browser at ``http://aipanda033.cern.ch:800Y``,
and make sure the SSH tunnel is running and proxy is set up in the browser.


--------------------------------
Building images for development
--------------------------------

From the root of the repository you can build docker images for backend and frontend.

``docker build --platform=linux/amd64 -f docker/Dockerfile.backend -t pandaui-backend:latest .``

