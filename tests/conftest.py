# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Common pytest fixtures and plugins."""

import json

import pytest

from kpiit.metrics.records import RecordsMetric
from kpiit.metricsinst.cod import CODRecordsMetricInst
from kpiit.metricsinst.zenodo import ZenodoRecordsMetricInst
from kpiit.providers import JSONURLProvider
from kpiit.publishers.json import JSONFilePublisher


@pytest.fixture
def records_metric():
    """Fixture for records metric."""
    return RecordsMetric()


@pytest.fixture
def url_provider(records_metric):
    """URL provider fixture."""
    return JSONURLProvider(records_metric, ZenodoRecordsMetricInst.URL)


@pytest.fixture
def zenodo_records_json():
    """Load JSON content from Zenodo records file."""
    data = None
    with open('tests/data/zenodo_records.json', 'r') as f:
        data = f.read()
    return data


@pytest.fixture
def zenodo_records(requests_mock, zenodo_records_json):
    """Fixture for Zenodo records metric instance."""
    requests_mock.get(
        'https://zenodo.org/api/records/?all_versions',
        text=zenodo_records_json
    )
    return ZenodoRecordsMetricInst()


@pytest.fixture
def cod_records_json():
    """Load JSON content from COD records file."""
    data = None
    with open('tests/data/cod_records.json', 'r') as f:
        data = f.read()
    return data


@pytest.fixture
def cod_records(requests_mock, cod_records_json):
    """Fixture for COD records metric instance."""
    requests_mock.get(
        'http://opendata.cern.ch/api/records/?all_versions',
        text=cod_records_json
    )
    return CODRecordsMetricInst()


@pytest.fixture
def json_publisher(tmpdir):
    """Fixture for JSON publisher."""
    filename = '{}/output.json'.format(tmpdir.dirname)
    return JSONFilePublisher(filename)
