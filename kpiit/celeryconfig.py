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

from .json import metric_dumps, metric_loads


def _env(key, default):
    return os.environ.get(key, default)


# Register new JSON serializer
register(
    'metricjson',
    metric_dumps,
    metric_loads,
    content_type='application/x-metricjson',
    content_encoding='utf-8'
)

#: URL of message broker for Celery (default is Redis).
broker_url = _env('BROKER_URL', 'redis://localhost:6379/0')
#: URL of backend for result storage (default is Redis).
result_backend = _env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
#: List of modules to import when the Celery worker starts.
imports = ['kpiit.tasks']
#: Scheduled tasks configuration (aka cronjobs).
beat_schedule = {
    'collect-kpi-every-day-after-midnight': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': crontab(hour=0, minute=20),
        # 'schedule': 10.0,
        'kwargs': {
            'metrics': [
                'kpiit.metrics.zenodo_records_metric',
                'kpiit.metrics.cod_records_metric',
                'kpiit.metrics.zenodo_doi_metric',
            ],
            'publisher': 'kpiit.publishers.json.JSONFilePublisher'
        }
    }
}
#: Accept the new serializer
accept_content = ['metricjson']
#: Serialize JSON with the custom serializer
task_serializer = 'metricjson'
#: Serialize result with the custom serializer
result_serializer = 'metricjson'
