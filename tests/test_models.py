# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPI model tests."""

import os

import pytest

from kpiit.models import Metric, Provider, Publisher


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
