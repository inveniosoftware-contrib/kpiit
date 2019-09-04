# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Uptime Robot provider."""

import os.path
import time
from datetime import datetime

import requests
from celery.utils.log import get_task_logger

from kpiit.providers import BaseProvider

logger = get_task_logger(__name__)


class UptimeRobotProvider(BaseProvider):
    """Uptime Robot provider."""

    def __init__(self, url, api_key, monitor_name):
        """Uptime Robot provider initialization."""
        if not url:
            raise ValueError("url can't be empty")
        if not monitor_name:
            raise ValueError("monitor_name can't be empty")

        self.url = url
        self.api_key = api_key
        self.monitor_name = monitor_name
        self.uptime_ratio = None
        self.response_time = None

    def collect(self):
        """Get data from Uptime Robot."""
        if not self.api_key:
            # Send dummy values if no API key is specified
            logger.warning(
                'no API key specified for Uptime provider: {}'.format(
                    self.monitor_name
                )
            )
            return {
                'response_time': None,
                'uptime_ratio': None
            }

        params = dict(
            all_time_uptime_ratio=1,
            response_times=1
        )
        resp = self.send('getMonitors', **params)
        if resp['stat'] == 'fail':
            raise ValueError('failed to download monitor data')
        return self._update_data(resp)

    def _update_data(self, resp):
        """Update uptime and response time attributes."""
        for monitor in resp['monitors']:
            name = monitor['friendly_name']
            if name == self.monitor_name:
                self.uptime_ratio = monitor['all_time_uptime_ratio']
                self.response_time = monitor['average_response_time']
                break
        return {
            'response_time': self.response_time,
            'uptime_ratio': self.uptime_ratio
        }

    def send(self, action, **kwargs):
        """Send request to UptimeRobot API and return the JSON object."""
        url = os.path.join(self.url, action)
        kwargs['api_key'] = self.api_key
        if 'format' not in kwargs:
            kwargs['format'] = 'json'
        if 'logs' not in kwargs:
            kwargs['logs'] = 1
        pairs = ['{}={}'.format(*item) for item in kwargs.items()]
        payload = '&'.join(pairs)
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'cache-control': 'no-cache'
        }
        resp = requests.request(
            'POST',
            url,
            data=payload,
            headers=headers
        )
        resp.raise_for_status()
        return resp.json()
