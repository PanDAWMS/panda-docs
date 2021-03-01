==========================
Deployment of Custom IAM
==========================

This document explains how to deploy a custom Identity and Access Management (IAM) service.

1. Installation of Indigo IAM
------------------------------
First, you need to install Indigo IAM following
`Indigo IAM admin guide <https://indigo-iam.github.io/docs/v/current/admin-guide/>`_.
Make sure that PUT and DELETE methods are allowed when configuring Nginx
since it is sometimes recommended to disable them for security purposes.
Also, you need to install a trusted host certificate to Nginx so that the IAM instance
can communicate with external services like CILogon.

2. Registration in CILogon
----------------------------
Next, register the IAM instance on `CILogon OIDC client registration portal <https://cilogon.org/oauth2/register>`_
where the most important information you need to provide is "Callback URLs" and "Scopes".
The former is the URL to which CILogon sends a callback once an external identity provider successfully
authenticates the user, and the scopes define OIDC claims the client receives. They must be something like

.. code-block:: text

 Scopes: [org.cilogon.userinfo, profile, email, openid]
 Callbacks: [https://{your_iam_hostname}/openid_connect_login]

You don't have to enable Refresh Tokens.

Once your registration request is approved, you will get a client ID and secret
and specify them in the IAM configuration.

3. Enabling Brokered OIDC auth through CILogon
------------------------------------------------
CILogon must be added as an OIDC provider in /etc/iam-login-service/config/application-oidc.yml.

.. code-block:: text

    oidc:
      providers:
      - name: cilogon
        issuer: https://cilogon.org
        client:
          clientId: ${IAM_CILOGON_CLIENT_ID}
          clientSecret: ${IAM_CILOGON_CLIENT_SECRET}
          redirectUris: ${iam.baseUrl}/openid_connect_login
          scope: openid,profile,email,org.cilogon.userinfo
        loginButton:
          text: Your ID Provider
          style: btn-primary
          image:
            fa-icon: none

where ``IAM_CILOGON_CLIENT_`` are specified in /etc/sysconfig/iam-login-service.

4. Customization
-------------------
You can modify /etc/sysconfig/iam-login-service. E.g.,

.. code-block:: text

    # Java VM arguments
    IAM_JAVA_OPTS=-Dspring.profiles.active=prod,registration,oidc

    # Generic options
    IAM_HOST=localhost
    IAM_PORT=8080
    IAM_BASE_URL=https://panda-iam-doma.cern.ch
    IAM_ISSUER=https://panda-iam-doma.cern.ch
    IAM_USE_FORWARDED_HEADERS=true
    IAM_KEY_STORE_LOCATION=file:///opt/iam/iam-keystore.jwks
    IAM_ORGANISATION_NAME=PanDA-DOMA

    # customization for PanDA
    IAM_TOPBAR_TITLE="PanDA DOMA"
    IAM_ACCESS_TOKEN_INCLUDE_AUTHN_INFO=true
    IAM_LOCAL_AUTHN_LOGIN_PAGE_VISIBILITY=hidden
    IAM_REGISTRATION_OIDC_ISSUER=https://cilogon.org
    IAM_CILOGON_CLIENT_ID=<your client ID>
    IAM_CILOGON_CLIENT_SECRET=<your client secret>

where you need `oidc` in ``IAM_JAVA_OPTS`` and specify your client ID and secret
in ``IAM_CILOGON_CLIENT_*``.

5. Start IAM
---------------
Now you can start the IAM instance.

.. prompt:: bash

  service iam-login-service start

Then go to `https://{your_iam_hostname}/login?sll=y` to enter the admin page
as the local auth login page is hidden due to ``IAM_LOCAL_AUTHN_LOGIN_PAGE_VISIBILITY`` in
/etc/sysconfig/iam-login-service.

Note that normal users should go to `https://{your_iam_hostname}/login`.

|br|