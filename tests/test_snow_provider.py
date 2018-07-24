# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit.providers.snow import ServiceNowQuery


def test_simple_queries():
    base = '/api/now/v2/table/incident?sysparm_query='
    q1 = ServiceNowQuery('incident').where(test='hello')
    assert str(q1) == base + 'test=hello'

    q1.and_(bool_test=True)
    assert str(q1) == base + 'test=hello^bool_test=true'

    q1.or_(hello='world', or_this=False)
    assert str(q1) == base + \
        'test=hello^bool_test=true^ORhello=world^ORor_this=false'
