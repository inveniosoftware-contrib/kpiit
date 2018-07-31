# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility function tests."""

import pytest

from kpiit.models import Metric, Provider
from kpiit.util import load_target


def test_load_class():
    """Tests for load_class utility function."""
    assert hasattr(load_target('kpiit.util.load_target'), '__call__')

    assert load_target('kpiit.models.Metric') == Metric
    assert load_target('kpiit.models.Provider') == Provider

    with pytest.raises(ImportError):
        assert load_target('kpiit.models2.Provider') == Provider
        assert load_target('kpiit.models.NonExisting') == Provider


def test_metric_clean_value():
    assert Metric.clean_value('hello') == 'hello'
    assert Metric.clean_value('') == ''
    assert Metric.clean_value('5123123') == 5123123
    assert Metric.clean_value('3.1415926') == 3.1415926
    assert Metric.clean_value(5123123) == 5123123
    assert Metric.clean_value(3.1415926) == 3.1415926
    assert Metric.clean_value(None) == 'null'
