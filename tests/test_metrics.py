# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest


def test_metric_base(records_metric):
    """Test metric base class."""
    assert records_metric.name == 'records'

    records_metric.update(test=5)
    assert records_metric.values[records_metric.name]['test'] == 5
    records_metric.update(test=1)
    assert records_metric.values[records_metric.name]['test'] == 1


def test_records_metric(records_metric):
    records_metric.update(num_records=5)
    assert records_metric.values['records']['num_records'] == 5

    records_metric.update(num_records=3)
    assert records_metric.values['records']['num_records'] == 3

    assert repr(records_metric) == 'RecordsMetric("records", num_records=3)'
