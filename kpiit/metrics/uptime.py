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

    def __init__(self, name, provider, fields=None):
        """Uptime metric initialization."""
        super().__init__(name, provider, fields or [
            'uptime_{}'.format(name),
            'response_time_{}'.format(name)
        ])

    def collect_done(self, data):
        """Process collected data."""
        up = data['uptime_ratio']
        resp = data['response_time']
        uptime = float(up) if up is not None else None
        response_time = float(resp) if resp is not None else None
        setattr(self, self.fields[0], uptime)
        setattr(self, self.fields[1], response_time)
