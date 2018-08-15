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
from .support_tickets import SupportTicketsMetric
from .visits import VisitsMetric
from .uptime import UptimeMetric
from ..models import Metric
from ..providers import DataCiteProvider, JSONURLProvider, DummyProvider
from ..providers.piwik import PiwikProvider
from ..providers.snow import ServiceNowProvider
from ..providers.uptime_robot import UptimeRobotProvider


class DummyMetric(Metric):
    """Dummy metric class."""

    def __init__(self, name, provider, fields):
        """Dummy metric initializer."""
        super().__init__(name, provider, fields=fields)

    def collect_done(self, data):
        """Process collected data."""
        for key, value in data.items():
            setattr(self, key, self.clean_value(value))


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

zenodo_website_uptime_metric = UptimeMetric(
    name='web',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('ZENODO_UPTIME_WEBSITE_API_KEY'),
        'Website'
    )
)

zenodo_search_uptime_metric = UptimeMetric(
    name='search',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('ZENODO_UPTIME_SEARCH_API_KEY'),
        'Search'
    )
)

zenodo_files_uptime_metric = UptimeMetric(
    name='files',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('ZENODO_UPTIME_FILES_API_KEY'),
        'Files upload/download'
    )
)

cds_videos_website_uptime_metric = UptimeMetric(
    name='web',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('CDS_VIDEOS_UPTIME_WEBSITE_API_KEY'),
        'Website'
    )
)

cds_videos_search_uptime_metric = UptimeMetric(
    name='search',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('CDS_VIDEOS_UPTIME_SEARCH_API_KEY'),
        'Search'
    )
)

cds_videos_files_uptime_metric = UptimeMetric(
    name='files',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('CDS_VIDEOS_UPTIME_FILES_API_KEY'),
        'Files upload/download'
    )
)

cod_website_uptime_metric = UptimeMetric(
    name='web',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('COD_UPTIME_WEBSITE_API_KEY'),
        'Website'
    )
)

cod_search_uptime_metric = UptimeMetric(
    name='search',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('COD_UPTIME_SEARCH_API_KEY'),
        'Search'
    )
)

cod_files_uptime_metric = UptimeMetric(
    name='files',
    provider=UptimeRobotProvider(
        'https://api.uptimerobot.com/v2/',
        os.getenv('COD_UPTIME_FILES_API_KEY'),
        'Files upload/download'
    )
)

# Support tickets metrics

support_fields = SupportTicketsMetric.FIELDS

dummy_support_metric = DummyMetric(
    name='dummy_support',
    provider=DummyProvider(support_fields),
    fields=support_fields
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

# Dummy metric

visits_fields = VisitsMetric.FIELDS

dummy_visits_metric = DummyMetric(
    name='visits',
    provider=DummyProvider(visits_fields),
    fields=visits_fields
)

zenodo_visits_metric = VisitsMetric(
    name='zenodo_visits',
    provider=PiwikProvider(site_id=57)
)

cds_videos_visits_metric = DummyMetric(
    name='cds_videos_visits',
    provider=DummyProvider(visits_fields),
    fields=visits_fields
)

cod_visits_metric = DummyMetric(
    name='cod_visits',
    provider=DummyProvider(visits_fields),
    fields=visits_fields
)
