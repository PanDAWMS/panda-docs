==================================
Identity and Access Management
==================================

PanDA has an Identity and Access Management (IAM) scheme fully compliant with OIDC/OAuth2.0
capable of identity federation among scientific and academic identity providers.
Although legacy x509 is also supported, it is recommended to avoid it since it is being outdated.

PanDA IAM is consist of

* `Indigo IAM <https://indigo-iam.github.io/docs/v/current/>`_

* `CILogon <https://cilogon.org/>`_

* `Identity providers <https://cilogon.org/idplist/>`_

Indigo IAM is an account and group membership management service to define virtual organizations (VOs) and groups,
to add/remove users to/from VOs and groups, and issue ID tokens once users are authenticated.
CILogon is a federated ID broker to delegate authentication to ID providers such as CERN, BNL IT/SDCC, KIT,
Google, ...

.. figure:: images/iam.png

The figure above shows the procedure of end-user authentication and authorization, where the device code flow is used
to allow users to run command-line tools.
First, the user invokes a command-line tool which checks if a valid ID token is locally available.
If not, the command-line tool sends an authentication request to Indigo IAM on behalf of the user and retrieves
a verification URL. Then the user opens a web browser to go to the verification URL, and is eventually
redirected to his/her own ID provider through CILogon. Once the user successfully logs on, a couple
of tokens are exchanged between CILogon and Indigo IAM, and an ID token is issued. The command-line
tool gets the ID token and put it to the HTTP request header when accessing the PanDA server.
The PanDA server decodes the token and authorizes the user based on OIDC claims such as name, username, and groups.

|br|

Detailed Authorization Flows for OIDC clients
---------------------------------------------------
PanDA's IAM scheme supports three types of OIDC clients: one for end-users, another for Web applications such as BigMon,
and a third for robotic clients like Harvester. It also has a capability to distribute
tokens for robotic clients to access external services. Authorization Flow for each OIDC
client is explained below.

|br|

End-user Authorization with Device-code Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: images/enduser_auth.png

End-users are authorized using the Device-code Flow.
When users run panda-client tools like ``pathena`` and ``prun`` in console terminals, the tools prompt
users to authenticate themselves by visiting links in their web browsers.
Users are redirected to their own ID providers, and after successful authentication,
those tools obtain ID tokens from Indigo IAM for accessing the PanDA server.
Typically, these ID tokens have a lifetime of 24 hours, reducing the need for frequent browser sessions.
The PanDA server authenticates end-users using the ``name`` claim in the ID token, and authorizes them
based on the ``groups`` claim.

|br|

Web Application Authorization with Authorization Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: images/bigmon_auth.png

Web applications like BigMon use the Authorization Code Flow to access the PanDA server
on behalf of end-users.
When users click links in web applications which require PanDA server access,
they redirect users to their own ID providers through Indigo IAM.
Once users are successfully authenticated, the web applications obtain ID tokens from Indigo IAM
for accessing the PanDA server.
Typically, these ID tokens have a lifetime of 24 hours.
The PanDA server authenticates users (delegators) using the ``name`` claim in the ID token, and authorizes them
based on the ``groups`` claim.

|br|

Robotic Client Authorization with Client Credentials Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: images/pilot_auth.png

Robotic clients like Harvester obtains access tokens from Indigo IAM using the Client Credentials Flow.

The sequence diagram above shows token usage in Harvester and the pilot.
Harvester first acquires access tokens from Indigo IAM. These access tokens, along with other files
in the sandbox, are then transmitted to the pilot. The pilot utilizes these access tokens to interact
with the PanDA server. Authentication of the pilot by the PanDA server is based on the ``sub`` (client ID)
and ``aud`` claims in the access token, as well as an internal mapping of client IDs to roles.
The lifetime of access tokens is typically 4 days, ensuring they are valid throughout the pilot's
operational period in batch systems.

|br|

Distributing Access Tokens for Robotic Clients to Access External Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: images/dist_token.png

The PanDA server has the capability to centrally renew access tokens and distribute them to robotic
clients. This is typically useful in reducing the frequency of token renewal with Indigo IAM,
especially when numerous robotic clients are running and they use short-lived access tokens for
accessing external services.

The sequence diagram above shows the process of renewing and utilizing short-lived access tokens.
The PanDA server periodically obtains new access tokens from Indigo IAM with the Client Credentials Flow.
The pilot retrieves these access tokens from the PanDA server immediately before accessing storage,
using the long-lived access tokens provided by Harvester.

|br|

DOMA PanDA IAM
---------------
There is an multipurpose IAM instance at `DOMA PanDA IAM <https://panda-iam-doma.cern.ch/login>`_
which can define any VO or group to play with PanDA.


Client setup
---------------------
:ref:`client/panda-client:panda-client` needs to set the following environment variables to enable
OIDC/OAuth2.0 based Auth.

.. prompt:: bash

 export PANDA_AUTH=oidc
 export PANDA_AUTH_VO=<name of virtual organization:(role)>
 export PANDA_VERIFY_HOST=off

where *<name of virtual organization>* should be replaced with the actual VO name.
The *role* is optional and can be omitted if the user does not belong to any role in the VO.


Adding a new VO to the PanDA server
-------------------------------------

Each VO can be defined as a group in PanDA IAM, so that VOs share the same OIDC client attributes
to skip the registration step in CILogon. In other words, if the VO wants to use a new OIDC
client it needs to be registered in CILogon at https://cilogon.org/oauth2/register.

There are three parameters in ``panda_server.cfg``.

.. code-block:: text

    # set to oidc to enable OpenID Connect
    token_authType = oidc

    # directory where OIDC authentication config files are placed
    auth_config = /opt/panda/etc/panda/auth/


``token_authType`` needs to be *oidc* to enable the OIDC/OAuth2.0 based Auth.
The OIDC authentication configuration file are placed under the directory specified by the ``auth_config``
parameter. The filename should be :blue:`\<name of virtual organization(.role)\>_auth_config.json`.
The configuration file contains

 * "audience"
 * "client_id"
 * "client_secret"
 * "oidc_config_url"
 * "vo"

The first three are attributes of the OIDC client defined in PanDA IAM, "oidc_config_url" is
the well-known openid-configuration URL of PanDA IAM, and "vo" is the VO name.
The file may include the following optional attributes:

 * "secondary_ids"
 * "robot_ids"

The former comprises a list of OIDC client IDs used by clients accessing the PanDA server on behalf
of the user via ID tokens, while the latter consists of OIDC client IDs used by robotic clients like
the pilot accessing the PanDA server via access tokens.

Those configuration files must be reachable through Web interface of the PanDA server, so that make sure that
the directory needs to be exposed in ``httpd.conf`` like

.. code-block:: text

    Alias /auth/ "/opt/panda/etc/panda/auth/"

Roles are defined as working groups in the VO in PanDA IAM.
It is possible to use another OIDC client for a special role in the same VO by adding the role name to the filename.
E.g, :blue:`a_vo_auth_config.json` for ordinary users in a VO and :blue:`a_vo.a_role_auth_config.json` for selected
users in the same VO.


PanDA IAM gives all group names in the OIDC group attribute. This means that each group name must be unique.
The authorization policy file describes
mapping between OIDC groups and actual groups in VOs. The "role" defines the permission level of
users in the group.
