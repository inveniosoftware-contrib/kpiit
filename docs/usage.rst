..
    Copyright (C) 2018 CERN.

    KPIit is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Usage
=====

.. automodule:: kpiit

Deployment
----------

The deployment process consist of building and tagging the Docker image. The image is then pushed to CERN's OpenShift container registry. The worker deployment's config file is then updated to force a restart.

All the steps described above are automated with the ``deploy`` command which is located in the ``openshift`` directory.

**Note:** The ``deploy`` script will only work if the user is authenticated with OpenShift using the ``oc login`` command. See ``oc login --help`` for more details on how to login. An alternative is to generate a one-time login command from `openshift.cern.ch <https://openshift.cern.ch/>`_ (click your username in the top right corner then "Copy Login Command" and paste in the terminal).

Secrets
~~~~~~~

To add a new secret to OpenShift use the following template: https://docs.openshift.com/container-platform/3.5/dev_guide/secrets.html

.. code-block:: yaml

    apiVersion: v1
    kind: Secret
    metadata:
    name: <name-of-secret>
    type: Opaque
    data:
    web_key: <Base64 encoded API key>
    search_key: <Base64 encoded API key>
    files_key: <Base64 encoded API key>

Save the YAML file then push the secret to OpenShift:

    oc create -f ./path/to/file.yaml

Open OpenShift and the deployment and edit the "Environment" and press "Add Value from Config Map or Secret" and choose the new secret.

Keytab file
~~~~~~~~~~~

A Kerberos keytab file should be generated with the ``ktutil`` command by using the following instructions:
https://kb.iu.edu/d/aumh#create

Example:

.. code-block:: bash

    > ktutil
    ktutil:  addent -password -p username@CERN.CH -k 1 -e aes256-cts
    Password for username@ADS.IU.EDU: [enter your password]
    ktutil:  wkt username.keytab
    ktutil:  quit

The keytab file should be created in the same directory as kpiit and the principal and keytab_file are specified using secrets.

Command: ``deploy``
~~~~~~~~~~~~~~~~~~~

.. argparse::
    :filename: ../openshift/deploy
    :func: create_parser
    :prog: deploy
