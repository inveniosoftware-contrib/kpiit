# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Support tickets metric."""

from ..models import Metric
from ..providers import DummyProvider


class SupportTicketsMetric(Metric):
    """Metric for support tickets."""

    FIELDS = ('support_requests', 'support_incidents', 'incident_stc')

    def __init__(self, provider, name='support_tickets', fields=FIELDS):
        """Support tickets metric initialization."""
        super().__init__(name, provider, fields)

    def collect_done(self, data):
        """Process collected data."""
        for key, value in data.items():
            print(key, value)
            if key == 'incident_stc':
                setattr(self, key, float(value))
            else:
                setattr(self, key, int(value))


class DummySupportTicketsMetric(SupportTicketsMetric):
    """Dummy metric for support tickets."""

    def collect_done(self, data):
        """Process collected data."""
        self.support_requests = -1
        self.support_incidents = -1
        self.incident_stc = -1.0
