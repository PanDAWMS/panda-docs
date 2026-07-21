PanDA Kubernetes Deployment with GitOps (ArgoCD)
=================================================

.. note::

   For manually installing a cluster with ``bin/install`` and general cluster operations
   (node failure recovery, CVMFS mounts), see :doc:`kubernetes`.

GitOps deployment with ArgoCD
------------------------------

`ArgoCD <https://argo-cd.readthedocs.io/>`_ is a declarative GitOps continuous delivery tool for Kubernetes.
Instead of running ``helm install`` / ``./bin/install`` manually, you register each PanDA component as an
ArgoCD *Application* that tracks a path in the ``panda-k8s`` Git repository.
ArgoCD then automatically syncs the cluster state whenever changes are merged to the target branch.

Installing ArgoCD
^^^^^^^^^^^^^^^^^

The ``panda-k8s`` repository ships ready-to-apply installation manifests under
``argocd-install/<cluster>/`` (e.g. ``argocd-install/doma/``, ``argocd-install/testbed/``).
Apply them once when bootstrapping ArgoCD on a new cluster — they cannot be managed by ArgoCD
itself (bootstrap chicken-and-egg).

.. note::

   The DNS alias for the ArgoCD hostname must be registered in LanDB **before** starting,
   otherwise the ingress will not resolve. At CERN this is done via the OpenStack server
   property ``landb-alias`` — see your cluster's setup notes for the exact command.

**Step 1 — Install ArgoCD**

.. prompt:: bash

  kubectl create namespace argocd
  kubectl apply -n argocd \
    -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.6/manifests/install.yaml
  kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=120s

**Step 2 — Prepare the TLS certificate**

Request a host certificate for ``argocd-<cluster>.cern.ch`` from the CERN CA. The certificate
is downloaded as a ``.p12`` file. Convert it to PEM format and store it alongside the other
cluster secrets:

.. prompt:: bash

  mkdir -p $HOME/cernbox/<cluster>/secrets/files/argocd_certs
  openssl pkcs12 -in argocd-<cluster>.p12 -clcerts -nokeys -passin pass: \
    -out $HOME/cernbox/<cluster>/secrets/files/argocd_certs/hostcert.pem
  openssl pkcs12 -in argocd-<cluster>.p12 -nocerts -nodes -passin pass: \
    -out $HOME/cernbox/<cluster>/secrets/files/argocd_certs/hostkey.pem
  chmod 600 $HOME/cernbox/<cluster>/secrets/files/argocd_certs/hostkey.pem

**Step 3 — Create the TLS secret**

.. prompt:: bash

  kubectl create secret tls argocd-tls -n argocd \
    --cert=$HOME/cernbox/<cluster>/secrets/files/argocd_certs/hostcert.pem \
    --key=$HOME/cernbox/<cluster>/secrets/files/argocd_certs/hostkey.pem

**Step 4 — Disable built-in TLS and apply the ingress**

The nginx ingress controller handles TLS termination, so ArgoCD's own TLS must be disabled.
Run the following from the ``panda-k8s`` repository root:

.. prompt:: bash

  kubectl apply -f argocd-install/<cluster>/argocd-cmd-params-cm.yaml
  kubectl apply -f argocd-install/<cluster>/ingress.yaml
  kubectl rollout restart deployment argocd-server -n argocd

**Step 5 — Retrieve the initial admin password**

.. prompt:: bash

  kubectl get secret argocd-initial-admin-secret -n argocd \
    -o jsonpath='{.data.password}' | base64 -d && echo

The ArgoCD UI will be available at ``https://argocd-<cluster>.cern.ch``.
Log in as ``admin`` with the password from the command above, then change it under
*User Info → Update Password*.

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

   Ready-to-use Application manifests are available in the ``panda-k8s`` repository for:

   * `argocd-apps/testbed <https://github.com/PanDAWMS/panda-k8s/tree/main/argocd-apps/testbed>`_ — ATLAS Testbed (panda-server/JEDI, harvester, bigmon, idds)
   * `argocd-apps/doma <https://github.com/PanDAWMS/panda-k8s/tree/main/argocd-apps/doma>`_ — DOMA cluster (panda-server/JEDI, harvester, bigmon, idds, msgsvc)

Once registered, ArgoCD will perform an initial sync. Subsequent merges to ``main`` are picked up
automatically within the configured polling interval (default: 3 minutes), or immediately if a
webhook is configured.

Automatic image updates with argocd-image-updater
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Components whose images are tagged ``latest`` (rather than a fixed version) do not get new
images automatically just because CI pushed one. Kubernetes only re-pulls an image when the
image reference in the pod spec changes, and a plain ``latest`` tag never changes as a string
— so a running pod happily keeps serving whatever it originally pulled, indefinitely, even
after a newer ``latest`` is published.

`argocd-image-updater <https://argocd-image-updater.readthedocs.io/>`_ solves this by
periodically checking the registry for the digest that a tag currently resolves to, and, when
it changes, pinning the image to that exact digest (e.g. ``latest@sha256:...``) as a Helm
parameter override on the Application. Because that string is different every time the
underlying image changes, Kubernetes treats it as a new image reference and pulls it — and
because ArgoCD's normal sync then applies the resulting spec change, the component actually
gets redeployed, not just re-pulled on some unrelated future restart.

.. important::

   The image-updater controller in this deployment runs in **operator/CRD mode**. It only
   acts on Applications that are explicitly enrolled via an ``ImageUpdater`` custom resource's
   ``applicationRefs`` — annotations on the Application alone do **nothing** without a matching
   ``ImageUpdater`` object. This is easy to miss: an Application can look fully configured
   (correct ``argocd-image-updater.argoproj.io/*`` annotations) and still never actually update,
   because no ``ImageUpdater`` resource references it.

Enrolling a component takes two pieces. First, annotate the Application:

.. code-block:: yaml

  metadata:
    annotations:
      argocd-image-updater.argoproj.io/image-list: bigmon=ghcr.io/pandawms/panda-bigmon-core:latest
      argocd-image-updater.argoproj.io/bigmon.update-strategy: digest
      argocd-image-updater.argoproj.io/bigmon.helm.image-name: main.image.repository
      argocd-image-updater.argoproj.io/bigmon.helm.image-tag: main.image.tag

Then create the ``ImageUpdater`` resource that actually enables it:

.. code-block:: yaml

  apiVersion: argocd-image-updater.argoproj.io/v1alpha1
  kind: ImageUpdater
  metadata:
    name: bigmon-image-updater
    namespace: argocd
  spec:
    applicationRefs:
      - namePattern: panda-bigmon
        useAnnotations: true

.. note::

   Working examples for bigmon, panda-server/JEDI, and panda-ui are in the
   `testbed Application manifests directory
   <https://github.com/PanDAWMS/panda-k8s/tree/main/argocd-apps/testbed>`_
   (``*-image-updater.yaml``, alongside the corresponding ``Application`` manifest's
   annotations).

.. warning::

   To stop tracking ``latest`` and pin a component to an explicit version instead, deleting
   the ``ImageUpdater`` resource is **not enough on its own**. The controller writes its pinned
   digest directly into the Application's ``spec.source.helm.parameters``, and that override is
   not automatically cleaned up when the ``ImageUpdater`` is removed — it will keep silently
   overriding whatever tag your values files specify. Remove it explicitly:

   .. prompt:: bash

     kubectl patch application <app-name> -n argocd --type=json \
       -p='[{"op": "remove", "path": "/spec/source/helm/parameters"}]'

   Only after that will ArgoCD fall back to the tag pinned in your Helm values.

Whether a component should track ``latest`` via image-updater or pin an explicit version is a
per-cluster choice. The ATLAS Testbed tracks ``latest`` for faster iteration during development;
DOMA pins explicit versions for every component instead, since it is treated as more
stability-sensitive.

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

