# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metrics module."""

import os

from dotenv import load_dotenv

from .doi import DOIMetric
from .records import RecordsMetric
from .uptime import UptimeMetric
from ..providers import DataCiteProvider, JSONURLProvider
from ..providers.uptime_robot import UptimeRobotProvider

# Load .env config file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '..', '..', '.env'))


# Record metrics

zenodo_records_metric = RecordsMetric(
    name='zenodo_records',
    provider=JSONURLProvider(
        'https://zenodo.org/api/records/?all_versions'
    )
)

cds_videos_records_metric = RecordsMetric(
    name='cds_videos_records',
    provider=JSONURLProvider(
        'https://videos.cern.ch/api/records/'
    )
)

cod_records_metric = RecordsMetric(
    name='cod_records',
    provider=JSONURLProvider(
        'http://opendata.cern.ch/api/records/'
    )
)

# DOI metrics

doi_attrs = ('doi_total', 'doi_2018', 'doi_2017')

zenodo_doi_metric = DOIMetric(
    name='zenodo_doi',
    provider=DataCiteProvider(
        'CERN - CERN - European Organization for Nuclear Research',
        'CERN.ZENODO',
        doi_attrs
    )
)

cds_videos_doi_metric = DOIMetric(
    name='cds_videos_doi',
    provider=DataCiteProvider(
        'CERN - CERN - European Organization for Nuclear Research',
        'CERN.CDS',
        doi_attrs
    )
)

cod_doi_metric = DOIMetric(
    name='opendata_doi',
    provider=DataCiteProvider(
        'CERN - CERN - European Organization for Nuclear Research',
        'CERN.OPENDATA',
        doi_attrs
    )
)

# Uptime metrics

website_uptime_metric = UptimeMetric(
    name='website_uptime',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('UPTIME_WEBSITE_API_KEY'),
        os.getenv('UPTIME_WEBSITE_NAME')
    )
)

search_uptime_metric = UptimeMetric(
    name='search_uptime',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('UPTIME_SEARCH_API_KEY'),
        os.getenv('UPTIME_SEARCH_NAME')
    )
)

files_uptime_metric = UptimeMetric(
    name='files_uptime',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('UPTIME_FILES_API_KEY'),
        os.getenv('UPTIME_FILES_NAME')
    )
)
