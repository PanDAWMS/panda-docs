==================================
Contributing Changes
==================================

PanDA components are developed based on `GitHub Flow <https://guides.github.com/introduction/flow/>`_
with small customization. The sequence is as follows:

#. Creation of a branch or fork. In git, branches are lightweight things that are often temporary and may be deleted
   anytime. The master branch is protected so that only a couple of persons can push commits there.

#. Adding commits to the branch. You can experiment with any changes since they don't affect the master branch.

#. Deployment of changes on a test instance. All changes must be verified before being merged to the master branch.

#. Submission of a Pull Request which will initiate a discussion about your changes.

#. Discussion and review on your code. Once a Pull Request has been opened, your changes are reviewed to check
   functionalities, the coding style, test results, and so on. Note that your code must follow PEP8.

#. Merging changes. Once your changes are approved, they will be merged to the master branch. The branch can be
   deleted at this stage since commit logs are also merged.


|br|

How to install your local changes to your instances
-----------------------------------------------------
You can install and test your changes locally before submitting pull requests.
The following example shows how to install local changes to your own PanDA server.

.. prompt:: bash

 # checkout the repository
 git clone https://github.com/PanDAWMS/panda-server.git

 # add changes in panda-server
 cd panda-server
 ...

 # stop the PanDA server
 /sbin/service httpd-pandasrv stop

 # go to virtual env if necessary
 . <venv_dir>/bin/activate

 # make sdist and install it twice with different pip options since pip doesn't install it
 # without those steps when the version number is incremented
 cd panda-server
 rm -rf dist
 python setup.py sdist
 pip install dist/p*.tar.gz --upgrade --force-reinstall --no-deps
 pip install dist/p*.tar.gz --upgrade

|br|

Publishing a new version of panda-* package on PyPI
---------------------------------------------------------
The procedures are as follows:

#. Increment the version number, which is typically defined in ``panda-*/PandaPkgInfo.py``.

#. Push it to the master branch of the git repository.

#. Make a new release on the master branch of the git repository in GitHub.

which automatically triggers a git action to publish the version on PyPI.

|br|