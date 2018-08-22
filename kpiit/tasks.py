# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

from celery import chain
from celery.utils.log import get_task_logger

from kpiit.app import app
from kpiit.util import load_target

logger = get_task_logger(__name__)


@app.task
def collect_and_publish_metrics(*args, **kwargs):
    """Collect metrics then publish."""
    metrics = kwargs['metrics']

    logger.info('collect_and_publish_metrics(%s, %s)' % (args, kwargs))

    # Skip publishing if no publisher is given
    if not ('publishers' in kwargs and isinstance(kwargs['publishers'], dict)):
        logger.debug('Skipping publishing because no publishers were set.')
        return collect_metrics.s(metrics)

    # Publish when collecting metrics is completed
    return chain(
        collect_metrics.s(metrics),
        publish_metrics.s(kwargs['publishers'])
    )()


@app.task
def collect_metrics(metrics):
    """Collect metrics."""
    logger.info('collect_metrics', metrics)
    metric_instances = [load_target(obj)(*args['args'], **args['kwargs'])
                        for obj, args in metrics.items()]

    for metric in metric_instances:
        metric.collect()

    return metric_instances


@app.task
def publish_metrics(metrics, publishers):
    """Publish metrics."""
    logger.debug('publish_metrics', metrics, publishers)
    publisher_instances = [load_target(obj)(*args['args'], **args['kwargs'])
                           for obj, args in publishers.items()]

    for publisher in publisher_instances:
        publisher.publish(metrics)
