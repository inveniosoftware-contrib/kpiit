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

**Note:** The ``deploy`` script will only work if the user is authenticated with OpenShift using the ``oc login`` command. See ``oc login --help`` for more details on how to login. An alternative is to generate a one-time login command from `openshift.cern.ch <https://openshift.cern.ch/>`_ (click your username in the top right corner then "Copy Login Command" and paste in the terminal.

Command: ``deploy``
~~~~~~~~~~~~~~~~~~~

.. argparse::
    :filename: openshift/deploy
    :func: create_parser
    :prog: deploy