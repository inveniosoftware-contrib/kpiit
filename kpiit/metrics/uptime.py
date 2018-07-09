# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records metric."""

from ..models import Metric


class UptimeMetric(Metric):
    """Metric for uptime and response time."""

    def __init__(self, name, provider, fields=['uptime', 'response_time']):
        """Uptime metric initialization."""
        super().__init__(name, provider, fields)

    def collect_done(self, data):
        """Process collected data."""
        self.uptime = data['uptime_ratio']
        self.response_time = data['response_time']
