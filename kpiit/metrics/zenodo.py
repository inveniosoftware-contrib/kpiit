# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""MetricInstances for Zenodo."""

from ..models import MetricInstance
from ..providers.records import RecordsURLProvider


class ZenodoRecordsMetric(MetricInstance):
    """Metric instance for # of records from Zenodo."""

    URL = 'https://zenodo.org/api/records/?all_versions'

    def __init__(self, provider=RecordsURLProvider(URL)):
        """Number of records metric for Zenodo initialization."""
        super().__init__(provider)
