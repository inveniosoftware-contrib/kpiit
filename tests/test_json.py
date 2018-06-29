# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility function tests."""

import json

import pytest

from kpiit.json import MetricDecoder, MetricEncoder
from kpiit.metrics.records import RecordsMetric


def test_metric_json_encode(records_metric):
    """Test JSON encoding of Metric."""
    records_metric.num_records = 8
    json_data = json.dumps(records_metric, cls=MetricEncoder)

    expected_json = ('{"_type": "kpiit.metrics.records.RecordsMetric",'
                     ' "name": "records",'
                     ' "values": {"num_records": 8},'
                     ' "provider": null}')
    assert json_data == expected_json

    metric = json.loads(json_data, cls=MetricDecoder)
    assert isinstance(metric, RecordsMetric)
    assert metric.num_records == 8
