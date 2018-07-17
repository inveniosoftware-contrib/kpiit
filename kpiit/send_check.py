# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Send JSON documents to CERN's Grafana instance."""

import json

import requests

PRODUCTION = False

PROD_URL = 'http://monit-metrics.cern.ch:10012'
DEV_URL = 'http://monit-metrics-dev:10012/'


def send(document, production):
    """Send JSON document to CERN monit."""
    host = PROD_URL if production else DEV_URL
    print('sending document to: ', host)
    return requests.post(
        host,
        data=json.dumps(document),
        headers={"Content-Type": "application/json; charset=UTF-8"}
    )
