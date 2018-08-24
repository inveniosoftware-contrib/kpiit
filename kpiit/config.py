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
from celery.utils.log import get_task_logger

from kpiit.util import args

logger = get_task_logger(__name__)


class Config(configobj.ConfigObj):
    """Config file."""

    def __init__(self, filename, environment):
        """Initialize config file."""
        super().__init__(filename, interpolation='Template', file_error=True)

        try:
            env_filename = self._env_filename(filename, environment)
            self._merge_environment_config(env_filename)
        except (configobj.ConfigObjError, IOError) as e:
            logger.exception('Failed to load environment config: {}'.format(
                env_filename
            ))

        self['environment'] = environment

        # Load secrets from OpenShift into config structure
        self['providers']['snow']['user'] = os.getenv('SNOW_USER')
        self['providers']['snow']['pass'] = os.getenv('SNOW_PASS')

    def _merge_environment_config(self, filename):
        """Merge the main config file with the env config file ConfigObj."""
        env_cfg = configobj.ConfigObj(filename, file_error=True)
        self.merge(env_cfg)

    @property
    def closed_task_states(self):
        """Get the IDs of the task states that are defined as "closed"."""
        names = self['providers']['snow']['closed_task_states']
        states = self['providers']['snow']['states']

        return [states[name] for name in names]

    @property
    def beat_schedule(self):
        """Get the tasks in celeryconfig beat schedule format."""
        tasks = {}
        cfg = self['celery'].dict()

        for name, data in cfg['tasks'].items():
            metrics = self._parse_instances(cfg, data['metrics'], 'metrics')
            publishers = self._parse_instances(
                cfg,
                data['publishers'],
                'publishers'
            )
            tasks[name] = {
                'task': data['task'],
                'schedule': crontab(**cfg['schedules'][data['schedule']]),
                'kwargs': {
                    'metrics': metrics,
                    'publishers': publishers
                }
            }

        return tasks

    @classmethod
    def _env_filename(cls, filename, environment):
        """Get environment config filename from a filename."""
        filename_split = filename.split('.')
        return '{}.{}.cfg'.format('.'.join(filename_split[:-1]), environment)

    @classmethod
    def _parse_instances(cls, cfg, names, instance_type):
        """Parse instances config values into celeryconfig format."""
        if isinstance(names, str):
            names = [names]
        tasks = [cfg[instance_type][name] for name in names]

        instances = {}
        for task in tasks:
            kwargs = task.copy()
            del kwargs['instance']
            instances[task['instance']] = args(**kwargs)
        return instances


environment = os.getenv('KPIIT_ENV', 'development')

config_path = os.path.join(os.path.dirname(__file__), 'config.cfg')
config = Config(config_path, environment)
