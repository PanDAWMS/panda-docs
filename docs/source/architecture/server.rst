=================
PanDA server
=================

The PanDA server is the central hub of the system consist of Apache-based RESTful Web servers
and time-based process schedulers, running on the database. It horizontally scales
by adding machines since Web servers are stateless and time-based processes are
fine-grained.

.. figure:: images/server_overview.png

The picture above shows the architecture of the PanDA server on a machine. PanDA Web applications are embedded in
WSGI daemons running behind an `Apache HTTP server <http://httpd.apache.org/>`_.
The master Apache process spawns WSGI
daemons via `mod_wsgi <https://modwsgi.readthedocs.io/en/master/>`_ in addition to
`Apache MPM workers <https://httpd.apache.org/docs/current/en/mod/worker.html>`_.
The number of WSGI daemons is static, while the number of MPM workers dynamically changes depending
on the load to optimize resource usages on the machine.
MPM workers receive requests from actors such as users and the pilot, to pass them
to PanDA Web applications through an internal request queue and WSGI daemons.
There are two types of requests; synchronous and asynchronous requests.
With synchronous requests, actors are blocked for a while and get responses when PanDA Web applications
complete processing the requests.
On the other hand, actors immediately get responses and then requests are
asynchronously processed typically when they need heavy procedures like access to external services,
in order to avoid the HTTP server from being clogged.
Roughly speaking, when the entire PanDA server is composed of `M` machines receiving requests
at `R` Hz, each PanDA server machine runs `W` PanDA Web applications, the average processing time of
the request is `A` sec, the following formula must be satisfied:

.. math::

 A \times R < M \times W

Otherwise, the HTTP server will get choked and requests will be terminated due to timeout errors.

The time-based process scheduler is a daemon to periodically launch various processes.
Its functionalities are very similar to the standard cron daemon, but it allows those processes
to share database connections and provides an exclusive control mechanism to avoid concurrently
launching the same process among multiple machines.

------------

|br|

PanDA Web application
----------------------

.. figure:: images/server_sync.png

The picture above shows the internal architecture of the PanDA Web application to process
synchronous requests. The ``panda`` module is the entry point of the application running in the
main process and implementing
the WSGI protocol to receive requests through the WSGI daemon.
Requests are fed into one of three modules, ``JobDispatcher``, ``UserIF``, and ``Utils``.
``JobDispatcher`` and ``UserIF`` modules provide APIs for the pilot and users, respectively, and
requests via those modules end up with the database access through ``TaskBuffer``, ``OraDBProxy``, and other
modules. On the other hand, the ``Utils`` module
provides utility APIs which don't involve the database access, such as API for file uploading.
``TaskBuffer`` and ``OraDBProxy`` modules provide high-level and low-level APIs for the database access,
respectively, and they are executed in separate processes and communicate through the ``ConBridge``
module. The ``ConBridge`` module allows the child process, which runs the ``OraDBProxy`` module, to get
killed due to timeout, in order to avoid deadlock of the main process.
The ``OraDBProxyPool`` is a pool of ``ConBridge`` objects where the ``TaskBuffer`` module picks up one
``ConBridge`` object to call ``OraDBProxy`` APIs.
The ``WrappedCursor`` module implements Python DB-API 2.0 interface to allow uniform access to various
database backends.
