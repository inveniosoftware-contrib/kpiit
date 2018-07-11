# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Generic providers."""

import re

import json
import requests
import urllib

from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from ..app import app
from ..models import Provider
from ..util import load_target

logger = get_task_logger(__name__)


class JSONURLProvider(Provider):
    """Basic URL-based provider."""

    def __init__(self, url):
        """URL provider initialization."""
        if not url:
            raise ValueError("url can't be empty")
        self.url = url
        self.data = None
        self.json = None

    def collect(self):
        """Get URL request."""
        self.data = requests.get(self.url)
        self.json = self.data.json()
        return self.json


class DataCiteProvider(Provider):
    """Retrieve DOI statistics from DataCite."""

    INDEX_URL = 'https://stats.datacite.org/stats/resolution-report/index.html'

    def __init__(self, prefix):
        """
        Provider DataCite initialization.
        """
        if not prefix:
            raise ValueError("prefix can't be empty")

        self.prefix = prefix
        self.data = None

    def collect(self):
        """Collect DOI statistics from DataCite."""
        return self.data
