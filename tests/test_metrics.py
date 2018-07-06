# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.metrics.records import RecordsMetric
from kpiit.models import Metric


def test_metric_base(records_metric):
    """Test metric base class."""
    assert records_metric.name == 'records'

    records_metric.num_records = 5
    assert records_metric.num_records == 5
    assert records_metric.value('num_records') == 5
    records_metric.num_records = 1
    assert records_metric.num_records == 1
    assert records_metric.value('num_records') == 1


def test_fail_metric(records_metric):
    with pytest.raises(ValueError):
        Metric(name=None, provider=None, fields=None)
    with pytest.raises(ValueError):
        Metric(name='test', provider=None, fields=None)
    with pytest.raises(ValueError):
        Metric(name=None, provider=None, fields=['abc'])
    with pytest.raises(AttributeError):
        records_metric.update(non_existant='test')


def test_metric_dynamic_attrs(records_metric):
    with pytest.raises(AttributeError):
        records_metric.num_records2

    records_metric.num_records = 5
    assert records_metric.num_records == 5

    records_metric.num_records = 2
    assert records_metric.num_records == 2


def test_records_metric(records_metric):
    records_metric.num_records = 5
    assert records_metric.num_records == 5

    records_metric.num_records = 3
    assert records_metric.num_records == 3

    assert repr(records_metric) == 'RecordsMetric("records", num_records=3)'


def test_records_metric_collect(test_provider):
    m = RecordsMetric(
        name='records',
        provider=test_provider
    )
    assert m.provider.json is None
    assert m.num_records is None
    m.collect()
    assert m.provider.json is not None
    assert m.num_records == 9


def test_doi_metric(doi_metric):
    assert doi_metric.data is None
    doi_metric.collect()
    assert doi_metric.data == 'collected'


def test_website_uptime_metric(website_uptime_metric):
    website_uptime_metric.uptime is None
    website_uptime_metric.response_time is None
    website_uptime_metric.collect()
    website_uptime_metric.uptime is None
    website_uptime_metric.response_time is not None


def test_search_uptime_metric(search_uptime_metric):
    pass


def test_files_uptime_metric(files_uptime_metric):
    pass
