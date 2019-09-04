# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration for KPIit."""

import os

from celery.schedules import crontab
from kombu.serialization import register

from kpiit.config import config
from kpiit.json import metric_dumps, metric_loads

# Register new JSON serializer
register(
    config['celery']['serializer'],
    metric_dumps,
    metric_loads,
    content_type='application/x-metricjson',
    content_encoding='utf-8'
)


# Default schedule crontabs
SCHEDULE_DOI_MONTHLY = crontab(**config['celery']['schedules']['doi'])
SCHEDULE_REPO_DAILY = crontab(**config['celery']['schedules']['repo'])

#: URL of message broker for Celery (default is Redis).
broker_url = config['celery']['broker_url']
#: URL of backend for result storage (default is Redis).
result_backend = config['celery']['result_backend']
#: List of modules to import when the Celery worker starts.
imports = ['kpiit.tasks']

#: Scheduled tasks configuration (aka cronjobs).
beat_schedule = config.beat_schedule

#: Accept the new serializer
accept_content = [config['celery']['serializer']]
#: Serialize JSON with the custom serializer
task_serializer = config['celery']['serializer']
#: Serialize result with the custom serializer
result_serializer = config['celery']['serializer']
