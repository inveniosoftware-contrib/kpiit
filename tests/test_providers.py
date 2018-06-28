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


def test_provider_base(records_metric):
    """Test provider base class."""
    provider = Provider()

    with pytest.raises(NotImplementedError):
        provider.collect()


def test_json_url_provider(records_metric):
    """Test JSON URL provider."""
    # TODO: add tess for json url provider
    pass
