# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Generic providers."""

import json
import requests

from ..models import Provider


class FileProvider(Provider):
    """Basic file-based provider."""

    def __init__(self, metric, filename):
        """File provider initialization."""
        super().__init__(metric)
        self.filename = filename

    def collect(self):
        """Collect data in file."""
        with open(self.filename, 'r') as f:
            self.data = f.read()
            self.json = json.loads(self.data)


class URLProvider(Provider):
    """Basic URL-based provider."""

    def __init__(self, metric, url):
        """URL provider initialization."""
        super().__init__(metric)
        self.url = url

    def collect(self):
        """Get URL request."""
        self.data = requests.get(self.url)
        self.json = self.data.json()

        return self.metric
