# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Config file handler."""

import os.path

import configobj

from celery.schedules import crontab

from kpiit.util import args


class Config(configobj.ConfigObj):
    """Config file."""

    def __init__(self, filename):
        """Initialize config file."""
        super().__init__(filename, interpolation='Template', file_error=True)

    @property
    def beat_schedule(self):
        """Get the tasks in celeryconfig beat schedule format."""
        tasks = {}

        for name, data in self['tasks'].items():
            schedule = self['schedules'][data['schedule']]

            metrics, publishers = {}, {}

            if isinstance(data['metrics'], str):
                metrics[data['metrics']] = self['metrics'][data['metrics']]
            else:
                for name in data['metrics']:
                    metrics[name] = self['metrics'][name]

            if isinstance(data['publishers'], str):
                publishers[data['publishers']] = \
                    self['publishers'][data['publishers']]
            else:
                for name in data['publishers']:
                    publishers[name] = self['publishers'][name]

            tasks[name] = {
                'task': data['task'],
                'schedule': crontab(**schedule),
                'kwargs': {
                    'metrics': self._parse_instances(metrics),
                    'publishers': self._parse_instances(publishers)
                }
            }

        return tasks

    @classmethod
    def _parse_instances(cls, data):
        """Parse instances config values into celeryconfig format."""
        instances = {}
        for name, values in data.items():
            kwargs = values.copy()
            del kwargs['instance']
            instances[values['instance']] = args(**kwargs)
        return instances
