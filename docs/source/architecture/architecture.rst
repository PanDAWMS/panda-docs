===================
System Architecture
===================

.. figure:: ../terminology/images/PandaSys.png

The PanDA system is composed of the following components.

.. toctree::
   :maxdepth: 1

   jedi
   server
   pilot
   monitor
   harvester
   iam

JEDI (Job Execution and Definition Interface) is a sophisticated engine designed
to optimize workload utilization across diverse resources. It interfaces with the
PanDA server to process tasks, manage job assignments, and ensure efficient use
of computing resources.
The PanDA server serves as the central hub of the system, comprising Apache-based
RESTful Web servers and time-based process schedulers integrated with the
database. It manages job lifecycle operations including receiving jobs from
JEDI and other sources, preparing and dispatching job data to worker nodes,
monitoring job progress, handling output data, and executing actions based
on configurable timeouts and user commands.
The Pilot is a modular component system designed for flexible job management.
Key functionalities are managed by controller components like Job Control,
Payload Control, and Data Control. Auxiliary components such as Pilot Monitor
and Job Monitor support internal operations, monitoring threads and job-specific
parameters like payload size.
Harvester facilitates Pilot provisioning across diverse computing resources
using specific communication protocols for each resource provider. In environments
without outbound network connectivity, Harvester acts as an intermediary,
communicating with the PanDA server on behalf of the Pilot to ensure seamless
operation and job management.
PanDA features an Identity and Access Management (IAM) system compliant with
OIDC/OAuth2.0 standards, supporting identity federation across scientific
and academic providers. While legacy x509 authentication is supported,
it is advised to transition away from it due to its outdated status,
ensuring secure and modern identity management practices.
PanDA Monitor is a web-based tool that tracks tasks and jobs managed by PanDA,
offering a unified interface for end users, central operations teams, and
remote site administrators.
The intelligent Data Delivery Service (`iDDS <https://idds.readthedocs.io/en/latest/>`_)
is a general service to orchestrate
the workload management system and data management system and to transform and
deliver needed data to consumers in order to improve the workflow between
the workload management system and the data management system. PanDA uses iDDS
as high-level service to support emerging workflows.

|br|