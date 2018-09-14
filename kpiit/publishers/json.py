# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON publishers."""

import json

from celery.utils.log import get_task_logger

from kpiit.publishers.cern import CERNPublisher

logger = get_task_logger(__name__)


class JSONFilePublisher(CERNPublisher):
    """Test class that manages publishing metrics to a JSON file."""

    def __init__(self, type, **tags):
        """JSON file provider initialization."""
        super().__init__(type, **tags)

        self.filename = None
        if 'doi_prefix' in tags:
            self.name = tags['doi_prefix']
        elif 'service' in tags:
            self.name = tags['service']
        else:
            self.name = type

    def publish(self, metrics):
        """Publish metrics to JSON file."""
        super().publish(metrics)

        self.filename = 'logs/{type}_{name}_{now}.json'.format(
            type=self.data['type'],
            name=self.name,
            now=self.get_timestamp()
        )

        with open(self.filename, 'w+') as f:
            f.write(json.dumps(self.data))
            logger.info('saved output JSON to: {}'.format(self.filename))
