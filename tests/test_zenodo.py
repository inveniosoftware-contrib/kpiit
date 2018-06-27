# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.metrics.zenodo import ZenodoRecordsMetric
from kpiit.models import Metric, MetricInstance, Provider, Publisher


def test_zenodo_records(requests_mock, zenodo_records, zenodo_records_json):
    requests_mock.get(
        'https://zenodo.org/api/records/?all_versions',
        text=zenodo_records_json
    )
    assert zenodo_records.collect().count == 406804
