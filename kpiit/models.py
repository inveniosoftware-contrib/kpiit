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


class Publisher(object):
    def publish(self, metrics):
        raise NotImplementedError()
