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


def test_provider_base(records_metric):
    """Test publisher base class."""
    publisher = Publisher()

    with pytest.raises(NotImplementedError):
        publisher.publish([])


def test_json_publisher(json_publisher, records_metric):
    assert not os.path.exists(json_publisher.filename)

    metrics = [records_metric]

    json_publisher.publish(metrics)
    assert os.path.exists(json_publisher.filename)


def test_test_publisher(test_publisher):
    pass
