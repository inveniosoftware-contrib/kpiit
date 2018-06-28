# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Zenodo tests."""

import os

import pytest


def test_zenodo_records(zenodo_records):
    zenodo_records.collect()

    assert zenodo_records.values[zenodo_records.name]['num_records'] == 406804
