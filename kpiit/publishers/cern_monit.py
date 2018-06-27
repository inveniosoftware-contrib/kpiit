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

SERVICE_ID = 'testserviceid'


class CERNMonitPublisher(Publisher):
    """Publish metrics to CERN monit grafana instance."""

    def build_kpi_message(self, serviceid, service_status, metrics):
        """Build a KPI message (JSON) that will be sent to monit."""
        data = CERNMonitPublisher.metrics_to_dict(metrics)
        timestamp = CERNMonitPublisher.get_timestamp()
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
        status = 'available'  # TODO: Implement proper status checking
        msg = self.build_kpi_message(SERVICE_ID, status, metrics)

        return msg

    @staticmethod
    def get_timestamp():
        """Get timestamp in milliseconds without decimals."""
        return round(datetime.utcnow().timestamp() * 1000)

    @staticmethod
    def metrics_to_dict(metrics):
        """Convert an array of metrics to a dict."""
        data = {}
        for metric in metrics:
            data[metric.name] = metric.value
        return data
