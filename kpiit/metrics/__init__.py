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
from .uptime import UptimeMetric
from ..models import Metric
from ..providers import DataCiteProvider, JSONURLProvider, DummyProvider
from ..providers.piwik import PiwikProvider
from ..providers.snow import ServiceNowProvider
from ..providers.uptime_robot import UptimeRobotProvider


class GenericMetric(Metric):
    """Generic metric class."""

    def __init__(self, name, provider, fields):
        """Generic metric initializer."""
        super().__init__(name, provider, fields=fields)

    def collect_done(self, data):
        """Process collected data."""
        for key, value in data.items():
            setattr(self, key, self.clean_value(value))


def records(name, url):
    """Get a records metric instance."""
    return RecordsMetric(name=name, provider=JSONURLProvider(url))


def doi(prefix):
    """Get a DOI metric instance."""
    return DOIMetric(provider=DataCiteProvider(prefix))


def uptime(name, url, api_key, monitor):
    """Get uptime metric instance."""
    return UptimeMetric(
        name=name,
        provider=UptimeRobotProvider(url, api_key, monitor)
    )


def support(name, service=None, dummy=False):
    """Get support ticket metric instance."""
    if dummy:
        provider = DummyProvider(SupportTicketsMetric.FIELDS)
    else:
        provider = ServiceNowProvider(service)

    return SupportTicketsMetric(name=name, provider=provider)


def visits(name, site_id=None, dummy=False):
    """Get visits metric instance.

    Create a dummy instance if site_id is None.
    """
    fields = ['visits', 'visits_unique']

    if dummy:
        provider = DummyProvider(fields)
    else:
        provider = PiwikProvider(site_id=site_id)
    return GenericMetric(
        name=name,
        provider=DummyProvider(fields),
        fields=fields
    )
