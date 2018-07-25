# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Publisher for CERN's Grafana instance."""

import json
from datetime import datetime

from celery.utils.log import get_task_logger

from ..metrics.doi import DOIMetric
from ..models import Publisher
from ..send_check import send

logger = get_task_logger(__name__)


class CERNPublisher(Publisher):
    """Publish metrics to CERN's Grafana instance."""

    def __init__(self, type, skip_fields=False, save_json=True, **tags):
        """CERN publisher initialize."""
        self.data = dict(
            producer='digitalrepos',
            type=type,
            type_prefix='raw',
            timestamp=None,
            idb_tags=[]
        )

        if not skip_fields:
            self.data['idb_fields'] = []

        self.save_json = save_json
        self.filename = None
        if save_json:
            if 'doi_prefix' in tags:
                self.name = tags['doi_prefix']
            elif 'service' in tags:
                self.name = tags['service']
            else:
                self.name = type

        # Add tags
        for key, value in tags.items():
            self.add_tag(key, value)

    def add_tag(self, name, value):
        """Add tag to message."""
        if name not in self.data['idb_tags']:
            self.data['idb_tags'].append(name)
        self.data[name] = value

    def delete_tag(self, name):
        """Remove tag from message."""
        self.data['idb_tags'].remove(name)
        if name in self.data:
            del self.data[name]

    def add_field(self, name, value):
        """Add field to message."""
        if 'idb_fields' in self.data and name not in self.data['idb_fields']:
            self.data['idb_fields'].append(name)
        self.data[name] = value

    def delete_field(self, name):
        """Remove field from message."""
        if 'idb_fields' in self.data:
            self.data['idb_fields'].remove(name)
        if name in self.data:
            del self.data[name]

    def save(self, format='json'):
        """Save data to file."""
        if format == 'json':
            encoded = json.dumps(self.data)
        else:
            raise NotImplementedError('format "%s" is not supported' % format)

        self.filename = 'logs/{type}_{name}_{now}.{format}'.format(
            type=self.data['type'],
            name=self.name,
            now=self.get_timestamp(),
            format=format
        )

        with open(self.filename, 'w+') as f:
            f.write(encoded)
            logger.info('saved output to: {}'.format(self.filename))

    def build_message(self, metrics):
        """Build KPI object from the given metrics."""
        for metric in metrics:
            for name, values in metric.values.items():
                for key, value in values.items():
                    self.add_field(key, value)

    def publish(self, metrics):
        """Publish KPIs to the grafana instance."""
        super().publish(metrics)
        self.data['timestamp'] = self.get_timestamp()

        if self.save_json:
            self.save(format='json')

    @staticmethod
    def get_timestamp():
        """Get timestamp in milliseconds without decimals."""
        return round(datetime.utcnow().timestamp() * 1000)

    @classmethod
    def create_doi(cls, prefix, skip_fields=False, save_json=True):
        """Create a DOI publisher."""
        return cls('doikpi', doi_prefix=prefix, skip_fields=skip_fields)

    @classmethod
    def create_repo(cls, service, env, skip_fields=False, save_json=True):
        """Create a repo publisher."""
        return cls(
            'repokpi',
            service=service.value,
            env=env.value,
            skip_fields=skip_fields
        )


class CERNMonitPublisher(CERNPublisher):
    """Publish JSON data to CERN's monit service."""

    def publish(self, metrics):
        """Publish KPIs to the grafana instance."""
        super().publish(metrics)

        resp = send([self.data], production=True)
        logger.debug('Response: %s' % resp)
