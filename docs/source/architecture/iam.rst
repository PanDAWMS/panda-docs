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

The figure above shows the procedure of user authentication and authorization, where the device code flow is used
to allow users to run command-line tools.
First, the user invokes a command-line tool which checks if a valid ID token is locally available.
If not, the command-line tool sends an authentication request to Indigo IAM on behalf of the user and retrieves
a verification URL. Then the user opens a web browser to go to the verification URL, and is eventually
redirected to his/her own ID provider through CILogon. Once the user successfully logs on, a couple
of tokens are exchanged between CILogon and Indigo IAM, and an ID token is issued. The command-line
tool gets the ID token and put it to the HTTP request header when accessing the PanDA server.
The PanDA server decodes the token and authorizes the user based on OIDC claims such as name, username, and groups.


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
parameter. The filename should be `\<name of virtual organization(.role)\>_auth_config.json`.
The configuration file contains

 * "audience"
 * "client_id"
 * "client_secret"
 * "oidc_config_url"
 * and "vo"

The first three are attributes of the OIDC client defined in PanDA IAM, "oidc_config_url" is
the well-known openid-configuration URL of PanDA IAM, and "vo" is the VO name.
Those configuration files must be reachable through Web interface of the PanDA server, so that make sure that
the directory needs to be exposed in ``httpd.conf`` like

.. code-block:: text

    Alias /auth/ "/opt/panda/etc/panda/auth/"

It is possible to use another OIDC client for a special role in the same VO by adding the role name to the filename,
e.g. `a_vo_auth_config.json` and `a_vo.a_role_auth_config.json`.


PanDA IAM gives all group names in the OIDC group attribute. This means that each group name must be unique.
The authorization policy file describes
mapping between OIDC groups and actual groups in VOs. The "role" defines the permission level of
users in the group.
