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

    def collect(self):
        """Get URL request."""
        self.data = requests.get(self.url)
        self.json = self.data.json()


class DataCiteProvider(Provider):
    """Retrieve DOI statistics from DataCite."""

    BASE_URL = 'https://search.datacite.org/list/generic?fq=allocator_facet:'

    ATTRS = dict(
        doi_total='',
        doi_2017='&fq=minted:[NOW/YEAR-1YEARS/YEAR+TO+NOW/YEAR]',
        doi_2018='&fq=minted:[NOW/YEAR+TO+*]',
        doi_last_30days='&fq=minted:[NOW-30DAYS/DAY+TO+*]',
        doi_searchable='&fq=has_metadata:true&fq=is_active:true',
        doi_hidden='&fq=is_active:false',
        doi_missing='&fq=has_metadata:false'
    )
    SUFFIX_URL = '&facet.field=datacentre_facet'

    def __init__(self, allocator, name, attrs=('doi_total', )):
        """
        Provider DataCite initialization.

        :param allocator: Name of the allocator
        :param name: Name of data center
        """
        if not allocator:
            raise ValueError("allocator can't be empty")
        if not name:
            raise ValueError("name can't be empty")

        self.allocator = allocator
        self.name = name
        self.attrs = attrs

        # Generate URLs
        base = DataCiteProvider.BASE_URL
        suffix = DataCiteProvider.SUFFIX_URL
        self.urls = {}
        for key in self.attrs:
            url = '{base}%22{allocator}%22&{attr}&{suffix}'.format(
                base=base,
                allocator=urllib.parse.quote_plus(self.allocator),
                attr=DataCiteProvider.ATTRS[key],
                suffix=suffix
            )
            self.urls[key] = url

        # Compile regular expressions to get the values from the text
        re_value = r'{}[^\;]+\;(?P<value>[^\;]+)\;'
        self.regex = re.compile(re_value.format(name))

    def collect(self):
        """Collect DOI statistics from DataCite."""
        data = {key: requests.get(url).text for key, url in self.urls.items()}
        self.values = {attr: None for attr in self.attrs}
        for key, value in data.items():
            m = self.regex.search(value)
            if m:
                self.values[key] = int(m.group('value').strip())
        return self.values
