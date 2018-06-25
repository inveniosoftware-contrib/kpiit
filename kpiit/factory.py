# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery application."""

import os

from celery import Celery


def create_app(config_module=None, **kwargs):
    """Celery application factory.

    Loading order of configuration (next one overrides previous):

        1. Config module.
        2. Keyword argument

    :param config_module: Import path to configuration module.
    :param kwargs: Runtime configuration.
    """
    app = Celery()

    # Initialize configuration.
    if config_module:
        app.config_from_object(config_module, force=True)

    # # Load keyword arguments configuration.
    app.conf.update(**kwargs)

    return app
