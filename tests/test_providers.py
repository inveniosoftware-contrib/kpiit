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
from kpiit.providers.uptime_robot import UptimeRobotProvider


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


def test_data_cite_provider():
    """Test DataCite provider."""
    with pytest.raises(ValueError):
        DataCiteProvider(prefix=None)


def test_uptime_provider(uptime_provider):
    """Test Uptime Robot provider."""
    assert uptime_provider.url == 'https://api.uptimerobot.com/v2/'
    assert uptime_provider.api_key == 'API_KEY'

    # assert uptime_provider.uptime_ratio is None
    assert uptime_provider.response_time is None

    uptime_provider.collect()

    # assert uptime_provider.uptime_ratio is not None
    assert uptime_provider.response_time is not None


def test_fail_uptime_provider(mocker, uptime_provider):
    """Test failing Uptime Robot provider."""
    with pytest.raises(ValueError):
        assert UptimeRobotProvider(url=None, api_key=None, monitor_name=None)
    with pytest.raises(ValueError):
        assert UptimeRobotProvider(url='test', api_key=None, monitor_name=None)
    with pytest.raises(ValueError):
        assert UptimeRobotProvider(url=None, api_key='test', monitor_name=None)
    with pytest.raises(ValueError):
        assert UptimeRobotProvider(url=None, api_key=None, monitor_name='test')
    with pytest.raises(ValueError):
        assert UptimeRobotProvider(url='a', api_key='a', monitor_name=None)


def test_failed_api_uptime_provider(mocker, uptime_provider):
    """Test failing API call for Uptime Robot provider."""
    # API call failed

    def send(self, *args, **kwargs):
        return {
            'stat': 'fail'
        }

    mocker.patch.object(UptimeRobotProvider, 'send', new=send)

    with pytest.raises(ValueError):
        uptime_provider.collect()
