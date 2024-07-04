===================================
Harvester HTCondor Plugins
===================================


Harvester HTCondor plugins can be used to interface HTCondor workload management system where a condor schedd service is running, including condor batch-system and condor-c (grid submission) service.


.. contents:: Table of Contents
    :local:
    :depth: 1


|br|


How to let harvester submit with condor plugins
-----------------------------------------------

Before letting harvester submit, one shall manually test to submit from harvester to the condor schedd instance(s), in order to make sure:

    - The communication and authentication between harvester and the condor instance(s) are good
    - The submit description file (SDF) describes the condor job correctly and the jobs submitted with the SDF can run and finish


Configure Condor on Harvester and Schedd
""""""""""""""""""""""""""""""""""""""""

The configurations of condor is outside the territory of harvester service, and hence not covered in this docs. The system admin should assure the harvester (condor client) and condor schedd service based on their own needs.

There are briefly two cases about harvester and condor schedd - local and remote\:

    * **Local**: The harvester and the condor schedd are running on the same node. Usually this means both harvester (condor client) and condor schedd share the same condor configuration files (e.g. under /etc/condor/config.d)
    * **Remote**: The harvester and the condor schedd are running on different nodes, communicating over network. This setup requires that both sides have their own condor configurations (for client vs schedd) and the harvester can reach and authenticate the condor schedd.

Both setups are fine, depending on the admins and the users.
The bottom-line is, the harvester should be able to submit jobs to and query the condor schedd without issue.

For the remote case, it important to know the pool name and schedd name of the remote schedd service. They are to be put after flags ``-pool`` and ``-name`` of condor command (condor_q, condor_submit, etc.) respectively, and they will be used in configuring harvester queueconfig about htcondor plugins.
One can get the pool name (usually made up of collector name + port) and schedd name by running the following commands on the schedd node\:

.. code-block:: text

    # pool name, here it is "myschedd.cern.ch:19618"
    [root@myschedd ~]# condor_config_val COLLECTOR_HOST
    myschedd.cern.ch:19618

    # schedd name, here  it is "myschedd.cern.ch"
    [root@myschedd ~]# condor_status -schedd
    Name               Machine            RunningJobs   IdleJobs   HeldJobs

    myschedd.cern.ch   myschedd.cern.ch          9580       2723         16


One may check `HTCondor docs <https://htcondor.readthedocs.io/en/latest/admin-manual/introduction-to-configuration.html>`_ . for more configuration details.


Assure communication and authentication to the Condor Schedd (Manual Test)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

After condor configuration, one can check the communication and authentication from harvester to condor schedd with condor_ping and condor_q command. In principle, these commands (from harvester to schedd) should all be successful without connection or authentication/authorization errors. 

Here are the examples for both local and remote cases.

.. tabs::

   .. code-tab:: text Local

        # Test READ/WRITE auth/permission with condor_ping
        # Given the local node to be the harvester with hostname myharvester
        # Given "atlpan" the user which harvester runs with, and also can authenticate the remote condor schedd (depending on configuration on schedd node)
        [root@harvester-test01 ~]# condor_ping -verbose -debug -type SCHEDD READ WRITE

        06/29/24 09:36:33 recognized READ as authorization level, using command 60020.
        06/29/24 09:36:33 recognized WRITE as authorization level, using command 60021.
        06/29/24 09:36:33 recognized DAEMON as authorization level, using command 60026.
        Destination:                 local schedd
        Remote Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Local  Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Session ID:                  harvester-test01:1676495:1719653793:10
        Instruction:                 READ
        Command:                     60020
        Encryption:                  AES
        Integrity:                   AES
        Authenticated using:         FS
        All authentication methods:  FS,SSL
        Remote Mapping:              condor@cern.ch
        Authorized:                  TRUE

        Destination:                 local schedd
        Remote Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Local  Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Session ID:                  harvester-test01:1676495:1719653793:11
        Instruction:                 WRITE
        Command:                     60021
        Encryption:                  AES
        Integrity:                   AES
        Authenticated using:         FS
        All authentication methods:  FS,SSL
        Remote Mapping:              condor@cern.ch
        Authorized:                  TRUE


        # query condor jobs on schedd with condor_q (-tot for brief summary only)
        [root@harvester-test01 ~]# condor_q -tot

        -- Schedd: harvester-test01.cern.ch : <188.184.72.215:21078?... @ 06/29/24 10:16:25
        Total for query: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended 
        Total for condor: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended 
        Total for all users: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended


   .. code-tab:: text Remote

        # Test READ/WRITE auth/permission with condor_ping
        # Given the local node to be the harvester with hostname myharvester
        # Given "atlpan" the user which harvester runs with, and also can authenticate the remote condor schedd (depending on configuration on schedd node)
        # Given the pool name and schedd name of remote schedd to be "myschedd.cern.ch:19618" and "myschedd.cern.ch"

        # Test READ/WRITE auth/permission with condor_ping
        [atlpan@myharvester ~]$ condor_ping -verbose -debug -type SCHEDD -pool myschedd.cern.ch:19618 -name myschedd.cern.ch READ WRITE
        06/29/24 09:48:38 recognized READ as authorization level, using command 60020.
        06/29/24 09:48:38 recognized WRITE as authorization level, using command 60021.
        Destination:                 schedd myschedd.cern.ch
        Remote Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Local  Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Session ID:                  schedd:993875:1719654518:136867
        Instruction:                 READ
        Command:                     60020
        Encryption:                  AES
        Integrity:                   AES
        Authenticated using:         CLAIMTOBE
        All authentication methods:  CLAIMTOBE,FS,SSL
        Remote Mapping:              atlpan
        Authorized:                  TRUE

        Destination:                 schedd myschedd.cern.ch
        Remote Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Local  Version:              $CondorVersion: 23.0.12 2024-06-13 BuildID: 739441 PackageID: 23.0.12-1 $
        Session ID:                  schedd:993875:1719654518:136868
        Instruction:                 WRITE
        Command:                     60021
        Encryption:                  AES
        Integrity:                   AES
        Authenticated using:         CLAIMTOBE
        All authentication methods:  CLAIMTOBE,FS,SSL
        Remote Mapping:              atlpan
        Authorized:                  TRUE


        # query condor jobs on schedd with condor_q (-tot for brief summary only)
        [atlpan@myharvester ~]$ condor_q -tot -pool myschedd.cern.ch:19618 -name myschedd.cern.ch

        -- Schedd: myschedd.cern.ch : <137.138.31.125:37170?... @ 06/29/24 10:14:50
        Total for query: 13926 jobs; 1541 completed, 63 removed, 2758 idle, 9547 running, 17 held, 0 suspended 
        Total for atlpan: 13926 jobs; 1541 completed, 63 removed, 2758 idle, 9547 running, 17 held, 0 suspended 
        Total for all users: 13926 jobs; 1541 completed, 63 removed, 2758 idle, 9547 running, 17 held, 0 suspended



Prepare SDF and submit test jobs (Manual Test)
"""""""""""""""""""""""""""""""""""""""""""""""

A submit description file (aka SDF, or JDL) is a file describing the condor jobs to submit (with condor_submit command).

One should prepare the SDF file to submit test jobs to their condor schedd to ensure the submission works and the job can finished correctly.

Examples of SDF file\:

.. tabs::

    .. code-tab:: text Hello World

        executable   = /usr/bin/echo
        arguments    = "Hello World!"

        log = /tmp/job.$(Cluster).$(Process).log
        output = /tmp/job.$(Cluster).$(Process).out
        error = /tmp/job.$(Cluster).$(Process).err

        request_cpus   = 1
        request_memory = 1024
        request_disk   = 10240

        should_transfer_files = yes
        when_to_transfer_output = on_exit

        queue 1


    .. code-tab:: text ATLAS Job

        # Running ATLAS pilot wrapper, submitting to PQ INFN-GENOVA through its HTCondorCE htcondorce01.ge.infn.it:9619, authenticating the CE with token

        executable = /cvmfs/atlas.cern.ch/repo/sw/PandaPilotWrapper/latest/runpilot2-wrapper.sh
        arguments = "-s INFN-GENOVA -r INFN-GENOVA -q INFN-GENOVA -j unified -i PR --pythonversion 3 -w generic --pilot-user ATLAS --url https://pandaserver.cern.ch  --harvester-submit-mode PULL --allow-same-user=False --job-type=unified --resource-type MCORE --pilotversion 3.7.7.3  "
        initialdir = /tmp/testdir
        universe = grid
        log = /tmp/testdir/grid.$(Cluster).$(Process).log
        output = /tmp/testdir/grid.$(Cluster).$(Process).out
        error = /tmp/testdir/grid.$(Cluster).$(Process).err
        transfer_executable = True
        x509userproxy = /the/x509_proxy/path

        grid_resource = condor htcondorce01.ge.infn.it htcondorce01.ge.infn.it:9619
        +remote_jobuniverse = 5
        +remote_ShouldTransferFiles = "YES"
        +remote_WhenToTransferOutput = "ON_EXIT_OR_EVICT"
        +remote_TransferOutput = ""
        +ioIntensity = 0
        +xcount = 8
        +maxMemory = 16000
        +remote_queue = "atlas"
        +maxWallTime = 2880

        delegate_job_GSI_credentials_lifetime = 0

        +ScitokensFile = "/the/token/path"

        queue 1


One can check more examples SDF file in `HTCondor docs <https://htcondor.readthedocs.io/en/latest/users-manual/submitting-a-job.html>`_ .

Examples of submission for both local and remote cases\:

.. tabs::

    .. code-tab:: text Local

        # Submit the SDF with condor_submit
        # Given the local node to be the harvester with hostname myharvester
        # Given "atlpan" the user which harvester runs with, and also can authenticate the remote condor schedd (depending on configuration on schedd node)
        [atlpan@myharvester ~]$ condor_submit /path/of/myjob.sdf


    .. code-tab:: text Remote

        # Submit the SDF with condor_submit
        # Given the local node to be the harvester with hostname myharvester
        # Given "atlpan" the user which harvester runs with, and also can authenticate the remote condor schedd (depending on configuration on schedd node)
        # Given the pool name and schedd name of remote schedd to be "myschedd.cern.ch:19618" and "myschedd.cern.ch"
        [atlpan@myharvester ~]$ condor_submit -pool myschedd.cern.ch:19618 -name myschedd.cern.ch /path/of/myjob.sdf


See more detailed descriptions about condor_submit and SDF file in `HTCondor docs (submitting-a-job) <https://htcondor.readthedocs.io/en/latest/users-manual/submitting-a-job.html>`_ . and `HTCondor docs (condor_submit)  <https://htcondor.readthedocs.io/en/latest/man-pages/condor_submit.html#submit-description-file-commands>`_ .


Prepare SDF template
""""""""""""""""""""

A submit description file template (JDL template), is a SDF with some values replaced with placeholders, so that it works as the template for generating real SDF files to submit. 

The placeholders are in the form of {keywords} (keywords between brackets, consistent with python fstring format). Harvester will resolve the placeholders with real values according to attributes of the worker to submit and/or the setup of the PanDA queue (PQ).

See :ref:`here <ref-all-placeholders>` for descriptions of all placeholders available.

One should prepare the SDF template according to the SDF file used for submitting successful test condor jobs. That is to say:

* Replace hard-coded values in the SDF with the placeholders available (usually about PQ and resource requirements)
* Set extra attributes to be corresponding placeholders in the SDF template for better harvester htcondor usage (e.g. ``+harvesterID`` and ``+harvesterWorkerID``, see below)


Note that:

* It is better to add ``+harvesterID = "{harvesterID}"`` and ``+harvesterWorkerID = "{workerID}"`` in the SDF template so that harvesterID and workerID are added to the condor job classads; thus the admin can easily query condor jobs on schedd about corresponding harvester workers. Moreover, these two lines in SDF template are mandatory if one wants to enable event-based htcondor_monitor.
* It is recommended to add ``+sdfPath = "{sdfPath}"`` so that one can track the path of SDF file of the condor job with its classads (can be queried with condor_q or condor_history).
*  For PUSH mode (1-to-1, 1-to-many, or many-to-1 pandaJob-worker mapping), pilot needs to be submitted together with the pre-fetched PanDA job(s) (fetched by harvester). Thus, in SDF template one should specify the job description file with ``{jobSpecFileName}`` placeholder (The true filename typically named ``pandaJobData.out`` or ``HPCJobs.json``, to be matched with pilot) to be one of the transfer_input_files of the condor job, like: ``transfer_input_files = {jobSpecFileName}``
* Assure the credentials (e.g. proxy certificate file, token) for the condor job to authenticate external components (e.g. PanDA server, CE) are set in the SDF template. For example ``x509userproxy=...`` , ``+ScitokensFile = "{tokenPath}"``
* Make sure one has one and only one ``queue 1`` at the end of SDF template, so that the condor job with a given workerID is submitted only once, as harvester expects that each harvester worker is mapped to one condor job.


Examples of complete SDF templates (and examples when their placeholders resolved by harvester during worker submission):

.. tabs::

    .. code-tab:: text ATLAS Grid PULL HTCondorCE SDF template

        executable = /cvmfs/atlas.cern.ch/repo/sw/PandaPilotWrapper/latest/runpilot2-wrapper.sh
        arguments = "-s {computingSite} -r {computingSite} -q {pandaQueueName} -j {pilotJobLabel} -i {pilotType} {pilotPythonOption} -w generic --pilot-user ATLAS --url https://pandaserver.cern.ch {pilotDebugOption} --harvester-submit-mode PULL --allow-same-user=False --job-type={pilotJobType} {pilotResourceTypeOption} --pilotversion {pilotVersion} {pilotUrlOption} {pilotArgs}"
        initialdir = {accessPoint}
        universe = grid
        log = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).log
        output = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).out
        error = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).err
        transfer_executable = True
        x509userproxy = {x509UserProxy}
        environment = "PANDA_JSID=harvester-{harvesterID} HARVESTER_ID={harvesterID} HARVESTER_WORKER_ID={workerID} GTAG={gtag} APFMON=http://apfmon.lancs.ac.uk/api APFFID={harvesterID} APFCID=$(Cluster).$(Process)"
        +harvesterID = "{harvesterID}"
        +harvesterWorkerID = "{workerID}"

        grid_resource = condor {ceHostname} {ceEndpoint}
        +remote_jobuniverse = 5
        +remote_ShouldTransferFiles = "YES"
        +remote_WhenToTransferOutput = "ON_EXIT_OR_EVICT"
        +remote_TransferOutput = ""
        #+remote_RequestCpus = {nCoreTotal}
        #+remote_RequestMemory = {requestRam}
        #+remote_RequestDisk = {requestDisk}
        #+remote_JobMaxVacateTime = {requestWalltime}
        +ioIntensity = {ioIntensity}
        +xcount = {nCoreTotal}
        +maxMemory = {requestRam}
        +remote_queue = "{ceQueueName}"
        +maxWallTime = {requestWalltimeMinute}

        delegate_job_GSI_credentials_lifetime = 0

        #+remote_Requirements = JobRunCount == 0
        periodic_remove = (JobStatus == 2 && (CurrentTime - EnteredCurrentStatus) > 604800)
        #+remote_PeriodicHold = ( JobStatus==1 && gridjobstatus=?=UNDEFINED && CurrentTime-EnteredCurrentStatus>3600 ) || ( (JobRunCount =!= UNDEFINED && JobRunCount > 0) ) || ( JobStatus == 2 && CurrentTime-EnteredCurrentStatus>604800 )
        +remote_PeriodicRemove = (JobStatus == 5 && (CurrentTime - EnteredCurrentStatus) > 3600) || (JobStatus == 1 && globusstatus =!= 1 && (CurrentTime - EnteredCurrentStatus) > 86400)

        +sdfPath = "{sdfPath}"
        +ScitokensFile = "{tokenPath}"

        +RequireGPUs = {requireGpus}
        +RequestGPUs = {requestGpus}

        {customSubmitAttributes}

        queue 1


    .. code-tab:: text SDF resolved

        executable = /cvmfs/atlas.cern.ch/repo/sw/PandaPilotWrapper/latest/runpilot2-wrapper.sh
        arguments = "-s INFN-GENOVA -r INFN-GENOVA -q INFN-GENOVA -j unified -i PR --pythonversion 3 -w generic --pilot-user ATLAS --url https://pandaserver.cern.ch  --harvester-submit-mode PULL --allow-same-user=False --job-type=unified --resource-type MCORE --pilotversion 3.7.7.3  "
        initialdir = /cephfs/atlpan/harvester/harvester_wdirs/CERN_central_B/70/41/549447041
        universe = grid
        log = /data2/atlpan/condor_logs/24-06-18_08/grid.$(Cluster).$(Process).log
        output = /data2/atlpan/condor_logs/24-06-18_08/grid.$(Cluster).$(Process).out
        error = /data2/atlpan/condor_logs/24-06-18_08/grid.$(Cluster).$(Process).err
        transfer_executable = True
        x509userproxy = /cephfs/atlpan/harvester/proxy/x509up_u25606_prod
        environment = "PANDA_JSID=harvester-CERN_central_B HARVESTER_ID=CERN_central_B HARVESTER_WORKER_ID=549447041 GTAG=https://aipanda024.cern.ch/condor_logs_2/24-06-18_08/grid.$(Cluster).$(Process).out APFMON=http://apfmon.lancs.ac.uk/api APFFID=CERN_central_B APFCID=$(Cluster).$(Process)"
        +harvesterID = "CERN_central_B"
        +harvesterWorkerID = "549447041"

        grid_resource = condor htcondorce01.ge.infn.it htcondorce01.ge.infn.it:9619
        +remote_jobuniverse = 5
        +remote_ShouldTransferFiles = "YES"
        +remote_WhenToTransferOutput = "ON_EXIT_OR_EVICT"
        +remote_TransferOutput = ""
        +ioIntensity = 0
        +xcount = 8
        +maxMemory = 16000
        +remote_queue = "atlas"
        +maxWallTime = 2880

        delegate_job_GSI_credentials_lifetime = 0

        periodic_remove = (JobStatus == 2 && (CurrentTime - EnteredCurrentStatus) > 604800)
        +remote_PeriodicRemove = (JobStatus == 5 && (CurrentTime - EnteredCurrentStatus) > 3600) || (JobStatus == 1 && globusstatus =!= 1 && (CurrentTime - EnteredCurrentStatus) > 86400)

        +sdfPath = "/cephfs/atlpan/harvester/harvester_wdirs/CERN_central_B/70/41/549447041/tmprgiecjw1_submit.sdf"
        +ScitokensFile = "/cephfs/atlpan/harvester/tokens/ce/prod/51b46f15b21a96bce7147c1f9f455105"

        +RequireGPUs = False
        +RequestGPUs = 0



        queue 1


.. tabs::

    .. code-tab:: text ATLAS Grid PUSH ARC-CE SDF template

        executable = /cvmfs/atlas.cern.ch/repo/sw/PandaPilotWrapper/latest/runpilot2-wrapper.sh
        arguments = "-s {computingSite} -r {computingSite} -q {pandaQueueName} -j {pilotJobLabel} -i {pilotType} {pilotPythonOption} -w generic --pilot-user ATLAS --url https://pandaserver.cern.ch {pilotDebugOption} --harvester-submit-mode PUSH {pilotResourceTypeOption} --pilotversion {pilotVersion} {pilotUrlOption} {pilotArgs}"
        initialdir = {accessPoint}
        universe = grid
        log = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).log
        output = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).out
        error = {logDir}/{logSubdir}/grid.$(Cluster).$(Process).err
        transfer_executable = True
        x509userproxy = {x509UserProxy}
        environment = "PANDA_JSID=harvester-{harvesterID} HARVESTER_ID={harvesterID} HARVESTER_WORKER_ID={workerID} GTAG={gtag} APFMON=http://apfmon.lancs.ac.uk/api APFFID={harvesterID} APFCID=$(Cluster).$(Process)"
        +harvesterID = "{harvesterID}"
        +harvesterWorkerID = "{workerID}"
        should_transfer_files = True
        transfer_input_files = {jobSpecFileName}

        grid_resource = arc {ceEndpoint}

        arc_resources = <QueueName>{ceQueueName}</QueueName> \
                        <RuntimeEnvironment> \
                            <Name>APPS/HEP/ATLAS-SITE-LCG</Name> \
                        </RuntimeEnvironment> \
                        <RuntimeEnvironment> \
                            <Name>ENV/PROXY</Name> \
                        </RuntimeEnvironment> \
                        <SlotRequirement> \
                            <NumberOfSlots>{nCoreTotal}</NumberOfSlots> \
                            <SlotsPerHost>{nCoreTotal}</SlotsPerHost> \
                        </SlotRequirement> \
                        <IndividualPhysicalMemory>{requestRamBytesPerCore}</IndividualPhysicalMemory> \
                        <WallTime>{requestWalltime}</WallTime> \
                        <TotalCPUTime>{requestCputime}</TotalCPUTime>

        arc_rte = APPS/HEP/ATLAS-SITE-LCG,ENV/PROXY

        +remote_jobuniverse = 5
        +remote_requirements = True
        +remote_ShouldTransferFiles = "YES"
        +remote_WhenToTransferOutput = "ON_EXIT"
        +remote_TransferOutput = ""

        #+remote_RequestCpus = {nCoreTotal}
        #+remote_RequestMemory = {requestRam}
        #+remote_RequestDisk = {requestDisk}
        #+remote_JobMaxVacateTime = {requestWalltime}
        +ioIntensity = {ioIntensity}

        #+remote_Requirements = JobRunCount == 0
        periodic_remove = (JobStatus == 2 && (CurrentTime - EnteredCurrentStatus) > 604800)
        #+remote_PeriodicHold = ( JobStatus==1 && gridjobstatus=?=UNDEFINED && CurrentTime-EnteredCurrentStatus>3600 ) || ( (JobRunCount =!= UNDEFINED && JobRunCount > 0) ) || ( JobStatus == 2 && CurrentTime-EnteredCurrentStatus>604800 )
        +remote_PeriodicRemove = (JobStatus == 5 && (CurrentTime - EnteredCurrentStatus) > 3600) || (JobStatus == 1 && globusstatus =!= 1 && (CurrentTime - EnteredCurrentStatus) > 86400)

        +sdfPath = "{sdfPath}"

        queue 1


    .. code-tab:: text SDF resolved

        executable = /cvmfs/atlas.cern.ch/repo/sw/PandaPilotWrapper/latest/runpilot2-wrapper.sh
        arguments = "-s LRZ-LMU_TEST -r LRZ-LMU_TEST -q LRZ-LMU_TEST -j managed -i PR --pythonversion 3 -w generic --pilot-user ATLAS --url https://pandaserver.cern.ch  --harvester-submit-mode PUSH --resource-type SCORE --pilotversion 3.7.7.3  "
        initialdir = /cephfs/atlpan/harvester/harvester_wdirs/CERN_central_B/55/91/551155591
        universe = grid
        log = /data2/atlpan/condor_logs/24-06-25_07/grid.$(Cluster).$(Process).log
        output = /data2/atlpan/condor_logs/24-06-25_07/grid.$(Cluster).$(Process).out
        error = /data2/atlpan/condor_logs/24-06-25_07/grid.$(Cluster).$(Process).err
        transfer_executable = True
        x509userproxy = /cephfs/atlpan/harvester/proxy/x509up_u25606_prod
        environment = "PANDA_JSID=harvester-CERN_central_B HARVESTER_ID=CERN_central_B HARVESTER_WORKER_ID=551155591 GTAG=https://aipanda157.cern.ch/condor_logs_2/24-06-25_07/grid.$(Cluster).$(Process).out APFMON=http://apfmon.lancs.ac.uk/api APFFID=CERN_central_B APFCID=$(Cluster).$(Process)"
        +harvesterID = "CERN_central_B"
        +harvesterWorkerID = "551155591"
        transfer_input_files = pandaJobData.out

        grid_resource = condor lcg-lrz-ce0.grid.lrz.de lcg-lrz-ce0.grid.lrz.de:9619
        +remote_jobuniverse = 5
        +remote_ShouldTransferFiles = "YES"
        +remote_WhenToTransferOutput = "ON_EXIT_OR_EVICT"
        +remote_TransferOutput = ""
        +ioIntensity = 0
        +xcount = 1
        +maxMemory = 1674
        +remote_queue = "atlas"
        +maxWallTime = 39

        delegate_job_GSI_credentials_lifetime = 0

        periodic_remove = (JobStatus == 2 && (CurrentTime - EnteredCurrentStatus) > 604800)
        +remote_PeriodicRemove = (JobStatus == 5 && (CurrentTime - EnteredCurrentStatus) > 3600) || (JobStatus == 1 && globusstatus =!= 1 && (CurrentTime - EnteredCurrentStatus) > 86400)

        +sdfPath = "/cephfs/atlpan/harvester/harvester_wdirs/CERN_central_B/55/91/551155591/tmpsrmx85mv_submit.sdf"
        +ScitokensFile = "/cephfs/atlpan/harvester/tokens/ce/prod/304874bac7d0e6691ab68356abc700ba"

        +RequireGPUs = False
        +RequestGPUs = 0



        queue 1



For ATLAS Grid, check `here <https://github.com/PanDAWMS/harvester_configurations/tree/master/GRID/condor_sdf_templates>`_. for all common SDF templates.



Configure htcondor plugins in ququeconfig
""""""""""""""""""""""""""""""""""""""""""

With the condor schedd and SDF template ready, one can configure the queueconfig for harvester to serve a PQ with htcondor plugins: htcondor_submitter, htcondor_monitor and htcondor_sweeper.

Submitter plugin
~~~~~~~~~~~~~~~~

To use htcondor_submitter plugin, set ``"module": "pandaharvester.harvestersubmitter.htcondor_submitter"`` and ``"name": "HTCondorSubmitter"`` in ``submitter`` section of the queue in the queueconfig, and the attributes of htcondor_submitter as well.

Examples of submitter section in of certain PQ in DOMA and ATLAS respectively\:

.. tabs::

    .. code-tab:: text DOMA

        "submitter": {
            "module": "pandaharvester.harvestersubmitter.htcondor_submitter",
            "name": "HTCondorSubmitter",
            "logBaseURL": "https://panda-doma.cern.ch/condor_logs/condor_logs",
            "logDir": "/var/log/condor_logs/condor_logs",
            "nProcesses": 8,
            "templateFile": "/opt/harvester/sandbox/cnaf_darkside.submit_pilot_token_push.sdf",
            "useCRIC": true,
            "useCRICGridCE": false,
            "x509UserProxy": "/data/harvester/darkside.short.proxy"
        },


    .. code-tab:: text ATLAS

        "submitter": {
            "module": "pandaharvester.harvestersubmitter.htcondor_submitter",
            "name": "HTCondorSubmitter",
            "CEtemplateDir": "/cephfs/atlpan/harvester/harvester_configurations/GRID/condor_sdf_templates/atlas-grid-ce_pull.sdf.d",
            "condorHostConfig": "/opt/harvester/etc/panda/condor_host_config.json",
            "logBaseURL": "https://[ScheddHostname]/condor_logs_2",
            "logDir": "/data2/atlpan/condor_logs",
            "nProcesses": 8,
            "payloadType": "atlas_pilot_wrapper",
            "rcPilotRandomWeightPermille": 10,
            "tokenDir": "/cephfs/atlpan/harvester/tokens/ce/prod",
            "tokenDirAnalysis": "/cephfs/atlpan/harvester/tokens/ce/pilot",
            "useCRICGridCE": true,
            "x509UserProxy": "/cephfs/atlpan/harvester/proxy/x509up_u25606_prod",
            "x509UserProxyAnalysis": "/cephfs/atlpan/harvester/proxy/x509up_u25606_pilot"
        },


Note that:

* Be aware of how the schedd instances are put in the config. Schedd instances can be put in with ``condorHostConfig`` attribute (recommended, see :ref:`here <ref-condor-host-config>`), or with the combination of ``condorPool`` and ``condorSchedd`` attributes 
* Be aware of how the SDF template is passed in the configuration. It can be passed with ``templateFile`` attribute (simple and straightforward), or indirectly with ``CEtemplateDir`` attribute (along with configuraions of CEs on CRIC)


See :ref:`here <ref-htcondor_submitter>` for descriptions of all configurable attributes and details of htcondor_submitter.


Monitor plugin
~~~~~~~~~~~~~~

To use htcondor_monitor plugin, set ``"module": "pandaharvester.harvestermonitor.htcondor_monitor"`` and ``"name": "HTCondorMonitor"`` in ``monitor`` section of the queue in the queueconfig, and the attributes of htcondor_monitor as well.

Examples of monitor section in of certain PQ in DOMA and ATLAS respectively\:

.. tabs::

    .. code-tab:: text DOMA

        "monitor": {
            "module": "pandaharvester.harvestermonitor.htcondor_monitor",
            "name": "HTCondorMonitor"
        },


    .. code-tab:: text ATLAS

        "monitor": {
            "module": "pandaharvester.harvestermonitor.htcondor_monitor",
            "name": "HTCondorMonitor"
        },


See :ref:`here <ref-htcondor_monitor>` for descriptions of all configurable attributes and details of htcondor_monitor.


Sweeper plugin
~~~~~~~~~~~~~~

To use htcondor_sweeper plugin, set ``"module": "pandaharvester.harvestersweeper.htcondor_sweeper"`` and ``"name": "HTCondorSweeper"`` in ``sweeper`` section of the queue in the queueconfig, and the attributes of htcondor_sweeper as well.

Examples of sweeper section in of certain PQ in DOMA and ATLAS respectively\:

.. tabs::

    .. code-tab:: text DOMA

        "sweeper": {
            "module": "pandaharvester.harvestersweeper.htcondor_sweeper",
            "name": "HTCondorSweeper"
        },


    .. code-tab:: text ATLAS

        "sweeper": {
            "module": "pandaharvester.harvestersweeper.htcondor_sweeper",
            "name": "HTCondorSweeper"
        },


See :ref:`here <ref-htcondor_sweeper>` for details of htcondor_sweeper.


Common section
~~~~~~~~~~~~~~

One can put attributes in common section, which will be passed to all plugins.

Although curretly htcondor plugins do not really require common attributes so far, it is good to put general attributes (that may be used by multiple htcondor plugins in the future) in the common section.

Examples of common section in of certain PQ in ATLAS\:

.. tabs::

    .. code-tab:: text ATLAS

        "common": {
            "payloadType": "atlas_pilot_wrapper"
        }



|br|

|br|


.. _ref-all-placeholders:

Placeholders in SDF template
----------------------------

The placeholders are in the form of {keywords} (keywords between brackets, consistent with python fstring format).

All placeholders available
""""""""""""""""""""""""""

* ``{accessPoint}``: The directory path where harvester put files for payload interaction about the worker. Specified from accessPoint in messenger section. Usually accessPoint is under a (shared) filesystem which both the Harvester and the Condor schedd service can access
* ``{ceEndpoint}``: Endpoint (usually hostname with prefix and/or port) of the computing element (CE). According to the PQ setup in local configuration or on CRIC ("ce_endpoint"). If one or more CEs are configured, one of the active CEs will be chosen (based on a weighting algorithm) for the worker and its endpoint will be put in ``{ceEndpoint}``
* ``{ceFlavour}``: Type (flavor) of the computing element (CE). Specified from the PQ setup on CRIC ("ce_flavour"). This placeholder is only useful when htcondor_submitter attribute useCRICGridCE = true .
* ``{ceHostname}``: Hostname of the computing element (CE). According to the PQ setup in local configuration or on CRIC (short hostname in "ce_endpoint"). If one or more CEs are configured, one of the active CEs will be chosen (based on a weighting algorithm) for the worker and its hostname will be put in ``{ceHostname}``
* ``{ceJobmanager}``: Type of job manager behind the computing element (CE). Specified from the PQ setup on CRIC ("ce_jobmanager"). This placeholder is only useful when htcondor_submitter attribute useCRICGridCE = true .
* ``{ceQueueName}``: Internal queue inside the computing element (CE) to be used (not to be confused with PanDA queue). Specified from the PQ setup on CRIC ("ce_queue_name"). This placeholder is only useful when htcondor_submitter attribute useCRICGridCE = true .
* ``{ceVersion}``: Version of the computing element (CE) to be used (not to be confused with PanDA queue). Specified from the PQ setup on CRIC ("ce_version"). This placeholder is only useful when htcondor_submitter attribute useCRICGridCE = true .
* ``{computingSite}``: Computing site to which the worker to submit. According the worker. Usually ``{computingSite}`` and {pandaQueueName} are identical
* ``{customSubmitAttributes}``: Custom condor submit attributes to append to the SDF file, in the form "+key = value". According to PQ setup on CRIC (associate parameters "jdl.plusattr.<key>" where <key> is the attribute key name).
* ``{executableFile}``: Path of the executable file to submit. Specified from htcondor_submitter attribute executableFile
* ``{gtag}``: The URL for the pilot log (usually stdout of the condor job) of the worker. According to htcondor_submitter attribute logBaseURL (which points to logDir) and the worker. Note the functionality to export logs has to be done additionally outside harvester (e.g. httpd file server)
* ``{harvesterID}``: harvesterID of this Harvester instance. According to harvester configuration
* ``{ioIntensity}``: IO intensity (data traffics over WAN) requested by the worker. According to the PQ or the worker.
* ``{jobSpecFileName}``: The filename of PanDA job description file (not to be confused with condor SDF) for payload interaction. For PUSH mode, the job description file needs to be set as an input file of the condor job. Specified from messenger.jobSpecFileName of the PQ in queueconfig, or harvester_config.payload_interaction.jobSpecFileName in harvester configuration. 
* ``{jobType}``: jobType (for internal harvester) of the worker. According to the worker. 
* ``{logDir}``: Path of the custom base directory to store logs of condor jobs. Specified from htcondor_submitter attribute logDir. By default, the real logs should be put under ``{logDir}/{logSubdir}``.
* ``{logSubdir}``: Path of the sub-directory for logs of condor jobs. The sub-directory name will be auto-generated with the date and time "yy-mm-dd_HH", which is useful to distribute logs into according to sub-directories according to workers' submission time.
* ``{nCoreFactor}``: A factor to adjust number of cores requested by the worker. Specified from htcondor_submitter attribute nCoreFactor (or default value 1)
* ``{nCorePerNode}``: Number of cores per node requested by the worker. According to the PQ or the worker
* ``{nCoreTotal}``: Number of total cores requested by the worker. According to the PQ or the worker
* ``{nNode}``: Number of nodes requested by the worker. According to the PQ or the worker
* ``{pandaQueueName}``: PanDA queue (PQ) name of the worker. According to the PQ
* ``{pilotArgs}``: Custom pilot arguments to append to pilot/wrapper command. According to PQ setup on CRIC (associate parameter "pilot_args").
* ``{pilotDebugOption}``: Default pilot debug option to append to pilot/wrapper command (empty string or "-d"). According to the prodSourceLabel of the worker. For "ptest" and "rc_test2" the value is "-d", and for the rest it is empty string.
* ``{pilotJobLabel}``: Pilot job label option to pass to pilot "-j" flag. According to the worker.
* ``{pilotJobType}``: Pilot job type option to pass to pilot "--job-type" flag. According to the worker.
* ``{pilotPythonOption}``: Python (to run pilot) version option to append to pilot/wrapper command (empty string or "--pythonversion <the_version>"). According to PQ setup on CRIC ("python_version").
* ``{pilotResourceTypeOption}``: equivalent to ``--resource-type {resourceType}``, resourceType for pilot resource-type option. According to the PQ and the worker. 
* ``{pilotType}``: Pilot type option to pass to pilot "-i" flag. According to the worker.
* ``{pilotUrlOption}``: Pilot url option to append to pilot/wrapper command (empty string or "--piloturl <the_url>"). According to PQ setup on CRIC (associate parameter  "pilot_url").
* ``{pilotVersion}``: Pilot version to pass to pilot "--pilotversion" flag. According to PQ setup on CRIC ("pilot_version").
* ``{prodSourceLabel}``: prodSourceLabel of the worker. Specified from htcondor_submitter attribute prodSourceLabel. Should match prodSourceLabel of corresponding PanDA jobs.
* ``{requestCputime}``: CPU time requested by the worker in seconds. According to the PQ or the worker
* ``{requestCputimeMinute}``: CPU time requested by the worker in minutes. According to the PQ or the worker
* ``{requestDisk}``: Disk space requested by the worker in KB. Derived from the PQ or the worker
* ``{requestGpus}``: Number of GPUs the worker requests. According to the worker and the PQ setup on CRIC (whether "resource_type" = "gpu"). Currently the number is always 1 or 0
* ``{requestRam}``: Memory requested by the worker in MB. According to the PQ or the worker
* ``{requestRamBytes}``: Memory requested by the worker in bytes. According to the PQ or the worker
* ``{requestRamBytesPerCore}``: Memory per core requested by the worker in bytes. According to the PQ or the worker
* ``{requestRamPerCore}``: Memory per core requested by the worker in MB. According to the PQ or the worker
* ``{requestWalltime}``: Walltime requested by the worker in seconds. According to the PQ or the worker
* ``{requestWalltimeMinute}``: Walltime requested by the worker in minutes. According to the PQ or the worker
* ``{requireGpus}``: Whether the worker requires GPU. According to the worker and the PQ setup on CRIC (whether "resource_type" = "gpu").
* ``{resourceType}``: resourceType of the worker. According to the PQ and the worker.
* ``{sdfPath}``: Path of the SDF file. Derived from htcondor_submitter attribute templateFile or CEtemplateDir
* ``{submissionHost}``: Hostname of the submission host of the worker. According to the worker.
* ``{submissionHostShort}``: Short hostname of the submission host of the worker. According to the worker.
* ``{tokenDir}``: Path of directory of tokens to authenticate CEs (containing all tokens, one for each CE). Specified from htcondor_submitter attribute tokenDir or tokenDirAnalysis (for analysis in unified case). The internal algorithm will select the very token corresponding to the CE in the directory to submit the worker with.
* ``{tokenFilename}``: Filename of the token selected.
* ``{tokenPath}``: Complete file path of the token selected, equivalent to ``{tokenDir}/{tokenFilename}``.
* ``{workerID}``: workerID of the worker to submit. According to the worker
* ``{x509UserProxy}``: Path of the x509 user proxy certificate. Specified from htcondor_submitter attribute x509UserProxy


|br|

.. _ref-htcondor_submitter:

htcondor_submitter
------------------

htcondor_submitter generates the real SDF file according to the SDF template, the worker and PQ setup, and then submits condor job with SDF file to the condor schedd.


Attributes of htcondor_submitter
""""""""""""""""""""""""""""""""

* ``"CEtemplateDir"``: Path of the directory containing SDF templates, one for each CE flavor. Only useful when useCRICGridCE = true, so that harvester selects one of the CEs on CRIC, and get the correct template file in CEtemplateDir according to the CE flavor (also set on CRIC "ce_flavour"). Will be ignored if templateFile is set. Currently the valid filename of SDF templates under CEtemplateDir should be either *htcondor-ce.sdf* for HTCondorCE or *arc-ce_arc.sdf* for ARC CE REST interface. Default is false
* ``"condorHostConfig"``: Path of JSON config file of remote condor hosts: condor schedds/pools and their weighting. For each worker, one of condor hosts in condorHostConfig will be selected, with probability according to the given weight, and harvester will submit **from** this condor host (not to be confused with batch-systems or CEs of the PQ, where submits **to**). If set, condorSchedd and condorPool are ignored. Default is null
* ``"condorPool"``: Condor pool name (condor collector). If there are multiple condor schedds/pools, use condorHostConfig instead. Default is null, i.e. localhost:9618
* ``"condorSchedd"``: Condor schedd name. If there are multiple condor schedds/pools, use condorHostConfig instead. Default is null, i.e. localhost
* ``"executableFile"``: Executable file of the condor jobs; only used for SDF template placeholder. Default is null
* ``"logBaseURL"``: Base URL of the file server which exports logDir. Default is null. logBaseURL will be used to construct real URL of the log files (stdout and stderr of the payload, and condor job log) for monitoring. The value of logBaseURL may contain a special placeholder ``[ScheddHostname]``, which will be resolved to the hostname of the condor schedd which hosts the job of the worker - this is useful when harvester submits through multiple condor schedd instances and the job logs are meant to stay on the condor schedd instances to export. Note that the file server (e.g. by apache) for exporting logs should be set up by the admin in addition to the harvester or condor service. 
* ``"logDir"``: Path of the custom base directory to store logs of condor jobs; only used for SDF template placeholder. Default is environment variable $TMPDIR or "/tmp"
* ``"minBulkToRandomizedSchedd"``: Number of minimum workers in a cycle that could be submitted from multiple condor hosts. If number of workers in a submitter cycle is less than minBulkToRandomizedSchedd, all the workers will be bulkily submitted from only one condor host. Default is 20
* ``"nCoreFactor"``: Factor to adjust number of cores requested by the worker. Default is 1
* ``"nProcesses"``: Number of processes (threads) for htcondor_submitter to submit. Default is 1
* ``"rcPilotRandomWeightPermille"``: Probability permille (per thousand) to randomly run PR pilot with RC pilot url. Default is 0; i.e. never
* ``"templateFile"``: Path of SDF template file. Default is null
* ``"tokenDir"``: Default token directory for a queue; only used for SDF template placeholder {token*} Default is null
* ``"tokenDirAnalysis"``: token directory for analysis workers in grandly unified queues (should not be used for unified dispatch); only used for SDF template placeholder {token*} if the worker is analysis. Default is null
* ``"useAnalysisCredentials"``: Try to use analysis credentials first. Default is false
* ``"useCRIC"``: Whether to use CRIC; i.e. to fill worker attributes and some SDF template placeholders with the PQ setup on CRIC. If false, the SDF template placeholders depending on CRIC (non-empty "harvester_template") should not be used. Default is false
* ``"useCRICGridCE"``: Whether to select Grid CEs from PQ setup on CRIC. If true, useCRIC will be overwritten to be true as well and for each worker, one of the CEs on CRIC will be selected (weighted by an internal algorithm) to submit the worker to. For Grid, useful with CEtemplateDir attribute. Default is false
* ``"useFQDN"``: Whether to use FQDN for harvester internal record. If false or null, short hostname is used. Default is null
* ``"useSpool"``: Whether to use condor spool mechanism. If false, need shared FS across remote schedd. Default is false
* ``"x509UserProxy"``: x509 user proxy; only used for SDF template placeholder ``{x509UserProxy}``. Default is null
* ``"x509UserProxyAnalysis"``: x509 user proxy for analysis workers in grandly unified queues (should not be used for unified dispatch); only used for SDF template placeholder ``{x509UserProxy}`` if the worker is analysis. Default is null


.. _ref-condor-host-config:

Configuration file for condorHostConfig
"""""""""""""""""""""""""""""""""""""""

The configuration file for ``condorHostConfig`` attribute is meant to describe all schedd instances the PQ can submit through with a given weight (proportion to the probability the schedd is selected to submit through). It is useful when there are multiple remote schedd instances.

It shoul be written in JSON with the form:\

.. code-block:: text

    {
        "schedd_name_1": {
            "pool": "pool_name_1",
            "weight": an_integer
        },
        "schedd_name_2": {
            "pool": "pool_name_2",
            "weight": an_integer
        },
        ...
    }

Where schedd_name_* and pool_name_* are the schedd name and pool name of the schedd instances, and the weight is an positive integer indicating the relative chance to choose the schedd instance (the final probability will be normalized over weights of all schedd instances).

Example of the JSON configuration file for ``condorHostConfig`` \:

.. code-block:: text

    {
        "myschedd1.cern.ch": {
            "pool": "myschedd1.cern.ch:19618",
            "weight": 1
        },
        "myschedd2.cern.ch": {
            "pool": "myschedd2.cern.ch:19618",
            "weight": 2
        },
        "myschedd3.cern.ch": {
            "pool": "myschedd3.cern.ch:19618",
            "weight": 3
        },
        "myschedd4.cern.ch": {
            "pool": "myschedd4.cern.ch:19618",
            "weight": 4
        }
    }


Here in the example one has 4 schedd instances, with probability 10%, 20%, 30% and 40% respectively.


|br|

.. _ref-htcondor_monitor:

htcondor_monitor
------------------

htcondor_monitor communicates with the condor schedd to fetch the status of condor jobs and translate them into workers status to update the workers. 

htcondor_monitor supports event-based monitor check (to be explained) feature.


Attributes of htcondor_monitor
""""""""""""""""""""""""""""""

* ``"cacheEnable"``: Whether to enable cache for htcondor_monitor to cache status of condor jobs in FIFO DB. Default follows monitor.pluginCacheEnable if set in harvester configuration, else false.
* ``"cacheRefreshInterval"``: Factor to adjust number of cores requested by the worker. Default follows harvester_config.monitor.pluginCacheRefreshInterval if set in harvester configuration, else follows monitor.checkInterval in harvester configuration
* ``"cancelUnknown"``: Whether to use consider workers to be cancelled when the status of their corresponding condor jobs is unknown (due to condor problem, connection issue, etc). If true, htcondor_monitor will mark the workers to be cancelled (a terminal status), attempt to kill the corresponding condor jobs, and will not check the workers any longer. If false, the workers will be checked again in next monitor cycle. Default is false
* ``"condorHostConfig_list"``: The extra list of condor host config files (appended to the list from eventBasedPlugins.condorHostConfig_list in harvester configuration) for htcondor_monitor to check and cache. Note condorHostConfig_list in queueconfig is only useful when event-based in enabled and htcondor_monitor event-based plugin is configured in harvester configuration (eventBasedEnable = true, eventBasedPlugins contains module=pandaharvester.harvestermonitor.htcondor_monitor, name=HTCondorMonitor, condorHostConfig_list is set). Default is null
* ``"heldTimeout"``: Timeout in seconds for a worker whose condor jobs in held status to be considered failed. Default is 3600, aka 1 hour
* ``"nProcesses"``: Number of processes (threads) for htcondor_monitor to query condor job status. Default is 1
* ``"payloadType"``: The type of payload, for the purpose of adding additional error messages according to the payload exit code. Default is null
* ``"useCondorHistory"``: Whether to query condor schedd the condor history. Default is true


|br|

.. _ref-htcondor_sweeper:

htcondor_sweeper
------------------

htcondor_sweeper kills condor jobs when corresponding workers are to be killed and cleaned up preparator directories for stage-in files (if there are any) after workers terminated.


Attributes of htcondor_sweeper
""""""""""""""""""""""""""""""

No customizable attribute yet.