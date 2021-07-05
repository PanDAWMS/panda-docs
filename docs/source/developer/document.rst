=====================
Writing Documentation
=====================

This section explains how to write PanDA documentation.
If you just want to add changes to existing documentation see
:doc:`Adding Changes to Documentation </developer/document_light>`.

1. Preparation
---------------

First, you need to install sphinx packages

.. prompt:: bash

    pip install sphinx
    pip install sphinx-rtd-theme
    pip install sphinx-prompt

and `pandoc <https://pandoc.org/installing.html>`_ .
Then fork the `panda-docs <https://github.com/PanDAWMS/panda-docs.git>`_ repository following
`GitHub HowTo <https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo>`_ .


2. Repository structure
-----------------------

You can see the following structure in the repository.

.. code-block:: none

    /panda-docs
        ├── /docs
           ├── /build
           ├── make.bat
           ├── Makefile
           └── /source
              ├── conf.py
              ├── index.rst
              ├── /images
              ├── /_static
              └── /section_name
                  ├── section_name.rst
                  ├── subsection_name.rst
                  └── ...

You edit or add RST files under the source directory or sub-directories in the source directory.
`index.rst` is the RST file for the main page, and
`conf.py` controls how sphinx builds documents. There is a sub-directory for each section in the source directory.
Each section is composed of one main RST file with the section name plus .rst extension
and other RST files for subsections.

3. Build documents
--------------------

Once you edit some RST files you need to build documents.

.. prompt:: bash

    cd panda-docs/docs
    make html

This will build html documents in the build directory. You can check how documents look like
by opening panda-docs/docs/build/html/index.html via your web browser.

4. Submitting pull requests
-------------------------------

Once you are comfortable with the changes, you should push them to your forked repository and submit a pull request following
`the github doc <https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request>`_ .
Then requests are reviewed, and the changes will be merged to the main branch once approved.

5. Publish the latest documents
----------------------------------

Actions on the git repository such as push and tagging trigger automatic-builds on the Read The Docs
and the latest documents show up at https://panda-wms.readthedocs.io/en/latest/ .
