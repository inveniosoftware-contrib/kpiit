# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Generic providers"""

from ..models import Provider


class FileProvider(Provider):
    def __init__(self, metric, filename):
        super().__init__(metric)
        self.filename = filename


class URLProvider(Provider):
    def __init__(self, metric, url):
        super().__init__(metric)
        self.url = url
