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


class CERNGrafanaPublisher(Publisher):
    """Publish metrics to CERN monit grafana instance."""

    def publish(self, metrics):
        """Publish KPIs to the grafana instance."""
        status = 'available'  # TODO: Implement proper status checking
        msg = CERNGrafanaPublisher.build_message(SERVICE_ID, status, metrics)

        return msg

    @classmethod
    def build_message(cls, serviceid, service_status, metrics, **kwargs):
        """Build a KPI message (JSON) that will be sent to monit."""
        data = cls.metrics_to_dict(metrics)
        timestamp = cls.get_timestamp()

        producer = kwargs.get('producer', 'kpi')
        type_ = kwargs.get('type', 'service')
        type_prefix = kwargs.get('type_prefix', 'raw')
        availabilityinfo = kwargs.get('availabilityinfo', None)
        availabilitydesc = kwargs.get('availabilitydesc', None)

        return json.dumps({
            'producer': producer,
            'type': type_,
            'serviceid': serviceid,
            'service_status': service_status,
            'type_prefix': type_prefix,
            'timestamp': timestamp,
            'availabilityinfo': availabilityinfo,
            'availabilitydesc': availabilitydesc,
            **data
        })

    @staticmethod
    def get_timestamp():
        """Get timestamp in milliseconds without decimals."""
        return round(datetime.utcnow().timestamp() * 1000)

    @staticmethod
    def metrics_to_dict(metrics):
        """Convert an array of metrics to a dict."""
        data = {}
        for metric in metrics:
            for name, values in metric.values.items():
                for key, value in values.items():
                    unique_key = '{}_{}'.format(name, key)
                    data[unique_key] = value
        return data
