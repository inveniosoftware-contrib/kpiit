# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility function tests."""

import pytest

from kpiit.metrics.base import BaseMetric
from kpiit.providers import BaseProvider
from kpiit.util import load_target


def test_load_class():
    """Tests for load_class utility function."""
    assert hasattr(load_target('kpiit.util.load_target'), '__call__')

    assert load_target('kpiit.metrics.base.BaseMetric') == BaseMetric
    assert load_target('kpiit.providers.BaseProvider') == BaseProvider

    with pytest.raises(ImportError):
        assert load_target('kpiit.models2.Provider') == BaseProvider
    with pytest.raises(AttributeError):
        assert load_target('kpiit.metrics.base.NonExisting') == BaseProvider


def test_metric_clean_value():
    assert BaseMetric.clean_value('hello') == 'hello'
    assert BaseMetric.clean_value('') == ''
    assert BaseMetric.clean_value('5123123') == 5123123
    assert BaseMetric.clean_value('3.1415926') == 3.1415926
    assert BaseMetric.clean_value(5123123) == 5123123
    assert BaseMetric.clean_value(3.1415926) == 3.1415926
    assert BaseMetric.clean_value(None) is None
