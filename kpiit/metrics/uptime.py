# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records metric."""

from kpiit.metrics.base import BaseMetric


class UptimeMetric(BaseMetric):
    """Metric for uptime and response time."""

    def __init__(self, name, provider, fields=None):
        """Uptime metric initialization."""
        super().__init__(name, provider, [
            'uptime_{}'.format(name),
            'response_time_{}'.format(name)
        ])

    def collect_done(self, data):
        """Process collected data."""
        setattr(self, self.fields[0], self.clean_value(data['uptime_ratio']))
        setattr(self, self.fields[1], self.clean_value(data['response_time']))
