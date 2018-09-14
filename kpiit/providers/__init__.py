# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Providers module."""


class BaseProvider(object):
    """Abstract class for collecting data."""

    def collect(self):
        """Collect metrics data."""
        raise NotImplementedError()
