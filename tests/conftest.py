# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Common pytest fixtures and plugins."""

import json
import sys

import pytest

from kpiit.metrics import *
from kpiit.metrics.records import RecordsMetric
from kpiit.providers import JSONURLProvider
from kpiit.publishers.json import JSONFilePublisher


@pytest.fixture
def json_url_provider():
    """JSON URL provider fixture."""
    return JSONURLProvider('http://opendata.cern.ch/api/records/?all_versions')


@pytest.fixture
def data_cite_provider():
    """Fixture for DataCite provider."""
    return DataCiteProvider(
        'CERN - CERN - European Organization for Nuclear Research',
        'CERN.CDS',
        ('doi_total', )
    )


@pytest.fixture
def records_metric(json_url_provider):
    """Fixture for records metric."""
    return RecordsMetric('records', json_url_provider, ['num_records'])


@pytest.fixture
def zenodo_records_json():
    """Load JSON content from Zenodo records file."""
    data = None
    with open('tests/data/zenodo_records.json', 'r') as f:
        data = f.read()
    return data


@pytest.fixture
def cod_records_json():
    """Load JSON content from COD records file."""
    data = None
    with open('tests/data/cod_records.json', 'r') as f:
        data = f.read()
    return data


def new_collect(data):
    """Mocked collect."""
    json_data = json.loads(data)

    def collect(self):
        """Test."""
        self.provider.json = json_data
        num_records = self.provider.json['hits']['total']
        self.num_records = num_records

    return collect


@pytest.fixture
def zenodo_records(mocker, zenodo_records_json):
    """Fixture for Zenodo records metric instance."""
    mocker.patch.object(RecordsMetric, 'collect',
                        new=new_collect(zenodo_records_json))
    return zenodo_records_metric


@pytest.fixture
def cod_records(mocker, cod_records_json):
    """Fixture for COD records metric instance."""
    mocker.patch.object(RecordsMetric, 'collect',
                        new=new_collect(cod_records_json))
    return cod_records_metric


@pytest.fixture
def json_publisher(tmpdir):
    """Fixture for JSON publisher."""
    filename = '{}/output.json'.format(tmpdir.dirname)
    return JSONFilePublisher(filename)
