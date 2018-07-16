# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records metric."""

from ..models import Metric


class DOIMetric(Metric):
    """Metric for DOI."""

    FIELDS = [
        'total_attempts', 'successful', 'failed', 'unique_doi_total',
        'unique_doi_successful', 'unique_doi_failed'
    ]

    def __init__(self, name, provider, fields=FIELDS):
        """DOI metric initialization."""
        super().__init__(name, provider, fields)

    def collect_done(self, data):
        """Process collected data."""
        for key, value in data.items():
            setattr(self, key, int(value))
