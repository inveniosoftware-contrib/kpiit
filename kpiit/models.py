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
        self.__values = {}

    def update(self, **kwargs):
        """Update metric data."""
        for key, value in kwargs.items():
            self.__values[key] = value

    @property
    def values(self):
        """Get metric values."""
        return self.__values

    def __repr__(self):
        """Metric representation."""
        pairs = [', {}={}'.format(key, value)
                 for key, value in self.values.items()]

        return '{clsname}("{name}"{value_pairs})'.format(
            clsname=self.__class__.__name__,
            name=self.name,
            value_pairs=''.join(sorted(pairs))
        )


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
