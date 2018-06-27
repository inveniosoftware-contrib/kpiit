# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.metricsinst.zenodo import ZenodoRecordsMetricInst
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_metric_base():
    """Test metric base class."""
    metric = Metric('testname')

    assert metric.name == 'testname'

    metric.update(test=5)
    assert metric.values['test'] == 5
    metric.update(test=1)
    assert metric.values['test'] == 1


def test_metricinstance_base(url_provider):
    """Test metric instance base class."""
    metric_inst = MetricInstance(url_provider)

    assert metric_inst.provider == url_provider
    assert metric_inst.metric is not None


def test_records_metric(records_metric):
    assert records_metric.name == 'records'
    assert records_metric.count is None

    records_metric.count = 5
    assert records_metric.count == 5

    records_metric.count = 3
    assert records_metric.count == 3

    assert repr(records_metric) == 'RecordsMetric("records", num_records=3)'
