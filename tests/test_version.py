# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Simple test of version import."""


def test_version():
    """Test version import."""
    from kpiit import __version__
    assert __version__
