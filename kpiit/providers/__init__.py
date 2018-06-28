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


class JSONURLProvider(Provider):
    """Basic URL-based provider."""

    def __init__(self, url):
        """URL provider initialization."""
        self.url = url

    def collect(self):
        """Get URL request."""
        self.data = requests.get(self.url)
        self.json = self.data.json()
