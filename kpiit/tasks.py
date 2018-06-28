# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

import os

from celery import chain
from celery.utils.log import get_task_logger

from .app import app
from .util import load_target

logger = get_task_logger(__name__)


@app.task
def collect_and_publish(*args, **kwargs):
    """Collect metrics then publish."""
    metrics_paths = kwargs['metrics']

    # Skip publishing if no publisher is given
    if 'publisher' not in kwargs or not isinstance(kwargs['publisher'], str):
        return collect_metrics.s(metrics_paths)

    # Publish when metrics collection is completed
    return chain(
        collect_metrics.s(metrics_paths),
        publish_metrics.s(kwargs['publisher'])
    )()


@app.task
def collect_metrics(metrics_paths):
    """Collect metrics."""
    metric_instances = [load_target(path)() for path in metrics_paths]

    for inst in metric_instances:
        inst.collect()

    return [inst.metric.values for inst in metric_instances]


@app.task
def publish_metrics(metrics, publisher_path):
    """Publish metrics."""
    Publisher = load_target(publisher_path)

    publisher = Publisher()
    publisher.publish(metrics)
