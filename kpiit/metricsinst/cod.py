# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""MetricInstances for COD."""

from ..metrics.records import RecordsMetric
from ..metricsinst.records import RecordsMetricInst
from ..providers import JSONURLProvider


class CODRecordsMetricInst(RecordsMetricInst):
    """Metric instance for # of records from COD."""

    URL = 'http://opendata.cern.ch/api/records/?all_versions'

    def __init__(self):
        """Number of records metric for COD initialization."""
        provider = JSONURLProvider(RecordsMetric('cod_record'), self.URL)
        super().__init__(provider)
