# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records metric."""

from ..models import Metric


class RecordsMetric(Metric):
    """Metric for number of records."""

    def __init__(self, name, provider):
        """Records metric initialization."""
        super().__init__(name, provider, ['records'])

    def collect_done(self, data):
        """Process collected data."""
        num_records = data['hits']['total']
        self.records = num_records
