# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON encoders and decoders."""


import json

from celery.utils.log import get_task_logger

from kpiit.metrics.base import BaseMetric
from kpiit.util import load_target

logger = get_task_logger(__name__)


class MetricEncoder(json.JSONEncoder):
    """JSON encoder for metric insances."""

    def default(self, o):  # pylint: disable=E0202
        """JSON encode a metric instance."""
        if not isinstance(o, BaseMetric):
            # return json.JSONEncoder.default(self, o)
            raise TypeError('object is not a Metric type: %s' % o)

        _type = '{}.{}'.format(o.__module__, o.__class__.__name__)
        return {
            '_type': _type,
            'name': o.name,
            'fields': o.fields,
            'values': {key: o.value(key) for key in o.fields},
            'provider': None
        }


class MetricDecoder(json.JSONDecoder):
    """JSON decoder for metric instances."""

    def __init__(self, *args, **kwargs):
        """Metric decoder initialization."""
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):  # pylint: disable=E0202
        """Create a Metric instance from JSON data."""
        return MetricDecoder.json_to_metric(obj)

    @classmethod
    def json_to_metric(cls, obj):
        """Convert JSON object to Metric instance."""
        if '_type' not in obj:
            return obj

        fields = obj['fields'] if 'fields' in obj else None

        metric_class = load_target(obj['_type'])
        metric = metric_class(
            name=obj['name'],
            provider=obj['provider'],
            fields=fields
        )
        metric.update(**obj['values'])
        return metric


def metric_dumps(metric):
    """JSON encode a Metric instance."""
    return json.dumps(metric, cls=MetricEncoder)


def metric_loads(metric):
    """JSON decode a Metric instance."""
    return json.loads(metric, cls=MetricDecoder)
