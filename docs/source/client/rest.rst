==================================
PanDA client python API reference
==================================

Low-level system API are available via the pandaclient.Client module.

.. code-block:: python

  from pandaclient import Client
  Client.function_xyz(...)

For example, you can get a new ID token for an administrative purpose as follows.

.. code-block:: python

  token = Client.get_new_token()
  print(token)

System API
-----------

.. code-block:: text

    call_idds_command(command_name, args=None, kwargs=None, dumper=None, verbose=False, compress=False, manager=False, loader=None, json_outputs=False)
        Call an iDDS command through PanDA
        args:
           command_name: command name
           args: a list of positional arguments
           kwargs: a dictionary of keyword arguments
           dumper: function object for json.dumps
           verbose: True to see verbose message
           compress: True to compress request body
           manager: True to use ClientManager
           loader: function object for json.loads
           json_outputs: True to use json outputs
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True, response from iDDS), or (False, diagnostic message) if failed

    call_idds_user_workflow_command(command_name, kwargs=None, verbose=False, json_outputs=False)
        Call an iDDS workflow user command
        args:
           command_name: command name
           kwargs: a dictionary of keyword arguments
           verbose: True to see verbose message
           json_outputs: True to use json outputs
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True, response from iDDS), or (False, diagnostic message) if failed

    dump_log(func_name, exception_obj, output)
        # dump log

    finishTask(jediTaskID, soft=False, verbose=False)
        finish a task
        args:
           jediTaskID: jediTaskID of the task to finish
           soft: True to wait until running jobs are done
           verbose: True to see debug messages
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           tuple of return code and diagnostic message, or None if failed
              0: request is registered
              1: server error
              2: task not found
              3: permission denied
              4: irrelevant task status
            100: non SSL connection
            101: irrelevant taskID

    getCachePrefixes(verbose)
        # get list of cache prefix
        # OBSOLETE to be removed in a future release

    getCmtConfigList(athenaVer, verbose)
        # get list of cmtConfig
        # OBSOLETE to be removed in a future release

    getDN(origString)
        # get DN

    getFile(filename, output_path=None, verbose=False)
        Get a file
        args:
           filename: filename to be downloaded
           output_path: output path. set to filename if unspecified
           verbose: True to see debug messages
        returns:
           status code
              0: communication succeeded to the panda server
              1: communication failure
           True if succeeded. diagnostic message otherwise

    getFullJobStatus(ids, verbose=False)
        Get detailed status of jobs

        args:
            ids: a list of PanDA IDs
            verbose: True to see verbose messages
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            a list of job specs, or None if failed

    getJediTaskDetails(taskDict, fullFlag, withTaskInfo, verbose=False)
        # get details of jedi task

    getJobIDsJediTasksInTimeRange(timeRange, dn=None, minTaskID=None, verbose=False, task_type='user')
        # get JobIDs and jediTasks in a time range

    getJobStatus(ids, verbose=False)
        Get status of jobs

        args:
            ids: a list of PanDA IDs
            verbose: True to see verbose messages
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            a list of job specs, or None if failed

    getPandaClientVer(verbose)
        # get client version

    getPandaIDsWithTaskID(jediTaskID, verbose=False)
        Get PanDA IDs with TaskID

        args:
            jediTaskID: jediTaskID of the task to get lit of PanDA IDs
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            the list of PanDA IDs, or error message if failed

    getProxyKey(verbose=False)
        # get proxy key

    getTaskParamsMap(jediTaskID)
        Get task parameters

        args:
            jediTaskID: jediTaskID of the task to get taskParamsMap
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            return: a tuple of return code and taskParamsMap, or error message if failed
                  1: logical error
                  0: success
                  None: database error

    getTaskStatus(jediTaskID, verbose=False)
        Get task status

        args:
            jediTaskID: jediTaskID of the task to get lit of PanDA IDs
            verbose: True to see verbose messages
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            the status string, or error message if failed

    getUserJobMetadata(task_id, verbose=False)
        Get metadata of all jobs in a task
        args:
           jediTaskID: jediTaskID of the task
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a list of job metadata dictionaries, or error message if failed

    get_cert_attributes(verbose=False)
        Get certificate attributes from the PanDA server
        args:
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a dictionary of attributes or diagnostic message

    get_new_token()
        Get new ID token

        returns: a string of ID token. None if failed

    get_token_string(tmp_log, verbose)
        # get token string

    get_user_name_from_token()
        Extract username and groups from ID token

        returns:
           a tuple of username and groups

    get_user_secerts(verbose=False)
        Get user secrets
        args:
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True/False and a dict of secrets). True if the request was accepted

    hello(verbose=False)
        Health check with the PanDA server
        args:
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           diagnostic message

    hide_sensitive_info(com)
        # hide sensitive info

    increase_attempt_nr(task_id, increase=3, verbose=False)
        increase attempt numbers to retry failed jobs
        args:
           task_id: jediTaskID of the task
           increase: increase for attempt numbers
           verbose: True to see verbose message
        returns:
           status code
                 0: communication succeeded to the panda server
                 255: communication failure
           return code
                 0: succeeded
                 1: unknown task
                 2: invalid task status
                 3: permission denied
                 4: wrong parameter
                 None: database error

    insertTaskParams(taskParams, verbose=False, properErrorCode=False, parent_tid=None)
        Insert task parameters

        args:
            taskParams: a dictionary of task parameters
            verbose: True to see verbose messages
            properErrorCode: True to get a detailed error code
            parent_tid: ID of the parent task
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            tuple of return code, message from the server, and taskID if successful, or error message if failed
                  0: request is processed
                  1: duplication in DEFT
                  2: duplication in JEDI
                  3: accepted for incremental execution
                  4: server error

    is_https(url)
        # check if https

    killJobs(ids, verbose=False)
        Kill jobs

        args:
            ids: a list of PanDA IDs
            verbose: True to see verbose messages
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            a list of server responses, or None if failed

    killTask(jediTaskID, verbose=False)
        Kill a task
        args:
           jediTaskID: jediTaskID of the task to be killed
           verbose: True to see debug messages
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           tuple of return code and diagnostic message, or None if failed
              0: request is registered
              1: server error
              2: task not found
              3: permission denied
              4: irrelevant task status
            100: non SSL connection
            101: irrelevant taskID

    pauseTask(jediTaskID, verbose=False)
        Pause task

        args:
            jediTaskID: jediTaskID of the task to pause
            verbose: True to see verbose messages
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            return: a tupple of return code and message, or error message if failed
                  0: request is registered
                  1: server error
                  2: task not found
                  3: permission denied
                  4: irrelevant task status
                  100: non SSL connection
                  101: irrelevant taskID
                  None: database error

    putFile(file, verbose=False, useCacheSrv=False, reuseSandbox=False)
        Upload a file with the size limit on 10 MB
        args:
           file: filename to be uploaded
           verbose: True to see debug messages
           useCacheSrv: True to use a dedicated cache server separated from the PanDA server
           reuseSandbox: True to avoid uploading the same sandbox files
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           diagnostic message

    reactivateTask(jediTaskID, verbose=False)
        Reactivate task

        args:
            jediTaskID: jediTaskID of the task to be reactivated
            verbose: True to see verbose messages
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            return: a tupple of return code and message, or error message if failed
                  0: unknown task
                  1: succeeded
                  None: database error

    registerProxyKey(credname, origin, myproxy, verbose=False)
        # register proxy key

    reload_input(task_id, verbose=False)
        Retry task
        args:
            task_id: jediTaskID of the task to reload and retry
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            tuple of return code and diagnostic message
                  0: request is registered
                  1: server error
                  2: task not found
                  3: permission denied
                  4: irrelevant task status
                100: non SSL connection
                101: irrelevant taskID

    requestEventPicking(eventPickEvtList, eventPickDataType, eventPickStreamName, eventPickDS, eventPickAmiTag, fileList, fileListName, outDS, lockedBy, params, eventPickNumSi
tes, eventPickWithGUID, ei_api, verbose=False)
        # request EventPicking

    resumeTask(jediTaskID, verbose=False)
        Resume task

        args:
            jediTaskID: jediTaskID of the task to be resumed
            verbose: True to see verbose messages
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            return: a tupple of return code and message, or error message if failed
                  0: request is registered
                  1: server error
                  2: task not found
                  3: permission denied
                  4: irrelevant task status
                  100: non SSL connection
                  101: irrelevant taskID
                  None: database error

    retryTask(jediTaskID, verbose=False, properErrorCode=False, newParams=None)
        retry a task
        args:
           jediTaskID: jediTaskID of the task to retry
           verbose: True to see debug messages
           newParams: a dictionary of task parameters to overwrite
           properErrorCode: True to get a detailed error code
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           tuple of return code and diagnostic message, or None if failed
              0: request is registered
              1: server error
              2: task not found
              3: permission denied
              4: irrelevant task status
            100: non SSL connection
            101: irrelevant taskID

    send_file_recovery_request(task_id, dry_run=False, verbose=False)
        Send a file recovery request
        args:
           task_id: task ID
           dry_run: True to run in the dry run mode
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True/False and diagnostic message). True if the request was accepted

    send_workflow_request(params, relay_host=None, check=False, verbose=False)
        Send a workflow request
        args:
           params: a workflow request dictionary
           relay_host: relay hostname to send request
           check: only check the workflow description
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True/False and diagnostic message). True if the request was accepted

    setCacheServer(host_name)
        # set cache server

    setDebugMode(pandaID, modeOn, verbose)
        # set debug mode

    setGlobalTmpDir(tmpDir)
        # set tmp dir

    set_user_secert(key, value, verbose=False)
        Set a user secret
        args:
           key: secret name. None to delete all secrets
           value: secret value. None to delete the secret
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           a tuple of (True/False and diagnostic message). True if the request was accepted

    str_decode(data)
        # string decode for python 2 and 3

    submitJobs(jobs, verbose=False)
        # submit jobs

    useDevServer()
        # use dev server

    useIntrServer()
        # use INTR server

    use_oidc()
        # use OIDC

    use_x509_no_grid()
        # use X509 without grid middleware



