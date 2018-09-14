# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility function tests."""

import json

import pytest
from tests.conftest import records_collect

from kpiit.metrics.records import RecordsMetric
from kpiit.tasks import collect_metrics, publish_metrics


def test_empty_collect_metrics(celery_app):
    pass
