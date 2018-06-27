# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.metrics.zenodo import ZenodoRecordsMetricInst
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_publisher_base(records_metric):
    """Test publisher base class."""
    metrics = [records_metric]

    publisher = Publisher()

    with pytest.raises(NotImplementedError):
        publisher.publish(metrics)
