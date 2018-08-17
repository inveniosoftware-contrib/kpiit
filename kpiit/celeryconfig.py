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

from kpiit import Env, Service
from kpiit.json import metric_dumps, metric_loads


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
# SCHEDULE_DOI_MONTHLY = crontab(day_of_month=1, hour=2)
SCHEDULE_DOI_MONTHLY = crontab(hour=11, minute=24)
SCHEDULE_REPO_DAILY = crontab(hour=11, minute=24)

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
                'kpiit.metrics.doi': args(prefix='10.5281')
            },
            'publisher': {
                'kpiit.publishers.doi': args(prefix='10.5281')
            }
        }
    },
    'collect-cds-videos-doi-kpis-every-month': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_DOI_MONTHLY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.doi': args(prefix='10.17181')
            },
            'publisher': {
                'kpiit.publishers.doi': args(prefix='10.17181')
            }
        }
    },
    'collect-cod-doi-kpis-every-month': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_DOI_MONTHLY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.doi': args(prefix='10.7483')
            },
            'publisher': {
                'kpiit.publishers.doi': args(prefix='10.7483')
            }
        }
    },
    'collect-zenodo-repo-kpis-every-day': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_REPO_DAILY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.records': args(
                    name='zenodo_records',
                    url='https://zenodo.org/api/records/?all_versions'
                ),
                'kpiit.metrics.uptime': args(
                    name='web',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('ZENODO_UPTIME_WEBSITE_API_KEY'),
                    monitor='Website',
                ),
                'kpiit.metrics.uptime': args(
                    name='search',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('ZENODO_UPTIME_SEARCH_API_KEY'),
                    monitor='Search',
                ),
                'kpiit.metrics.uptime': args(
                    name='files',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('ZENODO_UPTIME_FILES_API_KEY'),
                    monitor='Files upload/download',
                ),
                'kpiit.metrics.visits': args(
                    name='zenodo_support',
                    site_id=57
                ),
                'kpiit.metrics.support': args(
                    name='zenodo_support',
                    service=Service.ZENODO
                ),
            },
            'publisher': {
                'kpiit.publishers.repo': args(Service.ZENODO, Env.QA)
            }
        }
    },
    'collect-cds-videos-repo-kpis-every-day': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_REPO_DAILY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.records': args(
                    name='cds_videos_records',
                    url='https://videos.cern.ch/api/records/'
                ),
                'kpiit.metrics.uptime': args(
                    name='web',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('CDS_VIDEOS_UPTIME_WEBSITE_API_KEY'),
                    monitor='Website',
                ),
                'kpiit.metrics.uptime': args(
                    name='search',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('CDS_VIDEOS_UPTIME_SEARCH_API_KEY'),
                    monitor='Search',
                ),
                'kpiit.metrics.uptime': args(
                    name='files',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('CDS_VIDEOS_UPTIME_FILES_API_KEY'),
                    monitor='Files upload/download',
                ),
                'kpiit.metrics.visits': args(
                    name='cds_videos_support'
                ),
                'kpiit.metrics.support': args(
                    name='cds_videos_support',
                    service=Service.ZENODO
                ),
            },
            'publisher': {
                'kpiit.publishers.repo': args(Service.CDS_VIDEOS, Env.QA)
            }
        }
    },
    'collect-cod-repo-kpis-every-day': {
        'task': 'kpiit.tasks.collect_and_publish_metrics',
        'schedule': SCHEDULE_REPO_DAILY,
        'kwargs': {
            'metrics': {
                'kpiit.metrics.records': args(
                    name='cod_records',
                    url='http://opendata.cern.ch/api/records/'
                ),
                'kpiit.metrics.uptime': args(
                    name='web',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('COD_UPTIME_WEBSITE_API_KEY'),
                    monitor='Website',
                ),
                'kpiit.metrics.uptime': args(
                    name='search',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('COD_UPTIME_SEARCH_API_KEY'),
                    monitor='Search',
                ),
                'kpiit.metrics.uptime': args(
                    name='files',
                    url='https://api.uptimerobot.com/v2/',
                    api_key=os.getenv('COD_UPTIME_FILES_API_KEY'),
                    monitor='Files upload/download',
                ),
                'kpiit.metrics.visits': args(
                    name='cod_support'
                ),
                'kpiit.metrics.support': args(
                    name='cod_support',
                    service=Service.ZENODO
                ),
            },
            'publisher': {
                'kpiit.publishers.repo': args(Service.COD, Env.QA)
            }
        }
    },
}
#: Accept the new serializer
accept_content = ['metricjson']
#: Serialize JSON with the custom serializer
task_serializer = 'metricjson'
#: Serialize result with the custom serializer
result_serializer = 'metricjson'
