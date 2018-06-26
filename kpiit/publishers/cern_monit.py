# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPI Models"""

from datetime import datetime

from ..models import Publisher


class CERNMonitPublisher(Publisher):
    """Publish metrics to CERN monit grafana instance."""

    def publish(self, metrics):
        pass

    @staticmethod
    def get_timestamp_now():
        return round(datetime.utcnow().timestamp() * 1000)