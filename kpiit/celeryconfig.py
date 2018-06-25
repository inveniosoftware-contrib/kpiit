# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration for KPIit."""

import os


def _env(key, default):
    return os.environ.get(key, default)


#: URL of message broker for Celery (default is Redis).
broker_url = _env('BROKER_URL', 'redis://localhost:6379/0')
#: URL of backend for result storage (default is Redis).
result_backend = _env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
#: List of modules to import when the Celery worker starts.
imports = _env('CELERY_IMPORTS', ['kpiit.tasks'])
#: Scheduled tasks configuration (aka cronjobs).
beat_schedule = _env('CELERYBEAT_SCHEDULE', {
    'get-records-every-???': {
        'task': 'kpiit.tasks.num_records',
        'schedule': 3600.0,
        'args': ()
    }
})
