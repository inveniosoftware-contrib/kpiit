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

import kpiit.metrics as metrics
from kpiit.app import app
from kpiit.metrics.records import RecordsMetric
from kpiit.metrics.uptime import UptimeMetric
from kpiit.models import Provider, Publisher
from kpiit.providers import DataCiteProvider, JSONURLProvider
from kpiit.providers.uptime_robot import UptimeRobotProvider
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
def test_provider():
    """Fixture for the test provider."""
    class TestProvider(Provider):
        def __init__(self):
            super().__init__()
            self.data = None
            self.json = None

        def collect(self):
            self.data = 'empty'
            self.values = dict(data='collected')
            self.json = {
                'hits': {
                    'total': 9
                }
            }
            return self.json
    return TestProvider()


class UptimeRequest(object):
    """Uptime request test."""

    def __init__(self, *args, **kwargs):
        """Uptime request test initialization."""
        with open('tests/data/uptime_website.json', 'r') as f:
            self.data = json.loads(f.read())

    def json(self):
        """Get JSON data."""
        return self.data


@pytest.fixture
def uptime_provider(mocker):
    """Fixture for the Uptime Robot provider."""
    mocker.patch('requests.request', new=UptimeRequest)

    return UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        'API_KEY',
        'Website'
    )


@pytest.fixture
def test_publisher():
    """Fixture for the test publisher."""
    class TestPublisher(Publisher):
        def publish(self, metrics):
            pass
    return TestPublisher()


@pytest.fixture
def records_metric(json_url_provider):
    """Fixture for records metric."""
    return RecordsMetric('records', json_url_provider, ['num_records'])


@pytest.fixture
def doi_metric(test_provider):
    """Fixture for DOI metric."""
    class TestProvider(Provider):
        def __init__(self):
            super().__init__()
            self.data = None
            self.json = None

        def collect(self):
            self.data = dict(data='collected')
            return self.data
    return metrics.DOIMetric('doi', TestProvider(), ['data'])


@pytest.fixture
def website_uptime_metric(mocker):
    """Fixture for website uptime metric."""
    mocker.patch('requests.request', new=UptimeRequest)

    return metrics.website_uptime_metric


@pytest.fixture
def search_uptime_metric(mocker):
    """Fixture for search uptime metric."""
    mocker.patch('requests.request', new=UptimeRequest)

    return metrics.search_uptime_metric


@pytest.fixture
def files_uptime_metric(mocker):
    """Fixture for files uptime metric."""
    mocker.patch('requests.request', new=UptimeRequest)

    return metrics.files_uptime_metric


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


def records_collect(data):
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
                        new=records_collect(zenodo_records_json))
    return metrics.zenodo_records_metric


@pytest.fixture
def cod_records(mocker, cod_records_json):
    """Fixture for COD records metric instance."""
    mocker.patch.object(RecordsMetric, 'collect',
                        new=records_collect(cod_records_json))
    return metrics.cod_records_metric


@pytest.fixture
def json_publisher(tmpdir):
    """Fixture for JSON publisher."""
    filename = '{}/output.json'.format(tmpdir.dirname)
    return JSONFilePublisher(filename)


@pytest.fixture(scope='module')
def celery_app(request):
    """Fixture returning the Celery app instance."""
    return app
