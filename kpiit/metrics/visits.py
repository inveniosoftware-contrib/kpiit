# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Visits metric."""

from ..models import Metric
from ..providers import DummyProvider


class VisitsMetric(Metric):
    """Metric for number of visits."""

    def __init__(self, provider, name='visits',
                 fields=['visits', 'visits_unique']):
        """Visits metric initialization."""
        super().__init__(name, provider, fields)

    def collect_done(self, data):
        """Process collected data."""
        raise NotImplementedError()


class DummyVisitsMetric(Metric):
    """Dummy metric with fixed data."""

    def __init__(self, provider=DummyProvider(), name='visits',
                 fields=['visits', 'visits_unique']):
        """Visits metric initialization."""
        super().__init__(name, provider, fields)
        self.visits = None
        self.visits_unique = None

    def collect_done(self, data):
        """Process collected data."""
        pass
