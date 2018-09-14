# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit import Env, Service
from kpiit.publishers import doi, repo
from kpiit.publishers.base import BasePublisher
from kpiit.publishers.cern import CERNPublisher


def test_provider_base(zenodo_records):
    """Test publisher base class."""
    publisher = BasePublisher()

    with pytest.raises(NotImplementedError):
        publisher.publish([])


def test_json_publisher(json_publisher, zenodo_records):
    assert json_publisher.filename is None

    metrics = [zenodo_records]

    json_publisher.publish(metrics)
    assert json_publisher.filename is not None
    assert os.path.exists(json_publisher.filename)


def test_cern_doi_publisher_message(zenodo_doi_metric):
    publisher = doi(prefix='10.5281')

    zenodo_doi_metric.collect()

    publisher.build_message([zenodo_doi_metric])

    a = {
        "producer": "digitalrepos",
        "type": "doikpi",
        "type_prefix": "raw",
        "timestamp": 1483696735836,
        "doi_prefix": "10.5281",
        "doi_success": 710383,
        "doi_failed": 17164,
        "idb_tags": [
            "doi_prefix"
        ],
        "idb_fields": [
            "doi_success",
            "doi_failed"
        ]
    }
    b = publisher.data

    assert 'timestamp' in b

    del a['timestamp']
    del b['timestamp']

    assert a == b


def test_cern_repo_publisher_message(zenodo_records, website_uptime_metric,
                                     files_uptime_metric,
                                     search_uptime_metric,
                                     dummy_visits_metric):
    zenodo_records.collect()
    website_uptime_metric.collect()
    files_uptime_metric.collect()
    search_uptime_metric.collect()
    dummy_visits_metric.collect()

    publisher = repo(service=Service.ZENODO, env=Env.PROD)

    metrics = [
        zenodo_records, website_uptime_metric,
        search_uptime_metric, files_uptime_metric,
        dummy_visits_metric
    ]

    publisher.build_message(metrics)

    a = {
        "producer": "digitalrepos",
        "type": "repokpi",
        "type_prefix": "raw",
        "timestamp": 1483696735836,
        "service": "zenodo",
        "env": "prod",
        "records": 406804,
        "uptime_web": 99.96,
        "uptime_search": 99.96,
        "uptime_files": 99.96,
        "response_time_web": 120.10,
        "response_time_search": 120.10,
        "response_time_files": 120.10,
        "idb_tags": [
            "service",
            "env"
        ],
        "idb_fields": [
            "records",
            "uptime_web",
            "response_time_web",
            "uptime_search",
            "response_time_search",
            "uptime_files",
            "response_time_files",
        ]
    }
    b = publisher.data

    assert 'timestamp' in b

    del a['timestamp']
    del b['timestamp']

    assert a == b


def test_cern_monit_publisher(cern_monit_publisher, zenodo_records):
    """Test CERN monit publisher."""
    assert cern_monit_publisher is not None
    cern_monit_publisher.publish([zenodo_records])


def test_cern_publisher_tags():
    p = CERNPublisher('test', skip_fields=True)
    assert 'idb_fields' not in p.data
    p = CERNPublisher('test', skip_fields=False)
    assert 'idb_fields' in p.data

    tag1 = 'testtag1'
    assert len(p.data['idb_tags']) == 0

    p.add_tag(tag1, 'value')
    assert tag1 in p.data['idb_tags']
    assert tag1 in p.data and p.data[tag1] == 'value'

    p.delete_tag(tag1)
    assert len(p.data['idb_tags']) == 0


def test_cern_publisher_fields():
    p = CERNPublisher('test', skip_fields=False)
    assert 'idb_fields' in p.data

    field1 = 'testfield1'
    assert len(p.data['idb_fields']) == 0

    p.add_field(field1, 'value')
    assert field1 in p.data['idb_fields']
    assert field1 in p.data and p.data[field1] == 'value'

    p.delete_field(field1)
    assert len(p.data['idb_fields']) == 0
