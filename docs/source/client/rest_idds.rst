==================================
Using iDDS API through PanDA
==================================

iDDS delegates user authentication and authorization to the PanDA server so that iDDS APIs are available
through panda-client. The PanDA server forwards requests to iDDS after receiving them from users
and propagates responses from iDDS back to the users.
The following code snippets show how iDDS native codes migrate to panda-client based codes:

* iDDS native

.. code-block:: python

    from idds.client.client import Client
    from idds.client.clientmanager import ClientManager
    import idds.common.constants
    import idds.common.utils

    data = {
        'requester': 'panda',
        'request_type': idds.common.constants.RequestType.HyperParameterOpt,
        'transform_tag': idds.common.constants.RequestType.HyperParameterOpt.value,
        'status': idds.common.constants.RequestStatus.New,
        'priority': 0,
        'lifetime': 30,
        'request_metadata': {},
    }

    # using Client API
    cl = Client(idds.common.utils.get_rest_host())
    try:
        request_id = cl.add_request(**data)
    except Except:
        # error

    # using ClientManager
    cm = ClientManager(idds.common.utils.get_rest_host())
    try:
        req = cm.get_requests(request_id=request_id)
    except Exception:
        # error

* panda-client based

.. code-block:: python

    import pandaclient.idds_api
    import idds.common.constants
    import idds.common.utils

    data = {
        'requester': 'panda',
        'request_type': idds.common.constants.RequestType.HyperParameterOpt,
        'transform_tag': idds.common.constants.RequestType.HyperParameterOpt.value,
        'status': idds.common.constants.RequestStatus.New,
        'priority': 0,
        'lifetime': 30,
        'request_metadata': {},
    }

    # using Client API
    cl = pandaclient.idds_api.get_api(idds.common.utils.json_dumps, compress=True)
    ret = cl.add_request(**data)
    if ret[0] == 0 and ret[1][0]:
        request_id = ret[1][-1]
    else:
        # error

    # using ClientManager
    cm = pandaclient.idds_api.get_api(dumper=idds.common.utils.json_dumps, loader=idds.common.utils.json_loads,
        compress=True, manager=True)
    ret = cm.get_requests(request_id=request_id)
    if ret[0] == 0 and ret[1][0]:
        req = ret[1][-1]
    else:
        # error


All client functions of ``idds.client.client.Client`` and ``idds.client.clientmanager.ClientManager``
are available in the API object, which is returned by
``pandaclient.idds_api.get_api()``,
with the same arguments. Check with iDDS documentation for the details of iDDS API.
Here is the description of ``pandaclient.idds_api.get_api()``.

.. code-block:: text

    get_api(dumper=None, verbose=False, idds_host=None, compress=False, manager=False)
        Get an API object to access iDDS through PanDA

        args:
            dumper: function object to json-serialize data
            verbose: True to see verbose messages
            idds_host: iDDS host. e.g. https://aipanda160.cern.ch:443/idds
            compress: True to compress request body
            manager: True to use ClientManager API. False by default to use Client API
        return:
            an API object

The returns from any function of the API object are always as follows.

.. code-block:: text

        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True, the original response from iDDS), or (False, diagnostic message) if failed
