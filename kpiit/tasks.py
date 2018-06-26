# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

import json
import itertools
import os

import requests
from celery import chord
from celery.utils.log import get_task_logger

from .app import app

logger = get_task_logger(__name__)

RECORDS_URLS = dict(
    zenodo='zenodo_records.json',
    videos='videos_records.json',
    opendata='opendata_records.json',
    # zenodo='https://zenodo.org/api/records/?all_versions',
    # videos='https://videos.cern.ch/api/records/?all_versions',
    # opendata='http://opendata.cern.ch/api/records/?all_versions'
)


@app.task
def collect_kpi():
    # return chord([num_records_collect.s()])(collect_kpi_done.s())
    collect_num_records = (num_records.s(name, url)
                           for name, url in RECORDS_URLS.items())
    return chord(itertools.chain(collect_num_records))(collect_kpi_done.s())


@app.task
def collect_kpi_done(data):
    test = {key: value
            for num_record in data for key, value in num_record.items()}
    logger.info(test)
    return data


@app.task
def num_records(name, url):
    """Get # of records for the given URL."""
    # req = requests.get(url)
    # data = req.json()
    with open(url, 'r') as f:
        data = json.loads(f.read())

    record_count = data['hits']['total']
    # logger.debug('# of records ({}): {}'.format(name, record_coun))

    key = '{}_num_records'.format(name)

    return {key: record_count}
