# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base publisher."""

import json

import requests
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class BasePublisher(object):
    """Abstract class for publishing metrics."""

    def build_message(self, metrics):
        """Build message to be published."""
        raise NotImplementedError()

    def publish(self, metrics):
        """Publish metrics."""
        self.build_message(metrics)

    def send(cls, url, document, production):
        """Send data to url with a GET request."""
        logger.debug('sending document to: %s' % url)
        logger.debug('document: %s' % json.dumps(document))

        return requests.post(
            url,
            data=json.dumps(document),
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )
