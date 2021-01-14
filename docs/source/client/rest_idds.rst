==================================
Using iDDS API through PanDA
==================================

iDDS delegates user authentication and authorization to the PanDA server, so that iDDS APIs are available
through panda-client. The PanDA server forwards requests to iDDS after receiving them from users,
and propagates responses from iDDS back to the users.
The following code snippets show how iDDS native codes migrate to panda-client based codes:

* iDDS native

.. code-block:: python

    from idds.client.client import Client
    import idds.common.constants
    import idds.common.utils

    req = {
        'requester': 'panda',
        'request_type': idds.common.constants.RequestType.HyperParameterOpt,
        'transform_tag': idds.common.constants.RequestType.HyperParameterOpt.value,
        'status': idds.common.constants.RequestStatus.New,
        'priority': 0,
        'lifetime': 30,
        'request_metadata': {},
    }

    c = Client(idds.common.utils.get_rest_host())
    ret = c.add_request(**req)

* panda-client based

.. code-block:: python

    import pandatools.idds_api
    from pandatools.idds_common import constants

    req = {
        'requester': 'panda',
        'request_type': constants.RequestType.HyperParameterOpt,
        'transform_tag': constants.RequestType.HyperParameterOpt.value,
        'status': constants.RequestStatus.New,
        'priority': 0,
        'lifetime': 30,
        'request_metadata': {},
    }

    c = pandatools.idds_api.get_api()
    ret = c.add_request(**req)

All constants in *idds.common.constants* are available in ``constants`` of ``pandatools.idds_common``.
All client functions of ``idds.client.client.Client`` are available in the object returned by
``pandatools.idds_api.get_api()``
with the same arguments. Check with iDDS documentation for the details of iDDS API.