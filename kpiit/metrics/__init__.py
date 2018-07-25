# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metrics module."""

import os

from kpiit import Service

from .doi import DOIMetric
from .records import RecordsMetric
from .support_tickets import DummySupportTicketsMetric, SupportTicketsMetric
from .visits import DummyVisitsMetric
from .uptime import UptimeMetric
from ..providers import DataCiteProvider, JSONURLProvider, DummyProvider
from ..providers.snow import ServiceNowProvider
from ..providers.uptime_robot import UptimeRobotProvider


# Dummy metric

dummy_visits_metric = DummyVisitsMetric()

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

zenodo_doi_metric = DOIMetric(provider=DataCiteProvider('10.5281'))

cds_videos_doi_metric = DOIMetric(provider=DataCiteProvider('10.17181'))

cod_doi_metric = DOIMetric(provider=DataCiteProvider('10.7483'))

# Uptime metrics

website_uptime_metric = UptimeMetric(
    name='web',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('UPTIME_WEBSITE_API_KEY'),
        'Website'
    )
)

search_uptime_metric = UptimeMetric(
    name='search',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('UPTIME_SEARCH_API_KEY'),
        'Search'
    )
)

files_uptime_metric = UptimeMetric(
    name='files',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('UPTIME_FILES_API_KEY'),
        'Files upload/download'
    )
)

# Support tickets metrics

dummy_support_metric = DummySupportTicketsMetric(
    name='dummy_support',
    provider=DummyProvider()
)

cds_support_metric = SupportTicketsMetric(
    name='cds_support',
    provider=ServiceNowProvider(Service.CDS)
)

cds_videos_support_metric = SupportTicketsMetric(
    name='cds_videos_support',
    provider=ServiceNowProvider(Service.CDS_VIDEOS)
)

zenodo_support_metric = SupportTicketsMetric(
    name='zenodo_support',
    provider=ServiceNowProvider(Service.ZENODO)
)
