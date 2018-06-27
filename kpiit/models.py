# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPI models."""

import requests


class Metric(object):
    """Abstract KPI metric class."""

    def __init__(self, name):
        """Metric initialization."""
        self.name = name

    def update(self, *args, **kwargs):
        """Update metric data."""
        raise NotImplementedError()


class MetricInstance(object):
    """Instance of a metric."""

    def __init__(self, provider):
        """Metric instance initialization."""
        self.provider = provider
        self.metric = provider.metric

    def collect(self):
        """Collect metrics from the provider."""
        return self.provider.collect()


class Provider(object):
    """Abstract class for collecting data."""

    def __init__(self, metric):
        """Provider initialization."""
        self.metric = metric

    def collect(self):
        """Collect metrics data."""
        raise NotImplementedError()


class Publisher(object):
    """Abstract class for publishing metrics."""

    def publish(self, metrics):
        """Publish metrics."""
        raise NotImplementedError()
