# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON publishers."""

import json

from celery.utils.log import get_task_logger

from ..publishers.cern import CERNPublisher

logger = get_task_logger(__name__)


class JSONFilePublisher(CERNPublisher):
    """Test class that manages publishing metrics to a JSON file."""

    def __init__(self, filename, type, **tags):
        """JSON file provider initialization."""
        super().__init__(type, **tags)
        self.filename = filename

    def publish(self, metrics):
        """Publish metrics to JSON file."""
        super().publish(metrics)

        with open(self.filename, 'w+') as f:
            f.write(json.dumps(self.data))
            logger.info('Saved output JSON to: {}'.format(self.filename))
