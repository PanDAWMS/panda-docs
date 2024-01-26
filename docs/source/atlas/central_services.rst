==================================
Central Services Operations corner
==================================

Commands
---------------

Disable puppet

.. prompt:: bash

 puppet agent --disable 'reason for disabling puppet'

Enable puppet

.. prompt:: bash

 puppet agent --enable

Apply puppet once immediately with logging in the foreground

.. prompt:: bash

 puppet agent -t

Take a PanDA server out of load balancing

.. prompt:: bash

 touch /etc/iss.nologin

Put a PanDA server back into load balancing

.. prompt:: bash

 rm /etc/iss.nologin


Myproxy for PanDA ProxyCache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For ATLAS Robot proxy certificate of atlpilo1 and atlpilo2 are in use. Examples below are for atlpilo1.

CSOps manages an automatic renewal script that runs in acrontab of `atlpilo1` or `atlpilo2`. You can see check them like this:

.. prompt:: bash

    ssh root@<harvester instance>
    su -l atlpilo1
    /usr/sue/bin/kinit -kt /data/atlpilo1/keytab atlpilo1@CERN.CH 
    acrontab -l

.. code-block:: none

 ...
 #check and upload atlpilo2 proxy in myproxy
 00 09 * * * lxplus-acron.cern.ch /afs/cern.ch/user/a/atlpilo2/.globus/renew_myproxy.sh > /afs/cern.ch/user/a/atlpilo2/my_proxy.log 2>&1
 ...

You can try to check or renew the proxy manually. In case myproxy is not installed, install it first:

.. prompt:: bash

    yum install myproxy


Check myproxy info:

.. prompt:: bash

    myproxy-info -s myproxy.cern.ch -l '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=atlpilo1/CN=614260/CN=Robot: ATLAS Pilot1'

Reinitialize myproxy:

.. prompt:: bash

    myproxy-init -s myproxy.cern.ch -x -Z '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=pandasv1/CN=663551/CN=Robot: ATLAS Panda Server1' -d -k panda -c 4383 -t 0 -C ~/.globus/atlpilo1_latest_x509up.rfc.proxy -y ~/.globus/atlpilo1_latest_x509up.rfc.proxy;


Links
---------------

* Puppet templates: https://gitlab.cern.ch/ai/it-puppet-hostgroup-vopanda
* PanDA configurations: https://gitlab.cern.ch/ai/it-puppet-module-vopandaconfig
* CSOps managed machines: https://atlas-adcmon.cern.ch/cmdb/
