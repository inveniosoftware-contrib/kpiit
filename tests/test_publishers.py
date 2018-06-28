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


def test_publisher_base(records_metric):
    """Test publisher base class."""
    metrics = [records_metric]

    publisher = Publisher()

    with pytest.raises(NotImplementedError):
        publisher.publish(metrics)


def test_json_publisher(json_publisher, records_metric):
    assert not os.path.exists(json_publisher.filename)

    metrics = [records_metric.values]

    json_publisher.publish(metrics)
    assert os.path.exists(json_publisher.filename)
