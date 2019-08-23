# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks."""

from celery import chain
from celery.utils.log import get_task_logger
from requests.exceptions import RequestException

from kpiit.app import app
from kpiit.metrics.base import BaseMetric
from kpiit.util import load_target

logger = get_task_logger(__name__)


@app.task
def collect_and_publish_metrics(*args, **kwargs):
    """Collect metrics then publish."""
    metrics = kwargs['metrics']

    # Skip publishing if no publisher is given
    if not ('publishers' in kwargs and isinstance(kwargs['publishers'], dict)):
        logger.debug('Skipping publishing because no publishers were set.')
        return collect_metrics.s(metrics)

    for metric in metrics.values():
        chain(
            collect_metrics.s(metric),
            publish_metrics.s(kwargs['publishers'])
        )()


@app.task(autoretry_for=(RequestException,),
          retry_backoff=True,
          retry_kwargs={'max_retries': 10})
def collect_metrics(metric):
    """Collect metrics."""
    # when 'retrying' is passing the instance and not the metric dictionary
    if isinstance(metric, BaseMetric):
        metric_instance = metric
    else:
        metric_instance = load_target(metric['instance'])(*metric['args'],
                                                          **metric['kwargs'])
    metric_instance.collect()
    logger.debug('collected metrics for "{}"'.format(metric_instance.name))

    return metric_instance


@app.task(autoretry_for=(RequestException,),
          retry_backoff=True,
          retry_kwargs={'max_retries': 10})
def publish_metrics(metric, publishers):
    """Publish metrics."""
    publisher_instances = [load_target(
                           args['instance'])(*args['args'], **args['kwargs'])
                           for obj, args in publishers.items()
                           ]

    for publisher in publisher_instances:
        publisher.publish(metric)
        logger.debug('published metrics for "{}"'.format(metric.name))
