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


def args(*args, **kwargs):
    """Get function arguments as a dictionary."""
    return dict(args=args, kwargs=kwargs)


# Default schedule crontabs
SCHEDULE_DOI_MONTHLY = crontab(day_of_month=1, hour=2)
SCHEDULE_REPO_DAILY = crontab(hour=8, minute=39)

#: URL of message broker for Celery (default is Redis).
broker_url = _env('BROKER_URL', 'redis://localhost:6379/0')
#: URL of backend for result storage (default is Redis).
result_backend = _env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
#: List of modules to import when the Celery worker starts.
imports = ['kpiit.tasks']
#: Scheduled tasks configuration (aka cronjobs).
beat_schedule = {
    'collect-zenodo-doi-kpis-every-month': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_DOI_MONTHLY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.doi': args('10.5281')
            },
            'publisher': {
                'kpiit.publishers.doi': args('10.5281')
            }
        }
    },
    'collect-cds-videos-doi-kpis-every-month': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_DOI_MONTHLY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.doi': args('10.17181')
            },
            'publisher': {
                'kpiit.publishers.doi': args('10.17181')
            }
        }
    },
    'collect-cod-doi-kpis-every-month': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_DOI_MONTHLY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.doi': args('10.7483')
            },
            'publisher': {
                'kpiit.publishers.doi': args('10.7483')
            }
        }
    },
    # 'collect-zenodo-repo-kpis-every-day': {
    #     'task': 'kpiit.tasks.collect_and_publish_metrics',
    #     'schedule': SCHEDULE_REPO_DAILY,
    #     'kwargs': {
    #         'metrics': [
    #             'kpiit.metrics.zenodo_records_metric',
    #             'kpiit.metrics.zenodo_website_uptime_metric',
    #             'kpiit.metrics.zenodo_search_uptime_metric',
    #             'kpiit.metrics.zenodo_files_uptime_metric',
    #             'kpiit.metrics.zenodo_visits_metric',
    #             'kpiit.metrics.zenodo_support_metric',
    #         ],
    #         'publisher': 'kpiit.publishers.zenodo_repo'
    #     }
    # },
    # 'collect-cds-videos-repo-kpis-every-day': {
    #     'task': 'kpiit.tasks.collect_and_publish_metrics',
    #     'schedule': SCHEDULE_REPO_DAILY,
    #     'kwargs': {
    #         'metrics': [
    #             'kpiit.metrics.cds_videos_records_metric',
    #             'kpiit.metrics.cds_videos_website_uptime_metric',
    #             'kpiit.metrics.cds_videos_search_uptime_metric',
    #             'kpiit.metrics.cds_videos_files_uptime_metric',
    #             'kpiit.metrics.cds_videos_visits_metric',
    #             'kpiit.metrics.cds_videos_support_metric',
    #         ],
    #         'publisher': 'kpiit.publishers.cds_videos_repo'
    #     }
    # },
    # 'collect-cod-repo-kpis-every-day': {
    #     'task': 'kpiit.tasks.collect_and_publish_metrics',
    #     'schedule': SCHEDULE_REPO_DAILY,
    #     'kwargs': {
    #         'metrics': [
    #             'kpiit.metrics.cod_records_metric',
    #             'kpiit.metrics.cod_website_uptime_metric',
    #             'kpiit.metrics.cod_search_uptime_metric',
    #             'kpiit.metrics.cod_files_uptime_metric',
    #             'kpiit.metrics.cod_visits_metric',
    #             'kpiit.metrics.dummy_support_metric',
    #         ],
    #         'publisher': 'kpiit.publishers.cod_repo'
    #     }
    # },
}
#: Accept the new serializer
accept_content = ['metricjson']
#: Serialize JSON with the custom serializer
task_serializer = 'metricjson'
#: Serialize result with the custom serializer
result_serializer = 'metricjson'
