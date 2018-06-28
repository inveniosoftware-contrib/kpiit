# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records metric."""

from ..models import Metric


class RecordsMetric(Metric):
    """Metric for number of records."""

    def __init__(self, name='records'):
        """Records metric initialization."""
        super().__init__(name)

    @property
    def count(self):
        """Records count getter."""
        return self.values[self.name].get('num_records', None)

    @count.setter
    def count(self, value):
        """Records count setter."""
        return super().update(num_records=value)
