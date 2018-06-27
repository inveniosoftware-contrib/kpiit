# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Publisher for CERN's Grafana instance."""

import json
from datetime import datetime

from ..models import Publisher


class CERNMonitPublisher(Publisher):
    """Publish metrics to CERN monit grafana instance."""

    def build_kpi_message(self, serviceid, service_status, **data):
        """Build a KPI message (JSON) that will be sent to monit."""
        timestamp = None  # get_timestamp_now()
        availabilityinfo = None
        availabilitydesc = None

        return json.dumps({
            'producer': 'kpi',
            'type': 'service',
            'serviceid': serviceid,
            'service_status': service_status,
            'type_prefix': 'raw',
            'timestamp': timestamp,
            'availabilityinfo': availabilityinfo,
            'availabilitydesc': availabilitydesc,
            **data
        })

    def publish(self, metrics):
        """Publish KPIs to the grafana instance."""
        raise NotImplementedError()

    @staticmethod
    def get_timestamp():
        """Get timestamp in milliseconds without decimals."""
        return round(datetime.utcnow().timestamp() * 1000)
