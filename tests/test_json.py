# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility function tests."""

import pytest

from kpiit.json import metric_dumps, metric_loads
from kpiit.metrics.records import RecordsMetric
from kpiit.providers.base import BaseProvider
from kpiit.publishers.base import BasePublisher
from kpiit.publishers.json import JSONFilePublisher


def test_metric_json_encode(zenodo_records):
    """Test JSON encoding of Metric."""
    zenodo_records.collect()
    json_data = metric_dumps(zenodo_records)

    metric = metric_loads(json_data)
    assert isinstance(metric, RecordsMetric)
    assert metric.records == 406804


def test_fail_metric_json_encode(zenodo_records):
    zenodo_records.records = 4

    a = BaseProvider()
    b = BasePublisher()

    with pytest.raises(TypeError):
        metric_dumps(a)
        metric_dumps(b)


def test_json_publisher():
    publisher = JSONFilePublisher('type', doi_prefix='test')
    assert publisher.name == 'test'
    publisher = JSONFilePublisher('type', service='test')
    assert publisher.name == 'test'
    publisher = JSONFilePublisher('type', asdf='test')
    assert publisher.name == 'type'
