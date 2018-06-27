# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPI model tests."""

import os

import pytest
import requests

from kpiit.metrics.zenodo import ZenodoRecordsMetric
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_metric_base():
    """Test metric base class."""
    metric = Metric('testname')

    assert metric.name == 'testname'

    with pytest.raises(NotImplementedError):
        metric.update(5)


def test_provider_base(records_metric):
    """Test provider base class."""
    provider = Provider(records_metric)

    assert provider.metric == records_metric

    with pytest.raises(NotImplementedError):
        provider.collect()


def test_publisher_base(records_metric):
    """Test publisher base class."""
    metrics = [records_metric]

    publisher = Publisher()

    with pytest.raises(NotImplementedError):
        publisher.publish(metrics)


def test_metricinstance_base(file_provider):
    """Test metric instance base class."""
    metric_inst = MetricInstance(file_provider)

    assert metric_inst.provider == file_provider
    assert metric_inst.metric is not None


def test_zenodo_records(requests_mock, zenodo_records, zenodo_records_json):
    requests_mock.get(
        'https://zenodo.org/api/records/?all_versions',
        text=zenodo_records_json
    )
    assert zenodo_records.collect().count == 406804
