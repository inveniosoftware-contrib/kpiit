# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPI models."""


class Metric(object):
    """Abstract KPI metric class."""

    def __init__(self, name, provider, fields):
        """Metric initialization."""
        if not name:
            raise ValueError("name can't be empty")
        if not isinstance(name, str):
            raise TypeError("name needs to be a string")
        if not fields:
            raise ValueError("fields can't be empty")

        self.name = name
        self.provider = provider

        self.fields = fields
        for field in fields:
            self.__dict__[field] = None

    def collect(self):
        """Collect metrics from the provider."""
        data = self.provider.collect()
        self.collect_done(data)

    def collect_done(self, data):
        """Process collected data."""
        raise NotImplementedError()

    def value(self, key):
        """Get metric value."""
        return self.__dict__[key]

    def update(self, **kwargs):
        """Update metric value."""
        for key, value in kwargs.items():
            if key not in self.__dict__:
                raise AttributeError
            self.__dict__[key] = value

    @property
    def values(self):
        """Get values."""
        return {
            self.name: {field: self.value(field) for field in self.fields}
        }

    def __repr__(self):
        """Metric representation."""
        pairs = [', {}={}'.format(key, self.value(key))
                 for key in self.fields]

        return '{clsname}("{name}"{value_pairs})'.format(
            clsname=self.__class__.__name__,
            name=self.name,
            value_pairs=''.join(sorted(pairs))
        )

    @classmethod
    def clean_value(cls, value):
        """Clean string value and convert to appropriate type."""
        if value is None:
            return None
        elif isinstance(value, float) or isinstance(value, int):
            return value

        try:
            return float(value)
        except ValueError:
            pass

        try:
            return int(value)
        except ValueError:
            pass

        return str(value)


class Provider(object):
    """Abstract class for collecting data."""

    def collect(self):
        """Collect metrics data."""
        raise NotImplementedError()


class Publisher(object):
    """Abstract class for publishing metrics."""

    def build_message(self, metrics):
        """Build message to be published."""
        raise NotImplementedError()

    def publish(self, metrics):
        """Publish metrics."""
        self.build_message(metrics)
