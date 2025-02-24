===================================
Queue configuration
===================================

*This documentation is for Harvester v0.5.10 or above*

Queue attributes and plug-ins for each PQ (PanDA queue) is configured in the queue configuration.

The local queue configuration file is tyically named ``panda_queueconfig_grid.json``. 
The path of local queue configuration file is defined in ``[qconf] configFile`` in Harvester local configuration. It has to be put in the $PANDA_HOME/etc/panda directory and/or at URL (See for more details :ref:`here <ref-misc-remote_config_files>`)

Here are examples of the queue configuration file for
`the grid <https://github.com/HSF/harvester/blob/master/examples/panda_queueconfig_grid.json>`_
and for `HPC <https://github.com/HSF/harvester/blob/master/examples/panda_queueconfig_hpc.json>`_.

The content of a queue configuration in JSON format have the form\:

.. code-block:: text

	{
	"PandaQueueName1": {
			"QueueAttributeName1": ValueQ_1,
			"QueueAttributeName2": ValueQ_2,
			...
			"QueueAttributeNameN": ValueQ_N,
			"AgentPlugin1": {
					"module": Plugin1_module_name,
					"name": Plugin1_class_name,
					"AgentPluginAttribute1": ValueA_1,
					"AgentPluginAttribute2": ValueA_2,
					...
					},
			"AgentPlugin2": {
					...
					},
			...
	"PandaQueueName2": {
			...
			},
	...
	}



Queue Attributes
-----------------

Here is the list of all queue attributes\:


General Queue Attributes
""""""""""""""""""""""""

* ``allowJobMixture``: Whether to allow mixture of jobs in a single worker. If true, jobs from different tasks can be given to a single worker. Only useful for PUSH mode (``mapType`` is NOT ``NoJob``). Default is false
* ``mapType``: Map type between jobs and workers. Available values are ``NoJob`` (workers themselves get jobs directly from Panda after they are submitted, i.e. Pull or Pull_UPS), ``OneToOne`` (1 job to 1 worker, i.e. normal Push), ``OneToMany`` = (1 job to N workers, aka the multiple consumer mode), ``ManyToOne`` (N jobs to 1 worker, aka the multi-job pilot mode). Harvester prefetches jobs except ``NoJob``. Mandatory
* ``maxNewWorkersPerCycle``: Max number of workers which can be submitted within a single submission cycle. Note that ``maxNewWorkersPerCycle = 0`` is a special value which means no extra limit on the number of new workers per submission cycle (while number of the workers submitted can still be capped by other attributes, say ``nQueueLimitWorker``). Default is 0, i.e. no extra limit
* ``maxWorkers``: Max number of total workers (queuing + running). ``maxWorkers - nQueueLimitWorker`` is the upper limit of running workers. Default is 0 (i.e. no worker to submit!); thus one definitely had better set maxWorkers of the PQ
* ``nQueueLimitJob`` : Max number of jobs pre-fetched and queuing (i.e. jobs in starting status) by the job-fetcher agent. Only useful for PUSH mode (``mapType`` is NOT ``NoJob``). Default is null, i.e. no limit, so Harvester will try to fetch all jobs of the PQ available from PanDA server
* ``nQueueLimitJobMax`` : Alias of ``nQueueLimitJob``. Deprecated
* ``nQueueLimitJobRatio``: Limit on the ratio in percent of the number of starting jobs to the number of running jobs. E.g. ``nQueueLimitJobRatio = 60`` means Harvester will stop fetching more jobs when the number of starting jobs is more than 60% of number of running jobs. Only useful for PUSH mode (``mapType`` is NOT ``NoJob``). Default is null, i.e. not consider starting/running ratio
* ``nQueueLimitJobMin`` : Additional attribute for ``nQueueLimitJobRatio`` to define the lower limit on the number of starting jobs. If set, before there are at least ``nQueueLimitJobMin`` starting jobs, Harvester will not consider the limit by starting/running ratio and will keep fetching jobs. Only useful when ``nQueueLimitJobRatio`` is set. Default is null, i.e. no additional lower limit
* ``nQueueLimitJobCores`` : Max number of cores of jobs pre-fetched and queuing (i.e. jobs in starting status) by the job-fetcher agent. Only useful for PUSH mode (``mapType`` is NOT ``NoJob``). Default is null, i.e. no limit
* ``nQueueLimitJobCoresRatio``: Limit on the ratio in percent of the number of cores of starting jobs to the number of cores of running jobs. E.g. ``nQueueLimitJobCoresRatio = 40`` means Harvester will stop fetching more jobs when the number of cores of starting jobs is more than 40% of number of cores of running jobs. Only useful for PUSH mode (``mapType`` is NOT ``NoJob``). Default is null, i.e. not consider starting/running ratio
* ``nQueueLimitJobCoresMin`` : Additional attribute for ``nQueueLimitJobCoresRatio`` to define the lower limit on the number of cores of starting jobs. If set, before there are at least ``nQueueLimitJobCoresMin`` cores of starting jobs, Harvester will not consider the limit by starting/running ratio and will keep fetching jobs. Only useful when ``nQueueLimitJobCoresRatio`` is set. Default is null, i.e. no additional lower limit
* ``nQueueLimitWorker``: Max number of workers queuing, i.e. workers in submitted, ready, or idle status. Default is null, i.e. no limit
* ``nQueueLimitWorkerMax``: Alias of ``nQueueLimitWorker``. Deprecated
* ``nQueueLimitWorkerRatio``: The limit on the ratio in percent of number of queuing workers to number of running workers. E.g. ``nQueueLimitWorkerRatio = 70`` means Harvester will stop submitting new workers when the number of queuing workers is more than 70% of number of running workers. Default is null, i.e. not consider queue/running ratio
* ``nQueueLimitWorkerMin``: Additional attribute for ``nQueueLimitWorkerRatio`` to define the lower limit on the number of queuing workers. If set, before there are at least ``nQueueLimitWorkerMin`` queuing workers, Harvester will not consider the limit by queuing/running ratio and will keep submitting workers. Only useful when ``nQueueLimitWorkerRatio`` is set. Default is null, i.e. no additional lower limit
* ``nQueueLimitWorkerCores``: Max number of cores of queuing workers (i.e. workers in submitted, ready, or idle status). Default is null, i.e. no limit
* ``nQueueLimitWorkerCoresRatio``: The limit on the ratio in percent of number of cores of queuing workers to number of cores of running workers. E.g. ``nQueueLimitWorkerCoresRatio = 40`` means Harvester will stop submitting new workers when the number of cores of queuing workers is more than 40% of number of cores of running workers. Default is null, i.e. not consider queue/running ratio
* ``nQueueLimitWorkerCoresMin``: Additional attribute for ``nQueueLimitWorkerCoresRatio`` to define the lower limit on the number of cores of queuing workers. If set, before there are at least ``nQueueLimitWorkerCoresMin`` cores of queuing workers, Harvester will not consider the limit by queuing/running ratio and will keep submitting workers. Only useful when ``nQueueLimitWorkerCoresRatio`` is set. Default is null, i.e. no additional lower limit
* ``nQueueLimitWorkerMemory``: Max memory in MB of queuing workers (i.e. workers in submitted, ready, or idle status). Default is null, i.e. no limit
* ``nQueueLimitWorkerMemoryRatio``: The limit on the ratio in percent of memory of queuing workers to memory of running workers. E.g. ``nQueueLimitWorkerMemoryRatio = 40`` means Harvester will stop submitting new workers when the memory in MB of queuing workers is more than 40% of memory of running workers. Default is null, i.e. not consider queue/running ratio
* ``nQueueLimitWorkerMemoryMin``: Additional attribute for ``nQueueLimitWorkerMemoryRatio`` to define the lower limit on the memory in MB of queuing workers. If set, before there are at least ``nQueueLimitWorkerMemoryMin`` MB of memory of queuing workers, Harvester will not consider the limit by queuing/running ratio and will keep submitting workers. Only useful when ``nQueueLimitWorkerMemoryRatio`` is set. Default is null, i.e. no additional lower limit
* ``prodSourceLabel``: Source label of the queue; *managed* for production and *user* for analysis users. Mandatory
* ``prodSourceLabelRandomWeightsPermille``: A map of probability distribution (in permille, i.e. thousandths) to randomize the source label of the jobs that job_fetcher fetches. E.g. ``"prodSourceLabelRandomWeightsPermille": {"rc_test":150, "rc_test2":200, "rc_alrb":250}`` makes job_fetcher to fetch rc_test jobs in 15% probability, rc_test2 in 20%, rc_alrb in 25%, and jobs of ``prodSourceLabel`` (defined above) in the rest 40%. Default is 100% for ``prodSourceLabel`` defined and zero for any other source labels
* ``runMode``: The run mode of Harvester about this PQ. The available values are either ``self`` or ``slave``. If ``self``, Harvester itself decides when and how many workers to submit to the PQ based on queueconfig attributes (nQueueLimitWorker, maxWorkers, etc.); Harvester submits periodically (in every submitter cycle) as long as the limits according to queueconfig attributes, aka pure Pull. If ``slave``, Harvester will NOT decide when and how many workers to submit; instead, it relies on PanDA server's UPS (unified pilot streaming) to keep sending commands to Harvester about how many workers (of each resource_type and prodsourcelabel) to submit, aka Pull_UPS mode. Note that the upper limits of number of workers according to queueconfig attributes are still respected when ``runMode = "slave"``. Only useful when ``mapType`` is ``NoJob``, i.e. Pull or Pull_UPS (not Push). Default is "self"
* ``truePilot``: Whether the PQ should be handled in true-pilot mode; i.e. pilot takes full responsibility to report the status of jobs to PanDA server. If true, Harvester will suppress heartbeats for jobs in running, transferring, finished, failed status (and let pilot handle these case). Only useful for PUSH mode (``mapType`` is NOT ``NoJob``). Default is false 
* ``useJobLateBinding``: Whether to use job-level late-binding. If true, harvester prefetches jobs and pass them to workers only after those workers get CPU slots, aka late-binding; note that this requires the mechanism available for Harvester to send jobs to the compute resource (where the workers are running), say shared-filesystem between Harvester and compute resource. If false, jobs are bound to the workers and get submitted together with the workers. Only useful for PUSH mode (``mapType`` must NOT be ``NoJob``). Default is false


Agent Plugin Attributes
""""""""""""""""""

Agent plugin attributes are meant to specify the plugins for the Harvester agents to run for the PQ.

The section name (key) of an agent plugin section should be either:

* An agent name, including ``submitter``, ``monitor``, ``sweeper``, ``workerMaker``, ``messenger``, ``preparator`` and ``stager``: attributes insides the section are for the very agent plugin. Usually, submitter, monitor and sweeper plugins should be set for the same underlying batch-system or scheduling system for workers. Similarly, preparator and stager plugins are set for the same environment to stage in/out.
* ``common``: attributes inside ``common`` section will be accessible to all agent plugins.

Inside each agent plugin section (except for ``common``), two plugin attributes ``module`` and ``name`` are mandatory in order to define the module names and the class name of the plugin.
Other plugin attributes serve as to the parameters for the very agent plugin.

For example:

.. code-block:: text

	{
	"Your_PQ": {
			"maxWorkers": 999999,
			"nQueueLimitWorker": 1000,
			...
			"submitter":{
				"module":"pandaharvester.harvestersubmitter.htcondor_submitter",
				"name":"HTCondorSubmitter",
				"condorHostConfig": "/opt/harvester/etc/panda/condor_host_config.json",
				"useCRICGridCE":true,
				...
				},
			"monitor": {
				"module":"pandaharvester.harvestermonitor.htcondor_monitor",
				"name":"HTCondorMonitor",
				"cancelUnknown":false
				},
			...
			"common": {
				"payloadType": "atlas_pilot_wrapper"
				}
	}


Parameters for plugins are described in each plugin document.
[this page](https://github.com/HSF/harvester/wiki/Plugins-and-Agents-descriptions).



### Remote configuration files
It is possible to load system and/or queue configuration files via http/https. This is typically useful to have a centralized pool of configuration files, so that it is easy to see with which configuration each harvester instance is running. There are two environment variables *HARVESTER_INSTANCE_CONFIG_URL* and *HARVESTER_QUEUE_CONFIG_URL* to define URLs for system config and queue config files, respectively. If those variable are set, the harvester instance loads config files from those URLs and then overwrites parameters if they are specified in local config files. Sensitive information like database password should be stored only in local config files. System config files are read only when the harvester instance is launched, while queue config files are read every 10 min so that queue configuration can be dynamically changed during the instance is running. Note that remote queue config file is periodically cached in the database by Cacher which automatically gets started when the harvester instance is launched, so you don't have to do anything manually. However, when you edit remote queue config file and then want to run some unit tests which don't run Cacher, you have to manually cache it using cacherTest.py.
```
$ python lib/python*/site-packages/pandaharvester/harvestertest/cacherTest.py
```

----------


# Configuration on Harvester

Configuration on Harvester
To make harvester work with auto queue configuration, one needs some lines in harvester.cfg:
```
[qconf]

configFromCacher = True

queueList =
 DYNAMIC

resolverModule = pandaharvester.harvestermisc.info_utils

resolverClass = PandaQueuesDict


[cacher]

data =
 ...
 ddmendpoints_objectstores.json||(URL of remote object stores JSON)
 cric_ddmendpoints.json||(URL of remote DDM endpoint JSON)
 panda_queues.json||(URL of remote schedconfig JSON)
 queues_config_file||(URL of remote queue configuration JSON)
```

On CERN_central_A,B these URLs are:
* for CRIC **(obsoleted December 2020)**
```
data =
 ddmendpoints_objectstores.json||http://atlas-cric-api.cern.ch/request/ddmendpoint/query/list/?json&state=ACTIVE&site_state=ACTIVE&preset=dict&json_pretty=1&type[]=OS_LOGS&type[]=OS_ES
 panda_queues.json||http://atlas-cric-api.cern.ch/request/pandaqueue/query/list/?json&preset=schedconf.all&vo_name=atlas
 queues_config_file||https://raw.githubusercontent.com/PanDAWMS/harvester_configurations/master/GRID/common_grid_queueconfig_template.json
... # Don't delete other entries you might have in the cacher configuration
```
* links for CRIC **(recommended configuration)**. 
```
data = 
 ddmendpoints_objectstores.json||https://atlas-cric.cern.ch/api/atlas/ddmendpoint/query/?json&state=ACTIVE&site_state=ACTIVE&preset=dict&json_pretty=1&type[]=OS_LOGS&type[]=OS_ES
 panda_queues.json||https://atlas-cric.cern.ch/api/atlas/pandaqueue/query/?json
 cric_ddmendpoints.json||https://atlas-cric.cern.ch/api/atlas/ddmendpoint/query/list/?json&state=ACTIVE&site_state=ACTIVE&preset=dict&json_pretty=1
 queues_config_file||https://raw.githubusercontent.com/PanDAWMS/harvester_configurations/master/GRID/common_grid_queueconfig_template.json
... # Don't delete other entries you might have in the cacher configuration
```
Note that the CRIC links moved to https and require a certificate registered and authorised by CRIC. To authenticate in the https connection, Harvester will use the certificates configured here:
```
[pandacon]

...
# CA file: this path is the typical CA CERT coming in CSOps installed machines
ca_cert = /etc/pki/tls/certs/CERN-bundle.pem

# certificate
cert_file = <CERT FILE>

# key
key_file = <KEY FILE>
...
```
Because of the changes required for https, Harvester needs to have been updated after 3 July 2020. You can verify this in your pandaharvester/commit_timestamp.py file.

One can skip the line of “queues_config_file” if no remote queueconfig needed. 
There are other plugins that use "cacher" to download information for them, do not remove other entries.


# Details

## Basics

### Queue vs Template:

In Harvester queue configurations, an object (~JSON object) can be either a queue or a template.

#### Description
* Queue: A queue (or configuration of a queue) corresponds to the name of a real PanDA queue that Harvester works for. One can set a template of the queue in order to inherit all attributes (parameters) and values written in the template.
* Template: An abstract template of queue configuration meant to be reused in queues. Harvester does not store a template in DB and does not submit workers for a template.

#### Rules
* The object is a template if its name (key) ends up in "_TEMPLATE" or it has attribute `isTemplateQueue` set to be `True`. Otherwise, the object is a queue.
* A queue written in local or remote file takes a template with the attribute `templateQueueName` of the queue set to be the name of the template.
* A queue set on CRIC takes a template with name from PQ field `harvester_template`, or a default template name `<type>.<workflow>` (e.g. `production.push`) if field `harvester_template` is blank.
* Queue and template are exclusive to each others. A queue cannot be a template simultaneously and vice versa.
* A queue will be invalid if its `templateQueueName` is set to be an non-existing template or another queue. Harvester will ignore invalid queues.
* Nested templates is not allowed (and not possible) according to rules above.


### Attributes in Configurations
There are two types of attributes in harvester queue configurations:

#### Generic attributes
For general setup of the PQ. E.g. `maxWorkers`, `mapType`, etc.

#### Plugin attributes
For certain harvester plugin of the PQ. Contain subkey, subvalues. E.g. `monitor`, `submitter`, etc. and `common` (which applies to all plugins)


## Advanced

### Sources of queue configurations

Queue configurations can come from three kinds of sources:

* Local: Static JSON describing queue and/or template in a local file on harvester, say panda_queueconfig.json (filename defined in harvester.cfg)
* Remote: Static JSON describing queue and/or template in a remote file shared with HTTP URL (URL and related setup defined in harvester.cfg . See [how](https://github.com/HSF/harvester/wiki/Auto-Queue-Configuration-with-CRIC#configuration-on-harvester))
* Dynamic: Queues (only queues, no template) generated according to information on CRIC (related setup defined in harvester.cfg . See [how](https://github.com/HSF/harvester/wiki/Auto-Queue-Configuration-with-CRIC#configuration-on-harvester))

#### Acronyms
* **LT**: Local template, written in local queueconfig file (panda_queueconfig.json)
* **RT**: Remote template, on http source fetched by cacher (e.g. on GitHub)
* **FT**: Final template derived from RT and LT.
* **LQ**: Local queue configuration, written in local queueconfig file (panda_queueconfig.json)
* **RQ**: Remote queue configuration, on http source fetched by cacher, static (e.g. on GitHub)
* **DQ**: Dynamic queue configuration, configured with information from resolver (e.g. coming from CRIC)
* **FQ**: Final queue configuration of a PanDA queue derived from RQ, DQ, and LQ.

#### Priority rule
* Templates: LT > RT
* Queues: LQ > DQ > RQ

This priority rule for templates/queues with the same name from multiple sources will be taken in following steps.


### Dynamic Queues (DQ) set on CRIC
See [Instructions of configuration on CRIC](https://github.com/HSF/harvester/wiki/Auto-Queue-Configuration-with-CRIC#instructions-of-configuration-on-cric) and [Move configuration of existing PQ in Local queueconfig file to CRIC](https://github.com/HSF/harvester/wiki/Auto-Queue-Configuration-with-CRIC#move-configuration-of-existing-pq-in-local-queueconfig-file-to-cric)

### Update of a configuration
Here explains how a configuration A will be "updated" with another configuration B:
* For generic attributes in B but not in A: Add the attribute/value of B to A
* For generic attributes in both: Take the value of the same attribute in B
* For plugin attributes in B but not in A: Add the attribute and all keys/values of this attribute of B to A
* For plugin attributes in both: "Update" the attribute with B. That is, for all keys/values in the attribute of B, add the key/value to the attributes of A if the key does not exist in A's, or take the value of B's for the key if the key exists in A's.
* Some special attributes (say `isTemplateQueue`, `templateQueueName`) will be handled separately and not included during the update process (i.e. skipped).

### How does Harvester handle configurations from multiple sources

1. Collect configurations from all sources:
    * Get RTs and RQs from remote resource (e.g. GitHub, http URL)
    * Get LTs and LQs from local queueconfig file
    * Get DQs (only queue name, its template, and associate parameters) from CRIC

2. Generate final templates (FTs) via the rules:
    * If a RT (among RTs) and a LT (among LTs) have the same name, only the LT will be added to FTs. (following the priority rule)
    * Otherwise, all RTs and LTs without duplication in name will all be added to FTs.
    * That is, for any specific template name, FT = LT if LT exists else RT .

3. Define the template of each queue among all queues (RQ, DQ, LQ). Rules:
    * The template name for a queue will be defined by the queue with highest priority among all existing queue/queues among RQ, DQ, LQ with the same name AND taking a template. (following the priority rule)
    * If none of the queues with the same name takes template, then no template for this queue name.
    * That is, for any specific template name, its template name will be defined by: LQ if LQ exists and LQ takes template else (DQ if DQ exists and DQ takes template else RQ)
    
4. Generate configuration of each queue via steps:
    0. Start from an empty configuration object (say a JSON object `{}`)
    1. If the queue takes a template (decided in 3. above), then update (see [update](https://github.com/HSF/harvester/wiki/Auto-Queue-Configuration-with-CRIC#update-of-a-configuration)) the configuration object with the configurations of the template. If the queue takes an invalid template (not in FTs), then this queue will be skipped/unavailable in harvester. Otherwise, if no template taken, skip this step.
    2. If RQ exists, update the configuration object with RQ.
    3. If DQ exists, update the configuration object with DQ (only associate parameters count here).
    4. If LQ exists, update the configuration object with LQ.
    5. Then the configuration object is the FQ. In short, FQ = (template defined among RQ,DQ,LQ) updated with RQ, next updated with DQ, then updated with LQ .
    6. Go through some sanity checks, addition adjustments of FQ. If FQ ever gets checked as invalid (e.g. missing mandatory attributes like `submitter`), this queue will be skipped/unavailable in harvester.
    7. If FQ survives, it will be updated to harvester DB and harvester will submit workers for it.


### Instructions of configuration on CRIC
Note: Currently all the following steps ONLY work for Harvester instance CERN_central_A and CERN_central_B.

To add new PQ to Harvester on CRIC for auto queue configuration
- Open the CRIC page of the PQ.
- Make sure all steps on CRIC of a Harvester PQs are done first (e.g. pilot manager = Harvester, and some UCORE or UPS setup if necessary).
- Choose the step “Add a Normal Grid PQ” or “Add a PQ Requiring Special Template” below (yet not both!). And see if one needs to go through the optional “Add Associate Parameters”.

Examples following in several cases

#### Add a Normal Grid PQ
Among SchedConfig parameters, fill in field "harvester" and "workflow"

Thus, now the minimum auto pq configuration on CRIC looks like this:
```
harvester: CERN_central_B/Harvester (CERN-PROD)
workflow: pull_ups
```

- For "harvester", choose an harvester instance, typically either CERN_central_A/Harvester (CERN-PROD) or CERN_central_B/Harvester (CERN-PROD)
- For “workflow”, choose a workflow among Push, Pull, and Pull_UPS. For UPS (unified pilot streaming) PQs, choose Pull_UPS.

Note that the “harvester_template” must be left blank, otherwise it will override the template.

Done!

Associate parameters are not needed for most grid PQs (taking default values from template).

Description: If harvester_template is blank, then harvester will take the default template name as "<type>.<workflow>".
For instance, default template of Taiwan-LCG2-HPC2_Unified in the example above will be "production.pull_ups", and this template is defined on the common template file on github.


#### Add a PQ Requiring Special Template
Only PQs which cannot use default templates need this setup:

Among SchedConfig parameters, fill in field "harvester" and "harvester template" . E.g.
```
harvester: CERN_central_B/Harvester (CERN-PROD)
harvester template: PRODUCTION_PULL_UPS_SHAREDFS_TEMPLATE
```

For "harvester", choose an harvester instance, typically either CERN_central_A/Harvester (CERN-PROD) or CERN_central_B/Harvester (CERN-PROD)

For "harvester template", insert the string of a template name in the common grid queueconfig template on GitHub or local config file. (More templates can be added to GitHub in the future if necessary.). The “harvester_template” field overrides the name template of default from PQ type + workflow.

#### Add Associate Parameters (Optional)
Do this only when it is not enough to work with parameters in default template on GitHub. For new normal Grid PQ, better to skip this section and start with default to see how it goes, and then ramp up/down parameters via the approach introduced here to tune stuff.

Under Associated Params, one can add harvester queue parameters. Click "Attach new Parameters to PQ" and then insert param and value. E.g.

Currently only parameters following for limits of job/workers are available:
* For jobs: `nQueueLimitJob`, `nQueueLimitJobRatio`, `nQueueLimitJobMax`, `nQueueLimitJobMin`
* For workers: `nQueueLimitWorker`, `maxWorkers`, `maxNewWorkersPerCycle`, `nQueueLimitWorkerRatio`, `nQueueLimitWorkerMax`, `nQueueLimitWorkerMin`

#### Coda
Then, after 20~30 minutes (considering cacher update period ~ 10 min. + qconf object update period ~ 10 min.), the harvester instance specified shall fetch the information on CRIC and start to submit workers for the PQ.
Or, if one does not want to wait, one can manually refresh harvester cacher and queue configurations on harvester node via harvester-admin commands (new feature after 181124):

```
$ <dir_of_harvester-admin>/harvester-admin cacher refresh
$ <dir_of_harvester-admin>/harvester-admin qconf refresh
```
Done.


### Move configuration of existing PQ in Local queueconfig file to CRIC
Do the same steps in “Add new PQ to Harvester on CRIC”. 

Basically one can easily translate JSON object of a normal GRID PQ in local queueconfig file to configuration on CRIC.

E.g. Actually the example of CRIC configuration above is translated from the following PQ in local queueconfig file on CERN_central_B instance:
```
"Taiwan-LCG2-HPC_Unified":{
    	"queueStatus":"online",
    	"templateQueueName":"PRODUCTION_PULL_SHAREDFS_TEMPLATE",
    	"prodSourceLabel":"managed",
    	"nQueueLimitWorker":600,
    	"maxWorkers":900,
    	"maxNewWorkersPerCycle":200,
    	"runMode":"slave",
    	"mapType":"NoJob"
	}
```
where the “runMode” and “mapType” are defined in the template “PRODUCTION_PULL_UPS_SHAREDFS_TEMPLATE” on GitHub already; the “queueStatus” is always online if configured on CRIC (If one wants it offline on harvester instance, modify “pilot manager” field to be something else than “Harvester”)

After 20~30 minutes, remove the PQ in local queueconfig json file, and reload harvester service (or wait a few minutes more). 

One can then check whether the PQ is still on the harvester node (coming from CRIC) with harvester-admin command. E.g.
```
[root@aipanda173 ~]# /usr/local/bin/harvester-admin qconf dump -J Taiwan-LCG2-HPC_Unified
{
	"Taiwan-LCG2-HPC_Unified": {
    	"allowJobMixture": false,
    	"configID": 963,
    	"ddmEndpointIn": null,
    	"getJobCriteria": null,
    	"mapType": "NoJob",
    	"maxNewWorkersPerCycle": 200,
    	"maxSubmissionAttempts": 3,
    	"maxWorkers": 900,
        ...
}
```

If so, then done.



## Examples
See [slides](https://docs.google.com/presentation/d/1dt2Fe2pkN-3F3xYJJ-HBVZyCCrvmKzOGFiXVky86VFc/edit#slide=id.g3b9a1466bb_0_0) for some examples.


# FAQ

### What if the same PQ set both on CRIC and in local queueconfig file?

Priority of location to define the parameters (descending):
1. PQ in Local queueconfig json file on harvester node (LQ)
2. Associated Params on CRIC (DQ)
3. PQ on remote URL source (RQ). So far no RQ is set on GitHub but still possible
4. Template in Local queueconfig json file on harvester node (LT)
5. Template on GitHub (common grid queueconfig template), or other remote URL source (RT)


### What if one inserts erroneous values  in queue configuration (on CRIC or in local file)?

In principle, encountering invalid queue configurations of a PQ, harvester will:
- Drop the problematic PQ (offline and unavailable)
- Log error/warning message in panda-queue_config_mapper.log
- Keep running and serving the valid PQs and existing workers, without breaking anything

#### E.g.1

If “monitor” and “preparator” of Taiwan-LCG2-htcondor-score are not defined in CRIC, local file, or any templates, then this queue is consider invalid and will be unavailable on harvester:
```
# /opt/harvester/local/bin/harvester-admin qconf dump -J Taiwan-LCG2-htcondor-score
ERROR : Taiwan-LCG2-htcondor-score is not available
{}
```

And in panda-queue_config_mapper.log there can be:
```
2018-11-22 19:46:21,072 panda.log.queue_config_mapper: DEBUG	QueueConfigMapper.load_data : queue Taiwan-LCG2-htcondor-score comes from LQ
2018-11-22 19:46:21,076 panda.log.queue_config_mapper: ERROR	QueueConfigMapper.load_data : Missing mandatory attributes preparator,monitor . Omitted Taiwan-LCG2-htcondor-score in queue config
```
which shows the queue comes from LQ (local queue). Thus, one should check if something is fishy in local config file.

#### E.g.2:

One inserts the name of a non-existing harvester template on CRIC, say:

```
PanDA Queue: Taiwan-LCG2-htcondor-score
harvester template: xxxxxxxxxxxxxxxxxxxxxx
```

And assume nothing in local config file overrides it.
Then, this queue is consider invalid and will be unavailable on harvester, and in panda-queue_config_mapper.log there can be:
```
2018-11-22 19:46:20,935 panda.log.queue_config_mapper: WARNING  QueueConfigMapper.load_data : Invalid templateQueueName "xxxxxxxxxxxxxxxxxxxxxx" for Taiwan-LCG2-htcondor-score (DQ). Skipped
```
which shows the queue comes from DQ (dynamic queue). Thus, one knows they should check the setup of this PQ on CRIC.

If you find harvester gets broken with an erroneous queue configuration or error/warning message not informative enough, report the issue to developers.


### Can I determine the PQ to be UCORE or UPS queue elsewhere than CRIC? Say, in local queueconfig file on Harvester?

Short answer: No.

To make UPS (unifiled pilot streaming) working on a PQ, both PanDA server and Harvester need to know the PQ is a UPS queue (so PanDA computes how many workers of each resources type to submit, and harvester only submits workers passively according to commands from PanDA). Thus, the information of UPS setup of the PQ must share across both PanDA and harvester: CRIC is ideal for this. It makes no sense to set a PQ to be a UPS queue unilaterally.
As to UCORE (unified), well, harvester can still to submit workers without knowing the queue is UCORE or not: UCORE information only influence the computation of resource requirement of a worker. But there is no reason not to keep information about UCORE of the queue on CRIC.

Actually even for a MCORE or SCORE queue, Harvester does not need  set the string “MCORE” or “SCORE”. All one can do to define the number of cores is:
- Set nCore explicitly (fixed value) of the PQ in queue configuration,
- Or take the resource requirement (corecount) of the job (default) in push,
- Or take the capacity (corecount) of the site from CRIC (default) in rest cases
And the same situation holds for a UCORE queue. (and similar for memory requirement etc.)

So UCORE can only be reasonably run in Push where ncore of workers defined by jobs, or Pull_UPS where ncore of workers decided by PanDA. (In the case a UCORE running in pure Pull mode, Harvester will end up submitting workers with fixed ncore, either according to explicitly set nCore, or site corecount from CRIC)
Since CRIC information (site corecount, etc.) can be referenced for a queue no matter what, set the UCORE tag queue on CRIC is natural.
