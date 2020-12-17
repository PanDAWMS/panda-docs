=======
Clients
=======

There are client modules and tools to send commands to the PanDA server using standard HTTP methods.
The PanDA server, by default, listens on the port 25080 for plain HTTP and another port 25443 for HTTP over SSL.
Make sure that your local firewall doesn't block access to those ports.

The first part of this page is for end-users to use PanDA for their analysis,
while the second part is for system administrators and can be skipped unless you work for system operation
or intend to develop some applications on top of Python API.

For end-users
==============

.. toctree::
   :maxdepth: 1

   panda-client
   notebooks/python.ipynb
   jupyter

For system administrators
==========================

.. toctree::
   :maxdepth: 1

   rest
