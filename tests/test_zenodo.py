# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Zenodo tests."""

import os

import pytest

from kpiit.metricsinst.zenodo import ZenodoRecordsMetricInst
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_zenodo_records(zenodo_records):
    zenodo_records.collect()

    assert zenodo_records.metric.count == 406804
