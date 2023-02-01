PanDA System Kubernetes Deployment
===================================

Main Components
---------------
* PanDA: Workload manager, manages/schedules tasks and jobs.

  * panda-server
  * panda-JEDI
  * panda-database (postgresql)

* Harvester: Resource facing service to submit pilots to Grid/Cloud.

  * Harvester
  * Harvester-db (mariadb)

* iDDS: Workflow manager, manages the dependencies of tasks and jobs.

  * rest
  * daemon
  * database (postgresql)

* bigmon: panda monitor

* activemq: messaging service

* IAM: OIDC authentication service

  * indigo-iam-login_service
  * database (mariadb)

Github module for k8s deployment
---------------
You can find the kubernetes module with all the deployment helm charts at https://github.com/PanDAWMS/panda-k8s

Please checkout the module first:

.. prompt:: bash

  git clone https://github.com/PanDAWMS/panda-k8s.git

then enter the panda-k8s directory:

.. prompt:: bash

  cd panda-k8s

and follow the deployment instructions below.

Deployment order
-----------------
* PanDA, Harvester and iDDS depend on activemq.
* PanDA, Harvester, iDDS and bigmon depend on IAM.
* Harvester, iDDS and BigMon need to communicate with PanDA.
* So the installation order is

  * activemq, IAM
  * PanDA
  * Harvester, iDDS, BigMon

Deployment info
-----------------

There are different installations:

  * Secret installation: In this installation, secret information are kept in *secrets/*. You need to keep the secret file in a diferent place (such as applying *helm secrets*). For the secret deployment, you can keep them for long time and only update it when it's needed. After deploying the secrets, you can deploy the service.

  * Experiment based installation: For different experiments, there might be special requirements, for example different namespaces or different persistent volumens. In this case, an experiment specific file *values-<experiment>.yaml* is required.

  * **In the example, secrets are kept in the same location as service files. For a production instance, it's good to encrypt them or put them in a different location.**

Deployment with secrets
------------------------

* Deploy secrets. The secrets files can be kept in a private repository or use 'helm secrets' to encrypt them.
Different experiments many have different solutions to keep the secrets. Here we separate the secrets part because
we can keep them for long time after they are deployed. The updating frequence for secrets can be much less
than updating the instance.

Deploy secrets:
+++++++++++++++

The secrets can be stored in a private repository or in the same repository but encrypted. They can be deployed
one time and then used for long term (*Please set the values correctly in the secrets/<>/values.yaml*):

.. prompt:: bash

  helm install panda-secrets secrets/

Deploy the instances:
+++++++++++++++++++++

When the secrets are deployed. Someone else or some daemons can automatically deploy the panda instances.
There is a tool to deploy instances consistently with the secrets:

.. code-block:: bash

  $ ./bin/install -h
        usage: install [-h] [--affix AFFIX] [--experiment EXPERIMENT]
                   [--enable ENABLE] [--disable DISABLE] [--template]

        optional arguments:
          -h, --help            show this help message and exit
          --affix AFFIX, -a AFFIX
                                Prefix (blah-) or suffix (-blah) of instance names. If
                                this option is not specified, it looks for affix in
                                secrets/values.yaml. "test-" is used if affix is not
                                found in the values.yaml
          --experiment EXPERIMENT, -e EXPERIMENT
                                Experiment name
          --enable ENABLE, -c ENABLE
                                Comma-separated list of components to be installed
          --disable DISABLE, -d DISABLE
                                Comma-separated list of disabled components and/or
                                sub-components
          --template, -t        Dry-run

* Deploy ActiveMQ:

.. prompt:: bash

  ./bin/install -c msgsvc

* Deploy IAM:

.. prompt:: bash

  ./bin/install -c iam

* Deploy PanDA:

.. prompt:: bash

  ./bin/install -c panda

* Deploy iDDS:

.. prompt:: bash

  ./bin/install -c idds

* Deploy Harvester:

.. prompt:: bash

  ./bin/install -c harvester

* Deploy BigMon:

.. prompt:: bash

  ./bin/install -c bigmon

* Deploy all components in one go:

.. prompt:: bash

  ./bin/install

LSST deployment
-----------------

For LSST deployment (at SLAC), you need to specify `-e lsst`

* Deploy ActiveMQ for example:

.. prompt:: bash

  ./bin/install -c msgsvc -e lsst

* Deploy all components in one go:

.. prompt:: bash

  ./bin/install -e lsst


Sphenix deployment
------------------

For Sphenix deployment (at BNL), you need to specify `-e sphenix`

* Deploy ActiveMQ for example:

.. prompt:: bash

  ./bin/install -c msgsvc -e sphenix

* Deploy all components in one go:

.. prompt:: bash

  ./bin/install -e sphenix -d iam


CRIC-free deployment
----------------------

It is possible to deploy the PanDA system without CRIC. First, you need to prepare a couple of json files
that define PanDA queues, sites, storages, etc, and place them under ./secrets/files/cric_jsons.
It would be easiest to download json files from an exising CRIC instance and edit them. E.g.

.. prompt:: bash

  curl -s -k -o ./secrets/files/cric_jsons/sites.json "https://datalake-cric.cern.ch/api/atlas/site/query/?json"
  curl -s -k -o ./secrets/files/cric_jsons/panda_queues.json "https://datalake-cric.cern.ch/api/atlas/pandaqueue/query/?json"
  curl -s -k -o ./secrets/files/cric_jsons/ddm_endpoints.json "https://datalake-cric.cern.ch/api/atlas/ddmendpoint/query/?json"

Then, set the :green:`real` flag to ``true`` in the cric section in /secrets/values.yaml

.. code-block:: yaml

  # real CRIC
  real: true

and deploy secrets and the instances as usual.

.. prompt:: bash

  helm install panda-secrets secrets/
  ./bin/install -c ...

Those json files are mounted on a volume in service instances, so they are auto-updated
by periodic sync when secrets are updated, i.e., service instances don't have to be restarted.
For example, when you change a status of a PanDA queue in panda_queues.json, it is enough to do

.. prompt:: bash

  helm upgrade panda-secrets secrets/

The table below shows the list of json files. Files with \* are mandatory.

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - sites.json :sup:`*`
     - Site definitions
   * - panda_queues.json :sup:`*`
     - PanDA queue definitions
   * - ddm_endpoints.json :sup:`*`
     - Storage definitions
   * - ddm_blacklist.json
     - Blacklist of storages
   * - cm.json
     - Cost metrix of data transfer among storages
