# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.models import Metric


def test_metric_base(records_metric):
    """Test metric base class."""
    assert records_metric.name == 'records'

    records_metric.num_records = 5
    assert records_metric.num_records == 5
    assert records_metric.value('num_records') == 5
    records_metric.num_records = 1
    assert records_metric.num_records == 1
    assert records_metric.value('num_records') == 1


def test_fail_metric():
    with pytest.raises(ValueError):
        Metric(name=None, provider=None, fields=None)
        Metric(name='test', provider=None, fields=None)
        Metric(name=None, provider=None, fields=['abc'])


def test_metric_dynamic_attrs(records_metric):
    with pytest.raises(AttributeError):
        records_metric.num_records2

    records_metric.num_records = 5
    assert records_metric.num_records == 5

    records_metric.num_records = 2
    assert records_metric.num_records == 2


def test_records_metric(records_metric):
    records_metric.num_records = 5
    assert records_metric.num_records == 5

    records_metric.num_records = 3
    assert records_metric.num_records == 3

    assert repr(records_metric) == 'RecordsMetric("records", num_records=3)'
