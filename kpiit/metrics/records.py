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

    def __init__(self, name, provider, fields=['num_records']):
        """Records metric initialization."""
        super().__init__(name, provider, fields)

    def collect(self):
        """Collect data for this instance."""
        super().collect()

        num_records = self.provider.json['hits']['total']
        self.num_records = num_records
