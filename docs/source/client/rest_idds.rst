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

    c = pandatools.idds_api.get_api(idds.common.utils.json_dumps, compress=True)
    ret = c.add_request(**req)
    if ret[0] == 0 and ret[0][0]:
        ret = ret[0][-1]


All client functions of ``idds.client.client.Client`` are available in the API object given by
``pandatools.idds_api.get_api()``
with the same arguments. Check with iDDS documentation for the details of iDDS API.
Here is the description of ``pandatools.idds_api.get_api()``.

.. code-block:: text

    get_api(dumper=None, verbose=False, idds_host=None, compress=False)
        Get an API object to access iDDS through PanDA

        args:
            dumper: function object to json-serialize data
            verbose: True to see verbose messages
            idds_host: iDDS host. e.g. https://aipanda160.cern.ch:443/idds
            compress: True to compress request body
        return:
            an API object

The returns from any function of the API object are always as follows.

.. code-block:: text

        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True, the original response from iDDS), or (False, diagnostic message) if failed
