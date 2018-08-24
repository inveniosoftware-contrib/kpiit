# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Piwik tests."""

from tests.conftest import piwik_url

from kpiit.providers.piwik import Piwik


def test_url_builder():
    url = Piwik.build_url('aaa', 'bbb')
    query = '?module=API&method=aaa.bbb&format=json'
    assert url == piwik_url(query)

    url = Piwik.build_url('aaa', 'bbb', file_format='html')
    query = '?module=API&method=aaa.bbb&format=html'
    assert url == piwik_url(query)

    url = Piwik.build_url('axa', 'bxb')
    query = '?module=API&method=axa.bxb&format=json'
    assert url == piwik_url(query)

    url = Piwik.build_url('axa', 'bxb')
    query = '?module=API&method=axa.bxb&format=json'
    assert url == piwik_url(query)

    url = Piwik.build_url('aa', 'bb', filter_limit=10)
    query = '?module=API&method=aa.bb&format=json&filter_limit=10'
    assert url == piwik_url(query)

    url = Piwik.build_url('aa', 'bb', filter_limit=10, a='b')
    query = '?module=API&a=b&method=aa.bb&format=json&filter_limit=10'
    assert url == piwik_url(query)

    url = Piwik.build_url('aa', 'bb', filter_limit=10, a='b', c='d')
    query = '?module=API&a=b&c=d&method=aa.bb&format=json&filter_limit=10'
    assert url == piwik_url(query)
