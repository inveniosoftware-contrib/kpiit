# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

import os

import kpi
import requests
from celery import chord
from celery.utils.log import get_task_logger

from .app import app

logger = get_task_logger(__name__)

RECORDS_URLS = dict(
    zenodo='https://zenodo.org/api/records/?all_versions',
    videos='https://videos.cern.ch/api/records/?all_versions',
    opendata='http://opendata.cern.ch/api/records/?all_versions'
)


@app.task
def num_records_collect():
    """Get # of records for all services then collect them."""
    return chord(num_records.s(name, url) for name, url in RECORDS_URLS.items())(num_records_done.s())

@app.task
def num_records(name, url):
    """Get # of records for the given URL."""
    req = requests.get(url)
    json = req.json()

    num_records = json['hits']['total']
    logger.debug('# of records ({}): {}'.format(name, num_records))

    return name, num_records

@app.task
def num_records_done(values):
    logger.info('collected num_records KPI: {}'.format(values))
