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


def test_metric_base(zenodo_records):
    """Test metric base class."""
    assert zenodo_records.name == 'zenodo_records'

    zenodo_records.records = 5
    assert zenodo_records.records == 5
    assert zenodo_records.value('records') == 5
    zenodo_records.records = 1
    assert zenodo_records.records == 1
    assert zenodo_records.value('records') == 1


def test_fail_metric(zenodo_records, test_provider):
    with pytest.raises(ValueError):
        Metric(name=None, provider=None, fields=None)
    with pytest.raises(ValueError):
        Metric(name='test', provider=None, fields=None)
    with pytest.raises(ValueError):
        Metric(name=None, provider=None, fields=['abc'])
    with pytest.raises(AttributeError):
        zenodo_records.update(non_existant='test')
    metric = Metric('test', test_provider, ('test'))
    with pytest.raises(NotImplementedError):
        metric.collect()


def test_metric_dynamic_attrs(zenodo_records):
    with pytest.raises(AttributeError):
        zenodo_records.records2

    zenodo_records.records = 5
    assert zenodo_records.records == 5

    zenodo_records.records = 2
    assert zenodo_records.records == 2


def test_records_metric(zenodo_records):
    zenodo_records.records = 5
    assert zenodo_records.records == 5

    zenodo_records.records = 3
    assert zenodo_records.records == 3

    assert repr(zenodo_records) == 'RecordsMetric("zenodo_records", records=3)'


def test_records_metric_collect(test_provider):
    m = RecordsMetric(
        name='records',
        provider=test_provider
    )
    assert m.provider.json is None
    assert m.records is None
    m.collect()
    assert m.provider.json is not None
    assert m.records == 9


def test_doi_metric(zenodo_doi_metric):
    zenodo_doi_metric.collect()
    assert zenodo_doi_metric.doi_failed == 17164
    assert zenodo_doi_metric.doi_success == 710383


def test_website_uptime_metric(website_uptime_metric):
    website_uptime_metric.uptime is None
    website_uptime_metric.response_time is None
    website_uptime_metric.collect()
    website_uptime_metric.uptime is None
    website_uptime_metric.response_time is not None


def test_search_uptime_metric(search_uptime_metric):
    search_uptime_metric.uptime is None
    search_uptime_metric.response_time is None
    search_uptime_metric.collect()
    search_uptime_metric.uptime is not None
    search_uptime_metric.response_time is not None


def test_files_uptime_metric(files_uptime_metric):
    files_uptime_metric.uptime is None
    files_uptime_metric.response_time is None
    files_uptime_metric.collect()
    files_uptime_metric.uptime is not None
    files_uptime_metric.response_time is not None
