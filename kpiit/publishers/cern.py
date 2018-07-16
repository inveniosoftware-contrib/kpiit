# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Publisher for CERN's Grafana instance."""

import json
from datetime import datetime

from ..metrics.doi import DOIMetric
from ..models import Publisher


class CERNPublisher(Publisher):
    """Publish metrics to CERN's Grafana instance."""

    def __init__(self, type, **tags):
        """CERN publisher initialize."""
        self.data = dict(
            producer='invenio',
            type=type,
            type_prefix='raw',
            timestamp=None,
            idb_tags=[],
            idb_fields=[]
        )

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
        if name not in self.data['idb_fields']:
            self.data['idb_fields'].append(name)
        self.data[name] = value

    def delete_field(self, name):
        """Remove field from message."""
        self.data['idb_fields'].remove(name)
        if name in self.data:
            del self.data[name]

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

        # TODO: Send data to CERN

    @staticmethod
    def get_timestamp():
        """Get timestamp in milliseconds without decimals."""
        return round(datetime.utcnow().timestamp() * 1000)

    @classmethod
    def create_doi(cls, prefix):
        """Create a DOI publisher."""
        return CERNPublisher('doikpi', doi_prefix=prefix)

    @classmethod
    def create_repo(cls, service, env):
        """Create a repo publisher."""
        return CERNPublisher('repokpi', service=service, env=env)
