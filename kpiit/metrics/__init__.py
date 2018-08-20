# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metrics module."""

from kpiit.metrics.base import BaseMetric
from kpiit.metrics.records import RecordsMetric
from kpiit.metrics.uptime import UptimeMetric
from kpiit.providers import DataCiteProvider, JSONURLProvider, DummyProvider
from kpiit.providers.piwik import PiwikProvider
from kpiit.providers.snow import ServiceNowProvider
from kpiit.providers.uptime_robot import UptimeRobotProvider


class Metric(BaseMetric):
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
    return Metric(
        name='doi',
        provider=DataCiteProvider(prefix),
        fields=['doi_success', 'doi_failed']
    )


def uptime(name, url, api_key, monitor):
    """Get uptime metric instance."""
    return UptimeMetric(
        name=name,
        provider=UptimeRobotProvider(url, api_key, monitor)
    )


def support(name, service=None, dummy=False):
    """Get support ticket metric instance."""
    fields = [
        'support_requests',
        'support_incidents',
        'incident_stc',
        'reassignment_count'
    ]

    if dummy:
        provider = DummyProvider(fields)
    else:
        provider = ServiceNowProvider(service)

    return Metric(name=name, provider=provider, fields=fields)


def visits(name, site_id=None, dummy=False):
    """Get visits metric instance.

    Create a dummy instance if site_id is None.
    """
    fields = ['visits', 'visits_unique']

    if dummy:
        provider = DummyProvider(fields)
    else:
        provider = PiwikProvider(site_id=site_id)

    return Metric(name=name, provider=provider, fields=fields)
