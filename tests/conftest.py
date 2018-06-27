# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Common pytest fixtures and plugins."""

import pytest

from kpiit.metrics.records import RecordsMetric


@pytest.fixture
def records_metric():
    """Fixture for records metric."""
    return RecordsMetric()
