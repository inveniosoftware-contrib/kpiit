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

    def __init__(self):
        """Records metric initialization."""
        super().__init__('num_records')
        self.__count = None

    def update(self, count):
        """Update records count."""
        self.__count = count

    @property
    def count(self):
        """Records count getter."""
        return self.__count

    def __repr__(self):
        """Records metric representation."""
        return 'RecordsMetric("{}", count={})'.format(self.name, self.count)
