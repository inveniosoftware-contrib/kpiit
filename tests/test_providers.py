# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.metrics.zenodo import ZenodoRecordsMetricInst
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_provider_base(records_metric):
    """Test provider base class."""
    provider = Provider(records_metric)

    assert provider.metric == records_metric

    with pytest.raises(NotImplementedError):
        provider.collect()
