


# Harvester Admin Tool

Harvester Admin Tool is available since Harvester version 0.0.20, which provides the command for harvester administrative operations.

## Setup

After installation of Harvester, under {harvester_venv}/local/bin/ there is a script template harvester-admin.rpmnew.template . Copy it to be **harvester-admin** and modify it: Set the `userName` and `VIRTUAL_ENV` according to the user to run the admin tool and the harvester venv respectively. E.g. when venv directory is /opt/harvester :

    # cp /opt/harvester/local/bin/harvester-admin.rpmnew.template /opt/harvester/local/bin/harvester-admin
    # vim /opt/harvester/local/bin/harvester-admin

One may also want to make **harvester-admin** a default command (rather than executable file) in the shell by modifying `$PATH` .

## Usage

Run **harvester-admin** . Option -h after any command/sub-command provides help message. Some examples below.

Show help:

```
# /opt/harvester/local/bin/harvester-admin -h
usage: harvester-admin [-h] [-v] {test,get,fifo,cacher,qconf,kill} ...

positional arguments:
  {test,get,fifo,cacher,qconf,kill}
    test                for testing only
    get                 get attributes of this harvester
    fifo                fifo related
    cacher              cacher related
    qconf               queue configuration
    kill                kill something alive

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose, --debug
                        Print more verbose output. (Debug mode !)
```

Admin tool test:

```
# /opt/harvester/local/bin/harvester-admin -v test
[2019-10-04 00:17:03,197 CRITICAL] Harvester Admin Tool: test CRITICAL
[2019-10-04 00:17:03,198 ERROR] Harvester Admin Tool: test ERROR
[2019-10-04 00:17:03,198 WARNING] Harvester Admin Tool: test WARNING
[2019-10-04 00:17:03,198 INFO] Harvester Admin Tool: test INFO
[2019-10-04 00:17:03,198 DEBUG] Harvester Admin Tool: test DEBUG
Harvester Admin Tool: test
[2019-10-04 00:17:03,198 DEBUG] ARGS: Namespace(debug=True, which='test') ; RESULT: None 
[2019-10-04 00:17:03,198 DEBUG] Action completed in 0.001 seconds
```

Show help of qconf (queue configuration) sub-command:

```
# /opt/harvester/local/bin/harvester-admin qconf -h
usage: harvester-admin qconf [-h] {list,dump,refresh,purge} ...

positional arguments:
  {list,dump,refresh,purge}
    list                List queues. Only active queues listed by default
    dump                Dump queue configurations
    refresh             refresh queue configuration immediately
    purge               Purge the queue thoroughly from harvester DB (Be
                        careful !!)

optional arguments:
  -h, --help            show this help message and exit

```

List all queue configurations in harvester:

```
# /opt/harvester/local/bin/harvester-admin qconf list -a
configID : queue name
--------- ------------
   44795 : pic-htcondor_UCORE
   44796 : NIKHEF-ELPROD_MCORE
   ...
   44974 : INFN-T1_UCORE
```                                                                                                                                   

***




***

# PanDA Queue management

## How to offline a PQ from harvester

If one just wants the harvester not to submit more workers of the PQ, as temporary manual offline, it suffices to add the following line in the object of the PQ in harvester local queue configuration file. E.g.

    "CERN-EXTENSION_GOOGLE_HARVESTER": {
        "queueStatus": "OFFLINE",
        ...
    }

## How to remove a PQ from harvester

If one wants to remove the PQ completely from harvester (e.g. the PQ is renamed or no longer used), then:

0. Be sure that one really does not need anything jobs/workers/configs of the PQ any longer.
1. Modify the pilot_manager to be "local" of the PQ on AGIS and/or make sure harvester does not grab information about this PQ from AGIS anymore.
2. Remove all lines of the PQ in harvester local queue configuration file.
3. Run qconf purge with harvester admin tool in order to delete all records of this PQ in DB. E.g.:

        # harvester-admin qconf purge UKI-LT2-IC-HEP_SL6
        Purged UKI-LT2-IC-HEP_SL6 from harvester DB

KaBOOM!


# Worker management

## How to kill workers in a dead queue or dead CE

Sometimes one finds plenty of queuing workers submitted to a certain dead CE, preventing more jobs to get activated/submitted to the whole queue. Or may be a queue is totally blocked due to site issue and all workers already submitted to the site will never run.

In such cases, on the harvester instance one can manually kill workers which block the queue -- harvester admin tool allows one to kill workers filtered by worker status, queue (site), CE, and submissionhost (e.g. condor schedd).

E.g. Kill all submitted (queuing) workers submitted to CE "ce13.pic.es:9619" and CE "ce14.pic.es:9619" of site "pic-htcondor_UCORE":

```
# /opt/harvester/local/bin/harvester-admin kill workers --sites pic-htcondor_UCORE --ces ce13.pic.es:9619 ce14.pic.es:9619  --submissionhosts ALL
Sweeper will soon kill 7 workers, with status in ['submitted'], computingSite in ['pic-htcondor_UCORE'], computingElement in ['ce13.pic.es:9619', 'ce14.pic.es:9619'], submissionHost in ALL
```

E.g. Kill all submitted and idle workers submitted via submissionhost "aipanda183.cern.ch,aipanda183.cern.ch:19618" (full submissionhost name of aipanda183 condor schedd) to the CE "ce13.pic.es:9619" (say, condor GAHP processes to some CE are down on a certain schedd):

```
# /opt/harvester/local/bin/harvester-admin kill workers --status submitted idle --sites ALL --ces ALL --submissionhosts aipanda183.cern.ch,aipanda183.cern.ch:19618
Sweeper will soon kill 7 workers, with status in ['submitted', 'idle'], computingSite in ALL, computingElement in ['ce13.pic.es:9619'], submissionHost in ['aipanda183.cern.ch,aipanda183.cern.ch:19618']
```

Rules of command `harvester-admin kill workers`:
* Available filter flags are `--status`, `--sites`, `--ces`, `--submissionhosts`
* After the filter flags there can be one of the following: a single argument (workers matching the argument), multiple arguments separated by space (workers matching any of these arguments), or the keyword `ALL` (no constraint on this flag)
* `--sites`, `--ces`, `--submissionhosts` are mandatory. One MUST specify them to be valid argument(s), or `ALL`
* `--status` is optional. Available status arguments are `submitted`, `idle`, `running`, and their combination. 
If `--status` is omitted, its value is `submitted` by default.
* All workers which match the conditions of all filter flags will be killed by sweeper agent soon (next cycle).

_Note: For grid, the feature will be implemented on BigPanDA webpage as well for easier manual operation. Furthermore, in the future the monitoring system will automatically spot dead CEs and kill blocked workers._


## Get statistics of workers of a PQ

Harvester admin tool provides `query workers` command to get number of workers of the PQ specified, broken down by prodsourcelabel, resource_type (SCORE, MCORE, ...), and worker status.

For example, the worker stats of CERN-PROD_UCORE_2 :

```
# /opt/harvester/local/bin/harvester-admin query workers CERN-PROD_UCORE_2
{
    "CERN-PROD_UCORE_2": {
        "ANY": {
            "ANY": {
                "running": 0,
                "submitted": 0,
                "to_submit": 0
            }
        },
        "managed": {
            "SCORE": {
                "cancelled": 24,
                "finished": 33,
                "running": 0,
                "submitted": 2,
                "to_submit": 1
            }
        }
    }
}
```

