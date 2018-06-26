# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPI Metrics"""

from ..models import Metric


class RecordsMetric(Metric):
    def __init__(self):
        super().__init__('num_records')

    def update(self, count):
        self.__count = count

    @property
    def count(self):
        return self.__count
