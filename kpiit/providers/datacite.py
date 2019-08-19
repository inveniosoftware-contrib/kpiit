# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Uptime Robot provider."""

import requests
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from kpiit.config import config
from kpiit.providers import BaseProvider

logger = get_task_logger(__name__)


class DataCiteProvider(BaseProvider):
    """Retrieve DOI statistics from DataCite."""

    def __init__(self, prefix):
        """Provider DataCite initialization."""
        if not prefix:
            raise ValueError("prefix can't be empty")

        self.prefix = prefix
        self.data = None

    def load_index_data(self, url):
        """Download DOI index HTML data."""
        resp = requests.get(url).text
        resp.raise_for_status()
        return resp

    def load_stats_data(self, url):
        """Download DOI stats HTML data."""
        return requests.get(url).text

    def collect(self):
        """Collect DOI statistics from DataCite."""
        index_url = config['providers']['data_cite']['index_url']

        html_code = self.load_index_data(index_url)

        html = BeautifulSoup(html_code, 'html.parser')
        links = html.find_all('a')[-1]

        stats_url = '{base}{file}'.format(
            base=config['providers']['data_cite']['stats_url'],
            file=links.get('href')
        )
        stats_data = self.load_stats_data(stats_url)
        stats = BeautifulSoup(stats_data, 'html.parser')

        for tr in stats.find_all('tr'):
            a = tr.find('a')
            if a and a.get_text() == self.prefix:
                tds = tr.find_all('td')
                self.data = dict(
                    doi_success=tds[3].get_text(),
                    doi_failed=tds[4].get_text(),
                )
                return self.data
