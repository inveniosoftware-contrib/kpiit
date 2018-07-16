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

    FIELDS = ['doi_success', 'doi_failed']

    def __init__(self, provider, fields=FIELDS):
        """DOI metric initialization."""
        super().__init__('doi', provider, fields)

    def collect_done(self, data):
        """Process collected data."""
        for key, value in data.items():
            setattr(self, key, int(value))
