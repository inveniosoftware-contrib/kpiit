# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""COD tests."""

import os

import pytest

from kpiit.metricsinst.cod import CODRecordsMetricInst
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_cod_records(cod_records):
    cod_records.collect()

    assert cod_records.metric.count == 4613
