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
-------------------------------------
You can create a k8s cluster at CERN by following the CERN Kubernetes instructions here: https://kubernetes.docs.cern.ch/docs/getting-started/#create-a-cluster
It is fine to use your personal OpenStack project if this cluster is to be used solely for testing. If you plan to use it for production, you should request a new OpenStack project from the CERN IT department.
To create a new OpenStack project, you can follow the instructions here: https://clouddocs.web.cern.ch/projects/creating_projects.html
Before creating a kubernetes cluster, please first follow this guide to create a keypair: https://clouddocs.web.cern.ch/tutorial/create_your_openstack_profile.html
You can create a kubernetes cluster by running the following command:

.. prompt:: bash

  [ekaravak@lxplus981 ~]$ openstack coe cluster create PanDA-DOMA-k8s --keypair lxplus --cluster-template kubernetes-1.29.2-2 --node-count 4 --flavor m2.xlarge --master-flavor m2.xlarge --merge-labels --labels cern_enabled=true,ingress_controller=nginx,cinder_csi_enabled=True

This will create a k8s cluster with 1 master node of xlarge flavor and 4 nodes of xlarge flavor. If the xlarge flavor is not available, you can use a different flavor or request it from the CERN IT department by opening a SNOW request ticket. Please make sure you are using the latest cluster template version (kubernetes-1.29.2-2 in our example).

The following command will show the status of the cluster:

.. prompt:: bash

  [ekaravak@lxplus981 ~]$ openstack coe cluster list

It should be ``CREATE_IN_PROGRESS`` while it is being created and ``CREATE_COMPLETE`` when it is ready.

You may need to ``source ~/.openrc`` and ``eval $(ai-rc PROJECT_NAME)`` beforehand. Once ``status`` is in ``CREATE_COMPLETE``, you can generate an access
token with

.. prompt:: bash

   [ekaravak@lxplus981 ~]$ openstack coe cluster config PanDA-DOMA-k8s > panda-k8s-env.sh
   [ekaravak@lxplus981 ~]$ source panda-k8s-env.sh

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

We now need to set up the LanDB aliases, if we assume that the cluster name is ``panda-doma-k8s`` and the node names are ``panda-doma-k8s-xyz-node`` and we have 4 nodes, we can run the following command to set the aliases for each node. The aliases are comma separated and are in the form of ``<cluster_name>-<component>--load-N-``. For example, the first node (node-0) will have the alias ``panda-doma-k8s-xyz-node-load-1-``. The command to set the aliases is as follows:

.. prompt:: bash

  [ekaravak@lxplus981 ~]$ CLUSTER_NAME=panda-doma-k8s; NODE_NAME=$CLUSTER_NAME-xyz-node
  for N in 1 2 3 4 ; do
   openstack server set \
       --property landb-alias="$CLUSTER_NAME--load-$N-,$CLUSTER_NAME-harvester--load-$N-,$CLUSTER_NAME-panda--load-$N-,$CLUSTER_NAME-idds--load-$N-,$CLUSTER_NAME-bigmon--load-$N-,$CLUSTER_NAME-server--load-$N-" \
       NODE_NAME-$((N-1)) ; done

Then you can deploy PanDA as instructed in the guide below. We use `CERN Root CA <https://ca.cern.ch/ca/>`_ to obtain host certificates
("CERN Host Certificates" / "New CERN Host Certificate" / "Automatic Certificate Generation"). This CA is not provided in the generic Docker images (nor by PanDA images installed by Helm).
Make sure you copy the certificate in the `secrets/files` directory for `bigmon_certs`, `harvester_certs` and `panda_certs` (you will need the `hostkey.pem`, `hostcert.pem` and `chain.pem` files).

Github module for k8s deployment
---------------------------------------
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


GitOps deployment with ArgoCD
------------------------------

`ArgoCD <https://argo-cd.readthedocs.io/>`_ is a declarative GitOps continuous delivery tool for Kubernetes.
Instead of running ``helm install`` / ``./bin/install`` manually, you register each PanDA component as an
ArgoCD *Application* that tracks a path in the ``panda-k8s`` Git repository.
ArgoCD then automatically syncs the cluster state whenever changes are merged to the target branch.

Prerequisites
^^^^^^^^^^^^^

* A running ArgoCD instance in the cluster (see the `ArgoCD getting started guide <https://argo-cd.readthedocs.io/en/stable/getting_started/>`_).
* The ``panda-k8s`` repository accessible to ArgoCD (add it under *Settings → Repositories*).
* Secrets deployed separately via Helm (ArgoCD does not manage the secrets release — see below).

Deploying secrets
^^^^^^^^^^^^^^^^^

The secrets Helm chart contains sensitive values and is **not** tracked by ArgoCD.
Deploy and upgrade it manually as usual:

.. prompt:: bash

  helm install panda-secrets secrets/ -f secrets/values-secret.yaml
  # or to upgrade:
  helm upgrade panda-secrets secrets/ -f secrets/values-secret.yaml

Registering ArgoCD Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create one ArgoCD ``Application`` resource per PanDA component. The example below deploys ``panda-server``;
repeat the pattern for ``panda-jedi``, ``panda-idds``, ``panda-bigmon``, ``panda-harvester``, etc.,
adjusting ``path`` and ``releaseName`` accordingly.

.. code-block:: yaml

  apiVersion: argoproj.io/v1alpha1
  kind: Application
  metadata:
    name: panda-server
    namespace: argocd
  spec:
    project: default
    source:
      repoURL: https://github.com/PanDAWMS/panda-k8s.git
      targetRevision: main
      path: helm/panda
      helm:
        releaseName: panda-server
        valueFiles:
          - values/values-<your_experiment>.yaml
    destination:
      server: https://kubernetes.default.svc
      namespace: default
    syncPolicy:
      automated:
        prune: true
        selfHeal: true
      syncOptions:
        - ServerSideApply=true

Apply each Application manifest:

.. prompt:: bash

  kubectl apply -f argocd-apps/panda-server.yaml

.. note::

   Ready-to-use example Application manifests for the ATLAS Testbed (covering panda-server/JEDI,
   harvester, bigmon, and idds) are available at
   `argocd-apps/testbed <https://github.com/PanDAWMS/panda-k8s/tree/main/argocd-apps/testbed>`_
   in the ``panda-k8s`` repository.

Once registered, ArgoCD will perform an initial sync. Subsequent merges to ``main`` are picked up
automatically within the configured polling interval (default: 3 minutes), or immediately if a
webhook is configured.

Upgrade workflow
^^^^^^^^^^^^^^^^

The typical workflow for any configuration change is:

1. Edit the relevant Helm chart or values file in ``panda-k8s``.
2. Open a pull request and merge to ``main``.
3. ArgoCD detects the change and syncs the affected Application(s) automatically.
4. If the change also requires updated secrets (e.g. new environment variables), run
   ``helm upgrade panda-secrets secrets/ -f secrets/values-secret.yaml`` **before** or
   **after** the ArgoCD sync, then delete the affected pod(s) to pick up the new secret values.

You can also trigger a manual sync from the ArgoCD web UI (*App → Sync → Synchronize*) or by
restarting the ``argocd-repo-server`` pod if the UI reports a repository lock error:

.. prompt:: bash

  kubectl rollout restart deployment argocd-repo-server -n argocd

Using published Helm charts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``panda-k8s`` repository includes a GitHub Actions workflow
(``.github/workflows/helm-release.yml``) that automatically lints, packages, and publishes
the PanDA Helm charts as OCI artifacts to the GitHub Container Registry whenever changes
are merged to ``main``.

The charts are published to::

  oci://ghcr.io/pandawms/panda-k8s-charts

Instead of pointing ArgoCD at a Git repository path (as shown above), you can use the
pre-packaged OCI chart directly as the source:

.. code-block:: yaml

  source:
    repoURL: oci://ghcr.io/pandawms/panda-k8s-charts
    chart: panda
    targetRevision: "0.1.0"   # chart version
    helm:
      releaseName: panda-server
      valueFiles:
        - values/values-<your_experiment>.yaml

This is cleaner for stable deployments as it decouples the deployed version from the
live state of the Git repository.

The workflow can also be triggered manually on any branch (with the *Publish* option enabled),
which is useful for developers who want to publish a chart from their own fork for testing
without waiting for a merge to ``main``.

Developer workflow
^^^^^^^^^^^^^^^^^^

Individual developers can use the same ArgoCD pattern to deploy and test their changes in a
personal namespace **before** opening a pull request to the upstream project.
Each developer gets a fully isolated environment — secrets, application components, and
ArgoCD Applications all live in a personal namespace (e.g. ``dev-eddie``).
The ``default`` namespace is reserved for the ATLAS Testbed and must not be used for personal development deployments.

**Step 1 — Create a personal namespace**

.. prompt:: bash

  kubectl create namespace dev-eddie

**Step 2 — Fork the repositories**

Fork `panda-k8s <https://github.com/PanDAWMS/panda-k8s>`_ and the component(s) you are working on
(e.g. `panda-server <https://github.com/PanDAWMS/panda-server>`_) into your own GitHub account.

**Step 3 — Build and push a custom image**

After making code changes in your fork, build and push a Docker image to a registry you control
(e.g. GitHub Container Registry):

.. prompt:: bash

  docker build -t ghcr.io/<your-username>/panda-server:my-feature .
  docker push ghcr.io/<your-username>/panda-server:my-feature

You can automate this with a GitHub Actions workflow on push to your feature branch.

**Step 4 — Deploy personal secrets**

Each developer maintains their own ``values-secret.yaml`` with their own database credentials,
OIDC keys, etc., and deploys the secrets chart into their personal namespace:

.. prompt:: bash

  helm install panda-secrets secrets/ -f secrets/values-secret.yaml -n dev-eddie

This is completely isolated from production — Kubernetes secrets are namespace-scoped, so
``panda-secrets`` in ``dev-eddie`` is invisible to any other namespace.

**Step 5 — Override the image in your panda-k8s fork**

In your ``panda-k8s`` fork, create a personal values file (e.g. ``values/values-dev-eddie.yaml``)
that points to your custom image:

.. code-block:: yaml

  image:
    repository: ghcr.io/<your-username>/panda-server
    tag: my-feature

**Step 6 — Create an ArgoCD Application pointing to your fork**

Register an ArgoCD Application that tracks your fork and feature branch, deploying into your
personal namespace:

.. code-block:: yaml

  apiVersion: argoproj.io/v1alpha1
  kind: Application
  metadata:
    name: dev-eddie-panda-server
    namespace: argocd
  spec:
    project: default
    source:
      repoURL: https://github.com/<your-username>/panda-k8s.git
      targetRevision: my-feature-branch
      path: helm/panda
      helm:
        releaseName: dev-eddie-panda-server
        valueFiles:
          - values/values-<your_experiment>.yaml
          - values/values-dev-eddie.yaml
    destination:
      server: https://kubernetes.default.svc
      namespace: dev-eddie
    syncPolicy:
      automated:
        prune: true
        selfHeal: true
      syncOptions:
        - ServerSideApply=true

Every push to your feature branch will trigger an automatic re-deploy of your personal instance.
Once you are satisfied, open pull requests to the upstream code repository ``panda-k8s``.
