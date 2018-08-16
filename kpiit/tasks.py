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


@app.task
def collect_and_publish_metrics(*args, **kwargs):
    """Collect metrics then publish."""
    metrics = kwargs['metrics']

    # Skip publishing if no publisher is given
    if 'publisher' not in kwargs or not isinstance(kwargs['publisher'], str):
        return collect_metrics.s(metrics)

    # Publish when collecting metrics is completed
    return chain(
        collect_metrics.s(metrics),
        publish_metrics.s(kwargs['publisher'])
    )()


@app.task
def collect_metrics(metrics):
    """Collect metrics."""
    metric_instances = [load_target(obj)(*args['args'], **args['kwargs'])
                        for obj, args in metrics.items()]

    for metric in metric_instances:
        metric.collect()

    return metric_instances


@app.task
def publish_metrics(metrics, publishers):
    """Publish metrics."""
    publisher_instances = [load_target(obj)(*args['args'], **args['kwargs'])
                           for obj, args in publishers.items()]

    for publisher in publisher_instances:
        publisher.publish(metrics)
