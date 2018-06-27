# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""MetricInstances for records."""

from ..models import MetricInstance


class RecordsMetricInst(MetricInstance):
    """Metric instance for # of records from Zenodo."""

    def __init__(self, provider):
        """Number of records metric for Zenodo initialization."""
        super().__init__(provider)

    def collect(self):
        """Collect data for this instance."""
        super().collect()

        self.metric.count = self.provider.json['hits']['total']
