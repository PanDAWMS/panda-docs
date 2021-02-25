==================================
Contributing Changes
==================================

PanDA components are developed based on `GitHub Flow <https://guides.github.com/introduction/flow/>`_
with small customization. The sequence is as follows:

#. Create a branch or folk. In git, branches are light weight things that are often temporary and may be deleted
   anytime. The master branch is protected, so that only a couple of persons can push commits there.

#. Add commits to the branch. You can experiment any changes since they don't affect the master branch.

#. Deploy changes on a test instance. All changes must be verified before being merged to the master branch.

#. Submit a Pull Request which will initiate discussion about your changes.

#. Discuss and review your code. Once a Pull Request has been opened, your changes are reviewed to check
   functionalities, the coding style, test results, and so one. Note that your code must follow PEP8.

#. Merge changes. Once your changes are approved they will be merged to the master branch. The branch can be
   deleted at this stage since commit logs are also merged.


|br|

How to install your local changes to your instances
-----------------------------------------------------
You can install and test your changes locally before submitting pull requests.
The following examples shows how to install local changes to the PanDA server.

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

#. Increment the version number which is typically defined in ``panda-*/PandaPkgInfo.py``.

#. Push it to the master branch of the git repository.

#. Make a new release on the master branch of the git repository in GitHub.

which automatically triggers a git action to publish the version on PyPI.

|br|