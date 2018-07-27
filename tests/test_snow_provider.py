# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest

from kpiit import Service
from kpiit.providers.snow import *


def test_simple_queries():
    base = '/api/now/v2/table/incident?sysparm_query='
    q1 = ServiceNowQuery('incident').where(test='hello')
    assert str(q1) == base + 'test=hello'

    q1.and_(bool_test=True)
    assert str(q1) == base + 'test=hello^bool_test=true'

    q1.or_(hello='world', or_this=False)
    assert str(q1) == base + \
        'test=hello^bool_test=true^ORhello=world^ORor_this=false'


def test_restart_where_clause_queries():
    base = '/api/now/v2/table/incident?sysparm_query='
    q1 = ServiceNowQuery('incident').where(test='hello').and_(a='b')
    assert str(q1) == base + 'test=hello^a=b'

    q1.where(hello='world')
    assert str(q1) == base + 'hello=world'

    q1.and_(a='b')
    assert str(q1) == base + 'hello=world^a=b'


def test_limits():
    base = '/api/now/v2/table/incident?sysparm_query='
    q1 = ServiceNowQuery('incident').where(test='hello').limit(5)
    assert str(q1) == base + 'test=hello&sysparm_limit=5'

    q1.limit(10)
    assert str(q1) == base + 'test=hello&sysparm_limit=10'

    assert q1.url == INSTANCE_URLS['test'] + base + \
        'test=hello&sysparm_limit=10'


def test_count():
    base_old = '/api/now/v2/table/incident?sysparm_query='
    base = '/api/now/v1/stats/incident?sysparm_query='

    q1 = ServiceNowQuery('incident').where(test='hello').count()
    assert str(q1) == base + 'test=hello&sysparm_count=true'

    q1.limit(20)
    assert str(q1) == base + 'test=hello&sysparm_count=true&sysparm_limit=20'

    assert q1.url == INSTANCE_URLS['test'] + base + \
        'test=hello&sysparm_count=true&sysparm_limit=20'


def test_orderby():
    base = '/api/now/v2/table/incident?sysparm_query='

    q1 = ServiceNowQuery('incident').where(test='hello').limit(12)
    assert str(q1) == base + 'test=hello&sysparm_limit=12'

    q1.orderby('field1')
    assert str(q1) == base + \
        'test=hello&sysparm_limit=12&sysparm_orderby=field1'

    q1.orderby('field2', desc=True)
    assert str(q1) == base + \
        'test=hello&sysparm_limit=12&sysparm_orderby=field2^DESC'

    assert q1.url == INSTANCE_URLS['test'] + base + \
        'test=hello&sysparm_limit=12&sysparm_orderby=field2^DESC'
