# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

import itertools
import json
import os

import requests
from celery import chord
from celery.utils.log import get_task_logger

from .app import app

logger = get_task_logger(__name__)


@app.task
def collect_metrics():
    """Collect metrics."""
    pass


@app.task
def publish_metrics(metrics):
    """Publish metrics."""
    pass


# @app.task
# def collect_kpi():
#     """Collect KPI."""
#     collect_num_records = (num_records.s(name, url)
#                            for name, url in RECORDS_URLS.items())
#     return chord(itertools.chain(collect_num_records))(collect_kpi_done.s())


# @app.task
# def collect_kpi_done(data):
#     kpi = {key: value
#            for num_record in data for key, value in num_record.items()}
#     logger.info(kpi)
#     with open('output.json', 'w+') as f:
#         f.write(build_kpi_message('testserviceid', 'available', **kpi))
#     return kpi


# @app.task
# def num_records(name, url):
#     """Get # of records for the given URL."""
#     # req = requests.get(url)
#     # data = req.json()
#     with open(url, 'r') as f:
#         data = json.loads(f.read())

#     record_count = data['hits']['total']
#     # logger.debug('# of records ({}): {}'.format(name, record_coun))

#     key = '{}_num_records'.format(name)

#     return {key: record_count}
