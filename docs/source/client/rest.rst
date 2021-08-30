==================================
PanDA system python API reference
==================================

Low-level system API are available via the pandaclient.Client module.

.. code-block:: python

  from pandaclient import Client
  Client.function_xyz(...)

System API
-----------

.. code-block:: text

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


    getPandaIDsWithTaskID(jediTaskID, verbose=False)
        Get PanDA IDs with TaskID

        args:
            jediTaskID: jediTaskID of the task to get lit of PanDA IDs
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            the list of PanDA IDs, or error message if failed


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

    get_user_name_from_token()
        Extract user name and groups from ID token

        returns:
           a tuple of username and groups

    hello(verbose=False)
        Health check with the PanDA server
        args:
           verbose: True to see verbose message
        returns:
           status code
              0: communication succeeded to the panda server
            255: communication failure
           diagnostic message

    insertTaskParams(taskParams, verbose=False, properErrorCode=False)
        Insert task parameters

        args:
            taskParams: a dictionary of task parameters
            verbose: True to see verbose messages
            properErrorCode: True to get a detailed error code
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

    send_command_to_job(panda_id, com)
        args:
            panda_id: PandaID of the job
            com: a command string passed to the pilot. max 250 chars
        returns:
            status code
                  0: communication succeeded to the panda server
                  255: communication failure
            return: a tuple of return code and message
                  False: failed
                  True: the command received

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
