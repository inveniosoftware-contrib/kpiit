# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

import os
import requests

from celery.utils.log import get_task_logger
from .app import app

ZENODO_RECORDS_URL = 'https://zenodo.org/api/records/?all_versions'
logger = get_task_logger(__name__)


@app.task
def num_records():
    """Get KPI for number of records."""
    zenodo_req = requests.get(ZENODO_RECORDS_URL)
    zenodo_json = zenodo_req.json()

    # TODO: validate json content
    num_records = zenodo_json['hits']['total']

    return num_records
