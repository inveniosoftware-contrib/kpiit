# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metric tests."""

import os

import pytest


def test_json_publisher(json_publisher, records_metric):
    assert not os.path.exists(json_publisher.filename)

    metrics = [records_metric]

    json_publisher.publish(metrics)
    assert os.path.exists(json_publisher.filename)
