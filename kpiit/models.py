# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPI Models"""

import requests


class Metric(object):
    def __init__(self, name):
        self.name = name

    def update(self, *args, **kwargs):
        raise NotImplementedError()


class MetricInstance(object):
    def __init__(self, provider):
        self.provider = provider
        self.metric = provider.metric

    def collect(self):
        return self.provider.collect()


class Provider(object):
    def __init__(self, metric):
        self.metric = metric

    def collect(self):
        raise NotImplementedError()


class FileProvider(Provider):
    def __init__(self, metric, filename):
        super().__init__(metric)
        self.filename = filename


class URLProvider(Provider):
    def __init__(self, metric, url):
        super().__init__(metric)
        self.url = url


class RecordsMetric(Metric):
    def __init__(self):
        super().__init__('num_records')

    def update(self, count):
        self.__count = count

    @property
    def count(self):
        return self.__count


class RecordsURLProvider(URLProvider):
    """Provider that retrieves records data from a URL."""

    def __init__(self, url):
        super().__init__(RecordsMetric(), url)

    def collect(self):
        """Collect num_records from given URL."""
        req = requests.get(self.url)
        data = req.json()
        record_count = data['hits']['total']

        self.metric.update(record_count)

        return record_count


class ZenodoRecordsMetric(MetricInstance):
    ZENODO_RECORDS_URL = 'https://zenodo.org/api/records/?all_versions'

    def __init__(self):
        super().__init__(RecordsURLProvider(ZenodoRecordsMetric.ZENODO_RECORDS_URL))
