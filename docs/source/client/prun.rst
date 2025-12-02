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

 prun --helpGroup ALL

shows all available options.

Hello world
-------------

Here is an Hello world example.

.. tabs::

   .. code-tab:: bash ATLAS users

      prun --exec "pwd; ls; echo Hello-world > myout.txt" --outDS user.<your account>.`uuidgen` --nJobs 3 --output myout.txt

   .. code-tab:: bash DOMA users

      prun --exec "pwd; ls; echo Hello-world > myout.txt" --outDS user.<your account>.`uuidgen` --nJobs 3 --output myout.txt \
         --vo wlcg --site <your queue> --prodSourceLabel test --workingGroup ${PANDA_AUTH_VO} --noBuild

where ``--exec`` takes the execution string which is executed on remote computing resources,
and ``--outDS`` takes the basename of the output collection. DOMA users need to set
``--vo wlcg --workingGroup ${PANDA_AUTH_VO}`` since each organization is registered as a sub-VO in DOMA PanDA,
``--site`` to one of queues shown in `DOMA PanDA monitor <https://panda-doma.cern.ch/sites/>`_, and
``--noBuild`` since generally the build step is unused.

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


Running on GPU
--------------------

GPUs (Graphics Processing Unit) have numerous advantages in data-intensive tasks, 
physics analysis, machine learning, and other fields, making them powerful tools for 
high-performance and efficient calculations and processing.

GPU resources are available exclusively at designated sites, necessitating explicit job assignment. 
Users need to specify the GPU architecture in the ``--architecture`` option when executing ``prun``.
The option's argument is explained in `this section <../advanced/brokerage.html#checks-for-cpu-and-or-gpu-hardware>`__.
For example, to utilize NVIDIA GPUs, you can set the argument like: ``--architecture '&nvidia'``.　e.g.,

.. prompt:: bash

 prun --containerImage docker://gitlab-registry.cern.ch/hepimages/public/gpu-basic-test --exec "python /test-gpu.py" --outDS user.$USER.`uuidgen` --noBuild --nJobs=1 --architecture '&nvidia'
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
when jobs get started, while `%IN` is replaced with files in ``--inDS``.

Note that when dataset containers are used for secondaryDSs like `StreamName:nFilesPerJob:ContainerName` they
are expanded to constituent datasets and each job takes `nFilesPerJob` files from each constituent dataset.
This means that if a dataset container has `M` constituent datasets a single job cound take `M` x `nFilesPerJob`
files from the dataset
container. There are ``--notExpandInDS`` and ``--notExpandSecDS`` options so that jobs don't expand dataset containers,
use files across dataset boundaries in dataset containers, and take only `nFilesPerJob` files from each
dataset container.


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

Users can add metadata to each job in PanDA. If jobs produce json files userJobMetadata.json in the run directory
it is uploaded to PanDA and you can see it in pandamon or pbook. This is typically useful if jobs have very small
outputs, such as hyperparameter optimization for machine learning where each job could produce only one value.
Users can get results directly from PanDA rather than uploading/downloading small files to/from storages.
Note that the size of each metadata must be less than 1MB and metadata are available only for successfully
finished jobs.
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

How to run the task in parallel while the parent task is still running
-------------------------------------------------------------------------

It is possible to sequentially chain tasks using the ``--parentTaskID`` option. A typical use-case is as follows:

1. A parent task is running to produce some datasets.
2. A child task is submitted to use one or more datasets as input which the parent is producing.
3. The child task periodically checks the input datasets and generates jobs if new files are available.
4. Finally, the child task is finished once the parent is finished and all files produced by the parent
   have been processed.

The ``--parentTaskID`` option takes the taskID of the parent task that is producing ``--inDS``.
Note that if the child task is submitted without the ``--parentTaskID`` option,
it will run only on the available files when the task is submitted.

|br|

Difference between ``--useAthenaPackage`` and ``--athenaTag``
----------------------------------------------------------------
Both options set up Athena on remote compute nodes. The main difference is as follows.
``--useAthenaPackage`` requires Athena runtime environment on your local computer to automatically
configure the task by parsing environment variables and make a sandbox file by using cpack,
which is included in Athena, according to Athena's directory structure.
On the other hand, ``--athenaTag`` doesn't need Athena locally. It gathers files in the current directory
when making a sandbox file and passes the argument string to asetup executed on remote compute nodes.

|br|

How to control job size
----------------------------------------------------------------
``--nFilePerJob``, ``--nGBPerJob`` and ``--maxNFilesPerJob`` options  are available at task submission to
change a job size (e.g. job duration, size of output).  But if a user sets those options and they are assumed
to create many short jobs based on results of scouting jobs, those options are reset to
their default values ( ``--nFilePerJob`` =None, ``--nGBPerJob`` =MAX and ``--MaxNFilesPerJob`` =200).
In principle, the system centrally defines job size by taking into account execution time, resource usage,
input and output sizes, and so on, as explained in :ref:`advanced/sizing:Job Sizing`,
and it is recommended to leave it to the system rather than playing with those options.

|br|

Bulk task submission
---------------------------------
It is possible to submit multiple tasks in a single execution of prun.
First, you need to prepare a json file that specifies multiple combinations of input and output.
The file contains a json dump of `[{'inDS': a comma-concatenated input dataset names, 'outDS': output dataset name}, ...]`.
E.g.

.. code-block:: bash

    $ python
    >>> import json
    >>> data = [{"inDS": "group.susy.abc/,group.susy.def/", "outDS": "user.hoge.XYZ"},
                {"inDS": "group.susy.opq/", "outDS": "user.hoge.VWX"}]
    >>> with open('test.json', 'w') as f:
            json.dump(data, f)

where two combinations of input and output are specified. Note that outDS must be unique
since each combination is mapped to a single task.

Then you just need to execute prun with ``--inOutDsJson``

.. prompt:: bash

 prun --inOutDsJson test.json --exec ...

|br|

Running on a particular CPU hardware
--------------------------------------
Users can specify the CPU architecture as well as the GPU architecture using the ``--architecture`` option.
The option's argument is explained in `this section <../advanced/brokerage.html#checks-for-cpu-and-or-gpu-hardware>`__.
If the option is not specified the system automatically chooses computing resources without considering CPU architecture.

.. prompt:: bash $, auto

 $ # to utilize only x86_64 CPUs
 $ prun --architecture '#x86_64' ...

 $ # to utilize only intel x86_64 CPUs
 $ prun --architecture '#x86_64-intel' ...

 $ # to utilize only ARM CPUs
 $ prun --architecture '#aarch64' ...

 $ # to utilize both x86_64 and ARM CPUs
 $ prun --architecture '#(x86_64|aarch64)' ...

|br|
