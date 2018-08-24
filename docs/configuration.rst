..
    Copyright (C) 2018 CERN.

    KPIit is free software; you can redistribute it and/or modify i
    under the terms of the MIT License; see LICENSE file for more details.


Configuration
=============

KPIit can be configured by editing the configuration files located in
``kpiit/config.cfg`` and ``kpiit/config.<KPIIT_ENV>.cfg`` where ``<KPIIT_ENV>`` is
the selected environment. The environment can be specified using the
``KPIIT_ENV`` environment variable.

Config files are parsed using `configobj <https://configobj.readthedocs.io/en/latest/>`_.

Environment variables
---------------------

* ``KPIIT_ENV``: Environment to use, defaults to: *development*

See :ref:`secrets-label` for more information on the OpenShift secrets that are exposed as environment variables.

.. _secrets-label:

Secrets
~~~~~~~

OpenShift secrets are exposed as environment variables. Secrets are used to store usernames and passwords.

ServiceNow:

* ``SNOW_USER``: ServiceNow username
* ``SNOW_PASS``: ServiceNow password

Uptime:

* ``ZENODO_UPTIME_WEBSITE_API_KEY``: Zenodo web API key
* ``ZENODO_UPTIME_SEARCH_API_KEY``: Zenodo search API key
* ``ZENODO_UPTIME_FILES_API_KEY``: Zenodo files API key
* ``CDS_VIDEOS_UPTIME_WEBSITE_API_KEY``: CDS Videos web API key
* ``CDS_VIDEOS_UPTIME_SEARCH_API_KEY``: CDS Videos search API key
* ``CDS_VIDEOS_UPTIME_FILES_API_KEY``: CDS Videos files API key
* ``COD_UPTIME_WEBSITE_API_KEY``: COD web API key
* ``COD_UPTIME_SEARCH_API_KEY``: COD search API key
* ``COD_UPTIME_FILES_API_KEY``: COD files API key

Config files
------------

* ``kpiit/config.cfg``: Main config file
* ``kpiit/config.<KPIIT_ENV>.cfg``: The environment config file is loaded after the main file. Used for environment specific values that replaces the values in the main config file.