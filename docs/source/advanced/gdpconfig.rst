=================================================
System Configuration Parameters in the Database
=================================================

There is the ``PANDA.CONFIG`` table, so-called ``gdpconfig`` table in the database where you can define
any configuration parameter
shared by all PanDA applications, so that system admins don't have to tweak the static cfg files every time
they optimize the system.

The table has the following columns:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - APP
     - The application name which uses the parameter
   * - COMPONENT
     - The component name which uses the parameter
   * - KEY
     - The parameter name
   * - VALUE
     - The parameter value
   * - TYPE
     - The parameter type
   * - VO
     - The organization name which defines the parameter
   * - DESCR
     - Description of the parameter

Applications get those parameters through the ``pandaserver.taskbuffer.TaskBuffer`` module.

.. code-block:: python

  from pandaserver.taskbuffer.TaskBuffer import taskBuffer
  p = taskBuffer.getConfigValue(COMPONENT, KEY, APP, VO)

The method returns None if the parameter is undefined.

|br|