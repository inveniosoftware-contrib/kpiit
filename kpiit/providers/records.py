# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records providers."""

import requests

from ..metrics.records import RecordsMetric
from ..providers import URLProvider


class RecordsURLProvider(URLProvider):
    """
    Provider that retrieves records data from a URL.

    Supports retrieving # of records from zenodo, cds videos and opendata.
    """

    def __init__(self, url):
        """Records URL provider initialization."""
        super().__init__(RecordsMetric(), url)

    def collect(self):
        """Collect # of records from URL and returns the updated metrics."""
        req = requests.get(self.url)
        data = req.json()
        record_count = data['hits']['total']

        self.metric.update(record_count)

        return self.metric
