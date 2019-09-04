# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Common pytest fixtures and plugins."""

import json
import os.path
from os.path import join as join_path

import pytest
from celery.utils.log import get_task_logger

import kpiit.metrics as metrics
from kpiit.app import app
from kpiit.config import config
from kpiit.metrics.records import RecordsMetric
from kpiit.providers import BaseProvider
from kpiit.providers.datacite import DataCiteProvider
from kpiit.providers.json import JSONURLProvider
from kpiit.providers.piwik import BASE_URL
from kpiit.providers.snow import ServiceNowProvider
from kpiit.providers.uptime_robot import UptimeRobotProvider
from kpiit.publishers import doi as pub_doi
from kpiit.publishers.base import BasePublisher
from kpiit.publishers.cern import CERNMonitPublisher

logger = get_task_logger(__name__)


TEST_DIR = os.path.dirname(__file__)


@pytest.fixture
def json_url_provider():
    """JSON URL provider fixture."""
    return JSONURLProvider('http://opendata.cern.ch/api/records/?all_versions')


@pytest.fixture
def test_provider():
    """Fixture for the test provider."""
    class TestProvider(BaseProvider):
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
        with open(join_path(TEST_DIR, 'data/uptime_website.json'), 'r') as f:
            self.data = json.loads(f.read())

    def json(self):
        """Get JSON data."""
        return self.data

    def raise_for_status(self):
        """Mocked method."""
        return


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
    class TestPublisher(BasePublisher):
        def publish(self, metrics):
            pass
    return TestPublisher()


def uptime_collect(self):
    """Static collected uptime data for testing."""
    return {
        'response_time': 120.10,
        'uptime_ratio': 99.96
    }


@pytest.fixture
def dummy_visits_metric():
    """Fixture for dummy visits metric."""
    return metrics.visits('dummy_visits', dummy=True)


@pytest.fixture
def website_uptime_metric(mocker):
    """Fixture for website uptime metric."""
    mocker.patch.object(UptimeRobotProvider, 'collect', new=uptime_collect)

    return metrics.uptime('web', 'http://www.google.com', 'abc', 'Website')


@pytest.fixture
def search_uptime_metric(mocker):
    """Fixture for search uptime metric."""
    mocker.patch.object(UptimeRobotProvider, 'collect', new=uptime_collect)

    return metrics.uptime('search', 'http://www.google.com', 'abc', 'Search')


@pytest.fixture
def files_uptime_metric(mocker):
    """Fixture for files uptime metric."""
    mocker.patch.object(UptimeRobotProvider, 'collect', new=uptime_collect)

    return metrics.uptime(
        'files', 'http://www.google.com', 'abc', 'Files upload/download'
    )


@pytest.fixture
def zenodo_records_json():
    """Load JSON content from Zenodo records file."""
    data = None
    with open(join_path(TEST_DIR, 'data/zenodo_records.json'), 'r') as f:
        data = f.read()
    return data


@pytest.fixture
def cod_records_json():
    """Load JSON content from COD records file."""
    data = None
    with open(join_path(TEST_DIR, 'data/cod_records.json'), 'r') as f:
        data = f.read()
    return data


@pytest.fixture
def zenodo_doi_index_html():
    """Load HTML content for Zenodo DataCite index page."""
    data = None
    with open(join_path(TEST_DIR, 'data/datacite_doi_index.html'), 'r') as f:
        data = f.read()
    return data


@pytest.fixture
def zenodo_doi_june_html():
    """Load HTML content for Zenodo DataCite stats page for June 2018."""
    data = None
    with open(join_path(TEST_DIR, 'data/datacite_doi_2018-06.html'), 'r') as f:
        data = f.read()
    return data


def records_collect(data):
    """Mocked collect."""
    json_data = json.loads(data)

    def collect(self):
        """Test."""
        self.provider.json = json_data
        num_records = self.provider.json['hits']['total']
        self.records = num_records

    return collect


@pytest.fixture
def zenodo_records(mocker, zenodo_records_json):
    """Fixture for Zenodo records metric instance."""
    mocker.patch.object(RecordsMetric, 'collect',
                        new=records_collect(zenodo_records_json))
    return metrics.records('zenodo_records', 'http://www.google.com')


@pytest.fixture
def cod_records(mocker, cod_records_json):
    """Fixture for COD records metric instance."""
    mocker.patch.object(RecordsMetric, 'collect',
                        new=records_collect(cod_records_json))
    return metrics.records('cod_records', 'http://www.google.com')


@pytest.fixture
def zenodo_doi_metric(mocker, zenodo_doi_index_html, zenodo_doi_june_html):
    """Fixture for COD records metric instance."""
    prefix = '10.5281'

    def load_index_data(self, url):
        return zenodo_doi_index_html

    def load_stats_data(self, url):
        return zenodo_doi_june_html

    mocker.patch.object(DataCiteProvider, 'load_index_data',
                        new=load_index_data)
    mocker.patch.object(DataCiteProvider, 'load_stats_data',
                        new=load_stats_data)
    return metrics.doi(prefix=prefix)


@pytest.fixture
def json_publisher(tmpdir):
    """Fixture for JSON publisher."""
    return pub_doi('10.5281', save_json=True)


@pytest.fixture(scope='module')
def celery_app(request):
    """Fixture returning the Celery app instance."""
    return app


@pytest.fixture
def zenodo_support_ticket_metric(mocker):
    """Fixture for Zenodo support tickets metric."""
    def auth_get(cls, url, user='user', password='pass'):
        if '_avg_' in url and 'incident' in url:
            return dict(result=dict(stats=dict(avg=dict(calendar_stc='10'))))
        else:
            return dict(
                result=dict(
                    stats=dict(
                        count='100',
                        max=dict(u_reassignment_counter_fe='20')
                    )
                )
            )

    mocker.patch.object(ServiceNowProvider, 'auth_get', new=auth_get)

    return metrics.support('zenodo_support', config['zenodo_service'])


@pytest.fixture
def dummy_support_ticket_metric(mocker):
    """Fixture for dummy support ticket metric."""
    return metrics.support('dummy_support', dummy=True)


@pytest.fixture
def cern_monit_publisher(mocker):
    """Fixture for the CERN monit publisher."""
    def new_send(cls, url, document):
        logger.debug('doc', document)

    mocker.patch.object(BasePublisher, 'send', new=new_send)
    return CERNMonitPublisher('testkpi')


def piwik_url(query):
    """Get the full URL for the Piwik query."""
    return BASE_URL + '/index.php' + query
