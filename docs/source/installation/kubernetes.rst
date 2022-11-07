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

``git clone https://github.com/PanDAWMS/panda-k8s.git``

then enter the panda-k8s directory:

``cd panda-k8s``

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

  * Experiment based installation: For different experiments, there maybe special requirements, for example different namespaces or different persistent volumens. In this case, an experiment specific file *values-<experiment>.yaml* is required.

  * *In the example, secrets are kept in the same location as service files. For a production instance, it's good to encrypt them or put them in a different location.*

Deployment with secrets
------------------------

* Deploy secrets. The secrets files can be kept in a private repository or use 'helm secrets' to encrypt them.
Different experiments many have different solutions to keep the secrets. Here we separate the secrets part because
we can keep them for long time after they are deployed. The updating frequence for secrets can be much less
than updating the instance.

Deploy secrets:
+++++++++++++++

The secrets can be stored in a private repository or in the same repository but encrypted. They can be deployed
one time and then used for long term (*Please set the values correctly in the secrets/<>/values.yaml*)::

  $> helm install panda-secrets  secrets/

Deploy the instances:
+++++++++++++++++++++

When the secrets are deployed. Someone else or some daemons can automatically deploy the panda instances.
There is a tool to deploy instances consistently with the secrets::

  $> ./bin/install -h
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

* Deploy ActiveMQ::

  $> ./bin/install -c msgsvc

* Deploy IAM::

  $> ./bin/install -c iam

* Deploy PanDA::

  $> ./bin/install -c panda

* Deploy iDDS::

  $> ./bin/install -c idds

* Deploy Harvester::

  $> ./bin/install -c harvester

* Deploy BigMon::

  $> ./bin/install -c bigmon

* Deploy all components in one go::

  $> ./bin/install

LSST deployment
-----------------

For LSST deployment (at SLAC), you need to specify `-e lsst`

* Deploy ActiveMQ for example::

  $> ./bin/install -c msgsvc -e lsst

* Deploy all components in one go::

  $> ./bin/install -e lsst


Sphenix deployment
------------------

For Sphenix deployment (at BNL), you need to specify `-e sphenix`

* Deploy ActiveMQ for example::

  $> ./bin/install -c msgsvc -e sphenix

* Deploy all components in one go::

  $> ./bin/install -e sphenix -d iam
