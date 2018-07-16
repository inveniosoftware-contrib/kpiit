# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

import os
import time

from celery import chain
from celery.utils.log import get_task_logger

from .app import app
from .util import load_target

logger = get_task_logger(__name__)

PUBLISH_ID = 1


@app.task
def collect_and_publish_metrics(*args, **kwargs):
    """Collect metrics then publish."""
    metrics_paths = kwargs['metrics']

    # Skip publishing if no publisher is given
    if 'publisher' not in kwargs or not isinstance(kwargs['publisher'], str):
        return collect_metrics.s(metrics_paths)

    # Publish when collecting metrics is completed
    return chain(
        collect_metrics.s(metrics_paths),
        publish_metrics.s(kwargs['publisher'])
    )()


@app.task
def collect_metrics(metrics_paths):
    """Collect metrics."""
    metric_instances = [load_target(path) for path in metrics_paths]

    for inst in metric_instances:
        inst.collect()

    return metric_instances


@app.task
def publish_metrics(metrics, publisher_path):
    """Publish metrics."""
    Publisher = load_target(publisher_path)

    global PUBLISH_ID

    publisher = Publisher('output_{id}_{now}.json'.format(
        id=PUBLISH_ID,
        now=time.strftime("%Y%m%d-%H%M%S")
    ))
    PUBLISH_ID += 1
    publisher.publish(metrics)
