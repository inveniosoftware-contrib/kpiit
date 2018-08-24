# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Dummy provider module."""

from celery.utils.log import get_task_logger

from kpiit.providers import BaseProvider

logger = get_task_logger(__name__)


class DummyProvider(BaseProvider):
    """Dummy provider."""

    def __init__(self, fields):
        """Dummy provider initialization."""
        self.fields = fields

    def collect(self):
        """Get dummy data."""
        return {field: None for field in self.fields}
