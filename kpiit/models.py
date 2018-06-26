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
        pass

    def update(self, data):
        raise NotImplementedError()


class MetricInstance(object):
    def __init__(self, provider, metric):
        self.provider = provider
        self.metric = metric


class Provider(object):
    def __init__(self, name):
        self.name = name

    def collect(self):
        raise NotImplementedError()


class FileProvider(Provider):
    def __init__(self, filename):
        self.filename = filename


class URLProvider(Provider):
    def __init__(self, url):
        self.url = url


class RecordsMetric(Metric):
    def __init__(self):
        super('num_records')

    def update(self, count):
        self.__count = count

    @property
    def count(self):
        return self.__count


class ZenodoRecordsProvider(URLProvider):
    def __init__(self):
        super('zenodo', RecordsMetric())

    def collect(self):
        """Collect num_records from Zenodo."""
        req = requests.get(url)
        data = req.json()
        record_count = data['hits']['total']
