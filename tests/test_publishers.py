# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.models import Publisher
from kpiit.publishers.cern import CERNPublisher


def test_provider_base(zenodo_records):
    """Test publisher base class."""
    publisher = Publisher()

    with pytest.raises(NotImplementedError):
        publisher.publish([])


def test_json_publisher(json_publisher, zenodo_records):
    assert not os.path.exists(json_publisher.filename)

    metrics = [zenodo_records]

    json_publisher.publish(metrics)
    assert os.path.exists(json_publisher.filename)


def test_cern_doi_publisher_message(zenodo_doi_metric):
    publisher = CERNPublisher.create_doi(prefix='10.5281')

    publisher.build_message([zenodo_doi_metric])

    a = {
        "producer": "invenio",
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

    assert a['producer'] == b['producer']
