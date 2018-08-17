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
    def tasks(self):
        """Get the tasks in celeryconfig format."""
        tasks = {}

        for task_name, values in self['tasks'].items():
            schedule = self['schedules'][values['schedule']]

            metrics = self._parse_instances(values['metrics'])
            publishers = self._parse_instances(values['publishers'])

            tasks[task_name] = {
                'task': values['task'],
                'schedule': crontab(**schedule),
                'kwargs': {
                    'metrics': metrics,
                    'publishers': publishers
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
