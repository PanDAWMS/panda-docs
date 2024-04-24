======================================================
Descriptions of Task Parameters Dictating Behavior
======================================================

Tasks are defined by a range of parameters that dictate their behavior. Certain parameters are encoded as two-letter codes
in the ``splitRule`` attribute of the task. Below are the task parameters, accompanied by their complete descriptions and,
where applicable, corresponding two-letter codes.

allowEmptyInput (AE)
    The task will be allowed to go to finished instead of failed even if the input dataset is empty.

addNthFieldToLFN (AN)
    The task will add the N-th field of the input dataset name to the LFN of the output files.

allowPartialFinish (AP)
    Jobs in the task will be allowed to go to finished instead of failed even if they don't process some of the input files successfully.

altStageOut (AT)
    If set to "on", jobs in the task will use the alternative stage-out mechanism for PQs if the mechanism is available there.
    If set to "force", jobs will be assigned to PQs where the alternative stage-out mechanism is available and use it.

avoidVP (AV)
    The task will avoid PQs which use Virtual Placement.

maxCoreCount (CC)
    The maximum number of CPU cores that can be used by a single job in the task.

cloudAsVO (CV)
    If set to True, the task will use the cloud ``attribute`` as a VO.

ddmBackEnd (DE)
    The DDM backend name to use for the task.

disableAutoFinish (DF)
    If set to True, the task will not automatically go to finished due to timeout.

disableReassign (DI)
    If set to True, jobs in the task will not be automatically reassigned to another PQ due to timeout.

debugMode (DM)
    If set to True, jobs in the task will run in debug mode to send stdout.

disableAutoRetry (DR)
    If set to True, the task will not automatically retry failed jobs. Internally maxAttempt is set to 1.

dynamicNumEvents (DY)
    The minimum granularity to set the number of events per job dynamically.

nEsConsumers (EC)
    The number of Event Service consumers for each job in the task.

nEventsPerInput (EI)
    The number of events per input file. If set, the n_events metadata in DDM will be ignored.

encJobParams (EJ)
    The job parameters will be encrypted using Base64 encoding algorithm when jobs are being dispatched.

nEventsPerWorker (ES)
    The number of events per event range defined for Event Service jobs.

firstContentsFeed (FC)
    1 if the task does not yet feed input dataset contents to the database, 0 otherwise.

failGoalUnreached (FG)
    The task will go to failed if the goal is not reached.

fineGrainedProc (FP)
    Jobs in the task will keep track of processing using the event service mechanism.

firstEvent (FT)
    The first event number to process.

fullChain (FU)
    The task will use the full chain mechanism to be assigned to the nucleus based on the parent task.

groupBoundaryID (GB)
    The group boundary ID to split input.

hpoWorkflow (HO)
    The task will use the Hyper Parameter Optimization workflow.

instantiateTmplSite (IA)
    The task will instantiate output datasets at each PQ where jobs run.

inFilePosEvtNum (IF)
    The input file has positional event number.

ipStack (IK)
    The IP stack to use for the task. "IPv4" or "IPv6".

allowInputLAN (IL)
    If set to "use", the task will allow input files to be directly read over LAN.
    If set to "only", the task will only read input files over LAN.

ignoreMissingInDS (IM)
    The task will ignore missing input datasets which are deleted after the task is submitted.

intermediateTask (IN)
    The task is an intermediate task in a full-chain.

ipConnectivity (IP)
    The network connectivity requirement for the task. "full" or "http".

inputPreStaging (IS)
    The input of the task will be pre-staged by data carousel.

instantiateTmpl (IT)
    The task will instantiate output datasets using the template datasets.

allowInputWAN (IW)
    The task will allow input files to be directly read over WAN.

noLoopingCheck (LC)
    The task will disable the check for looping jobs.

useLocalIO (LI)
    The task will always copy input files to scratch disk even if PQs are configured to read input files over LAN.

limitedSites (LS)
    The task will use only limit PQs specified or unspecified in the task.

loadXML (LX)
    The task will load the XML file to generate jobs.

minCpuEfficiency (MC)
    The minimum CPU efficiency to be allowed for the task. If the CPU efficiency is lower than this value, the task will go to exhausted.

messageDriven (MD)
    The task will use the message-driven mechanism for internal communication among system components.

mergeEsOnOS (ME)
    The task will merge event service outputs on the object store where the output files are stored.

nMaxFilesPerJob (MF)
    The maximum number of input files to be processed by a single job in the task.

maxJumboPerSite (MJ)
    The maximum number of jumbo jobs to be assigned to a single PQ.

maxNumJobs (MN)
    The maximum number of jobs to be generated for a single HPO task.

mergeOutput (MO)
    The task will merge output files.

multiStepExec (MS)
    Each job in the task will execute the payload in multiple steps.

maxWalltime (MW)
    The maximum walltime for a single job in the task.

maxEventsPerJob (MX)
    The maximum number of events to be processed by a single job in the task when the number of events is set dynamically.

noExecStrCnv (NC)
    The pilot doesn't convert the execution string when executing the payload.

notDiscardEvents (ND)
    The task will not discard events when retrying event service jobs.

nEvents
    The total number of events to be processed by the task.

nEventsPerJob (NE)
    The number of events to be processed by a single job in the task.

nFiles
    The total number of input files to be processed by the task.

nFilesPerJob (NF)
    The number of input files to be processed by a single job in the task.

nGBPerJob (NG)
    The maximum input size in GB to be processed by a single job in the task.

noInputPooling (NI)
    The task will not use input pooling so that it will generate a job as soon as one input is ready.

nJumboJobs (NJ)
    The number of jumbo jobs to be generated for the task.

nSitesPerJob (NS)
    The number of PQs to be used for a group of event service consumers.

nChunksToWait (NT)
    The number of chunks to wait before generating jobs.

noWaitParent (NW)
    The task will not wait for the parent task to finish and will start processing while the parent task is running.

orderInputBy (OI)
    The input files will be ordered by the specified attribute.

orderByLB (OL)
    The input files will be ordered by the lumi block number.

onSiteMerging (OM)
    The task will merge output files on the PQ where the output files are stored.

osMatching (OS)
    The task will require operating system matching for the PQs.

onlyTagsForFC (OT)
    The task will use only tag matching in the brokerage to run the fat container.

pushStatusChanges (PC)
    The task will push status changes to the message broker.

pushJob (PJ)
    The task will push a job to the pilot through the message broker.

pfnList (PL)
    The task will use the PFN list to specify input files.

putLogToOS (PO)
    Jobs in the task will upload log files to the object store.

runUntilClosed (RC)
    The task will keep running until the input dataset is closed.

registerDatasets (RD)
    The task will register the output datasets in DDM.

registerEsFiles (RE)
    The task will register the event service output files in DDM.

respectLB (RL)
    The task will respect the lumi block number when generating jobs, so that each job processes files with the same lumi block number.

retryModuleRules (RM)
    The list of task parameters and their initial values modified by the retry module.

reuseSecOnDemand (RO)
    The task will reuse secondary datasets if they are insufficient in comparison to the primary dataset.

releasePerLB (RP)
    The task will generate jobs when all input files with the same lumi block number are ready.

respectSplitRule (RR)
    Scout jobs in the task will respect the ``splitRule`` attribute of the task when they are being generated.

randomSeed (RS)
    The random seed to be used for the task.

retryRamOffset (RX)
    The offset to be added to the RAM size of the job when the retry module changes memory requirements.

retryRamStep (RY)
    The step to be added to the RAM size of the job when the retry module changes memory requirements.

resurrectConsumers (SC)
    The task will resurrect event service consumers.

switchEStoNormal (SE)
    The task will switch event service jobs to normal jobs if the remaining number of events is less than the threshold.

stayOutputOnSite (SO)
    The task will keep the output files on the PQ where the output files are stored.

scoutSuccessRate (SS)
    The success rate of scout jobs to be satisfied in the task.

useSecrets (ST)
    Jobs in the task will use secrets stored in PanDA.

segmentedWork (SW)
    The workload in the task is segmented so that jobs are generated for each segment.

totNumJobs (TJ)
    The maximum number of jobs to be generated for the task.

tgtNumEventsPerJob
    The number of events to be targeted for a single job in the task.

tgtMaxOutputForNG (TN)
    The maximum output size in GB to be targeted for a single job in the task when nGBPerJob is set.

t1Weight (TW)
    The weight in the brokerage to assign jobs to nuclei. -1 to assign all jobs to the nucleus.

useBuild (UB)
    The task will use the build job following by multiple run jobs.

useJobCloning (UC)
    The task will use the job cloning mechanism to process the same payload by multiple jobs.
    "runonce" to kill other jobs when one job takes the payload.
    "storeonce" to kill other jobs when one job successfully uploads the output.

useRealNumEvents (UE)
    The task will use the real number of events for each input file available as the n_events metadata in DDM.

useFileAsSourceLFN (UF)
    The task will use a part of the input file name as the source LFN of the output files.

usePrePro (UP)
    The task will run the pre-processing job to process actual payload.

useScout (US)
    The task will run scout jobs with a small fraction of input files before generating jobs for all the rest.

usePrefetcher (UT)
    Jobs in the task will use the prefetcher to download input files.

useExhausted (UX)
    The task will go to exhausted if the task is finished incompletely.

useZipToPin (UZ)
    The task will use the zip datasets to pin input files.

writeInputToFile (WF)
    Jobs in the task will write input file names to a file and pass it to the payload to avoid executing the payload with a long argument list.

waitInput (WI)
    The task will wait for the input dataset before it is registered in DDM.

maxAttemptES (XA)
    The maximum number of attempts for event range.

decAttOnFailedES (XF)
    Event service jobs in the task will decrease the number of attempts when they fail.

maxAttemptEsJob (XJ)
    The maximum number of attempts for event service jobs.

nEventsPerMergeJob (ZE)
    The number of events to be processed by a single merge job.

nFilesPerMergeJob (ZF)
    The number of input files to be processed by a single merge job.

nGBPerMergeJob (ZG)
    The maximum input size in GB to be processed by a single merge job.

nMaxFilesPerMergeJob (ZM)
    The maximum number of input files to be processed by a single merge job.

------------

|br|

Priorities of Task Parameters for Input Sizing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Task parameters related to input sizing may sometimes conflict with each other. Below are these parameters listed in descending order of priority:

* nEventsPerJob
* nFilesPerJob
* nGBPerJob
* tgtNumEventsPerJob
* tgtMaxOutputForNG

Once one of these parameters is set, the others with lower priorities will be ignored.
E.g., nFilesPerJob overrides all others except for nEventsPerJob.

---------------

|br|