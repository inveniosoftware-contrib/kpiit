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


class DummyProvider(Provider):
    """Dummy provider."""

    def collect(self):
        """Get dummy data."""
        pass


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
        self.data = requests.get(self.url, verify=False)
        self.json = self.data.json()
        return self.json


class DataCiteProvider(Provider):
    """Retrieve DOI statistics from DataCite."""

    INDEX_URL = 'https://stats.datacite.org/stats/resolution-report/index.html'
    STATS_URL = 'https://stats.datacite.org/stats/resolution-report/'

    def __init__(self, prefix):
        """Provider DataCite initialization."""
        if not prefix:
            raise ValueError("prefix can't be empty")

        self.prefix = prefix
        self.data = None

    def load_index_data(self, url):
        """Download DOI index HTML data."""
        return requests.get(url).text

    def load_stats_data(self, url):
        """Download DOI stats HTML data."""
        return requests.get(url).text

    def collect(self):
        """Collect DOI statistics from DataCite."""
        html_code = self.load_index_data(self.INDEX_URL)

        html = BeautifulSoup(html_code, 'html.parser')
        links = html.find_all('a')[-1]

        stats_url = '{base}{file}'.format(
            base=self.STATS_URL,
            file=links.get('href')
        )
        stats_data = self.load_stats_data(stats_url)
        stats = BeautifulSoup(stats_data, 'html.parser')

        for tr in stats.find_all('tr'):
            a = tr.find('a')
            if a and a.get_text() == self.prefix:
                tds = tr.find_all('td')
                self.data = dict(
                    # total_attempts=tds[2].get_text(),
                    doi_success=tds[3].get_text(),
                    doi_failed=tds[4].get_text(),
                    # unique_doi_total=tds[5].get_text(),
                    # unique_doi_successful=tds[6].get_text(),
                    # unique_doi_failed=tds[7].get_text()
                )
                return self.data
        return None
