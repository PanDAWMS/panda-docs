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

Apply puppet

.. prompt:: bash

 puppet agent -t

Take a PanDA server out of load balancing

.. prompt:: bash

 touch /etc/iss.nologin

Links
---------------

* Puppet templates: https://gitlab.cern.ch/ai/it-puppet-hostgroup-vopanda
* PanDA configurations: https://gitlab.cern.ch/ai/it-puppet-module-vopandaconfig
* CSOps managed machines: https://atlas-adcmon.cern.ch/cmdb/
