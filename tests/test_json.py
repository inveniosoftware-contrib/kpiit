# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility function tests."""

import json

import pytest

from kpiit.json import MetricDecoder, MetricEncoder, metric_dumps, metric_loads
from kpiit.metrics.records import RecordsMetric
from kpiit.models import Provider, Publisher


def test_metric_json_encode(records_metric):
    """Test JSON encoding of Metric."""
    records_metric.num_records = 8
    json_data = metric_dumps(records_metric)

    expected_json = ('{"_type": "kpiit.metrics.records.RecordsMetric",'
                     ' "name": "records",'
                     ' "values": {"num_records": 8},'
                     ' "provider": null}')
    assert json_data == expected_json

    metric = metric_loads(json_data)
    assert isinstance(metric, RecordsMetric)
    assert metric.num_records == 8


def test_fail_metric_json_encode(records_metric):
    records_metric.num_records = 4

    a = Provider()
    b = Publisher()

    with pytest.raises(TypeError):
        metric_dumps(a)
        metric_dumps(b)
