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

Setting up a k8s cluster at CERN
---------------
You can create a k8s cluster at CERN by following the CERN Kubernetes instructions here: https://kubernetes.docs.cern.ch/docs/getting-started/#create-a-cluster
It is fine to use your personal OpenStack project if this cluster is to be used solely for testing. If you plan to use it for production, you should request a new OpenStack project from the CERN IT department.
To create a new OpenStack project, you can follow the instructions here: https://clouddocs.web.cern.ch/projects/creating_projects.html
You can create a kubernetes cluster by running the following command:

.. prompt:: bash

  openstack coe cluster create PanDA-DOMA-k8s --keypair lxplus --cluster-template kubernetes-1.29.2-2 --node-count 4 --flavor m2.xlarge --master-flavor m2.xlarge --merge-labels --labels cern_enabled=true,ingress_controller=nginx,cinder_csi_enabled=True

This will create a k8s cluster with 1 master node of xlarge flavor and 4 nodes of xlarge flavor. If the xlarge flavor is not available, you can use a different flavor or request it from the CERN IT department by opening a SNOW request ticket. Please make sure you are using the latest cluster template version (kubernetes-1.29.2-2 in our example).

The following command will show the status of the cluster:

.. prompt:: bash

  openstack coe cluster list

It should be ``CREATE_IN_PROGRESS`` while it is being created and ``CREATE_COMPLETE`` when it is ready.

You may need to ``source ~/.openrc`` and ``eval $(ai-rc PROJECT_NAME)`` beforehand. Once ``status`` is in ``CREATE_COMPLETE``, you can generate an access
token with

.. prompt:: bash

   openstack coe cluster config PanDA-DOMA-k8s > panda-k8s-env.sh
   source panda-k8s-env.sh

Keep the generated ``panda-k8s-env.sh`` and ``.config`` files for further usage. Let's check our nodes now.


.. prompt:: bash

  [ekaravak@lxplus981 ~]$ kubectl get nodes
  NAME                                   STATUS   ROLES    AGE    VERSION
  panda-doma-k8s-xyz-master-0   Ready    master   137m   v1.29.2
  panda-doma-k8s-xyz-node-0     Ready    <none>   120m   v1.29.2
  panda-doma-k8s-xyz-node-1     Ready    <none>   120m   v1.29.2
  panda-doma-k8s-xyz-node-2     Ready    <none>   120m   v1.29.2
  panda-doma-k8s-xyz-node-3     Ready    <none>   119m   v1.29.2

PanDA Helm charts use nginx
`advanced configuration with snippets <https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-snippets/>`_
and for secure connection one will also need the SSL passthrough, so nginx is
a must. So we need to setup the ingress controller on all 4 nodes (excluding the master):

.. prompt:: bash

  [ekaravak@lxplus981 ~]$ kubectl label node panda-doma-k8s-xyz-node-0 role=ingress
  node/panda-doma-k8s-xyz-node-0 labeled

We do the same for the remaining nodes. To enabled snippets (they are disabled by default), edit the config of ingress
controller by running:

.. prompt:: bash

  [ekaravak@lxplus981 ~]$ kubectl edit cm -n kube-system cern-magnum-ingress-nginx-controller

and setting ``"allow-snippet-annotations"`` from ``"false"`` to ``"true"`` (caveat: it *must* be a string).

We now need to set up the LanDB aliases:

.. prompt:: bash

  [ekaravak@lxplus981 ~]$ CLUSTER_NAME=panda-doma-k8s
  for N in 1 2 3 4 ; do
   openstack server set \
       --property landb-alias="$CLUSTER_NAME--load-$N-,$CLUSTER_NAME-harvester--load-$N-,$CLUSTER_NAME-panda--load-$N-,$CLUSTER_NAME-idds--load-$N-,$CLUSTER_NAME-bigmon--load-$N-,$CLUSTER_NAME-server--load-$N-" \
       $CLUSTER_NAME-$((N-1)) ; done

Then you can deploy PanDA as instructed in the guide below. We use `CERN Root CA <https://ca.cern.ch/ca/>`_ to obtain host certificates
("CERN Host Certificates" / "New CERN Host Certificate" / "Automatic Certificate Generation"). This CA is not provided in the generic Docker images (nor by PanDA images installed by Helm).
Make sure you copy the certificate in the `secrets/files` directory for `bigmon_certs`, `harvester_certs` and `panda_certs` (you will need the `hostkey.pem`, `hostcert.pem` and `chain.pem` files).

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

  * Secret installation: In this installation, secret information are kept in *secrets/*. You need to keep the secret file in a different place (such as applying *helm secrets*). For the secret deployment, you can keep them for long time and only update it when it's needed. After deploying the secrets, you can deploy the service.

  * Experiment based installation: For different experiments, there might be special requirements, for example different namespaces or different persistent volumes. In this case, an experiment specific file *values-<experiment>.yaml* is required.

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
