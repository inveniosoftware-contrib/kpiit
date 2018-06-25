# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Simple test of version import."""

import os

import pytest

from kpiit.app import create_app


def test_app_conf_env(monkeypatch):
    """Test environment variable configuration."""
    app = create_app(
        config_module='kpiit.celeryconfig',
    )
    assert app.conf.broker_url == 'redis://localhost:6379/0'
    app = create_app(
        config_module='kpiit.celeryconfig',
        broker_url='redis://localhost:6379/3'
    )
    assert app.conf.broker_url == 'redis://localhost:6379/3'
