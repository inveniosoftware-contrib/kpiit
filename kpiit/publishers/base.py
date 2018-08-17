# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base publisher."""


class BasePublisher(object):
    """Abstract class for publishing metrics."""

    def build_message(self, metrics):
        """Build message to be published."""
        raise NotImplementedError()

    def publish(self, metrics):
        """Publish metrics."""
        self.build_message(metrics)
