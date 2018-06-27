# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.metrics.zenodo import ZenodoRecordsMetric
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_metric_base():
    """Test metric base class."""
    metric = Metric('testname')

    assert metric.name == 'testname'

    with pytest.raises(NotImplementedError):
        metric.update(5)


def test_metricinstance_base(file_provider):
    """Test metric instance base class."""
    metric_inst = MetricInstance(file_provider)

    assert metric_inst.provider == file_provider
    assert metric_inst.metric is not None


def test_records_metric(records_metric):
    assert records_metric.name == 'num_records'
    assert records_metric.count is None

    records_metric.update(5)
    assert records_metric.count == 5

    records_metric.update(3)
    assert records_metric.count == 3

    assert repr(records_metric) == 'RecordsMetric("num_records", count=3)'
