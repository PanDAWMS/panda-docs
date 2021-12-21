=========================
Using secrets
=========================

Introduction
--------------

A secret is a small amount of sensitive data such as an access token and a password.
PanDA allows users to define arbitrary key-value strings to feed secrets to jobs.
They are encrypted in PanDA and decrypted on the compute node, and are exposed to jobs
as environment variables.
Note that the key-values are random strings from PanDA’s point of view, and users can further encrypt
those strings by themselves, so the system should not abuse the sensitive information.

.. figure:: images/secrets.png

How to manage secrets
---------------------------

``pbook`` provides following functions to manage secrets.

.. code-block:: bash

    set_secret
    list_secrets
    delete_secret
    delete_all_secrets

You can define a set of key-value strings using :blue:`set_secret`.

.. code-block:: bash

   >>> # set_secret(key, value)
   >>> set_secret('MY_SECRET', 'random_string')
   INFO : OK

The key is used as the environment variable name on worker nodes. The value must be a string.
If you want to define non-string secrets, serialize them using ``json.dumps``,
``base64.b64encode``, or something, beforehand. E.g.,

.. code-block:: bash

   >>> # define a dictionary secret using json.dumps
   >>> import json
   >>> set_secret('MY_SECRET_DIC', json.dumps({'a_key': 'a_value'}))
   INFO : OK

It is also possible to upload secret files if their size is less than 1000 kB,

.. code-block:: bash

   >>> # upload a secret file
   >>> set_secret('my_secret_file.dat', '/somewhere/secret_file_path', is_file=True)
   INFO : OK

so that jobs get those files, where the key is the remote filename while the value is the local file path.

``list_secrets`` shows all secrets.

.. code-block:: bash

    >>> list_secrets()

        Key                : Value
        ------------------ : --------------------
        MY_SECRET          : random_string
        MY_SECRET_DIC      : {"a_key": "a_value"}
        my_secret_file.dat : H4sIABmjwWEAA+3TTU7DMBA...
        ...

where value strings are truncated by default. Set ``full=True`` to see entire strings.

You can delete secrets using :blue:`delete_secret` and/or :blue:`delete_all_secrets`.

Using secrets in your jobs
---------------------------------

``prun`` has the :blue:`--useSecrets` option to feed secrets into jobs running on computing resources.
Once jobs get started the secrets should be available as environment variables or files in the current directory.
Your applications would do something like

.. code-block:: python

  import os
  import json
  # using an ordinary secret
  do_something_with_a_secret(os.environ['MY_SECRET'])
  # using a dictionary secret
  dict_secret = json.loads(os.environ['MY_SECRET_DIC'])
  do_something_with_a_dictionary_secret(dict_secret['a_key'])
  # using a secret file
  with open('my_secret_file.dat', 'wb') as f:
      do_something_with_a_secret_file(f)
