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

    def __init__(self, name, provider, fields=None):
        """DOI metric initialization."""
        super().__init__(name, provider, fields or provider.attrs)

    def collect(self):
        """Collect data for this instance."""
        super().collect()

        for field in self.fields:
            setattr(self, field, self.provider.values[field])
