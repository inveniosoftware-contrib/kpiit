# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery application."""

import os

from celery import Celery

from .factory import create_app

#: Celery application instance.
app = create_app(config_module='kpiit.celeryconfig')
