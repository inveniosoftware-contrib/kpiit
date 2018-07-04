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

from ..models import Provider


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

    URLS = dict(
        doi_total='https://search.datacite.org/list/generic?fq=allocator_facet:%22{allocator}%22&&facet.field=datacentre_facet',
        doi_2017='https://search.datacite.org/list/generic?fq=allocator_facet:%22{allocator}%22&&fq=minted:[NOW/YEAR-1YEARS/YEAR+TO+NOW/YEAR]&facet.field=datacentre_facet',
        doi_2018='https://search.datacite.org/list/generic?fq=allocator_facet:%22{allocator}%22&&fq=minted:[NOW/YEAR+TO+*]&facet.field=datacentre_facet',
        doi_last_30days='https://search.datacite.org/list/generic?fq=allocator_facet:%22{allocator}%22&&fq=minted:[NOW-30DAYS/DAY+TO+*]&facet.field=datacentre_facet',
        doi_searchable='https://search.datacite.org/list/generic?fq=allocator_facet:%22{allocator}%22&&fq=has_metadata:true&fq=is_active:true&facet.field=datacentre_facet',
        doi_hidden='https://search.datacite.org/list/generic?fq=allocator_facet:%22{allocator}%22&&fq=is_active:false&facet.field=datacentre_facet',
        doi_missing='https://search.datacite.org/list/generic?fq=allocator_facet:%22{allocator}%22&&fq=has_metadata:false&facet.field=datacentre_facet'
    )

    def __init__(self, allocator, names):
        """
        DataCite provider initialization.

        :param allocator: Name of the allocator
        :param names: List of data center names (e.g. ['CERN.CDS', 'CERN.ZENODO'])
        """
        if not allocator:
            raise ValueError("allocator can't be empty")
        if not names:
            raise ValueError("names can't be empty")

        self.allocator = allocator
        self.names = names

        # Generate URLs
        url_templates = DataCiteProvider.URLS
        self.urls = {}
        for key in ('doi_total', ):
            template = url_templates[key]
            url = template.format(allocator=urllib.parse.quote_plus(self.allocator))
            self.urls[key] = url
    
        # Compile regular expressions
        re_value = r'{}[^\;]+\;(?P<value>[^\;]+)\;'
        self.regex = {name: re.compile(re_value.format(name)) for name in names}

    def collect(self):
        """Collect DOI statistics from DataCite."""
        data = [requests.get(url).text for key, url in self.urls.items()]
        return data

