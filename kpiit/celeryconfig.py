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


def _env(key, default):
    return os.environ.get(key, default)


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
#   'collect-zenodo-repo-kpis-every-day': {
#       'task': 'kpiit.tasks.collect_and_publish_metrics',
#       'schedule': SCHEDULE_REPO_DAILY,
#       'kwargs': {
#           'metrics': {
#               'kpiit.metrics.records': args(
#                   name='zenodo_records',
#                   url='https://zenodo.org/api/records/?all_versions'
#               ),
#               'kpiit.metrics.uptime': args(
#                   name='web',
#                   url='https://api.uptimerobot.com/v2/',
#                   api_key=os.getenv('ZENODO_UPTIME_WEBSITE_API_KEY'),
#                   monitor='Website',
#               ),
#               'kpiit.metrics.uptime': args(
#                   name='search',
#                   url='https://api.uptimerobot.com/v2/',
#                   api_key=os.getenv('ZENODO_UPTIME_SEARCH_API_KEY'),
#                   monitor='Search',
#               ),
#               'kpiit.metrics.uptime': args(
#                   name='files',
#                   url='https://api.uptimerobot.com/v2/',
#                   api_key=os.getenv('ZENODO_UPTIME_FILES_API_KEY'),
#                   monitor='Files upload/download',
#               ),
#               'kpiit.metrics.visits': args(
#                   name='zenodo_support',
#                   site_id=57
#               ),
#               'kpiit.metrics.support': args(
#                   name='zenodo_support',
#                   service=Service.ZENODO
#               ),
#           },
#           'publisher': {
#               'kpiit.publishers.repo': args(Service.ZENODO, Env.QA)
#           }
#       }
#   },
#     'collect-cds-videos-repo-kpis-every-day': {
#         'task': 'kpiit.tasks.collect_and_publish_metrics',
#         'schedule': SCHEDULE_REPO_DAILY,
#         'kwargs': {
#             'metrics': {
#                 'kpiit.metrics.records': args(
#                     name='cds_videos_records',
#                     url='https://videos.cern.ch/api/records/'
#                 ),
#                 'kpiit.metrics.uptime': args(
#                     name='web',
#                     url='https://api.uptimerobot.com/v2/',
#                     api_key=os.getenv('CDS_VIDEOS_UPTIME_WEBSITE_API_KEY'),
#                     monitor='Website',
#                 ),
#                 'kpiit.metrics.uptime': args(
#                     name='search',
#                     url='https://api.uptimerobot.com/v2/',
#                     api_key=os.getenv('CDS_VIDEOS_UPTIME_SEARCH_API_KEY'),
#                     monitor='Search',
#                 ),
#                 'kpiit.metrics.uptime': args(
#                     name='files',
#                     url='https://api.uptimerobot.com/v2/',
#                     api_key=os.getenv('CDS_VIDEOS_UPTIME_FILES_API_KEY'),
#                     monitor='Files upload/download',
#                 ),
#                 'kpiit.metrics.visits': args(
#                     name='cds_videos_support'
#                 ),
#                 'kpiit.metrics.support': args(
#                     name='cds_videos_support',
#                     service=Service.ZENODO
#                 ),
#             },
#             'publisher': {
#                 'kpiit.publishers.repo': args(Service.CDS_VIDEOS, Env.QA)
#             }
#         }
#     },
#     'collect-cod-repo-kpis-every-day': {
#         'task': 'kpiit.tasks.collect_and_publish_metrics',
#         'schedule': SCHEDULE_REPO_DAILY,
#         'kwargs': {
#             'metrics': {
#                 'kpiit.metrics.records': args(
#                     name='cod_records',
#                     url='http://opendata.cern.ch/api/records/'
#                 ),
#                 'kpiit.metrics.uptime': args(
#                     name='web',
#                     url='https://api.uptimerobot.com/v2/',
#                     api_key=os.getenv('COD_UPTIME_WEBSITE_API_KEY'),
#                     monitor='Website',
#                 ),
#                 'kpiit.metrics.uptime': args(
#                     name='search',
#                     url='https://api.uptimerobot.com/v2/',
#                     api_key=os.getenv('COD_UPTIME_SEARCH_API_KEY'),
#                     monitor='Search',
#                 ),
#                 'kpiit.metrics.uptime': args(
#                     name='files',
#                     url='https://api.uptimerobot.com/v2/',
#                     api_key=os.getenv('COD_UPTIME_FILES_API_KEY'),
#                     monitor='Files upload/download',
#                 ),
#                 'kpiit.metrics.visits': args(
#                     name='cod_support'
#                 ),
#                 'kpiit.metrics.support': args(
#                     name='cod_support',
#                     service=Service.ZENODO
#                 ),
#             },
#             'publisher': {
#                 'kpiit.publishers.repo': args(Service.COD, Env.QA)
#             }
#         }
#     },
# }

#: Accept the new serializer
accept_content = [config['celery']['serializer']]
#: Serialize JSON with the custom serializer
task_serializer = config['celery']['serializer']
#: Serialize result with the custom serializer
result_serializer = config['celery']['serializer']
