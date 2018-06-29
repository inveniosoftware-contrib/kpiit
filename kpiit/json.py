# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON encoders and decoders."""


import json

from .models import Metric


class MetricEncoder(json.JSONEncoder):
    """JSON encoder for metric insances."""

    def default(self, o):  # pylint: disable=E0202
        """JSON encode a metric instance."""
        if isinstance(o, Metric):
            _type = '{}.{}'.format(o.__module__, o.__class__.__name__)
            return {
                '_type': _type,
                'name': o.name,
                'values': {key: o.value(key) for key in o.fields},
                'provider': None  # TODO: add support for encoding provider
            }

        return super().default(o)
