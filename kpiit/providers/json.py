# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON providers."""

import requests
from celery.utils.log import get_task_logger

from kpiit.providers import BaseProvider

logger = get_task_logger(__name__)


class JSONURLProvider(BaseProvider):
    """Generic URL-based JSON provider."""

    def __init__(self, url):
        """URL provider initialization."""
        if not url:
            raise ValueError("url can't be empty")
        self.url = url
        self.data = None
        self.json = None

    def collect(self):
        """Get URL request."""
        self.data = requests.get(self.url, verify=False)
        self.json = self.data.json()
        return self.json
