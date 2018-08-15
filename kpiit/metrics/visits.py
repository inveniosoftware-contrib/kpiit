# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Visits metric."""

from ..models import Metric


class VisitsMetric(Metric):
    """Metric for number of visits."""

    FIELDS = ['visits', 'visits_unique']

    def __init__(self, name, provider, fields=FIELDS):
        """Visits metric initialization."""
        super().__init__(name, provider, fields)

    def collect_done(self, data):
        """Process collected data."""
        for key, value in data.items():
            setattr(self, key, self.clean_value(value))
