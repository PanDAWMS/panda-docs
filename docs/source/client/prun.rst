===========================
Running ordinary analysis
===========================

``prun`` is the command-line tool to allow users to run any application on PanDA.
The application could be ROOT (CINT, C++, pyRoot), python, user's executable, shell script, and so on,
and must be made available on computing resources beforehand.
``prun`` sends all files except too large files under the current directory to computing resources.
Users can construct arbitrary runtime environments there
and can do anything in principle. However, please avoid careless network operations
connecting to remote servers (e.g., git clone and wget) unless the remote servers permit them.
Your task is split into many jobs, and these jobs are executed in parallel,
so that those operations tend to become a DDoS attack and easily break
the remote servers.

.. contents:: Table of Contents
    :local:

-----------

|br|

How to run
============

.. prompt:: bash

 prun -h

shows all available options.

Hello world
-------------

Here is an Hello world example.

.. prompt:: bash

 prun --exec "pwd; ls; echo Hello-world > myout.txt" --outDS user.hoge.`uuidgen` --nJos 3 --output myout.txt

where ``--exec`` takes the execution string which is executed on remote computing resources,
and ``--outDS`` takes the basename of the output collection.

This task generates 1 build job to setup and 3 run jobs to produce `myout.txt`, and creates two collections
(e.g., dataset containers); one for output data and the other for log files. The next section explains what the
build job is. Each run job executes *pwd; ls; echo Hello-World > myout.txt* and produces an output file, *myout.txt*.
The output file is renamed to `<jediTakID>._<serial_number>.myout.txt` to be unique
in the entire system and is then added to the output data collection.
Each run job also produces a tarball of log files `<jediTakID>._<serial_number>.log.tgz` and adds it
to the log collection.

This example doesn't take input data, so it will generate 3 identical jobs.
It is possible to give unique numbers to jobs by adding *%RNDM:basenumber* in ``--exec``
which is incremented per job. E.g.,

.. prompt:: bash

 prun --exec "echo %RNDM:123 %RNDM:456"" ...

The first job executes "echo 123 456", the second job executes "echo 124 457", and so on.


Running with input files and a separate build step
----------------------------------------------------

Large input data must be transferred via data management systems instead of directly sending them from current directly.
You can specify the name of input data collection (e.g., input dataset name or container name) in ``--inDS``. *%IN* is
a placeholder
in ``--exec`` to be replaced with a comma-concatenated list of input data (e.g., filenames) when being executed
on computing resources.

It would be suboptimal to build runtime environment and run the application in each job, if the build step is
time-consuming.
It is possible to execute the build step only once in a build job and let many run jobs share the runtime.

The following example compiles a ROOT C++ source file in build jobs on remote computing resources and starts many
run jobs with input files once build jobs finished.

First, you need to prepare source files and Makefile locally.
For example,

.. code-block:: bash

    $ cat cpptest.cc

    #include <string>
    #include <vector>
    #include <iostream>
    #include <stdlib.h>

    #include "TROOT.h"
    #include "TFile.h"
    #include "TTree.h"
    #include "TChain.h"
    #include "TBranch.h"

    int main(int argc, char **argv)
    {
      // split by ','
      std::string argStr = argv[1];
      std::vector<std::string> fileList;
      for (size_t i=0,n; i <= argStr.length(); i=n+1)
        {
          n = argStr.find_first_of(',',i);
          if (n == std::string::npos)
            n = argStr.length();
          std::string tmp = argStr.substr(i,n-i);
          fileList.push_back(tmp);
        }

      // open input files
      TChain fChain("CollectionTree");
      for (unsigned int iFile=0; iFile<fileList.size(); ++iFile)
        {
          std::cout << "open " << fileList[iFile].c_str() << std::endl;
          fChain.Add(fileList[iFile].c_str());
        }

      Int_t           EventNumber;
      TBranch        *b_EventNumber;
      fChain.SetBranchAddress("EventNumber", &EventNumber, &b_EventNumber);

      // main loop
      Long64_t nentries = fChain.GetEntriesFast();
      for (Long64_t jentry=0; jentry<nentries;jentry++)
        {
          Long64_t ientry = fChain.LoadTree(jentry);
          if (ientry < 0)
            break;
          fChain.GetEntry(jentry);

          std::cout << EventNumber << std::endl;
        }
    }

Make file could be something like

.. code-block:: bash

    $ cat Makefile

    ROOTCFLAGS    = $(shell root-config --cflags)
    ROOTLIBS      = $(shell root-config --libs)
    ROOTGLIBS     = $(shell root-config --glibs)

    CXX           = g++
    CXXFLAGS      =-I$(ROOTSYS)/include -O -Wall -fPIC
    LD            = g++
    LDFLAGS       = -g
    SOFLAGS       = -shared

    CXXFLAGS     += $(ROOTCFLAGS)
    LIBS          = $(ROOTLIBS)
    GLIBS         = $(ROOTGLIBS)

    OBJS          = cpptest.o

    cpptest: $(OBJS)
            $(CXX) -o $@ $(OBJS) $(CXXFLAGS) $(LIBS)

    # suffix rule
    .cc.o:
            $(CXX) -c $(CXXFLAGS) $(GDBFLAGS) $<

    # clean
    clean\:
            rm -f *~ *.o *.o~ core

Then

.. prompt:: bash

 prun --exec "cpptest %IN" --bexec "make" --inDS valid1.006384.PythiaH120gamgam.recon.AOD.e322_s412_r577 --rootVer recommended ...

`prun` sends files including cpptest.cc and Makefile in the current directory to remote computing resources.
Note that a build job is generated for each computing resource if the task is split to multiple comput resources
for parallel execution. The build job executess the argument of ``--bexec`` to produce binary files, and then
run jobs get started with those binary files. *%IN* is dynamically converted to a commma-concatenated filenames
in the input data collection specified by ``--inDS``.


Running python
-------------------

This example runs a python job.

.. code-block:: bash

    $ cat purepython.py

    import sys
    print sys.argv
    f = open('out.dat','w')
    f.write('hello')
    f.close()
    sys.exit(0)

Then

.. prompt:: bash

 prun --exec "python purepython.py %IN" --inDS ...

It will run with the system python on the remote resource.


Running stand-alone containers
------------------------------------

It is possible run standalone containers by using ``--containerImage`` option.

.. prompt:: bash

 prun --containerImage docker://alpine --exec "echo Hello World" --outDS user.hoge.`uuidgen`

Your job will download the docker image and execute echo in the container.
``--containerImage`` can also take the CVMFS path if the the image is unpacked in CVMFS.
This has the advantage for each job to avoid downloading the image.

.. prompt:: bash

 prun --containerImage /cvmfs/unpacked.cern.ch/registry.hub.docker.com/atlasml/ml-base:latest --exec "echo Hello World" ...

IO is done through the initial working directory `$PWD` where the container is launched. The working directly
is mounted to ``/srv/workDir``.
It is recommended to dynamically get the path of the initial working directory
using ``os.getcwd()``, ``echo $PWD``, and so on, when the application is executed in the container
rather than hard-coding ``/srv/workDir`` in the
application, since the convention might be changed in the future.

.. prompt:: bash

 prun --containerImage docker://atlasml/ml-base --exec "my_command %IN" --outputs my-output-file.h5 --forceStaged --inDS ...

Input files are copied to `$PWD` even if the computing resource is configured to read files directly from the
storage resource since ``--forceStaged" option is used.
`%IN` in ``--exec`` is replaced to a comma-concatenated list of the copied input files.
It is user's responsibility to copy output files to `$PWD`, i.e., `my_command` in this example has to put
`my-output-file.h5` to `$PWD`, then the system takes care of subsequent procedures
like renaming and stage-out.

---------

|br|

FAQ
======

Output with wildcards
-----------------------------
When the number of output files produced by each job or a part of their filenames is unknown,
it is possible to specify their names with wildcards in ``--outputs`` option.

.. prompt:: bash

 prun --outputs "abc.data,JiveXML_*.xml" ...

Each job will have two output files, *<jediTaskID>.<serial number>.abc.data* and
*<jediTaskID>.<serial number>.JiveXML_XYZ.xml.tgz*.
The latter is a tarball of all JiveXML_*.xml produced by the job. Note that you need to escape the wildcard character
using \\ or "" to disable shell-globing, i.e. JiveXML\_\\*.xml or "JiveXML_*.xml".

|br|

Send jobs to particular computing resources
----------------------------------------------------
The system automatically chooses appropriate computing resources by using various information like data locality,
resource occupancy, and user's profile. However, users can still send jobs to particular sites using ``--site`` option.
e.g.,

.. prompt:: bash

 prun --site TRIUMF ...

|br|

Filtering files in the input dataset
-------------------------------------
The ``--match`` option allows user to choose files matching a given pattern. The argument is a comma-separated string.

.. prompt:: bash

 prun --match "*AOD*" ...
 prun --match "*r123*,*r345*" ...

If you need to skip specific files, use the ``--antiMatch`` option.

|br|

How to use multiple input datasets
----------------------------------------------------
If you just want to submit a single task running on multiple datasets, you just need to specify a comma-separated
list of input datasets.

.. prompt:: bash

 prun --inDS dsA,dsB,dsC,dsD ...

However, if you want to read multiple datasets in each job, i.e., one for signal and the other for background,
you need something more complicated.
The ``--secondaryDSs`` option specifies secondary dataset names. The argument is a comma-separated list of
`StreamName:nFilesPerJob:DatasetName[:MatchingPattern[:nSkipFiles]]` where

StreamName
   the name of stream in the --exec argument

nFilesPerJob
   the number of files per subjob

DatasetName
   the dataset name

MatchingPattern
   to use files matching a pattern (can be omitted)

nSkipFiles
   to skip files (can be omitted)

For example,

.. prompt:: bash

  prun --exec "test %IN %IN2 %IN3" --secondaryDSs IN2:3:data19.106017.gg2WW0240_JIMMY_WW_taunutaunu.recon.AOD.e371_s462_r563/,IN3:2:mc08.105200.T1_McAtNlo_Jimmy.recon.AOD.e357_s462_r541/ --inDS ...

`%IN2` and `%IN3` will be replaced with actual filenames in data19.blah and mc08.blah, respectively,
when jobs get started.
Note that `%IN` is replaced with files in ``--inDS``.

|br|

Merge output files
--------------------
The ``--mergeOutput`` option merges output files on the fly. E.g.,

.. prompt:: bash

 prun ... --mergeOutput --mergeScript="your_merger.py -o %OUT -i %IN"

Merge jobs (pmerge jobs) are generated once run jobs produce premerged files.
Each merge job executes the application described above to merge
`%IN` will be replaced with a comma-separated list of premerged filenames, and `%OUT` replaced with the final output
filename, when merge jobs get started. Each merge job merges the premerged files using Merging_trf.py for pool files,
hadd for ROOT hist and ntuple, gzip for log and text, or the application specified in the ``--mergeScript`` option.

|br|

Adding job metadata
----------------------

Users can add metadata to each job in PanDA. If jobs produce json files userJobMetadata.json in the run directory it is uploaded to PanDA and you can see it in pandamon or pbook. This is typically useful if jobs have very small outputs, such as hyperparameter optimization for machine learning where each job could produce only one value. Users can get results directly from PanDA rather than uploading/downloading small files to/from storages. Note that the size of each metadata must be less than 1MB and metadata are available only for successfully finished jobs.
First you need to change your application to produce a json file, e.g.

.. code-block:: bash

    $ cat a.py
    # do something useful and then
    import json
    json.dump({'aaaaaa':'bbbbbb', 'ccc':[1,2,5]}, open('userJobMetadata.json', 'w'))

Then submit tasks as usual. You don't need any special option. E.g.,

.. prompt:: bash

 prun --exec 'python a.py' --outDS user.hage.`uuidgen`

Once jobs have successfully finished you can see metadata in the job metadata field in the job page of
PanDA monitor.
You can fetch a json dump through
https://bigpanda.cern.ch/jobs/?jeditaskid=<taskID>&fields=metastruct&json
or in pbook

.. code-block:: bash

    $ pbook
    >>> getUserJobMetadata(taskID, output_json_filename)

or through end-user python API.

|br|
