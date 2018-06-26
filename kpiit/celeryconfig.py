# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration for KPIit."""

import os

from celery.schedules import crontab


def _env(key, default):
    return os.environ.get(key, default)


#: URL of message broker for Celery (default is Redis).
broker_url = _env('BROKER_URL', 'redis://localhost:6379/0')
#: URL of backend for result storage (default is Redis).
result_backend = _env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
#: List of modules to import when the Celery worker starts.
imports = _env('CELERY_IMPORTS', ['kpiit.tasks'])
#: Scheduled tasks configuration (aka cronjobs).
beat_schedule = {
    'collect-kpi-every-day-after-midnight': {
        'task': 'kpiit.tasks.collect_kpi',
        # 'schedule': crontab(hour=0, minute=20),
        'schedule': 10.0,
        'args': ()
    }
}
