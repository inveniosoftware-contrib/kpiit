# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.models import Provider
from kpiit.providers import DataCiteProvider, JSONURLProvider


def test_provider_base(records_metric):
    """Test provider base class."""
    provider = Provider()

    with pytest.raises(NotImplementedError):
        provider.collect()


def test_json_url_provider(json_url_provider, records_metric):
    """Test JSON URL provider."""
    with pytest.raises(ValueError):
        JSONURLProvider(url=None)

    # TODO: Test JSON content
    assert json_url_provider.json is None
    json_url_provider.collect()
    assert json_url_provider.json is not None


def test_data_cite_provider(data_cite_provider):
    """Test DataCite provider."""
    with pytest.raises(ValueError):
        DataCiteProvider(allocator=None, name='test')
    with pytest.raises(ValueError):
        DataCiteProvider(allocator='alloc', name=None)

    # TODO: Validate DataCite content
    assert data_cite_provider.values is None
    data_cite_provider.collect()
    assert data_cite_provider.values is not None
