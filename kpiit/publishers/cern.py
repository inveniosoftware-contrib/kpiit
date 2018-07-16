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
    """Abstract CERN publisher for publishing to the Grafana instance."""

    def __init__(self, type, **tags):
        """CERN publisher initialize."""
        self.data = dict(
            producer='invenio',
            type=type,
            type_prefix='raw',
            timestamp=self.get_timestamp(),
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
        del self.data[name]

    def add_field(self, name, value):
        """Add field to message."""
        if name not in self.data['idb_fields']:
            self.data['idb_fields'].append(name)
        self.data[name] = value

    def delete_field(self, name):
        """Remove field from message."""
        self.data['idb_fields'].remove(name)
        del self.data[name]

    def build_message(self, metrics):
        """Build KPI object from the given metrics."""
        for metric in metrics:
            for name, values in metric.values.items():
                for key, value in values.items():
                    self.add_field(key, value)

    def publish(self, metrics):
        """Publish KPIs to the grafana instance."""
        # TODO: Send to Grafana
        self.build_message(metrics)
        return json.dumps(self.data)

    @staticmethod
    def get_timestamp():
        """Get timestamp in milliseconds without decimals."""
        return round(datetime.utcnow().timestamp() * 1000)
