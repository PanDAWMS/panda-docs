============
Pilot
============

The Pilot is component based, with each component being responsible for different tasks.
The main tasks are handled by controller components, such as Job Control, Payload Control and Data Control.
There is also a set of components with auxiliary functionalities, e.g. Pilot Monitor and Job Monitor
- one for internal use which monitors threads and one that is tied to the job and checks parameters that
are relevant for the payload (e.g. size checks). The Information System component presents an interface
to a database containing knowledge about the resource where the Pilot is running
(e.g. which copy tool to use and where to read and write data).

The Pilot architecture is described on
`an external wiki page <https://github.com/PanDAWMS/pilot2/wiki/Pilot-architecture>`_
in details.

-----

|br|

Pilot components
==================

.. toctree::
   :maxdepth: 2

   pilot_components/index

------

|br|
